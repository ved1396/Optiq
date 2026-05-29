from engines.base import BaseEngine
import re

class CalculatorEngine(BaseEngine):
    def process(self, query: str) -> str:
        # Simple extraction for MVP
        try:
            # Extract only math characters
            math_expr = re.sub(r'[^0-9\+\-\*\/\.\(\)\s]', '', query)
            if not math_expr.strip():
                return "I couldn't find a valid mathematical expression."
            
            # Use eval safely by disabling builtins
            result = eval(math_expr, {"__builtins__": None}, {})
            return str(result)
        except Exception as e:
            return f"Error evaluating math expression: {str(e)}"
