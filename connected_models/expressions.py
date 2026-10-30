"""Bounded algebra interpreted directly from AST nodes; never eval or exec."""

import ast
import operator
from collections.abc import Mapping

from .contracts import DIMENSIONLESS, Dimensions, ModelError, finite

MAX_EXPRESSION_CHARS = 2048
MAX_EXPRESSION_NODES = 128
MAX_ABS_EXPONENT = 100
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
            return (left[0] + right[0], left[1] + right[1])
        if isinstance(node.op, ast.Div):
            return (left[0] - right[0], left[1] - right[1])
        if isinstance(node.op, ast.Pow) and left == right == DIMENSIONLESS:
            return DIMENSIONLESS
        raise ModelError("Expression has incompatible dimensions or an unsupported operator.")
    raise ModelError("Only declared names, numbers and scalar arithmetic are executable.")


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
                    raise ModelError(f"Exponent exceeds supported magnitude {MAX_ABS_EXPONENT}.")
                return finite(left**right, "Power result")
            if type(node.op) in ARITHMETIC:
                return finite(ARITHMETIC[type(node.op)](left, right), "Arithmetic result")
    except (ArithmeticError, ValueError) as exc:
        raise ModelError(f"Arithmetic failed: {exc}") from exc
    raise ModelError("Unsupported expression node.")


def check_guard(node: ast.Compare, names: Mapping[str, float]) -> bool:
    """Evaluate a previously validated domain predicate."""
    return COMPARISONS[type(node.ops[0])](evaluate(node.left, names), evaluate(node.comparators[0], names))
