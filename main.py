import os
import uvicorn
import asyncio
from fastapi import FastAPI
from app.database import models
from app.database.engine import AsyncSession, engine
from app.api.endpoints import machine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

    # Create an initial Site record using the SITE_MAX_POWER environment variable
    site_max_power = int(os.environ.get("SITE_MAX_POWER", 1000))
    async with AsyncSession(bind=engine) as db:
        site = models.Site(max_power=site_max_power)
        db.add(site)
        await db.commit()


app = FastAPI()

app.include_router(machine.router, prefix="/machines", tags=["machines"])


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "init_db":
        asyncio.run(init_db())
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
