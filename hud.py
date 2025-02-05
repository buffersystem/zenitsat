import numpy as np
import pandas as pd
import customtkinter as ctk
import awesometkinter as atk
import matplotlib.pyplot as plt
import mplcyberpunk as mcp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as TkAgg

from comms import *


class Screen(ctk.CTk):
    def __init__(self, width: int, height: int, name: str, font: str = "system"):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name
        self.font = font

        self.bars: list[tuple[ctk.CTkLabel, ctk.CTkProgressBar]] = []
        self.graphs: list[tuple[ctk.CTkLabel, TkAgg]] = []
        self.rows = 0
        self.columns = 0

        self.geometry(f"{width}x{height}")
        self.title(name)


    def create_grid(self):
        # grid
        for i in range(16):
            self.rowconfigure(index= i, uniform= "True", minsize= self.height/16, weight= 1)
        for i in range(16):
            self.columnconfigure(index= i, uniform= "True", minsize= self.width/16, weight= 1)
        
        # frame objects
        frame_stats = atk.Frame3d(parent= self).grid(row= 0, column= 0, sticky= "NWES", columnspan= 11, rowspan= 2)
        frame_pos = atk.Frame3d(parent= self).grid(row= 0, column= 11, sticky= "NWES", columnspan= 5, rowspan= 2)
        frame_bars = atk.Frame3d(parent= self).grid(row=2, column= 0, sticky= "NWES", columnspan= 16, rowspan= 5)
        frame_graphs = atk.Frame3d(parent= self).grid(row= 7, column= 0, sticky= "NWES", columnspan= 16, rowspan= 9)

        a = ctk.CTkProgressBar(master= self, height= 5, width= 100, bg_color= "#333333", progress_color= "cyan")
        a.grid(row= 4, column= 0, sticky= "NWES", padx= 20, pady= 10, columnspan= 4)
        b = ctk.CTkProgressBar(master= self, orientation= "vertical", bg_color= "#333333", progress_color= "cyan")
        b.grid(row= 0, column= 4, sticky= "NWES", padx= 20, pady= 10, rowspan= 2)
        c = ctk.CTkProgressBar(master= self, height= 5, width= 100, bg_color= "#333333", progress_color= "cyan")
        c.grid(row= 4, column= 4, sticky= "NWES", padx= 20, pady= 10, columnspan= 4)
        d = ctk.CTkProgressBar(master= self, height= 5, width= 100, bg_color= "#333333", progress_color= "cyan")
        d.grid(row= 4, column= 8, sticky= "NWES", padx= 20, pady= 10, columnspan= 4)
        e = ctk.CTkProgressBar(master= self, height= 5, width= 100, bg_color= "#333333", progress_color= "cyan")
        e.grid(row= 4, column= 12, sticky= "NWES", padx= 20, pady= 10, columnspan= 4)


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


    def add_graph(self, title: str, color: str, var: list[int], marker: str = "", xlabel: str = "", ylabel: str = ""):
        text = ctk.CTkLabel(master= self, fg_color= "#333333", text= title, font= (self.font, 18))
        figure, ax = plt.subplots(facecolor= "#333333")
        figure.set_facecolor("#333333")
        ax.set_facecolor("#333333")


        x = [i/10 for i in range(len(var))]
        filled = pd.Series(var).ffill()
        ax.plot(x, filled, color= color, marker= marker, linewidth= 2)
        ax.grid(alpha= .2)

        ax.set_xlabel(xlabel= xlabel, color= "white", family= self.font, size= 12)
        ax.set_ylabel(ylabel= ylabel, color= "white", family= self.font, size= 12)
        ax.tick_params(color= "white", labelcolor= "white", width= 1)

        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        mcp.make_lines_glow(ax)
        mcp.add_gradient_fill(ax, alpha_gradientglow= 0.4)
        widget = TkAgg(figure).get_tk_widget()

        return text, widget




ctk.set_appearance_mode("dark")
plt.style.use("dark_background")

root = Screen(960, 640, "Zenitsat control HUD")
root.create_grid()
text, widget = root.add_graph(title= "testing", color= "magenta", var= [0, 2, 1, 6, np.nan, 3, 4, np.nan, np.nan, 5, 8, 3, 6, 9, 2, np.nan, np.nan, 5, np.nan, 3, 1, 9])
text.grid(row= 6, column= 0, columnspan= 3, sticky= "NWES")
widget.grid(row= 7, column= 0, rowspan= 3, columnspan= 3, sticky= "NWES")




#graph, ax = plt.subplots(facecolor= "#333333")
#graph.set_facecolor("#333333")
#line, = ax.plot(x, y, color= "magenta", marker= "o", linewidth= 2)
#ax.grid(alpha= .2)
#ax.set_xlabel("Eje x", color= "white", family= "Cambria", size= 15)
#ax.set_ylabel("Eje y", color= "white", family= "Cambria", size= 15)
#ax.tick_params(color= "white", labelcolor= "white", width= 1)
#ax.spines["bottom"].set_color("white")
#ax.spines["left"].set_color("white")
#ax.spines["top"].set_visible(False)
#ax.spines["right"].set_visible(False)
#ax.set_facecolor("#333333")
#mcp.make_lines_glow(ax)
#mcp.add_gradient_fill(ax, alpha_gradientglow= 0.4)
#TkAgg(graph).get_tk_widget()
#plt.show()

text = ctk.CTkLabel(master= root, text= "testing", font= ("fixedsys", 24), fg_color= "#333333").grid(row= 0, column= 0, rowspan= 2, columnspan= 2, sticky= "NWES")

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