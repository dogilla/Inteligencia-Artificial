class Tablero:
    ''' Definicion de un tablero para el juego de Othello '''
    def __init__(self, dimension=8, tamCasilla=60):
        ''' Constructor base de un tablero
        :param dimension: Cantidad de casillas en horizontal y vertical del tablero
        :type dimension: int
        :param tamCasilla: El tamano en pixeles de cada casilla cuadrada del tablero
        :type tamCasilla: int
        '''
        #dificultad del juego 3 para facil y 5 pa dificil
        self.dificultad = 3 #facil por default
        self.dimension = dimension
        self.tamCasilla = tamCasilla
        self.turno = True  #Representa de quien es el turno bajo la siguiente convencion: true = jugador 1, false = jugador 2
        self.numeroDeTurno = 0 # Contador de la cantidad de turnos en el tablero
        self.mundo = [[0 for i in range(self.dimension)] for j in range(self.dimension)] # Representacion logica del tablero. Cada numero representa: 0 = vacio, 1 = ficha jugador1, 2 = ficha jugador 2
        # Configuracion inicial (colocar 4 fichas al centro del tablero):
        self.mundo[(self.dimension/2)-1][self.dimension/2] = 1
        self.mundo[self.dimension/2][(self.dimension/2)-1] = 1
        self.mundo[(self.dimension/2)-1][(self.dimension/2)-1] = 2
        self.mundo[self.dimension/2][self.dimension/2] = 2
        
    def display(self):
        ''' Dibuja en pantalla el tablero, es decir, dibuja las casillas y las fichas de los jugadores '''
        fondo = color(63, 221, 24) # El color del fondo del tablero
        linea = color(0) # El color de linea del tablero
        grosor = 2 # Ancho de linea (en pixeles)
        jugador1 = color(0) # Color de ficha para el primer jugador
        jugador2 = color(255) # Color de ficha para el segundo jugador
        
        # Doble iteracion para recorrer cada casilla del tablero
        for i in range(self.dimension):
            for j in range(self.dimension):
                # Dibujar cada casilla del tablero:
                fill(fondo)
                stroke(linea)
                strokeWeight(grosor)
                rect(i*self.tamCasilla, j*self.tamCasilla, self.tamCasilla, self.tamCasilla)
                # Dibujar las fichas de los jugadores:
                if not self.mundo[i][j] == 0 and (self.mundo[i][j] == 1 or self.mundo[i][j] == 2): # en caso de que la casilla no este vacia
                    fill(jugador1 if self.mundo[i][j] == 1 else jugador2) # establecer el color de la ficha
                    noStroke() # quitar contorno de linea
                    ellipse(i*self.tamCasilla+(self.tamCasilla/2), j*self.tamCasilla+(self.tamCasilla/2), self.tamCasilla*3/5, self.tamCasilla*3/5)

    #establece la dificultad del juego
    def setDificultad(self, dificil):
        if dificil == "facil":
            self.dificultad = 3
        elif dificil == "media":
            self.dificultad = 4
        elif dificil == "dificil":
            self.dificultad = 5
        else:
            self.dificultad = 3
    
    def getMundo(self):
        return self.mundo
    
    def setFicha(self, posX, posY, turno=None):
        ''' Coloca o establece una ficha en una casilla especifica del tablero.
        Nota: El eje vertical esta invertido y el contador empieza en cero.
        :param posX: Coordenada horizontal de la casilla para establecer la ficha
        :type posX: int
        :param posY: Coordenada vertical de la casilla para establecer la ficha
        :type posY: int
        :param turno: Representa el turno o color de ficha a establecer
        :type turno: bool
        '''
        turno = self.turno if turno is None else turno # permite definir un parametro default que es instancia de la clase (self.turno)
        self.mundo[posX][posY] = 1 if turno else 2
   
    def cambiarTurno(self):
        ''' Representa el cambio de turno. Normalmente representa la ultima accion del turno '''
        self.turno = not self.turno
        self.numeroDeTurno += 1
        
    def estaOcupado(self, posX, posY):
        ''' Verifica si en la posicion de una casilla dada existe una ficha (sin importar su color)
        :param posX: Coordenada horizontal de la casilla a verificar
        :type posX: int
        :param posY: Coordenada vertical de la casilla a verificar
        :type posY: int
        :returns: True si hay una ficha de cualquier color en la casilla, false en otro caso
        :rtype: bool
        '''
        return self.mundo[posX][posY] != 0 and self.mundo[posX][posY] != -1 
    
    def cantidadFichas(self):
        ''' Cuenta la cantidad de fichas en el tablero
        :returns: La cantidad de fichas de ambos jugadores en el tablero como vector donde x = jugador 1, y = jugador 2
        :rtype: PVector 
        '''
        contador = PVector()
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.mundo[i][j] == 1:
                    contador.x = contador.x + 1
                if self.mundo[i][j] == 2:
                    contador.y = contador.y + 1
        return contador

        
    def colorea(self, posx, posy):
        ''' Colorea del color del turno las fichas opuestas que esten entre dos fichas del
        color del turno
        '''
        pj = self.propaga(posx,posy)
        for i,j in pj:
            self.setFicha(i,j,self.turno)

        
        
    """
    nos dice si dadas dos coordenas hay fichas de otro color entre las coordenas
    y otra de nuestro color
    """
    def hayColoreables(self, posx,posy):
        return len(self.propaga(posx,posy)) > 0 
    

    
    """
    Nos dice si dadas dos cordenadas una ficha tiene otra ficha adyacente
    del color opuesto. Hay que revizar muchos casos pues python se puede
    salir del arreglo
    """
    def adyacente(self, x, y):
        c = 2 if self.turno else 1
        """
        Primero reviza si la ficha esta a la orilla en la izquierda
        """
        if(x == 0):
            right = self.mundo[x+1][y]
            if(y == 0):
                return right == c or self.mundo[x][y+1] == c or self.mundo[x+1][y+1] == c
            elif(y == 7):
                return right == c or self.mundo[x][y-1] == c or self.mundo[x+1][y-1] == c
            else:
                return right == c or self.mundo[x][y-1] == c or self.mundo[x][y+1] == c or self.mundo[x+1][y-1] == c or self.mundo[x+1][y+1] == c
        elif(x == 7):
            left = self.mundo[x-1][y]            
            if(y == 0):
                return left == c or self.mundo[x][y+1] == c or self.mundo[x-1][y+1] == c
            if(y == 7):
                return self.mundo[x][y-1] == c or left == c or self.mundo[x-1][y-1] == c    
            else:
                return self.mundo[x][y+1] == c or self.mundo[x-1][y+1] == c or left == c or self.mundo[x-1][y-1] == c or self.mundo[x][y-1] == c
        elif(y == 0):
            return self.mundo[x-1][y] == c or self.mundo[x-1][y+1] == c or self.mundo[x][y+1] == c or self.mundo[x+1][y+1] == c or self.mundo[x+1][y] == c
        elif(y == 7):
            return self.mundo[x-1][y]  == c or self.mundo[x+1][y] == c or self.mundo[x-1][y-1] == c or self.mundo[x][y-1] == c or self.mundo[x+1][y-1] == c
        else:
            return self.mundo[x+1][y] == c or self.mundo[x-1][y] == c or self.mundo[x][y+1] == c or self.mundo[x][y-1] == c or self.mundo[x-1][y-1] == c or self.mundo[x+1][y-1] == c or self.mundo[x-1][y+1] == c or self.mundo[x+1][y+1] == c    

    
    '''
    imprime el tablero logico
    '''
    def imprimeTablero(self):
        print('\n'.join(''.join(str(i)) for i in self.mundo))
    
    #Nos dice si dos puntos estan en el limite del mundo
    def limite(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <=7
    
    """
    dado una coordenada x y el algoritmo se propaga a todos lados, si encuentra
    una del mismo color del turno se regresa guardando las fichas en una lista
    """    
    def propaga(self, mousex, mousey):
        #turno contrario
        c = 2 if self.turno else 1
        #turno correcto
        r = 1 if self.turno else 2
        
        #lista de fichas que vamos a voltear (cambiar al color opuesto)
        volteadas = []
        for i, j in [[0,1],[1,1],[1, 0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
            x,y = mousex , mousey
            x+=i
            y+=j
            if self.limite(x,y) and self.mundo[x][y] == c:
                x = x+i
                y = y+j
                if not self.limite(x,y):
                    continue
                while self.mundo[x][y] == c:
                    x+=i
                    x+=j
                    if not self.limite(x,y):
                        break
                if not self.limite(x,y):
                    continue
                if self.mundo[x][y] == r:
                    while True:
                        x-=i
                        y-=j
                        if x == mousex and y == mousey:
                            break
                        volteadas.append([x,y])
        return volteadas
    
    #regresa una lista con las posibles jugadas del jugador
    def jugadasPosibles(self):
        jugadas = []
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.hayColoreables(i, j) and self.adyacente(i,j):
                    jugadas.append([i,j])    
        print(str(jugadas))    
        
    """    
    funcion que hace jugar a la inteligencia artificial, pone una ficha en la
    posicion (x,y) y cambia el turno      
    """
    def juegaIA(self, x, y):
        self.setFicha(x,y)
        #turno del contrario
        self.mundo[x][y] = 1 if self.turno else 2
        self.cambiarTurno()
        print '[Turno # {!s}] {} (Score {!s} - {!s})'.format(self.numeroDeTurno, 'jugo ficha blanca' if self.turno else 'jugo ficha negra', int(self.cantidadFichas().x), int(self.cantidadFichas().y))
        
          
        
        
         
