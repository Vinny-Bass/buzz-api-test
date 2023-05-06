import os
import uvicorn
import asyncio
from fastapi import FastAPI
from app.database import models
from app.database.engine import AsyncSession, engine
from app.api.endpoints import machine

app = FastAPI()

app.include_router(machine.router, prefix="/machines", tags=["machines"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
