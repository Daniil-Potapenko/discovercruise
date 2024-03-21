from database import TaskOrm, new_sessions
from sqlalchemy import select
from schemas import SCruiseAdd, STaskAdd
from models.cruise import CruiseOrm


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_sessions() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def get_all(cls):
        async with new_sessions() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models

    @classmethod
    async def add_cruise(cls, data: SCruiseAdd) -> int:
        async with new_sessions() as session:
            cruise_dict = data.model_dump()

            cruise = CruiseOrm(**cruise_dict)
            session.add(cruise)
            await session.flush()
            await session.commit()
            return cruise.id

    @classmethod
    async def get_all_cruises(cls):
        async with new_sessions() as session:
            query = select(CruiseOrm)
            result = await session.execute(query)
            cruise_models = result.scalars().all()
            return cruise_models

    @classmethod
    async def get_one_cruise(cls):
        async with new_sessions() as session:
            query = select(CruiseOrm).where(CruiseOrm.name == 'Aasdfasfg')
            result = await session.execute(query)
            cruise = result.scalars().all()
            return cruise