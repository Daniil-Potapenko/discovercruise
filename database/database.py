import datetime
import enum
from typing import Optional, List
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType, ImageType
from sqlalchemy import Column, ForeignKey, inspect, Integer

load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL'))
new_sessions = async_sessionmaker(engine, expire_on_commit=False)
storage = FileSystemStorage(path="./storage/")


class Model(DeclarativeBase):
    pass


class CruiseStatuses(enum.Enum):
    archive = 1
    canceled = 2
    active = 3


class CruiseTypeOrm(Model):
    __tablename__ = 'cruises_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]

    def __str__(self):
        return f"{self.name}"


class CruiseOrm(Model):
    __tablename__ = 'cruises'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    info: Mapped[Optional[str]]
    status: Mapped[CruiseStatuses]

    type_id: Mapped[int] = mapped_column(ForeignKey("cruises_types.id"))
    type: Mapped['CruiseTypeOrm'] = relationship(back_populates="")

    price: Mapped[float]
    sale_price: Mapped[Optional[float]]

    date_start: Mapped[datetime.datetime]
    date_end: Mapped[datetime.datetime]

    ship_id: Mapped[int] = mapped_column(ForeignKey("ships.id"))
    ship: Mapped['ShipOrm'] = relationship()
    duration: Mapped[int]

    company_id: Mapped[int] = mapped_column(ForeignKey("company's.id"))
    company: Mapped["CompanyOrm"] = relationship(back_populates='')

    departure_point_id: Mapped[int] = mapped_column(ForeignKey("harbour.id"))
    departure_point: Mapped["HarbourOrm"] = relationship(back_populates='',  foreign_keys=[departure_point_id])
    destination_point_id: Mapped[int] = mapped_column(ForeignKey("harbour.id"))
    destination_point: Mapped["HarbourOrm"] = relationship(back_populates='',  foreign_keys=[destination_point_id])

    image_1 = Column(ImageType(storage))
    image_2 = Column(ImageType(storage))
    image_3 = Column(ImageType(storage))
    image_4 = Column(ImageType(storage))
    image_5 = Column(ImageType(storage))


class ShipOrm(Model):
    __tablename__ = 'ships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    image_1 = Column(ImageType(storage))
    image_2 = Column(ImageType(storage))
    image_3 = Column(ImageType(storage))

    def __str__(self):
        return f"{self.name}"


class CompanyOrm(Model):
    __tablename__ = "company's"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    image_1 = Column(ImageType(storage))

    def __str__(self):
        return f"{self.name}"


class HarbourOrm(Model):
    __tablename__ = 'harbour'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    image_1 = Column(ImageType(storage))
    image_2 = Column(ImageType(storage))

    def __str__(self):
        return f"{self.name}"


class UserOrm(Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    hashed_pass: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
