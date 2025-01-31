import pygame
import pygame.freetype as ft

108, 378, 216, 108
540, 378, 216, 108

# upload sprites
title_screen = pygame.image.load("assets/title_screen.png")
background = pygame.image.load("assets/background_cup.png")
board = pygame.image.load("assets/board.png")
button = pygame.image.load("assets/button.png")

token_red = pygame.image.load("assets/token_red.png")
token_green = pygame.image.load("assets/token_green.png")
token_orange = pygame.image.load("assets/token_orange.png")
token_blue = pygame.image.load("assets/token_blue.png")
tokens = [token_red, token_green, token_orange, token_blue]

dice_default = pygame.image.load("assets/dice_default.png")
dice_selected = pygame.image.load("assets/dice_selected.png")
dice_used = pygame.image.load("assets/dice_used.png")
dice_sel_red = pygame.image.load("assets/dice_selected_red.png")
dice_sel_green = pygame.image.load("assets/dice_selected_green.png")
dice_sel_orange = pygame.image.load("assets/dice_selected_orange.png")
dice_sel_blue = pygame.image.load("assets/dice_selected_blue.png")

dice_1 = pygame.image.load("assets/dice_1.png")
dice_2 = pygame.image.load("assets/dice_2.png")
dice_3 = pygame.image.load("assets/dice_3.png")
dice_4 = pygame.image.load("assets/dice_4.png")
dice_5 = pygame.image.load("assets/dice_5.png")
dice_6 = pygame.image.load("assets/dice_6.png")
dice_5_special = pygame.image.load("assets/dice_5_special.png")
dice_7_special = pygame.image.load("assets/dice_7_special.png")

dices_num = [None, dice_1, dice_2, dice_3, dice_4, dice_5, dice_6]

winner_cup = pygame.image.load("assets/winner_cup.png")
turn_indicator = pygame.image.load("assets/turn_indicator.png")


# upload fonts
ft.init()
font = ft.Font("fonts/PublicPixel.ttf")


# create colors
RED = (163, 5, 55)
RED_D = (107, 14, 45)
GREEN = (23, 145, 58)
GREEN_D = (18, 107, 37)
ORANGE = (196, 119, 55)
ORANGE_D = (158, 75, 16)
BLUE = (79, 112, 219)
BLUE_D = (49, 78, 163)
YELLOW_SL = (250, 237, 205)
BLACK = (0, 0, 0)