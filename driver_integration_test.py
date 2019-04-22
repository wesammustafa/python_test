import pytest
import requests
import json
import time
import constants
from random import randint
from helper import create_driver, login, update_status, update_location, get_company_areas, get_area


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
def driver2(admin_token):
    json_response = create_driver(admin_token)
    assert json_response.get('status') == 'SUCCESS'
    if json_response.get('status') == 'SUCCESS':
        print('\nDriver2 ==> {} <== has been created successfully'.format(
            json_response.get('data').get('email')))
    return json_response.get('data')


def test_create_driver(admin_token):
    json_response = create_driver(admin_token)
    print('\nDriver ==> {} <== has been created successfully: '.format(
        json_response.get('data').get('name')))
    assert json_response['status'] == 'SUCCESS'


def test_create_and_list_driver(driver):
    driver_email = driver.get('email')
    time.sleep(5)
    url = 'https://taxi3.rytalo.com/api/taxi3/drivers/?company_id=1'
    response = requests.get(url)
    json_response = json.loads(response.text)
    found = False
    for d in json_response:
        if d['email'] == driver_email:
            found = True
            break
    assert found == True
    if found == True:
        print('Driver ==> {} <== has been found successfully in the list'.format(
            driver_email))


def test_driver_status_change(driver):
    driver_email = driver.get('email')
    driver_password = constants.PASSWORD

    json_response = login("Driver", driver_email, driver_password)
    assert json_response.get('status') == "SUCCESS"
    assert json_response.get('data').get('status') == 'Away-Off'
    if json_response.get('data').get('status') == 'Away-Off':
        print('Driver ==> {} <== status confirmed Away-Off after first login'.format(
            driver_email))

    driver_token = json_response.get('data').get('api_token')
    ''' take care here you are calling change status twice because single hit causes error '''
    json_response = update_status(driver_token, 'Available')
    json_response = update_status(driver_token, 'Available')
    assert json_response.get('status') == "SUCCESS"
    if json_response.get('status') == "SUCCESS":
        print('Driver ==> {} <== status has been successfully changed into Available'.format(
            driver_email))


def test_driver_location(admin_token, driver):
    driver_email = driver.get('email')
    driver_password = constants.PASSWORD

    login_data = login("Driver", driver_email, driver_password)
    driver_token = login_data.get('data').get('api_token')

    lat = 74.06658571622343,
    lng = 63.30840301513672

    '''take care that here we are calling tracking api twice in order to be able to change location'''
    location_json_response = update_location(driver_token, lat, lng)
    location_json_response = update_location(driver_token, lat, lng)
    assert location_json_response.get('status') == 'SUCCESS'
    if location_json_response.get('status') == 'SUCCESS':
        print('Driver ==> {} <== location has been set successfully to out area'.format(
            driver_email))

    company_areas_json = get_company_areas()
    if len(company_areas_json):
        print('Areas have been loaded successfully')

    founded_out = False
    for area in company_areas_json:
        if area == 'Out':
            for id in company_areas_json[area]:
                if str(id) == str(login_data.get('data').get('id')):
                    founded_out = True
                    break

    assert founded_out == True
    if founded_out == True:
        print('Driver ==> {} <== has been confirmed at Out area'.format(
            driver_email))

    area_details_json = get_area(admin_token, 1)
    assert area_details_json.get('status') == 'SUCCESS'
    if area_details_json.get('status') == 'SUCCESS':
        print('Area ==> {} <== points have been loaded successfully'.format(
            area_details_json.get('data').get('name')))

    new_area_name = area_details_json.get('data').get('name')
    lat = area_details_json['data']['points'][0]['lat']
    lng = area_details_json['data']['points'][0]['lng']
    time.sleep(2)

    '''take care that here we are calling tracking api once here because we did it before'''
    new_location_json = update_location(driver_token, lat, lng)
    assert new_location_json.get('status') == 'SUCCESS'
    if new_location_json.get('status') == 'SUCCESS':
        print('Driver ==> {} <== location has been set successfully to {} area'.format(
            driver_email, new_area_name))

    updated_company_areas_json = get_company_areas()
    if len(updated_company_areas_json):
        print('Areas have been loaded successfully')

    founded_in = False
    for area in updated_company_areas_json:
        if area == new_area_name:
            for id in updated_company_areas_json.get(area).keys():
                if str(id) == str(login_data.get('data').get('id')):
                    founded_in = True
                    break

    assert founded_in == True
    if founded_in == True:
        print('Driver ==> {} <== has been confirmed at {}'.format(
            driver_email, new_area_name))


def test_drivers_area_order(driver, driver2, admin_token):
    driver1_email = driver.get('email')
    driver1_password = 123456

    driver2_email = driver2.get('email')
    driver2_password = 123456

    driver1_login_json = login("Driver", driver1_email, driver1_password)
    assert driver1_login_json['status'] == "SUCCESS"
    if driver1_login_json['data']['status'] == 'Away-Off':
        print('Driver ==> {} <== status confirmed Away-Off after first login'.format(
            driver1_email))

    driver1_token = driver1_login_json['data']['api_token']
    print('driver1_token: ', driver1_token)

    '''take care that here we are calling change status api twice in order to be able to change status'''
    change_status_json = update_status(driver1_token, "Available")
    change_status_json = update_status(driver1_token, "Available")
    assert change_status_json['status'] == "SUCCESS"
    if change_status_json['status'] == "SUCCESS":
        print('Driver ==> {} <== status has been successfully changed into Available'.format(
            driver1_email))

    driver2_login_json = login("Driver", driver2_email, driver2_password)
    assert driver2_login_json['status'] == "SUCCESS"
    if driver2_login_json['data']['status'] == 'Away-Off':
        print('Driver ==> {} <== status confirmed Away-Off after first login'.format(
            driver2_email))

    driver2_token = driver2_login_json['data']['api_token']
    print('driver2_token: ', driver2_token)

    '''take care that here we are calling change status api twice in order to be able to change status'''
    change_status_json = update_status(driver2_token, "Available")
    change_status_json = update_status(driver2_token, "Available")
    assert change_status_json['status'] == "SUCCESS"
    if change_status_json['status'] == "SUCCESS":
        print('Driver ==> {} <== status has been successfully changed into Available'.format(
            driver2_email))

    point = {
        "lat": 30.06657871622343,
        "lng": 31.30840301513672
    }

    driver1_tracking_json = update_location(driver1_token, point['lat'], point['lng'])
    assert driver1_tracking_json['status'] == 'SUCCESS'
    if driver1_tracking_json['status'] == 'SUCCESS':
        print('Driver ==> {} <== location has been set successfully'.format(
            driver1_email))

    driver2_tracking_json = update_location(driver2_token, point['lat'], point['lng'])
    assert driver2_tracking_json['status'] == 'SUCCESS'
    if driver2_tracking_json['status'] == 'SUCCESS':
        print('Driver ==> {} <== location has been set successfully'.format(
            driver2_email))
