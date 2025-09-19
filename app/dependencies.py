from collections import deque
import re
from fastapi import HTTPException
from app.schema import ExpressionIn

HISTORY_MAX = 1000
# Moved history here
history = deque(maxlen=HISTORY_MAX)

# Regular expressions for percent expansion (moved from old models.py/calculator.py)
_percent_pair = re.compile(r"""
    (?P<a>\d+(?:\.\d+)?)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""", re.VERBOSE)
_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")

# Dependency to get the history deque
def get_history():
    """Returns the in-memory history deque."""
    return history

# Dependency to expand the expression (previously a method on Expression)
def expand_percent(request: ExpressionIn) -> str:
    """
    Handles A op B% and standalone N% patterns.
    Raises an HTTPException if the expression is None or empty.
    """
    if not request.expr:
        raise HTTPException(status_code=400, detail="Expression cannot be empty")
        
    s = request.expr
    
    # Check for empty string after expansion logic
    if not s.strip():
        raise HTTPException(status_code=400, detail="Expression results in empty string after percent expansion")

    while True:
        # Replace A op B%
        m = _percent_pair.search(s)
        if not m:
            break
        a, op, b = m.group("a", "op", "b")
        if op in "+-":
            # A op B% -> A op ((B/100)*A)
            repl = f"{a} {op} (({b}/100)*{a})"
        elif op == "*":
            # A * B% -> A * (B/100)
            repl = f"{a} * ({b}/100)"
        else: # op == "/"
            # A / B% -> A / (B/100)
            repl = f"{a} / ({b}/100)"
        s = s[:m.start()] + repl + s[m.end():]

    # Replace B% (standalone)
    s = _number_percent.sub(lambda m: f"({m.group('n')}/100)", s)
    return s