/**
 * Proyecto base para el juego de Othello/Reversi
 * @author Rodrigo Colín
 */

Tablero tablero;

/**
 * Método para establecet tamaño de ventana al incluir variables
 */
void settings(){
  tablero =  new Tablero();
  size(tablero.dimension * tablero.tamCasilla, tablero.dimension * tablero.tamCasilla);
}

/**
 * Inicializaciones
 */
void setup(){
  println("Proyecto base para el juego de mesa Othello");
}

/**
 * Ciclo de dibujado
 */
void draw(){
  tablero.display();
}

/**
 * Evento para detectar cuando el usuario da clic
 */
void mousePressed() {
  int posx = mouseX/tablero.tamCasilla;
  int posy =mouseY/tablero.tamCasilla;
  println("\nClic en la casilla " + "[" + ((posx)+1) + ", " + ((posy)+1) + "]");
  if(!tablero.estaOcupado(posx, posy)){
    tablero.setFicha(posx, posy);
    tablero.cambiarTurno();
    println("[Turno #" + tablero.numeroDeTurno + "] "  + (tablero.turno ? "jugó ficha blanca" : "jugó ficha negra") + " (Score: " + int(tablero.cantidadFichas().x) + " - " + int(tablero.cantidadFichas().y) + ")");
  }
  
  //tablero.colorea(posx, posy);
}
