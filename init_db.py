import os
import asyncio
from app.database import models
from app.database.engine import AsyncSession, engine


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

asyncio.run(init_db())
