import math
import random
from random import randint
import pygame
import tkinter as tk
from tkinter import messagebox
 
class cube(object):
    """ clase que representa un cuadro del tablero de juego"""
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def print_cube(self):
        print("la posicion de la carnada es " + str(self.pos))
  
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
 
class DecisionTree(object):
    """ clase que representa un arbol de desición """
    xy = (0,0)
    #izquierda, derecha, arriba, abajo
    options = [(-1,0),(1,0),(0,-1),(0,1)]
    node = []

    def __init__(self, head, snack):
        self.xy = head

    def question(self, head, snack, filter_list=[]):
        vertical = lambda  a: True if a == (1,0) else False 
        horizontal = lambda a,b: (0,-1) if a<= b else (0,1)
        if len(filter_list) == 0:
            return self.question(head, snack, filter(vertical(head,snack),self.options))
        
                
    def get_result(self):
        return self.xy
 
class snake(object):
    """ clase que representa a la serpiente del juego """
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def set_movement(self, x, y):
        """ mueve la cabeza a una direccion y hace que el resto del cuerpo lo siga"""
        #la cabeza se mueve hacia la direccion señalada por x y
        self.dirnx = x
        self.dirny = y
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        #Esto hace que el resto del cuerpo siga la cabeza
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
       
 
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
 
 
    def addCube(self):
        """ Agrega un cuadro a la serpiente cuando llega al objetivo """
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
 
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
       
 
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
       
 
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()
 
 
def randomSnack(rows, item):
    """Crea de manera aleatoria una carnada para la serpiente del juego"""
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)
 
 
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
 
def main():
    """ funcion principal que pone en funcion el juego hasta que termine """
    #declaramos las variables globales del juego
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((0,255,0), (10,10))
    #posicion de la carnada
    snackpos = randomSnack(rows, s)
    snack = cube(snackpos, color=(0,255,0))
    snack.print_cube()
    flag = True
 
    clock = pygame.time.Clock()
   
    while flag:
        pygame.time.delay(60)
        clock.tick(8)
        randx = randint(0,1)
        randy = randint(0,1)
        s.set_movement(randx, randy)
        DecisionTree(s.body[0].pos, snack.pos)
        #si la posicion de la serpiente es igual al de la carnada significa que llego
        # al objetivo por tanto se agrega un cuadro y se crea otra carnada        
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
            snack.print_cube()
 
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ' , len(s.body))
                message_box('You Lost! Play again...' )
                s.reset((10,10))
                break  
        redrawWindow(win)    
    pass
 
 
 
main()
