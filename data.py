import random
import comms

altitude = []
speed = []
acceleration = []


def add_data():
    altitude.append(random.randint(1, 30))
    speed.append(random.randint(1, 60))
    acceleration.append(random.randint(1, 10))