from pydantic import BaseModel, validator
from app.database.models import MachineType


class MachineBase(BaseModel):
    name: str
    nominal_power: int
    type: MachineType
    site_id: int = None

    class Config:
        orm_mode = True


class MachineCreate(MachineBase):

    @validator("nominal_power")
    def validate_nominal_power(cls, nominal_power):
        if nominal_power < 1:
            raise ValueError("Nominal power must be greater than 0")
        return nominal_power


class MachineUpdate(MachineBase):
    name: str = None
    nominal_power: int = None
    type: MachineType = None
    site_id: int = None
