from fastapi import  FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from sqladmin import Admin, ModelView
from database import engine
from models.cruise import CruiseOrm
from router import router as tasksRouter
from router import cruise_router

@asynccontextmanager
async def lifespan(app: FastAPI):
  await create_tables()
  print("[DB] =-=-=-=-=-=-=-==-=-=-=-=-=-=-= Database connected")
  yield
  print("[DB] =-=-=-=-=-=-=-==-=-=-=-=-=-=-= Database disconnected")


app = FastAPI(lifespan=lifespan)

app.include_router(tasksRouter) 
app.include_router(cruise_router)


admin = Admin(app, engine)

class UserAdmin(ModelView, model=CruiseOrm):
    column_list = [CruiseOrm.id, CruiseOrm.name]
admin.add_view(UserAdmin)