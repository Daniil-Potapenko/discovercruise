from typing import Annotated
from fastapi import APIRouter, Depends
from schemas import SCruise, SCruiseAdd
from repository.data import CruiseRepository


cruise_router = APIRouter(
    prefix='/cruises',
    tags=["Круизы"]
)


@cruise_router.post('')
async def add_cruise(
        cruise: Annotated[SCruiseAdd, Depends()]
):
    cruise_id = await CruiseRepository.add_cruise(cruise)
    return {"success": 'true', "id": cruise_id}


@cruise_router.get('')
async def get_all() -> list[SCruise]:
    cruises = await CruiseRepository.get_all_cruises()
    return cruises


@cruise_router.get('/find')
async def get_one():
    cruise = await CruiseRepository.get_one_cruise()
    return cruise
