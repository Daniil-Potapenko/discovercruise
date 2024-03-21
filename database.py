from typing import Optional
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column
load_dotenv()

engine = create_async_engine(
  os.getenv('DATABASE_URL')
)

new_sessions = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
  pass



class TaskOrm(Model):
  __tablename__  = 'tasks'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  description: Mapped[Optional[str]]



async def create_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Model.metadata.drop_all)