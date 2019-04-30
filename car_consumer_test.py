import pytest
import requests
import json
import time
import constants
from helper import create_car, get_car_redis

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
def car(admin_token):
    json_response = create_car(admin_token)
    assert json_response.get('status') == 'SUCCESS'
    if json_response.get('status') == 'SUCCESS':
        print('\n ==> {} <== has been created successfully'.format(
            json_response.get('data').get('name')))
    return json_response.get('data')

def test_area_consumer(car):
  time.sleep(5)
  car_id = car['id']
  company_id = constants.COMPANY_ID
  car_type_id = get_car_redis(car_id, company_id)
  assert car['car_type_id'] == str(car_type_id)
  print('Car consumer is working properly')