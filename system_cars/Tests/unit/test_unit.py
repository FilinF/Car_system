import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
from uuid import uuid4
from datetime import datetime
from applications.application_service import create_route, location_cars, notify
from applications.models import CarEntry, CarEntryStatus


@pytest.fixture
def car_id():
    return 1


@pytest.fixture
def car_coordinates():
    return (10, 20)


@pytest.fixture
def car_entry(car_id, car_coordinates):
    return create_route(car_id, *car_coordinates)


def test_create_route(car_id, car_coordinates, car_entry):
    assert car_entry.id == car_id
    assert car_entry.coordinate_x == car_coordinates[0]
    assert car_entry.coordinate_y == car_coordinates[1]
    assert car_entry.status == CarEntryStatus.START
    assert car_entry.s_location == list(car_coordinates)
    assert isinstance(car_entry.created_at, datetime)


def test_update_route(car_id, car_coordinates):
    updated_coordinates = (30, 40)
    create_route(car_id, *car_coordinates)
    updated_car_entry = create_route(car_id, *updated_coordinates)

    assert updated_car_entry.id == car_id
    assert updated_car_entry.coordinate_x == updated_coordinates[0]
    assert updated_car_entry.coordinate_y == updated_coordinates[1]
    assert updated_car_entry.s_location == list(car_coordinates)


def test_location_cars(car_id, car_coordinates):
    create_route(car_id, *car_coordinates)
    active_cars = location_cars()

    assert len(active_cars) == 1
    car_entry = list(active_cars)[0]
    assert car_entry.id == car_id
    assert car_entry.status != CarEntryStatus.FINISH


def test_notify(ca
    r_id, car_coordinates):
    create_route(car_id, *car_coordinates)
    notified_car_entry = notify(car_id)

    assert notified_car_entry.id == car_id
    assert notified_car_entry.status == CarEntryStatus.FINISH