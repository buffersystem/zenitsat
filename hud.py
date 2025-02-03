import customtkinter as ctk
import awesometkinter as atk
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


    def create_fonts(self):
        self.font_title = ctk.CTkFont(family= "Noto Sans", weight= "bold", size= 24)
        self.font_subtitle = ctk.CTkFont(family= "Noto Sans", weight= "bold", size= 20)
        self.font_text = ctk.CTkFont(family= "Noto Sans", weight= "normal", size= 16)
        self.font_itallic = ctk.CTkFont(family= "Noto Sans", weight= "normal", size= 16, slant= "italic")

    def create_grid(self):
        # grid
        for i in range(16):
            self.rowconfigure(index= i, uniform= "True", weight= 1)
        for i in range(16):
            self.columnconfigure(index= i, uniform= "True", weight= 1)
        
        # frame objects
        frame_stats = atk.Frame3d(parent= self).grid(row= 0, column= 0, sticky= "NWES", columnspan= 11, rowspan= 2)
        frame_pos = atk.Frame3d(parent= self).grid(row= 0, column= 11, sticky= "NWES", columnspan= 5, rowspan= 2)
        frame_bars = atk.Frame3d(parent= self).grid(row=2, column= 0, sticky= "NWES", columnspan= 16, rowspan= 5)
        frame_graphs = atk.Frame3d(parent= self).grid(row= 7, column= 0, sticky= "NWES", columnspan= 16, rowspan= 9)

        a = ctk.CTkProgressBar(master= self, height= 5, width= 100, bg_color= "#333333", progress_color= "cyan")
        a.grid(row= 4, column= 0, sticky= "NWES", padx= 20, columnspan= 15)
        b = ctk.CTkProgressBar(master= self, orientation= "vertical", bg_color= "#333333", progress_color= "cyan")
        b.grid(row= 0, column= 4, sticky= "NWES", padx= 20, pady= 10, rowspan= 2)


    def create_settings(self):
        label_title = ctk.CTkLabel(master= self, text= "Widget settings", font= self.font_title)
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


def sep_by(num: int, len: int):
    n = num
    sep = []
    while n > len:
        n -= len
        sep.append(len)
    sep.append(n)
    return sep




ctk.set_appearance_mode("dark")
plt.style.use("dark_background")

root = Screen(960, 640, "Zenitsat control HUD")
root.create_grid()



#graph, axis = plt.subplots(dpi= 80, facecolor= "#000000")
#graph.set_facecolor("#000000")
#line, = axis.plot(x, y, color= "aqua", marker= "o", linewidth= 2)
#axis.grid(alpha= .2)
#axis.set_xlabel("Eje x", color= "white", family= "Cambria", size= 15)
#axis.set_ylabel("Eje y", color= "white", family= "Cambria", size= 15)
#axis.tick_params(color= "white", labelcolor= "white", length= 6, width= 2)
#axis.spines["bottom"].set_color("white")
#axis.spines["left"].set_color("white")
#mcp.make_lines_glow(axis)
#mcp.add_gradient_fill(alpha_gradientglow= 0.6)
#plt.show()


#add_data()
#root.add_graph(title= "Altitude", font= root.font_subtitle, var= altitude)
#root.add_graph(title= "Speed", font= root.font_subtitle, var= speed)
#root.add_graph(title= "Acceleration", font= root.font_subtitle, var= acceleration)
#root.plot_data()


root.mainloop()
#running = True
#while running:
    #add_data()
    #root.update_idletasks()
    #root.update()