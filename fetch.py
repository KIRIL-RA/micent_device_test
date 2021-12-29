from requests.models import requote_uri
import requests
from log_functions import server_error_log, server_log_event
# FUNCTIONS FOR WORK WITH NETWORK   

url = 'http://193.104.57.76/' # Final url
#url = 'http://localhost/' # Test url

def subscribe(parameters, id):
    try:
        # Wait for get data about control from server
        request = requests.get(url + 'test/subscribe_device?id=' + str(id))
        if(request.status_code == 200):
            response = request.json()
            
            if not "data_request" in response:
                if(response["auto"] != 'undefined'):
                    #parameters["auto"] = bool(int(response["auto"]))
                    # If auto mode active, we dont't need to update control parameters
                    if(parameters["auto"] == False):
                        if(response["light1"] != 'undefined'): parameters["light1"] = bool(int(response["light1"]))
                        if(response["cooling"] != 'undefined'): parameters["cooling"] = bool(int(response["cooling"]))
                        if(response["ventilation"] != 'undefined'): parameters["ventilation"] = bool(int(response["ventilation"]))
                        if(response["pump"] != 'undefined'): parameters["pump"] = bool(int(response["pump"]))
    except Exception:
        server_error_log(parameters["now_time"], Exception)
    finally:
        # Send to server response, that we recieve data
        send_data(parameters, id)

def send_data(parameters, id):
    # Forming data to send
    send_url = url + 'test/send_data_from_device?id=' + str(id) + '&'
    send_url += 'temperature=' + str(int(parameters["temperature"])) + '&'
    send_url += 'humidity=' + str(int(parameters["humidity"])) + '&'
    send_url += 'light1=' + str(int(parameters["light1"])) + '&'
    send_url += 'ventilation=' + str(int(parameters["ventilation"])) + '&'
    send_url += 'cooling=' + str(int(parameters["cooling"])) + '&'
    send_url += 'pump=' + str(int(parameters["pump"])) + '&'
    send_url += 'auto=' + str(int(parameters["auto"]))

    # Send data to server
    requests.get(send_url)
    server_log_event(parameters["now_time"], "Sended data")