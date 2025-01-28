import datetime, time, pathlib
import awesometkinter as atk
import customtkinter as ctk
import tkinter.ttk as ttk
import tkinter as tk


startdate = datetime.datetime.today()
starttime = time.time()
filename = f"datasaves/{startdate.strftime(f"%d_%m_%Y_%H_%M_%S")}.txt"
#https://docs.espressif.com/projects/esptool/en/latest/esp32/
#https://projecthub.arduino.cc/ansh2919/serial-communication-between-python-and-arduino-663756


class Screen(ctk.CTk):
    def __init__(self, width: int, height: int, name: str):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name

        self.geometry(f"{width}x{height}")
        self.title(name)

    def create_grid(self, rows, columns):
        for row in range(rows):
            self.rowconfigure(index= row, minsize= int(self.height/rows), weight= 1)
        for column in range(columns):
            self.columnconfigure(index= column, minsize= int(self.width/columns), weight= 1)


def create_file():
    with open(filename, "x") as file:
        file.write(f"Zenitsat communication log\n{startdate.strftime(f"%d/%m/%Y - %H:%M:%S")}\n")
        file.close()

def save_data():
    with open(filename, "a") as file:
        timestamp = time_since_start()
        file.write(f"\n{timestamp} >>> None")
        file.close()

def read_data(filename):
    with open(filename, "r") as file:
        file.close()


def time_since_start():
    end = time.time()
    t = round(end-starttime, 3)
    return f"{time.strftime("%M:%S", time.gmtime(int(t)))}:{str(t%1)[2:]}"


create_file()

main = Screen(960, 640, "Prueba")
main.create_grid(4, 4)

bar = ctk.CTkProgressBar(master= main, width= 100, height= 20, corner_radius= 10)
bar.grid(row= 1, column= 1 , padx= 0, pady= 0)

main.mainloop()




# TO DO:
#   Nothing (for now)

# GRAPHICS:
#   matplotlib
#   print graphs in screen

# DATA:
#   calculate number of lost packages
