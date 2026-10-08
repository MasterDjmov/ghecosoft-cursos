from genc import m
from c_r01 import KIRA, TIZON, FERRUM, CHISPA

VIVA = "La Forja Viva"
TALLER = "El Taller de los Autómatas"
SALAMANDRA = "La Salamandra del Horno (salamandra de fuego vivo hecha de píxeles encendidos que dejan una estela)"
GUARDIAN = "El Autómata Guardián (autómata de latón del tamaño de un perro grande, cables a la vista, leds por ojos y un servomotor en cada articulación)"
SIN_VENTANA = "Acá no se abre una ventana: se prueba la lógica del juego sola, como en las pruebas de cualquier juego de verdad. El dibujo con SDL3 queda para tu compu."
SIN_PLACA = "Acá no hay placa: se prueba la lógica del autómata sola, con el tiempo y los pines simulados. En la placa de verdad, lo mismo va adentro de loop()."

NODOS = [
    {
        "titulo": "S01-N01 · La Forja Viva: ventana y bucle de juego",
        "misiones": [
            m(id="S01-N01-P1", titulo="Sesenta veces por segundo",
              lugar=VIVA, personajes="Kira, Gheco, Tizón",
              carta="El bucle de juego | leer la entrada, actualizar, dibujar, y otra vez · cada vuelta es un cuadro · el juego no termina hasta que se cierra",
              recompensa="xp 15, oro 15",
              escena="Kira abre su primera ventana y la cierra sin querer en el mismo segundo: su programa terminaba enseguida. Tizón cronometra: «Duró 0,02 segundos. Récord». " + SIN_VENTANA,
              sugiere="Un juego es un bucle: en cada vuelta (un **cuadro**) se actualiza el mundo. Acá el bucle corre 5 cuadros y en cada uno la caja avanza su velocidad.",
              desafio="Completá la actualización de la posición en cada cuadro.",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  int main(void)
                  {
                      int x = 0;
                      int velocidad = 12;
                      bool corriendo = true;
                      int cuadro = 0;
                      while (corriendo) {
                          ___;
                          cuadro++;
                          printf("cuadro %d: caja en x = %d\\n", cuadro, x);
                          if (cuadro == 5) {
                              corriendo = false;
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  int main(void)
                  {
                      int x = 0;
                      int velocidad = 12;
                      bool corriendo = true;
                      int cuadro = 0;
                      while (corriendo) {
                          x += velocidad;
                          cuadro++;
                          printf("cuadro %d: caja en x = %d\\n", cuadro, x);
                          if (cuadro == 5) {
                              corriendo = false;
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Cinco cuadros, la caja avanza. Tizón le pide que no cierre más la ventana sin avisarle: quiere cronometrar todo.",
              imagen=["Una puerta de vidrio negro detrás de la cual una caja de luz cian se mueve sobre una superficie que brilla.", KIRA + " frente a la puerta.", TIZON + " con un cronómetro."]),
            m(id="S01-N01-P2", titulo="La misma velocidad a 60 o a 240",
              lugar=VIVA, personajes="Kira, Gheco, Tizón",
              carta="Delta time | x += velocidad * dt · dt es el tiempo del cuadro en segundos · así el juego va igual en cualquier compu",
              recompensa="xp 15, oro 15",
              escena="En la compu de Tizón (rapidísima) la caja vuela; en la de Chispa (vieja) se arrastra. Ferrum: —El metal no puede andar más rápido porque el horno es nuevo.",
              sugiere="La velocidad se piensa en **píxeles por segundo** y cada cuadro avanza `velocidad * dt`, donde `dt` es lo que duró el cuadro. Con 60 cuadros de 1/60 o 240 de 1/240, al segundo se llega al mismo lugar.",
              desafio="Completá el avance con `dt`.",
              inicial='''
                  #include <stdio.h>

                  double un_segundo(int cuadros_por_segundo)
                  {
                      double x = 0.0;
                      double velocidad = 120.0;
                      double dt = 1.0 / cuadros_por_segundo;
                      for (int i = 0; i < cuadros_por_segundo; i++) {
                          x += ___;
                      }
                      return x;
                  }

                  int main(void)
                  {
                      printf("a 60 cuadros: %.1f px\\n", un_segundo(60));
                      printf("a 240 cuadros: %.1f px\\n", un_segundo(240));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  double un_segundo(int cuadros_por_segundo)
                  {
                      double x = 0.0;
                      double velocidad = 120.0;
                      double dt = 1.0 / cuadros_por_segundo;
                      for (int i = 0; i < cuadros_por_segundo; i++) {
                          x += velocidad * dt;
                      }
                      return x;
                  }

                  int main(void)
                  {
                      printf("a 60 cuadros: %.1f px\\n", un_segundo(60));
                      printf("a 240 cuadros: %.1f px\\n", un_segundo(240));
                      return 0;
                  }
              ''',
              al_superar="Ciento veinte píxeles en las dos. Chispa, por primera vez, juega a la misma velocidad que Tizón. Pierde igual.",
              imagen=["Dos pantallas lado a lado, una moderna y una vieja, con la misma caja en el mismo lugar.", CHISPA + " frente a la pantalla vieja."]),
            m(id="S01-N01-P3", titulo="Rebotar en los bordes",
              lugar=VIVA, personajes="Kira, Gheco, Maese Ferrum",
              carta="Rebote | si se pasa del borde, se queda en el borde y la velocidad cambia de signo · vx = -vx",
              recompensa="xp 15, oro 15",
              escena="La caja de Kira se escapa por el borde derecho de la pantalla y no vuelve más. Ferrum golpea el marco de la ventana: —Que rebote como el martillo en el yunque.",
              sugiere="Si `x` pasa el borde derecho (`x > ANCHO - LADO`), se la deja en el borde y se invierte la velocidad (`vx = -vx`). Lo mismo con el izquierdo (`x < 0`).",
              desafio="Completá el rebote en el borde derecho.",
              inicial='''
                  #include <stdio.h>

                  #define ANCHO 100
                  #define LADO 10

                  int main(void)
                  {
                      int x = 70, vx = 15;
                      for (int cuadro = 1; cuadro <= 6; cuadro++) {
                          x += vx;
                          if (x > ANCHO - LADO) {
                              x = ANCHO - LADO;
                              ___;
                          } else if (x < 0) {
                              x = 0;
                              vx = -vx;
                          }
                          printf("cuadro %d: x = %d, vx = %d\\n", cuadro, x, vx);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define ANCHO 100
                  #define LADO 10

                  int main(void)
                  {
                      int x = 70, vx = 15;
                      for (int cuadro = 1; cuadro <= 6; cuadro++) {
                          x += vx;
                          if (x > ANCHO - LADO) {
                              x = ANCHO - LADO;
                              vx = -vx;
                          } else if (x < 0) {
                              x = 0;
                              vx = -vx;
                          }
                          printf("cuadro %d: x = %d, vx = %d\\n", cuadro, x, vx);
                      }
                      return 0;
                  }
              ''',
              al_superar="La caja choca, vuelve y sigue. Ferrum la mira rebotar un rato largo, hipnotizado. Nadie se anima a interrumpirlo.",
              imagen=["Una caja de luz que rebota contra el borde de una pantalla, dejando una estela.", FERRUM + " hipnotizado mirándola."]),
        ],
    },
    {
        "titulo": "S01-N02 · Teclado, mouse y movimiento",
        "misiones": [
            m(id="S01-N02-P1", titulo="Apretar o mantener",
              lugar=VIVA, personajes="Kira, Gheco, Tizón",
              carta="Teclas | un evento dice «se apretó» una vez · el estado dice «está apretada» en cada cuadro · saltar va con el evento, caminar con el estado",
              recompensa="xp 15, oro 15",
              escena="El personaje de Kira salta **todo el tiempo** mientras mantiene la tecla, como un resorte. Tizón lo mide: 60 saltos por segundo. " + SIN_VENTANA,
              sugiere="«Recién apretada» es: está apretada **ahora** y **no** lo estaba en el cuadro anterior. Para saltar se usa eso; para caminar alcanza con «está apretada».",
              desafio="Completá la condición de «recién apretada».",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  int main(void)
                  {
                      /* la tecla de saltar en 6 cuadros seguidos: 1 = apretada */
                      bool tecla[6] = { false, true, true, true, false, true };
                      bool antes = false;
                      int saltos = 0;
                      for (int c = 0; c < 6; c++) {
                          if (___) {
                              saltos++;
                              printf("cuadro %d: salta\\n", c);
                          }
                          antes = tecla[c];
                      }
                      printf("saltos: %d\\n", saltos);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  int main(void)
                  {
                      /* la tecla de saltar en 6 cuadros seguidos: 1 = apretada */
                      bool tecla[6] = { false, true, true, true, false, true };
                      bool antes = false;
                      int saltos = 0;
                      for (int c = 0; c < 6; c++) {
                          if (tecla[c] && !antes) {
                              saltos++;
                              printf("cuadro %d: salta\\n", c);
                          }
                          antes = tecla[c];
                      }
                      printf("saltos: %d\\n", saltos);
                      return 0;
                  }
              ''',
              al_superar="Dos saltos, uno por apretada. El personaje deja de rebotar como un resorte. Tizón anota: «Golpe de martillo ≠ sostener el martillo».",
              imagen=["Un personaje pixelado que salta una vez sobre una plataforma.", TIZON + " anota en la libreta."]),
            m(id="S01-N02-P2", titulo="Caminar en diagonal",
              lugar=VIVA, personajes="Kira, Gheco, Chispa",
              carta="Dirección | sumar las teclas: derecha +1, izquierda -1 · en diagonal, normalizar para no ir más rápido · dividir por la raíz de 2",
              recompensa="xp 15, oro 15",
              escena="Chispa descubrió que caminando en diagonal su personaje va **más rápido** que derecho, y lo usa para ganar todas las carreras. Kira lo arregla.",
              sugiere="Con derecha y abajo a la vez, el vector es (1, 1), que mide raíz de 2. Para que mida 1, se divide cada parte por `sqrt(dx*dx + dy*dy)` (si no es 0).",
              desafio="Completá la normalización.",
              inicial='''
                  #include <stdio.h>
                  #include <math.h>

                  void mover(int derecha, int izquierda, int abajo, int arriba)
                  {
                      double dx = derecha - izquierda;
                      double dy = abajo - arriba;
                      double largo = sqrt(dx * dx + dy * dy);
                      if (largo > 0) {
                          ___;
                          ___;
                      }
                      printf("paso: (%.3f, %.3f)\\n", dx, dy);
                  }

                  int main(void)
                  {
                      mover(1, 0, 0, 0);
                      mover(1, 0, 1, 0);
                      mover(0, 0, 0, 0);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <math.h>

                  void mover(int derecha, int izquierda, int abajo, int arriba)
                  {
                      double dx = derecha - izquierda;
                      double dy = abajo - arriba;
                      double largo = sqrt(dx * dx + dy * dy);
                      if (largo > 0) {
                          dx /= largo;
                          dy /= largo;
                      }
                      printf("paso: (%.3f, %.3f)\\n", dx, dy);
                  }

                  int main(void)
                  {
                      mover(1, 0, 0, 0);
                      mover(1, 0, 1, 0);
                      mover(0, 0, 0, 0);
                      return 0;
                  }
              ''',
              al_superar="En diagonal, cada paso mide lo mismo. Chispa pierde su truco y su primera carrera. Pide revancha por diagonal. No hay diagonal más rápida.",
              imagen=["Dos personajes pixelados corriendo, uno derecho y otro en diagonal, llegando juntos.", CHISPA + " con cara de estafado."]),
            m(id="S01-N02-P3", titulo="No salirse de la pantalla",
              lugar=VIVA, personajes="Kira, Gheco, Tizón",
              carta="Limitar | después de mover, x = limitar(x, 0, ANCHO - LADO) · lo mismo con y · el personaje se frena en el borde",
              recompensa="xp 15, oro 15",
              escena="El personaje de Kira se va por el borde y no vuelve. Lo vuelve a crear. Lo vuelve a perder. Tizón dibuja con tiza el borde de la pantalla en el piso, por las dudas.",
              sugiere="Después de mover, se limita cada coordenada al rango de la pantalla con una función `limitar(valor, min, max)`.",
              desafio="Completá `limitar`.",
              inicial='''
                  #include <stdio.h>

                  #define ANCHO 320
                  #define LADO 16

                  int limitar(int valor, int min, int max)
                  {
                      ___
                  }

                  int main(void)
                  {
                      int pruebas[4] = { -20, 100, 310, 400 };
                      for (int i = 0; i < 4; i++) {
                          printf("%d -> %d\\n", pruebas[i], limitar(pruebas[i], 0, ANCHO - LADO));
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define ANCHO 320
                  #define LADO 16

                  int limitar(int valor, int min, int max)
                  {
                      if (valor < min) {
                          return min;
                      }
                      if (valor > max) {
                          return max;
                      }
                      return valor;
                  }

                  int main(void)
                  {
                      int pruebas[4] = { -20, 100, 310, 400 };
                      for (int i = 0; i < 4; i++) {
                          printf("%d -> %d\\n", pruebas[i], limitar(pruebas[i], 0, ANCHO - LADO));
                      }
                      return 0;
                  }
              ''',
              al_superar="Ni para un lado ni para el otro. El personaje se frena en el borde. Tizón borra la tiza del piso, con un poquito de pena.",
              imagen=["Un personaje pixelado que choca contra el borde de la pantalla y se queda.", TIZON + " borra una línea de tiza del piso."]),
        ],
    },
    {
        "titulo": "S01-N03 · Colisiones y enemigos",
        "misiones": [
            m(id="S01-N03-P1", titulo="¿Se tocan?",
              lugar=VIVA, personajes="Kira, Gheco, Tizón",
              carta="Colisión entre rectángulos | se tocan si se superponen en x Y en y · a.x < b.x + b.ancho && b.x < a.x + a.ancho · lo mismo en y",
              recompensa="xp 15, oro 15",
              escena="Las criaturas de Kira atraviesan las paredes como fantasmas toda la tarde. Chispa propone venderlas como «función nueva». Tizón propone preguntar si dos rectángulos se tocan.",
              sugiere="Dos rectángulos se superponen si se superponen **en x** (`a.x < b.x + b.w && b.x < a.x + a.w`) **y** en y (lo mismo con `y` y `h`).",
              desafio="Completá la superposición en y.",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  typedef struct {
                      int x, y, w, h;
                  } Rect;

                  bool se_tocan(Rect a, Rect b)
                  {
                      return a.x < b.x + b.w && b.x < a.x + a.w && ___;
                  }

                  int main(void)
                  {
                      Rect kira = { 10, 10, 16, 16 };
                      Rect pared = { 20, 0, 8, 40 };
                      Rect moneda = { 60, 60, 8, 8 };
                      Rect techo = { 0, 30, 50, 4 };
                      printf("pared: %d, moneda: %d, techo: %d\\n", se_tocan(kira, pared), se_tocan(kira, moneda), se_tocan(kira, techo));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  typedef struct {
                      int x, y, w, h;
                  } Rect;

                  bool se_tocan(Rect a, Rect b)
                  {
                      return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
                  }

                  int main(void)
                  {
                      Rect kira = { 10, 10, 16, 16 };
                      Rect pared = { 20, 0, 8, 40 };
                      Rect moneda = { 60, 60, 8, 8 };
                      Rect techo = { 0, 30, 50, 4 };
                      printf("pared: %d, moneda: %d, techo: %d\\n", se_tocan(kira, pared), se_tocan(kira, moneda), se_tocan(kira, techo));
                      return 0;
                  }
              ''',
              al_superar="Pared sí, moneda no, techo no. Las criaturas dejan de atravesar paredes. Chispa se queda sin producto nuevo.",
              imagen=["Tres rectángulos de luz alrededor de un personaje; uno se ilumina en rojo al tocarlo.", CHISPA + " decepcionado."]),
            m(id="S01-N03-P2", titulo="La criatura que persigue",
              lugar=VIVA, personajes="Kira, Gheco, Tizón",
              carta="Perseguir | en cada cuadro, acercarse un paso: si está a la derecha, x++; si a la izquierda, x-- · lo mismo en y",
              recompensa="xp 15, oro 15",
              escena="Las criaturas de hierro de la Forja Viva siguen el rastro de Kira. La primera que programó ella se queda quieta mirando a la nada, «pensando».",
              sugiere="En cada cuadro, la criatura compara su posición con la de Kira y da **un paso** hacia ella en cada eje (si ya está alineada en un eje, no se mueve en ese).",
              desafio="Completá el paso en x.",
              inicial='''
                  #include <stdio.h>

                  int paso_hacia(int desde, int hasta)
                  {
                      if (desde < hasta) {
                          return desde + 1;
                      }
                      if (desde > hasta) {
                          return desde - 1;
                      }
                      return desde;
                  }

                  int main(void)
                  {
                      int kx = 5, ky = 3;
                      int cx = 1, cy = 5;
                      for (int cuadro = 1; cuadro <= 4; cuadro++) {
                          cx = ___;
                          cy = paso_hacia(cy, ky);
                          printf("cuadro %d: criatura en (%d, %d)\\n", cuadro, cx, cy);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int paso_hacia(int desde, int hasta)
                  {
                      if (desde < hasta) {
                          return desde + 1;
                      }
                      if (desde > hasta) {
                          return desde - 1;
                      }
                      return desde;
                  }

                  int main(void)
                  {
                      int kx = 5, ky = 3;
                      int cx = 1, cy = 5;
                      for (int cuadro = 1; cuadro <= 4; cuadro++) {
                          cx = paso_hacia(cx, kx);
                          cy = paso_hacia(cy, ky);
                          printf("cuadro %d: criatura en (%d, %d)\\n", cuadro, cx, cy);
                      }
                      return 0;
                  }
              ''',
              al_superar="Cuatro cuadros y la criatura llega a Kira. Ella grita, aunque la programó ella. Tizón cronometra el grito.",
              imagen=["Una criatura de hierro pixelada que avanza en diagonal hacia un personaje.", KIRA + " retrocede con un grito."]),
            m(id="S01-N03-P3", titulo="Juntar las monedas",
              lugar=VIVA, personajes="Kira, Gheco, Chispa",
              carta="Recolectar | recorrer las monedas activas · si toca al personaje, se desactiva y suma · nunca se cuenta dos veces",
              recompensa="xp 15, oro 15",
              escena="Hay monedas de fuego frío por todo el nivel. Chispa propone que valgan el doble «si las agarra él». Kira hace que cada moneda se cuente **una sola vez**.",
              sugiere="Cada moneda tiene `activa`. Si está activa y toca al personaje, se desactiva y se suma. Desactivada, ya no cuenta aunque la vuelva a tocar.",
              desafio="Completá la condición y la recolección.",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  typedef struct {
                      int x;
                      bool activa;
                  } Moneda;

                  int main(void)
                  {
                      Moneda m[3] = { { 4, true }, { 7, true }, { 9, true } };
                      int recorrido[6] = { 3, 4, 4, 5, 7, 4 };
                      int juntadas = 0;
                      for (int paso = 0; paso < 6; paso++) {
                          for (int i = 0; i < 3; i++) {
                              if (___) {
                                  ___;
                                  juntadas++;
                                  printf("paso %d: moneda en %d\\n", paso, m[i].x);
                              }
                          }
                      }
                      printf("monedas: %d de 3\\n", juntadas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  typedef struct {
                      int x;
                      bool activa;
                  } Moneda;

                  int main(void)
                  {
                      Moneda m[3] = { { 4, true }, { 7, true }, { 9, true } };
                      int recorrido[6] = { 3, 4, 4, 5, 7, 4 };
                      int juntadas = 0;
                      for (int paso = 0; paso < 6; paso++) {
                          for (int i = 0; i < 3; i++) {
                              if (m[i].activa && m[i].x == recorrido[paso]) {
                                  m[i].activa = false;
                                  juntadas++;
                                  printf("paso %d: moneda en %d\\n", paso, m[i].x);
                              }
                          }
                      }
                      printf("monedas: %d de 3\\n", juntadas);
                      return 0;
                  }
              ''',
              al_superar="Dos de tres, cada una contada una vez. Chispa pasa tres veces por la misma moneda «por si acaso». Sigue valiendo una.",
              imagen=["Monedas de fuego frío flotando en un nivel pixelado; dos se apagan al ser tocadas.", CHISPA + " pasa una y otra vez por el mismo lugar."]),
        ],
    },
    {
        "titulo": "S01-N04 · Jefe de la Forja Viva: la Salamandra del Horno",
        "misiones": [
            m(id="S01-N04-P1", titulo="Los estados del juego",
              lugar=VIVA, personajes="Kira, Gheco, Tizón",
              criatura="dragon",
              carta="Máquina de estados | enum { MENU, JUGANDO, GANASTE, PERDISTE } · cada estado decide qué se actualiza · las transiciones, en un solo lugar",
              recompensa="xp 20, oro 20",
              escena="En el corazón de la Forja Viva vive la **Salamandra del Horno**. La primera partida dura cuatro segundos, y el juego sigue «jugando» después de perder. Kira ordena el juego en **estados**.",
              sugiere="El juego está siempre en **un** estado. Según el evento (`empezar`, `todas las monedas`, `te alcanzó`), cambia de estado. Una función `siguiente(estado, evento)` decide.",
              desafio="Completá las dos transiciones que faltan.",
              inicial='''
                  #include <stdio.h>

                  typedef enum { MENU, JUGANDO, GANASTE, PERDISTE } Estado;
                  typedef enum { EMPEZAR, MONEDAS, ALCANZADA } Evento;

                  const char *nombre(Estado e)
                  {
                      const char *n[] = { "menu", "jugando", "ganaste", "perdiste" };
                      return n[e];
                  }

                  Estado siguiente(Estado e, Evento ev)
                  {
                      if (e == MENU && ev == EMPEZAR) {
                          return JUGANDO;
                      }
                      if (e == JUGANDO && ev == MONEDAS) {
                          return ___;
                      }
                      if (e == JUGANDO && ev == ALCANZADA) {
                          return ___;
                      }
                      return e;
                  }

                  int main(void)
                  {
                      Evento partida[4] = { MONEDAS, EMPEZAR, ALCANZADA, MONEDAS };
                      Estado e = MENU;
                      for (int i = 0; i < 4; i++) {
                          e = siguiente(e, partida[i]);
                          printf("%s\\n", nombre(e));
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef enum { MENU, JUGANDO, GANASTE, PERDISTE } Estado;
                  typedef enum { EMPEZAR, MONEDAS, ALCANZADA } Evento;

                  const char *nombre(Estado e)
                  {
                      const char *n[] = { "menu", "jugando", "ganaste", "perdiste" };
                      return n[e];
                  }

                  Estado siguiente(Estado e, Evento ev)
                  {
                      if (e == MENU && ev == EMPEZAR) {
                          return JUGANDO;
                      }
                      if (e == JUGANDO && ev == MONEDAS) {
                          return GANASTE;
                      }
                      if (e == JUGANDO && ev == ALCANZADA) {
                          return PERDISTE;
                      }
                      return e;
                  }

                  int main(void)
                  {
                      Evento partida[4] = { MONEDAS, EMPEZAR, ALCANZADA, MONEDAS };
                      Estado e = MENU;
                      for (int i = 0; i < 4; i++) {
                          e = siguiente(e, partida[i]);
                          printf("%s\\n", nombre(e));
                      }
                      return 0;
                  }
              ''',
              al_superar="Perder ahora es perder: el juego no sigue solo. Tizón lleva la estadística de partidas en la pared, al lado de la cuenta de espadazos.",
              imagen=[SALAMANDRA + " corre por una pantalla que muestra «PERDISTE».", TIZON + " anota en la pared."]),
            m(id="S01-N04-P2", titulo="La Salamandra se duerme",
              lugar=VIVA, personajes="Kira, Gheco, Tizón, Maese Ferrum",
              criatura="dragon",
              carta="El juego entero | bucle + movimiento + persecución + colisiones + estados · cada parte en su función · un juego que alguien quiera jugar dos veces",
              recompensa="xp 30, oro 30",
              escena="""
                  Última partida. Kira tiene el recorrido planeado en la libreta de Tizón. Si junta las tres monedas antes de que la Salamandra la alcance, la Salamandra se duerme.
              """,
              sugiere="En cada cuadro: Kira avanza un paso de su recorrido, junta lo que toca, la Salamandra da un paso hacia ella, y se revisa si la alcanzó. El juego termina en `GANASTE` o `PERDISTE`.",
              desafio="Completá la condición de victoria y la de derrota.",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  int paso_hacia(int desde, int hasta)
                  {
                      return desde < hasta ? desde + 1 : desde > hasta ? desde - 1 : desde;
                  }

                  int main(void)
                  {
                      int recorrido[6] = { 2, 3, 4, 5, 6, 7 };
                      int monedas[3] = { 3, 5, 7 };
                      bool juntada[3] = { false, false, false };
                      int juntadas = 0;
                      int salamandra = -4;
                      for (int c = 0; c < 6; c++) {
                          int kira = recorrido[c];
                          for (int i = 0; i < 3; i++) {
                              if (!juntada[i] && monedas[i] == kira) {
                                  juntada[i] = true;
                                  juntadas++;
                              }
                          }
                          salamandra = paso_hacia(salamandra, kira);
                          printf("cuadro %d: Kira en %d, salamandra en %d, monedas %d\\n", c + 1, kira, salamandra, juntadas);
                          if (___) {
                              printf("GANASTE: la salamandra se duerme\\n");
                              break;
                          }
                          if (___) {
                              printf("PERDISTE: la salamandra te alcanzo\\n");
                              break;
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  int paso_hacia(int desde, int hasta)
                  {
                      return desde < hasta ? desde + 1 : desde > hasta ? desde - 1 : desde;
                  }

                  int main(void)
                  {
                      int recorrido[6] = { 2, 3, 4, 5, 6, 7 };
                      int monedas[3] = { 3, 5, 7 };
                      bool juntada[3] = { false, false, false };
                      int juntadas = 0;
                      int salamandra = -4;
                      for (int c = 0; c < 6; c++) {
                          int kira = recorrido[c];
                          for (int i = 0; i < 3; i++) {
                              if (!juntada[i] && monedas[i] == kira) {
                                  juntada[i] = true;
                                  juntadas++;
                              }
                          }
                          salamandra = paso_hacia(salamandra, kira);
                          printf("cuadro %d: Kira en %d, salamandra en %d, monedas %d\\n", c + 1, kira, salamandra, juntadas);
                          if (juntadas == 3) {
                              printf("GANASTE: la salamandra se duerme\\n");
                              break;
                          }
                          if (salamandra == kira) {
                              printf("PERDISTE: la salamandra te alcanzo\\n");
                              break;
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Tres monedas, y la Salamandra todavía a dos pasos. Se acurruca en un rincón de la pantalla y se duerme, chisporroteando bajito. Ferrum pide jugar. Pierde en cuatro segundos. Pide revancha.",
              imagen=[SALAMANDRA + " dormida en un rincón de la pantalla, chisporroteando.", KIRA + " con tres monedas de fuego frío en la mano.", FERRUM + " agarra el control, entusiasmado."]),
        ],
    },
    {
        "titulo": "S02-N01 · Los Autómatas: el primer autómata",
        "misiones": [
            m(id="S02-N01-P1", titulo="Parpadear sin delay",
              lugar=TALLER, personajes="Kira, Gheco, Tizón",
              carta="El tiempo sin frenar | guardar cuándo fue el último cambio · si ya pasó el intervalo, cambiar y anotar el momento · millis() en la placa",
              recompensa="xp 15, oro 15",
              escena="Kira prende su primera luz y se queda mirándola un minuto entero. Con `delay`, la placa no hace **nada más** mientras espera. Tizón quiere que parpadee y que, a la vez, siga escuchando. " + SIN_PLACA,
              sugiere="En lugar de esperar, se guarda `ultimo` (el momento del último cambio). En cada vuelta, si `ahora - ultimo >= INTERVALO`, se cambia el led y `ultimo = ahora`.",
              desafio="Completá la condición y lo que se anota.",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  #define INTERVALO 500

                  int main(void)
                  {
                      bool led = false;
                      unsigned long ultimo = 0;
                      for (unsigned long ahora = 0; ahora <= 2000; ahora += 100) {
                          if (___) {
                              led = !led;
                              ___;
                              printf("%lu ms: led %s\\n", ahora, led ? "prendido" : "apagado");
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  #define INTERVALO 500

                  int main(void)
                  {
                      bool led = false;
                      unsigned long ultimo = 0;
                      for (unsigned long ahora = 0; ahora <= 2000; ahora += 100) {
                          if (ahora - ultimo >= INTERVALO) {
                              led = !led;
                              ultimo = ahora;
                              printf("%lu ms: led %s\\n", ahora, led ? "prendido" : "apagado");
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Cada medio segundo, exacto. Tizón lo mide: «Quinientos. Exacto. Bien». Y la placa sigue libre para escuchar lo que venga.",
              imagen=["Una placa de electrónica con un led rojo que parpadea, sobre una mesa de latón.", KIRA + " mira el led, fascinada.", TIZON + " con un cronómetro."]),
            m(id="S02-N01-P2", titulo="El semáforo del Taller",
              lugar=TALLER, personajes="Kira, Gheco, Chispa",
              carta="Secuencias con tiempo | un estado y cuánto dura cada uno · al terminar el tiempo, pasar al siguiente · % para volver a empezar",
              recompensa="xp 15, oro 15",
              escena="La puerta del Taller tiene un semáforo para que los autómatas no choquen. Chispa lo cruza siempre en rojo «porque tiene apuro». Kira programa el ciclo.",
              sugiere="Tres estados con su duración: verde 3000, amarillo 1000, rojo 2000. Cuando pasó la duración del estado actual, se pasa al siguiente con `(estado + 1) % 3`.",
              desafio="Completá el cambio de estado.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      const char *nombres[3] = { "verde", "amarillo", "rojo" };
                      unsigned long duracion[3] = { 3000, 1000, 2000 };
                      int estado = 0;
                      unsigned long desde = 0;
                      printf("0 ms: verde\\n");
                      for (unsigned long ahora = 0; ahora <= 8000; ahora += 500) {
                          if (ahora - desde >= duracion[estado]) {
                              estado = ___;
                              desde = ahora;
                              printf("%lu ms: %s\\n", ahora, nombres[estado]);
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      const char *nombres[3] = { "verde", "amarillo", "rojo" };
                      unsigned long duracion[3] = { 3000, 1000, 2000 };
                      int estado = 0;
                      unsigned long desde = 0;
                      printf("0 ms: verde\\n");
                      for (unsigned long ahora = 0; ahora <= 8000; ahora += 500) {
                          if (ahora - desde >= duracion[estado]) {
                              estado = (estado + 1) % 3;
                              desde = ahora;
                              printf("%lu ms: %s\\n", ahora, nombres[estado]);
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Verde, amarillo, rojo, verde. Chispa espera el verde por primera vez. Le parece una eternidad. Fueron dos segundos.",
              imagen=["Un semáforo de latón con tres luces en la puerta del Taller.", CHISPA + " esperando, impaciente, con un pie golpeando el piso."]),
            m(id="S02-N01-P3", titulo="Los bits del puerto",
              lugar=TALLER, personajes="Kira, Gheco, Tizón",
              carta="Pines como bits | un byte puede ser 8 leds · encender: puerto |= (1 << pin) · apagar: puerto &= ~(1 << pin)",
              recompensa="xp 15, oro 15",
              escena="El autómata tiene 8 leds en el pecho, y el Taller los guarda en un solo byte: cada bit, un led. Tizón quiere encender el 0 y el 3 y apagar el 7, sin tocar los demás.",
              sugiere="Encender el led `n`: `puerto |= (1 << n)`. Apagarlo: `puerto &= ~(1 << n)`. `%02X` muestra el byte en hexa con dos cifras.",
              desafio="Completá el encendido y el apagado.",
              inicial='''
                  #include <stdio.h>

                  void mostrar(unsigned char puerto)
                  {
                      for (int pin = 7; pin >= 0; pin--) {
                          putchar(puerto & (1 << pin) ? '*' : '.');
                      }
                      printf("  0x%02X\\n", puerto);
                  }

                  int main(void)
                  {
                      unsigned char puerto = 0x80;
                      mostrar(puerto);
                      puerto ___ (1 << 0);
                      puerto ___ (1 << 3);
                      mostrar(puerto);
                      puerto ___ ~(1 << 7);
                      mostrar(puerto);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  void mostrar(unsigned char puerto)
                  {
                      for (int pin = 7; pin >= 0; pin--) {
                          putchar(puerto & (1 << pin) ? '*' : '.');
                      }
                      printf("  0x%02X\\n", puerto);
                  }

                  int main(void)
                  {
                      unsigned char puerto = 0x80;
                      mostrar(puerto);
                      puerto |= (1 << 0);
                      puerto |= (1 << 3);
                      mostrar(puerto);
                      puerto &= ~(1 << 7);
                      mostrar(puerto);
                      return 0;
                  }
              ''',
              al_superar="Dos leds prendidos, uno apagado, el resto intacto. El pecho del autómata dibuja una carita. Tizón jura que no fue a propósito.",
              imagen=["El pecho de un autómata de latón con una fila de 8 leds, algunos encendidos.", TIZON + " sonríe, sospechosamente."]),
        ],
    },
    {
        "titulo": "S02-N02 · Botones y perillas",
        "misiones": [
            m(id="S02-N02-P1", titulo="El botón que rebota",
              lugar=TALLER, personajes="Kira, Gheco, Tizón",
              carta="Antirrebote | el contacto rebota unos milisegundos · aceptar el cambio solo si la lectura se mantuvo estable un tiempo · contar al apretar, no al rebotar",
              recompensa="xp 15, oro 15",
              escena="Kira aprieta un botón **una** vez y el autómata cuenta **siete**. Tizón se pasa la tarde mirando el botón con la lupa hasta que lo ve: el contacto **rebota** como una pelota. " + SIN_PLACA,
              sugiere="Se guarda la última lectura cruda y desde cuándo está así. El estado «de verdad» cambia solo si la lectura cruda se mantuvo igual al menos `ESTABLE` ms. Y se cuenta cuando ese estado pasa a apretado.",
              desafio="Completá la condición de lectura estable.",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  #define ESTABLE 20

                  int main(void)
                  {
                      /* lecturas cada 5 ms: 1 = apretado (rebota al apretar y al soltar) */
                      int lectura[16] = { 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0 };
                      int estable = 0, ultima = 0, pulsaciones = 0;
                      unsigned long desde = 0;
                      for (int i = 0; i < 16; i++) {
                          unsigned long ahora = i * 5;
                          if (lectura[i] != ultima) {
                              ultima = lectura[i];
                              desde = ahora;
                          }
                          if (___ && ultima != estable) {
                              estable = ultima;
                              if (estable == 1) {
                                  pulsaciones++;
                                  printf("%2lu ms: apretado\\n", ahora);
                              }
                          }
                      }
                      printf("pulsaciones: %d\\n", pulsaciones);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  #define ESTABLE 20

                  int main(void)
                  {
                      /* lecturas cada 5 ms: 1 = apretado (rebota al apretar y al soltar) */
                      int lectura[16] = { 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0 };
                      int estable = 0, ultima = 0, pulsaciones = 0;
                      unsigned long desde = 0;
                      for (int i = 0; i < 16; i++) {
                          unsigned long ahora = i * 5;
                          if (lectura[i] != ultima) {
                              ultima = lectura[i];
                              desde = ahora;
                          }
                          if (ahora - desde >= ESTABLE && ultima != estable) {
                              estable = ultima;
                              if (estable == 1) {
                                  pulsaciones++;
                                  printf("%2lu ms: apretado\\n", ahora);
                              }
                          }
                      }
                      printf("pulsaciones: %d\\n", pulsaciones);
                      return 0;
                  }
              ''',
              al_superar="Una pulsación, aunque el contacto rebotó cuatro veces. Tizón guarda la lupa con cariño: fue su gran descubrimiento.",
              imagen=["Un botón de latón visto con lupa, con chispitas de rebote en el contacto.", TIZON + " con la lupa en la mano, triunfante."]),
            m(id="S02-N02-P2", titulo="La perilla y el servo",
              lugar=TALLER, personajes="Kira, Gheco, Chispa",
              carta="map() | llevar un valor de un rango a otro · (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min · la perilla da 0 a 1023, el servo va de 0 a 180",
              recompensa="xp 15, oro 15",
              escena="La perilla del autómata da números de 0 a 1023, y el brazo (un servo) va de 0 a 180 grados. Chispa giró la perilla al máximo y el brazo intentó ir a 1023 grados. Hubo un ruido feo.",
              sugiere="`mapear(x, in_min, in_max, out_min, out_max)` hace la regla de tres. Con enteros, multiplicar antes de dividir para no perder precisión.",
              desafio="Completá la cuenta de `mapear`.",
              inicial='''
                  #include <stdio.h>

                  long mapear(long x, long in_min, long in_max, long out_min, long out_max)
                  {
                      return ___;
                  }

                  int main(void)
                  {
                      long lecturas[4] = { 0, 512, 767, 1023 };
                      for (int i = 0; i < 4; i++) {
                          printf("perilla %4ld -> brazo a %3ld grados\\n", lecturas[i], mapear(lecturas[i], 0, 1023, 0, 180));
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  long mapear(long x, long in_min, long in_max, long out_min, long out_max)
                  {
                      return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
                  }

                  int main(void)
                  {
                      long lecturas[4] = { 0, 512, 767, 1023 };
                      for (int i = 0; i < 4; i++) {
                          printf("perilla %4ld -> brazo a %3ld grados\\n", lecturas[i], mapear(lecturas[i], 0, 1023, 0, 180));
                      }
                      return 0;
                  }
              ''',
              al_superar="De 0 a 180, sin ruidos feos. El brazo del autómata saluda a Chispa. Chispa no sabe si es un saludo o una amenaza.",
              imagen=["Un brazo de autómata de latón que gira suave, con una perilla al lado.", CHISPA + " devuelve el saludo, inseguro."]),
            m(id="S02-N02-P3", titulo="Promediar la perilla",
              lugar=TALLER, personajes="Kira, Gheco, Tizón",
              carta="Suavizar lecturas | las lecturas analógicas tiemblan · promediar las últimas N con un array circular · la suma se actualiza sin recorrer todo",
              recompensa="xp 15, oro 15",
              escena="La perilla tiembla: 510, 515, 508, 600 (un salto), 512… y el brazo tiembla con ella. Tizón propone promediar las últimas 4 lecturas.",
              sugiere="Un array circular de 4: al llegar una lectura, se resta de la suma la que sale, se guarda la nueva en su lugar y se suma. El promedio es `suma / 4` (cuando ya hay 4).",
              desafio="Completá la actualización de la suma.",
              inicial='''
                  #include <stdio.h>

                  #define N 4

                  int main(void)
                  {
                      int lecturas[8] = { 510, 515, 508, 600, 512, 509, 514, 511 };
                      int ventana[N] = { 0 };
                      int suma = 0;
                      for (int i = 0; i < 8; i++) {
                          int pos = i % N;
                          suma -= ___;
                          ventana[pos] = lecturas[i];
                          suma += ___;
                          if (i >= N - 1) {
                              printf("lectura %d: promedio %d\\n", lecturas[i], suma / N);
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define N 4

                  int main(void)
                  {
                      int lecturas[8] = { 510, 515, 508, 600, 512, 509, 514, 511 };
                      int ventana[N] = { 0 };
                      int suma = 0;
                      for (int i = 0; i < 8; i++) {
                          int pos = i % N;
                          suma -= ventana[pos];
                          ventana[pos] = lecturas[i];
                          suma += ventana[pos];
                          if (i >= N - 1) {
                              printf("lectura %d: promedio %d\\n", lecturas[i], suma / N);
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="El salto de 600 apenas mueve el promedio. El brazo deja de temblar. Tizón, en cambio, tiembla de emoción.",
              imagen=["Un gráfico de líneas sobre un pergamino: una línea que tiembla y otra suave encima.", TIZON + " emocionado."]),
        ],
    },
    {
        "titulo": "S02-N03 · Hablar con la compu",
        "misiones": [
            m(id="S02-N03-P1", titulo="Una línea por mensaje",
              lugar=TALLER, personajes="Kira, Gheco, Tizón",
              carta="Protocolo de texto | una línea por mensaje · la primera letra dice qué es · S temperatura, B botón · lo que no se entiende, se ignora",
              recompensa="xp 15, oro 15",
              escena="El primer autómata de Kira le manda a la compu un mensaje larguísimo sin pausas y la compu entiende «BANANA». Tizón inventa un idioma: **una línea por mensaje**, con una letra al principio que dice de qué se trata.",
              sugiere="Se lee línea por línea. `S 23` es un sensor con su valor; `B 1` es el botón. Con `sscanf(linea, \"%c %d\", &tipo, &valor) == 2` se separan. Lo que no encaja se cuenta como ignorado.",
              desafio="Completá la lectura del mensaje.",
              entrada="S 23\nB 1\nBANANA\nS 25\n\nB 0\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[50];
                      char tipo;
                      int valor, ignoradas = 0;
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (___ && (tipo == 'S' || tipo == 'B')) {
                              printf(tipo == 'S' ? "sensor: %d grados\\n" : "boton: %d\\n", valor);
                          } else {
                              ignoradas++;
                          }
                      }
                      printf("ignoradas: %d\\n", ignoradas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[50];
                      char tipo;
                      int valor, ignoradas = 0;
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (sscanf(linea, "%c %d", &tipo, &valor) == 2 && (tipo == 'S' || tipo == 'B')) {
                              printf(tipo == 'S' ? "sensor: %d grados\\n" : "boton: %d\\n", valor);
                          } else {
                              ignoradas++;
                          }
                      }
                      printf("ignoradas: %d\\n", ignoradas);
                      return 0;
                  }
              ''',
              al_superar="Cuatro mensajes entendidos, dos ignorados, ni una banana. Funciona a la primera; Tizón no lo puede creer y lo prueba tres veces más.",
              imagen=["Un cable que une un autómata de latón con una compu; por el cable viajan renglones de luz.", TIZON + " incrédulo."]),
            m(id="S02-N03-P2", titulo="La suma de control",
              lugar=TALLER, personajes="Kira, Gheco, Chispa",
              carta="Checksum | el que manda agrega un número calculado con los datos · el que recibe lo recalcula · si no coincide, el mensaje se dañó en el camino",
              recompensa="xp 15, oro 15",
              escena="Chispa se paró arriba del cable y algunos mensajes llegan cambiados. Kira agrega a cada mensaje una **suma de control**: si no coincide, el mensaje se descarta.",
              sugiere="El mensaje es `S valor suma`, donde `suma = valor % 97`. Al recibir, se recalcula: si `valor % 97 != suma`, el mensaje está dañado.",
              desafio="Completá la comprobación.",
              entrada="S 230 36\nS 251 57\nS 240 99\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[50];
                      char tipo;
                      int valor, suma;
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (sscanf(linea, "%c %d %d", &tipo, &valor, &suma) != 3) {
                              continue;
                          }
                          if (___) {
                              printf("valor %d: ok\\n", valor);
                          } else {
                              printf("valor %d: danado, se descarta\\n", valor);
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[50];
                      char tipo;
                      int valor, suma;
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (sscanf(linea, "%c %d %d", &tipo, &valor, &suma) != 3) {
                              continue;
                          }
                          if (valor % 97 == suma) {
                              printf("valor %d: ok\\n", valor);
                          } else {
                              printf("valor %d: danado, se descarta\\n", valor);
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="El mensaje dañado no pasa. Chispa se baja del cable. Dice que estaba «revisando la instalación».",
              imagen=["Un cable con un mensaje de luz que se pone rojo al pasar por debajo del pie de alguien.", CHISPA + " parado arriba del cable, silbando."]),
        ],
    },
    {
        "titulo": "S02-N04 · Jefe de los Autómatas: el Autómata Guardián",
        "misiones": [
            m(id="S02-N04-P1", titulo="El joystick de bronce",
              lugar=TALLER, personajes="Kira, Gheco, Tizón",
              criatura="dragon",
              carta="Zona muerta | el joystick en reposo no da exactamente el centro · lo que está cerca del centro cuenta como quieto · el resto da la dirección",
              recompensa="xp 20, oro 20",
              escena="""
                  En el fondo del Taller espera el **Autómata Guardián**, con un joystick de bronce. Kira lo agarra como si fuera una espada. El Guardián pita, ofendido. Ella lo suelta, respira, y lo vuelve a agarrar con dos dedos.
                  En reposo, el joystick no marca 512 exacto: marca 509, 515… y el personaje camina solo.
              """,
              sugiere="Los valores entre `CENTRO - ZONA` y `CENTRO + ZONA` se toman como quieto. Más abajo, `izquierda`; más arriba, `derecha`.",
              desafio="Completá la condición de la zona muerta.",
              entrada="509\n515\n100\n900\n540\n",
              inicial='''
                  #include <stdio.h>

                  #define CENTRO 512
                  #define ZONA 40

                  const char *direccion(int x)
                  {
                      if (___) {
                          return "quieto";
                      }
                      return x < CENTRO ? "izquierda" : "derecha";
                  }

                  int main(void)
                  {
                      int x;
                      while (scanf("%d", &x) == 1) {
                          printf("%d: %s\\n", x, direccion(x));
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define CENTRO 512
                  #define ZONA 40

                  const char *direccion(int x)
                  {
                      if (x > CENTRO - ZONA && x < CENTRO + ZONA) {
                          return "quieto";
                      }
                      return x < CENTRO ? "izquierda" : "derecha";
                  }

                  int main(void)
                  {
                      int x;
                      while (scanf("%d", &x) == 1) {
                          printf("%d: %s\\n", x, direccion(x));
                      }
                      return 0;
                  }
              ''',
              al_superar="El personaje se queda quieto cuando tiene que quedarse quieto. El Guardián deja de pitar. Las luces del pecho se ponen verdes, una por una.",
              imagen=[GUARDIAN + " con un joystick de bronce en la mano extendida.", KIRA + " lo agarra con dos dedos, concentrada."]),
            m(id="S02-N04-P2", titulo="La placa y la compu, cada una en lo suyo",
              lugar=TALLER, personajes="Kira, Gheco, Tizón, Maese Ferrum",
              criatura="dragon",
              carta="Todo junto | la placa manda una línea por evento · la compu interpreta y mueve el juego · cada parte en lo suyo, con un idioma simple",
              recompensa="xp 30, oro 30",
              escena="""
                  Última prueba del Guardián: recorrer la mazmorra del Dragón con **su** control. La placa manda `J` con la dirección y `B` cuando se aprieta el botón (que abre puertas). La compu mueve a Kira.
              """,
              sugiere="Por cada línea: `J -1` o `J 1` mueve a Kira un lugar; `B 1` abre la puerta si está justo al lado (la puerta está en 4). Al llegar a 6 con la puerta abierta, se gana.",
              desafio="Completá el movimiento y la apertura de la puerta.",
              entrada="J 1\nJ 1\nJ 1\nJ 1\nB 1\nJ 1\nJ 1\nJ 1\n",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  #define PUERTA 4
                  #define SALIDA 6

                  int main(void)
                  {
                      char linea[20], tipo;
                      int valor, pos = 0;
                      bool abierta = false;
                      while (fgets(linea, sizeof linea, stdin) != NULL && pos < SALIDA) {
                          if (sscanf(linea, "%c %d", &tipo, &valor) != 2) {
                              continue;
                          }
                          if (tipo == 'J') {
                              int nueva = pos + valor;
                              if (nueva == PUERTA && !abierta) {
                                  printf("la puerta esta cerrada\\n");
                              } else if (nueva >= 0) {
                                  ___;
                                  printf("Kira en %d\\n", pos);
                              }
                          } else if (tipo == 'B' && valor == 1 && ___) {
                              abierta = true;
                              printf("se abre la puerta\\n");
                          }
                      }
                      printf(pos == SALIDA ? "el guardian se inclina\\n" : "todavia no\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  #define PUERTA 4
                  #define SALIDA 6

                  int main(void)
                  {
                      char linea[20], tipo;
                      int valor, pos = 0;
                      bool abierta = false;
                      while (fgets(linea, sizeof linea, stdin) != NULL && pos < SALIDA) {
                          if (sscanf(linea, "%c %d", &tipo, &valor) != 2) {
                              continue;
                          }
                          if (tipo == 'J') {
                              int nueva = pos + valor;
                              if (nueva == PUERTA && !abierta) {
                                  printf("la puerta esta cerrada\\n");
                              } else if (nueva >= 0) {
                                  pos = nueva;
                                  printf("Kira en %d\\n", pos);
                              }
                          } else if (tipo == 'B' && valor == 1 && pos == PUERTA - 1) {
                              abierta = true;
                              printf("se abre la puerta\\n");
                          }
                      }
                      printf(pos == SALIDA ? "el guardian se inclina\\n" : "todavia no\\n");
                      return 0;
                  }
              ''',
              al_superar="Kira llega a la salida. El Autómata Guardián se inclina, las luces del pecho todas en verde, y pita una melodía corta. Tizón jura que es una canción de las Forjas. Ferrum, que la conoce, no dice nada y se seca un ojo.",
              imagen=[GUARDIAN + " inclinado, con todas las luces del pecho en verde.", KIRA + " con el joystick en la mano.", FERRUM + " se seca un ojo disimuladamente."]),
        ],
    },
]
