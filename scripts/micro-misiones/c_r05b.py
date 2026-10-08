from genc import m
from c_r01 import KIRA, TIZON, FERRUM

FRAGUA = "La fragua bajo la Montaña"
DRAGON = "El Dragón bajo la Montaña (dragón de hierro negro con escamas como placas de forja, venas de lava, alas de chapa remachada y un horno encendido en el pecho)"

NODOS = [
    {
        "titulo": "R05-N04 · Jefe final: el Dragón bajo la Montaña",
        "misiones": [
            m(id="R05-N04-P1", titulo="Primera escama: el valor que vale",
              lugar=FRAGUA, personajes="Kira, Gheco, Tizón",
              criatura="dragon",
              carta="Leer validando | fgets + sscanf · si no es un número o está fuera de rango, avisar y volver a pedir el MISMO dato",
              recompensa="xp 20, oro 20",
              escena="""
                  El Dragón duerme sobre el plomo del Vidriero y ronca fuego. En la primera escama del lomo hay grabado un pedido: temperaturas entre 0 y 1500 grados, y ni una que no lo sea.
                  Kira se sienta, saca la libreta de Tizón y empieza por lo primero: leer **bien**.
              """,
              sugiere="`leer_valor` lee una línea con `fgets`; si `sscanf` no da un número o el número está fuera de 0.0 a 1500.0, avisa y vuelve a leer. Recién cuando el dato sirve, lo devuelve.",
              desafio="Completá la condición del dato válido.",
              entrada="900\n5000\nfuego\n1200\n",
              inicial='''
                  #include <stdio.h>

                  double leer_valor(void)
                  {
                      char linea[50];
                      double valor;
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (___) {
                              return valor;
                          }
                          printf("valor invalido, de nuevo\\n");
                      }
                      return 0.0;
                  }

                  int main(void)
                  {
                      double a = leer_valor();
                      double b = leer_valor();
                      printf("aceptados: %.1f y %.1f\\n", a, b);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  double leer_valor(void)
                  {
                      char linea[50];
                      double valor;
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (sscanf(linea, "%lf", &valor) == 1 && valor >= 0.0 && valor <= 1500.0) {
                              return valor;
                          }
                          printf("valor invalido, de nuevo\\n");
                      }
                      return 0.0;
                  }

                  int main(void)
                  {
                      double a = leer_valor();
                      double b = leer_valor();
                      printf("aceptados: %.1f y %.1f\\n", a, b);
                      return 0;
                  }
              ''',
              al_superar="La primera escama se apaga. El Dragón abre un ojo, mira a Kira, y lo vuelve a cerrar. No parece preocupado. Todavía.",
              imagen=[DRAGON + " dormido sobre un lago de plomo fundido, con una escama del lomo apagándose.", KIRA + " sentada con una libreta, mirándolo sin miedo."]),
            m(id="R05-N04-P2", titulo="Segunda escama: el pico y dónde fue",
              lugar=FRAGUA, personajes="Kira, Gheco, Tizón",
              criatura="dragon",
              carta="El mayor de una matriz con su lugar | recorrer filas y columnas · guardar la fila y la columna, no solo el valor · devolverlas por puntero",
              recompensa="xp 20, oro 20",
              escena="La segunda escama pide el día y el horno de la temperatura más alta de la semana. —El número solo no me sirve —dice Tizón—. Necesito saber **dónde** fue, para ir a medirlo.",
              sugiere="`pico(t, &dia, &horno)` arranca con `(0, 0)` y recorre la matriz: cuando encuentra uno mayor que `t[*dia][*horno]`, guarda esa fila y esa columna.",
              desafio="Completá la comparación y lo que se guarda.",
              inicial='''
                  #include <stdio.h>

                  #define DIAS 3
                  #define HORNOS 4

                  void pico(double t[DIAS][HORNOS], int *dia, int *horno)
                  {
                      *dia = 0;
                      *horno = 0;
                      for (int d = 0; d < DIAS; d++) {
                          for (int h = 0; h < HORNOS; h++) {
                              if (___) {
                                  *dia = d;
                                  *horno = ___;
                              }
                          }
                      }
                  }

                  int main(void)
                  {
                      double t[DIAS][HORNOS] = {
                          { 800, 950, 700, 1000 },
                          { 820, 900, 720, 1100 },
                          { 860, 1180, 680, 1060 },
                      };
                      int dia, horno;
                      pico(t, &dia, &horno);
                      printf("pico: %.1f, dia %d, horno %d\\n", t[dia][horno], dia + 1, horno + 1);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define DIAS 3
                  #define HORNOS 4

                  void pico(double t[DIAS][HORNOS], int *dia, int *horno)
                  {
                      *dia = 0;
                      *horno = 0;
                      for (int d = 0; d < DIAS; d++) {
                          for (int h = 0; h < HORNOS; h++) {
                              if (t[d][h] > t[*dia][*horno]) {
                                  *dia = d;
                                  *horno = h;
                              }
                          }
                      }
                  }

                  int main(void)
                  {
                      double t[DIAS][HORNOS] = {
                          { 800, 950, 700, 1000 },
                          { 820, 900, 720, 1100 },
                          { 860, 1180, 680, 1060 },
                      };
                      int dia, horno;
                      pico(t, &dia, &horno);
                      printf("pico: %.1f, dia %d, horno %d\\n", t[dia][horno], dia + 1, horno + 1);
                      return 0;
                  }
              ''',
              al_superar="Día 3, horno 2: 1180 grados. Tizón va a medirlo y vuelve con las cejas un poco más cortas, como Ferrum. Se siente un herrero de verdad.",
              imagen=["Una tabla de temperaturas grabada en una escama de hierro, con una celda que brilla en rojo.", TIZON + " vuelve con las cejas chamuscadas, orgulloso."]),
            m(id="R05-N04-P3", titulo="Tercera escama: ordenar sin perder el horno",
              lugar=FRAGUA, personajes="Kira, Gheco, Maese Ferrum",
              criatura="dragon",
              carta="Ordenar con su referencia | un array de structs {horno, promedio} · se intercambia el struct entero · el número viaja con su promedio",
              recompensa="xp 20, oro 20",
              escena="La tercera escama pide los promedios de los hornos de mayor a menor. Kira ordenó el array de promedios suelto y ya no sabe de qué horno es cada uno. Ferrum gruñe: —Que el número viaje con su promedio.",
              sugiere="Con `PromedioHorno v[4]`, la burbuja compara `v[i].promedio` pero intercambia **el struct entero**: el número de horno se mueve junto con su promedio.",
              desafio="Completá la comparación (de mayor a menor) y el intercambio.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int horno;
                      double promedio;
                  } PromedioHorno;

                  int main(void)
                  {
                      PromedioHorno v[4] = { { 1, 845.7 }, { 2, 930.0 }, { 3, 701.4 }, { 4, 1042.9 } };
                      for (int pasada = 0; pasada < 3; pasada++) {
                          for (int i = 0; i < 3 - pasada; i++) {
                              if (___) {
                                  PromedioHorno aux = v[i];
                                  ___;
                                  v[i + 1] = aux;
                              }
                          }
                      }
                      for (int i = 0; i < 4; i++) {
                          printf("horno %d: %.1f\\n", v[i].horno, v[i].promedio);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int horno;
                      double promedio;
                  } PromedioHorno;

                  int main(void)
                  {
                      PromedioHorno v[4] = { { 1, 845.7 }, { 2, 930.0 }, { 3, 701.4 }, { 4, 1042.9 } };
                      for (int pasada = 0; pasada < 3; pasada++) {
                          for (int i = 0; i < 3 - pasada; i++) {
                              if (v[i + 1].promedio > v[i].promedio) {
                                  PromedioHorno aux = v[i];
                                  v[i] = v[i + 1];
                                  v[i + 1] = aux;
                              }
                          }
                      }
                      for (int i = 0; i < 4; i++) {
                          printf("horno %d: %.1f\\n", v[i].horno, v[i].promedio);
                      }
                      return 0;
                  }
              ''',
              al_superar="Horno 4, 2, 1 y 3, cada uno con su promedio. La tercera escama se apaga y el Dragón se despierta del todo. Se levanta. Es enorme.",
              imagen=[DRAGON + " despertándose, con tres escamas apagadas en el lomo.", FERRUM + " en la entrada de la fragua, sin intervenir."]),
            m(id="R05-N04-P4", titulo="Cuarta escama: la hoja que se mide",
              lugar=FRAGUA, personajes="Kira, Gheco, Tizón, Maese Ferrum",
              criatura="dragon",
              carta="Clasificar con varias reglas | el orden de las condiciones importa · la más exigente primero · «ninguna nota menor a 7» es un && de las tres",
              recompensa="xp 25, oro 25",
              item="Hoja Templada",
              escena="""
                  El Dragón ruge y escupe fuego sobre el yunque de la fragua. Es el momento: Kira mete en el fuego el acero que guardó toda la temporada y empieza a forjar **su propia hoja**. Cada golpe se mide; cada temple se clasifica.
                  Tizón le pasa las medidas sin que se las pida. Ella las usa sin protestar.
              """,
              sugiere="Primero la regla más exigente: **templada** si el promedio es 8 o más y **ninguna** de las tres medidas es menor a 7. Si no, **usable** si el promedio es 6 o más. Si no, **de vuelta al fuego**.",
              desafio="Completá las dos condiciones.",
              entrada="9 8 9\n10 8 6\n5 6 4\n",
              inicial='''
                  #include <stdio.h>

                  const char *temple(int a, int b, int c)
                  {
                      double promedio = (a + b + c) / 3.0;
                      if (___) {
                          return "templada";
                      } else if (___) {
                          return "usable";
                      }
                      return "de vuelta al fuego";
                  }

                  int main(void)
                  {
                      int a, b, c;
                      while (scanf("%d %d %d", &a, &b, &c) == 3) {
                          printf("%d %d %d -> %s\\n", a, b, c, temple(a, b, c));
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  const char *temple(int a, int b, int c)
                  {
                      double promedio = (a + b + c) / 3.0;
                      if (promedio >= 8 && a >= 7 && b >= 7 && c >= 7) {
                          return "templada";
                      } else if (promedio >= 6) {
                          return "usable";
                      }
                      return "de vuelta al fuego";
                  }

                  int main(void)
                  {
                      int a, b, c;
                      while (scanf("%d %d %d", &a, &b, &c) == 3) {
                          printf("%d %d %d -> %s\\n", a, b, c, temple(a, b, c));
                      }
                      return 0;
                  }
              ''',
              al_superar="La primera medida da «templada». Kira saca la hoja del agua: brilla con un filo cian, medida grado por grado. Es **la Hoja Templada**, forjada por ella misma, y va a tu mochila. Ferrum no dice nada. Golpea el yunque dos veces. Después, una tercera.",
              imagen=[KIRA + " saca del agua una espada que brilla con un filo cian, envuelta en vapor.",
                      DRAGON + " retrocede ante el brillo.", TIZON + " sostiene la libreta abierta con las medidas.", FERRUM + " golpea el yunque."]),
            m(id="R05-N04-P5", titulo="La última escama",
              lugar=FRAGUA, personajes="Kira, Gheco, Tizón, Maese Ferrum",
              criatura="dragon",
              carta="El parcial entero | matriz + estructuras + archivo · validar, recorrer, ordenar, dar de baja · cada pieza en su función, y tres horas para todo",
              recompensa="xp 30, oro 40",
              item="Matriz del Marco",
              escena="""
                  La última escama es la del corazón. Para apagarla hay que dar de baja, en el registro de la fragua, las piezas falsas que el Dragón fue tragando (las de temperatura imposible), sin borrar ninguna, y contar las que quedan.
              """,
              sugiere="Se recorre el archivo con `\"r+b\"`: a cada pieza con temperatura mayor a 1500 se le pone `'B'`, se vuelve con `fseek` y se reescribe; entre escribir y leer de nuevo va un `fseek(f, 0, SEEK_CUR)`. Después se cuentan las activas.",
              desafio="Completá la vuelta atrás y el conteo de activas.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      double grados;
                      char estado;
                  } Pieza;

                  int main(void)
                  {
                      Pieza p[5] = { { 1, 900, 'A' }, { 2, 99999, 'A' }, { 3, 1200, 'A' }, { 4, 7000, 'A' }, { 5, 850, 'A' } };
                      FILE *f = fopen("fragua.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      fwrite(p, sizeof p[0], 5, f);
                      fclose(f);

                      f = fopen("fragua.dat", "r+b");
                      if (f == NULL) {
                          return 1;
                      }
                      Pieza x;
                      while (fread(&x, sizeof x, 1, f) == 1) {
                          if (x.grados > 1500 && x.estado == 'A') {
                              x.estado = 'B';
                              fseek(f, ___, SEEK_CUR);
                              fwrite(&x, sizeof x, 1, f);
                              fseek(f, 0, SEEK_CUR);
                          }
                      }
                      rewind(f);
                      int activas = 0;
                      while (fread(&x, sizeof x, 1, f) == 1) {
                          if (___) {
                              activas++;
                          }
                      }
                      fclose(f);
                      printf("piezas activas: %d de 5\\n", activas);
                      if (activas == 3) {
                          printf("la ultima escama se apaga\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      double grados;
                      char estado;
                  } Pieza;

                  int main(void)
                  {
                      Pieza p[5] = { { 1, 900, 'A' }, { 2, 99999, 'A' }, { 3, 1200, 'A' }, { 4, 7000, 'A' }, { 5, 850, 'A' } };
                      FILE *f = fopen("fragua.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      fwrite(p, sizeof p[0], 5, f);
                      fclose(f);

                      f = fopen("fragua.dat", "r+b");
                      if (f == NULL) {
                          return 1;
                      }
                      Pieza x;
                      while (fread(&x, sizeof x, 1, f) == 1) {
                          if (x.grados > 1500 && x.estado == 'A') {
                              x.estado = 'B';
                              fseek(f, -(long) sizeof x, SEEK_CUR);
                              fwrite(&x, sizeof x, 1, f);
                              fseek(f, 0, SEEK_CUR);
                          }
                      }
                      rewind(f);
                      int activas = 0;
                      while (fread(&x, sizeof x, 1, f) == 1) {
                          if (x.estado == 'A') {
                              activas++;
                          }
                      }
                      fclose(f);
                      printf("piezas activas: %d de 5\\n", activas);
                      if (activas == 3) {
                          printf("la ultima escama se apaga\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="La última escama se apaga y el Dragón bajo la Montaña se echa, manso, a un costado del lago de plomo. Detrás de él hay un molde enorme: **la Matriz del Marco** que dejó el Vidriero, con la inscripción *«para quien llegue»*. Va a tu mochila. Ferrum la mira largo rato. —Este es el marco —dice—. El mismo que dicen que espera en la torre más alta del Imperio.",
              imagen=[DRAGON + " echado y manso junto a un lago de plomo, con todas las escamas apagadas.",
                      "Un molde de plomo enorme con forma de marco de vitral y la inscripción «para quien llegue».",
                      KIRA + " con la Hoja Templada en la mano, frente al molde.", FERRUM + " y " + TIZON + " detrás, en silencio."]),
        ],
    },
]
