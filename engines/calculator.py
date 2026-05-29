import ast
import operator
import re

from engines.base import BaseEngine


class CalculatorEngine(BaseEngine):
    """Safely evaluates arithmetic expressions used in query routing."""

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def _eval_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._operators:
            return self._operators[type(node.op)](self._eval_node(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in self._operators:
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self._operators[type(node.op)](left, right)
        raise ValueError("Unsupported mathematical expression.")

    def process(self, query: str) -> str:
        expression = re.sub(r"[^0-9\.\+\-\*\/\(\)\%\^\s]", "", query).replace("^", "**")
        if not expression.strip():
            return "I could not find a valid mathematical expression to evaluate."
        try:
            parsed = ast.parse(expression, mode="eval")
            result = self._eval_node(parsed.body)
            return f"The result is {result:g}."
        except ZeroDivisionError:
            return "Division by zero is undefined."
        except Exception:
            return "I could not evaluate that expression safely."
