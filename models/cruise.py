from typing import Optional
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column


class Model(DeclarativeBase):
  pass

class CruiseOrm(Model):
  __tablename__  = 'cruises'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  description: Mapped[Optional[str]]
  type: Mapped[str]
  date_start: Mapped[str]
  date_end:Mapped[str]
  ship: Mapped[str]
  duration: Mapped[int]
  images: Mapped[str]
  company: Mapped[str]
  departure_point: Mapped[str]
  destination_point: Mapped[str]