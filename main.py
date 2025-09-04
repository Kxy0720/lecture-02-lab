import math
from collections import deque
from datetime import datetime
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

# Import the new models from models.py
from models import Expression, CalculatorLog

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(request: Expression):  # Changed parameter to accept an Expression object
    try:
        # Use the expand_percent() method from the Expression object
        code = request.expand_percent()
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": request.expr, "result": "", "error": msg}

        # Create a CalculatorLog object to store in history
        log_entry = CalculatorLog(
            timestamp=datetime.now(),
            expr=request.expr,
            result=result,
        )
        history.appendleft(log_entry)
        
        return {"ok": True, "expr": request.expr, "result": result, "error": ""}

    except Exception as e:
        return {"ok": False, "expr": request.expr, "error": str(e)}


@app.get("/history", response_model=List[CalculatorLog])
def get_history(limit: int = 50):
    # The return type is now a list of CalculatorLog objects
    return list(history)[: max(0, min(limit, HISTORY_MAX))]


@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True, "cleared": True}