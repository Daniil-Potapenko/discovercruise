from typing import Optional
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL'))
new_sessions = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class CruiseOrm(Model):
    __tablename__ = 'cruises'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    type: Mapped[str]
    status: Mapped[str]
    price: Mapped[int]
    date_start: Mapped[str]
    date_end: Mapped[str]
    ship: Mapped[str]
    duration: Mapped[int]
    images: Mapped[str]
    company: Mapped[str]
    departure_point: Mapped[str]
    destination_point: Mapped[str]


class ShipOrm(Model):
    __tablename__ = 'ships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    images: Mapped[str]


class CompanyOrm(Model):
    __tablename__ = "company's"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    images: Mapped[str]


class HarbourOrm(Model):
    __tablename__ = 'harbour'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    images: Mapped[str]


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
