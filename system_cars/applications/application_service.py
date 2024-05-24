from .models import CarEntry, CarEntryStatus, NewRoute

cars: dict[int, CarEntry] = {}

def create_route(id : int,coordinate_x:int, coordinate_y:int):
    if id not in cars:
        cr = CarEntry(id,coordinate_x, coordinate_y)
        cars[id] = cr
        return cr
    else :
        cars[id].coordinate_x = coordinate_x
        cars[id].coordinate_y = coordinate_y
        return cars[id]

def location_cars():
    temp: dict[int, CarEntry] = {}
    for key, value in cars.items():
        if value.status != CarEntryStatus.FINISH:
            temp[key] = value

    return temp.values()

def notify(id: int):
    car = cars[id]
    car.status = CarEntryStatus.FINISH
    return car

