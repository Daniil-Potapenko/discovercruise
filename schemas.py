from typing import Optional
from pydantic import BaseModel


class STaskAdd(BaseModel):
  name:str
  description: Optional[str] = None

class STask(STaskAdd):
  id: int



class SCruiseAdd(BaseModel):
  name: str
  description:str
  type: str
  date_start: str
  date_end:str
  ship: str
  duration: int
  images: str
  company: str
  departure_point: str
  destination_point: str


class SCruise(SCruiseAdd):
  id: int