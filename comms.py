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

        self.create_fonts()


    def create_grid(self, bars: list, graphs: list):
        bar_count = sep_by(len(bars), 3)
        graph_count = sep_by(len(graphs), 3)

        self.bar_frame = ctk.CTkFrame(master= self, height= 100*len(bar_count))
        self.bar_frame.rowconfigure(index= 0, minsize= 80, weight= 1)
        for row in range(len(bar_count)):
            self.bar_frame.rowconfigure(index= row+1, minsize= 100, weight= 1)
        for column in range(bar_count[0]):
            self.bar_frame.columnconfigure(index= column, minsize= 200, weight= 1)

        self.graph_frame = ctk.CTkFrame(master= self, height= 200*len(graph_count))
        self.graph_frame.rowconfigure(index= 0, minsize= 80, weight= 1)
        for row in range(len(graph_count)):
            self.graph_frame.rowconfigure(index= row+1, minsize= 200, weight= 1)
        for column in range(graph_count[0]):
            self.graph_frame.columnconfigure(index= column, minsize= 200, weight= 1)


    def create_fonts(self):
        self.font_title = ctk.CTkFont(family= "Noto Sans", weight= "bold", size= 24)
        self.font_subtitle = ctk.CTkFont(family= "Noto Sans", weight= "bold", size= 20)
        self.font_text = ctk.CTkFont(family= "Noto Sans", weight= "normal", size= 16)
        self.font_itallic = ctk.CTkFont(family= "Noto Sans", weight= "normal", size= 16, slant= "italic")


    def create_settings(self):
        label_title = ctk.CTkLabel(master= self, text= "Widget settings", font= self.font_title)
        space1 = add_space(self, 30)
        space1.pack()
        label_title.pack(pady= 5)

        # bar options
        label_bars = ctk.CTkLabel(master= self, text= "Bars", font= self.font_subtitle)
        bar_speed = ctk.CTkCheckBox(master= self, text= "Speed", font= self.font_text)
        bar_temperature = ctk.CTkCheckBox(master= self, text= "Temperature", font= self.font_text)
        bar_pressure = ctk.CTkCheckBox(master= self, text= "Pressure", font= self.font_text)
        bar_humidity = ctk.CTkCheckBox(master= self, text= "Humidity", font= self.font_text)
        bar_altitude = ctk.CTkCheckBox(master= self, text= "Altitude", font= self.font_text)
        bar_acceleration = ctk.CTkCheckBox(master= self, text= "Acceleration", font= self.font_text)
        self.bars = [bar_speed, bar_temperature, bar_pressure, bar_humidity, bar_altitude, bar_acceleration]

        space2 = add_space(self, 20)
        space2.pack()
        label_bars.pack(pady= 5)
        for bar in self.bars:
            bar.pack(pady= 5)
        
        # graph options
        label_graphs = ctk.CTkLabel(master= self, text= "Graphs", font= self.font_subtitle)
        graph_speed = ctk.CTkCheckBox(master= self, text= "Speed", font= self.font_text)
        graph_temperature = ctk.CTkCheckBox(master= self, text= "Temperature", font= self.font_text)
        graph_pressure = ctk.CTkCheckBox(master= self, text= "Pressure", font= self.font_text)
        graph_humidity = ctk.CTkCheckBox(master= self, text= "Humidity", font= self.font_text)
        graph_altitude = ctk.CTkCheckBox(master= self, text= "Altitude", font= self.font_text)
        graph_acceleration = ctk.CTkCheckBox(master= self, text= "Acceleration", font= self.font_text)
        self.graphs = [graph_speed, graph_temperature, graph_pressure, graph_humidity, graph_altitude, graph_acceleration]

        space3 = add_space(self, 20)
        space3.pack()
        label_graphs.pack(pady= 5)
        for graph in self.graphs:
            graph.pack(pady= 5)


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


def sep_by(num: int, len: int):
    n = num
    sep = []
    while n > len:
        n -= len
        sep.append(len)
    sep.append(n)
    return sep


def add_space(master, height: int):
    return ctk.CTkLabel(master= master, height= height, text= "")

#create_file()
root = Screen(960, 640, "Zenitsat control HUD")
#settings = Screen(240, 960, "Settings")
root.create_settings()
root.mainloop()




# TO DO:
#   Finish grid system

# GRAPHICS:
#   matplotlib
#   print graphs in screen

# DATA:
#   calculate number of lost packages
