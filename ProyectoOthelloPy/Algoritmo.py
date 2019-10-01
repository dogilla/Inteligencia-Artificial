''' Algoritmos para el juego de Othello/Reversi 
:authores: 
Mario Guzman Mosco
Miguel Angel M Mendoza
Miriam Torres Bucio
'''

from Tablero import *
from copy import deepcopy

class Algoritmo:
    def __init__(self):
        self.tree = []
        self.raiz = 0
        self.alfabeta = (0,0)
        
    def setTree(self, arbol):
        self.tree = arbol
    
    #Funcion heuristica con estrategia de fichas
    def h1(self, tablero):
        #puntuacion final
        pFinal = int(tablero.cantidadFichas().y) - int(tablero.cantidadFichas().x)
        if(pFinal > 0):
            return 10*pFinal
        else:
            return -10*pFinal
    
    #crea un nivel extra en el arbol de juego
    def creaNivel(self, tablero):
        print("crea nivel")
        jugadas = tablero.jugadasPosibles()
        nivel = []
        for jugada in jugadas:
            tablero_n = self.copiaTablero(tablero)
            tablero_n.setFicha(jugada[0], jugada[1])
            nivel.append(tablero_n)
        return nivel
    
    #regresa la jugada de la IA segun la heuristica y el algoritmo alfa-beta    
    def creaArbolFacil(self, tablero):
        nivel = self.creaNivel(tablero)
        heuristicas = []
        for jugada in nivel:
            heuristicas.append(self.h1(jugada))
        result = self.podaalphabeta(heuristicas,0,-15,15)
        for i in nivel:
            if (self.h1(i) == result):
                return i        
        
    #Toma un tablero logico y devuelve una instancia nueva con los mismo valores    
    def copiaTablero(self, tablero):
        #nuevo tablero
        nt = Tablero()
        nt.turno , nt.numeroDeTurno = tablero.turno, tablero.numeroDeTurno
        for i in range(8):
            for j in range(8):
                nt.mundo[i][j] = tablero.mundo[i][j]
        #nt.mundo = deepcopy(tablero.getMundo())
        return nt
        
    #Algitmo MinMax con optimizacion poda alfa-beta    
    def podaalphabeta(self, arbol, depth, alfa, beta):
        i = 0
        for rama in arbol:
            if type(rama) is list:
                (nalfa,nbeta) = self.podaalphabeta(rama, depth+1, alfa, beta)
                #usamos modulo para saber si es rama con profundidad par o impar
                if depth % 2 == 1:
                    beta = nalfa if nalfa < beta else beta
                else:
                    alfa = nbeta if nbeta > alfa else alfa
                rama[i] = alfa if depth % 2 == 0 else beta
                i = i+1
            else:
                if depth % 2 == 0 and alfa < rama:
                    alfa = rama
                if depth % 2 == 1 and beta > rama:
                    beta = rama
                if alfa >= beta:
                    break
        if depth == self.raiz:
            arbol = alfa if self.raiz == 0 else beta
        return arbol    
