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
def create_driver_2(admin_token):
    json_response = create_driver(admin_token)
    assert json_response.get('status') == 'SUCCESS'
    if json_response.get('status') == 'SUCCESS':
        print('\nDriver2 ==> {} <== has been created successfully'.format(
            json_response.get('data').get('email')))
    return json_response('data')


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


# def test_drivers_area_order(create_driver, create_driver_2, admin_token):
#     driver_1_email = create_driver['email']
#     driver_1_password = 123456

#     driver_2_email = create_driver_2['email']
#     driver_2_password = 123456

#     driver_1_login_payload = {
#         "type": "Driver",
#         "email": driver_1_email,
#         "password": driver_1_password
#     }
#     url = 'https://taxi3.rytalo.com/api/authenticate/login'
#     driver_1_login_response = requests.post(url, data=driver_1_login_payload)
#     driver_1_login_json = json.loads(driver_1_login_response.text)
#     assert driver_1_login_json['status'] == "SUCCESS"
#     assert driver_1_login_json['data']['status'] == 'Away-Off'
#     print('Driver ==> {} <== status confirmed Away-Off after first login'.format(
#         driver_1_email))

#     driver_1_token = driver_1_login_json['data']['api_token']
#     print('driver_1_token: ', driver_1_token)
#     driver_1_change_status_params = {
#         'token': driver_1_token,
#         'driver_status': 'Available'
#     }
#     change_status_url = 'https://taxi3.rytalo.com/api/taxi3/driver/status/'

#     '''take care that here we are calling change status api twice in order to be able to change status'''
#     change_status_response = requests.get(
#         change_status_url, params=driver_1_change_status_params)
#     change_status_json = json.loads(change_status_response.text)

#     change_status_response = requests.get(
#         change_status_url, params=driver_1_change_status_params)
#     change_status_json = json.loads(change_status_response.text)

#     assert change_status_json['status'] == "SUCCESS"
#     print('Driver ==> {} <== status has been successfully changed into Available'.format(
#         driver_1_email))

#     driver_2_login_payload = {
#         "type": "Driver",
#         "email": driver_2_email,
#         "password": driver_2_password
#     }
#     url = 'https://taxi3.rytalo.com/api/authenticate/login'
#     driver_2_login_response = requests.post(url, data=driver_2_login_payload)
#     driver_2_login_json = json.loads(driver_2_login_response.text)
#     assert driver_2_login_json['status'] == "SUCCESS"
#     assert driver_2_login_json['data']['status'] == 'Away-Off'
#     print('Driver ==> {} <== status confirmed Away-Off after first login'.format(
#         driver_2_email))

#     driver_2_token = driver_2_login_json['data']['api_token']
#     print('driver_1_token: ', driver_1_token)

#     driver_2_change_status_params = {
#         'token': driver_2_token,
#         'driver_status': 'Available'
#     }
#     change_status_url = 'https://taxi3.rytalo.com/api/taxi3/driver/status/'

#     '''take care that here we are calling change status api twice in order to be able to change status'''
#     change_status_response = requests.get(
#         change_status_url, params=driver_2_change_status_params)
#     change_status_json = json.loads(change_status_response.text)

#     change_status_response = requests.get(
#         change_status_url, params=driver_2_change_status_params)
#     change_status_json = json.loads(change_status_response.text)

#     assert change_status_json['status'] == "SUCCESS"
#     print('Driver2 ==> {} <== status has been successfully changed into Available'.format(
#         driver_2_email))

#     nasr_city_lat_lng_params = {
#         "lat": 30.06657871622343,
#         "lng": 31.30840301513672
#     }
#     '''take care that here we are calling tracking api twice in order to be able to change location'''
#     drive_tracking_url = 'https://taxi3.rytalo.com/api/taxi3/driver/track/'
#     driver_1_tracking_response = requests.get(drive_tracking_url, params=nasr_city_lat_lng_params, headers={
#         'Authorization': 'Bearer {}'.format(driver_1_token)})
#     driver_1_tracking_response = requests.get(drive_tracking_url, params=nasr_city_lat_lng_params, headers={
#         'Authorization': 'Bearer {}'.format(driver_1_token)})
#     driver_1_tracking_json = json.loads(driver_1_tracking_response.text)
#     assert driver_1_tracking_json['status'] == 'SUCCESS'
#     print('Driver ==> {} <== location has been set successfully to nasr city area'.format(
#         driver_1_email))

#     '''take care that here we are calling tracking api twice in order to be able to change location'''
#     drive_tracking_url = 'https://taxi3.rytalo.com/api/taxi3/driver/track/'
#     driver_2_tracking_response = requests.get(drive_tracking_url, params=nasr_city_lat_lng_params, headers={
#         'Authorization': 'Bearer {}'.format(driver_2_token)})
#     driver_2_tracking_response = requests.get(drive_tracking_url, params=nasr_city_lat_lng_params, headers={
#         'Authorization': 'Bearer {}'.format(driver_2_token)})
#     driver_2_tracking_json = json.loads(driver_2_tracking_response.text)
#     assert driver_2_tracking_json['status'] == 'SUCCESS'
#     print('Driver ==> {} <== location has been set successfully to nasr city area'.format(
#         driver_2_email))
