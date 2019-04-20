import pytest
import requests
import json
import time
from random import randint
import constants

from helper import create_driver, create_customer, update_status, login, create_booking, dispatch_booking 
from socket_helper import init_socket


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


@pytest.fixture
def customer(admin_token):
    json_response = create_customer(admin_token)
    assert json_response.get('status') == 'SUCCESS'
    if json_response.get('status') == 'SUCCESS':
        print('Customer ==> {} <== has been created successfully'.format(
            json_response.get('data').get('email')))
    return json_response.get('data')


def test(driver, customer):

    driver_email = driver.get('email')
    driver_password = constants.PASSWORD

    login_json = login("Driver", driver_email, driver_password)
    assert login_json.get('status') == "SUCCESS"
    assert login_json.get('data').get('status') == 'Away-Off'
    if login_json.get('data').get('status') == 'Away-Off':
        print('Driver confirmed Away-Off after first login')

    driver_token = login_json.get('data').get('api_token')
    print('driver_token: ', driver_token)

    customer_email = customer.get('email')
    customer_token = customer.get('api_token')
    print('customer_token: ', customer_token)

    ''' take care here we are hitting status response twice for a reason '''
    status_response = update_status(driver_token, 'Available')
    status_response = update_status(driver_token, 'Available')
    print(status_response)
    assert status_response.get('status') == "SUCCESS"
    if status_response.get('status') == "SUCCESS":
      print('Driver status changed to Available')

    init_socket(driver_token)

    booking_json = create_booking(customer_token)
    assert booking_json.get('status') == 'SUCCESS'
    company_id = booking_json.get('data').get('company_id')
    booking_id = booking_json.get('data').get('id')
    driver_id = driver.get('id')
    dispatch_booking(company_id, booking_id, driver_id)

