from genc import m
from c_r01 import KIRA, TIZON, FERRUM, CHISPA
from c_r01b import HULDA

PASILLOS = "Los pasillos numerados"
ARANA = "La Araña de las Direcciones (araña gigante de metal pavonado, patas como flechas de cartel, ojos con números hexadecimales, telaraña de hilos de cobre)"

NODOS = [
    {
        "titulo": "R02-N01 · Arrays y matrices",
        "misiones": [
            m(id="R02-N01-P1", titulo="Los estantes desde el cero",
              lugar=PASILLOS, personajes="Kira, Gheco, Tizón",
              criatura="orco",
              carta="Array | int v[5] guarda 5 enteros seguidos · las posiciones van de 0 a 4 · v[5] ya no existe",
              recompensa="xp 10, oro 10",
              escena="""
                  Debajo de la Forja corren los pasillos numerados: estantes de hierro que empiezan en **cero**. Kira, que cuenta desde uno, busca el estante 5 de una hilera de cinco… y encuentra un **orco** durmiendo la siesta.
              """,
              sugiere="`int pesos[5]` tiene los lugares `pesos[0]` a `pesos[4]`. El bucle va de `i = 0` mientras `i < 5`: con `<=` se pasa uno y despierta al orco.",
              desafio="Arreglá el bucle para recorrer solo los cinco estantes.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int pesos[5] = { 12, 7, 30, 18, 9 };
                      int total = 0;
                      for (int i = 1; i <= 5; i++) {
                          total += pesos[i];
                      }
                      printf("peso total: %d kg\\n", total);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int pesos[5] = { 12, 7, 30, 18, 9 };
                      int total = 0;
                      for (int i = 0; i < 5; i++) {
                          total += pesos[i];
                      }
                      printf("peso total: %d kg\\n", total);
                      return 0;
                  }
              ''',
              al_superar="Setenta y seis kilos, y el orco sigue durmiendo. Kira se aleja en puntas de pie.",
              imagen=["Un pasillo de piedra con cinco estantes de hierro numerados del 0 al 4, y un sexto hueco sin número.",
                      "Un orco grande duerme en el hueco.", KIRA + " retrocede en puntas de pie."]),
            m(id="R02-N01-P2", titulo="El estante más pesado",
              lugar=PASILLOS, personajes="Kira, Gheco, Tizón",
              carta="Buscar el mayor | arrancar con el primero · recorrer comparando · guardar también DÓNDE estaba",
              recompensa="xp 10, oro 10",
              escena="Tizón quiere saber qué estante carga más, y **cuál** es, para reforzarlo. Con el peso solo no le alcanza.",
              sugiere="Se arranca con el primero como el mayor (`mayor = v[0]`, `donde = 0`) y se recorre desde el 1: si uno supera al mayor, se guardan su valor y su posición.",
              desafio="Completá la comparación y lo que se guarda.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int pesos[6] = { 12, 7, 30, 18, 9, 25 };
                      int mayor = pesos[0];
                      int donde = 0;
                      for (int i = 1; i < 6; i++) {
                          if (___) {
                              mayor = pesos[i];
                              donde = ___;
                          }
                      }
                      printf("el estante %d carga %d kg\\n", donde, mayor);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int pesos[6] = { 12, 7, 30, 18, 9, 25 };
                      int mayor = pesos[0];
                      int donde = 0;
                      for (int i = 1; i < 6; i++) {
                          if (pesos[i] > mayor) {
                              mayor = pesos[i];
                              donde = i;
                          }
                      }
                      printf("el estante %d carga %d kg\\n", donde, mayor);
                      return 0;
                  }
              ''',
              al_superar="El estante 2. Tizón le pone un puntal de hierro, lo mide, y le pone otro, por las dudas.",
              imagen=["Una hilera de estantes con bolsas de distinto tamaño; uno se combea por el peso.", TIZON + " coloca un puntal de hierro."]),
            m(id="R02-N01-P3", titulo="La tabla de los hornos",
              lugar=PASILLOS, personajes="Kira, Gheco, Maese Ferrum",
              carta="Matriz | int t[3][4]: 3 filas, 4 columnas · t[fila][columna] · dos bucles anidados la recorren",
              recompensa="xp 10, oro 10",
              escena="Ferrum anota la temperatura de 4 hornos durante 3 días, en una tabla. Quiere el promedio de cada **horno** (cada columna), no de cada día.",
              sugiere="En `t[dia][horno]`, el promedio de un horno suma **una columna**: el bucle de afuera recorre los hornos y el de adentro, los días.",
              desafio="Completá la suma de la columna.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int t[3][4] = {
                          { 800, 950, 700, 1000 },
                          { 820, 900, 720, 1100 },
                          { 860, 910, 680, 1060 },
                      };
                      for (int horno = 0; horno < 4; horno++) {
                          int suma = 0;
                          for (int dia = 0; dia < 3; dia++) {
                              suma += ___;
                          }
                          printf("horno %d: promedio %.1f\\n", horno + 1, suma / 3.0);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int t[3][4] = {
                          { 800, 950, 700, 1000 },
                          { 820, 900, 720, 1100 },
                          { 860, 910, 680, 1060 },
                      };
                      for (int horno = 0; horno < 4; horno++) {
                          int suma = 0;
                          for (int dia = 0; dia < 3; dia++) {
                              suma += t[dia][horno];
                          }
                          printf("horno %d: promedio %.1f\\n", horno + 1, suma / 3.0);
                      }
                      return 0;
                  }
              ''',
              al_superar="El horno 4 es el más caliente. Ferrum lo sospechaba: ahí se le quemaron las cejas.",
              imagen=["Una pizarra con una tabla de 3 filas y 4 columnas de temperaturas.", FERRUM + " señala la cuarta columna."]),
            m(id="R02-N01-P4", titulo="Contadores en un array",
              lugar=PASILLOS, personajes="Kira, Gheco, Tizón",
              carta="Array de contadores | cuenta[valor]++ · el dato es el índice · inicializar todo en 0 con = { 0 }",
              recompensa="xp 15, oro 15",
              escena="Tizón tiró su dado medido veinte veces y anotó cada resultado. Quiere saber cuántas veces salió cada número del 1 al 6, «para demostrar que no está cargado».",
              sugiere="Un array de contadores usa el **dato como índice**: `cuenta[dado]++`. Con 7 lugares, del 1 al 6 se usan tal cual (el 0 queda sin usar). `= { 0 }` pone todo en cero.",
              desafio="Completá la línea que cuenta.",
              entrada="3 6 1 4 6 2 5 6 3 1 2 6 4 5 3 6 1 2 4 5\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int cuenta[7] = { 0 };
                      int dado;
                      for (int i = 0; i < 20; i++) {
                          scanf("%d", &dado);
                          ___;
                      }
                      for (int cara = 1; cara <= 6; cara++) {
                          printf("el %d salio %d veces\\n", cara, cuenta[cara]);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int cuenta[7] = { 0 };
                      int dado;
                      for (int i = 0; i < 20; i++) {
                          scanf("%d", &dado);
                          cuenta[dado]++;
                      }
                      for (int cara = 1; cara <= 6; cara++) {
                          printf("el %d salio %d veces\\n", cara, cuenta[cara]);
                      }
                      return 0;
                  }
              ''',
              al_superar="El 6 salió cinco veces. Tizón dice que es casualidad. Los de la taberna dicen que no. La discusión sigue hasta hoy.",
              imagen=["Seis montoncitos de piedritas, uno por cara de un dado, el del 6 más alto.", TIZON + " defiende su dado frente a aprendices desconfiados."]),
        ],
    },
    {
        "titulo": "R02-N02 · Strings (textos)",
        "misiones": [
            m(id="R02-N02-P1", titulo="OROHIERRO",
              lugar="El mostrador de etiquetas", personajes="Kira, Gheco, Chispa",
              criatura="orco",
              carta="El '\\0' | un texto termina en '\\0' · \"ORO\" ocupa 4 bytes · el array tiene que tener lugar para el tapón",
              recompensa="xp 10, oro 10",
              escena="""
                  Chispa etiqueta un lingote con «ORO» en una placa de **tres** casilleros. El lector sigue de largo hasta la placa de al lado y el lingote de hierro se vende como «OROHIERRO».
                  Tizón lo descubre a la media hora. Chispa jura que fue sin querer.
              """,
              sugiere="Un texto en C es un array de `char` que termina en `'\\0'`. `\"ORO\"` necesita **4** lugares: tres letras y el tapón. Con `char etiqueta[3]`, no entra.",
              desafio="Dale a la etiqueta el tamaño justo para «ORO» y su tapón.",
              inicial='''
                  #include <stdio.h>
                  #include <string.h>

                  int main(void)
                  {
                      char etiqueta[___];
                      strcpy(etiqueta, "ORO");
                      printf("etiqueta: %s (%zu letras, %zu bytes)\\n", etiqueta, strlen(etiqueta), sizeof etiqueta);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <string.h>

                  int main(void)
                  {
                      char etiqueta[4];
                      strcpy(etiqueta, "ORO");
                      printf("etiqueta: %s (%zu letras, %zu bytes)\\n", etiqueta, strlen(etiqueta), sizeof etiqueta);
                      return 0;
                  }
              ''',
              al_superar="ORO, tres letras, cuatro bytes. Chispa vuelve a etiquetar todos los lingotes. Tizón los revisa uno por uno.",
              imagen=["Dos placas de hierro pegadas: «ORO» y «HIERRO», sin separación.", "Un orco chiquito sale de la unión entre las dos placas.", CHISPA + " con cara de inocente."]),
            m(id="R02-N02-P2", titulo="No se compara con ==",
              lugar="El mostrador de etiquetas", personajes="Kira, Gheco, Tizón",
              criatura="ogro",
              carta="strcmp | strcmp(a, b) da 0 si son iguales · negativo si a va antes · positivo si va después · == compara direcciones, no letras",
              recompensa="xp 10, oro 10",
              escena="Kira busca la caja de Tizón comparando nombres con `==`. Nunca la encuentra, aunque está ahí, con su nombre escrito clarito.",
              sugiere="Con textos, `==` compara **dónde están** guardados, no las letras. `strcmp(a, b) == 0` pregunta si tienen las mismas letras.",
              desafio="Cambiá la comparación.",
              inicial='''
                  #include <stdio.h>
                  #include <string.h>

                  int main(void)
                  {
                      char caja[10] = "Tizon";
                      char buscado[10] = "Tizon";
                      if (caja == buscado) {
                          printf("encontrada\\n");
                      } else {
                          printf("no esta\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <string.h>

                  int main(void)
                  {
                      char caja[10] = "Tizon";
                      char buscado[10] = "Tizon";
                      if (strcmp(caja, buscado) == 0) {
                          printf("encontrada\\n");
                      } else {
                          printf("no esta\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="Encontrada. Adentro de la caja de Tizón hay otra libreta, más chica, con las medidas de la libreta grande.",
              imagen=["Una pared de cajas etiquetadas; una dice Tizon.", KIRA + " abre la caja y encuentra una libreta más chica."]),
            m(id="R02-N02-P3", titulo="El nombre con espacios",
              lugar="El mostrador de etiquetas", personajes="Kira, Gheco, Chispa",
              carta="fgets y el \\n | fgets lee la línea con espacios · deja el '\\n' al final · strcspn(s, \"\\n\") encuentra dónde está para borrarlo",
              recompensa="xp 10, oro 10",
              escena="Chispa quiere que su etiqueta diga «Chispa el Veloz», con espacios. `scanf(\"%s\")` se corta en el primer espacio. `fgets` lo lee entero, pero trae un salto de línea de regalo.",
              sugiere="`fgets(s, sizeof s, stdin)` lee la línea entera, con el `'\\n'`. `s[strcspn(s, \"\\n\")] = '\\0';` lo cambia por el fin de texto.",
              desafio="Sacale el salto de línea al nombre.",
              entrada="Chispa el Veloz\n",
              inicial='''
                  #include <stdio.h>
                  #include <string.h>

                  int main(void)
                  {
                      char nombre[40];
                      fgets(nombre, sizeof nombre, stdin);
                      ___
                      printf("[%s] tiene %zu letras\\n", nombre, strlen(nombre));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <string.h>

                  int main(void)
                  {
                      char nombre[40];
                      fgets(nombre, sizeof nombre, stdin);
                      nombre[strcspn(nombre, "\\n")] = '\\0';
                      printf("[%s] tiene %zu letras\\n", nombre, strlen(nombre));
                      return 0;
                  }
              ''',
              al_superar="[Chispa el Veloz], quince letras. Chispa la manda a grabar en bronce. Tizón le cobra la medición.",
              imagen=["Una placa de bronce con «Chispa el Veloz» grabado.", CHISPA + " posa al lado, orgulloso."]),
            m(id="R02-N02-P4", titulo="Armar el cartel",
              lugar="El mostrador de etiquetas", personajes="Kira, Gheco, Tizón",
              carta="Armar textos | strcpy copia · strcat agrega al final · snprintf arma con formato sin pasarse del tamaño",
              recompensa="xp 15, oro 15",
              escena="Tizón quiere un cartel para la puerta de cada taller: el oficio, un guion y el nombre. Kira lo arma pegando pedazos.",
              sugiere="`snprintf(destino, sizeof destino, \"%s - %s\", a, b)` arma el texto con formato **sin pasarse** del tamaño del array. Es la forma segura.",
              desafio="Armá el cartel con `snprintf`.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char oficio[] = "Herreria";
                      char nombre[] = "Maese Ferrum";
                      char cartel[30];
                      ___;
                      printf("%s\\n", cartel);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char oficio[] = "Herreria";
                      char nombre[] = "Maese Ferrum";
                      char cartel[30];
                      snprintf(cartel, sizeof cartel, "%s - %s", oficio, nombre);
                      printf("%s\\n", cartel);
                      return 0;
                  }
              ''',
              al_superar="«Herreria - Maese Ferrum». Ferrum lo clava en la puerta y lo mira un rato largo. Es la primera vez que tiene cartel.",
              imagen=["Un cartel de madera recién clavado en una puerta de hierro: Herreria - Maese Ferrum.", TIZON + " le alcanza los clavos a Kira."]),
        ],
    },
    {
        "titulo": "R02-N03 · Structs, enum, typedef y union",
        "misiones": [
            m(id="R02-N03-P1", titulo="La ficha de hierro",
              lugar="El depósito de fichas", personajes="Kira, Gheco, Maese Ferrum",
              carta="struct | agrupa datos de distinto tipo · se accede con el punto: f.nombre · typedef le da un nombre corto",
              recompensa="xp 10, oro 10",
              escena="Antes había una lista de nombres, otra de vidas y otra de fuerzas. Un día alguien ordenó una y no las otras, y Kira quedó con la vida de Tizón durante una semana. Ferrum manda hacer **fichas**.",
              sugiere="`typedef struct { … } Aprendiz;` define un tipo con varios campos. Cada campo se usa con el punto: `kira.vida`.",
              desafio="Completá los campos que faltan en la ficha.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      ___
                      ___
                  } Aprendiz;

                  int main(void)
                  {
                      Aprendiz kira = { "Kira", 90, 15 };
                      printf("%s: vida %d, fuerza %d\\n", kira.nombre, kira.vida, kira.fuerza);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                      int fuerza;
                  } Aprendiz;

                  int main(void)
                  {
                      Aprendiz kira = { "Kira", 90, 15 };
                      printf("%s: vida %d, fuerza %d\\n", kira.nombre, kira.vida, kira.fuerza);
                      return 0;
                  }
              ''',
              al_superar="Una ficha, todo junto. Ya nadie le puede cambiar la vida a Kira por ordenar otra lista. Kira se siente aliviada; Tizón, un poco menos medido.",
              imagen=["Una ficha de hierro con campos grabados: nombre, vida, fuerza.", FERRUM + " cuelga la ficha en un tablero."]),
            m(id="R02-N03-P2", titulo="El oficio con nombre",
              lugar="El depósito de fichas", personajes="Kira, Gheco, Tizón",
              carta="enum | enum { HERRERO, MINERA, MERCADER } · son enteros con nombre (0, 1, 2) · se leen mejor que números sueltos",
              recompensa="xp 10, oro 10",
              escena="En las fichas viejas el oficio era un número: 0, 1 o 2. Nadie se acordaba cuál era cuál y Chispa figuraba como «minero».",
              sugiere="Un `enum` pone nombre a cada valor: `HERRERO` vale 0, `MINERA` 1 y `MERCADER` 2. Un `switch` puede usarlos en los `case`.",
              desafio="Completá los `case` del `switch` con los nombres del `enum`.",
              inicial='''
                  #include <stdio.h>

                  typedef enum { HERRERO, MINERA, MERCADER } Oficio;

                  const char *nombre_oficio(Oficio o)
                  {
                      switch (o) {
                      case ___: return "herrero";
                      case ___: return "minera";
                      case ___: return "mercader";
                      }
                      return "?";
                  }

                  int main(void)
                  {
                      printf("Tizon: %s\\n", nombre_oficio(HERRERO));
                      printf("Hulda: %s\\n", nombre_oficio(MINERA));
                      printf("Chispa: %s\\n", nombre_oficio(MERCADER));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef enum { HERRERO, MINERA, MERCADER } Oficio;

                  const char *nombre_oficio(Oficio o)
                  {
                      switch (o) {
                      case HERRERO: return "herrero";
                      case MINERA: return "minera";
                      case MERCADER: return "mercader";
                      }
                      return "?";
                  }

                  int main(void)
                  {
                      printf("Tizon: %s\\n", nombre_oficio(HERRERO));
                      printf("Hulda: %s\\n", nombre_oficio(MINERA));
                      printf("Chispa: %s\\n", nombre_oficio(MERCADER));
                      return 0;
                  }
              ''',
              al_superar="Chispa, mercader. Por fin. Hulda se queja de que la sacaron de «minero» y la pusieron en «minera». Le gustaba más el error.",
              imagen=["Tres fichas de hierro con oficios grabados: herrero, minera, mercader.", HULDA + " mira su ficha con desconfianza."]),
            m(id="R02-N03-P3", titulo="Fichas dentro de fichas",
              lugar="El depósito de fichas", personajes="Kira, Gheco, Hulda",
              carta="Structs anidados | un campo puede ser otro struct · se llega con dos puntos: h.pos.x · se copian enteros con =",
              recompensa="xp 10, oro 10",
              escena="Hulda quiere saber **dónde** está cada minero: cada ficha necesita una posición en la mina (galería y profundidad). Y quiere poder mover a alguien de lugar sin rehacer la ficha.",
              sugiere="Un struct puede tener otro struct adentro: `minero.pos.galeria`. Para mover, se cambian los campos de la posición.",
              desafio="Mové a Tizon a la galería 3, profundidad 40.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int galeria;
                      int profundidad;
                  } Posicion;

                  typedef struct {
                      char nombre[12];
                      Posicion pos;
                  } Minero;

                  int main(void)
                  {
                      Minero tizon = { "Tizon", { 1, 10 } };
                      ___
                      ___
                      printf("%s esta en la galeria %d, a %d metros\\n", tizon.nombre, tizon.pos.galeria, tizon.pos.profundidad);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int galeria;
                      int profundidad;
                  } Posicion;

                  typedef struct {
                      char nombre[12];
                      Posicion pos;
                  } Minero;

                  int main(void)
                  {
                      Minero tizon = { "Tizon", { 1, 10 } };
                      tizon.pos.galeria = 3;
                      tizon.pos.profundidad = 40;
                      printf("%s esta en la galeria %d, a %d metros\\n", tizon.nombre, tizon.pos.galeria, tizon.pos.profundidad);
                      return 0;
                  }
              ''',
              al_superar="Galería 3, cuarenta metros. Tizón baja, mide la profundidad con una soga, y vuelve: cuarenta metros y dos centímetros. Lo deja pasar.",
              imagen=["Un mapa de la mina con galerías numeradas y una ficha clavada en la galería 3.", HULDA + " señala el mapa con el pico."]),
            m(id="R02-N03-P4", titulo="PARA QUIEN LLEGUE",
              lugar="El depósito de fichas", personajes="Kira, Gheco, Tizón",
              carta="union | sus campos comparten la misma memoria · un número y sus bytes son lo mismo visto distinto · en las PC, el byte de menor peso va primero",
              recompensa="xp 15, oro 15",
              escena="""
                  La ficha del pedido de plomo tiene un campo raro: un número que, según Ferrum, «no pesa nada que tenga sentido». Kira sospecha que hay que leerlo **de otra forma**.
              """,
              sugiere="En un `union`, los campos ocupan el **mismo lugar**. Si se guarda un número en `valor`, `letras[0]` … `letras[3]` son sus cuatro bytes, empezando por el de menor peso (*little endian*).",
              desafio="Mostrá los cuatro bytes del número como letras.",
              inicial='''
                  #include <stdio.h>
                  #include <stdint.h>

                  typedef union {
                      uint32_t valor;
                      char letras[4];
                  } Marca;

                  int main(void)
                  {
                      Marca m;
                      m.valor = 1095909712u;
                      printf("como numero: %u\\n", m.valor);
                      printf("como letras: ");
                      for (int i = 0; i < 4; i++) {
                          putchar(___);
                      }
                      printf("\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdint.h>

                  typedef union {
                      uint32_t valor;
                      char letras[4];
                  } Marca;

                  int main(void)
                  {
                      Marca m;
                      m.valor = 1095909712u;
                      printf("como numero: %u\\n", m.valor);
                      printf("como letras: ");
                      for (int i = 0; i < 4; i++) {
                          putchar(m.letras[i]);
                      }
                      printf("\\n");
                      return 0;
                  }
              ''',
              al_superar="«PARA». La primera palabra. Kira revisa el resto de los campos de la ficha, uno por uno, de la misma manera: «PARA QUIEN LLEGUE». Tizón se sienta en el piso, sin medir nada, por primera vez en su vida.",
              imagen=["Una ficha de hierro vieja con números grabados, y encima, en luz cian, las letras PARA QUIEN LLEGUE.",
                      KIRA + " sostiene la ficha contra la luz de una antorcha.", TIZON + " sentado en el piso, sin el calibre en la mano."]),
        ],
    },
    {
        "titulo": "R02-N04 · Punteros",
        "misiones": [
            m(id="R02-N04-P1", titulo="El cartel que señala",
              lugar=PASILLOS, personajes="Kira, Gheco, Tizón",
              carta="Puntero | int *p = &x guarda DÓNDE está x · *p es el valor de lo apuntado · cambiar *p cambia x",
              recompensa="xp 10, oro 10",
              escena="En los pasillos hay **carteles** que no guardan nada: señalan dónde está cada cosa. Tizón quiere cambiar la carga de un estante sin ir hasta él: le alcanza con tirar del cartel.",
              sugiere="`&carga` es la dirección de `carga`. Un puntero la guarda: `int *cartel = &carga;`. Con `*cartel = 50;` se cambia lo apuntado.",
              desafio="Completá el puntero y el cambio a través de él.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int carga = 20;
                      int *cartel = ___;
                      ___ = 50;
                      printf("carga del estante: %d\\n", carga);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int carga = 20;
                      int *cartel = &carga;
                      *cartel = 50;
                      printf("carga del estante: %d\\n", carga);
                      return 0;
                  }
              ''',
              al_superar="Cincuenta, sin moverse del lugar. Tizón tira de todos los carteles del pasillo para comprobar que andan. Andan.",
              imagen=["Un cartel de hierro con una flecha que se estira como un hilo de cobre hasta un estante lejano.", TIZON + " tira del cartel."]),
            m(id="R02-N04-P2", titulo="El cartel a ninguna parte",
              lugar=PASILLOS, personajes="Kira, Gheco, Hulda",
              criatura="troll",
              carta="NULL | un puntero que no apunta a nada vale NULL · antes de usarlo, preguntar if (p != NULL) · *NULL rompe el programa",
              recompensa="xp 15, oro 15",
              item="Amuleto del Volcado",
              escena="""
                  Kira sigue un cartel que dice «por acá» con toda la confianza del mundo. El cartel no apuntaba a nada: Kira cae por un hueco, el programa revienta y en la pared queda escrito *Violación de segmento*.
                  Hulda la saca con una soga.
              """,
              sugiere="Un puntero que no apunta a nada vale `NULL`. Usar `*p` con `p == NULL` rompe el programa. Siempre se pregunta antes: `if (p != NULL)`.",
              desafio="Protegé la lectura: si el cartel es `NULL`, avisá en lugar de seguirlo.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int tesoro = 7;
                      int *carteles[2] = { &tesoro, NULL };
                      for (int i = 0; i < 2; i++) {
                          printf("cartel %d: hay %d lingotes\\n", i, *carteles[i]);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int tesoro = 7;
                      int *carteles[2] = { &tesoro, NULL };
                      for (int i = 0; i < 2; i++) {
                          if (carteles[i] != NULL) {
                              printf("cartel %d: hay %d lingotes\\n", i, *carteles[i]);
                          } else {
                              printf("cartel %d: no apunta a nada\\n", i);
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Hulda le cuelga a Kira un amuleto al cuello. —El **Amuleto del Volcado**: guarda lo que pasó antes de cada caída. Para la próxima que te caigas, que va a haber. —El amuleto va a tu mochila.",
              imagen=["Un hueco oscuro en el piso del pasillo, al lado de un cartel que apunta al vacío.",
                      HULDA + " levanta a " + KIRA + " con una soga.", "Un amuleto con forma de gota de lava brilla en la mano de Hulda."]),
            m(id="R02-N04-P3", titulo="Intercambiar de verdad",
              lugar=PASILLOS, personajes="Kira, Gheco, Chispa",
              carta="Punteros como parámetros | void f(int *a) recibe la dirección · *a = … cambia la variable de quien llama · se llama con f(&x)",
              recompensa="xp 10, oro 10",
              escena="Chispa intercambió dos estantes con una función que trabajaba con copias. Los estantes, claro, siguen igual. Él dice que «en su compu andaba».",
              sugiere="Para que una función cambie variables de afuera, recibe sus **direcciones** (`int *a, int *b`) y cambia `*a` y `*b`. Se llama con `intercambiar(&x, &y)`.",
              desafio="Completá la función y la llamada.",
              inicial='''
                  #include <stdio.h>

                  void intercambiar(int *a, int *b)
                  {
                      int aux = ___;
                      *a = ___;
                      ___ = aux;
                  }

                  int main(void)
                  {
                      int estante_a = 12, estante_b = 30;
                      intercambiar(___, ___);
                      printf("a: %d, b: %d\\n", estante_a, estante_b);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  void intercambiar(int *a, int *b)
                  {
                      int aux = *a;
                      *a = *b;
                      *b = aux;
                  }

                  int main(void)
                  {
                      int estante_a = 12, estante_b = 30;
                      intercambiar(&estante_a, &estante_b);
                      printf("a: %d, b: %d\\n", estante_a, estante_b);
                      return 0;
                  }
              ''',
              al_superar="Ahora sí, intercambiados. Chispa dice que esa era su idea desde el principio.",
              imagen=["Dos estantes que cambian de lugar en el aire, unidos por hilos de cobre.", CHISPA + " se atribuye el mérito."]),
            m(id="R02-N04-P4", titulo="Avanzar por los estantes",
              lugar=PASILLOS, personajes="Kira, Gheco, Tizón",
              carta="Aritmética de punteros | p + 1 es el SIGUIENTE elemento (no el siguiente byte) · *(p + i) es lo mismo que p[i] · el nombre del array es la dirección del primero",
              recompensa="xp 15, oro 15",
              escena="Tizón descubre que puede recorrer el pasillo moviendo el cartel, sin contar estantes: cada `+ 1` lo lleva al siguiente, mida lo que mida cada uno.",
              sugiere="Si `p` apunta a `v[0]`, `p + 1` apunta a `v[1]`: C avanza de a **un elemento**. `*(p + i)` es `v[i]`.",
              desafio="Recorré los pesos con el puntero, sin corchetes.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int pesos[4] = { 5, 12, 8, 20 };
                      int *p = pesos;
                      int total = 0;
                      for (int i = 0; i < 4; i++) {
                          total += ___;
                      }
                      printf("total: %d, el ultimo pesa %d\\n", total, ___);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int pesos[4] = { 5, 12, 8, 20 };
                      int *p = pesos;
                      int total = 0;
                      for (int i = 0; i < 4; i++) {
                          total += *(p + i);
                      }
                      printf("total: %d, el ultimo pesa %d\\n", total, *(p + 3));
                      return 0;
                  }
              ''',
              al_superar="Cuarenta y cinco. Tizón recorre el pasillo moviendo el cartel de un lado a otro, fascinado, hasta que Hulda le pide que pare.",
              imagen=["Un cartel que salta de estante en estante dejando una estela de luz cian.", TIZON + " lo mueve con un dedo, fascinado."]),
        ],
    },
    {
        "titulo": "R02-N05 · Punteros y structs",
        "misiones": [
            m(id="R02-N05-P1", titulo="Mandar el cartel, no la copia",
              lugar="El taller de fichas", personajes="Kira, Gheco, Maese Ferrum",
              carta="Struct por puntero | void f(Aprendiz *a) · a->vida es (*a).vida · cambia la ficha original",
              recompensa="xp 10, oro 10",
              escena="Kira manda su ficha al taller para que le suban la fuerza, y vuelve igual: el taller cambió una **copia**. —Es como fundir otra espada cada vez que querés afilarla —dice Ferrum—. Mandá el cartel.",
              sugiere="Con `Aprendiz *a`, la función recibe la dirección de la ficha. `a->fuerza` es el campo de la ficha original. Se llama con `entrenar(&kira)`.",
              desafio="Hacé que `entrenar` reciba un puntero y cambie la ficha original.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int fuerza;
                  } Aprendiz;

                  void entrenar(Aprendiz a)
                  {
                      a.fuerza += 5;
                  }

                  int main(void)
                  {
                      Aprendiz kira = { "Kira", 15 };
                      entrenar(kira);
                      printf("%s: fuerza %d\\n", kira.nombre, kira.fuerza);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int fuerza;
                  } Aprendiz;

                  void entrenar(Aprendiz *a)
                  {
                      a->fuerza += 5;
                  }

                  int main(void)
                  {
                      Aprendiz kira = { "Kira", 15 };
                      entrenar(&kira);
                      printf("%s: fuerza %d\\n", kira.nombre, kira.fuerza);
                      return 0;
                  }
              ''',
              al_superar="Fuerza 20. Kira flexiona el brazo. Ferrum le recuerda que la fuerza no se usa contra portones.",
              imagen=["Una ficha de hierro unida por un hilo de cobre a un taller donde un enano la martilla.", KIRA + " flexiona el brazo."]),
            m(id="R02-N05-P2", titulo="La carta a la dirección de la carta",
              lugar="El taller de fichas", personajes="Kira, Gheco, Tizón, Hulda",
              criatura="esqueleto",
              carta="Punto o flecha | con el struct: h.vida · con un puntero: p->vida · usar . con un puntero no compila",
              recompensa="xp 10, oro 10",
              escena="Tizón manda un cartel a la ficha de Hulda… pero confunde el **punto** con la **flecha** y el Horno no quiere saber nada. Hulda todavía no sabe si reírse.",
              sugiere="Con la variable struct se usa el punto: `hulda.vida`. Con un **puntero** a struct, la flecha: `p->vida`.",
              desafio="Corregí los accesos: uno es una variable y el otro, un puntero.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                  } Minero;

                  int main(void)
                  {
                      Minero hulda = { "Hulda", 120 };
                      Minero *p = &hulda;
                      p.vida -= 20;
                      printf("%s: vida %d\\n", hulda->nombre, hulda.vida);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                  } Minero;

                  int main(void)
                  {
                      Minero hulda = { "Hulda", 120 };
                      Minero *p = &hulda;
                      p->vida -= 20;
                      printf("%s: vida %d\\n", hulda.nombre, hulda.vida);
                      return 0;
                  }
              ''',
              al_superar="Cien de vida. Hulda decide reírse. Tizón anota: «Punto: la cosa. Flecha: el cartel a la cosa».",
              imagen=["Una carta con una flecha dibujada que apunta a sí misma.", HULDA + " se ríe a carcajadas.", TIZON + " anota en la libreta, colorado."]),
            m(id="R02-N05-P3", titulo="La función que solo mira",
              lugar="El taller de fichas", personajes="Kira, Gheco, Chispa",
              carta="const con punteros | void mostrar(const Ficha *f) · puede leer, no cambiar · evita copiar structs grandes",
              recompensa="xp 10, oro 10",
              escena="Chispa pidió ver la ficha de un lingote «solo para mirar», y le bajó el precio a la mitad. Ferrum quiere una ventanilla que muestre pero **no deje tocar**.",
              sugiere="Con `const Ficha *f`, la función recibe la dirección (no copia la ficha entera) pero el compilador **no deja** cambiarla. Mostrar sí.",
              desafio="Agregá `const` al parámetro y completá lo que muestra.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      char metal[12];
                      int precio;
                  } Ficha;

                  void mostrar(___ Ficha *f)
                  {
                      printf("%s: %d lingotes\\n", ___, ___);
                  }

                  int main(void)
                  {
                      Ficha oro = { "oro", 40 };
                      mostrar(&oro);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      char metal[12];
                      int precio;
                  } Ficha;

                  void mostrar(const Ficha *f)
                  {
                      printf("%s: %d lingotes\\n", f->metal, f->precio);
                  }

                  int main(void)
                  {
                      Ficha oro = { "oro", 40 };
                      mostrar(&oro);
                      return 0;
                  }
              ''',
              al_superar="Cuarenta lingotes, y nadie lo puede cambiar desde la ventanilla. Chispa intenta igual. El Horno le contesta con un error.",
              imagen=["Una ventanilla con un vidrio grueso: detrás, una ficha de oro.", CHISPA + " con la nariz pegada al vidrio."]),
            m(id="R02-N05-P4", titulo="El más herido",
              lugar="El taller de fichas", personajes="Kira, Gheco, Hulda",
              carta="Devolver un puntero | Minero *mas_herido(Minero v[], int n) · devuelve la dirección del elemento · quien llama lo cambia directo",
              recompensa="xp 15, oro 15",
              escena="Después de un derrumbe, Hulda tiene vendas para uno solo: para el más herido de la cuadrilla. Quiere una función que le **señale** a quién, para curarlo ahí mismo.",
              sugiere="La función recorre el array y devuelve `&v[i]` del de menos vida. Con ese puntero, `herido->vida += 30` cura al original.",
              desafio="Completá el puntero que se devuelve y la cura.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                  } Minero;

                  Minero *mas_herido(Minero v[], int n)
                  {
                      Minero *peor = &v[0];
                      for (int i = 1; i < n; i++) {
                          if (v[i].vida < peor->vida) {
                              peor = ___;
                          }
                      }
                      return peor;
                  }

                  int main(void)
                  {
                      Minero cuadrilla[3] = { { "Tizon", 60 }, { "Kira", 25 }, { "Chispa", 40 } };
                      Minero *herido = mas_herido(cuadrilla, 3);
                      ___;
                      for (int i = 0; i < 3; i++) {
                          printf("%s: %d\\n", cuadrilla[i].nombre, cuadrilla[i].vida);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                  } Minero;

                  Minero *mas_herido(Minero v[], int n)
                  {
                      Minero *peor = &v[0];
                      for (int i = 1; i < n; i++) {
                          if (v[i].vida < peor->vida) {
                              peor = &v[i];
                          }
                      }
                      return peor;
                  }

                  int main(void)
                  {
                      Minero cuadrilla[3] = { { "Tizon", 60 }, { "Kira", 25 }, { "Chispa", 40 } };
                      Minero *herido = mas_herido(cuadrilla, 3);
                      herido->vida += 30;
                      for (int i = 0; i < 3; i++) {
                          printf("%s: %d\\n", cuadrilla[i].nombre, cuadrilla[i].vida);
                      }
                      return 0;
                  }
              ''',
              al_superar="Kira, de 25 a 55. Hulda le venda el brazo con un nudo de minera. —La próxima, no te pongas adelante del derrumbe.",
              imagen=["Una cuadrilla de mineros sentados entre piedras después de un derrumbe.", HULDA + " venda el brazo de " + KIRA + "."]),
        ],
    },
    {
        "titulo": "R02-N06 · Arrays de structs",
        "misiones": [
            m(id="R02-N06-P1", titulo="El estante de fichas",
              lugar="El registro de la Forja", personajes="Kira, Gheco, Tizón",
              carta="Array de structs | Aprendiz v[10]; · v[i].nombre · una cantidad aparte dice cuántos hay cargados",
              recompensa="xp 10, oro 10",
              escena="El registro de la Forja es un estante con lugar para diez fichas, pero hoy hay cuatro. Tizón quiere el listado y el promedio de fuerza, sin contar los lugares vacíos.",
              sugiere="Un array de structs se recorre igual que cualquier array, hasta la **cantidad** cargada (no hasta el tamaño): `v[i].fuerza`.",
              desafio="Completá el recorrido y la suma.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int fuerza;
                  } Aprendiz;

                  int main(void)
                  {
                      Aprendiz registro[10] = { { "Kira", 20 }, { "Tizon", 14 }, { "Hulda", 30 }, { "Chispa", 8 } };
                      int cantidad = 4;
                      int suma = 0;
                      for (int i = 0; i < ___; i++) {
                          printf("%-7s %3d\\n", registro[i].nombre, registro[i].fuerza);
                          suma += ___;
                      }
                      printf("promedio: %.2f\\n", (double) suma / cantidad);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int fuerza;
                  } Aprendiz;

                  int main(void)
                  {
                      Aprendiz registro[10] = { { "Kira", 20 }, { "Tizon", 14 }, { "Hulda", 30 }, { "Chispa", 8 } };
                      int cantidad = 4;
                      int suma = 0;
                      for (int i = 0; i < cantidad; i++) {
                          printf("%-7s %3d\\n", registro[i].nombre, registro[i].fuerza);
                          suma += registro[i].fuerza;
                      }
                      printf("promedio: %.2f\\n", (double) suma / cantidad);
                      return 0;
                  }
              ''',
              al_superar="Promedio 18. Chispa queda último en fuerza y propone que la tabla se ordene «por simpatía».",
              imagen=["Un estante con diez lugares y cuatro fichas colgadas.", TIZON + " suma con el lápiz."]),
            m(id="R02-N06-P2", titulo="Buscar por legajo",
              lugar="El registro de la Forja", personajes="Kira, Gheco, Maese Ferrum",
              carta="Buscar | recorrer comparando el campo clave · devolver la posición o -1 si no está · -1 es «no está»",
              recompensa="xp 10, oro 10",
              escena="Ferrum busca a un aprendiz por su número de legajo. Si no existe, quiere un aviso, no un aprendiz cualquiera.",
              sugiere="La función recorre y devuelve la **posición** donde está el legajo, o `-1` si no lo encuentra. Quien la llama pregunta si dio `-1`.",
              desafio="Completá la comparación y lo que se devuelve si no está.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int legajo;
                      char nombre[12];
                  } Aprendiz;

                  int buscar(const Aprendiz v[], int n, int legajo)
                  {
                      for (int i = 0; i < n; i++) {
                          if (___) {
                              return i;
                          }
                      }
                      return ___;
                  }

                  int main(void)
                  {
                      Aprendiz v[3] = { { 101, "Kira" }, { 102, "Tizon" }, { 105, "Hulda" } };
                      int buscados[2] = { 105, 103 };
                      for (int k = 0; k < 2; k++) {
                          int pos = buscar(v, 3, buscados[k]);
                          if (pos == -1) {
                              printf("legajo %d: no existe\\n", buscados[k]);
                          } else {
                              printf("legajo %d: %s\\n", buscados[k], v[pos].nombre);
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int legajo;
                      char nombre[12];
                  } Aprendiz;

                  int buscar(const Aprendiz v[], int n, int legajo)
                  {
                      for (int i = 0; i < n; i++) {
                          if (v[i].legajo == legajo) {
                              return i;
                          }
                      }
                      return -1;
                  }

                  int main(void)
                  {
                      Aprendiz v[3] = { { 101, "Kira" }, { 102, "Tizon" }, { 105, "Hulda" } };
                      int buscados[2] = { 105, 103 };
                      for (int k = 0; k < 2; k++) {
                          int pos = buscar(v, 3, buscados[k]);
                          if (pos == -1) {
                              printf("legajo %d: no existe\\n", buscados[k]);
                          } else {
                              printf("legajo %d: %s\\n", buscados[k], v[pos].nombre);
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="El 103 no existe. Chispa jura que es el suyo. Ferrum le recuerda que Chispa no es aprendiz: es un problema.",
              imagen=["Un fichero de hierro con legajos numerados.", FERRUM + " sostiene una ficha y mira a Chispa de reojo."]),
            m(id="R02-N06-P3", titulo="Burbuja con desempate",
              lugar="El registro de la Forja", personajes="Kira, Gheco, Tizón",
              carta="Ordenar con desempate | una función va_antes(a, b) · primero el promedio (mayor primero) · si empatan, strcmp del nombre",
              recompensa="xp 15, oro 15",
              escena="Ferrum quiere el cuadro de honor por temple de mayor a menor y, si empatan, por nombre. Kira los ordenó por altura. Tizón quedó primero por tercera vez y nadie le cree.",
              sugiere="`va_antes` decide el orden: si los promedios son distintos, va antes el mayor; si empatan, el que va antes alfabéticamente (`strcmp(a, b) < 0`). La burbuja intercambia cuando el de la derecha `va_antes` que el de la izquierda.",
              desafio="Completá el desempate.",
              inicial='''
                  #include <stdio.h>
                  #include <string.h>
                  #include <stdbool.h>

                  typedef struct {
                      char nombre[12];
                      int temple;
                  } Aprendiz;

                  bool va_antes(const Aprendiz *a, const Aprendiz *b)
                  {
                      if (a->temple != b->temple) {
                          return a->temple > b->temple;
                      }
                      return ___;
                  }

                  int main(void)
                  {
                      Aprendiz v[4] = { { "Tizon", 8 }, { "Kira", 9 }, { "Hulda", 8 }, { "Chispa", 5 } };
                      for (int pasada = 0; pasada < 3; pasada++) {
                          for (int i = 0; i < 3 - pasada; i++) {
                              if (va_antes(&v[i + 1], &v[i])) {
                                  Aprendiz aux = v[i];
                                  v[i] = v[i + 1];
                                  v[i + 1] = aux;
                              }
                          }
                      }
                      for (int i = 0; i < 4; i++) {
                          printf("%d. %s (%d)\\n", i + 1, v[i].nombre, v[i].temple);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <string.h>
                  #include <stdbool.h>

                  typedef struct {
                      char nombre[12];
                      int temple;
                  } Aprendiz;

                  bool va_antes(const Aprendiz *a, const Aprendiz *b)
                  {
                      if (a->temple != b->temple) {
                          return a->temple > b->temple;
                      }
                      return strcmp(a->nombre, b->nombre) < 0;
                  }

                  int main(void)
                  {
                      Aprendiz v[4] = { { "Tizon", 8 }, { "Kira", 9 }, { "Hulda", 8 }, { "Chispa", 5 } };
                      for (int pasada = 0; pasada < 3; pasada++) {
                          for (int i = 0; i < 3 - pasada; i++) {
                              if (va_antes(&v[i + 1], &v[i])) {
                                  Aprendiz aux = v[i];
                                  v[i] = v[i + 1];
                                  v[i + 1] = aux;
                              }
                          }
                      }
                      for (int i = 0; i < 4; i++) {
                          printf("%d. %s (%d)\\n", i + 1, v[i].nombre, v[i].temple);
                      }
                      return 0;
                  }
              ''',
              al_superar="Kira primera; Hulda y Tizón empatados, en orden alfabético. Tizón pide que lo midan de nuevo. Lo miden. Sigue tercero.",
              imagen=["El cuadro de honor de la Forja colgado en la pared, con cuatro nombres.", TIZON + " pide que lo midan, con el calibre en la mano."]),
            m(id="R02-N06-P4", titulo="El autómata que ordena",
              lugar="El registro de la Forja", personajes="Kira, Gheco, Maese Ferrum",
              carta="qsort | qsort(v, n, sizeof v[0], comparar) · comparar recibe const void * · devuelve <0, 0 o >0, como strcmp",
              recompensa="xp 15, oro 15",
              escena="Ferrum saca de un cajón un autómata de bronce que ordena cualquier cosa… si le explicás cómo comparar. Kira tiene que escribir esa explicación para ordenar los lingotes por precio.",
              sugiere="`qsort` necesita una función `int comparar(const void *a, const void *b)`. Adentro se convierten: `const Lingote *x = a;` y se devuelve `x->precio - y->precio` (negativo si va antes).",
              desafio="Completá la comparación.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct {
                      char metal[10];
                      int precio;
                  } Lingote;

                  int comparar(const void *a, const void *b)
                  {
                      const Lingote *x = a;
                      const Lingote *y = b;
                      return ___;
                  }

                  int main(void)
                  {
                      Lingote v[4] = { { "oro", 40 }, { "hierro", 5 }, { "plomo", 9 }, { "cobre", 12 } };
                      qsort(v, 4, sizeof v[0], comparar);
                      for (int i = 0; i < 4; i++) {
                          printf("%-7s %3d\\n", v[i].metal, v[i].precio);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  typedef struct {
                      char metal[10];
                      int precio;
                  } Lingote;

                  int comparar(const void *a, const void *b)
                  {
                      const Lingote *x = a;
                      const Lingote *y = b;
                      return x->precio - y->precio;
                  }

                  int main(void)
                  {
                      Lingote v[4] = { { "oro", 40 }, { "hierro", 5 }, { "plomo", 9 }, { "cobre", 12 } };
                      qsort(v, 4, sizeof v[0], comparar);
                      for (int i = 0; i < 4; i++) {
                          printf("%-7s %3d\\n", v[i].metal, v[i].precio);
                      }
                      return 0;
                  }
              ''',
              al_superar="Del más barato al más caro. El autómata de bronce hace una reverencia y vuelve solo a su cajón. Kira juraría que guiñó un ojo.",
              imagen=["Un autómata de bronce chiquito ordenando lingotes sobre una mesa.", FERRUM + " lo mira con cariño de abuelo."]),
        ],
    },
    {
        "titulo": "R02-N07 · Jefe: la Araña de las Direcciones",
        "misiones": [
            m(id="R02-N07-P1", titulo="Los carteles falsos",
              lugar="La Arena de los pasillos", personajes="Kira, Gheco, Tizón",
              criatura="dragon",
              carta="Seguir punteros | un puntero puede apuntar a otro puntero · **pp llega al valor · anotar cada dirección antes de seguirla",
              recompensa="xp 15, oro 15",
              escena="""
                  En la Arena, la **Araña de las Direcciones** teje carteles que apuntan a otros carteles. Kira, por primera vez, no tira el primer golpe: saca la libreta de Tizón y sigue los hilos de a uno.
              """,
              sugiere="Un puntero a puntero (`int **pp`) guarda la dirección de otro puntero. `*pp` es el puntero del medio y `**pp`, el valor del final.",
              desafio="Seguí los dos carteles hasta el tesoro.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int tesoro = 99;
                      int *cartel = &tesoro;
                      int **cartel_al_cartel = &cartel;
                      printf("el tesoro vale %d\\n", ___);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int tesoro = 99;
                      int *cartel = &tesoro;
                      int **cartel_al_cartel = &cartel;
                      printf("el tesoro vale %d\\n", **cartel_al_cartel);
                      return 0;
                  }
              ''',
              al_superar="Noventa y nueve. La Araña cambia los carteles de lugar, furiosa. Kira ya los tiene anotados.",
              imagen=[ARANA + " teje carteles que apuntan a otros carteles.", KIRA + " anota en la libreta de Tizón, concentrada."]),
            m(id="R02-N07-P2", titulo="La red de la Araña",
              lugar="La Arena de los pasillos", personajes="Kira, Gheco, Hulda",
              criatura="orco",
              carta="No pasarse | recorrer hasta la cantidad · comprobar el índice antes de usarlo · la Araña vive del lugar que sigue al último",
              recompensa="xp 15, oro 15",
              escena="La Araña tiende su red justo después del último lugar del array: espera que alguien lea uno de más. Hulda le pasa a Kira una regla: «antes de pisar, contá».",
              sugiere="Antes de usar `v[pos]`, se comprueba `pos >= 0 && pos < n`. Si no, se avisa y no se toca.",
              desafio="Completá la comprobación.",
              entrada="2 5 -1 0\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int pociones[4] = { 30, 15, 50, 10 };
                      int n = 4;
                      int pos;
                      for (int k = 0; k < 4; k++) {
                          scanf("%d", &pos);
                          if (___) {
                              printf("pocion %d: cura %d\\n", pos, pociones[pos]);
                          } else {
                              printf("pocion %d: es la red de la arania\\n", pos);
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int pociones[4] = { 30, 15, 50, 10 };
                      int n = 4;
                      int pos;
                      for (int k = 0; k < 4; k++) {
                          scanf("%d", &pos);
                          if (pos >= 0 && pos < n) {
                              printf("pocion %d: cura %d\\n", pos, pociones[pos]);
                          } else {
                              printf("pocion %d: es la red de la arania\\n", pos);
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Dos trampas esquivadas. La Araña sube por su tela, nerviosa, y cambia de estrategia.",
              imagen=["Una red de cobre tendida después del último estante de una hilera.", HULDA + " sostiene una regla de madera."]),
            m(id="R02-N07-P3", titulo="El hilo que cambia todo",
              lugar="La Arena de los pasillos", personajes="Kira, Gheco, Tizón",
              carta="Funciones con punteros a struct | la función recibe Luchador * · cambia vida del original · devuelve si sigue en pie",
              recompensa="xp 15, oro 15",
              escena="La Araña muerde y envenena: cada turno le saca vida a quien muerde. Kira escribe un turno que actúa sobre las fichas **originales**, con carteles.",
              sugiere="`void morder(Luchador *atacante, Luchador *victima)` resta el ataque de uno a la vida del otro con `->`. La vida no baja de 0.",
              desafio="Completá la mordida.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                      int ataque;
                  } Luchador;

                  void morder(const Luchador *atacante, Luchador *victima)
                  {
                      victima->vida -= ___;
                      if (victima->vida < 0) {
                          victima->vida = 0;
                      }
                  }

                  int main(void)
                  {
                      Luchador arania = { "Arania", 80, 12 };
                      Luchador kira = { "Kira", 50, 30 };
                      morder(&arania, &kira);
                      morder(&kira, &arania);
                      morder(&kira, &arania);
                      printf("%s: %d, %s: %d\\n", kira.nombre, kira.vida, arania.nombre, arania.vida);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      char nombre[12];
                      int vida;
                      int ataque;
                  } Luchador;

                  void morder(const Luchador *atacante, Luchador *victima)
                  {
                      victima->vida -= atacante->ataque;
                      if (victima->vida < 0) {
                          victima->vida = 0;
                      }
                  }

                  int main(void)
                  {
                      Luchador arania = { "Arania", 80, 12 };
                      Luchador kira = { "Kira", 50, 30 };
                      morder(&arania, &kira);
                      morder(&kira, &arania);
                      morder(&kira, &arania);
                      printf("%s: %d, %s: %d\\n", kira.nombre, kira.vida, arania.nombre, arania.vida);
                      return 0;
                  }
              ''',
              al_superar="Kira con 38, la Araña con 20. Tizón, en la tribuna, se emociona tanto que se le cae el calibre.",
              imagen=[ARANA + " retrocede herida.", KIRA + " con el escudo en alto."]),
            m(id="R02-N07-P4", titulo="La Araña se enreda",
              lugar="La Arena de los pasillos", personajes="Kira, Gheco, Tizón, Maese Ferrum",
              criatura="dragon",
              carta="Todo junto | array de structs + punteros + funciones · recorrer y cambiar por dirección · cada pieza en su lugar",
              recompensa="xp 25, oro 30",
              item="Hilo de las Direcciones",
              escena="""
                  La Araña tiene cuatro patas sanas y una vida enorme. Kira anotó en la libreta qué golpe va a cada pata. Si los aplica en orden, sobre las patas **originales**, la Araña se enreda en su propia tela.
              """,
              sugiere="`golpear(&patas[i], golpe)` cambia la pata original. Al final se cuentan las patas con resistencia 0.",
              desafio="Completá la llamada y la cuenta de patas rotas.",
              entrada="25 40 18 30\n",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int numero;
                      int resistencia;
                  } Pata;

                  void golpear(Pata *p, int golpe)
                  {
                      p->resistencia = golpe >= p->resistencia ? 0 : p->resistencia - golpe;
                  }

                  int main(void)
                  {
                      Pata patas[4] = { { 1, 25 }, { 2, 35 }, { 3, 20 }, { 4, 30 } };
                      int rotas = 0;
                      for (int i = 0; i < 4; i++) {
                          int golpe;
                          scanf("%d", &golpe);
                          golpear(___, golpe);
                          printf("pata %d: queda %d\\n", patas[i].numero, patas[i].resistencia);
                          if (___) {
                              rotas++;
                          }
                      }
                      printf("patas rotas: %d de 4\\n", rotas);
                      if (rotas >= 3) {
                          printf("la arania se enreda en su propia tela\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int numero;
                      int resistencia;
                  } Pata;

                  void golpear(Pata *p, int golpe)
                  {
                      p->resistencia = golpe >= p->resistencia ? 0 : p->resistencia - golpe;
                  }

                  int main(void)
                  {
                      Pata patas[4] = { { 1, 25 }, { 2, 35 }, { 3, 20 }, { 4, 30 } };
                      int rotas = 0;
                      for (int i = 0; i < 4; i++) {
                          int golpe;
                          scanf("%d", &golpe);
                          golpear(&patas[i], golpe);
                          printf("pata %d: queda %d\\n", patas[i].numero, patas[i].resistencia);
                          if (patas[i].resistencia == 0) {
                              rotas++;
                          }
                      }
                      printf("patas rotas: %d de 4\\n", rotas);
                      if (rotas >= 3) {
                          printf("la arania se enreda en su propia tela\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="La Araña de las Direcciones queda colgando de su propia tela, enredada en carteles que apuntan a sí mismos. De la tela, Kira saca un hilo de cobre que **siempre sabe adónde va**: el **Hilo de las Direcciones**, que va a tu mochila. En la ficha del pedido de plomo, una última línea: el plomo salió **de las Minas**.",
              imagen=[ARANA + " colgando enredada en su propia tela.",
                      KIRA + " enrolla un hilo de cobre brillante en la mano.", TIZON + " y " + FERRUM + " en la tribuna; Tizón levanta el calibre."]),
        ],
    },
]
