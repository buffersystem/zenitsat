import os, pygame
import pygame.freetype as ft
from functions import *
from assets import *


# pygame setup
pygame.init()

# Window meizures
os.environ["SDL_VIDEO_CENTERED"] = "1"
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h # Obtiene la resolución de la pantalla
screen_scale = [screen_width/1920, screen_height/1080]


# create object lists
players_obj = []
boxes_obj = []
dices_obj = []
tokens_obj = []
last_token = Token


# Global that indicate whom is the turn
clock = pygame.time.Clock()
screen = None
turn = 1


def main():
    # When starting the game, open menu.
    menu()
    pygame.quit()


def menu():
    # set window title
    pygame.display.set_caption("Mierdi Parchís")
    # Create screen 
    screen = pygame.display.set_mode((960, 540))
    screen.blit(title_screen, (0, 0))

    # create buttons and hitboxes
    button1 = pygame.rect.Rect(120, 300, 240, 60)
    screen.blit(button, button1)
    text1, text1_rect = ft.Font.render(font, "Play", BLACK, size= 18)
    screen.blit(text1, (button1.left+(button1.width-text1_rect.width)/2, button1.top+(button1.height-text1_rect.height)/2))

    button2 = pygame.rect.Rect(600, 300, 240, 60)
    screen.blit(button, button2)
    text2, text2_rect = ft.Font.render(font, "Multiplayer", BLACK, size= 18)
    screen.blit(text2, (button2.left+(button2.width-text2_rect.width)/2, button2.top+(button2.height-text2_rect.height)/2))

    title_text, title_rect = ft.Font.render(font, "Mierdi Parchís", BLACK, size= 50)
    screen.blit(title_text, ((960-title_rect.width)/2, 180))

    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if button1.collidepoint(pos):
                    running = False
                    game()
                elif button2.collidepoint(pos):
                    running = False
                    multiplayer()

        # blit buttons and title


        # flip() the display to put your work on screen (flip updates all screen)
        # update() the display to update a portion of the screen
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60


def game():
    global screen, background, board, screen_width, screen_height, screen_scale, turn, players_obj, boxes_obj, dices_obj, tokens_obj, font, last_token

    # set window title
    pygame.display.set_caption("Mierdi Parchís")
    screen = pygame.display.set_mode((screen_width, screen_height))


    # create objects
    players_obj, boxes_obj, dices_obj, tokens_obj = create_objects()

    # create exit
    hb_exit = pygame.rect.Rect(1826*screen_scale[0], 46*screen_scale[1], 48*screen_scale[0], 48*screen_scale[1])


    # warning text
    warn = ""
    warn_count = 0


    running = True

    while running:
        # Render the board and the background
        screen.fill((255,255,255))
        screen.blit(background, (0, 0))
        pos_board = resize_sprites()
        screen.blit(board,(pos_board[0], pos_board[1]))


        # active player
        player = players_obj[turn-1]


        # update barrier tokens
        for b in boxes_obj:
            if len(b.tokens) == 2:
                b.barrier = True
                for t in b.tokens:
                    t.barrier = True
            else:
                b.barrier = False
                for t in b.tokens:
                    t.barrier = False

        for p in players_obj:
            # create hud
            screen.blits(((p.player_text, (p.hudx, p.hudy)),
                        (p.name_text, (p.hudx, p.hudy+55)),
                        (p.wins_text,(p.hudx+32, p.hudy+95)))
                        )

            # update dices
            if p.dice_1.used and p.dice_2.used:
                p.dice_1.used = False
                p.dice_2.used = False
                p.dices_thrown = False

                if p.double_count == 2:
                    p.double = False
                    p.double_count = 0
                    last_box = boxes_obj[last_token.pos]
                    last_token.eaten(last_box)

                elif p.double:
                    p.throw_dices()
                    p.double = False
                    p.double_count += 1

                else:
                    if turn == 4:
                        turn = 1
                    else:
                        turn += 1

            # update home tokens count
            p.home_tokens = 0
            for t in p.tokens:
                if t.pos < 1:
                    p.home_tokens += 1

            # check if all tokens are out (6 turns into 7)
            if p.home_tokens == 0:
                p.seven = True

            # update barrier variable
            p.barrier = False
            for t in p.tokens:
                if t.barrier and not p.barrier:
                    p.barrier = True

            if p.tokens_win == 4:
                p.wins += 1
                turn = 1
                for t in p.tokens:
                    box = find_box(boxes_obj, t.pos)
                    t.pos = 100
                    box = find_box(boxes_obj, t.pos)
                    box.tokens.remove(t)
                    boxes_obj[-1].tokens.append(t)


        # Render changing objects
        for b in boxes_obj:
            b.calc_token_pos()

        for t in tokens_obj:
            screen.blit(t.sprite, t.px)

        for d in dices_obj:
            screen.blit(d.bg, (d.px))
            if d.fg != None:
                screen.blit(d.fg, (d.px))

        screen.blit(turn_indicator, (player.hudx-44, player.hudy + 3))


        warn_text, warn_rect = ft.Font.render(font, warn, BLACK, size= 20)
        coord = (960*screen_scale[0] - warn_rect.width/2, 84*screen_scale[1])
        screen.blit(warn_text, coord)

        if warn != "":
            if warn_count == 30:
                warn_count = 0
                warn = ""
            else:
                warn_count += 1


        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu()

            elif event.type == pygame.VIDEORESIZE:
                pos_board = resize_sprites()

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if hb_exit.collidepoint(pos):
                    running = False

                for p in players_obj:
                    if p.dice_1.hitbox.collidepoint(pos) == True:
                        if p.id == turn:
                            if p.dices_thrown == False:
                                p.throw_dices()

                            elif p.ff == True:
                                p.dice_1.used = True
                                p.dice_2.used = True
                                p.ff = False

                            elif p.dice_1.used == False:
                                if p.selected_dice == 0:
                                    p.selected_dice = 1
                                    p.dice_1.bg = p.dice_sel

                                elif p.selected_dice == 1:
                                    p.selected_dice = 0
                                    p.dice_1.bg = dice_default

                                else:
                                    warn = "You have already selected a dice"                                
                                    warn_count = 0

                            else:
                                warn = "You have already thrown your dices"
                                warn_count = 0

                        else:
                            warn = "It's not their turn"
                            warn_count = 0

                    elif p.dice_2.hitbox.collidepoint(pos) == True:
                        if p.id == turn:
                            if p.dices_thrown == False:
                                p.throw_dices()

                            elif p.ff == True:
                                p.dice_1.used = True
                                p.dice_2.used = True
                                p.ff = False

                            elif p.dice_2.used == False:
                                if p.selected_dice == 0:
                                    p.selected_dice = 2
                                    p.dice_2.bg = p.dice_sel

                                elif p.selected_dice == 2:
                                    p.selected_dice = 0
                                    p.dice_2.bg = dice_default

                                elif p.dices_thrown == True:
                                    warn = "You have already selected a dice"                                
                                    warn_count = 0

                            else:
                                warn = "You have already thrown your dices"
                                warn_count = 0

                        else:
                            warn = "It's not their turn"
                            warn_count = 0

                for t in tokens_obj:
                    if t.hitbox.collidepoint(pos):
                        if int(t.id/10) == turn:

                            if player.dices_thrown:
                                if player.selected_dice != 0:
                                    if player.selected_dice == 1:
                                        dice = player.dice_1
                                    else:
                                        dice = player.dice_2

                                    box_start = find_box(boxes_obj, t.pos)
                                    box_end, extra_steps = calc_box_end(player, boxes_obj, t, box_start, dice.value)   # extra steps taken for eating or promoting a token
                                    blocked = check_path(boxes_obj, box_start, box_end, turn)

                                    if not blocked:
                                        # check if the player will eat any token
                                        extra_steps.extend(check_eaten(box_end, turn))
                                        t.move(box_start, box_end)

                                        while len(extra_steps) > 0:
                                            extra_steps.sort()
                                            box_extra, blocked_extra, extra_steps = calc_box_extra(player, boxes_obj, t, box_end, extra_steps)

                                            if blocked_extra:
                                                warn = "You can't move any extra steps"
                                                warn_count = 0
                                            else:
                                                t.move(box_end, box_extra)
                                                warn = f"You moved {sum(extra_steps)} extra steps"
                                                extra_steps = check_eaten(box_end, turn)

                                        dice.used = True
                                        dice.bg = dice_used

                                        if dice.fg == dice_5_special:
                                            dice.fg = dice_5

                                        player.selected_dice = 0
                                        last_token = t

                                    else:
                                        warn = "The path is blocked"
                                        warn_count = 0

                                else:
                                    warn = "You haven't selected a dice yet"
                                    warn_count = 0

                            else:
                                warn = "You haven't thrown your dices yet"
                                warn_count = 0

                        else:
                            warn = "It's not their turn"
                            warn_count = 0


        # flip() the display to put your work on screen (flip updates all screen)
        # update() the display to update a portion of the screen
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60


def multiplayer():
    ... 




def resize_sprites():
    global background, board, players_obj, tokens_obj, dices_obj, hb_exit

    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen_scale = [screen_width/1920, screen_height/1080]

    background = pygame.transform.scale(background, (1920*screen_scale[0], 1080*screen_scale[1]))
    board = pygame.transform.scale(board,(828*screen_scale[1], 828*screen_scale[1]))
    pos_board = (546*screen_scale[0], 126*screen_scale[1])

    for t in tokens_obj:   # cambiar (para eliminar Token.coord y Token.px)
        px_x, px_y = t.px
        pygame.transform.scale(t.sprite, (28*screen_scale[1], 28*screen_scale[1]))
        t.hitbox = t.sprite.get_rect(left= px_x, top= px_y)

    for d in dices_obj:
        px_x, px_y = d.px
        pygame.transform.scale(d.bg, (120*screen_scale[1], 120*screen_scale[1]))
        if d.fg != None:
            pygame.transform.scale(d.fg, (120*screen_scale[1], 120*screen_scale[1]))
        d.hitbox = d.bg.get_rect(left= px_x, top= px_y)

    for p in players_obj:
        p.hudx = p.hud[0]*screen_scale[0]
        p.hudy = p.hud[1]*screen_scale[1]

    hb_exit = pygame.rect.Rect(1826*screen_scale[0], 46*screen_scale[1], 48*screen_scale[0], 48*screen_scale[1])

    return pos_board


def find_box(boxes: list[Box], num):
    for b in boxes:
        if b.id == num:
            return b


def check_path(boxes: list[Box], start: Box, end: Box, turn):
    pnt_1 = boxes.index(start)+1
    pnt_2 = boxes.index(end)+1

    if start.id < 1:
        boxes_sliced = [end]
    else:
        boxes_sliced = boxes[pnt_1:pnt_2]

    for b in boxes_sliced:
        if len(b.tokens) >= 2:
            if b.tipo == "classic":
                if int(b.tokens[0].id/10) == turn and int(b.tokens[1].id/10) == turn:
                        return True
            else:
                return True

    return False


def calc_box_end(player: Player, boxes: list[Box], token: Token, start: Box, value: int):
    extra_steps = []

    if start.tipo == "in":
        box_end = find_box(boxes, player.home)

    elif start.tipo == "stair":
        end = round(start.id%1, 1) + value/10

        while end > 0.8:
            end = 1.6 - end

            if end > 0.8:
                end -= 0.8

            elif end == 0.8:
                player.tokens_win += 1

                if player.tokens_win < 4:
                    extra_steps.append(10)

        box_end = find_box(boxes, float(player.entry + end))

    else:
        end = token.pos + value

        if end > 68:
            end -= 68

        if start.id < player.entry and end > player.entry:
            extra = end - player.entry   # extra steps taken

            while extra > 8:
                extra = 16 - extra
                if extra > 8:
                    extra -= 8

                elif extra == 8:
                    player.tokens_win += 1

                    if player.tokens_win < 4:
                        extra_steps.append(10)

            box_end = find_box(boxes, player.entry + extra/10)

        else:
            box_end = find_box(boxes, end)

    return box_end, extra_steps


def calc_box_extra(player: Player, boxes: list[Box], token: Token, start: Box, extra: list[int]):
    box_extra, extra_steps = calc_box_end(player, boxes, token, start, sum(extra))
    blocked_extra = check_path(boxes, start, box_extra, turn)
    move_extra = extra

    if blocked_extra:
        move_extra.pop(0)
        calc_box_extra(player, boxes, token, start, move_extra)

    return box_extra, blocked_extra, move_extra


def check_eaten(box: Box, turn):
    extra = []
    for t in box.tokens:
        if int(t.id/10) != turn and box.tipo == "classic":
            box_home = find_box(boxes_obj, float(t.id/100))
            t.eaten(box, box_home)
            extra.append(20)
    return extra



if __name__ == "__main__":

    main()
