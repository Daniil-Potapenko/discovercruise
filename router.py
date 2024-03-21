from typing import Annotated
from fastapi import APIRouter, Depends
from schemas import SCruise, SCruiseAdd, STask, STaskAdd
from repository import TaskRepository

router = APIRouter(
    prefix='/tasks',
    tags=["Таски"]
)


@router.post('')
async def add_task(
        task: Annotated[STaskAdd, Depends()]
):
    task_id = await TaskRepository.add_one(task)
    return {"success": 'true', "id": task_id}


@router.get('')
async def get_all() -> list[STask]:
    tasks = await TaskRepository.get_all()
    return tasks


cruise_router = APIRouter(
    prefix='/cruises',
    tags=["Cruises"]
)


@cruise_router.post('')
async def add_cruise(
        cruise: Annotated[SCruiseAdd, Depends()]
):
    cruise_id = await TaskRepository.add_cruise(cruise)
    return {"success": 'true', "id": cruise_id}


@cruise_router.get('')
async def get_all() -> list[SCruise]:
    cruises = await TaskRepository.get_all_cruises()
    return cruises


@cruise_router.get('/find')
async def get_one():
    cruise = await TaskRepository.get_one_cruise()
    return cruise
