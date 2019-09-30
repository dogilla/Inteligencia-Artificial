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
    
    """    
    crea un arbol de juego segun una jugada
    def ArbolJuego(self,tablero, x, y):
        arbol = []
        tree = [[[5, 1, 2], [8, -8, -9]], [[9, 4, 5], [-3, 4, 3]]]
        jugadas = tablero.jugadasPosibles()
        if (len(jugadas) == 0):
            return
        elif(len(jugadas % 2) == 0):
        
        else:
    """
    
    #crea un nivel extra en el arbol de juego
    def creaNivel(tablero):
        jugadas = tablero.jugadasPosibles()
        nivel = []
        for jugada in jugadas:
            tablero_n = copiaTablero(tablero)
            tablero_n.setFicha(jugada.get(0), jugada.get(1))
            tablero_n.nivelUp()
            nivel.append(tablero_n)
        return nivel
    
    def creaArreglo(self, num, arreglo):
        while(num>0):
            arreglo.append([])
            num = num-1 
            
        
    def CreaArbol(tablero):
        i = tablero.getDificultad()
        n = 0
        arbolJuego = self.creaNivel(tablero)
        nthnivel = []
        while (i > 0):
            for j in range(len(arbolJuego)):
                n_jugadas = self.creaNivel(arbolJuego[j])
                nthnivel.append(n_jugadas)
                arbolJuego = []
            i=i-1
    
    """
    r = [tablero]
    for i in r:
        if type(r) = tablero then...
    """    
    def creaArbolFacil(tablero):
        nivel = self.creaNivel(tablero)
        heuristicas = []
        for jugada in nivel:
            heuristicas.append(self.h1(jugada))
        result = self.podaalphabeta(heuristicas,1, 0,0)
        for i in nivel:
            if (self.h1(i) == result):
                return i

            
            
        
            
     
            
        
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
                    
        
