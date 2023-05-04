from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Site
from sqlalchemy import select


async def get_site(db: AsyncSession, site_id: int) -> Optional[Site]:
    stmt = select(Site).where(Site.id == site_id)
    result = await db.execute(stmt)
    site = result.scalars().one_or_none()
    return site
