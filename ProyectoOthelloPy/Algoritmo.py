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
        pFinal = int(tablero.cantidadFichas().x) - int(tablero.cantidadFichas().y)
        if(pFinal > 0):
            return 100*pFinal
        else:
            return -100*pFinal
    
    """    
    crea un arbol de juego segun una jugada
    def ArbolJuego(self,tablero):
    tablero.getMundo()
    """ 
            
        
    #Toma un tablero logico y devuelve una instancia nueva con los mismo valores    
    def copiaTablero(tablero):
        #nuevo tablero
        nt = Tablero()
        nt.turno , nt.numeroTurno = tablero.turno, tablero.numeroTurno
        nt.mundo = deepcopy(tablero.mundo)
        return nt
        
    #Algitmo MinMax con optimizacion poda alfa-beta    
    def podaalphabeta(self, arbol, depth, alfa, beta):
        i = 0
        for rama in arbol:
            if type(rama) is list:
                (nalfa,nbeta) = podaalphabeta(rama, depth+1, alfa, beta)
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
            self.setTree(arbol)
        return (alfa, beta)
                    
        
