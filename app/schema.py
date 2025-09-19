from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base model for the expression string
class BaseExpression(BaseModel):
    expr: str

# Model for incoming request (Expression)
class ExpressionIn(BaseExpression):
    """Model for the calculator request body."""
    # No extra fields needed, inherits 'expr'

# Model for outgoing log/response (CalculatorLog)
class ExpressionOut(BaseExpression):
    """Model for the calculator log entry and response."""
    timestamp: Optional[datetime] = None  # Optional for the main response
    result: float
    # Inherits 'expr' from BaseExpression