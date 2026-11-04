"""Bounded inverse views of existing equations, with original-domain verification.

The polynomial converter uses only the already allowlisted AST, never symbolic
string evaluation. It solves after substituting all other numerical quantities.
"""

import ast
import math
from collections.abc import Callable
from fractions import Fraction
from typing import Any

from .contracts import (
    UNITS,
    Model,
    ModelError,
    Node,
    NumericalError,
    Port,
    Value,
    finite,
)
from .expressions import check_guard, evaluate

OUTPUT_BINDING = "__output__"
MAX_WORKING_DEGREE = 4
MAX_SOLVE_DEGREE = 2
MAX_COEFFICIENT_BITS = 4096
MAX_SEARCH_POINTS = 1000
MAX_BISECTION_ITERATIONS = 200
MAX_ITERATIVE_EVALUATIONS = 10000
RESIDUAL_REL_TOL = 1e-9
RESIDUAL_ABS_TOL = 1e-9
PROFILE = "rational-polynomial-degree-2-or-bounded-search/2"
Polynomial = tuple[Fraction, ...]


class SolveError(ModelError):
    """A classified inability to produce one admissible scalar solution."""

    def __init__(
        self,
        code: str,
        message: str,
        candidates: list[float] | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        """Preserve candidate roots and scope evidence without choosing an arbitrary branch."""
        super().__init__(message)
        self.diagnostic = {
            "code": code,
            "candidates": candidates or [],
            "evidence": evidence or {},
        }


def node_ports(node: Node, model: Model) -> tuple[dict[str, Port], Port]:
    """Describe a directional view without changing the source model or its admission."""
    if OUTPUT_BINDING in model.inputs:
        raise ModelError(f"{OUTPUT_BINDING} is reserved for a known original output.")
    if node.relation not in {"equal", "at_least"}:
        raise ModelError("Supported solve relations are equal and at_least.")
    if node.branch not in (None, "all"):
        raise ModelError("Supported branch selections are all or unset.")
    if node.solve_for is None:
        if node.relation != "equal":
            raise ModelError("A threshold relation needs an explicit solve target.")
        if node.branch is not None:
            raise ModelError("Branch inspection needs an explicit solve target.")
        return model.inputs, model.output
    if node.solve_for in model.families:
        raise ModelError("Cannot solve for an index family; families are forward-only.")
    if node.solve_for not in model.inputs:
        raise ModelError(
            "Solve target must be a declared model input, not a literal constant or invented symbol."
        )
    if (
        node.relation == "at_least"
        and model.inputs[node.solve_for].meaning != "period_count"
    ):
        raise SolveError(
            "unsupported_relation",
            "Threshold search currently requires an integer period-count target.",
        )
    inputs = {
        name: port for name, port in model.inputs.items() if name != node.solve_for
    }
    return {**inputs, OUTPUT_BINDING: model.output}, model.inputs[node.solve_for]


def trim(coefficients: Polynomial) -> Polynomial:
    """Canonicalize and bound exact rational polynomial coefficients."""
    result = list(coefficients)
    while len(result) > 1 and not result[-1]:
        result.pop()
    if len(result) - 1 > MAX_WORKING_DEGREE or any(
        max(abs(c.numerator).bit_length(), c.denominator.bit_length())
        > MAX_COEFFICIENT_BITS
        for c in result
    ):
        raise SolveError(
            "unsupported_complexity",
            "Inverse polynomial exceeds the declared degree/coefficient limits.",
        )
    return tuple(result)


def add(left: Polynomial, right: Polynomial, sign: int = 1) -> Polynomial:
    """Add or subtract bounded coefficient vectors in ascending degree order."""
    return trim(
        tuple(
            (left[i] if i < len(left) else Fraction(0))
            + sign * (right[i] if i < len(right) else Fraction(0))
            for i in range(max(len(left), len(right)))
        )
    )


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply coefficient vectors while enforcing the working-degree bound."""
    if len(left) + len(right) - 2 > MAX_WORKING_DEGREE:
        raise SolveError(
            "unsupported_degree", "Intermediate polynomial exceeds supported degree."
        )
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(tuple(result))


def rational(
    node: ast.AST, target: str, known: dict[str, float]
) -> tuple[Polynomial, Polynomial]:
    """Translate restricted arithmetic into numerator/denominator polynomials."""
    one = (Fraction(1),)
    if not any(
        isinstance(item, ast.Name) and item.id == target for item in ast.walk(node)
    ):
        return (Fraction(str(evaluate(node, known))),), one
    if isinstance(node, ast.Name) and node.id == target:
        return (Fraction(0), Fraction(1)), one
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        numerator, denominator = rational(node.operand, target, known)
        return (
            tuple(-c for c in numerator) if isinstance(node.op, ast.USub) else numerator
        ), denominator
    if not isinstance(node, ast.BinOp):
        raise SolveError(
            "unsupported_expression",
            "Inverse view requires supported scalar rational arithmetic.",
        )
    if isinstance(node.op, ast.Pow):
        if any(
            isinstance(item, ast.Name) and item.id == target
            for item in ast.walk(node.right)
        ):
            raise SolveError(
                "unsupported_expression",
                "Unknown exponents are not polynomial inversions; bounded search needs explicit finite guard bounds.",
            )
        exponent = evaluate(node.right, known)
        if not exponent.is_integer() or abs(exponent) > MAX_SOLVE_DEGREE:
            raise SolveError(
                "unsupported_degree",
                "Unknown-dependent powers must be integers of magnitude at most two.",
            )
        numerator, denominator = rational(node.left, target, known)
        if exponent < 0:
            numerator, denominator = denominator, numerator
        top: Polynomial = one
        bottom: Polynomial = one
        for _ in range(abs(int(exponent))):
            top, bottom = multiply(top, numerator), multiply(bottom, denominator)
        return top, bottom
    a, b = rational(node.left, target, known)
    c, d = rational(node.right, target, known)
    if isinstance(node.op, ast.Add):
        return add(multiply(a, d), multiply(c, b)), multiply(b, d)
    if isinstance(node.op, ast.Sub):
        return add(multiply(a, d), multiply(c, b), -1), multiply(b, d)
    if isinstance(node.op, ast.Mult):
        return multiply(a, c), multiply(b, d)
    if isinstance(node.op, ast.Div):
        return multiply(a, d), multiply(b, c)
    raise SolveError("unsupported_expression", "Unsupported inverse operator.")


def roots(coefficients: Polynomial) -> list[float]:
    """Solve linear/quadratic equations, distinguishing no solution from non-uniqueness."""
    coefficients = trim(coefficients)
    degree = len(coefficients) - 1
    if degree == 0:
        if coefficients[0] == 0:
            raise SolveError(
                "underdetermined",
                "This equation does not identify a unique value of the requested variable.",
            )
        return []
    if degree > MAX_SOLVE_DEGREE:
        raise SolveError(
            "unsupported_degree",
            "The substituted equation has degree greater than two.",
        )
    if degree == 1:
        return [coefficient_float(-coefficients[0] / coefficients[1])]
    c, b, a = coefficients
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return []
    if discriminant == 0:
        return [coefficient_float(-b / (2 * a))]
    # Stable quadratic formula avoids subtracting nearly equal floating values.
    af, bf, cf = (coefficient_float(value) for value in (a, b, c))
    q = -0.5 * bf - 0.5 * math.copysign(math.sqrt(coefficient_float(discriminant)), bf)
    if af == 0 or q == 0:
        raise SolveError(
            "numerical_limit",
            "Quadratic coefficients cannot be resolved safely at this precision.",
        )
    return [finite(q / af, "Quadratic root"), finite(cf / q, "Quadratic root")]


def coefficient_float(value: Fraction) -> float:
    """Reject coefficients outside binary64 rather than leaking arithmetic exceptions."""
    try:
        result = finite(float(value), "Polynomial coefficient")
        if value != 0 and result == 0:
            raise ModelError("A nonzero coefficient underflows binary64.")
        return result
    except (OverflowError, ModelError) as exc:
        raise SolveError(
            "numerical_limit",
            "Polynomial coefficients exceed the supported numerical range.",
        ) from exc


def integer_bounds(
    target: str, guards: tuple[ast.Compare, ...], known: dict[str, float]
) -> tuple[int, int]:
    """Find finite integer bounds from explicit original model guards, never a guessed horizon."""
    lower, upper = None, None
    for guard in guards:
        left, right, operation = guard.left, guard.comparators[0], guard.ops[0]
        if isinstance(right, ast.Name) and right.id == target:
            left, right = right, left
            inverse = {
                ast.Gt: ast.Lt,
                ast.GtE: ast.LtE,
                ast.Lt: ast.Gt,
                ast.LtE: ast.GtE,
                ast.Eq: ast.Eq,
            }
            operation = inverse[type(operation)]()
        if (
            not isinstance(left, ast.Name)
            or left.id != target
            or any(
                isinstance(item, ast.Name) and item.id == target
                for item in ast.walk(right)
            )
        ):
            continue
        bound = evaluate(right, known)
        if isinstance(operation, (ast.Gt, ast.GtE, ast.Eq)):
            candidate = (
                math.floor(bound) + 1
                if isinstance(operation, ast.Gt)
                else math.ceil(bound)
            )
            lower = max(lower, candidate) if lower is not None else candidate
        if isinstance(operation, (ast.Lt, ast.LtE, ast.Eq)):
            candidate = (
                math.ceil(bound) - 1
                if isinstance(operation, ast.Lt)
                else math.floor(bound)
            )
            upper = min(upper, candidate) if upper is not None else candidate
    if lower is None or upper is None:
        raise SolveError(
            "unbounded_search",
            "Integer inversion requires explicit lower and upper bounds in the model's guards.",
        )
    if lower > upper:
        raise SolveError(
            "invalid_domain", "The declared integer search interval is empty."
        )
    if upper - lower + 1 > MAX_SEARCH_POINTS:
        raise SolveError(
            "unsupported_complexity",
            "Declared integer search domain exceeds the evaluation limit.",
        )
    return lower, upper


def continuous_bounds(
    target: str, guards: tuple[ast.Compare, ...], known: dict[str, float]
) -> tuple[float, float]:
    """Find a finite continuous bracket from explicit original model guards, never a guessed horizon."""
    lower, upper = None, None
    for guard in guards:
        left, right, operation = guard.left, guard.comparators[0], guard.ops[0]
        if isinstance(right, ast.Name) and right.id == target:
            left, right = right, left
            inverse = {
                ast.Gt: ast.Lt,
                ast.GtE: ast.LtE,
                ast.Lt: ast.Gt,
                ast.LtE: ast.GtE,
                ast.Eq: ast.Eq,
            }
            operation = inverse[type(operation)]()
        if (
            not isinstance(left, ast.Name)
            or left.id != target
            or any(
                isinstance(item, ast.Name) and item.id == target
                for item in ast.walk(right)
            )
        ):
            continue
        bound = evaluate(right, known)
        if not math.isfinite(bound):
            raise SolveError(
                "unbounded_search",
                "Continuous inversion requires explicit finite lower and upper bounds in the model's guards.",
            )
        if isinstance(operation, (ast.Gt, ast.GtE, ast.Eq)):
            candidate = (
                math.nextafter(bound, math.inf)
                if isinstance(operation, ast.Gt)
                else bound
            )
            lower = max(lower, candidate) if lower is not None else candidate
        if isinstance(operation, (ast.Lt, ast.LtE, ast.Eq)):
            candidate = (
                math.nextafter(bound, -math.inf)
                if isinstance(operation, ast.Lt)
                else bound
            )
            upper = min(upper, candidate) if upper is not None else candidate
    if lower is None or upper is None:
        raise SolveError(
            "unbounded_search",
            "Continuous inversion requires explicit finite lower and upper bounds in the model's guards.",
        )
    if lower > upper:
        raise SolveError(
            "invalid_domain", "The declared continuous search interval is empty."
        )
    return lower, upper


def has_finite_bracket(
    target: str, guards: tuple[ast.Compare, ...], known: dict[str, float]
) -> bool:
    """Peek for an explicit finite bracket without disturbing the exact-method diagnostic."""
    try:
        continuous_bounds(target, guards, known)
    except SolveError:
        return False
    return True


def _iterative_matches(
    expression: ast.AST,
    guards: tuple[ast.Compare, ...],
    target: str,
    known: dict[str, float],
    expected: float,
    evidence: dict[str, Any],
    valid: Callable[[float], tuple[bool, float | None]],
) -> tuple[list[tuple[float, float]], list[float], dict[str, Any]]:
    """Scan an explicit finite bracket for sign changes, then bisect each one.

    Every proposed root is verified against the original equation, guards and
    residual tolerances through the caller-provided check; this search proposes.
    """
    lower, upper = continuous_bounds(target, guards, known)
    evidence.update(
        {
            "method": "scan-then-bisection",
            "domain": [lower, upper],
            "detection": (
                "Sign-changing crossings and on-sample hits only; "
                "sub-resolution gaps, guard-interrupted intervals "
                "and touching zeros may be missed."
            ),
        }
    )
    matches: list[tuple[float, float]] = []
    proposed: list[float] = []
    evaluations = 0

    def bisect(
        left: float, out_left: float, right: float, out_right: float
    ) -> float | None:
        """Bisect one sign-change interval; gaps abort the interval without a claim."""
        nonlocal evaluations
        best, best_output = left, out_left
        for _ in range(MAX_BISECTION_ITERATIONS):
            middle = (left + right) / 2
            if middle in (left, right):
                break
            try:
                output = evaluate(expression, {**known, target: middle})
            except NumericalError as exc:
                raise SolveError(
                    "numerical_limit",
                    "Cannot verify all required candidates within numerical limits; no root or earliest-crossing claim is made.",
                    evidence=evidence,
                ) from exc
            except ModelError:
                return None
            evaluations += 1
            if evaluations > MAX_ITERATIVE_EVALUATIONS:
                raise SolveError(
                    "unsupported_complexity",
                    "Bracketed search exceeds the evaluation limit.",
                    evidence=evidence,
                )
            if abs(output - expected) < abs(best_output - expected):
                best, best_output = middle, output
            if math.isclose(
                output, expected, rel_tol=RESIDUAL_REL_TOL, abs_tol=RESIDUAL_ABS_TOL
            ):
                return middle
            if (output < expected) == (out_left < expected):
                left, out_left = middle, output
            else:
                right = middle
        return best

    if lower == upper:
        accepted, output = valid(lower)
        evaluations += 1
        if (
            accepted
            and output is not None
            and math.isclose(
                output, expected, rel_tol=RESIDUAL_REL_TOL, abs_tol=RESIDUAL_ABS_TOL
            )
        ):
            proposed.append(lower)
            matches.append((lower, output))
        evidence.update(
            {"scan_intervals": 0, "scan_width": 0.0, "evaluations": evaluations}
        )
        return matches, proposed, evidence
    intervals = MAX_SEARCH_POINTS
    width = (upper - lower) / intervals
    samples: list[tuple[float, bool, float | None]] = []
    for index in range(intervals + 1):
        point = upper if index == intervals else lower + index * width
        accepted, output = valid(point)
        evaluations += 1
        samples.append((point, accepted, output))
    hits: set[float] = set()
    for point, accepted, output in samples:
        if (
            accepted
            and output is not None
            and math.isclose(
                output, expected, rel_tol=RESIDUAL_REL_TOL, abs_tol=RESIDUAL_ABS_TOL
            )
        ):
            hits.add(point)
            proposed.append(point)
            matches.append((point, output))
    for left, right in zip(samples, samples[1:]):
        if not left[1] or not right[1] or left[0] in hits or right[0] in hits:
            continue
        out_left, out_right = left[2], right[2]
        if out_left is None or out_right is None:
            continue
        if (out_left < expected) == (out_right < expected):
            continue
        root = bisect(left[0], out_left, right[0], out_right)
        if root is None:
            continue
        proposed.append(root)
        accepted, output = valid(root)
        evaluations += 1
        if (
            accepted
            and output is not None
            and math.isclose(
                output, expected, rel_tol=RESIDUAL_REL_TOL, abs_tol=RESIDUAL_ABS_TOL
            )
        ):
            matches.append((root, output))
    evidence.update(
        {"scan_intervals": intervals, "scan_width": width, "evaluations": evaluations}
    )
    return matches, proposed, evidence


def _verified_matches(
    model: Model,
    expression: ast.AST,
    guards: tuple[ast.Compare, ...],
    target: str,
    bindings: dict[str, float],
    relation: str,
) -> tuple[list[tuple[float, float]], list[float], dict[str, Any]]:
    """Verify every candidate against the original equation; the caller makes the terminal choice."""
    if model.families:
        raise SolveError(
            "unsupported_expression",
            "Indexed families are forward-only; inverse views are not supported.",
        )
    expected = bindings[OUTPUT_BINDING]
    known = {name: value for name, value in bindings.items() if name != OUTPUT_BINDING}
    port = model.inputs[target]
    evidence: dict[str, Any] = {
        "profile": PROFILE,
        "solve_for": target,
        "relation": relation,
        "target_output_canonical": expected,
        "output_declared_unit": model.output.unit,
        "solution_declared_unit": port.unit,
        "solution_unit_scale": UNITS[port.unit].scale,
    }

    def valid(candidate: float) -> tuple[bool, float | None]:
        """Check original guards, integer semantics, denominators and finite forward output."""
        numbers = {**known, target: candidate}
        try:
            Value(
                candidate / UNITS[port.unit].scale,
                port,
                "derived",
                "inverse verification",
            ).bind(port)
            if not all(check_guard(guard, numbers) for guard in guards):
                return False, None
            return True, evaluate(expression, numbers)
        except NumericalError as exc:
            raise SolveError(
                "numerical_limit",
                "Cannot verify all required candidates within numerical limits; no root or earliest-crossing claim is made.",
                evidence=evidence,
            ) from exc
        except ModelError:
            return False, None

    converted = None
    use_integer_search = relation == "at_least"
    use_iterative_search = False
    if not use_integer_search:
        try:
            converted = rational(expression, target, known)
        except SolveError as exc:
            if exc.diagnostic["code"] not in {
                "unsupported_expression",
                "unsupported_degree",
            }:
                raise
            if port.meaning == "period_count":
                use_integer_search = True
            elif has_finite_bracket(target, guards, known):
                use_iterative_search = True
            else:
                raise
    if use_integer_search:
        lower, upper = integer_bounds(target, guards, known)
        evidence.update(
            {"method": "bounded-integer-enumeration", "domain": [lower, upper]}
        )
        matches: list[tuple[float, float]] = []
        for step in range(lower, upper + 1):
            candidate = float(step)
            accepted, output = valid(candidate)
            if not accepted or output is None:
                continue
            if (relation == "at_least" and output >= expected) or (
                relation == "equal"
                and math.isclose(
                    output,
                    expected,
                    rel_tol=RESIDUAL_REL_TOL,
                    abs_tol=RESIDUAL_ABS_TOL,
                )
            ):
                if relation == "at_least":
                    evidence.update(
                        {
                            "original_output": output,
                            "evaluations": step - lower + 1,
                        }
                    )
                    return [(candidate, output)], [], evidence
                matches.append((candidate, output))
        if relation == "at_least":
            raise SolveError(
                "no_crossing_in_domain",
                f"No threshold crossing in the model's declared integer domain {lower}..{upper}; this is not a claim of no crossing outside it.",
                evidence=evidence,
            )
        evidence["evaluations"] = upper - lower + 1
        return matches, [], evidence
    if use_iterative_search:
        return _iterative_matches(
            expression, guards, target, known, expected, evidence, valid
        )
    assert converted is not None  # integer and iterative searches return above
    numerator, denominator = converted
    if denominator == (Fraction(0),):
        raise SolveError(
            "invalid_domain",
            "The original relationship is undefined for the supplied known values.",
        )
    equation = add(
        numerator,
        tuple(Fraction(str(expected)) * coefficient for coefficient in denominator),
        -1,
    )
    evidence.update(
        {
            "method": "rational-polynomial",
            "coefficients_ascending": [str(value) for value in equation],
        }
    )
    proposed = roots(equation)
    matches = []
    for candidate in proposed:
        accepted, output = valid(candidate)
        if not accepted or output is None:
            continue
        if math.isclose(
            output, expected, rel_tol=RESIDUAL_REL_TOL, abs_tol=RESIDUAL_ABS_TOL
        ):
            matches.append((candidate, output))
    evidence["candidate_roots"] = proposed
    return matches, proposed, evidence


def solve(
    model: Model,
    expression: ast.AST,
    guards: tuple[ast.Compare, ...],
    target: str,
    bindings: dict[str, float],
    relation: str,
) -> tuple[float, dict[str, Any]]:
    """Solve in canonical units and verify candidates against the unmodified original equation."""
    matches, _, evidence = _verified_matches(
        model, expression, guards, target, bindings, relation
    )
    if not matches:
        raise SolveError(
            "no_admissible_solution",
            "No candidate passed the original equation, guards, types and numerical checks at this precision.",
            evidence=evidence,
        )
    if len(matches) != 1:
        raise SolveError(
            "multiple_solutions",
            f"Multiple admissible solutions remain; set branch to 'all' to inspect all {len(matches)} candidates.",
            sorted(amount for amount, _ in matches),
            evidence,
        )
    candidate, _ = matches[0]
    known = {name: value for name, value in bindings.items() if name != OUTPUT_BINDING}
    evidence.update(
        {
            "original_output": evaluate(expression, {**known, target: candidate}),
            "residual_relative_tolerance": RESIDUAL_REL_TOL,
            "residual_absolute_tolerance": RESIDUAL_ABS_TOL,
        }
    )
    return candidate, evidence


def solve_all(
    model: Model,
    expression: ast.AST,
    guards: tuple[ast.Compare, ...],
    target: str,
    bindings: dict[str, float],
    relation: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return every verified root in ascending order; never select a branch silently."""
    matches, proposed, evidence = _verified_matches(
        model, expression, guards, target, bindings, relation
    )
    if not matches:
        raise SolveError(
            "no_admissible_solution",
            "No candidate passed the original equation, guards, types and numerical checks at this precision.",
            evidence=evidence,
        )
    ordered = sorted(matches, key=lambda pair: pair[0])
    admitted = {amount for amount, _ in ordered}
    excluded = sorted({float(candidate) for candidate in proposed} - admitted)
    evaluated = evidence.get("evaluations", len(proposed))
    evidence.update(
        {
            "admitted_roots": len(ordered),
            "excluded_roots": evaluated - len(ordered),
            "candidate_roots": proposed,
        }
    )
    diagnostics = []
    for _, output in ordered:
        diagnostics.append(
            {
                **evidence,
                "original_output": output,
                "residual_relative_tolerance": RESIDUAL_REL_TOL,
                "residual_absolute_tolerance": RESIDUAL_ABS_TOL,
            }
        )
    return {
        "amounts": [amount for amount, _ in ordered],
        "excluded": excluded,
        "diagnostics": diagnostics,
    }, evidence
