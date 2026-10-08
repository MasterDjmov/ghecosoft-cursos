from genc import m
from c_r01 import KIRA, TIZON, FERRUM, CHISPA
from c_r01b import HULDA

TEMPLE = "La Prueba del Temple"

NODOS = [
    {
        "titulo": "R05-N01 · Depuración",
        "misiones": [
            m(id="R05-N01-P1", titulo="La pieza que suena hueca",
              lugar=TEMPLE, personajes="Kira, Gheco, Maese Ferrum",
              criatura="ogro",
              carta="Error de lógica | compila y corre, pero el resultado está mal · mirar los valores paso a paso · el depurador frena en la línea justa",
              recompensa="xp 10, oro 10",
              escena="""
                  La primera sala está llena de piezas que parecen perfectas. Kira le grita a una espada que no anda. Ferrum la aparta, golpea cada pieza con un martillito y **escucha** dónde suena hueca.
                  —No hace falta gritarle —dice—. Hace falta frenarla en la línea justa.
              """,
              sugiere="El promedio de 4 notas da 7 y no 7.5: la división se hace con dos enteros. Seguilo línea por línea (o con un `printf` de depuración): ¿qué valor tiene la división antes de guardarse?",
              desafio="Arreglá el promedio sin cambiar las notas.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int notas[4] = { 8, 7, 9, 6 };
                      int suma = 0;
                      for (int i = 0; i < 4; i++) {
                          suma += notas[i];
                      }
                      double promedio = suma / 4;
                      printf("promedio: %.2f\\n", promedio);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int notas[4] = { 8, 7, 9, 6 };
                      int suma = 0;
                      for (int i = 0; i < 4; i++) {
                          suma += notas[i];
                      }
                      double promedio = suma / 4.0;
                      printf("promedio: %.2f\\n", promedio);
                      return 0;
                  }
              ''',
              al_superar="7,50. La pieza suena maciza. Ferrum guarda el martillito sin decir nada; Kira entiende que eso es un elogio.",
              imagen=["Una sala oscura llena de espadas colgadas; una tiene una grieta fina que brilla.", FERRUM + " golpea una espada con un martillito y escucha."]),
            m(id="R05-N01-P2", titulo="El que nunca entra",
              lugar=TEMPLE, personajes="Kira, Gheco, Tizón",
              criatura="ogro",
              carta="= contra == | if (x = 0) ASIGNA y da falso · if (x == 0) compara · -Wall avisa: «suggest parentheses»",
              recompensa="xp 10, oro 10",
              escena="Tizón escribió un control que dice «stock agotado» cuando el stock es 0. Nunca lo dice. Y después de pasar por el control, el stock de todo queda en 0.",
              sugiere="`if (stock = 0)` **guarda** 0 en `stock` y la condición vale 0 (falso). Para comparar se usa `==`. El compilador lo avisa con `-Wall`: leé las advertencias.",
              desafio="Corregí la comparación.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int stocks[3] = { 5, 0, 12 };
                      for (int i = 0; i < 3; i++) {
                          int stock = stocks[i];
                          if (stock = 0) {
                              printf("pieza %d: agotada\\n", i);
                          } else {
                              printf("pieza %d: quedan %d\\n", i, stock);
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int stocks[3] = { 5, 0, 12 };
                      for (int i = 0; i < 3; i++) {
                          int stock = stocks[i];
                          if (stock == 0) {
                              printf("pieza %d: agotada\\n", i);
                          } else {
                              printf("pieza %d: quedan %d\\n", i, stock);
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Ahora sí avisa, y el stock no desaparece. Tizón se promete leer **todas** las advertencias. Las anota en la libreta, para medirlas.",
              imagen=["Un cartel de stock que muestra ceros en todas las filas, tachado.", TIZON + " lee una advertencia amarilla del Horno."]),
            m(id="R05-N01-P3", titulo="La variable sin valor",
              lugar=TEMPLE, personajes="Kira, Gheco, Hulda",
              criatura="ogro",
              carta="Sin inicializar | una variable local empieza con basura · el acumulador va en 0 ANTES del bucle · -Wall a veces lo avisa",
              recompensa="xp 10, oro 10",
              escena="Hulda suma las cargas del día con un programa que a veces da bien y a veces da cualquier cosa, según el día. —En mi compu anda —dice. Ferrum: —«En mi compu anda» no alcanza.",
              sugiere="Una variable local sin valor inicial tiene **basura**: lo que quedó en esa memoria. El acumulador tiene que arrancar en 0.",
              desafio="Inicializá el acumulador.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int cargas[4] = { 120, 80, 200, 50 };
                      int total___;
                      for (int i = 0; i < 4; i++) {
                          total += cargas[i];
                      }
                      printf("total del dia: %d kg\\n", total);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int cargas[4] = { 120, 80, 200, 50 };
                      int total = 0;
                      for (int i = 0; i < 4; i++) {
                          total += cargas[i];
                      }
                      printf("total del dia: %d kg\\n", total);
                      return 0;
                  }
              ''',
              al_superar="Cuatrocientos cincuenta, todos los días igual. Hulda le pone un cero bien grande al principio de la tablilla, para no olvidarse más.",
              imagen=["Una tablilla de minera con un cero enorme escrito al principio.", HULDA + " lo remarca con tiza."]),
            m(id="R05-N01-P4", titulo="Uno de menos",
              lugar=TEMPLE, personajes="Kira, Gheco, Tizón",
              criatura="ogro",
              carta="Off by one | contar desde 1 pide <= · contar desde 0 pide < · probá con el primero y el último a mano",
              recompensa="xp 15, oro 15",
              escena="Tizón suma el carbón de los 7 días de la semana y le da de menos. Lo revisa tres veces con el calibre: el carbón está, el que falta es un **día**.",
              sugiere="Si el contador arranca en 1, para llegar al 7 la condición es `dia <= 7`. Con `< 7` se queda en el 6: le falta uno. Probá a mano la primera y la última vuelta.",
              desafio="Corregí el límite para que se cuenten los 7 días.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int total = 0;
                      int dias = 0;
                      for (int dia = 1; dia < 7; dia++) {
                          total += 10 * dia;
                          dias++;
                      }
                      printf("%d dias, %d bolsas de carbon\\n", dias, total);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int total = 0;
                      int dias = 0;
                      for (int dia = 1; dia <= 7; dia++) {
                          total += 10 * dia;
                          dias++;
                      }
                      printf("%d dias, %d bolsas de carbon\\n", dias, total);
                      return 0;
                  }
              ''',
              al_superar="Siete días, doscientas ochenta bolsas. Tizón le pone nombre al domingo en la libreta para no volver a perderlo.",
              imagen=["Un calendario de piedra con siete días; el último estaba tapado con una tela.", TIZON + " destapa el domingo, aliviado."]),
        ],
    },
    {
        "titulo": "R05-N02 · Tests",
        "misiones": [
            m(id="R05-N02-P1", titulo="El martillo de prueba",
              lugar=TEMPLE, personajes="Kira, Gheco, Tizón",
              carta="Un mini framework | una macro PROBAR(cond) cuenta y muestra la línea que falla · al final, cuántas pasaron",
              recompensa="xp 10, oro 10",
              escena="La segunda sala está llena de martillos de prueba. Tizón entra, ve los martillos y los calibres, y se emociona hasta las lágrimas: por fin alguien le **pide** que mida todo.",
              sugiere="`PROBAR(cond)` suma 1 a las pruebas y, si `cond` es falsa, muestra la línea (`__LINE__`). Si es verdadera, suma 1 a las que pasaron.",
              desafio="Completá la macro: si la condición se cumple, cuenta una que pasó.",
              inicial='''
                  #include <stdio.h>

                  static int pruebas = 0, pasaron = 0;
                  #define PROBAR(cond) do { pruebas++; if (cond) { ___; } else { printf("falla en la linea %d\\n", __LINE__); } } while (0)

                  int maximo(int a, int b)
                  {
                      return a > b ? a : b;
                  }

                  int main(void)
                  {
                      PROBAR(maximo(3, 7) == 7);
                      PROBAR(maximo(7, 3) == 7);
                      PROBAR(maximo(-2, -9) == -2);
                      PROBAR(maximo(4, 4) == 4);
                      printf("%d de %d pruebas pasaron\\n", pasaron, pruebas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  static int pruebas = 0, pasaron = 0;
                  #define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\\n", __LINE__); } } while (0)

                  int maximo(int a, int b)
                  {
                      return a > b ? a : b;
                  }

                  int main(void)
                  {
                      PROBAR(maximo(3, 7) == 7);
                      PROBAR(maximo(7, 3) == 7);
                      PROBAR(maximo(-2, -9) == -2);
                      PROBAR(maximo(4, 4) == 4);
                      printf("%d de %d pruebas pasaron\\n", pasaron, pruebas);
                      return 0;
                  }
              ''',
              al_superar="Cuatro de cuatro. Tizón prueba cada pieza tres veces. Después, por las dudas, una cuarta.",
              imagen=["Una sala con martillos de prueba colgados y una pizarra que dice 4/4.", TIZON + " llorando de emoción con un calibre en cada mano."]),
            m(id="R05-N02-P2", titulo="Probar en los bordes",
              lugar=TEMPLE, personajes="Kira, Gheco, Maese Ferrum",
              criatura="ogro",
              carta="Casos límite | probar el 0, el máximo, el mínimo, el borde exacto · los errores viven en los bordes",
              recompensa="xp 15, oro 15",
              escena="—No se prueba donde la espada es fuerte —dice Ferrum—. Se prueba en los bordes. —La función que clasifica la temperatura anda con 500 y con 1100… y falla justo en 800.",
              sugiere="Las pruebas del borde (800 exacto) muestran el error: «templada» empieza **en** 800, así que la comparación es `>=`.",
              desafio="Corregí la función para que pasen las cinco pruebas.",
              inicial='''
                  #include <stdio.h>
                  #include <string.h>

                  static int pruebas = 0, pasaron = 0;
                  #define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\\n", __LINE__); } } while (0)

                  const char *estado(int grados)
                  {
                      if (grados > 1200) {
                          return "quemada";
                      }
                      if (grados > 800) {
                          return "templada";
                      }
                      return "fria";
                  }

                  int main(void)
                  {
                      PROBAR(strcmp(estado(500), "fria") == 0);
                      PROBAR(strcmp(estado(799), "fria") == 0);
                      PROBAR(strcmp(estado(800), "templada") == 0);
                      PROBAR(strcmp(estado(1200), "templada") == 0);
                      PROBAR(strcmp(estado(1201), "quemada") == 0);
                      printf("%d de %d pruebas pasaron\\n", pasaron, pruebas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <string.h>

                  static int pruebas = 0, pasaron = 0;
                  #define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\\n", __LINE__); } } while (0)

                  const char *estado(int grados)
                  {
                      if (grados > 1200) {
                          return "quemada";
                      }
                      if (grados >= 800) {
                          return "templada";
                      }
                      return "fria";
                  }

                  int main(void)
                  {
                      PROBAR(strcmp(estado(500), "fria") == 0);
                      PROBAR(strcmp(estado(799), "fria") == 0);
                      PROBAR(strcmp(estado(800), "templada") == 0);
                      PROBAR(strcmp(estado(1200), "templada") == 0);
                      PROBAR(strcmp(estado(1201), "quemada") == 0);
                      printf("%d de %d pruebas pasaron\\n", pasaron, pruebas);
                      return 0;
                  }
              ''',
              al_superar="Cinco de cinco. Ferrum golpea el yunque dos veces. Kira, esta vez, sabe exactamente qué significa.",
              imagen=["Un termómetro de cobre con una marca en 800 que brilla.", FERRUM + " golpea el yunque dos veces."]),
            m(id="R05-N02-P3", titulo="Primero la prueba",
              lugar=TEMPLE, personajes="Kira, Gheco, Tizón",
              carta="Primero la prueba | escribir las pruebas antes de la función · al principio fallan · se programa hasta que pasen",
              recompensa="xp 15, oro 15",
              escena="Tizón propone algo raro: escribir las pruebas **antes** que la función. Las pruebas de `es_bisiesto` ya están; la función no.",
              sugiere="Un año es bisiesto si es divisible por 4, salvo los divisibles por 100, que solo lo son si también son divisibles por 400.",
              desafio="Escribí `es_bisiesto` hasta que pasen las cinco pruebas.",
              inicial='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  static int pruebas = 0, pasaron = 0;
                  #define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\\n", __LINE__); } } while (0)

                  bool es_bisiesto(int anio)
                  {
                      ___
                  }

                  int main(void)
                  {
                      PROBAR(es_bisiesto(2024));
                      PROBAR(!es_bisiesto(2023));
                      PROBAR(!es_bisiesto(1900));
                      PROBAR(es_bisiesto(2000));
                      PROBAR(es_bisiesto(2028));
                      printf("%d de %d pruebas pasaron\\n", pasaron, pruebas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdbool.h>

                  static int pruebas = 0, pasaron = 0;
                  #define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\\n", __LINE__); } } while (0)

                  bool es_bisiesto(int anio)
                  {
                      return (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
                  }

                  int main(void)
                  {
                      PROBAR(es_bisiesto(2024));
                      PROBAR(!es_bisiesto(2023));
                      PROBAR(!es_bisiesto(1900));
                      PROBAR(es_bisiesto(2000));
                      PROBAR(es_bisiesto(2028));
                      printf("%d de %d pruebas pasaron\\n", pasaron, pruebas);
                      return 0;
                  }
              ''',
              al_superar="Cinco de cinco, al tercer intento. Tizón anota la fecha y la hora exacta en que pasaron todas. Con minutos y segundos.",
              imagen=["Una pizarra con cinco pruebas escritas antes que la función; las cinco con un tilde verde.", TIZON + " anota la hora en la libreta."]),
            m(id="R05-N02-P4", titulo="La prueba que encuentra al ogro",
              lugar=TEMPLE, personajes="Kira, Gheco, Chispa",
              criatura="ogro",
              carta="Una prueba para cada error | cuando aparece un error, primero se escribe la prueba que lo muestra · después se arregla · así no vuelve",
              recompensa="xp 15, oro 15",
              escena="Chispa encontró un error en la balanza del Gremio y, por primera vez en su vida, el error es **en contra suya**: con 1999 centavos y 10 % de descuento le cobran 1799 en vez de 1800. Antes de arreglarlo, Kira escribe la prueba que lo muestra.",
              sugiere="La regla del Gremio: el descuento es el 10 % del precio, en centavos enteros y **redondeado para abajo** (`centavos / 10`), y se resta. Con 1999, el descuento es 199 y se paga 1800. La cuenta `centavos * 9 / 10` redondea el precio final para abajo y da 1799.",
              desafio="Arreglá la función para que pase la prueba nueva sin romper las otras.",
              inicial='''
                  #include <stdio.h>

                  static int pruebas = 0, pasaron = 0;
                  #define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\\n", __LINE__); } } while (0)

                  int con_descuento(int centavos)
                  {
                      return centavos * 9 / 10;
                  }

                  int main(void)
                  {
                      PROBAR(con_descuento(1000) == 900);
                      PROBAR(con_descuento(500) == 450);
                      PROBAR(con_descuento(1999) == 1800);
                      printf("%d de %d pruebas pasaron\\n", pasaron, pruebas);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  static int pruebas = 0, pasaron = 0;
                  #define PROBAR(cond) do { pruebas++; if (cond) { pasaron++; } else { printf("falla en la linea %d\\n", __LINE__); } } while (0)

                  int con_descuento(int centavos)
                  {
                      int descuento = centavos / 10;
                      return centavos - descuento;
                  }

                  int main(void)
                  {
                      PROBAR(con_descuento(1000) == 900);
                      PROBAR(con_descuento(500) == 450);
                      PROBAR(con_descuento(1999) == 1800);
                      printf("%d de %d pruebas pasaron\\n", pasaron, pruebas);
                      return 0;
                  }
              ''',
              al_superar="Tres de tres. Chispa recupera su centavo y lo festeja como un tesoro. Después calcula cuántos centavos ganó en toda su vida con los errores **a su favor** y prefiere no decirlo en voz alta.",
              imagen=["Una balanza de bronce con un centavo de cobre que vuelve volando a la mano de un cliente.", CHISPA + " pálido, haciendo cuentas."]),
        ],
    },
    {
        "titulo": "R05-N03 · Proyecto: la agenda del Gremio",
        "misiones": [
            m(id="R05-N03-P1", titulo="Un teléfono sin letras",
              lugar="La sede del Gremio", personajes="Kira, Gheco, Chispa",
              carta="Validar un texto | recorrer letra por letra · isdigit, el espacio y el + valen · al menos 6 dígitos",
              recompensa="xp 10, oro 10",
              escena="Los comerciantes del Gremio pierden los teléfonos de sus proveedores. Chispa es el primero en probar la agenda: carga su teléfono como «llamame».",
              sugiere="Se recorre el texto: cada carácter tiene que ser un dígito, un espacio o un `+`, y tiene que haber al menos 6 dígitos.",
              desafio="Completá la condición de carácter inválido.",
              inicial='''
                  #include <stdio.h>
                  #include <ctype.h>
                  #include <stdbool.h>

                  bool telefono_valido(const char *t)
                  {
                      int digitos = 0;
                      for (int i = 0; t[i] != '\\0'; i++) {
                          if (isdigit((unsigned char) t[i])) {
                              digitos++;
                          } else if (___) {
                              return false;
                          }
                      }
                      return digitos >= 6;
                  }

                  int main(void)
                  {
                      const char *pruebas[4] = { "380 4223344", "llamame", "+54 380 1", "12345" };
                      for (int i = 0; i < 4; i++) {
                          printf("%-12s %s\\n", pruebas[i], telefono_valido(pruebas[i]) ? "valido" : "invalido");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <ctype.h>
                  #include <stdbool.h>

                  bool telefono_valido(const char *t)
                  {
                      int digitos = 0;
                      for (int i = 0; t[i] != '\\0'; i++) {
                          if (isdigit((unsigned char) t[i])) {
                              digitos++;
                          } else if (t[i] != ' ' && t[i] != '+') {
                              return false;
                          }
                      }
                      return digitos >= 6;
                  }

                  int main(void)
                  {
                      const char *pruebas[4] = { "380 4223344", "llamame", "+54 380 1", "12345" };
                      for (int i = 0; i < 4; i++) {
                          printf("%-12s %s\\n", pruebas[i], telefono_valido(pruebas[i]) ? "valido" : "invalido");
                      }
                      return 0;
                  }
              ''',
              al_superar="«llamame», inválido. Chispa intenta «el de siempre». También. Al final lo carga bien, y es la primera vez que alguien en las Forjas tiene el teléfono de Chispa.",
              imagen=["Una agenda de cuero con renglones; uno dice «llamame» tachado en rojo.", CHISPA + " escribe su teléfono de verdad, a regañadientes."]),
            m(id="R05-N03-P2", titulo="Buscar sin importar mayúsculas",
              lugar="La sede del Gremio", personajes="Kira, Gheco, Hulda",
              carta="Comparar sin mayúsculas | pasar las dos a minúsculas con tolower letra por letra · después strcmp · o comparar letra a letra",
              recompensa="xp 15, oro 15",
              escena="Hulda busca en la agenda «HULDA», «hulda» y «Hulda», y solo la encuentra con la última. Grita fuerte. Kira tiene que hacer que la encuentre siempre.",
              sugiere="Se comparan letra por letra con `tolower`: si alguna difiere, no son iguales; si las dos terminan juntas, sí.",
              desafio="Completá la comparación letra por letra.",
              inicial='''
                  #include <stdio.h>
                  #include <ctype.h>
                  #include <stdbool.h>

                  bool iguales_sin_mayusculas(const char *a, const char *b)
                  {
                      int i = 0;
                      while (a[i] != '\\0' && b[i] != '\\0') {
                          if (___) {
                              return false;
                          }
                          i++;
                      }
                      return a[i] == '\\0' && b[i] == '\\0';
                  }

                  int main(void)
                  {
                      const char *buscados[3] = { "HULDA", "hulda", "Huldo" };
                      for (int i = 0; i < 3; i++) {
                          printf("%s: %s\\n", buscados[i], iguales_sin_mayusculas("Hulda", buscados[i]) ? "encontrada" : "no esta");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <ctype.h>
                  #include <stdbool.h>

                  bool iguales_sin_mayusculas(const char *a, const char *b)
                  {
                      int i = 0;
                      while (a[i] != '\\0' && b[i] != '\\0') {
                          if (tolower((unsigned char) a[i]) != tolower((unsigned char) b[i])) {
                              return false;
                          }
                          i++;
                      }
                      return a[i] == '\\0' && b[i] == '\\0';
                  }

                  int main(void)
                  {
                      const char *buscados[3] = { "HULDA", "hulda", "Huldo" };
                      for (int i = 0; i < 3; i++) {
                          printf("%s: %s\\n", buscados[i], iguales_sin_mayusculas("Hulda", buscados[i]) ? "encontrada" : "no esta");
                      }
                      return 0;
                  }
              ''',
              al_superar="Encontrada, encontrada. «Huldo», no. Hulda quiere saber quién es Huldo. Nadie sabe.",
              imagen=["Una agenda abierta con el nombre Hulda resaltado tres veces.", HULDA + " grita «¡HULDA!» con las manos en la boca."]),
            m(id="R05-N03-P3", titulo="Campos con espacios",
              lugar="La sede del Gremio", personajes="Kira, Gheco, Tizón",
              carta="Leer campos separados | una línea «nombre;telefono;email» · %[^;] lee hasta el ; con espacios incluidos · validar cada campo",
              recompensa="xp 15, oro 15",
              escena="Cada renglón que llega al Gremio dice «nombre;teléfono;email», y los nombres tienen espacios («Maese Ferrum»). Tizón quiere los tres campos bien separados.",
              sugiere="`sscanf(linea, \"%29[^;];%19[^;];%39[^\\n]\", nombre, tel, mail)` lee los tres campos aunque tengan espacios. Si devuelve 3, están los tres.",
              desafio="Completá el formato del `sscanf`.",
              entrada="Maese Ferrum;380 4110000;ferrum@forjas.ar\nTizon;380 4229999\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[100], nombre[30], tel[20], mail[40];
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (sscanf(linea, "___", nombre, tel, mail) == 3) {
                              printf("[%s] [%s] [%s]\\n", nombre, tel, mail);
                          } else {
                              printf("renglon incompleto\\n");
                          }
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[100], nombre[30], tel[20], mail[40];
                      while (fgets(linea, sizeof linea, stdin) != NULL) {
                          if (sscanf(linea, "%29[^;];%19[^;];%39[^\\n]", nombre, tel, mail) == 3) {
                              printf("[%s] [%s] [%s]\\n", nombre, tel, mail);
                          } else {
                              printf("renglon incompleto\\n");
                          }
                      }
                      return 0;
                  }
              ''',
              al_superar="Ferrum, completo; Tizón, sin email («no tengo», dice, «lo mido todo a mano»). La agenda los separa sin problema.",
              imagen=["Un renglón de pergamino que se separa en tres casillas de luz.", TIZON + " muestra que no tiene email, orgulloso."]),
            m(id="R05-N03-P4", titulo="La agenda ordenada",
              lugar="La sede del Gremio", personajes="Kira, Gheco, Maese Ferrum",
              carta="El proyecto entero | array de structs + validación + qsort por nombre · cada función hace una cosa",
              recompensa="xp 15, oro 15",
              escena="El Gremio quiere la agenda impresa, ordenada por nombre, para colgarla en la sede. Ferrum revisa que cada parte sea su propia función.",
              sugiere="`qsort` con una comparación que use `strcmp` de los nombres. Los contactos inválidos ni se agregan.",
              desafio="Completá la comparación por nombre.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  typedef struct {
                      char nombre[30];
                      char telefono[20];
                  } Contacto;

                  int por_nombre(const void *a, const void *b)
                  {
                      const Contacto *x = a;
                      const Contacto *y = b;
                      return ___;
                  }

                  int main(void)
                  {
                      Contacto agenda[4] = {
                          { "Tizon", "380 4229999" },
                          { "Chispa", "380 4000001" },
                          { "Hulda", "380 4335566" },
                          { "Maese Ferrum", "380 4110000" },
                      };
                      qsort(agenda, 4, sizeof agenda[0], por_nombre);
                      for (int i = 0; i < 4; i++) {
                          printf("%-13s %s\\n", agenda[i].nombre, agenda[i].telefono);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  typedef struct {
                      char nombre[30];
                      char telefono[20];
                  } Contacto;

                  int por_nombre(const void *a, const void *b)
                  {
                      const Contacto *x = a;
                      const Contacto *y = b;
                      return strcmp(x->nombre, y->nombre);
                  }

                  int main(void)
                  {
                      Contacto agenda[4] = {
                          { "Tizon", "380 4229999" },
                          { "Chispa", "380 4000001" },
                          { "Hulda", "380 4335566" },
                          { "Maese Ferrum", "380 4110000" },
                      };
                      qsort(agenda, 4, sizeof agenda[0], por_nombre);
                      for (int i = 0; i < 4; i++) {
                          printf("%-13s %s\\n", agenda[i].nombre, agenda[i].telefono);
                      }
                      return 0;
                  }
              ''',
              al_superar="La agenda cuelga en la sede del Gremio, ordenada. Chispa queda primero en la lista por primera vez en su vida. Lo festeja más que si hubiera ganado algo.",
              imagen=["Una agenda grande clavada en la pared de la sede del Gremio, con cuatro nombres en orden.", CHISPA + " señala su nombre, primero, feliz."]),
        ],
    },
    {
        "titulo": "R05-N05 · La Encrucijada del Yunque",
        "misiones": [
            m(id="R05-N05-P1", titulo="La cuenta de la pared",
              lugar="La Encrucijada del Yunque", personajes="Kira, Gheco, Maese Ferrum, Tizón",
              carta="Mirar hacia atrás | todo lo que se forjó: tipos, bucles, funciones, punteros, memoria, archivos · cada pieza en su lugar",
              recompensa="xp 20, oro 20",
              escena="""
                  En la entrada de las Forjas, la pared de la cuenta de espadazos está llena de palitos. Ferrum le da a Kira la tiza: falta la última línea.
              """,
              sugiere="Un último programa para la pared: recorré los registros y mostrá cada uno alineado.",
              desafio="Completá el `printf` para que la pared quede alineada (nombre a la izquierda en 30 lugares, número a la derecha en 3).",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      const char *que;
                      int cuantos;
                  } Registro;

                  int main(void)
                  {
                      Registro pared[4] = {
                          { "Espadazos", 41 },
                          { "Problemas resueltos a espadazos", 0 },
                          { "Herraduras banana", 40 },
                          { "Problemas resueltos midiendo", 99 },
                      };
                      for (int i = 0; i < 4; i++) {
                          printf("___\\n", pared[i].que, pared[i].cuantos);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      const char *que;
                      int cuantos;
                  } Registro;

                  int main(void)
                  {
                      Registro pared[4] = {
                          { "Espadazos", 41 },
                          { "Problemas resueltos a espadazos", 0 },
                          { "Herraduras banana", 40 },
                          { "Problemas resueltos midiendo", 99 },
                      };
                      for (int i = 0; i < 4; i++) {
                          printf("%-31s %3d\\n", pared[i].que, pared[i].cuantos);
                      }
                      return 0;
                  }
              ''',
              al_superar="Ferrum mira la pared, golpea el yunque **tres veces** y le saca la tiza de la mano a Kira. Tacha el 99 y escribe: «todos». Kira no sabe qué hacer con las manos. Tizón llora sin disimular.",
              imagen=["Una pared de piedra llena de palitos de tiza bajo títulos como Espadazos y Herraduras banana.",
                      FERRUM + " escribe «todos» con tiza.", KIRA + " con la Hoja Templada a la espalda.", TIZON + " llorando."]),
            m(id="R05-N05-P2", titulo="Dos caminos",
              lugar="La Encrucijada del Yunque", personajes="Kira, Gheco, Maese Ferrum",
              carta="Elegir camino | la Forja Viva: juegos con SDL3 · el Taller de los Autómatas: Arduino · lo que sigue es tuyo",
              recompensa="xp 20, oro 20",
              escena="Del yunque viejo salen dos caminos. Uno lleva a una puerta de vidrio negro donde el metal se mueve solo, sesenta veces por segundo. El otro, a un taller lleno de figuras de latón con ojos que se prenden y se apagan.",
              sugiere="Un último `switch`: según el camino elegido, se muestra adónde lleva.",
              desafio="Completá los dos `case` con los caminos.",
              entrada="1\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int camino;
                      scanf("%d", &camino);
                      switch (camino) {
                      ___
                          printf("La Forja Viva: el metal se mueve en una pantalla (SDL3)\\n");
                          break;
                      ___
                          printf("El Taller de los Automatas: el codigo mueve cosas de verdad (Arduino)\\n");
                          break;
                      default:
                          printf("Ese camino no existe (todavia)\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int camino;
                      scanf("%d", &camino);
                      switch (camino) {
                      case 1:
                          printf("La Forja Viva: el metal se mueve en una pantalla (SDL3)\\n");
                          break;
                      case 2:
                          printf("El Taller de los Automatas: el codigo mueve cosas de verdad (Arduino)\\n");
                          break;
                      default:
                          printf("Ese camino no existe (todavia)\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="Ferrum se apoya en el martillo. —Lo que sigue no es obligatorio. Es **tuyo**. —Kira mira los dos caminos. Por primera vez desde que llegó, no tiene apuro.",
              imagen=["Un yunque viejo en una encrucijada, con dos caminos: uno hacia una puerta de vidrio negro y otro hacia un taller con autómatas de latón.",
                      KIRA + " de espaldas, mirando los dos caminos.", FERRUM + " apoyado en su martillo enorme."]),
        ],
    },
]
