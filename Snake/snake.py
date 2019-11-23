import math
import random
from random import randint
import pygame
import tkinter as tk
from tkinter import messagebox
 
class Cuadro(object):
    """ clase que representa un cuadro del tablero de juego"""
    filas = 20
    w = 500
    def __init__(self,inicio,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = inicio
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def print_Cuadro(self):
        print("la posicion de la carnada es " + str(self.pos))
  
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, superficie, ojos=False):
        distancia = self.w // self.filas
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(superficie, self.color, (i*distancia+1,j*distancia+1, distancia-2, distancia-2))
        if ojos:
            centro = distancia//2
            radius = 3
            circleMiddle = (i*distancia+centro-radius,j*distancia+8)
            circleMiddle2 = (i*distancia + distancia -radius*2, j*distancia+8)
            pygame.draw.circle(superficie, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(superficie, (0,0,0), circleMiddle2, radius)
       
 
class DecisionTree(object):
    """ clase que representa un arbol de desición """
    etiquetas = {}

    def __init__(self):
        self.etiquetas = {
            "l":(-1,0),
            "r":(1,0),
            "u":(0,-1),
            "d":(0,1),
        }
        
    def Pregunta(self, cabeza, carnada, filter_list=[]):
        if len(filter_list) == 0:
            #derecha
            if carnada[0] < cabeza[0]:
                self.etiquetas.pop("r")
                #arriba
                if carnada[1] < cabeza[1]:
                    self.etiquetas.pop("d")
                    return self.Pregunta(cabeza, carnada, self.etiquetas)
                else:
                    self.etiquetas.pop("u")
                    return self.Pregunta(cabeza, carnada, self.etiquetas)
            else:
                self.etiquetas.pop("l")
                if carnada[1] < cabeza[1]:
                    self.etiquetas.pop("d")
                    return self.Pregunta(cabeza, carnada, self.etiquetas)
                else:
                    self.etiquetas.pop("u")
                    return self.Pregunta(cabeza, carnada, self.etiquetas)
        else:
            m1 = self.etiquetas.popitem()[1]
            m2 = self.etiquetas.popitem()[1]
            return m1,m2
            
 
class Serpiente(object):
    """ 
    Clase que representa a la serpiente del juego 

    ...

    atributos
    ---------
    cuerpo: List
        lista que guarda las posiciones del cuerpo de la serpiente
    giros: Dictionary
        diccionario que guarda los posibles giros de posición según las reglas del juego
        e indica si el giro está activo.
    color: Color
        color de la serpiente en el juego según codigo RGB
    cabeza: Cuadro
        cuadro que guarda la cabeza de la serpiente
    dirnx: int
        direccion el la que se mueve la serpiente en el eje x de un plano en dos dimensiones
        1 indica una dirección positiva y 0 negativa
    dirny: int
        direccion el la que se mueve la serpiente en el eje y de un plano en dos dimensiones
        1 indica una dirección negativa y 0 positiva
    """
    cuerpo = []
    giros = {}

    def __init__(self, color, pos):
        """ constructor de la clase Serpiente """
        self.color = color
        self.cabeza = Cuadro(pos)
        self.cuerpo.append(self.cabeza)
        self.dirnx = 0
        self.dirny = 1

    def haz_movimiento(self, direction):
        """ mueve la cabeza a una direccion y hace que el resto del cuerpo lo siga"""
        #la cabeza se mueve hacia la direccion señalada por x y
        self.dirnx = direction[0]
        self.dirny = direction[1]
        self.giros[self.cabeza.pos[:]] = [self.dirnx, self.dirny]
        #Esto hace que el resto del cuerpo siga la cabeza
        for i, c in enumerate(self.cuerpo):
            p = c.pos[:]
            if p in self.giros:
                turn = self.giros[p]
                c.move(turn[0],turn[1])
                if i == len(self.cuerpo)-1:
                    self.giros.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.filas-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.filas-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.filas-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.filas-1)
                else: c.move(c.dirnx,c.dirny)
 
    def reinicio(self, pos):
        """ reinicia la posicion inical de la serpiente y su tamaño de 1 cuadro """
        self.cabeza = Cuadro(pos)
        self.cuerpo = []
        self.cuerpo.append(self.cabeza)
        self.giros = {}
        self.dirnx = 0
        self.dirny = 1
 
 
    def agrega_cuadro(self):
        """ Agrega un cuadro a la serpiente cuando llega al objetivo (carnada) """
        tail = self.cuerpo[-1]
        dx, dy = tail.dirnx, tail.dirny
 
        if dx == 1 and dy == 0:
            self.cuerpo.append(Cuadro((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.cuerpo.append(Cuadro((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.cuerpo.append(Cuadro((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.cuerpo.append(Cuadro((tail.pos[0],tail.pos[1]+1)))
 
        self.cuerpo[-1].dirnx = dx
        self.cuerpo[-1].dirny = dy
       
 
    def draw(self, superficie):
        """ dibuja la serpiente dinamicamente en el tablero """
        for i, c in enumerate(self.cuerpo):
            if i ==0:
                c.draw(superficie, True)
            else:
                c.draw(superficie)
 
 
def cuadricula(w, filas, superficie):
    """ dibuja la cuadricula del tablero """
    tamano = w // filas
    x = 0
    y = 0
    for l in range(filas):
        x = x + tamano
        y = y + tamano
        #dibuja lineas blancas
        pygame.draw.line(superficie, (255,255,255), (x,0),(x,w))
        pygame.draw.line(superficie, (255,255,255), (0,y),(w,y))
       
 
def redibuja(superficie):
    """ vuelve a dibujar el tablero al perder """
    global filas, anchura, agente, carnada
    superficie.fill((0,0,0))
    agente.draw(superficie)
    carnada.draw(superficie)
    cuadricula(anchura,filas, superficie)
    pygame.display.update()
 
 
def random_carnada(filas, item):
    """Crea de manera aleatoria una carnada para la serpiente del juego"""
    posiciones = item.cuerpo
    while True:
        x = random.randrange(filas)
        y = random.randrange(filas)
        if len(list(filter(lambda z:z.pos == (x,y), posiciones))) > 0:
            continue
        else:
            break
    return (x,y)
 
 
def message_box(asunto, contenido):
    origen = tk.Tk()
    origen.attributes("-topmost", True)
    origen.withdraw()
    messagebox.showinfo(asunto, contenido)
    try:
        origen.destroy()
    except:
        pass
 
 
def main():
    """ funcion principal que pone en funcion el juego hasta que termine """
    #declaramos las variables globales del juego
    global anchura, filas, agente, carnada, jugadas
    jugadas = []
    anchura = 500
    filas = 20
    fin_juego = pygame.display.set_mode((anchura, anchura))

    agente = Serpiente((0,255,0), (10,10))
    #posicion de la carnada
    carnadapos = random_carnada(filas, agente)
    carnada = Cuadro(carnadapos, color=(0,255,0))
    carnada.print_Cuadro()
    flag = True
 
    clock = pygame.time.Clock()
   
    while flag:
        pygame.time.delay(60)
        clock.tick(8)
        dt = DecisionTree()
        m1,m2 = dt.Pregunta(agente.cuerpo[0].pos, carnada.pos)
        if m1 not in jugadas:
            jugadas.append(m1)
        if m2 not in jugadas:
            jugadas.append(m2)        
        agente.haz_movimiento(jugadas.pop(0))      
        #si la posicion de la serpiente es igual al de la carnada significa que llego
        # al objetivo por tanto se agrega un cuadro y se crea otra carnada        
        if agente.cuerpo[0].pos == carnada.pos:
            agente.agrega_cuadro()
            carnada = Cuadro(random_carnada(filas, agente), color=(0,255,0))
            carnada.print_Cuadro()  
        
        #verifica si el agente ha perdido o sigue en juego
        for x in range(len(agente.cuerpo)):
            if agente.cuerpo[x].pos in list(map(lambda z:z.pos,agente.cuerpo[x+1:])):
                message_box("Ha perdido", "volvera a juagar")
                agente.reinicio((10,10))
                break 
        redibuja(fin_juego)
    

    pass
 
 
main()
