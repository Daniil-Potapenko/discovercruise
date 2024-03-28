from database.database import new_sessions
from sqlalchemy import select
from schemas import SCruiseAdd
from database.database import CruiseOrm


class CruiseRepository:

    @classmethod
    async def add_cruise(cls, data: SCruiseAdd) -> int | None:
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

