from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import cruise_router
from sqladmin import Admin
from database import engine
from admin import CruiseAdmin, ShipsAdmin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    print("[DB] =-=-=-=-=-=-=-==-=-=-=-=-=-=-= Database connected")
    yield
    print("[DB] =-=-=-=-=-=-=-==-=-=-=-=-=-=-= Database disconnected")


app = FastAPI(lifespan=lifespan)
app.include_router(cruise_router)


admin = Admin(app, engine)
admin.add_view(CruiseAdmin)
admin.add_view(ShipsAdmin)
