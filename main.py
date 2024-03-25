from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqladmin import Admin
from admin import CruiseAdmin, ShipsAdmin, AdminAuth, UsersAdmin
from database.database import engine, create_tables as create_data_db, delete_tables as delete_data_db
from repository.users import create_tables as create_users_db, delete_tables as delete_users_db
from router import cruise_router
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_users_db()
    await delete_data_db()
    await create_users_db()
    await create_data_db()
    print("[DB] =-=-=-=-=-=-=-==-=-=-=-=-=-=-= Database connected")
    yield
    print("[DB] =-=-=-=-=-=-=-==-=-=-=-=-=-=-= Database disconnected")

app = FastAPI(lifespan=lifespan)
app.include_router(cruise_router)

authentication_backend = AdminAuth(secret_key=os.getenv('SECRET_KEY'))
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(CruiseAdmin)
admin.add_view(ShipsAdmin)
# admin.add_view(UsersAdmin)

