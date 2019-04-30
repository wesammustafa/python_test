import pytest
import requests
import json
import time
import constants
from helper import create_car_type, get_car_type


@pytest.fixture
def admin_token():
    payload = {
        "email": constants.ADMIN_EMAIL,
        "password": constants.ADMIN_PASSWORD
    }
    url = 'http://grapes.mi-taxi.ca/taxi3/public/api/cms/v1/admins/login'
    response = requests.post(url, data=payload)
    json_response = json.loads(response.text)
    assert response.ok == True
    assert json_response.get('status') == 'SUCCESS'
    return json_response.get('data').get('api_token')


@pytest.fixture
def car_type(admin_token):
    json_response = create_car_type(admin_token, constants.COMPANY_ID, 4)
    assert json_response.get('status') == 'SUCCESS'
    print('\n ==> {} <== has been created successfully'.format(
        json_response.get('data').get('name')))
    return json_response.get('data')


def test_car_type_consumer(car_type):
    time.sleep(2)
    car_type_id = car_type['id']
    car_type_name = car_type['name']
    car_type = get_car_type(car_type_id)
    assert car_type['data']['name'] == car_type_name
    print('Car type consumer is working properly')
