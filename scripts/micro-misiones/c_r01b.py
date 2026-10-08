from genc import m
from c_r01 import KIRA, TIZON, FERRUM, CHISPA

HULDA = "Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro)"

NODOS = [
    {
        "titulo": "R01-N06 · Bucles",
        "misiones": [
            m(id="R01-N06-P1", titulo="Cuarenta martillazos",
              lugar="El yunque de la Forja", personajes="Kira, Gheco, Maese Ferrum",
              carta="for | for (int i = 1; i <= n; i++) { … } · arranque; condición; paso · para repetir una cantidad sabida",
              recompensa="xp 10, oro 10",
              escena="Una herradura lleva **exactamente** cuarenta martillazos. Ferrum quiere que Kira cuente de diez en diez, en voz alta, para que no se pase.",
              sugiere="`for (arranque; condición; paso)` repite mientras la condición se cumpla. Con `i += 10` el paso es de diez en diez.",
              desafio="Completá el `for` para contar de 10 a 40 de diez en diez.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      for (int golpes = ___; golpes ___ 40; golpes ___) {
                          printf("%d martillazos\\n", golpes);
                      }
                      printf("herradura lista\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      for (int golpes = 10; golpes <= 40; golpes += 10) {
                          printf("%d martillazos\\n", golpes);
                      }
                      printf("herradura lista\\n");
                      return 0;
                  }
              ''',
              al_superar="Cuarenta, ni uno más. Ferrum golpea el yunque dos veces. Kira no entiende si es un aplauso o un tic.",
              imagen=[KIRA + " martilla una herradura al rojo sobre un yunque.", FERRUM + " cuenta con los dedos.", "Números luminosos 10, 20, 30, 40 flotan sobre el yunque."]),
            m(id="R01-N06-P2", titulo="El fuelle que no para",
              lugar="El horno de la Forja", personajes="Kira, Gheco, Maese Ferrum, Tizón",
              criatura="ogro",
              carta="while | while (condición) { … } · repite mientras se cumpla · algo adentro tiene que acercarlo al final",
              recompensa="xp 10, oro 10",
              escena="""
                  El fuelle mecánico sopló toda la noche: la orden decía «soplá mientras el horno **no esté frío**». A la mañana, la Forja es un volcán y Ferrum tiene las cejas chamuscadas.
                  En la pared, Tizón agrega: «Fuelles que no paran: 1».
              """,
              sugiere="`while (condición)` repite **mientras** la condición se cumpla. Tiene que decir cuándo **seguir**: mientras el horno no llegue a la temperatura.",
              desafio="Corregí la condición: soplar mientras el horno esté por debajo de 900 grados.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int grados = 600;
                      int soplidos = 0;
                      while (grados > 2000) {
                          grados += 75;
                          soplidos++;
                      }
                      printf("%d soplidos: horno a %d grados\\n", soplidos, grados);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int grados = 600;
                      int soplidos = 0;
                      while (grados < 900) {
                          grados += 75;
                          soplidos++;
                      }
                      printf("%d soplidos: horno a %d grados\\n", soplidos, grados);
                      return 0;
                  }
              ''',
              al_superar="Cuatro soplidos y el horno queda justo en 900. Ferrum se mira las cejas en el reflejo de un escudo, suspira, y no dice nada.",
              imagen=["Un fuelle mecánico de cobre soplando junto a un horno enorme.", FERRUM + " con las cejas chamuscadas.", TIZON + " escribe en la pared con tiza."]),
            m(id="R01-N06-P3", titulo="Preguntar hasta que conteste bien",
              lugar="La ventanilla de la Forja", personajes="Kira, Gheco, Chispa",
              carta="do-while | do { … } while (condición); · se ejecuta al menos una vez · ideal para validar lo que se pide",
              recompensa="xp 10, oro 10",
              escena="Chispa tiene que elegir una cantidad de 1 a 10 herraduras. Contesta 0, después 15, después 4. La ventanilla tiene que seguir preguntando hasta que el número tenga sentido.",
              sugiere="`do { … } while (condición);` ejecuta el bloque **primero** y pregunta después: sirve para pedir un dato hasta que sea válido. Termina con `;`.",
              desafio="Completá la condición para repetir mientras la cantidad no esté entre 1 y 10.",
              entrada="0\n15\n4\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int cantidad;
                      int intentos = 0;
                      do {
                          scanf("%d", &cantidad);
                          intentos++;
                      } while (___);
                      printf("Chispa pide %d herraduras (al intento %d)\\n", cantidad, intentos);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int cantidad;
                      int intentos = 0;
                      do {
                          scanf("%d", &cantidad);
                          intentos++;
                      } while (cantidad < 1 || cantidad > 10);
                      printf("Chispa pide %d herraduras (al intento %d)\\n", cantidad, intentos);
                      return 0;
                  }
              ''',
              al_superar="Cuatro herraduras, al tercer intento. —Precio de amigo —dice Chispa—, porque sos vos. —Tizón revisa la balanza.",
              imagen=["Una ventanilla con tres fichas: un 0 y un 15 tachados, y un 4 aprobado.", CHISPA + " sonriendo con el diente de oro."]),
            m(id="R01-N06-P4", titulo="El acumulador del carbón",
              lugar="El depósito de la Forja", personajes="Kira, Gheco, Tizón",
              carta="Acumular y contar | total += valor en cada vuelta · contador++ para saber cuántos · inicializar ANTES del bucle",
              recompensa="xp 15, oro 15",
              escena="Llegan bolsas de carbón de distinto peso, una por línea, y al final un 0. Tizón quiere el total y el promedio, «con los decimales que correspondan».",
              sugiere="Un **acumulador** (`total += peso`) y un **contador** (`bolsas++`) se inicializan en 0 antes del bucle. El promedio se calcula al final, con `(double)`.",
              desafio="Completá el acumulador y el contador.",
              entrada="12\n8\n15\n5\n0\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int peso;
                      int total = 0;
                      int bolsas = 0;
                      scanf("%d", &peso);
                      while (peso != 0) {
                          ___;
                          ___;
                          scanf("%d", &peso);
                      }
                      printf("%d bolsas, %d kg, promedio %.2f kg\\n", bolsas, total, (double) total / bolsas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int peso;
                      int total = 0;
                      int bolsas = 0;
                      scanf("%d", &peso);
                      while (peso != 0) {
                          total += peso;
                          bolsas++;
                          scanf("%d", &peso);
                      }
                      printf("%d bolsas, %d kg, promedio %.2f kg\\n", bolsas, total, (double) total / bolsas);
                      return 0;
                  }
              ''',
              al_superar="Cuatro bolsas, cuarenta kilos, diez de promedio. Tizón queda feliz: el promedio dio redondo.",
              imagen=["Bolsas de carbón de distinto tamaño en fila, con números de peso.", TIZON + " suma en la libreta con la lengua afuera."]),
        ],
    },
    {
        "titulo": "R01-N07 · Funciones",
        "misiones": [
            m(id="R01-N07-P1", titulo="El martillo de cada uno",
              lugar="El taller de los martillos", personajes="Kira, Gheco, Hulda",
              carta="Función | tipo nombre(parámetros) { … return valor; } · se llama con sus argumentos · devuelve un resultado",
              recompensa="xp 10, oro 10",
              escena="Kira agarra el martillo de Hulda para calcular el daño de un golpe… y le tuerce el mango. Hulda le explica, con la voz de capataz, que cada cuenta tiene su martillo: su **función**.",
              sugiere="Una función se escribe una vez y se usa muchas: `int danio(int ataque, int defensa) { return …; }` y se llama `danio(15, 4)`.",
              desafio="Completá la función: el daño es el ataque menos la defensa.",
              inicial='''
                  #include <stdio.h>

                  int danio(int ataque, int defensa)
                  {
                      ___
                  }

                  int main(void)
                  {
                      printf("Kira contra un goblin: %d\\n", danio(15, 4));
                      printf("Hulda contra un orco: %d\\n", danio(22, 9));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int danio(int ataque, int defensa)
                  {
                      return ataque - defensa;
                  }

                  int main(void)
                  {
                      printf("Kira contra un goblin: %d\\n", danio(15, 4));
                      printf("Hulda contra un orco: %d\\n", danio(22, 9));
                      return 0;
                  }
              ''',
              al_superar="Un martillo, dos golpes, dos resultados. Hulda le devuelve a Kira el martillo torcido para que lo enderece. Con su propia función.",
              imagen=["Una pared con martillos colgados, cada uno con una etiqueta: afilar, templar, daño.", HULDA + " sostiene un martillo con el mango torcido."]),
            m(id="R01-N07-P2", titulo="La copia que no cura",
              lugar="El taller de los martillos", personajes="Kira, Gheco, Tizón",
              criatura="ogro",
              carta="Paso por valor | la función recibe una COPIA · cambiarla no cambia la de afuera · devolvé el valor nuevo y guardalo",
              recompensa="xp 10, oro 10",
              escena="Tizón se lastimó la mano. Kira llama a la función `curar`… y la vida de Tizón sigue igual. —¿Me curaste o no? —pregunta, mirándose la mano.",
              sugiere="C pasa una **copia** del argumento: si la función la cambia, la variable de afuera no se entera. La función tiene que **devolver** la vida nueva y quien llama, guardarla.",
              desafio="Hacé que `curar` devuelva la vida nueva y guardala.",
              inicial='''
                  #include <stdio.h>

                  void curar(int vida)
                  {
                      vida = vida + 30;
                  }

                  int main(void)
                  {
                      int vida_tizon = 50;
                      curar(vida_tizon);
                      printf("vida de Tizon: %d\\n", vida_tizon);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int curar(int vida)
                  {
                      return vida + 30;
                  }

                  int main(void)
                  {
                      int vida_tizon = 50;
                      vida_tizon = curar(vida_tizon);
                      printf("vida de Tizon: %d\\n", vida_tizon);
                      return 0;
                  }
              ''',
              al_superar="Ochenta. Tizón mueve los dedos, uno por uno, y anota en la libreta: «Curado: sí. Copia: no».",
              imagen=[TIZON + " con una mano vendada que brilla de verde.", KIRA + " lee un pergamino con la función curar."]),
            m(id="R01-N07-P3", titulo="El contador que recuerda",
              lugar="El taller de los martillos", personajes="Kira, Gheco, Maese Ferrum",
              carta="static local | static int n = 0; se inicializa UNA vez · recuerda su valor entre llamadas · solo la ve su función",
              recompensa="xp 10, oro 10",
              escena="Ferrum quiere saber cuántos espadazos lleva Kira, pero cada vez que llama a `espadazo()` la cuenta vuelve a 1. La función se olvida de todo al terminar.",
              sugiere="Una variable local nace y muere con cada llamada. Con `static` delante se inicializa **una sola vez** y **recuerda** su valor.",
              desafio="Hacé que la función recuerde la cuenta.",
              inicial='''
                  #include <stdio.h>

                  int espadazo(void)
                  {
                      int cuenta = 0;
                      cuenta++;
                      return cuenta;
                  }

                  int main(void)
                  {
                      espadazo();
                      espadazo();
                      printf("Espadazos: %d\\n", espadazo());
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int espadazo(void)
                  {
                      static int cuenta = 0;
                      cuenta++;
                      return cuenta;
                  }

                  int main(void)
                  {
                      espadazo();
                      espadazo();
                      printf("Espadazos: %d\\n", espadazo());
                      return 0;
                  }
              ''',
              al_superar="Tres espadazos, contados. Ferrum los suma a la cuenta de la pared, que ya va por treinta y pico. Kira pide que no la sume en voz alta.",
              imagen=["Una pared con una cuenta de tiza larguísima bajo el título «Espadazos».", FERRUM + " agrega tres palitos más."]),
            m(id="R01-N07-P4", titulo="La página que se llama a sí misma",
              lugar="El libro de la Forja", personajes="Kira, Gheco, Tizón",
              carta="Recursión | una función que se llama con un problema más chico · caso base: cuándo parar · sin caso base, la pila se desborda",
              recompensa="xp 15, oro 15",
              item=None,
              escena="En el libro de la Forja hay una página rara: «para contar los eslabones de una cadena, contá el primero y después contá los eslabones del resto». Tizón la lee tres veces y se marea.",
              sugiere="Una función **recursiva** se llama a sí misma con un caso más chico y tiene un **caso base** que corta. `eslabones(0)` es 0; `eslabones(n)` es 1 más `eslabones(n - 1)`.",
              desafio="Completá el caso base y la llamada recursiva.",
              inicial='''
                  #include <stdio.h>

                  int eslabones(int n)
                  {
                      if (n == 0) {
                          return ___;
                      }
                      return 1 + ___;
                  }

                  int main(void)
                  {
                      printf("una cadena de 7: %d eslabones\\n", eslabones(7));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int eslabones(int n)
                  {
                      if (n == 0) {
                          return 0;
                      }
                      return 1 + eslabones(n - 1);
                  }

                  int main(void)
                  {
                      printf("una cadena de 7: %d eslabones\\n", eslabones(7));
                      return 0;
                  }
              ''',
              al_superar="Siete. Entre las páginas del libro cae un papel viejo: un **pedido de plomo** enorme, pagado por adelantado, firmado con el dibujo de un vitral. Igual al que estaba junto a Kira cuando despertó.",
              imagen=["Un libro enorme de la Forja abierto en una página con una cadena dibujada que se repite cada vez más chica.",
                      "Un papel viejo que cae del libro: un pedido de plomo firmado con el dibujo de un vitral.",
                      KIRA + " lo levanta del piso, seria."]),
        ],
    },
    {
        "titulo": "R01-N08 · El preprocesador y las macros",
        "misiones": [
            m(id="R01-N08-P1", titulo="El sello del tamaño",
              lugar="El taller de marcar", personajes="Kira, Gheco, Tizón",
              carta="#define | #define NOMBRE valor · el preprocesador lo reemplaza antes de compilar · en MAYUSCULAS y sin ;",
              recompensa="xp 10, oro 10",
              escena="En el taller de marcar, cada caja dice cuántas piezas lleva. Tizón escribió el 12 en cinco lugares distintos de la receta, y ahora las cajas son de 10. Le toca buscar cada 12. Hay un sello mejor.",
              sugiere="`#define PIEZAS_POR_CAJA 10` define una constante: antes de compilar, el preprocesador cambia cada `PIEZAS_POR_CAJA` por `10`. Va sin `;`.",
              desafio="Definí la constante para que todo el programa use 10.",
              inicial='''
                  #include <stdio.h>

                  ___

                  int main(void)
                  {
                      int piezas = 47;
                      printf("cajas llenas: %d\\n", piezas / PIEZAS_POR_CAJA);
                      printf("sueltas: %d\\n", piezas % PIEZAS_POR_CAJA);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define PIEZAS_POR_CAJA 10

                  int main(void)
                  {
                      int piezas = 47;
                      printf("cajas llenas: %d\\n", piezas / PIEZAS_POR_CAJA);
                      printf("sueltas: %d\\n", piezas % PIEZAS_POR_CAJA);
                      return 0;
                  }
              ''',
              al_superar="Un solo lugar para cambiar el tamaño. Tizón tacha en la libreta «buscar cada 12» y escribe «nunca más».",
              imagen=["Un sello de bronce que estampa «10» sobre muchas cajas a la vez.", TIZON + " tacha una lista larguísima."]),
            m(id="R01-N08-P2", titulo="La herradura banana",
              lugar="El taller de marcar", personajes="Kira, Gheco, Tizón, Maese Ferrum",
              criatura="ogro",
              carta="Macro con parámetros | #define CUBO(a) ((a) * (a) * (a)) · un paréntesis por parámetro y otro por todo · la macro copia texto, no piensa",
              recompensa="xp 10, oro 10",
              escena="""
                  Tizón talló un sello que marca el **cubo** de un número: `a*a*a`. Con 2 da 8. Con `2+1`… da 7. Toda la partida sale **con forma de banana**.
                  —El sello no piensa —gruñe Ferrum—. **Copia**.
              """,
              sugiere="`CUBO(2+1)` con `a*a*a` se copia como `2+1*2+1*2+1`, que es 7. Con paréntesis en cada `a` y en todo, se copia como `((2+1) * (2+1) * (2+1))`.",
              desafio="Arreglá la macro para que `CUBO(2+1)` dé 27.",
              inicial='''
                  #include <stdio.h>

                  #define CUBO(a) a*a*a

                  int main(void)
                  {
                      printf("CUBO(2+1) = %d\\n", CUBO(2+1));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define CUBO(a) ((a) * (a) * (a))

                  int main(void)
                  {
                      printf("CUBO(2+1) = %d\\n", CUBO(2+1));
                      return 0;
                  }
              ''',
              al_superar="Veintisiete, y ni una banana. En la pared, debajo de la cuenta de espadazos, alguien escribe: «Herraduras banana: 40». Tizón no quiere hablar del tema.",
              imagen=["Una pila de herraduras torcidas con forma de banana.", FERRUM + " sostiene una con dos dedos, mirando a Tizón.", KIRA + " llorando de risa."]),
            m(id="R01-N08-P3", titulo="Cambiar sin una auxiliar a la vista",
              lugar="El taller de marcar", personajes="Kira, Gheco, Chispa",
              carta="Macro SWAP | intercambia dos variables de cualquier tipo · do { … } while (0) la vuelve una sola instrucción · el tipo va como parámetro",
              recompensa="xp 10, oro 10",
              escena="Chispa cambió de lugar los precios de dos piezas «sin querer». Hay que volver a intercambiarlos, y después lo mismo con los pesos (que son decimales).",
              sugiere="`SWAP(tipo, a, b)` usa una variable auxiliar del tipo que le pases: `tipo aux = a; a = b; b = aux;`. Envuelto en `do { … } while (0)` se comporta como una sola instrucción.",
              desafio="Usá la macro para intercambiar los precios y los pesos.",
              inicial='''
                  #include <stdio.h>

                  #define SWAP(tipo, a, b) do { tipo aux_ = (a); (a) = (b); (b) = aux_; } while (0)

                  int main(void)
                  {
                      int precio_espada = 12, precio_escudo = 45;
                      double peso_espada = 6.5, peso_escudo = 2.0;
                      ___;
                      ___;
                      printf("espada: %d lingotes, %.1f kg\\n", precio_espada, peso_espada);
                      printf("escudo: %d lingotes, %.1f kg\\n", precio_escudo, peso_escudo);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define SWAP(tipo, a, b) do { tipo aux_ = (a); (a) = (b); (b) = aux_; } while (0)

                  int main(void)
                  {
                      int precio_espada = 12, precio_escudo = 45;
                      double peso_espada = 6.5, peso_escudo = 2.0;
                      SWAP(int, precio_espada, precio_escudo);
                      SWAP(double, peso_espada, peso_escudo);
                      printf("espada: %d lingotes, %.1f kg\\n", precio_espada, peso_espada);
                      printf("escudo: %d lingotes, %.1f kg\\n", precio_escudo, peso_escudo);
                      return 0;
                  }
              ''',
              al_superar="Todo en su lugar. Chispa jura que fue un error de imprenta. Tizón le muestra que las etiquetas las escribió él, a mano.",
              imagen=["Dos etiquetas de precio que cambian de lugar en el aire.", CHISPA + " silba mirando para otro lado."]),
            m(id="R01-N08-P4", titulo="Modo práctica",
              lugar="El taller de marcar", personajes="Kira, Gheco, Maese Ferrum",
              carta="Compilación condicional | #if / #elif / #else / #endif · #ifdef pregunta si algo está definido · lo que no se cumple ni llega al compilador",
              recompensa="xp 15, oro 15",
              escena="Ferrum quiere una sola receta para el horno, que se compile en «modo práctica» para los aprendices y en «modo forja» para los oficiales. Kira es aprendiz. Por ahora.",
              sugiere="`#if MODO == 1` … `#else` … `#endif` elige qué líneas se compilan según el valor de `MODO`. Lo que no se cumple el compilador ni lo ve.",
              desafio="Completá la condición para que con `MODO` en 1 se compile el modo práctica.",
              inicial='''
                  #include <stdio.h>

                  #define MODO 1

                  int main(void)
                  {
                  ___
                      printf("modo practica: horno a 600 grados\\n");
                  #else
                      printf("modo forja: horno a 1200 grados\\n");
                  #endif
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define MODO 1

                  int main(void)
                  {
                  #if MODO == 1
                      printf("modo practica: horno a 600 grados\\n");
                  #else
                      printf("modo forja: horno a 1200 grados\\n");
                  #endif
                      return 0;
                  }
              ''',
              al_superar="Seiscientos grados. Kira cambia el 1 por un 2 «para ver qué pasa». Ferrum se lo vuelve a cambiar sin decir una palabra.",
              imagen=["Un horno con una perilla de dos posiciones: práctica y forja.", FERRUM + " gira la perilla de vuelta a práctica."]),
        ],
    },
    {
        "titulo": "R01-N09 · Bibliotecas estándar útiles",
        "misiones": [
            m(id="R01-N09-P1", titulo="Cajas que no se parten",
              lugar="El estante de herramientas", personajes="Kira, Gheco, Tizón",
              carta="ceil y floor | ceil redondea hacia arriba · floor hacia abajo · devuelven double · están en math.h",
              recompensa="xp 10, oro 10",
              escena="Kira se pasó una semana fabricando un redondeador casero. Ferrum abre el armario del fondo: en un estante que dice `math.h` ya estaba todo hecho. Hay que mandar 47 clavos en cajas de 10.",
              sugiere="Con `#include <math.h>`: `ceil(x)` redondea **hacia arriba** (las cajas que hacen falta) y `floor(x)`, **hacia abajo** (las que se llenan). Las dos devuelven `double`: se muestran con `%.0f`.",
              desafio="Usá `ceil` y `floor`.",
              inicial='''
                  #include <stdio.h>
                  #include <math.h>

                  int main(void)
                  {
                      double clavos = 47.0;
                      printf("cajas necesarias: %.0f\\n", ___(clavos / 10));
                      printf("cajas llenas: %.0f\\n", ___(clavos / 10));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <math.h>

                  int main(void)
                  {
                      double clavos = 47.0;
                      printf("cajas necesarias: %.0f\\n", ceil(clavos / 10));
                      printf("cajas llenas: %.0f\\n", floor(clavos / 10));
                      return 0;
                  }
              ''',
              al_superar="Cinco cajas, cuatro llenas. Kira guarda su redondeador casero en un cajón, sin hacer comentarios. Tizón le da una palmadita en la espalda.",
              imagen=["Un armario abierto con estantes etiquetados: math.h, ctype.h, stdlib.h.", KIRA + " esconde un artefacto casero detrás de la espalda."]),
            m(id="R01-N09-P2", titulo="La cuenta del alambre",
              lugar="El estante de herramientas", personajes="Kira, Gheco, Tizón",
              carta="math.h | sqrt raíz · pow potencia · fabs valor absoluto · en la terminal se compila con -lm",
              recompensa="xp 10, oro 10",
              escena="Hay que cortar el alambre para la diagonal de un marco de 3 por 4. Tizón lo quiere medir con el calibre; Kira quiere usar el estante.",
              sugiere="Con `#include <math.h>`: `sqrt(x)` es la raíz cuadrada y `pow(b, e)` es b elevado a e. La diagonal es `sqrt(ancho² + alto²)`.",
              desafio="Calculá la diagonal con `sqrt` y `pow`.",
              inicial='''
                  #include <stdio.h>
                  #include <math.h>

                  int main(void)
                  {
                      double ancho = 3.0, alto = 4.0;
                      double diagonal = ___;
                      printf("diagonal: %.1f\\n", diagonal);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <math.h>

                  int main(void)
                  {
                      double ancho = 3.0, alto = 4.0;
                      double diagonal = sqrt(pow(ancho, 2) + pow(alto, 2));
                      printf("diagonal: %.1f\\n", diagonal);
                      return 0;
                  }
              ''',
              al_superar="Cinco. Tizón lo mide con el calibre para comprobar: cinco, exacto. Se queda en silencio, muy impresionado.",
              imagen=["Un marco de hierro de 3 por 4 con un alambre cruzado en diagonal.", TIZON + " mide la diagonal, boquiabierto."]),
            m(id="R01-N09-P3", titulo="Letras al derecho",
              lugar="El estante de herramientas", personajes="Kira, Gheco, Chispa",
              carta="ctype.h y getchar | getchar lee un carácter · toupper devuelve la mayúscula · isdigit pregunta si es un dígito · putchar lo muestra",
              recompensa="xp 10, oro 10",
              escena="Chispa escribió el cartel de su puesto en minúsculas «para ahorrar tinta». Kira lo quiere en mayúsculas, y quiere saber cuántos números tiene.",
              sugiere="`getchar()` lee **un** carácter (devuelve un `int`). Con `#include <ctype.h>`, `toupper(c)` da su mayúscula e `isdigit(c)` dice si es un dígito. `putchar(c)` lo muestra.",
              desafio="Completá el bucle que lee el cartel de a un carácter hasta el fin de la línea.",
              entrada="lingotes a 3 por 5\n",
              inicial='''
                  #include <stdio.h>
                  #include <ctype.h>

                  int main(void)
                  {
                      int c;
                      int digitos = 0;
                      while ((c = getchar()) != '\\n' && c != EOF) {
                          if (___(c)) {
                              digitos++;
                          }
                          putchar(___(c));
                      }
                      printf(" (%d numeros)\\n", digitos);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <ctype.h>

                  int main(void)
                  {
                      int c;
                      int digitos = 0;
                      while ((c = getchar()) != '\\n' && c != EOF) {
                          if (isdigit(c)) {
                              digitos++;
                          }
                          putchar(toupper(c));
                      }
                      printf(" (%d numeros)\\n", digitos);
                      return 0;
                  }
              ''',
              al_superar="LINGOTES A 3 POR 5. Chispa se queja del gasto de tinta. Después ve que vende el doble y se calla.",
              imagen=["Un cartel de madera de un puesto de mercado con letras grandes en mayúscula.", CHISPA + " cuenta monedas detrás del puesto."]),
            m(id="R01-N09-P4", titulo="Los dados de Tizón",
              lugar="La taberna de la Forja", personajes="Kira, Gheco, Tizón",
              carta="Pseudoazar a mano | un número semilla y una cuenta que lo cambia · misma semilla, misma secuencia · rand() hace algo parecido",
              recompensa="xp 15, oro 15",
              escena="Tizón no confía en los dados de hueso de la taberna («nunca caen igual en dos Forjas distintas»). Inventó su propio dado: un número que se transforma con una cuenta cada vez que se tira.",
              sugiere="Un generador simple: `semilla = (semilla * 17 + 5) % 101` en cada tirada, y el dado es `semilla % 6 + 1` (de 1 a 6). Así sale **siempre** la misma secuencia, en cualquier compu. `rand()` hace algo parecido, pero su cuenta cambia según el sistema.",
              desafio="Completá la tirada del dado.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int semilla = 7;
                      for (int tirada = 1; tirada <= 5; tirada++) {
                          semilla = (semilla * 17 + 5) % 101;
                          int dado = ___;
                          printf("tirada %d: %d\\n", tirada, dado);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int semilla = 7;
                      for (int tirada = 1; tirada <= 5; tirada++) {
                          semilla = (semilla * 17 + 5) % 101;
                          int dado = semilla % 6 + 1;
                          printf("tirada %d: %d\\n", tirada, dado);
                      }
                      return 0;
                  }
              ''',
              al_superar="Cinco tiradas que salen igual en cualquier Forja del mundo. Los de la taberna dicen que el dado de Tizón está cargado. Tizón dice que está **medido**.",
              imagen=["Una mesa de taberna con un dado de bronce tallado a mano.", TIZON + " anota cada tirada en la libreta; alrededor, aprendices desconfiados."]),
        ],
    },
    {
        "titulo": "R01-N10 · Jefe: el Gólem de Escoria",
        "misiones": [
            m(id="R01-N10-P1", titulo="La escoria se levanta",
              lugar="El patio de la Forja", personajes="Kira, Gheco, Maese Ferrum",
              criatura="dragon",
              carta="Partir el problema | cada paso en su función · main queda como una receta que se lee",
              recompensa="xp 15, oro 15",
              escena="""
                  En el patio, toda la escoria de la Forja se junta y se levanta: el **Gólem de Escoria**, negro, con grietas de lava y puntos y coma incrustados en el pecho. Algunos pedazos son de la primera semana de Kira.
                  —No lo vas a vencer de un golpe —dice Ferrum—. Partilo.
              """,
              sugiere="Cada parte del combate en su función: `vida_restante(vida, golpe)` devuelve la vida que queda (nunca menos de 0).",
              desafio="Completá la función: si el golpe es mayor que la vida, la vida queda en 0.",
              inicial='''
                  #include <stdio.h>

                  int vida_restante(int vida, int golpe)
                  {
                      ___
                  }

                  int main(void)
                  {
                      int golem = 50;
                      golem = vida_restante(golem, 18);
                      printf("el golem resiste: %d\\n", golem);
                      golem = vida_restante(golem, 40);
                      printf("el golem resiste: %d\\n", golem);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int vida_restante(int vida, int golpe)
                  {
                      if (golpe >= vida) {
                          return 0;
                      }
                      return vida - golpe;
                  }

                  int main(void)
                  {
                      int golem = 50;
                      golem = vida_restante(golem, 18);
                      printf("el golem resiste: %d\\n", golem);
                      golem = vida_restante(golem, 40);
                      printf("el golem resiste: %d\\n", golem);
                      return 0;
                  }
              ''',
              al_superar="El gólem tambalea, pero se vuelve a juntar. En la pared, la cuenta de espadazos sigue en 41 a 0. Kira, por primera vez, no levanta la espada.",
              imagen=["El Gólem de Escoria: un gigante de escoria negra y roca fundida con grietas de lava naranja y puntos y coma incrustados en el pecho.",
                      KIRA + " frente a él, con la espada rajada en la vaina.", FERRUM + " a un costado, con los brazos cruzados."]),
            m(id="R01-N10-P2", titulo="Validar lo que dice el gólem",
              lugar="El patio de la Forja", personajes="Kira, Gheco, Tizón",
              criatura="goblin",
              carta="Validar en un bucle | leer con fgets · sscanf devuelve 1 si era un número · repetir hasta que el dato sirva",
              recompensa="xp 15, oro 15",
              escena="El gólem grita números falsos para confundir: «¡mil!», «¡nada!», «¡-5!». Tizón le pasa a Kira una regla: solo valen los golpes entre 1 y 99.",
              sugiere="Se lee la línea con `fgets` y se interpreta con `sscanf`. Si `sscanf` no devuelve 1 o el número está fuera de rango, se ignora y se lee la siguiente.",
              desafio="Completá la condición para aceptar solo números entre 1 y 99.",
              entrada="mil\nnada\n-5\n42\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[50];
                      int golpe = 0;
                      int ignorados = 0;
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (___) {
                              break;
                          }
                          ignorados++;
                      }
                      printf("golpe valido: %d (ignorados: %d)\\n", golpe, ignorados);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[50];
                      int golpe = 0;
                      int ignorados = 0;
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (sscanf(linea, "%d", &golpe) == 1 && golpe >= 1 && golpe <= 99) {
                              break;
                          }
                          ignorados++;
                      }
                      printf("golpe valido: %d (ignorados: %d)\\n", golpe, ignorados);
                      return 0;
                  }
              ''',
              al_superar="Tres gritos ignorados y un golpe de verdad: cuarenta y dos. El gólem se queda sin trucos. Tizón le guiña un ojo a Kira desde la tribuna.",
              imagen=["El Gólem de Escoria grita números que salen de su boca como chispas.", TIZON + " sostiene un cartel con «1 a 99»."]),
            m(id="R01-N10-P3", titulo="Las placas del pecho",
              lugar="El patio de la Forja", personajes="Kira, Gheco, Maese Ferrum",
              carta="Bucle y decisión | leer en un for · contar las que cumplen · guardar el mayor en la misma vuelta",
              recompensa="xp 15, oro 15",
              escena="El gólem tiene en el pecho ocho placas con números de temple, que Tizón le va dictando a Kira. Solo las placas con temple mayor a 600 resisten; las demás se pueden romper. Kira tiene que saber cuántas son y cuál es la más dura.",
              sugiere="Un `for` lee las ocho placas con `scanf`; en cada vuelta, un `if` cuenta las blandas y otro guarda la más dura (la primera placa arranca como la más dura).",
              entrada="450 720 300 980 610 550 120 800\n",
              desafio="Completá las dos condiciones.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int placa;
                      int blandas = 0;
                      int mas_dura = 0;
                      for (int i = 1; i <= 8; i++) {
                          scanf("%d", &placa);
                          if (___) {
                              blandas++;
                          }
                          if (i == 1 || ___) {
                              mas_dura = placa;
                          }
                      }
                      printf("placas para romper: %d\\n", blandas);
                      printf("la mas dura: %d\\n", mas_dura);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int placa;
                      int blandas = 0;
                      int mas_dura = 0;
                      for (int i = 1; i <= 8; i++) {
                          scanf("%d", &placa);
                          if (placa <= 600) {
                              blandas++;
                          }
                          if (i == 1 || placa > mas_dura) {
                              mas_dura = placa;
                          }
                      }
                      printf("placas para romper: %d\\n", blandas);
                      printf("la mas dura: %d\\n", mas_dura);
                      return 0;
                  }
              ''',
              al_superar="Cuatro placas blandas. Kira las rompe una por una con un martillo chico, sin apuro, sin espadazos. Ferrum anota algo en la pared que Kira no alcanza a leer.",
              imagen=["El pecho del Gólem de Escoria con ocho placas numeradas; cuatro se resquebrajan.", KIRA + " golpea con un martillo chico, concentrada."]),
            m(id="R01-N10-P4", titulo="El gólem cae",
              lugar="El patio de la Forja", personajes="Kira, Gheco, Maese Ferrum, Tizón",
              criatura="dragon",
              carta="Todo junto | funciones + bucle + decisiones · main se lee como una historia · cada pieza en su lugar",
              recompensa="xp 25, oro 30",
              item="Espada Reforjada",
              escena="""
                  Solo queda el corazón del gólem: una piedra de lava con 60 de vida. Kira tiene tres golpes medidos: 15, 25 y 30. Si los aplica en orden, con la función de antes, el gólem cae.
                  —Medí antes de pegar —le dice Tizón, y le pasa la libreta.
              """,
              sugiere="Un bucle lee cada golpe, lo aplica con `vida_restante` y corta (`break`) cuando la vida llega a 0.",
              entrada="15 25 30\n",
              desafio="Completá el bucle y el corte.",
              inicial='''
                  #include <stdio.h>

                  int vida_restante(int vida, int golpe)
                  {
                      return golpe >= vida ? 0 : vida - golpe;
                  }

                  int main(void)
                  {
                      int corazon = 60;
                      int golpe;
                      for (int i = 0; i < 3; i++) {
                          scanf("%d", &golpe);
                          corazon = ___;
                          printf("golpe de %d: le quedan %d\\n", golpe, corazon);
                          if (___) {
                              printf("el golem de escoria cae\\n");
                              break;
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int vida_restante(int vida, int golpe)
                  {
                      return golpe >= vida ? 0 : vida - golpe;
                  }

                  int main(void)
                  {
                      int corazon = 60;
                      int golpe;
                      for (int i = 0; i < 3; i++) {
                          scanf("%d", &golpe);
                          corazon = vida_restante(corazon, golpe);
                          printf("golpe de %d: le quedan %d\\n", golpe, corazon);
                          if (corazon == 0) {
                              printf("el golem de escoria cae\\n");
                              break;
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="El Gólem de Escoria se desarma en una montaña de piedras tibias. Ferrum toma la espada rajada de Kira, la mete al horno y la **reforja** delante de todos. —La próxima —le dice, devolviéndosela— la forjás vos. —La **Espada Reforjada** va a tu mochila. En la pared, la cuenta queda: «Espadazos: 41. Problemas resueltos a espadazos: 0. Gólems: 1».",
              imagen=["El Gólem de Escoria se desarma en una montaña de piedras tibias.",
                      FERRUM + " saca del horno la espada de Kira, reforjada y brillante.",
                      KIRA + " la recibe con las dos manos.", TIZON + " aplaude en la tribuna."]),
        ],
    },
]
