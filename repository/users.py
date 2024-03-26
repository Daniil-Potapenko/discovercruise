from database.database import new_sessions, UserOrm
from sqlalchemy import select


class UsersRepository:
    @classmethod
    async def find_user(cls, user_name: str) -> UserOrm:
        async with new_sessions() as session:
            query = select(UserOrm).where(UserOrm.name == user_name)
            result = await session.execute(query)
            user = result.scalars().one()
            return user

