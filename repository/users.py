import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

engine = create_async_engine(os.getenv('DATABASE_USERS_URL'))
new_sessions = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class UserOrm(Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Mapped[str]
    hash = Mapped[str]


class UsersRepository:
    @classmethod
    async def find_user(cls, name: str) -> UserOrm:
        async with new_sessions() as session:
            query = select(UserOrm).where(UserOrm.name == name)
            result = await session.execute(query)
            user = result.scalars().one()
            return user


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
