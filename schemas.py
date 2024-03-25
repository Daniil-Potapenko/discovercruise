from typing import Optional
from pydantic import BaseModel


class SCruiseAdd(BaseModel):
    name: str
    description: str
    type: str
    status: str
    price: int
    date_start: str
    date_end: str
    ship: str
    duration: int
    images: str
    company: str
    departure_point: str
    destination_point: str


class SCompany(BaseModel):
    id: int
    name: str
    description: str
    images: list[str]


class SShip(BaseModel):
    id: int
    name: str
    description: str
    images: list[str]


class SHarbour(BaseModel):
    id: int
    name: str
    description: str
    images: list[str]


class SCruise(SCruiseAdd):
    id: int
