from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import Machine
from app.database.schemas import MachineCreate, MachineUpdate
from .site_service import get_site
from app.services.shared.errors import SiteEnergyError


async def get_machines(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Machine]:
    stmt = select(Machine)
    result = await db.execute(stmt)
    machines = result.scalars().all()
    return machines


async def get_machine(db: AsyncSession, machine_id: int) -> Optional[Machine]:
    stmt = select(Machine).where(Machine.id == machine_id)
    result = await db.execute(stmt)
    machine = result.scalars().one_or_none()
    return machine


async def get_machines_by_site_id(db: AsyncSession, site_id: int) -> List[Machine]:
    stmt = select(Machine).where(Machine.site_id == site_id)
    result = await db.execute(stmt)
    machines = result.scalars().all()
    return machines


async def get_site_accumulated_energy(db: AsyncSession, site_id: int) -> int:
    machines_on_site = await get_machines_by_site_id(db, site_id)
    accumulated_energy_on_site = 0
    for machine in machines_on_site:
        accumulated_energy_on_site += machine.nominal_power
    return accumulated_energy_on_site


async def create_machine(db: AsyncSession, machine: MachineCreate) -> Optional[Machine]:
    new_machine = Machine(**machine.dict())
    if new_machine.site_id:
        accumulated_energy_on_site = await get_site_accumulated_energy(
            db, new_machine.site_id)
        site = await get_site(db, new_machine.site_id)
        site_max_energy = site.max_power if site else 0
        if accumulated_energy_on_site + new_machine.nominal_power > site_max_energy:
            raise SiteEnergyError(
                "Cannot create machine, site energy limit exceeded")

    db.add(new_machine)
    await db.commit()
    await db.refresh(new_machine)
    return machine


async def update_machine(db: AsyncSession, machine_id: int, machine: MachineUpdate) -> Optional[Machine]:
    existing_machine = await get_machine(db, machine_id)
    if existing_machine is None:
        return None

    for key, value in machine.dict().items():
        if value is not None:
            setattr(existing_machine, key, value)

    await db.commit()
    await db.refresh(existing_machine)
    return existing_machine


async def delete_machine(db: AsyncSession, machine_id: int) -> bool:
    machine = await get_machine(db, machine_id)
    if machine is None:
        return None

    await db.delete(machine)
    await db.commit()
    return True
