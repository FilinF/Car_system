import requests

base_url = 'http://127.0.0.1:8000'


def test_create_route():
    url = f'{base_url}/car/'
    data = {
        'id': 1,
        'coordinate_x': 10,
        'coordinate_y': 20
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201


def test_get_cars():
    # First, create a route
    create_url = f'{base_url}/car/'
    data = {
        'id': 2,
        'coordinate_x': 30,
        'coordinate_y': 40
    }
    requests.post(create_url, json=data)

    # Now, get the list of cars
    list_url = f'{base_url}/car/get_cars/'
    response = requests.get(list_url)
    assert response.status_code == 200
    resp_data = response.json()
    assert len(resp_data) > 0
    car = next(car for car in resp_data if car['id'] == 2)
    assert car['coordinate_x'] == 30
    assert car['coordinate_y'] == 40


def test_notify_car():
    # First, create a route
    create_url = f'{base_url}/car/'
    data = {
        'id': 3,
        'coordinate_x': 50,
        'coordinate_y': 60
    }
    requests.post(create_url, json=data)

    # Now, notify the car
    notify_url = f'{base_url}/car/change_st/notifyed/3/'
    response = requests.get(notify_url)
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data['id'] == 3


def test_get_cars_after_notify():
    # First, create and notify a route
    create_url = f'{base_url}/car/'
    data = {
        'id': 4,
        'coordinate_x': 70,
        'coordinate_y': 80
    }
    requests.post(create_url, json=data)
    notify_url = f'{base_url}/car/change_st/notifyed/4/'
    requests.get(notify_url)

    # Now, get the list of cars
    list_url = f'{base_url}/car/get_cars/'
    response = requests.get(list_url)
    assert response.status_code == 200
    resp_data = response.json()
    assert all(car['id'] != 4 for car in resp_data)  # Car with id 4 should not be in the list