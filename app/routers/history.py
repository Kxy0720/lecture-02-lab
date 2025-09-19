from typing import List
from collections import deque
from fastapi import APIRouter, Depends
from app.schema import ExpressionOut
from app.dependencies import get_history, HISTORY_MAX

router = APIRouter(
    prefix="/history",
    tags=["history"],
)

@router.get("", response_model=List[ExpressionOut])
def get_history_log(
    limit: int = 50,
    history_deque: deque = Depends(get_history) # Dependency for history access
):
    # The return type is a list of ExpressionOut objects
    return list(history_deque)[: max(0, min(limit, HISTORY_MAX))]

@router.delete("")
def clear_history_log(
    history_deque: deque = Depends(get_history) # Dependency for history access
):
    history_deque.clear()
    return {"ok": True, "cleared": True}