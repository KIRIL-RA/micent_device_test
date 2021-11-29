import threading
from fetch import subscribe

ID = 111 # Device id

#KEY NAMES MUST MATCH IN "parameters" AND "previous_parameters"
parameters = {"light1":False,
        "cooling":False,
        "ventilation":False,
        "humidity":0,
        "temperature":0,
        "pump":False,
        "auto":False}
previous_parameters = parameters

if __name__ == "__main__":
    th = threading.Thread(target=subscribe, args=(parameters, ID))
    while True:
        if(not th.is_alive()):
            th = threading.Thread(target=subscribe, args=(parameters, ID))
            th.start()
    th.join()

