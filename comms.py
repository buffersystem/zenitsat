import datetime, time
import customtkinter as ctk
import matplotlib.pyplot as plt
import mplcyberpunk as mcp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FTK


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
        self.barcount = 0
        self.rows = 0
        self.columns = 0

        self.geometry(f"{width}x{height}")
        self.title(name)

    def create_grid(self):
        return
        self.row = int(self.height/rows)
        for row in range(rows):
            self.rowconfigure(index= row, minsize= self.row, weight= 1)

        self.column = int(self.width/columns)
        for column in range(columns):
            self.columnconfigure(index= column, minsize= self.column, weight= 1)

    def add_pbar(self, title, font, var, varname):
        text = ctk.CTkLabel(master= self, text= title, font= font)
        varobj = ctk.Variable(value= var, name= varname)
        pbar = ctk.CTkProgressBar(master= root, corner_radius= 10, variable= varobj)
        self.barcount += 1
        return (text, pbar)

    def add_graph(self, title, font, var, varname):
        text = ctk.CTkLabel(master= self, text= title, font= font)
        varobj = ctk.Variable(value= var, name= varname)
        graph = None


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




#create_file()

root = Screen(960, 640, "Prueba")
root.create_grid(4, 4)
font = ctk.CTkFont(family= "Noto Sans", weight= "normal", size= 32)

speedtext = ctk.CTkLabel(master= root, width= root.column-40, height= 40, text= "Speed", font= font)
speedtext.grid(row= 0, column= 0, padx= 10, pady= 10)
speedbar = ctk.CTkProgressBar(master= root, width= root.column-40, height= 20, corner_radius= 10)
speedbar.grid(row= 0, column= 0, padx= 10, pady= 10)

root.mainloop()




# TO DO:
#   Nothing (for now)

# GRAPHICS:
#   matplotlib
#   print graphs in screen

# DATA:
#   calculate number of lost packages
