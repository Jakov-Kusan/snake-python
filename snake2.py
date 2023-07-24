import time
import pygame
import threading
import random
import tkinter
from playsound import playsound


pygame.init()

surface = pygame.display.set_mode((600,600))
event = pygame.event.get()

x=240
y=240

yellow = (250,240,0)
red = (250,0,0)
green2 = (0,255,0)

direction = ""
tails = []
apples_eaten = 0

apple = (random.randint(1,9)*60,random.randint(1,9)*60)

def activate_move_sound_effect():
    soundplay = threading.Thread(target=play_move_sound_effect)
    soundplay.start()

def play_move_sound_effect():
    playsound("move_sound.mp3")


def grid_update():
    grid_y = -60

    for i in range(14):
        grid_y = grid_y+60
        grid_x = -60
        for j in range(20):
            grid_x = grid_x+60
            pygame.draw.rect(surface, (255,255,255), pygame.Rect(grid_x, grid_y, 60, 60),1)


def spawn_apple():
    global apple
    global tails

    apple = (random.randint(1,9)*60,random.randint(1,9)*60)

    for i in range(len(tails)):
        if tails[i][0] == apple[0] and tails[i][1] == apple[1] or apple[0] == x and apple[1] == y:
            print("hi")
            spawn_apple()


def draw_apple():
    global apples_eaten
    global apple
    global x,y
    global red
    pygame.draw.rect(surface, red, pygame.Rect(apple[0], apple[1], 56, 56))

def appleupdate():
    global apples_eaten
    global apple
    global x,y
    global red

    if apple[0] == x and apple[1] == y:
        apples_eaten = apples_eaten+1

        spawn_apple()
    
    

    

def draw_tails():
    global tails
    for i in range(len(tails)):
        if 255-i*4 < 10:
            pygame.draw.rect(surface, (0,50,0), pygame.Rect(tails[i][0], tails[i][1], 55, 55))
        else:
            pygame.draw.rect(surface, (0,255-i*4,0), pygame.Rect(tails[i][0], tails[i][1], 55, 55))

def tailupdate():
    global tails
    global x,y
    global apples_eaten

    to_remove = []

    for i in range(len(tails)):
        tails[i] = (tails[i][0],tails[i][1],tails[i][2]-1)

        if apples_eaten != 0:
            if tails[i][0] == x and tails[i][1] == y:
                pygame.quit()
        
        if tails[i][2] < 1:
            to_remove.append(i)



    for i in range(len(to_remove)):
        tails.pop(to_remove[i])




def automove():
    global x,y
    global direction

    if direction == "up":
        y -= 60
        if y < 0:
            pygame.quit()

    elif direction == "down":
        y += 60
        if y > 540:
            pygame.quit()

    elif direction == "left":
        x -= 60
        if x < 0:
            pygame.quit()

    elif direction == "right":
        x += 60
        if x > 540:
            pygame.quit()

def head_move():
    global x,y
    global direction
    global tails
    global apples_eaten

    tails.append((x,y,apples_eaten))
    nokeypressed = 0

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_TAB:
                activate_move_sound_effect()
                pygame.quit()
            
            if event.key == pygame.K_a and direction != "right":
                activate_move_sound_effect()
                x -= 60
                if x < 0:
                    pygame.quit()
                direction = "left"
                nokeypressed= 1

            elif event.key == pygame.K_d and direction != "left":
                activate_move_sound_effect()
                x += 60
                if x > 540:
                    pygame.quit()
                direction = "right"
                nokeypressed= 1

            elif event.key == pygame.K_w and direction != "down":
                activate_move_sound_effect()
                y -= 60
                if y < 0:
                    pygame.quit()
                direction = "up"
                nokeypressed= 1

            elif event.key == pygame.K_s and direction != "up":
                activate_move_sound_effect()
                y += 60
                if y > 540:
                    pygame.quit()
                direction = "down"
                nokeypressed= 1

    if nokeypressed == 0:
        automove()


    
while True:
        title = "Snake: "+str(apples_eaten)+" apples eaten - "+str(x)+","+str(y)
        pygame.display.set_caption(title)
        
        time.sleep(0.13)

        head_move()
        tailupdate()
        appleupdate()

        #print("Apples eaten:",apples_eaten)
        #print(direction)
        #print(tails)
        #print(apple)


        surface.fill((0, 0, 0))
        grid_update()
        draw_apple()
        draw_tails()
        pygame.draw.rect(surface, yellow, pygame.Rect(x, y, 55, 55))
        pygame.display.update()