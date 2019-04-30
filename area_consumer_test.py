import pytest
import requests
import json
import time
import constants
from helper import create_area, get_area_redis

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
def area(admin_token):
    json_response = create_area(admin_token)
    assert json_response.get('status') == 'SUCCESS'
    if json_response.get('status') == 'SUCCESS':
        print('\n ==> {} <== has been created successfully'.format(
            json_response.get('data').get('name')))
    return json_response.get('data')

def test_area_consumer(area):
  time.sleep(5)
  area_id = area['id']
  company_id = constants.COMPANY_ID
  result = get_area_redis(area_id, company_id)
  assert area['name'] == result['area_name']
  print('Area consumer is working properly')