from database.database import CruiseOrm, ShipOrm, UserOrm, CruiseTypeOrm, HarbourOrm, CompanyOrm
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from auth import gen_hash, check_password, gen_token, check_token


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


class CruiseTypes(ModelView, model=CruiseTypeOrm):
    name = 'Тип круиза'
    name_plural = 'Типы круиза'
    column_list = [CruiseTypeOrm.id, CruiseTypeOrm.name]


class Harbours(ModelView, model=HarbourOrm):
    name = 'Порт'
    name_plural = 'Порты'
    column_list = [HarbourOrm.id, HarbourOrm.name]


class Companys(ModelView, model=CompanyOrm):
    name = 'Компания'
    name_plural = 'Компании'
    column_list = [CompanyOrm.id, CompanyOrm.name]


class UsersAdmin(ModelView, model=UserOrm):
    name = 'Пользователь'
    name_plural = 'Пользователи'
    column_list = [UserOrm.id, UserOrm.name]
    category = 'admin'

    async def on_model_change(self, data, model, is_created, request):
        old_pass = model.hashed_pass
        new_pass = data.get('hashed_pass')

        if old_pass == new_pass:
            return

        hash_of_new_pass = await gen_hash(new_pass)
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
