from database.database import CruiseOrm, ShipOrm
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
# from starlette.responses import RedirectResponse
from repository.users import UserOrm


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


class CruiseAdmin(ModelView, model=CruiseOrm):
    name = 'Круиз'
    name_plural = "Круизы"
    column_list = [CruiseOrm.id, CruiseOrm.name]


class ShipsAdmin(ModelView, model=ShipOrm):
    name = 'Корабль'
    name_plural = "Корабли"
    column_list = [ShipOrm.id, ShipOrm.name]


class UsersAdmin(ModelView, model=UserOrm):
    name = 'Пользователь'
    name_plural = 'Пользователи'
    column_list = [UserOrm.id, UserOrm.name]

