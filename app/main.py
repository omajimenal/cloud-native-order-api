import os
import signal
import sys
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

# Config via env vars
APP_ENV = os.getenv("APP_ENV", "dev")
APP_VERSION = os.getenv("APP_VERSION", "0.0.1")
SIMULATE_CPU = os.getenv("SIMULATE_CPU", "false").lower() == "true"

# Structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
)
logger = logging.getLogger()

orders_db = []

class Order(BaseModel):
    id: int
    item: str
    quantity: int

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/readyz")
def readiness():
    return {"status": "ready"}

@app.get("/orders", response_model=List[Order])
def list_orders():
    return orders_db

@app.post("/orders")
def create_order(order: Order):
    orders_db.append(order)
    return order

@app.get("/simulate-load")
def simulate_load():
    if SIMULATE_CPU:
        logger.info("Simulating CPU load...")
        start = time.time()
        while time.time() - start < 5:
            pass
    return {"load": "done"}

def handle_sigterm(*args):
    logger.info("Received SIGTERM, shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)