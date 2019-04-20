import requests
import json
from random import randint
import constants
import datetime
from point_helper import rand_p


def create_driver(admin_token):
    random_number = randint(100000, 10000000)
    payload = {
        "name": "driver{}".format(random_number),
        "phone": random_number,
        "driver_group_id": 1,
        "city_id": 1,
        "car_id": 1,
        "insurance": 54867878,
        "email": "driver{}@test.com".format(random_number),
        "password": constants.PASSWORD,
        "is_active": 1,
        "image": ""
    }
    url = 'http://grapes.mi-taxi.ca/taxi3/public/api/cms/v1/drivers'
    headers = {
        'Authorization': 'Bearer {}'.format(admin_token),
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.text)


def create_customer(admin_token):
    random_number = randint(100000, 10000000)
    payload = {
        "name": "customer{}".format(random_number),
        "email": "customer{}@test.com".format(random_number),
        "phone": random_number,
        "image": "",
        "company_id": 1,
        "password": 123456,
        "password_confirmation": 123456
    }
    url = 'http://grapes.mi-taxi.ca/taxi3/public/api/customer-app/v1/register'
    headers = {
        'Authorization': 'Bearer {}'.format(admin_token),
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    resp = requests.post(url, json=payload, headers=headers)
    return json.loads(resp.text)


def login(type, driver_email, driver_password):
    payload = {
        "type": type,
        "email": driver_email,
        "password": driver_password
    }
    url = 'https://taxi3.rytalo.com/api/authenticate/login'
    login_response = requests.post(url, data=payload)
    return json.loads(login_response.text)


def update_status(token, driver_status="Available"):
    params = {
        'token': token,
        'driver_status': driver_status
    }
    url = 'https://taxi3.rytalo.com/api/taxi3/driver/status/'
    response = requests.get(url, params=params)
    return json.loads(response.text)


def update_location(token, lat, lng, status=None, ride_status=None, ride_id=None):
    params = {
        'lat': lat,
        'lng': lng
    }
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    url = 'https://taxi3.rytalo.com/api/taxi3/driver/track/'
    response = requests.get(url, params=params, headers=headers)
    return json.loads(response.text)


def get_company_areas(id=1):
    url = 'https://taxi3.rytalo.com/api/taxi3/area_list/?company_id={}'.format(
        id)
    response = requests.get(url)
    return json.loads(response.text)


def get_area(token, id):
    url = 'http://grapes.mi-taxi.ca/taxi3/public/api/cms/v1/areas/{}'.format(
        id)
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def create_booking(token):
    url = "http://grapes.mi-taxi.ca/taxi3/public/api/customer-app/v1/bookings"
    payload = {
        "pickup_time": get_pickup_time(),
        "pickup": {
            "address": "pickup",
            "lat": constants.PICKUP_POINT.get('lat'),
            "lng": constants.PICKUP_POINT.get("lng")
        },
        "destination": {
            "address": "dest",
            "lat": constants.DIST_POINT.get('lat'),
            "lng": constants.DIST_POINT.get('lng')
        },
        "passengers_count": 1,
        "bags_count": 0,
        "car_type_id": 1
    }
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Bearer {}".format(token),
    }

    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.text)


def get_pickup_time():
    now = datetime.datetime.now()
    pickup_time = now + datetime.timedelta(minutes=10)
    return str(pickup_time.strftime("%Y-%m-%d %H:%M"))


def dispatch_booking(company_id, booking_id, driver_id):
    url = 'https://taxi3.rytalo.com/api/taxi3/manual_dispatch/'
    params = {
        'company_id': company_id,
        'booking_id': booking_id,
        'driver_id': driver_id
    }
    response = requests.get(url, params=params)
    return json.loads(response.text)


def see_booking(booking_id, token):
    url = "https://taxi3.rytalo.com/api/taxi3/booking/seen/"

    querystring = {"booking_id": booking_id}
    headers = {
        'Authorization': "Bearer {}".format(token),
        'cache-control': "no-cache",
    }

    response = requests.get(url, headers=headers, params=querystring)
    return json.loads(response.text)


def confirm_booking(booking_id, token):
    url = "https://taxi3.rytalo.com/api/taxi3/booking/confirm/"

    querystring = {"booking_id": booking_id}

    headers = {
        'Authorization': "Bearer {}".format(token),
        'cache-control': "no-cache",
    }

    response = requests.get(url, headers=headers, params=querystring)

    print("Confirm response: {}".format(response.text))


def start_booking(booking_id, token):
    url = "https://taxi3.rytalo.com/api/taxi3/booking/start/"

    querystring = {"booking_id": booking_id}

    headers = {
        'Authorization': "Bearer {}".format(token),
        'cache-control': "no-cache",
    }

    response = requests.get(url, headers=headers, params=querystring)

    print("Start response: {}".format(response.text))


def wait_for_passanger(booking_id, token):
    url = "https://taxi3.rytalo.com/api/taxi3/booking/wfp/"
    querystring = {"booking_id": booking_id}

    headers = {
        'Authorization': "Bearer {}".format(token),
        'cache-control': "no-cache"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print("Waiting for passanger response: {}".format(response.text))


def passenger_on_board(booking_id, token):
    url = "https://taxi3.rytalo.com/api/taxi3/booking/pob/"
    querystring = {"booking_id": booking_id}

    headers = {
        'Authorization': "Bearer {}".format(token),
        'cache-control': "no-cache"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print("passanger on board response: {}".format(response.text))


def complete_booking(booking_id, token):
    url = "https://taxi3.rytalo.com/api/taxi3/booking/completed/"
    r_point = rand_p()
    querystring = {"booking_id": booking_id,
                   "lat": r_point[0], "lng": r_point[1]}

    payload = "{}"
    headers = {
        'Authorization': "Bearer {}".format(token),
        'cache-control': "no-cache"
    }

    response = requests.post(url, data=payload, headers=headers, params=querystring)

    print("Complete response: {}".format(response.text))


def update_random_point(token, status=None, ride_status=None, ride_id=None):
    url = "https://taxi3.rytalo.com/api/taxi3/driver/track/"
    querystring = {}
    if status:
        querystring['status'] = status
    if ride_status:
        querystring['ride_status'] = ride_status
    if ride_id:
        querystring['ride_id'] = ride_id
    r_point = rand_p()
    querystring['lat'] = r_point[0]
    querystring['lng'] = r_point[1]

    headers = {
        'Authorization': "Bearer {}".format(token),
        'cache-control': "no-cache"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print("Update location response: {}".format(response.text))
    resp = json.loads(response.text)
    return resp.get("data")
