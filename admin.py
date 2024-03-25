from database import CruiseOrm, ShipOrm
from sqladmin import ModelView


class CruiseAdmin(ModelView, model=CruiseOrm):
    name = 'Круиз'
    name_plural = "Круизы"
    column_list = [CruiseOrm.id, CruiseOrm.name]


class ShipsAdmin(ModelView, model=ShipOrm):
    name = 'Корабль'
    name_plural = "Корабли"
    column_list = [ShipOrm.id, ShipOrm.name]
