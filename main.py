from asyncio.windows_events import NULL
from os import fsdecode
from re import sub
import threading
import requests
from requests.models import requote_uri

#KEY NAMES MUST MATCH IN "parameters" AND "previous_parameters"
parameters = {"light1":False,
        "cooling":False,
        "ventilation":False,
        "humidity":0,
        "temperature":0,
        "pump":False,
        "auto":False}

previous_parameters = {"light1":False,
        "cooling":False,
        "ventilation":False,
        "humidity":0,
        "temperature":0,
        "pump":False,
        "auto":False}

url = 'http://a0585513.xsph.ru/'
id = 111

def subscribe(parameters, id):
    global previous_parameters
    request = requests.get(url + 'test/subscribe_device?id=' + str(id))
    response = request.json()
    if(response["auto"] != 'undefined'):
        parameters["auto"] = bool(int(response["auto"]))
        if(parameters["auto"] == False):
            if(response["light1"] != 'undefined'): parameters["light1"] = bool(int(response["light1"]))
            if(response["cooling"] != 'undefined'): parameters["cooling"] = bool(int(response["cooling"]))
            if(response["ventilation"] != 'undefined'): parameters["ventilation"] = bool(int(response["ventilation"]))
            if(response["pump"] != 'undefined'): parameters["pump"] = bool(int(response["pump"]))
    
    print(parameters)

def send_data(parameters, id):
    send_url = url + 'test/send_data_from_device?id=' + str(id) + '&'
    send_url += 'temperature=' + str(int(parameters["temperature"])) + '&'
    send_url += 'humidity=' + str(int(parameters["humidity"])) + '&'
    send_url += 'light1=' + str(int(parameters["light1"])) + '&'
    send_url += 'ventilation=' + str(int(parameters["ventilation"])) + '&'
    send_url += 'cooling=' + str(int(parameters["cooling"])) + '&'
    send_url += 'pump=' + str(int(parameters["pump"])) + '&'
    send_url += 'auto=' + str(int(parameters["auto"]))
    requests.get(send_url)

def check_need_send_data(parameters, previous_parameters):
    for key in parameters:
        if(parameters[key] != previous_parameters[key]):
            send_data(parameters, id)       
            return True
    return False

def control():
    global previous_parameters
    check_need_send_data(parameters, previous_parameters)
    for key in parameters:
        previous_parameters[key] = parameters[key]

if __name__ == "__main__":
    th = threading.Thread(target=subscribe, args=(parameters, id))
    while True:
        if(not th.is_alive()):
            th = threading.Thread(target=subscribe, args=(parameters, id))
            th.start()
        control()
    th.join()

