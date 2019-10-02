''' 
Algoritmos necesarios para la implementacion del juego de Othello/Reversi
Estos algoritmos son implementados para ser usados sobre la representacion del tablero
:authores: 
Mario Guzman Mosco
Miguel Angel M Mendoza
Miriam Torres Bucio
'''

from Tablero import *

class Algoritmo:
    def __init__(self):
        self.dificultad = 1
        self.tree = []
        #raiz del arbol de juego
        self.raiz = 0
        self.alfabeta = (0,0)
        
    def setTree(self, arbol):
        self.tree = arbol
    
    #Funcion heuristica con estrategia de maximizacion de fichas
    def h1(self, tablero):
        #puntuacion final
        pFinal = int(tablero.cantidadFichas().y) - int(tablero.cantidadFichas().x)
        if(pFinal > 0):
            return 10*pFinal
        else:
            return -10*pFinal
        
    #selecciona la dificultad del juego                
    def selectDificulty(self,y):
        if y >= 240:
            self.dificultad = 1
            print("MODO FACIL")
        else:
            self.dificultad = 2
            print("MODO DIFICIL")
        
    
    #crea un nivel extra en el arbol de juego
    def creaNivel(self, tablero):
        jugadas = tablero.jugadasPosibles()
        nivel = []
        for jugada in jugadas:
            tablero_n = self.copiaTablero(tablero)
            tablero_n.setFicha(jugada[0], jugada[1])
            nivel.append(tablero_n)
        return nivel
    
    """
    Recibe el tablero del juego y regresa la jugada que va a hacer IA 
    segun la funcion heuristica y el algoritmo poda alfa-beta 
    """   
    def creaArbol(self, tablero):
        nivel = self.creaNivel(tablero)
        #lista con los valores heuristicos de las posibles jugadas
        heuristicas = []
        for jugada in nivel:
            #uso de la heuristica en las posibles jugadas
            heuristicas.append(self.h1(jugada))
        result = self.podaalphabeta(heuristicas,0,-15,15)
        for i in nivel:
            if (self.h1(i) == result):
                return i
            
        
    #Toma un tablero y devuelve una instancia nueva con los mismos valores    
    def copiaTablero(self, tablero):
        #nuevo tablero
        nt = Tablero()
        nt.turno , nt.numeroDeTurno = tablero.turno, tablero.numeroDeTurno
        for i in range(8):
            for j in range(8):
                nt.mundo[i][j] = tablero.mundo[i][j]
        return nt
        
    #Algitmo MiniMax con optimizacion poda alfa-beta    
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
            #sabemos que un nodo es una hoja si en un valor y no una lista
            else:
                if depth % 2 == 0 and alfa < rama:
                    alfa = rama
                if depth % 2 == 1 and beta > rama:
                    beta = rama
                if alfa >= beta:
                    break
        if depth == self.raiz:
            arbol = alfa if self.raiz == 0 else beta
        """
        Al final regresa el mejor valor heuristico, si no ha acabado la recursion 
        entoces regresa un arbol de juego y continua el algoritmo
        """
        return arbol    
