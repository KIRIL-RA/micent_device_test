import Exceptions

def control(parameters):
    pass

def get():
    dataIsValid = True
    if (dataIsValid):
        humidity = 33
        temperature = 20
        return humidity, temperature
    else:
        raise Exceptions.SensorReadingError("Error reading data")

def init():
    pass
