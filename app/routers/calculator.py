import math
from collections import deque
from datetime import datetime
from fastapi import APIRouter, Depends
from asteval import Interpreter
from app.schema import ExpressionIn, ExpressionOut
from app.dependencies import expand_percent, get_history

# ---------- Safe evaluator setup ----------
# Moved Interpreter setup here since it's only used for calculation
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

# Router setup
router = APIRouter(
    prefix="/calculate",
    tags=["calculator"],
)

@router.post("")
def calculate_expression(
    request: ExpressionIn,
    expanded_expr: str = Depends(expand_percent), # Dependency for expansion
    history_deque: deque = Depends(get_history)   # Dependency for history access
):
    try:
        result = aeval(expanded_expr)
        
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            
            error_log = ExpressionOut(expr=request.expr, result=0.0, timestamp=None)
            response_data = error_log.model_dump()
            response_data["ok"] = False
            response_data["error"] = msg
            return response_data

        # Create the log entry (ExpressionOut model)
        log_entry = ExpressionOut(
            timestamp=datetime.now(),
            expr=request.expr,
            result=result,
        )
        history_deque.appendleft(log_entry)
        
        # Convert the Pydantic model to a dict first
        response_data = log_entry.model_dump() 
        # Then manually update the dictionary keys required by the client
        response_data["ok"] = True
        response_data["error"] = ""
        return response_data # Return the standard Python dictionary

    except Exception as e:
        error_log = ExpressionOut(expr=request.expr, result=0.0, timestamp=None)
        # Convert to dict and update
        response_data = error_log.model_dump()
        response_data["ok"] = False
        response_data["error"] = str(e)
        return response_data