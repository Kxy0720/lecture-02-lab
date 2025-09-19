from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the routers
from app.routers import calculator, history

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the new routers
app.include_router(calculator.router)
app.include_router(history.router)

# Note: The original /calculate, /history, and HISTORY_MAX/history variables 
# have been removed/moved to dependencies.py and the router files.