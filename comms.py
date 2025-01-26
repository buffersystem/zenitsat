import datetime, pathlib
import customtkinter as ctk


starttime = datetime.datetime.today()
#https://docs.espressif.com/projects/esptool/en/latest/esp32/
#https://projecthub.arduino.cc/ansh2919/serial-communication-between-python-and-arduino-663756


class Screen(ctk.CTk):
    def __init__(self, size: str, title: str):
        super().__init__()
        self.geometry(size)   
        self.title(title)

        # add widgets


    # add methods 
    def save_data():
        a = open("data", "w")




def create_file(datetime):
    filename = f"datasaves/{datetime.strftime("%d_%m_%Y_%H_%M_%S")}.txt"
    with open(filename, "x") as file:
        file.write(f"Zenitsat communication log\n{datetime.strftime("%d/%m/%Y - %H:%M:%S")}\n")
        file.close()
    return filename




filename = create_file(starttime)

main = Screen("960x640", "Prueba")
main.mainloop()




# TO DO:
#   add clock for timestamps
#   save data in document (with timestamps)

# GRAPHICS:
#   matplotlib
#   print graphs in screen

# DATA:
#   save time since start
#   calculate number of lost packages
