import random, time, datetime


startdate = datetime.datetime.today()
starttime = time.time()
filename = f"datasaves/{startdate.strftime(f"%d_%m_%Y_%H_%M_%S")}.txt"
#https://docs.espressif.com/projects/esptool/en/latest/esp32/
#https://projecthub.arduino.cc/ansh2919/serial-communication-between-python-and-arduino-663756


def create_file():
    with open(filename, "x") as file:
        file.write(f"Zenitsat communication log\n{startdate.strftime(f"%d/%m/%Y - %H:%M:%S")}\n\n00:00:000 >>> Start")
        file.close()

def save_data(data):
    with open(filename, "a") as file:
        timestamp = time_since_start()
        file.write(f"\n{timestamp} >>> {data}")
        file.close()

def read_data(filename):
    with open(filename, "r") as file:
        file.close()


def time_since_start(rounded= False):
    end = time.time()
    t = round(end-starttime, 3)
    if rounded:
        return int(((t/10)+1)*10)
    else:
        return f"{time.strftime("%M:%S", time.gmtime(int(t)))}:{str(t%1)[2:5]}"




#create_file()
#time.sleep(.1)
#save_data("hello")








# TO DO:
#   Finish grid system

# GRAPHICS:
#   matplotlib
#   print graphs in screen

# DATA:
#   calculate number of lost packages