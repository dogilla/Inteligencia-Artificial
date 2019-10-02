''' Proyecto base para el juego de Othello/Reversi 
:authores: 
Rodrigo Colin (tablero)
Mario Guzman Mosco
Miguel Angel M Mendoza
Miriam Torres Bucio
'''
from Tablero import *
from Algoritmo import *

tablero = Tablero()
algoritmo = Algoritmo()

def settings():
    ''' Metodo para establecer tamano de ventana al incluir variables '''
    size(tablero.dimension * tablero.tamCasilla+150, tablero.dimension * tablero.tamCasilla)

def setup():
    ''' Inicializaciones '''
    println("Proyecto base para el juego de mesa Othello")
            
def draw():
    ''' Ciclo de dibujado '''
    tablero.display()
    fill(0)
    rect(480, 0, 150, 240)
    textSize(32)
    text("Modo", 490, 280)
    text("Facil", 490, 310)
    fill(180)
    text("Modo", 490, 80)
    text("dificil", 490, 110)
    

def mousePressed():
    clickX = mouseX/tablero.tamCasilla
    clickY = mouseY/tablero.tamCasilla
    if(mouseX > 480):
        algoritmo.selectDificulty(mouseY)
    if(mouseX < 480):
        ''' Evento para detectar cuando el usuario da clic '''
        println("\nClic en la casilla " + "[" + str(clickX) + ", " + str(clickY) + "]")
        if tablero.adyacente(clickX, clickY) and tablero.hayColoreables(clickX,clickY):
            if(not tablero.hayGanador()):
                tablero.colorea(clickX, clickY)
                if not tablero.estaOcupado(clickX, clickY):
                    tablero.setFicha(clickX, clickY)
                    tablero.cambiarTurno()
                    print '[Turno # {!s}] {} (Score {!s} - {!s})'.format(tablero.numeroDeTurno, 'jugo ficha blanca' if tablero.turno else 'jugo ficha negra', int(tablero.cantidadFichas().x), int(tablero.cantidadFichas().y))
                    tablero.juegaIA(tablero.turnoIA(algoritmo.creaArbol(tablero)))
                    if(tablero.hayGanador()):
                        tablero.ganador()
            else:
                tablero.colorea(clickX, clickY)
                tablero.setFicha(clickX, clickY)
                tablero.ganador()

            

        
