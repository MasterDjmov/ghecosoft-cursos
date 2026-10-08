from genc import m
from c_r01 import KIRA, TIZON, FERRUM, CHISPA
from c_r01b import HULDA

MINAS = "Las Minas"
SANGUIJUELA = "La Sanguijuela de las Minas (sanguijuela enorme y translúcida, violeta oscura, con vagonetas tragadas que se ven dentro de su cuerpo)"

NODOS = [
    {
        "titulo": "R03-N01 · Memoria dinámica",
        "misiones": [
            m(id="R03-N01-P1", titulo="Las vagonetas prestadas",
              lugar=MINAS, personajes="Kira, Gheco, Hulda",
              carta="malloc y free | malloc(n * sizeof *p) pide memoria · devuelve NULL si no hay · free(p) la devuelve",
              recompensa="xp 10, oro 10",
              escena="""
                  En la boca de las Minas, Hulda presta vagonetas y las anota en su tablilla. Kira pide lugar para guardar el peso de 5 cargas.
                  —Vagoneta que sacás, vagoneta que devolvés —dice Hulda, con el pico al hombro.
              """,
              sugiere="`int *cargas = malloc(5 * sizeof *cargas);` pide lugar para 5 enteros. Si devuelve `NULL`, no hubo lugar. Al terminar, `free(cargas);`.",
              desafio="Pedí la memoria y devolvela al final.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int *cargas = ___;
                      if (cargas == NULL) {
                          printf("no hay vagonetas\\n");
                          return 1;
                      }
                      for (int i = 0; i < 5; i++) {
                          cargas[i] = (i + 1) * 100;
                      }
                      printf("la ultima carga pesa %d\\n", cargas[4]);
                      ___;
                      printf("vagonetas devueltas\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int *cargas = malloc(5 * sizeof *cargas);
                      if (cargas == NULL) {
                          printf("no hay vagonetas\\n");
                          return 1;
                      }
                      for (int i = 0; i < 5; i++) {
                          cargas[i] = (i + 1) * 100;
                      }
                      printf("la ultima carga pesa %d\\n", cargas[4]);
                      free(cargas);
                      printf("vagonetas devueltas\\n");
                      return 0;
                  }
              ''',
              al_superar="Hulda tacha las cinco vagonetas de la tablilla, una por una. —Así me gusta. Ni un chiste malo.",
              imagen=["La boca de las Minas: vías que se pierden en la oscuridad y vagonetas en fila.", HULDA + " anota en una tablilla.", KIRA + " empuja una vagoneta de vuelta."]),
            m(id="R03-N01-P2", titulo="Tantas como haga falta",
              lugar=MINAS, personajes="Kira, Gheco, Tizón",
              carta="Tamaño en ejecución | el tamaño puede venir de la entrada · malloc(n * sizeof *v) · con un array fijo habría que adivinar",
              recompensa="xp 10, oro 10",
              escena="Tizón no sabe cuántas cargas van a llegar hoy: se lo dicen al empezar el turno. Con un array fijo tendría que adivinar. Con las vagonetas de Hulda, pide justo las que hacen falta.",
              sugiere="Se lee `n` y se pide `malloc(n * sizeof *v)`. Después se usa `v[i]` como cualquier array.",
              desafio="Pedí lugar para `n` cargas.",
              entrada="4\n120 80 200 50\n",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int n;
                      scanf("%d", &n);
                      int *v = ___;
                      if (v == NULL) {
                          return 1;
                      }
                      int total = 0;
                      for (int i = 0; i < n; i++) {
                          scanf("%d", &v[i]);
                          total += v[i];
                      }
                      printf("%d cargas, %d kg en total\\n", n, total);
                      free(v);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int n;
                      scanf("%d", &n);
                      int *v = malloc(n * sizeof *v);
                      if (v == NULL) {
                          return 1;
                      }
                      int total = 0;
                      for (int i = 0; i < n; i++) {
                          scanf("%d", &v[i]);
                          total += v[i];
                      }
                      printf("%d cargas, %d kg en total\\n", n, total);
                      free(v);
                      return 0;
                  }
              ''',
              al_superar="Cuatrocientos cincuenta kilos en cuatro vagonetas, ni una de más. Tizón calcula que se ahorraron seis vagonetas vacías. Lo celebra solo.",
              imagen=["Cuatro vagonetas cargadas de mineral en fila.", TIZON + " cuenta vagonetas con los dedos."]),
            m(id="R03-N01-P3", titulo="El chiste malo de Kira",
              lugar=MINAS, personajes="Kira, Gheco, Hulda",
              criatura="troll",
              carta="Fugas | cada malloc con su free · lo que no se devuelve se pierde hasta que el programa termina · en un bucle, la fuga crece",
              recompensa="xp 10, oro 10",
              escena="""
                  Kira pidió vagonetas en cada vuelta del turno y no devolvió ninguna. Hulda la frena con una mano del tamaño de una pala y la hace contar un chiste malo **frente a toda la mina**.
                  El chiste es tan malo que nadie en las Minas vuelve a olvidarse una vagoneta.
              """,
              sugiere="Si en cada vuelta se hace un `malloc`, en cada vuelta hace falta un `free` cuando ya no se usa. Si no, el **troll** se va comiendo la memoria.",
              desafio="Devolvé la vagoneta al final de cada vuelta.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int devueltas = 0;
                      for (int turno = 1; turno <= 3; turno++) {
                          int *carga = malloc(sizeof *carga);
                          if (carga == NULL) {
                              return 1;
                          }
                          *carga = turno * 50;
                          printf("turno %d: %d kg\\n", turno, *carga);
                      }
                      printf("vagonetas devueltas: %d\\n", devueltas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int devueltas = 0;
                      for (int turno = 1; turno <= 3; turno++) {
                          int *carga = malloc(sizeof *carga);
                          if (carga == NULL) {
                              return 1;
                          }
                          *carga = turno * 50;
                          printf("turno %d: %d kg\\n", turno, *carga);
                          free(carga);
                          devueltas++;
                      }
                      printf("vagonetas devueltas: %d\\n", devueltas);
                      return 0;
                  }
              ''',
              al_superar="Tres de tres. Hulda borra a Kira de la lista de deudores. Kira jura no volver a contar ese chiste nunca más. Toda la mina lo repite igual.",
              imagen=[KIRA + " cuenta un chiste, colorada, frente a una fila de mineros que no se ríen.", HULDA + " con los brazos cruzados.", "Un troll chiquito se escabulle con una vagoneta."]),
            m(id="R03-N01-P4", titulo="El texto a medida",
              lugar=MINAS, personajes="Kira, Gheco, Chispa",
              carta="Copia dinámica | malloc(strlen(s) + 1) · el +1 es para el '\\0' · strcpy copia y free libera",
              recompensa="xp 15, oro 15",
              escena="Chispa quiere guardar el nombre de cada cliente en una vagoneta del tamaño **justo**, ni una letra de más («la vagoneta se cobra por letra»).",
              sugiere="Para copiar un texto en memoria dinámica: `char *copia = malloc(strlen(s) + 1);` (el `+1` es el `'\\0'`) y `strcpy(copia, s);`.",
              desafio="Completá el tamaño justo.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  char *copiar(const char *s)
                  {
                      char *copia = malloc(___);
                      if (copia != NULL) {
                          strcpy(copia, s);
                      }
                      return copia;
                  }

                  int main(void)
                  {
                      char *cliente = copiar("Hulda");
                      if (cliente == NULL) {
                          return 1;
                      }
                      printf("%s ocupa %zu bytes\\n", cliente, strlen(cliente) + 1);
                      free(cliente);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  char *copiar(const char *s)
                  {
                      char *copia = malloc(strlen(s) + 1);
                      if (copia != NULL) {
                          strcpy(copia, s);
                      }
                      return copia;
                  }

                  int main(void)
                  {
                      char *cliente = copiar("Hulda");
                      if (cliente == NULL) {
                          return 1;
                      }
                      printf("%s ocupa %zu bytes\\n", cliente, strlen(cliente) + 1);
                      free(cliente);
                      return 0;
                  }
              ''',
              al_superar="Seis bytes justos. Chispa le cobra a Hulda seis lingotes «por la vagoneta». Hulda le cobra un chiste. Chispa paga los seis lingotes.",
              imagen=["Una vagoneta chiquita con un nombre grabado letra por letra.", CHISPA + " le extiende la mano a " + HULDA + ", que lo mira sin pestañear."]),
        ],
    },
    {
        "titulo": "R03-N02 · Un array que crece",
        "misiones": [
            m(id="R03-N02-P1", titulo="Cavar del doble",
              lugar=MINAS, personajes="Kira, Gheco, Tizón",
              carta="realloc | realloc(p, nuevo_tamaño) agranda y muda los datos · guardar en un auxiliar por si da NULL · duplicar la capacidad",
              recompensa="xp 10, oro 10",
              escena="La galería donde Hulda anota a los enemigos se llena todo el tiempo. Tizón hace cuentas diez minutos y anuncia: —Conviene cavar una **del doble** cada vez. —Por una vez, nadie le discute.",
              sugiere="`int *nuevo = realloc(v, nueva_cap * sizeof *v);` pide un lugar más grande y muda los datos. Si da `NULL`, el viejo sigue sano: por eso se guarda primero en `nuevo`.",
              desafio="Completá la nueva capacidad (el doble) y el `realloc`.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int cap = 2, n = 0;
                      int *v = malloc(cap * sizeof *v);
                      if (v == NULL) {
                          return 1;
                      }
                      for (int enemigo = 1; enemigo <= 5; enemigo++) {
                          if (n == cap) {
                              int nueva_cap = ___;
                              int *nuevo = ___;
                              if (nuevo == NULL) {
                                  free(v);
                                  return 1;
                              }
                              v = nuevo;
                              cap = nueva_cap;
                              printf("galeria agrandada a %d\\n", cap);
                          }
                          v[n++] = enemigo * 10;
                      }
                      printf("%d enemigos, capacidad %d\\n", n, cap);
                      free(v);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int cap = 2, n = 0;
                      int *v = malloc(cap * sizeof *v);
                      if (v == NULL) {
                          return 1;
                      }
                      for (int enemigo = 1; enemigo <= 5; enemigo++) {
                          if (n == cap) {
                              int nueva_cap = cap * 2;
                              int *nuevo = realloc(v, nueva_cap * sizeof *v);
                              if (nuevo == NULL) {
                                  free(v);
                                  return 1;
                              }
                              v = nuevo;
                              cap = nueva_cap;
                              printf("galeria agrandada a %d\\n", cap);
                          }
                          v[n++] = enemigo * 10;
                      }
                      printf("%d enemigos, capacidad %d\\n", n, cap);
                      free(v);
                      return 0;
                  }
              ''',
              al_superar="De 2 a 4 y de 4 a 8: dos mudanzas en lugar de cuatro. Hulda le da a Tizón una palmada que lo deja sin aire.",
              imagen=["Una galería de mina que se ensancha al doble, con mineros mudando cajas.", HULDA + " le da una palmada en la espalda a " + TIZON + "."]),
            m(id="R03-N02-P2", titulo="La lista de la galería",
              lugar=MINAS, personajes="Kira, Gheco, Hulda",
              carta="Agregar al final | si está lleno, agrandar · después v[n++] = valor · la función recibe punteros a v, n y cap",
              recompensa="xp 10, oro 10",
              escena="Hulda quiere una función `agregar` que haga todo sola: si hay lugar, guarda; si no, agranda y guarda. Las cargas llegan hasta un 0.",
              sugiere="`agregar(&v, &n, &cap, valor)` recibe las **direcciones** porque las cambia. Adentro, `*n`, `*cap` y `*v` son las variables de afuera.",
              desafio="Completá la línea que guarda el valor.",
              entrada="30 15 40 22 8 0\n",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int agregar(int **v, int *n, int *cap, int valor)
                  {
                      if (*n == *cap) {
                          int nueva = *cap * 2;
                          int *nuevo = realloc(*v, nueva * sizeof **v);
                          if (nuevo == NULL) {
                              return 0;
                          }
                          *v = nuevo;
                          *cap = nueva;
                      }
                      ___;
                      return 1;
                  }

                  int main(void)
                  {
                      int cap = 2, n = 0;
                      int *v = malloc(cap * sizeof *v);
                      int valor;
                      if (v == NULL) {
                          return 1;
                      }
                      while (scanf("%d", &valor) == 1 && valor != 0) {
                          agregar(&v, &n, &cap, valor);
                      }
                      printf("%d cargas (capacidad %d):", n, cap);
                      for (int i = 0; i < n; i++) {
                          printf(" %d", v[i]);
                      }
                      printf("\\n");
                      free(v);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int agregar(int **v, int *n, int *cap, int valor)
                  {
                      if (*n == *cap) {
                          int nueva = *cap * 2;
                          int *nuevo = realloc(*v, nueva * sizeof **v);
                          if (nuevo == NULL) {
                              return 0;
                          }
                          *v = nuevo;
                          *cap = nueva;
                      }
                      (*v)[*n] = valor;
                      (*n)++;
                      return 1;
                  }

                  int main(void)
                  {
                      int cap = 2, n = 0;
                      int *v = malloc(cap * sizeof *v);
                      int valor;
                      if (v == NULL) {
                          return 1;
                      }
                      while (scanf("%d", &valor) == 1 && valor != 0) {
                          agregar(&v, &n, &cap, valor);
                      }
                      printf("%d cargas (capacidad %d):", n, cap);
                      for (int i = 0; i < n; i++) {
                          printf(" %d", v[i]);
                      }
                      printf("\\n");
                      free(v);
                      return 0;
                  }
              ''',
              al_superar="Cinco cargas en una galería de ocho. Hulda guarda la función en su tablilla, «para la próxima temporada».",
              imagen=["Una tablilla de minera con una lista de cargas que se alarga sola.", HULDA + " la mira satisfecha."]),
            m(id="R03-N02-P3", titulo="Achicar al terminar",
              lugar=MINAS, personajes="Kira, Gheco, Tizón",
              carta="Achicar | realloc también achica · al terminar de cargar, dejar la capacidad justa · no se pierde ningún dato",
              recompensa="xp 10, oro 10",
              escena="Terminó el turno: la galería tiene lugar para 8 y hay 5 cargas. Tizón quiere devolver los 3 lugares que sobran, «para que el troll no se los coma».",
              sugiere="`realloc(v, n * sizeof *v)` con `n` menor que la capacidad **achica** el bloque y conserva los primeros `n` datos.",
              desafio="Achicá el bloque a la cantidad justa.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int cap = 8, n = 5;
                      int *v = malloc(cap * sizeof *v);
                      if (v == NULL) {
                          return 1;
                      }
                      for (int i = 0; i < n; i++) {
                          v[i] = (i + 1) * 7;
                      }
                      int *justo = ___;
                      if (justo != NULL) {
                          v = justo;
                          cap = n;
                      }
                      printf("capacidad %d, ultimo dato %d\\n", cap, v[n - 1]);
                      free(v);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int main(void)
                  {
                      int cap = 8, n = 5;
                      int *v = malloc(cap * sizeof *v);
                      if (v == NULL) {
                          return 1;
                      }
                      for (int i = 0; i < n; i++) {
                          v[i] = (i + 1) * 7;
                      }
                      int *justo = realloc(v, n * sizeof *v);
                      if (justo != NULL) {
                          v = justo;
                          cap = n;
                      }
                      printf("capacidad %d, ultimo dato %d\\n", cap, v[n - 1]);
                      free(v);
                      return 0;
                  }
              ''',
              al_superar="Capacidad 5, ni un lugar vacío. Tizón tapa los tres huecos de la galería con piedras y los mide, por las dudas.",
              imagen=["Una galería que se achica, con piedras tapando el final.", TIZON + " coloca la última piedra."]),
            m(id="R03-N02-P4", titulo="Los enemigos con nombre",
              lugar=MINAS, personajes="Kira, Gheco, Hulda",
              carta="Array dinámico de structs | Enemigo *v = malloc(cap * sizeof *v) · v[i].vida · se agranda igual que uno de int",
              recompensa="xp 15, oro 15",
              escena="Hulda no quiere solo números: quiere cada enemigo con su nombre y su vida, y que la lista crezca sola. Llegan de a uno por línea hasta «fin».",
              sugiere="Un array dinámico de structs funciona igual: `realloc` con `sizeof *v`, que ahora es el tamaño de un `Enemigo`.",
              desafio="Completá el `realloc` del array de structs.",
              entrada="goblin 12\norco 30\nslime 5\nfin\n",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                  } Enemigo;

                  int main(void)
                  {
                      int cap = 1, n = 0;
                      Enemigo *v = malloc(cap * sizeof *v);
                      char nombre[12];
                      int vida;
                      if (v == NULL) {
                          return 1;
                      }
                      while (scanf("%11s", nombre) == 1 && strcmp(nombre, "fin") != 0 && scanf("%d", &vida) == 1) {
                          if (n == cap) {
                              Enemigo *nuevo = ___;
                              if (nuevo == NULL) {
                                  free(v);
                                  return 1;
                              }
                              v = nuevo;
                              cap *= 2;
                          }
                          strcpy(v[n].nombre, nombre);
                          v[n].vida = vida;
                          n++;
                      }
                      for (int i = 0; i < n; i++) {
                          printf("%-7s %3d\\n", v[i].nombre, v[i].vida);
                      }
                      printf("capacidad final: %d\\n", cap);
                      free(v);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                  } Enemigo;

                  int main(void)
                  {
                      int cap = 1, n = 0;
                      Enemigo *v = malloc(cap * sizeof *v);
                      char nombre[12];
                      int vida;
                      if (v == NULL) {
                          return 1;
                      }
                      while (scanf("%11s", nombre) == 1 && strcmp(nombre, "fin") != 0 && scanf("%d", &vida) == 1) {
                          if (n == cap) {
                              Enemigo *nuevo = realloc(v, cap * 2 * sizeof *v);
                              if (nuevo == NULL) {
                                  free(v);
                                  return 1;
                              }
                              v = nuevo;
                              cap *= 2;
                          }
                          strcpy(v[n].nombre, nombre);
                          v[n].vida = vida;
                          n++;
                      }
                      for (int i = 0; i < n; i++) {
                          printf("%-7s %3d\\n", v[i].nombre, v[i].vida);
                      }
                      printf("capacidad final: %d\\n", cap);
                      free(v);
                      return 0;
                  }
              ''',
              al_superar="Tres enemigos con nombre y vida. Hulda los clava en el tablero de la mina. El slime, ofendido por su vida de 5, se va a llorar a un rincón.",
              imagen=["Un tablero de la mina con fichas de enemigos: goblin, orco, slime.", HULDA + " clava la última ficha con el pico.", "Un slime llorando en un rincón."]),
        ],
    },
    {
        "titulo": "R03-N03 · Lista enlazada",
        "misiones": [
            m(id="R03-N03-P1", titulo="Enganchar adelante",
              lugar="Las vías de la mina", personajes="Kira, Gheco, Hulda",
              carta="Insertar al frente | el nuevo apunta a la cabeza · el nuevo pasa a ser la cabeza · la función devuelve la cabeza nueva",
              recompensa="xp 10, oro 10",
              escena="Más abajo, los vagones van enganchados con cadenas. Para agregar uno no hay que mudar nada: se engancha adelante y listo. Hulda le muestra a Kira el primer enganche.",
              sugiere="Insertar al frente: `n->siguiente = cabeza;` y la cabeza pasa a ser `n`. La función devuelve la cabeza nueva: `cabeza = insertar(cabeza, …);`.",
              desafio="Completá el enganche.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Vagon {
                      int carga;
                      struct Vagon *siguiente;
                  } Vagon;

                  Vagon *insertar(Vagon *cabeza, int carga)
                  {
                      Vagon *n = malloc(sizeof *n);
                      if (n == NULL) {
                          exit(1);
                      }
                      n->carga = carga;
                      n->siguiente = ___;
                      return ___;
                  }

                  int main(void)
                  {
                      Vagon *tren = NULL;
                      tren = insertar(tren, 300);
                      tren = insertar(tren, 120);
                      tren = insertar(tren, 450);
                      for (Vagon *p = tren; p != NULL; p = p->siguiente) {
                          printf("[%d]", p->carga);
                      }
                      printf("\\n");
                      while (tren != NULL) {
                          Vagon *sig = tren->siguiente;
                          free(tren);
                          tren = sig;
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Vagon {
                      int carga;
                      struct Vagon *siguiente;
                  } Vagon;

                  Vagon *insertar(Vagon *cabeza, int carga)
                  {
                      Vagon *n = malloc(sizeof *n);
                      if (n == NULL) {
                          exit(1);
                      }
                      n->carga = carga;
                      n->siguiente = cabeza;
                      return n;
                  }

                  int main(void)
                  {
                      Vagon *tren = NULL;
                      tren = insertar(tren, 300);
                      tren = insertar(tren, 120);
                      tren = insertar(tren, 450);
                      for (Vagon *p = tren; p != NULL; p = p->siguiente) {
                          printf("[%d]", p->carga);
                      }
                      printf("\\n");
                      while (tren != NULL) {
                          Vagon *sig = tren->siguiente;
                          free(tren);
                          tren = sig;
                      }
                      return 0;
                  }
              ''',
              al_superar="Tres vagones enganchados, el último que llegó adelante. El tren sale marcha atrás. Hulda dice que para eso está la próxima lección.",
              imagen=["Un tren de mina de tres vagones unidos por cadenas que brillan.", HULDA + " ajusta un enganche."]),
            m(id="R03-N03-P2", titulo="Engancharlos ordenados",
              lugar="Las vías de la mina", personajes="Kira, Gheco, Hulda",
              carta="Inserción ordenada | si va primero, se engancha adelante · si no, avanzar mientras el siguiente sea menor · enganchar entre p y su siguiente",
              recompensa="xp 15, oro 15",
              escena="Kira enganchó los vagones en cualquier orden y el tren salió con el más pesado adelante. Hulda le explica, con mucha calma y bastante volumen, que se enganchan **ordenados por peso**.",
              sugiere="Si la lista está vacía o el nuevo es menor que la cabeza, va primero. Si no, se avanza con `p` mientras `p->siguiente` exista y sea menor, y se engancha entre `p` y su siguiente.",
              desafio="Completá la condición del avance y el enganche del medio.",
              entrada="300 120 450 200 80\n",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Vagon {
                      int carga;
                      struct Vagon *siguiente;
                  } Vagon;

                  Vagon *insertar_ordenado(Vagon *cabeza, Vagon *n)
                  {
                      if (cabeza == NULL || n->carga <= cabeza->carga) {
                          n->siguiente = cabeza;
                          return n;
                      }
                      Vagon *p = cabeza;
                      while (___) {
                          p = p->siguiente;
                      }
                      n->siguiente = ___;
                      p->siguiente = ___;
                      return cabeza;
                  }

                  int main(void)
                  {
                      Vagon *tren = NULL;
                      int carga;
                      while (scanf("%d", &carga) == 1) {
                          Vagon *n = malloc(sizeof *n);
                          if (n == NULL) {
                              return 1;
                          }
                          n->carga = carga;
                          tren = insertar_ordenado(tren, n);
                      }
                      for (Vagon *p = tren; p != NULL; p = p->siguiente) {
                          printf("[%d]", p->carga);
                      }
                      printf("\\n");
                      while (tren != NULL) {
                          Vagon *sig = tren->siguiente;
                          free(tren);
                          tren = sig;
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Vagon {
                      int carga;
                      struct Vagon *siguiente;
                  } Vagon;

                  Vagon *insertar_ordenado(Vagon *cabeza, Vagon *n)
                  {
                      if (cabeza == NULL || n->carga <= cabeza->carga) {
                          n->siguiente = cabeza;
                          return n;
                      }
                      Vagon *p = cabeza;
                      while (p->siguiente != NULL && p->siguiente->carga < n->carga) {
                          p = p->siguiente;
                      }
                      n->siguiente = p->siguiente;
                      p->siguiente = n;
                      return cabeza;
                  }

                  int main(void)
                  {
                      Vagon *tren = NULL;
                      int carga;
                      while (scanf("%d", &carga) == 1) {
                          Vagon *n = malloc(sizeof *n);
                          if (n == NULL) {
                              return 1;
                          }
                          n->carga = carga;
                          tren = insertar_ordenado(tren, n);
                      }
                      for (Vagon *p = tren; p != NULL; p = p->siguiente) {
                          printf("[%d]", p->carga);
                      }
                      printf("\\n");
                      while (tren != NULL) {
                          Vagon *sig = tren->siguiente;
                          free(tren);
                          tren = sig;
                      }
                      return 0;
                  }
              ''',
              al_superar="Del más liviano al más pesado. El tren sale derecho, sin chirriar. Hulda baja el volumen.",
              imagen=["Un tren de mina ordenado de vagones chicos a grandes.", HULDA + " asiente con los brazos cruzados.", KIRA + " suelta el último enganche."]),
            m(id="R03-N03-P3", titulo="Soltar sin perder",
              lugar="Las vías de la mina", personajes="Kira, Gheco, Tizón",
              criatura="troll",
              carta="Quitar un nodo | buscar el ANTERIOR · anterior->siguiente = a_quitar->siguiente · después free · si es la cabeza, la cabeza cambia",
              recompensa="xp 15, oro 15",
              escena="Hay que desenganchar el vagón de 200 kg del medio del tren sin perder los de atrás. —Si soltás la cadena antes de agarrar la siguiente —advierte Tizón—, todo lo de atrás se pierde en la oscuridad.",
              sugiere="Para quitar, se busca el nodo **anterior** al que sale y se lo une con el que sigue: `ant->siguiente = sale->siguiente;` y recién ahí `free(sale)`.",
              desafio="Completá la unión y la liberación.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Vagon {
                      int carga;
                      struct Vagon *siguiente;
                  } Vagon;

                  Vagon *agregar_al_frente(Vagon *cabeza, int carga)
                  {
                      Vagon *n = malloc(sizeof *n);
                      if (n == NULL) {
                          exit(1);
                      }
                      n->carga = carga;
                      n->siguiente = cabeza;
                      return n;
                  }

                  Vagon *quitar(Vagon *cabeza, int carga)
                  {
                      if (cabeza != NULL && cabeza->carga == carga) {
                          Vagon *resto = cabeza->siguiente;
                          free(cabeza);
                          return resto;
                      }
                      for (Vagon *ant = cabeza; ant != NULL && ant->siguiente != NULL; ant = ant->siguiente) {
                          if (ant->siguiente->carga == carga) {
                              Vagon *sale = ant->siguiente;
                              ___;
                              ___;
                              break;
                          }
                      }
                      return cabeza;
                  }

                  int main(void)
                  {
                      Vagon *tren = NULL;
                      tren = agregar_al_frente(tren, 450);
                      tren = agregar_al_frente(tren, 200);
                      tren = agregar_al_frente(tren, 120);
                      tren = quitar(tren, 200);
                      for (Vagon *p = tren; p != NULL; p = p->siguiente) {
                          printf("[%d]", p->carga);
                      }
                      printf("\\n");
                      while (tren != NULL) {
                          Vagon *sig = tren->siguiente;
                          free(tren);
                          tren = sig;
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Vagon {
                      int carga;
                      struct Vagon *siguiente;
                  } Vagon;

                  Vagon *agregar_al_frente(Vagon *cabeza, int carga)
                  {
                      Vagon *n = malloc(sizeof *n);
                      if (n == NULL) {
                          exit(1);
                      }
                      n->carga = carga;
                      n->siguiente = cabeza;
                      return n;
                  }

                  Vagon *quitar(Vagon *cabeza, int carga)
                  {
                      if (cabeza != NULL && cabeza->carga == carga) {
                          Vagon *resto = cabeza->siguiente;
                          free(cabeza);
                          return resto;
                      }
                      for (Vagon *ant = cabeza; ant != NULL && ant->siguiente != NULL; ant = ant->siguiente) {
                          if (ant->siguiente->carga == carga) {
                              Vagon *sale = ant->siguiente;
                              ant->siguiente = sale->siguiente;
                              free(sale);
                              break;
                          }
                      }
                      return cabeza;
                  }

                  int main(void)
                  {
                      Vagon *tren = NULL;
                      tren = agregar_al_frente(tren, 450);
                      tren = agregar_al_frente(tren, 200);
                      tren = agregar_al_frente(tren, 120);
                      tren = quitar(tren, 200);
                      for (Vagon *p = tren; p != NULL; p = p->siguiente) {
                          printf("[%d]", p->carga);
                      }
                      printf("\\n");
                      while (tren != NULL) {
                          Vagon *sig = tren->siguiente;
                          free(tren);
                          tren = sig;
                      }
                      return 0;
                  }
              ''',
              al_superar="El vagón del medio sale y el tren sigue entero. Tizón respira de nuevo: había contenido el aire todo el tiempo.",
              imagen=["Un vagón que se desengancha del medio de un tren mientras los otros dos se unen.", TIZON + " aguanta la respiración con las mejillas infladas."]),
            m(id="R03-N03-P4", titulo="La veta del plomo",
              lugar="La vía muerta", personajes="Kira, Gheco, Hulda",
              carta="Recorrer de vuelta | una función recursiva que se llama con el siguiente · si muestra DESPUÉS de llamarse, la lista sale al revés",
              recompensa="xp 15, oro 15",
              escena="Al final de una vía muerta hay un tren viejo, abandonado. Hulda quiere leer sus vagones **desde el último**, que es el más cercano a la pared de roca.",
              sugiere="`al_reves(p)`: si `p` es `NULL`, termina; si no, se llama con `p->siguiente` y **después** muestra `p`. Así se muestra a la vuelta, del último al primero.",
              desafio="Completá la llamada recursiva.",
              inicial='''
                  #include <stdio.h>

                  typedef struct Vagon {
                      const char *contenido;
                      struct Vagon *siguiente;
                  } Vagon;

                  void al_reves(const Vagon *p)
                  {
                      if (p == NULL) {
                          return;
                      }
                      ___;
                      printf("%s\\n", p->contenido);
                  }

                  int main(void)
                  {
                      Vagon c = { "plomo con un vitral grabado", NULL };
                      Vagon b = { "carbon", &c };
                      Vagon a = { "piedras", &b };
                      al_reves(&a);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct Vagon {
                      const char *contenido;
                      struct Vagon *siguiente;
                  } Vagon;

                  void al_reves(const Vagon *p)
                  {
                      if (p == NULL) {
                          return;
                      }
                      al_reves(p->siguiente);
                      printf("%s\\n", p->contenido);
                  }

                  int main(void)
                  {
                      Vagon c = { "plomo con un vitral grabado", NULL };
                      Vagon b = { "carbon", &c };
                      Vagon a = { "piedras", &b };
                      al_reves(&a);
                      return 0;
                  }
              ''',
              al_superar="El último vagón está lleno de **plomo**, gris y brillante, y en la roca de atrás alguien grabó un vitral chiquito. El plomo del pedido salió de acá. Hulda se saca el casco, despacio.",
              imagen=["Una vía muerta que termina en una pared de roca con una veta de plomo brillante y un vitral chiquito grabado.",
                      HULDA + " se saca el casco, sorprendida.", KIRA + " ilumina la veta con el farol."]),
        ],
    },
    {
        "titulo": "R03-N04 · Pilas y colas",
        "misiones": [
            m(id="R03-N04-P1", titulo="El almuerzo de Tizón",
              lugar="El montacargas", personajes="Kira, Gheco, Tizón, Hulda",
              carta="Pila | apilar arriba, desapilar de arriba · el último que entra es el primero que sale · con array: datos y cantidad",
              recompensa="xp 10, oro 10",
              escena="""
                  En el montacargas, las bolsas se apilan una encima de otra. Tizón subió su almuerzo **primero**, abajo de todo. Hulda descarga desde arriba, sin una gota de compasión.
              """,
              sugiere="Una pila con array: `apilar` guarda en `datos[cantidad++]` y `desapilar` saca `datos[--cantidad]`. Sale primero lo último que entró.",
              desafio="Completá apilar y desapilar.",
              inicial='''
                  #include <stdio.h>

                  #define MAX 5

                  typedef struct {
                      int datos[MAX];
                      int cantidad;
                  } Pila;

                  void apilar(Pila *p, int x)
                  {
                      if (p->cantidad < MAX) {
                          ___;
                      }
                  }

                  int desapilar(Pila *p)
                  {
                      return ___;
                  }

                  int main(void)
                  {
                      Pila montacargas = { .cantidad = 0 };
                      apilar(&montacargas, 1);
                      apilar(&montacargas, 2);
                      apilar(&montacargas, 3);
                      printf("baja la bolsa %d\\n", desapilar(&montacargas));
                      printf("baja la bolsa %d\\n", desapilar(&montacargas));
                      printf("baja la bolsa %d (el almuerzo de Tizon)\\n", desapilar(&montacargas));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define MAX 5

                  typedef struct {
                      int datos[MAX];
                      int cantidad;
                  } Pila;

                  void apilar(Pila *p, int x)
                  {
                      if (p->cantidad < MAX) {
                          p->datos[p->cantidad++] = x;
                      }
                  }

                  int desapilar(Pila *p)
                  {
                      return p->datos[--p->cantidad];
                  }

                  int main(void)
                  {
                      Pila montacargas = { .cantidad = 0 };
                      apilar(&montacargas, 1);
                      apilar(&montacargas, 2);
                      apilar(&montacargas, 3);
                      printf("baja la bolsa %d\\n", desapilar(&montacargas));
                      printf("baja la bolsa %d\\n", desapilar(&montacargas));
                      printf("baja la bolsa %d (el almuerzo de Tizon)\\n", desapilar(&montacargas));
                      return 0;
                  }
              ''',
              al_superar="El almuerzo de Tizón baja último, frío. —Es una pila —le dice Hulda—. Último en entrar, primero en salir. —Tizón come en silencio, apuntando algo en la libreta.",
              imagen=["Un montacargas de mina con bolsas apiladas.", TIZON + " mira su almuerzo frío.", HULDA + " descarga una bolsa."]),
            m(id="R03-N04-P2", titulo="Al fondo, mercader",
              lugar="La fila de vagonetas", personajes="Kira, Gheco, Chispa, Hulda",
              carta="Cola | se encola al fondo, se desencola del frente · el primero que llega es el primero que sale · con nodos: punteros al frente y al fondo",
              recompensa="xp 10, oro 10",
              escena="Chispa intenta meter su vagoneta adelante de todas, sonriendo con el diente de oro. Hulda ni lo mira: —Es una **cola**, mercader. Al fondo.",
              sugiere="Al encolar con nodos: si la cola está vacía, el nuevo es el frente; si no, se engancha detrás del fondo (`fondo->siguiente = n`). En los dos casos, el nuevo pasa a ser el fondo.",
              desafio="Completá el enganche al fondo.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Nodo {
                      const char *duenio;
                      struct Nodo *siguiente;
                  } Nodo;

                  typedef struct {
                      Nodo *frente;
                      Nodo *fondo;
                  } Cola;

                  void encolar(Cola *c, Nodo *n)
                  {
                      n->siguiente = NULL;
                      if (c->fondo == NULL) {
                          c->frente = n;
                      } else {
                          ___;
                      }
                      ___;
                  }

                  int main(void)
                  {
                      Nodo a = { "Kira", NULL }, b = { "Tizon", NULL }, d = { "Chispa", NULL };
                      Cola fila = { NULL, NULL };
                      encolar(&fila, &a);
                      encolar(&fila, &b);
                      encolar(&fila, &d);
                      for (Nodo *p = fila.frente; p != NULL; p = p->siguiente) {
                          printf("sale %s\\n", p->duenio);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Nodo {
                      const char *duenio;
                      struct Nodo *siguiente;
                  } Nodo;

                  typedef struct {
                      Nodo *frente;
                      Nodo *fondo;
                  } Cola;

                  void encolar(Cola *c, Nodo *n)
                  {
                      n->siguiente = NULL;
                      if (c->fondo == NULL) {
                          c->frente = n;
                      } else {
                          c->fondo->siguiente = n;
                      }
                      c->fondo = n;
                  }

                  int main(void)
                  {
                      Nodo a = { "Kira", NULL }, b = { "Tizon", NULL }, d = { "Chispa", NULL };
                      Cola fila = { NULL, NULL };
                      encolar(&fila, &a);
                      encolar(&fila, &b);
                      encolar(&fila, &d);
                      for (Nodo *p = fila.frente; p != NULL; p = p->siguiente) {
                          printf("sale %s\\n", p->duenio);
                      }
                      return 0;
                  }
              ''',
              al_superar="Kira, Tizón y, al final, Chispa. Kira, que siempre quiere pasar primero, se puso al fondo sin que nadie se lo dijera. Ferrum, desde lejos, golpea el yunque dos veces.",
              imagen=["Una fila de vagonetas en la boca de la mina.", CHISPA + " empuja su vagoneta al final de la fila, resignado.", HULDA + " con el pico al hombro."]),
            m(id="R03-N04-P3", titulo="Las llaves que cierran",
              lugar="El Archivo de planos", personajes="Kira, Gheco, Chispa",
              carta="Pila de char | cada apertura se apila · cada cierre tiene que coincidir con el tope · al final, la pila vacía",
              recompensa="xp 15, oro 15",
              escena="El Archivero desconfía de los planos de Chispa: dice que nunca cierra lo que abre. Kira revisa cada plano con una pila.",
              sugiere="Con una pila de `char`: `(` y `[` se apilan; `)` exige que el tope sea `(` y `]` que sea `[`. Si no coincide o al final queda algo, no cierra.",
              desafio="Completá el carácter de apertura que espera cada cierre.",
              entrada="([()])\n([)]\n((\n",
              inicial='''
                  #include <stdio.h>
                  #include <string.h>

                  int cierra(const char *s)
                  {
                      char pila[50];
                      int n = 0;
                      for (int i = 0; s[i] != '\\0'; i++) {
                          if (s[i] == '(' || s[i] == '[') {
                              pila[n++] = s[i];
                          } else if (s[i] == ')' || s[i] == ']') {
                              char espera = s[i] == ')' ? ___ : ___;
                              if (n == 0 || pila[n - 1] != espera) {
                                  return 0;
                              }
                              n--;
                          }
                      }
                      return n == 0;
                  }

                  int main(void)
                  {
                      char linea[50];
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          linea[strcspn(linea, "\\n")] = '\\0';
                          printf("%-8s %s\\n", linea, cierra(linea) ? "cierra" : "no cierra");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <string.h>

                  int cierra(const char *s)
                  {
                      char pila[50];
                      int n = 0;
                      for (int i = 0; s[i] != '\\0'; i++) {
                          if (s[i] == '(' || s[i] == '[') {
                              pila[n++] = s[i];
                          } else if (s[i] == ')' || s[i] == ']') {
                              char espera = s[i] == ')' ? '(' : '[';
                              if (n == 0 || pila[n - 1] != espera) {
                                  return 0;
                              }
                              n--;
                          }
                      }
                      return n == 0;
                  }

                  int main(void)
                  {
                      char linea[50];
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          linea[strcspn(linea, "\\n")] = '\\0';
                          printf("%-8s %s\\n", linea, cierra(linea) ? "cierra" : "no cierra");
                      }
                      return 0;
                  }
              ''',
              al_superar="Uno cierra, dos no. El Archivero devuelve los dos planos de Chispa con una nota: «Cierre lo que abre». Chispa guarda la nota en un bolsillo y se olvida para siempre.",
              imagen=["Tres planos con paréntesis y corchetes; dos tienen marcas rojas.", CHISPA + " recibe los planos devueltos con una nota."]),
            m(id="R03-N04-P4", titulo="La cola que da la vuelta",
              lugar="El horno grande", personajes="Kira, Gheco, Tizón",
              carta="Cola circular | posición = (frente + cantidad) % MAX · al sacar, frente = (frente + 1) % MAX · se aprovechan los lugares que se liberan",
              recompensa="xp 15, oro 15",
              escena="El horno grande tiene lugar para 3 piezas esperando, en un riel que da la vuelta. Tizón no entiende cómo la pieza nueva va a parar al lugar 0 si ya pasó por ahí.",
              sugiere="En una cola circular con array, el próximo lugar es `(frente + cantidad) % MAX`: al pasarse del final, el `%` lo vuelve al principio.",
              desafio="Completá la posición donde entra cada pieza.",
              inicial='''
                  #include <stdio.h>

                  #define MAX 3

                  int main(void)
                  {
                      int riel[MAX];
                      int frente = 0, cantidad = 0;
                      int piezas[5] = { 10, 11, 12, 13, 14 };
                      for (int i = 0; i < 5; i++) {
                          if (cantidad == MAX) {
                              printf("sale la pieza %d del lugar %d\\n", riel[frente], frente);
                              frente = (frente + 1) % MAX;
                              cantidad--;
                          }
                          int pos = ___;
                          riel[pos] = piezas[i];
                          cantidad++;
                          printf("entra la pieza %d en el lugar %d\\n", piezas[i], pos);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define MAX 3

                  int main(void)
                  {
                      int riel[MAX];
                      int frente = 0, cantidad = 0;
                      int piezas[5] = { 10, 11, 12, 13, 14 };
                      for (int i = 0; i < 5; i++) {
                          if (cantidad == MAX) {
                              printf("sale la pieza %d del lugar %d\\n", riel[frente], frente);
                              frente = (frente + 1) % MAX;
                              cantidad--;
                          }
                          int pos = (frente + cantidad) % MAX;
                          riel[pos] = piezas[i];
                          cantidad++;
                          printf("entra la pieza %d en el lugar %d\\n", piezas[i], pos);
                      }
                      return 0;
                  }
              ''',
              al_superar="Las piezas 13 y 14 vuelven a los lugares 0 y 1. Tizón dibuja el riel en la libreta como un reloj y por fin lo entiende. Lo dibuja diez veces más, por gusto.",
              imagen=["Un riel circular frente a un horno, con tres lugares numerados 0, 1 y 2.", TIZON + " dibuja un reloj en la libreta."]),
        ],
    },
    {
        "titulo": "R03-N05 · Punteros a función",
        "misiones": [
            m(id="R03-N05-P1", titulo="La palanca que señala",
              lugar="El tablero de palancas", personajes="Kira, Gheco, Hulda",
              carta="Puntero a función | int (*accion)(int) = doble; · se llama accion(5) · cambia la función a la que apunta y cambia lo que hace",
              recompensa="xp 10, oro 10",
              escena="En el taller de las Minas hay un tablero de palancas. Cada palanca no hace nada sola: **señala** una máquina. Cambiando adónde señala, la misma palanca hace otra cosa.",
              sugiere="`int (*palanca)(int) = bomba;` guarda la función `bomba`. `palanca(10)` la llama. Después, `palanca = fuelle;` y la misma línea hace otra cosa.",
              desafio="Hacé que la palanca señale primero a `bomba` y después a `fuelle`.",
              inicial='''
                  #include <stdio.h>

                  int bomba(int litros)
                  {
                      return litros * 2;
                  }

                  int fuelle(int grados)
                  {
                      return grados + 100;
                  }

                  int main(void)
                  {
                      int (*palanca)(int) = ___;
                      printf("la palanca da %d\\n", palanca(10));
                      palanca = ___;
                      printf("la palanca da %d\\n", palanca(10));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int bomba(int litros)
                  {
                      return litros * 2;
                  }

                  int fuelle(int grados)
                  {
                      return grados + 100;
                  }

                  int main(void)
                  {
                      int (*palanca)(int) = bomba;
                      printf("la palanca da %d\\n", palanca(10));
                      palanca = fuelle;
                      printf("la palanca da %d\\n", palanca(10));
                      return 0;
                  }
              ''',
              al_superar="Veinte litros de agua, y después ciento diez grados. Hulda deja la palanca en «bomba»: la mina se estaba inundando un poquito.",
              imagen=["Un tablero de palancas de hierro, cada una unida por un cable a una máquina distinta.", HULDA + " mueve una palanca."]),
            m(id="R03-N05-P2", titulo="La palanca de Chispa",
              lugar="El tablero de palancas", personajes="Kira, Gheco, Chispa, Tizón",
              carta="Tabla de funciones | un array de punteros a función · la opción elige el índice · menos if, más orden",
              recompensa="xp 15, oro 15",
              escena="Chispa instaló una palanca nueva que manda **todos** los trenes a su puesto de ventas. Tizón la encontró en cinco minutos: estaba etiquetada «NO TOCAR, NO ES DE CHISPA». Kira arma un tablero honesto.",
              sugiere="Un array de punteros a función: `Destino destinos[3] = { a_la_forja, a_la_mina, al_archivo };` y se llama `destinos[opcion](tren)`.",
              desafio="Completá la llamada con la tabla.",
              entrada="0 2 1\n",
              inicial='''
                  #include <stdio.h>

                  typedef void (*Destino)(int);

                  void a_la_forja(int tren) { printf("tren %d a la forja\\n", tren); }
                  void a_la_mina(int tren) { printf("tren %d a la mina\\n", tren); }
                  void al_archivo(int tren) { printf("tren %d al archivo\\n", tren); }

                  int main(void)
                  {
                      Destino destinos[3] = { a_la_forja, a_la_mina, al_archivo };
                      int opcion;
                      for (int tren = 1; tren <= 3; tren++) {
                          scanf("%d", &opcion);
                          ___;
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef void (*Destino)(int);

                  void a_la_forja(int tren) { printf("tren %d a la forja\\n", tren); }
                  void a_la_mina(int tren) { printf("tren %d a la mina\\n", tren); }
                  void al_archivo(int tren) { printf("tren %d al archivo\\n", tren); }

                  int main(void)
                  {
                      Destino destinos[3] = { a_la_forja, a_la_mina, al_archivo };
                      int opcion;
                      for (int tren = 1; tren <= 3; tren++) {
                          scanf("%d", &opcion);
                          destinos[opcion](tren);
                      }
                      return 0;
                  }
              ''',
              al_superar="Ningún tren al puesto de Chispa. Chispa propone agregar un cuarto destino, «el comercio local». Votan en contra todos, incluso el slime.",
              imagen=["Un tablero de palancas con tres destinos tallados: forja, mina, archivo.", CHISPA + " señala un cuarto lugar vacío en el tablero."]),
            m(id="R03-N05-P3", titulo="Contar los que cumplen",
              lugar="El tablero de palancas", personajes="Kira, Gheco, Tizón",
              carta="Funciones como parámetro | contar(v, n, criterio) · el criterio es una función que dice sí o no · la misma cuenta sirve para cualquier pregunta",
              recompensa="xp 15, oro 15",
              escena="Tizón escribe una función para contar las cargas pesadas, otra para las livianas, otra para las pares… Kira le muestra que con **una sola** alcanza, si se le pasa la pregunta.",
              sugiere="`int contar(const int v[], int n, int (*criterio)(int))` recorre y suma 1 cada vez que `criterio(v[i])` es verdadero. Se llama `contar(cargas, 6, es_pesada)`.",
              desafio="Completá la pregunta dentro de `contar`.",
              inicial='''
                  #include <stdio.h>

                  int es_pesada(int c) { return c > 200; }
                  int es_par(int c) { return c % 2 == 0; }

                  int contar(const int v[], int n, int (*criterio)(int))
                  {
                      int cuantas = 0;
                      for (int i = 0; i < n; i++) {
                          if (___) {
                              cuantas++;
                          }
                      }
                      return cuantas;
                  }

                  int main(void)
                  {
                      int cargas[6] = { 120, 350, 75, 210, 400, 90 };
                      printf("pesadas: %d\\n", contar(cargas, 6, es_pesada));
                      printf("pares: %d\\n", contar(cargas, 6, es_par));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int es_pesada(int c) { return c > 200; }
                  int es_par(int c) { return c % 2 == 0; }

                  int contar(const int v[], int n, int (*criterio)(int))
                  {
                      int cuantas = 0;
                      for (int i = 0; i < n; i++) {
                          if (criterio(v[i])) {
                              cuantas++;
                          }
                      }
                      return cuantas;
                  }

                  int main(void)
                  {
                      int cargas[6] = { 120, 350, 75, 210, 400, 90 };
                      printf("pesadas: %d\\n", contar(cargas, 6, es_pesada));
                      printf("pares: %d\\n", contar(cargas, 6, es_par));
                      return 0;
                  }
              ''',
              al_superar="Tres pesadas, cinco pares, una sola función. Tizón tacha cinco páginas de la libreta. Le duele, pero las tacha.",
              imagen=[TIZON + " tacha páginas enteras de la libreta, con lágrimas en los ojos.", KIRA + " le da una palmadita."]),
            m(id="R03-N05-P4", titulo="El ordenador que pide cómo",
              lugar="El tablero de palancas", personajes="Kira, Gheco, Maese Ferrum",
              carta="qsort de mayor a menor | la comparación decide el orden · b - a ordena de mayor a menor · el autómata no sabe: vos le explicás",
              recompensa="xp 15, oro 15",
              escena="El autómata de bronce que ordenaba el cuadro de honor funcionaba así: vos le dabas la palanca. Ferrum quiere las cargas de **mayor a menor**, para mandar primero las pesadas.",
              sugiere="`qsort` llama a tu comparación con dos punteros. Para ordenar de **mayor a menor**, se devuelve `*y - *x` (al revés que de menor a mayor).",
              desafio="Completá la comparación de mayor a menor.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int mayor_primero(const void *a, const void *b)
                  {
                      const int *x = a;
                      const int *y = b;
                      return ___;
                  }

                  int main(void)
                  {
                      int cargas[6] = { 120, 350, 75, 210, 400, 90 };
                      qsort(cargas, 6, sizeof cargas[0], mayor_primero);
                      for (int i = 0; i < 6; i++) {
                          printf(i == 0 ? "%d" : " %d", cargas[i]);
                      }
                      printf("\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int mayor_primero(const void *a, const void *b)
                  {
                      const int *x = a;
                      const int *y = b;
                      return *y - *x;
                  }

                  int main(void)
                  {
                      int cargas[6] = { 120, 350, 75, 210, 400, 90 };
                      qsort(cargas, 6, sizeof cargas[0], mayor_primero);
                      for (int i = 0; i < 6; i++) {
                          printf(i == 0 ? "%d" : " %d", cargas[i]);
                      }
                      printf("\\n");
                      return 0;
                  }
              ''',
              al_superar="Cuatrocientos primero. El autómata de bronce hace su reverencia. Ferrum le da una palmadita en la cabeza, cuando cree que nadie lo ve.",
              imagen=["Un autómata de bronce chiquito ordenando bolsas de mayor a menor.", FERRUM + " le da una palmadita en la cabeza."]),
        ],
    },
    {
        "titulo": "R03-N06 · Jefe: la Sanguijuela de las Minas",
        "misiones": [
            m(id="R03-N06-P1", titulo="La tablilla de las deudas",
              lugar="Lo más hondo de las Minas", personajes="Kira, Gheco, Hulda",
              criatura="dragon",
              carta="Contar lo pedido y lo devuelto | un contador sube en cada malloc y baja en cada free · al final tiene que dar 0",
              recompensa="xp 15, oro 15",
              escena="""
                  En lo más hondo, algo enorme y blando se arrastra entre los túneles: la **Sanguijuela**, gordísima. Hulda revisa la tablilla: casi todas las vagonetas que se comió son de Chispa.
                  Chispa silba mirando para otro lado.
              """,
              sugiere="Se envuelven `malloc` y `free` en funciones que cuentan: `pedir()` suma 1 y `devolver()` resta 1. Si al final queda algo, hay fuga.",
              desafio="Completá las dos cuentas.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  static int prestadas = 0;

                  int *pedir(void)
                  {
                      int *p = malloc(sizeof *p);
                      if (p != NULL) {
                          ___;
                      }
                      return p;
                  }

                  void devolver(int *p)
                  {
                      if (p != NULL) {
                          free(p);
                          ___;
                      }
                  }

                  int main(void)
                  {
                      int *a = pedir();
                      int *b = pedir();
                      int *c = pedir();
                      devolver(a);
                      devolver(c);
                      printf("sin devolver: %d\\n", prestadas);
                      devolver(b);
                      printf("sin devolver: %d\\n", prestadas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  static int prestadas = 0;

                  int *pedir(void)
                  {
                      int *p = malloc(sizeof *p);
                      if (p != NULL) {
                          prestadas++;
                      }
                      return p;
                  }

                  void devolver(int *p)
                  {
                      if (p != NULL) {
                          free(p);
                          prestadas--;
                      }
                  }

                  int main(void)
                  {
                      int *a = pedir();
                      int *b = pedir();
                      int *c = pedir();
                      devolver(a);
                      devolver(c);
                      printf("sin devolver: %d\\n", prestadas);
                      devolver(b);
                      printf("sin devolver: %d\\n", prestadas);
                      return 0;
                  }
              ''',
              al_superar="Cero sin devolver. La Sanguijuela se da vuelta, molesta: por ese lado no le queda nada para comer.",
              imagen=[SANGUIJUELA + " enroscada en las vías.", HULDA + " sostiene una tablilla con una cuenta que llega a cero."]),
            m(id="R03-N06-P2", titulo="Liberar toda la cadena",
              lugar="Lo más hondo de las Minas", personajes="Kira, Gheco, Tizón",
              criatura="troll",
              carta="Liberar una lista | guardar el siguiente ANTES del free · después del free, el nodo ya no se puede leer",
              recompensa="xp 15, oro 15",
              escena="La Sanguijuela se enrosca en un tren abandonado de cinco vagones. Para dejarla sin comida, hay que liberar los cinco… sin leer ningún vagón ya liberado.",
              sugiere="En el bucle: `Vagon *sig = p->siguiente;` **antes** de `free(p)`, y después `p = sig;`.",
              desafio="Completá la liberación segura.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Vagon {
                      int numero;
                      struct Vagon *siguiente;
                  } Vagon;

                  int main(void)
                  {
                      Vagon *tren = NULL;
                      for (int i = 5; i >= 1; i--) {
                          Vagon *n = malloc(sizeof *n);
                          if (n == NULL) {
                              return 1;
                          }
                          n->numero = i;
                          n->siguiente = tren;
                          tren = n;
                      }
                      int liberados = 0;
                      Vagon *p = tren;
                      while (p != NULL) {
                          ___;
                          free(p);
                          liberados++;
                          ___;
                      }
                      printf("vagones liberados: %d\\n", liberados);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Vagon {
                      int numero;
                      struct Vagon *siguiente;
                  } Vagon;

                  int main(void)
                  {
                      Vagon *tren = NULL;
                      for (int i = 5; i >= 1; i--) {
                          Vagon *n = malloc(sizeof *n);
                          if (n == NULL) {
                              return 1;
                          }
                          n->numero = i;
                          n->siguiente = tren;
                          tren = n;
                      }
                      int liberados = 0;
                      Vagon *p = tren;
                      while (p != NULL) {
                          Vagon *sig = p->siguiente;
                          free(p);
                          liberados++;
                          p = sig;
                      }
                      printf("vagones liberados: %d\\n", liberados);
                      return 0;
                  }
              ''',
              al_superar="Cinco vagones liberados, ni uno perdido. La Sanguijuela se queda sin el tren y empieza a achicarse.",
              imagen=["Un tren de cinco vagones que se desarma de a uno, en orden.", "La Sanguijuela, más flaca, se aleja."]),
            m(id="R03-N06-P3", titulo="La lámpara que no deja esconderse",
              lugar="Lo más hondo de las Minas", personajes="Kira, Gheco, Hulda",
              carta="El orden de los free | primero lo de adentro, después lo de afuera · un struct con un puntero a memoria pedida necesita dos free",
              recompensa="xp 15, oro 15",
              escena="Hulda le da a Kira una lámpara que brilla distinto, y con esa luz se ve el truco: cada minero tiene un **nombre** pedido aparte. Liberar la ficha sin liberar el nombre deja comida para la Sanguijuela.",
              sugiere="Si un struct pedido con `malloc` tiene adentro otro bloque pedido (el nombre), primero se libera el de **adentro** (`free(m->nombre)`) y después el de afuera (`free(m)`).",
              desafio="Completá los dos `free` en el orden correcto.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  typedef struct {
                      char *nombre;
                      int vida;
                  } Minero;

                  Minero *crear(const char *nombre, int vida)
                  {
                      Minero *m = malloc(sizeof *m);
                      if (m == NULL) {
                          return NULL;
                      }
                      m->nombre = malloc(strlen(nombre) + 1);
                      if (m->nombre == NULL) {
                          free(m);
                          return NULL;
                      }
                      strcpy(m->nombre, nombre);
                      m->vida = vida;
                      return m;
                  }

                  void destruir(Minero *m)
                  {
                      ___;
                      ___;
                  }

                  int main(void)
                  {
                      Minero *m = crear("Hulda", 120);
                      if (m == NULL) {
                          return 1;
                      }
                      printf("%s con %d de vida\\n", m->nombre, m->vida);
                      destruir(m);
                      printf("ficha y nombre devueltos\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  typedef struct {
                      char *nombre;
                      int vida;
                  } Minero;

                  Minero *crear(const char *nombre, int vida)
                  {
                      Minero *m = malloc(sizeof *m);
                      if (m == NULL) {
                          return NULL;
                      }
                      m->nombre = malloc(strlen(nombre) + 1);
                      if (m->nombre == NULL) {
                          free(m);
                          return NULL;
                      }
                      strcpy(m->nombre, nombre);
                      m->vida = vida;
                      return m;
                  }

                  void destruir(Minero *m)
                  {
                      free(m->nombre);
                      free(m);
                  }

                  int main(void)
                  {
                      Minero *m = crear("Hulda", 120);
                      if (m == NULL) {
                          return 1;
                      }
                      printf("%s con %d de vida\\n", m->nombre, m->vida);
                      destruir(m);
                      printf("ficha y nombre devueltos\\n");
                      return 0;
                  }
              ''',
              al_superar="Con la lámpara encendida, la Sanguijuela ya no tiene dónde esconderse. Se encoge contra la pared de roca.",
              imagen=["Una lámpara de minero que proyecta una luz cian sobre las paredes de la mina.", HULDA + " se la entrega a " + KIRA + "."]),
            m(id="R03-N06-P4", titulo="La Sanguijuela, flaquita",
              lugar="Lo más hondo de las Minas", personajes="Kira, Gheco, Hulda, Chispa",
              criatura="dragon",
              carta="Todo junto | pedir, crecer, enganchar y devolver todo · contar lo que queda prestado · terminar en cero",
              recompensa="xp 25, oro 30",
              item="Lámpara del Minero",
              escena="""
                  Última pelea. La Sanguijuela tiene en la panza las vagonetas de toda la temporada. Kira arma una cola de vagonetas, las saca una por una por la boca de la mina, y las devuelve todas. Si al final la tablilla da cero, la Sanguijuela no tiene de qué vivir.
              """,
              sugiere="Encolar pide (`malloc`, suma 1), desencolar devuelve (`free`, resta 1). Al terminar, se desencola todo y la cuenta tiene que dar 0.",
              desafio="Completá el desencolado y la cuenta.",
              entrada="3\n",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Nodo {
                      int numero;
                      struct Nodo *siguiente;
                  } Nodo;

                  static int prestadas = 0;

                  int main(void)
                  {
                      Nodo *frente = NULL, *fondo = NULL;
                      int salen;
                      for (int i = 1; i <= 6; i++) {
                          Nodo *n = malloc(sizeof *n);
                          if (n == NULL) {
                              return 1;
                          }
                          prestadas++;
                          n->numero = i;
                          n->siguiente = NULL;
                          if (fondo == NULL) {
                              frente = n;
                          } else {
                              fondo->siguiente = n;
                          }
                          fondo = n;
                      }
                      scanf("%d", &salen);
                      for (int k = 0; k < salen; k++) {
                          Nodo *sale = frente;
                          frente = frente->siguiente;
                          printf("sale la vagoneta %d\\n", sale->numero);
                          free(sale);
                          prestadas--;
                      }
                      printf("en la panza de la sanguijuela: %d\\n", prestadas);
                      while (frente != NULL) {
                          Nodo *sale = frente;
                          ___;
                          ___;
                          ___;
                      }
                      fondo = NULL;
                      printf("en la panza de la sanguijuela: %d\\n", prestadas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct Nodo {
                      int numero;
                      struct Nodo *siguiente;
                  } Nodo;

                  static int prestadas = 0;

                  int main(void)
                  {
                      Nodo *frente = NULL, *fondo = NULL;
                      int salen;
                      for (int i = 1; i <= 6; i++) {
                          Nodo *n = malloc(sizeof *n);
                          if (n == NULL) {
                              return 1;
                          }
                          prestadas++;
                          n->numero = i;
                          n->siguiente = NULL;
                          if (fondo == NULL) {
                              frente = n;
                          } else {
                              fondo->siguiente = n;
                          }
                          fondo = n;
                      }
                      scanf("%d", &salen);
                      for (int k = 0; k < salen; k++) {
                          Nodo *sale = frente;
                          frente = frente->siguiente;
                          printf("sale la vagoneta %d\\n", sale->numero);
                          free(sale);
                          prestadas--;
                      }
                      printf("en la panza de la sanguijuela: %d\\n", prestadas);
                      while (frente != NULL) {
                          Nodo *sale = frente;
                          frente = frente->siguiente;
                          free(sale);
                          prestadas--;
                      }
                      fondo = NULL;
                      printf("en la panza de la sanguijuela: %d\\n", prestadas);
                      return 0;
                  }
              ''',
              al_superar="Cero. La Sanguijuela queda flaquita y avergonzada, y se escurre por una grieta. Hulda le regala a Kira la lámpara: **la Lámpara del Minero**, que va a tu mochila. —Para que no se te esconda nada nunca más. —Chispa paga, por primera vez, todas sus vagonetas atrasadas. En chistes.",
              imagen=["La Sanguijuela, flaquita y avergonzada, se escurre por una grieta.",
                      HULDA + " le da una lámpara de minero a " + KIRA + ".", CHISPA + " cuenta un chiste frente a toda la mina."]),
        ],
    },
]
