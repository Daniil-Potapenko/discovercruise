from starlette.responses import RedirectResponse
from database.database import CruiseOrm, ShipOrm, UserOrm
from sqladmin import ModelView, action
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from auth import gen_hash, check_password, gen_token, check_token


# from starlette.responses import RedirectResponse
# from repository.users import UserOrm


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:

        form = await request.form()
        username, password = form["username"], form["password"]

        if username and password:
            password_is_correct = await check_password(username, password)
            if not password_is_correct:
                return False
            token = await gen_token()
            request.session.update({"token": token})
            return True
        else:
            return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        return await check_token(token)


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

    async def on_model_change(self, data, model, is_created, request):
        old_pass = model.hashed_pass
        new_pass = data.get('hashed_pass')

        if old_pass == new_pass:
            return

        hash_of_new_pass = gen_hash(new_pass)
        data.update({
            'hashed_pass': hash_of_new_pass
        })

    # @action(
    #     name="approve_users",
    #     label="Approve",
    #     confirmation_message="Are you sure?",
    #     add_in_detail=True,
    #     add_in_list=True,
    # )
    # async def approve_users(self, request: Request):
    #     pks = request.query_params.get("pks", "").split(",")
    #
    #     if pks:
    #         for pk in pks:
    #             model: UserOrm = await self.get_object_for_edit(pk)
    #             print(model.name)
    #
    #     referer = request.headers.get("Referer")
    #     if referer:
    #         return RedirectResponse(referer)
    #     else:
    #         return RedirectResponse(request.url_for("admin:list", identity=self.identity))
