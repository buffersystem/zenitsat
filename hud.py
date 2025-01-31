import customtkinter as ctk
import matplotlib.pyplot as plt
import mplcyberpunk as mcp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as TkAgg

from data import *


class Screen(ctk.CTk):
    def __init__(self, width: int, height: int, name: str):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name
        self.bars: list[tuple[ctk.CTkLabel, ctk.CTkProgressBar]] = []
        self.graphs: list[tuple[ctk.CTkLabel]] = []
        self.rows = 0
        self.columns = 0

        self.geometry(f"{width}x{height}")
        self.title(name)

        self.create_fonts()


    def grid(self, rows = 2, columns = 3):
        for row in range(rows):
            self.rowconfigure(index= row*2, minsize= 100, weight= 1)
            self.rowconfigure(index= (row*2)+1, minsize= 100, weight= 1)
        for column in range(columns):
            self.columnconfigure(index= column, minsize= 200, weight= 1)

    def plot_data(self):
        for (text, bar) in self.bars:
            text.grid(row= 0, column= self.bars.index((text, bar)))
            bar.grid(row= 1, column= self.bars.index((text, bar)))

        for (text, graph, axis) in self.graphs:
            text.grid(row= 2, column= self.graphs.index((text, graph)))
            axis.grid(row= 3, column= self.graphs.index((text, graph)), expand= True, fill= "both")
            TkAgg(figure= graph, master= self).get_tk_widget().grid(row= 3, column= self.bars.index(text), expand= True, fill= "both")


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
        bar_temperature = ctk.CTkCheckBox(master= self, text= "Temperature", font= self.font_text)
        bar_pressure = ctk.CTkCheckBox(master= self, text= "Pressure", font= self.font_text)
        bar_humidity = ctk.CTkCheckBox(master= self, text= "Humidity", font= self.font_text)
        bar_altitude = ctk.CTkCheckBox(master= self, text= "Altitude", font= self.font_text)
        bar_speed = ctk.CTkCheckBox(master= self, text= "Speed", font= self.font_text)
        bar_acceleration = ctk.CTkCheckBox(master= self, text= "Acceleration", font= self.font_text)
        self.bars = [bar_temperature, bar_pressure, bar_humidity, bar_altitude, bar_speed, bar_acceleration]

        space2 = add_space(self, 20)
        space2.pack()
        label_bars.pack(pady= 5)
        for bar in self.bars:
            bar.pack(pady= 5)
        
        # graph options
        label_graphs = ctk.CTkLabel(master= self, text= "Graphs", font= self.font_subtitle)
        graph_temptime = ctk.CTkCheckBox(master= self, text= "Temperature over time", font= self.font_text)
        graph_tempalt = ctk.CTkCheckBox(master= self, text= "Temperature over altitude", font= self.font_text)
        graph_prestime = ctk.CTkCheckBox(master= self, text= "Pressure over time", font= self.font_text)
        graph_presalt = ctk.CTkCheckBox(master= self, text= "Pressure over altitude", font= self.font_text)
        graph_humitime = ctk.CTkCheckBox(master= self, text= "Humidity over time", font= self.font_text)
        graph_humialt = ctk.CTkCheckBox(master= self, text= "Humidity over altitude", font= self.font_text)
        graph_altitude = ctk.CTkCheckBox(master= self, text= "Altitude over time", font= self.font_text)
        graph_speed = ctk.CTkCheckBox(master= self, text= "Speed over time", font= self.font_text)
        graph_acceleration = ctk.CTkCheckBox(master= self, text= "Acceleration over time", font= self.font_text)
        # wind speed and direction
        self.graphs = [graph_temptime, graph_tempalt, graph_prestime, graph_presalt, graph_humitime, graph_humialt, graph_altitude, graph_speed, graph_acceleration]

        space3 = add_space(self, 20)
        space3.pack()
        label_graphs.pack(pady= 5)
        for graph in self.graphs:
            graph.pack(pady= 5)


    def add_pbar(self, title, font, var):
        text = ctk.CTkLabel(master= self, text= title, font= font)
        varobj = ctk.Variable(value= var, varname= "var")
        pbar = ctk.CTkProgressBar(master= self, corner_radius= 10, variable= varobj)
        self.bars.append((text, pbar))


    def add_graph(self, title, font, var):
        text = ctk.CTkLabel(master= self, text= title, font= font)
        graph, axis = plt.plot(var, "-r")
        self.graphs.append((text, graph, axis))



def add_space(master, height: int):
    return ctk.CTkLabel(master= master, height= height, text= "")

def sep_by(num: int, len: int):
    n = num
    sep = []
    while n > len:
        n -= len
        sep.append(len)
    sep.append(n)
    return sep







root = Screen(960, 640, "Zenitsat control HUD")
root.grid()
plt.plot([0, 2, 9, 4], "-r")
plt.show()


#add_data()
#root.add_graph(title= "Altitude", font= root.font_subtitle, var= altitude)
#root.add_graph(title= "Speed", font= root.font_subtitle, var= speed)
#root.add_graph(title= "Acceleration", font= root.font_subtitle, var= acceleration)
#root.plot_data()


running = True
while running:
    #add_data()
    root.update_idletasks()
    root.update()