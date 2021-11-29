from fetch import send_data

# FUNCTIONS FOR WORK IN AUTO MODE

def check_need_send_data(parameters, previous_parameters):
    # Check if any data has changed
    for key in parameters:
        if(parameters[key] != previous_parameters[key]):
            # If any parameters were changed, send new parameters to server
            return True
    return False

def control(parameters, previous_parameters):
    if check_need_send_data(parameters, previous_parameters): send_data(parameters, id)
    for key in parameters:
        previous_parameters[key] = parameters[key]