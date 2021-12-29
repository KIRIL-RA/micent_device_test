import threading
import datetime
import adapter
from fetch import subscribe
from fetch import send_data
from automode import autocontrol

ID = 111 # Device id
now = datetime.datetime.now()

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
        "humidity":10,
        "temperature":0,
        "temperature_on_street" : 0,
        "pump":False,
        "auto":True,
        "now_time": now}
previous_parameters = {}

if __name__ == "__main__":
    for key in parameters:
        previous_parameters[key] = parameters[key]

    adapter.init()
    parameters["humidity"], parameters["temperature"] = adapter.get()

    send_data(parameters, ID)
    th = threading.Thread(target=subscribe, args=(parameters, ID))

    while True:
        now = datetime.datetime.now()
        parameters["now_time"] = now

        if(parameters["auto"] == True): autocontrol(parameters, previous_parameters, auto_mode_parameters, ID)
        adapter.control(parameters)

        if(not th.is_alive()):
            th = threading.Thread(target=subscribe, args=(parameters, ID))
            th.start()
    th.join()

