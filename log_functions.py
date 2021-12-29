DIRECTORY = "./logs/"

def file_log_event(Time, Event):
    f = open(DIRECTORY + "log.csv", "a")
    print("-- Event log: " + str(Time) + " : " + Event)
    f.write(str(Time) + ", " + Event + "\n")
    f.close()
    
def server_log_event(Time, Event):
    f = open(DIRECTORY + "server.csv", "a")
    print("-- Server log: " + str(Time) + " : " + Event)
    f.write(str(Time) + ", " + Event + "\n")
    f.close()

def server_error_log(Time, Event):
    f = open(DIRECTORY + "server_error.csv", "a")
    print("-- Server error: " + str(Time) + " : " + Event)
    f.write(str(Time) + ", " + Event + "\n")
    f.close()
