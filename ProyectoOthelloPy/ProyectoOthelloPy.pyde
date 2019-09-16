''' Proyecto base para el juego de Othello/Reversi 
:author: Rodrigo Colin
'''
from Tablero import *
tablero = Tablero()

def settings():
    ''' Metodo para establecer tamano de ventana al incluir variables '''
    size(tablero.dimension * tablero.tamCasilla, tablero.dimension * tablero.tamCasilla)

def setup():
    ''' Inicializaciones '''
    println("Proyecto base para el juego de mesa Othello")
            
def draw():
    ''' Ciclo de dibujado '''
    tablero.display()

def mousePressed():
    clickX = mouseX/tablero.tamCasilla
    clickY = mouseY/tablero.tamCasilla
    ''' Evento para detectar cuando el usuario da clic '''
    println("\nClic en la casilla " + "[" + str(clickX) + ", " + str(clickY) + "]")
    println(str(tablero.adyacente(clickX, clickY)))
    if tablero.adyacente(clickX, clickY):
        tablero.colorea(clickX, clickY)
        if not tablero.estaOcupado(clickX, clickY):
            tablero.setFicha(clickX, clickY)
            tablero.cambiarTurno()
            print '[Turno # {!s}] {} (Score {!s} - {!s})'.format(tablero.numeroDeTurno, 'jugo ficha blanca' if tablero.turno else 'jugo ficha negra', int(tablero.cantidadFichas().x), int(tablero.cantidadFichas().y))
    
