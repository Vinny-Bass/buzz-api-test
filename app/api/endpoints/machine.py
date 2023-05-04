from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import machine_service
from app.database.schemas import MachineBase, MachineCreate, MachineUpdate
from app.database.engine import get_db_session
from app.api.shared.responses import DeleteResponse
from app.services.shared.errors import SiteEnergyError

router = APIRouter()


@router.get("/", response_model=List[MachineBase])
async def get_machines(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db_session)):
    machines = await machine_service.get_machines(db, skip=skip, limit=limit)
    return machines


@router.get("/{machine_id}", response_model=MachineBase)
async def get_machine(machine_id: int, db: AsyncSession = Depends(get_db_session)):
    machine = await machine_service.get_machine(db, machine_id)
    if machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine


@router.post("/", response_model=MachineBase)
async def create_machine(machine: MachineCreate, db: AsyncSession = Depends(get_db_session)):
    try:
        new_machine = await machine_service.create_machine(db, machine)
    except SiteEnergyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if new_machine is None:
        raise HTTPException(status_code=400, detail="Failed to create machine")

    return new_machine


@router.put("/{machine_id}", response_model=MachineBase)
async def update_machine(machine_id: int, machine: MachineUpdate, db: AsyncSession = Depends(get_db_session)):
    updated_machine = await machine_service.update_machine(db, machine_id, machine)
    if updated_machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return updated_machine


@router.delete("/{machine_id}", response_model=DeleteResponse)
async def delete_machine(machine_id: int, db: AsyncSession = Depends(get_db_session)):
    deleted_machine = await machine_service.delete_machine(db, machine_id)
    if deleted_machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return DeleteResponse()
