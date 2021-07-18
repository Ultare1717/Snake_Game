from Pygame_game import BLACK, WHITE
import pygame
import random
import tkinter as tk
from tkinter import messagebox
pygame.init()

class cube():
    rows = 0
    w = 0

    def __init__(self,start):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = (255,0,0)

    def move(self,dirnx,dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0]+self.dirnx,self.pos[1]+self.dirny)

    def draw(self,surface,eyes = False):
        dis = 500 // 20
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface,self.color,(i*dis + 1,j*dis+1,dis-2,dis-2))
        if eyes is True:
            centre = dis // 2
            radius = 3
            eye1 = (i*dis + centre - radius, j*dis + 8)
            eye2 = (i*dis + dis - radius*2, j*dis + 8)
            pygame.draw.circle(surface,BLACK,eye1,radius)
            pygame.draw.circle(surface,BLACK,eye2,radius)
        


class Snake:
    body = []
    turns = {}

    def __init__(self,color,pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT] and (self.dirnx != 1 or len(self.body)==1):
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT] and (self.dirnx != -1 or len(self.body)==1):
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                elif keys[pygame.K_UP] and (self.dirny != 1 or len(self.body)==1):
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                
                elif keys[pygame.K_DOWN] and (self.dirny != -1 or len(self.body)==1):
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (19,c.pos[1])
                elif c.dirnx == 1 and c.pos[0]>19:
                    c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1]>=19:
                    c.pos = (c.pos[0],0)
                elif c.dirny == -1 and c.pos[1]<=0:
                    c.pos = (c.pos[0],19)
                else:
                    c.move(c.dirnx,c.dirny)



        
    def reset(self,pos):
        self.body = []
        self.turns = {}
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self,surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow(surface):
    global width,rows,s,snack
    surface.fill(BLACK)
    drawGrid(width,rows,surface)
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()

def drawGrid(w, rows, surface):
    sizebtwn = w // rows
    x = 0
    y = 0
    for i in range(rows):
        x += sizebtwn
        y += sizebtwn
        pygame.draw.line(surface,WHITE,(x,0),(x,w))
        pygame.draw.line(surface,WHITE,(0,y),(w,y,))



def randomSnack(rows,item):
    global s
    dis = 500 // 20
    x = random.randrange(20)
    y = random.randrange(20)
    for i, c in enumerate(item.body):
        p = c.pos[:]
        if p == (x,y):
            continue
        else: break
    return (x,y)
    

def message_box(subject,content):
    pass
def main():
    global width, rows,s,snack
    width = 500
    height = 500
    rows = 20
    left = False
    right = False
    up = False
    down = False
    win = pygame.display.set_mode((width,height))
    s = Snake((255,0,0),(10,10))
    snack = cube((randomSnack(rows,s)))
    snack.color = (0,255,0)
    s.w = width
    s.rows = width
    flag = True
    clock =   pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()  
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube((randomSnack(rows,s)))
            snack.color = (0,255,0)
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                 print('Score:', len(s.body))
                 s.reset((10,10))
                 break

        redrawWindow(win)


main()