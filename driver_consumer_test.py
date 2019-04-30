import pytest
import requests
import json
import time
import constants
from random import randint
from helper import create_driver, login, get_driver_redis


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
def driver(admin_token):
    json_response = create_driver(admin_token)
    assert json_response.get('status') == 'SUCCESS'
    if json_response.get('status') == 'SUCCESS':
        print('\nDriver ==> {} <== has been created successfully'.format(
            json_response.get('data').get('email')))
    return json_response.get('data')

def test_driver_consumer(driver):
    time.sleep(5)
    id = driver['id']
    company_id = constants.COMPANY_ID
    result = get_driver_redis(id, company_id)
    assert type(result) is dict
    assert result['email'] == driver['email']
    print('driver consumer is working properly')