import re
import numexpr as ne
import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# --- 1.1. Definition of the input schema for the calculator with Pydantic ---
class CalculatorInput(BaseModel):
    """Schema for the input of the calculator tool."""
    expression: str = Field(
        description="The mathematical expression to evaluate, for example: '2 + 2 * 3'. "
                    "Must be a valid numerical expression."
    )

# --- 1.2. Tool function 'calculator' ---
def Calculator(expression: str) -> str:
    """
    Executes a simple mathematical expression and returns the result.
    """

    logger.info(f"Tool 'calculator' called with the expression: '{expression}'")
    try:
        result = str(ne.evaluate(expression))
        logger.info(f"Result of the expression '{expression}': {result}")
        return result
    except SyntaxError:
        logger.error(f"Syntax error in the expression '{expression}'.")
        return "Erreur de syntaxe : L'expression mathématique est mal formée."
    except ZeroDivisionError:
        logger.error(f"Error : Division by zero in the expression '{expression}'.")
        return "Mathematical error : Division by zero."
    except Exception as e:
        logger.error(f"Unexpected error when calculating the expression '{expression}': {e}")
        return f"Calculation error : {e}"
