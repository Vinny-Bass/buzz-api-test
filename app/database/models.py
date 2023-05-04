from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum


class MachineType(enum.Enum):
    FURNACE = "furnace"
    COMPRESSOR = "compressor"
    CHILLER = "chiller"
    ROLLING_MILL = "rolling mill"


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    max_power = Column(Integer, nullable=False)

    machines = relationship("Machine", back_populates="site")


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nominal_power = Column(Integer, nullable=False)
    type = Column(Enum(MachineType), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)

    site = relationship("Site", back_populates="machines")
