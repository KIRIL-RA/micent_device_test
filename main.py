from os import read
import threading, time
import datetime
import Exceptions
import adapter
from typing import cast
from log_functions import file_log_event
from fetch import subscribe
from fetch import send_data
from automode import autocontrol, check_connected_devices

ID = 111 # Device id
now = datetime.datetime.now()
sensor_error_counter = 0

auto_mode_parameters = {
    "min_temperature" : 17,
    "max_temperature" : 22,
    "start_lamp_hour" : 6,
    "stop_lamp_hour" : 22,
    "ventilation_seconds" : 10,
    "condition_seconds" : 10,
    "last_ventilation_hour" : 1
}

parameters = {"light1":False,
        "cooling":False,
        "ventilation":False,
        "humidity":0,
        "temperature":0,
        "temperature_on_street" : 0,
        "pump":False,
        "auto":True,
        "now_time": now}
previous_parameters = {}

connected_devices = {
    "light1":True,
    "cooling":True,
    "ventilation":True,
    "pump":True,
    "temperature_humidity_sensor": True
}

def read_sensors(parameters, connected_devices):
    global sensor_error_counter
    if(connected_devices["temperature_humidity_sensor"]):
        try:
            # Trying read sensors
            parameters["humidity"], parameters["temperature"] = adapter.get()
            # If all ok, reset number of error and start timer for next data getting
            sensor_error_counter = 0
            threading.Timer(2, read_sensors,args=[parameters, connected_devices]).start()

        except Exceptions.SensorReadingError:
            # If we catch error, updating error counter 
            sensor_error_counter += 1
            file_log_event(parameters["now_time"], "Error reading sensor data, attempt: " + str(sensor_error_counter))

            if(sensor_error_counter >= 5):
                # If we get max number of errors, disconnecting sensor
                connected_devices["temperature_humidity_sensor"] = False
                file_log_event(parameters["now_time"], "Temperature and humidity sensor not connected, please power off device, connect sensor and power on device")

            else:
                # Wait 2 seconds and trying get data again
                time.sleep(2)
                read_sensors(parameters, connected_devices)
            

if __name__ == "__main__":
    for key in parameters:
        previous_parameters[key] = parameters[key]

    now = datetime.datetime.now()
    parameters["now_time"] = now

    adapter.init()
    read_sensors(parameters, connected_devices)
    check_connected_devices(parameters, connected_devices)

    send_data(parameters, ID)
    th = threading.Thread(target=subscribe, args=(parameters, ID))

    while True:
        now = datetime.datetime.now()
        parameters["now_time"] = now

        if(parameters["auto"] == True): autocontrol(parameters, previous_parameters, auto_mode_parameters, connected_devices, ID)
        adapter.control(parameters)

        if(not th.is_alive()):
            th = threading.Thread(target=subscribe, args=(parameters, ID))
            th.start()
    th.join()

