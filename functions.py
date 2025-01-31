import random, pygame
import numpy as np
from assets import *


hor = list(int(i) for i in np.r_[1:9, 26:43, 60:69])
hor.extend([34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 68.1, 68.2, 68.3, 68.4, 68.5, 68.6, 68.7, 68.8])
ver = list(int(i) for i in np.r_[9:26, 43:60])
ver.extend([17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8, 51.1, 51.2, 51.3, 51.4, 51.5, 51.6, 51.7, 51.8])
cas_home = [5, 22, 39, 56]
cas_shield = [12, 29, 46, 63]

boxes_num = hor + ver
boxes_num.append(100)
boxes_num.sort()

special_boxes = {8: [(-28, 0), (4, 0)], 9: [(0, -28), (0, 4)], 25: [(0, -4), (0, 28)], 26: [(-28, 0), (4, 0)],
                42: [(-4, 0), (28, 0)], 43: [(0, -28), (0, 4)], 59: [(0, -4), (0, 28)], 60: [(-4, 0), (28, 0)]}

triple_boxes = {17.8: [(1012, 526), (1038, 510), (1038, 542)], 34.8: [(946, 460), (930, 434), (962, 434)],
                51.8: [(880, 526), (854, 510), (854, 542)], 68.8: [(946, 592), (930, 618), (962, 618)]}

boxes_px = [552, 590, 628, 666, 704, 742, 780, 818, 848, 946, 1044, 1074, 1112, 1150, 1188, 1226, 1264, 1302, 1340]

boxes_array = np.array([[   0,   0,   0,   0,   0,   0,   0,   0,  35,34  ,  33,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  36,34.1,  32,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,0.11,   0,0.13,   0,   0,   0,  37,34.2,  31,   0,   0,   0,0.41,   0,0.43,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  38,34.3,  30,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,0.12,   0,0.14,   0,   0,   0,  39,34.4,  29,   0,   0,   0,0.42,   0,0.44,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  40,34.5,  28,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  41,34.6,  27,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  42,34.7,  26,   0,   0,   0,   0,   0,   0,   0,   0],
                        [  50,  49,  48,  47,  46,  45,  44,  43,   0,34.8,   0,  25,  24,  23,  22,  21,  20,  19,  18],
                        [  51,51.1,51.2,51.3,51.4,51.5,51.6,51.7,51.8, 100,17.8,17.7,17.6,17.5,17.4,17.3,17.2,17.1,  17],
                        [  52,  53,  54,  55,  56,  57,  58,  59,   0,68.8,   0,   9,  10,  11,  12,  13,  14,  15,  16],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  60,68.7,   8,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  61,68.6,   7,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  62,68.5,   6,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,0.21,   0,0.23,   0,   0,   0,  63,68.4,   5,   0,   0,   0,0.31,   0,0.33,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  64,68.3,   4,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,0.22,   0,0.24,   0,   0,   0,  65,68.2,   3,   0,   0,   0,0.32,   0,0.34,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  66,68.1,   2,   0,   0,   0,   0,   0,   0,   0,   0],
                        [   0,   0,   0,   0,   0,   0,   0,   0,  67,68  ,   1,   0,   0,   0,   0,   0,   0,   0,   0]], np.float16)


class Player:
    def __init__ (self, name, mclr, dclr, dice_sel, turn, home, entry, hud):
        self.id = turn   # Indicate the turn
        self.name = name
        self.mclr = mclr   # main color
        self.dclr = dclr   # dark color
        self.wins = 0
        self.tokens_win = 0

        self.home = home
        self.entry = entry

        if self.id != 0:
            self.dice_1 = Dice(id= int(f"1{self.id}1"))
            self.dice_2 = Dice(id= int(f"1{self.id}2"))
        self.selected_dice = 0
        self.dices_thrown = False
        self.dice_sel = dice_sel

        self.double = False
        self.double_count = 0
        self.ff = False
        self.seven = False

        self.tokens = [Token]
        self.tokens.clear()
        self.home_tokens = 4
        self.barrier = False

        self.hud = hud
        self.hudx = hud[0]
        self.hudy = hud[1]

        self.player_text, player_rect = ft.Font.render(font, f"PLAYER {self.id}", self.dclr, size= 40)
        self.name_text, name_rect = ft.Font.render(font, str(self.name), self.mclr, size= 20)
        self.wins_text, wins_rect = ft.Font.render(font, f"{self.wins} wins", YELLOW_SL, size= 20)


    def throw_dices(self):
        dices = [self.dice_1, self.dice_2]
        self.dice_1.value = random.randint(1, 6)
        self.dice_2.value = random.randint(1, 6)

        for d in dices:
            d.bg = dice_default
            if d.value == 5 and self.home_tokens > 0:
                d.fg = dice_5_special
            elif self.seven == True and d.value == 6:
                d.value = 7
                d.fg = dice_7_special
            else:
                d.fg = dices_num[d.value]

        self.dices_thrown = True
        if self.dice_1.value >= 6 and self.dice_2.value >= 6:
            self.double = True
            if self.home_tokens == 4:
                self.ff = True

        elif self.home_tokens == 4 and self.dice_1.value != 5 and self.dice_2.value != 5:
            self.dice_1.used = True
            self.dice_1.bg = dice_used
            self.dice_2.used = True
            self.dice_2.bg = dice_used


class Box:
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo
        self.barrier = False
        self.tokens = [Token]
        self.tokens.clear()

        self.coord = np.argwhere(boxes_array == id).flatten().tolist()
        self.px = [boxes_px[self.coord[1]], boxes_px[self.coord[0]]-420]

        self.orient = None
        if self.id in hor:
            self.orient = "hor"
        else:
            self.orient = "ver"


    def calc_token_pos(self):
        if self.id == 100:
            for t in self.tokens:
                t.calc_pos(self.tokens.index(t), orient= None, win= True)

        elif len(self.tokens) == 0:
            return

        elif len(self.tokens) == 1:
            self.tokens[0].calc_pos(0, self.orient)

        else:
            for t in self.tokens:
                t.calc_pos(self.tokens.index(t)+1, self.orient)


class Dice:
    px_dices = [[144, 334], [304, 334], [144, 748], [304, 748], [1488, 748], [1648, 748], [1488, 334], [1648, 334]]
    counter = 0

    def __init__(self, id):
        self.id = id
        self.value = 0
        self.used = False
        self.bg = dice_used
        self.fg = None

        self.px = Dice.px_dices[Dice.counter]
        self.hitbox = pygame.Rect

        if id != 0:
            Dice.counter += 1


class Token:
    win_px = [(930, 510), (962, 510), (930, 542), (962, 542)]

    def __init__(self, id: int):
        self.id = id
        self.barrier = False
        self.sprite = tokens[int(id/10)-1]

        self.pos = id/100
        self.coord = np.argwhere(boxes_array == self.pos).flatten().tolist()   # eliminar
        self.px = [boxes_px[self.coord[1]], boxes_px[self.coord[0]]-420]   # eliminar
        self.hitbox = pygame.Rect


    def calc_pos(self, num, orient, win= False):
        self.coord = np.argwhere(boxes_array == self.pos).flatten().tolist()

        if num == 0:
            self.px = (boxes_px[self.coord[1]], boxes_px[self.coord[0]]-420)

        elif win:
            self.px = Token.win_px[num]

        else:
            if self.pos in special_boxes:
                dx, dy = special_boxes[self.pos][num-1]
                self.px = (boxes_px[self.coord[1]]+dx, boxes_px[self.coord[0]]+dy-420)

            elif self.pos in triple_boxes:
                self.px = triple_boxes[self.pos][num-1]

            else:
                if orient == "hor":
                    if num == 1:
                        self.px = (boxes_px[self.coord[1]]-20, boxes_px[self.coord[0]]-420)
                    else:
                        self.px = (boxes_px[self.coord[1]]+20, boxes_px[self.coord[0]]-420)

                elif orient == "ver":
                    if num == 1:
                        self.px = (boxes_px[self.coord[1]], boxes_px[self.coord[0]]-440)
                    else:
                        self.px = (boxes_px[self.coord[1]], boxes_px[self.coord[0]]-400)


    def move(self, start: Box, end: Box):
        self.pos = end.id
        start.tokens.remove(self)
        end.tokens.append(self)


    def eaten(self, end: Box, home: Box):
        
        self.pos = float(self.id/100)
        end.tokens.remove(self)
        home.tokens.append(self)


def create_objects():
    global boxes_num, cas_home, cas_shield

    boxes_obj = [Box(0, 0)]
    dices_obj = [Dice(0)]
    tokens_obj = [Token(0)]

    player_1 = Player(name= "Alejandro", mclr= RED, dclr= RED_D, dice_sel= dice_sel_red, turn= 1, home= 39, entry= 34, hud= (140, 182))
    player_2 = Player(name= "Juan Carlos", mclr= GREEN, dclr= GREEN_D, dice_sel= dice_sel_green, turn= 2, home= 56, entry= 51, hud= (140, 596))
    player_3 = Player(name= "Julieta", mclr= ORANGE, dclr= ORANGE_D, dice_sel= dice_sel_orange, turn= 3, home= 5, entry= 68, hud= (1484, 596))
    player_4 = Player(name= "Heimerdinger", mclr= BLUE, dclr= BLUE_D, dice_sel= dice_sel_blue, turn= 4, home= 22, entry= 17, hud= (1484, 182))
    players_obj = [player_1, player_2, player_3, player_4]

    boxes_obj.clear()
    for i in boxes_num:
        if i == 100:
            boxes_obj.append(Box(i, "win"))
        elif i in cas_home:
            boxes_obj.append(Box(i, "home"))
        elif i in cas_shield:
            boxes_obj.append(Box(i, "shield"))
        elif type(i) == int:
            boxes_obj.append(Box(i, "classic"))
        else:
            boxes_obj.append(Box(i, "stair"))

    tokens_obj.clear()
    for i in range(1, 5):
        for j in range(1, 5):
            obj = Token(id= int(f"{i}{j}"))
            tokens_obj.append(obj)
            players_obj[i-1].tokens.append(obj)

            box_in = Box(float(f"0.{i}{j}"), "in")
            box_in.tokens.append(obj)
            boxes_obj.append(box_in)
    
    dices_obj.clear()
    for player in players_obj:
        if player.id != 0:
            dices_obj.append(player.dice_1)
            dices_obj.append(player.dice_2)

    return players_obj, boxes_obj, dices_obj, tokens_obj


def reset_objects(tokens: list[Token], boxes: list[Box], player: Player):
    boxes_in = boxes[-1:-17]
    boxes_in.sort()
    reset_tokens = tokens
    for t in player.tokens:
        reset_tokens.remove(t)

    for b in boxes:
        b.tokens.clear()
    
    for t in reset_tokens:
        t.pos = float(t.id/100)
        boxes_in[tokens.index(t)].tokens.append(t)





# To do:
#   error se pierde el valor del dado cuando hay movimientos posibles

#   cambiar colores dados (temporales)
#   cambiar sprites fichas (temporales)
