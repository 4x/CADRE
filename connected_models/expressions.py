"""Bounded algebra interpreted directly from AST nodes; never eval or exec."""

import ast
import math
import operator
from collections.abc import Mapping
from fractions import Fraction

from .contracts import DIMENSIONLESS, Dimensions, ModelError, NumericalError, finite

MAX_EXPRESSION_CHARS = 2048
MAX_EXPRESSION_NODES = 128
MAX_ABS_EXPONENT = 100
MAX_EXPONENT_DENOMINATOR = 1024
SCALAR_FUNCTIONS = frozenset({"log", "exp", "sqrt", "sum", "prod"})
ARITHMETIC = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
COMPARISONS = {ast.Gt: operator.gt, ast.GtE: operator.ge, ast.Lt: operator.lt, ast.LtE: operator.le, ast.Eq: operator.eq}


def parse(expression: str) -> ast.AST:
    """Parse a short expression and enforce a bounded node count."""
    if not isinstance(expression, str) or len(expression) > MAX_EXPRESSION_CHARS:
        raise ModelError("Expression is missing or exceeds the size limit.")
    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, RecursionError) as exc:
        raise ModelError("Invalid scalar expression.") from exc
    if sum(1 for _ in ast.walk(tree)) > MAX_EXPRESSION_NODES:
        raise ModelError("Expression exceeds the complexity limit.")
    return tree.body


def _rational_exponent(node: ast.AST) -> Fraction:
    """Evaluate an exponent subtree to an exact rational; names and calls are rejected."""
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return Fraction(node.value)
    if isinstance(node, ast.Constant) and type(node.value) is float:
        exact = Fraction(node.value)
        if exact.denominator > MAX_EXPONENT_DENOMINATOR:
            raise ModelError(f"Exponent {node.value} is not an exact rational with denominator at most "
                             f"{MAX_EXPONENT_DENOMINATOR}; write it as an integer ratio such as 1/3.")
        return exact
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _rational_exponent(node.operand)
        return -value if isinstance(node.op, ast.USub) else value
    if isinstance(node, ast.BinOp) and type(node.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div):
        left, right = _rational_exponent(node.left), _rational_exponent(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ModelError("Exponent ratio divides by zero.")
        return {ast.Add: left + right, ast.Sub: left - right, ast.Mult: left * right, ast.Div: left / right}[type(node.op)]
    raise ModelError("Dimensional powers require a bounded exact-rational exponent without names or calls.")


def dimensions(node: ast.AST, names: Mapping[str, Dimensions]) -> Dimensions:
    """Check the grammar and dimensional consistency without evaluating values."""
    if isinstance(node, ast.Constant):
        finite(node.value, "Literal")
        return DIMENSIONLESS
    if isinstance(node, ast.Name) and node.id in names:
        return names[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return dimensions(node.operand, names)
    if isinstance(node, ast.BinOp):
        left, right = dimensions(node.left, names), dimensions(node.right, names)
        if isinstance(node.op, (ast.Add, ast.Sub)) and left == right:
            return left
        if isinstance(node.op, ast.Mult):
            return tuple(a + b for a, b in zip(left, right, strict=True))
        if isinstance(node.op, ast.Div):
            return tuple(a - b for a, b in zip(left, right, strict=True))
        if isinstance(node.op, ast.Pow) and left == right == DIMENSIONLESS:
            return DIMENSIONLESS
        if isinstance(node.op, ast.Pow) and right == DIMENSIONLESS:
            exponent = _rational_exponent(node.right)
            if abs(exponent) > MAX_ABS_EXPONENT or exponent.denominator > MAX_EXPONENT_DENOMINATOR:
                raise ModelError(f"Dimensional powers require an exponent of magnitude at most {MAX_ABS_EXPONENT} "
                                 f"with denominator at most {MAX_EXPONENT_DENOMINATOR}.")
            return tuple(exponent * power for power in left)
        raise ModelError("Expression has incompatible dimensions or an unsupported operator.")
    if isinstance(node, ast.Call):
        return call_dimensions(node, names)
    raise ModelError("Only declared names, numbers, scalar arithmetic and log/exp/sqrt/sum/prod calls are executable.")


def call_arguments(node: ast.Call) -> tuple[str, tuple[ast.AST, ...]]:
    """Reject keywords, starred arguments and non-allowlisted callees without inventing semantics."""
    if not isinstance(node.func, ast.Name) or node.func.id not in SCALAR_FUNCTIONS:
        raise ModelError("Only log, exp, sqrt, sum and prod calls are executable.")
    if node.keywords or any(isinstance(arg, ast.Starred) for arg in node.args):
        raise ModelError(f"{node.func.id} takes positional arguments only.")
    return node.func.id, tuple(node.args)


def call_dimensions(node: ast.Call, names: Mapping[str, Dimensions]) -> Dimensions:
    """Type an allowlisted call: log/exp need dimensionless arguments, sum needs uniform dimensions."""
    name, args = call_arguments(node)
    if name in {"log", "exp", "sqrt"} and len(args) != 1:
        raise ModelError(f"{name} takes exactly one argument.")
    if name in {"sum", "prod"} and not args:
        raise ModelError(f"{name} needs at least one argument.")
    kinds = [dimensions(arg, names) for arg in args]
    if name in {"log", "exp"}:
        if kinds[0] != DIMENSIONLESS:
            raise ModelError(f"{name} needs a dimensionless argument.")
        return DIMENSIONLESS
    if name == "sqrt":
        return tuple(Fraction(1, 2) * power for power in kinds[0])
    if name == "sum":
        if any(kind != kinds[0] for kind in kinds):
            raise ModelError("sum needs identical dimensions on every argument.")
        return kinds[0]
    return tuple(sum(powers) for powers in zip(*kinds, strict=True))


def guard_dimensions(node: ast.AST, names: Mapping[str, Dimensions]) -> None:
    """Accept a single numeric comparison with compatible dimensions."""
    if not isinstance(node, ast.Compare) or len(node.ops) != 1 or type(node.ops[0]) not in COMPARISONS:
        raise ModelError("A guard must be a single supported comparison.")
    left, right = dimensions(node.left, names), dimensions(node.comparators[0], names)
    zero = any(isinstance(part, ast.Constant) and type(part.value) in (int, float) and part.value == 0 for part in (node.left, node.comparators[0]))
    if left != right and not zero:
        raise ModelError("Guard compares incompatible dimensions.")


def evaluate(node: ast.AST, names: Mapping[str, float]) -> float:
    """Evaluate the validated algebra, checking domains and every intermediate."""
    try:
        if isinstance(node, ast.Constant):
            return finite(node.value, "Literal")
        if isinstance(node, ast.Name) and node.id in names:
            return names[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            result = evaluate(node.operand, names)
            return -result if isinstance(node.op, ast.USub) else result
        if isinstance(node, ast.BinOp):
            left, right = evaluate(node.left, names), evaluate(node.right, names)
            if isinstance(node.op, ast.Pow):
                if abs(right) > MAX_ABS_EXPONENT:
                    raise NumericalError(f"Exponent exceeds supported magnitude {MAX_ABS_EXPONENT}.")
                if left < 0 and not float(right).is_integer():
                    raise ModelError("Real powers need a nonnegative base for a fractional exponent.")
                return finite(left**right, "Power result")
            if type(node.op) in ARITHMETIC:
                return finite(ARITHMETIC[type(node.op)](left, right), "Arithmetic result")
        if isinstance(node, ast.Call):
            name, args = call_arguments(node)
            values = [evaluate(arg, names) for arg in args]
            if name in {"log", "exp", "sqrt"} and len(values) != 1:
                raise ModelError(f"{name} takes exactly one argument.")
            if name in {"sum", "prod"} and not values:
                raise ModelError(f"{name} needs at least one argument.")
            if name == "log":
                if values[0] <= 0:
                    raise ModelError("Logarithm needs a positive argument.")
                return finite(math.log(values[0]), "Logarithm result")
            if name == "exp":
                return finite(math.exp(values[0]), "Exponential result")
            if name == "sqrt":
                if values[0] < 0:
                    raise ModelError("Square root needs a nonnegative argument.")
                return finite(math.sqrt(values[0]), "Square-root result")
            if name == "sum":
                return finite(sum(values), "Sum result")
            return finite(math.prod(values), "Product result")
    except NumericalError:
        raise
    except OverflowError as exc:
        raise NumericalError("Arithmetic overflowed the supported numerical range.") from exc
    except (ArithmeticError, ValueError) as exc:
        raise ModelError(f"Arithmetic failed: {exc}") from exc
    raise ModelError("Unsupported expression node.")


def check_guard(node: ast.Compare, names: Mapping[str, float]) -> bool:
    """Evaluate a previously validated domain predicate."""
    return COMPARISONS[type(node.ops[0])](evaluate(node.left, names), evaluate(node.comparators[0], names))
