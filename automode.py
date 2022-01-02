from fetch import send_data
from threading import Timer
from log_functions import file_log_event
# FUNCTIONS FOR WORK IN AUTO MODE

def check_need_send_data(parameters, previous_parameters):
    # Check if any data has changed
    for key in parameters:
        if(parameters[key] != previous_parameters[key] and key != "now_time"):
            # If any parameters were changed, send new parameters to server
            return True
    return False

def check_connected_devices(parameters, connected_devices):
    if(not connected_devices["temperature_humidity_sensor"]): file_log_event(parameters["now_time"], "Temperature control disabled decause humidity-temperaute sensor disconnected")

def autocontrol(parameters, previous_parameters, automode_parameters, connected_devices, id):
    if check_need_send_data(parameters, previous_parameters):
        send_data(parameters, id)

    for key in parameters:
        previous_parameters[key] = parameters[key]

    if(connected_devices["temperature_humidity_sensor"]): temperature_control(parameters, automode_parameters)
    light_control(parameters, automode_parameters)
    ventilation_control(parameters, automode_parameters)

def ventilation_control(parameters, automode_parameters):
    if(parameters["now_time"].hour != automode_parameters["last_ventilation_hour"]):
        #If ventilation not were in this hour, then start ventilation
        automode_parameters["last_ventilation_hour"] = parameters["now_time"].hour
        parameters["ventilation"] = True
        file_log_event(parameters["now_time"], "Ventilation started, caller: " + "ventilation_control")
        Timer(automode_parameters["ventilation_seconds"], ventilation_logic, [parameters, automode_parameters, "ventilation_control"]).start()

def light_control(parameters, automode_parameters):
    if(parameters["now_time"].hour >= automode_parameters["start_lamp_hour"] and parameters["now_time"].hour < automode_parameters["stop_lamp_hour"]):
        if(parameters["light1"] == False):
            #If light time and light not working, then start lightning
            file_log_event(parameters["now_time"], "Light started")
            parameters["light1"] = True
    elif(parameters["light1"] == True):
        #If not light time and light working, then stop lightning
        file_log_event(parameters["now_time"], "Light stoped")
        parameters["light1"] = False

def temperature_control(parameters, automode_parameters):
    if(parameters["temperature"] >= automode_parameters["max_temperature"]):
        if(parameters["temperature_on_street"] >= automode_parameters["max_temperature"]):
            #If temperature on street bigger, that max temperature then launch condition
            pass
        elif(parameters["ventilation"] == False):
            #If temperature on street lower, that max temeperature then launch ventilation
            parameters["ventilation"] = True
            file_log_event(parameters["now_time"], "Ventilation started, caller: " + "temperature_control")
            Timer(automode_parameters["ventilation_seconds"], ventilation_logic, [parameters, automode_parameters, "temperature_control"]).start()

def ventilation_logic(parameters, automode_parameters, caller):
    if (caller == "temperature_control"):
        #If ventilation were started for temperature control, check temperature
        if(parameters["temperature"] >= automode_parameters["max_temperature"]):
            Timer(automode_parameters["ventilation_seconds"], ventilation_logic, [parameters, automode_parameters, "temperature_control"]).start()
            file_log_event(parameters["now_time"], "Ventilation continued, caller: " + caller)
        else:
            parameters["ventilation"] = False
            file_log_event(parameters["now_time"], "Ventilation stoped, caller: " + caller)

    if(caller == "ventilation_control"):
        parameters["ventilation"] = False
        file_log_event(parameters["now_time"], "Ventilation stoped, caller: " + caller)