# models.py
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import List, Union


class CarEntryStatus(Enum):
    START = 'in_start'
    INPROGRESS = 'riding'
    FINISH = 'on_place'

class NewRoute:
    id: int
    coordinate_x: int
    coordinate_y: int

class CarEntry:
    id: int
    status: CarEntryStatus
    coordinate_x: int
    coordinate_y: int
    created_at: datetime
    s_location: List[int]=[]
    f_location: List[int]=[]

    def __init__(self, id: int, coordinate_x:int, coordinate_y:int):
        self.id = id
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.s_location = [coordinate_x, coordinate_y]
        self.f_location = []
        self.status = CarEntryStatus.START
        self.created_at = datetime.now()

class Operation:
    id: UUID
    done: bool
    result = None

    def __init__(self, id: UUID, done: bool = False, result = None):
        self.id = id
        self.done = done
        self.result = result