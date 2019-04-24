from helper import see_booking, confirm_booking, start_booking, update_random_point, \
    wait_for_passanger, passenger_on_board, complete_booking
import csv
import logging
import _thread
import time
from threading import Thread
from socketIO_client_nexus import SocketIO, LoggingNamespace, BaseNamespace

logging.getLogger('socketIO-client').setLevel(logging.ERROR)
logging.basicConfig()


class DriverNamespace(BaseNamespace):
    def on_connect(self):
        print("Connected to driver namespace")


def start_socket(token):
    print("Starting listen to token: {}".format(token))
    with SocketIO('http://grapes.mi-taxi.ca', 4201, LoggingNamespace, params={"token": token}) as socketIO:
        def on_dispatch(*args):
            message = args[0]
            booking = message.get("booking")
            socketIO.disconnect()
            assert booking.get('id')
            print("New booking with id: {}".format(booking.get('id')))

            seen = see_booking(booking.get("id"), token)
            assert seen.get('status') == 'SUCCESS'
            print('Booking seen successfully')


            confirm = confirm_booking(booking.get("id"), token)
            assert confirm.get('status') == 'SUCCESS'
            print('Booking confirmed successfully')
            time.sleep(5)

            start = start_booking(booking.get("id"), token)
            assert start['status'] == 'SUCCESS'
            print('Booking started successfully')
            time.sleep(5)

            update_point = update_random_point(
                token, "Busy", "WFP", booking.get("id"))
            assert update_point['status'] == 'SUCCESS'
            print('Driver moved to pick point successfully')

            wait = wait_for_passanger(booking.get("id"), token)
            assert wait['status'] == 'SUCCESS'
            print('Waiting for passanger successfully')
            time.sleep(5)

            onboard = passenger_on_board(booking.get("id"), token)
            assert onboard['status'] == 'SUCCESS'
            print('Passenger onboard successfully')
            time.sleep(5)

            for _ in range(10):
                update_random_point(token, "Busy", "POB", booking.get("id"))
                print('Driver on his way to destinations')
                time.sleep(2)

            complete = complete_booking(booking.get("id"), token)
            assert complete['status'] == 'SUCCESS'
            print('Booking completed successfully')

        driver_namespace = socketIO.define(DriverNamespace, '/drivers')
        driver_namespace.on("dispatch", on_dispatch)
        socketIO.wait()


def init_socket(token):
    print('inside socket: ', token)
    try:
        t = Thread(target=start_socket, args=(token,))
        t.start()
    except:
        print("Error: unable to start thread")
