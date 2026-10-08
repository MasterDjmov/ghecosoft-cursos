from genc import m

BOCA = "La boca de la Forja"
EJECUTAR = "Tocá **Ejecutar**: C se compila acá mismo, en tu navegador (la primera vez baja el compilador y tarda un poco)."
KIRA = "Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian)"
TIZON = "Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello)"
FERRUM = "Maese Ferrum (enano macizo, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura)"
CHISPA = "Chispa (mercader alto y flaco, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro)"

NODOS = [
    {
        "titulo": "R00-N01 · Clase 0 · Hola, C",
        "misiones": [
            m(id="R00-N01-P1", titulo="La primera receta",
              lugar=BOCA, personajes="Kira, Gheco, Maese Ferrum",
              carta="Mostrar texto | printf(\"texto\\n\"); · \\n salta de línea · cada instrucción termina con ;",
              recompensa="xp 10, oro 10",
              escena="""
                  Kira despierta junto a un vitral apagado, frente al portón de las Forjas. Un enano de barba trenzada la mira de arriba abajo: **Maese Ferrum**.
                  —Acá la magia se escribe en C. Decime quién sos. Por escrito.
                  Sobre el hombro de Kira aparece un gecko de luz con antiparras: **Gheco**. —Escribilo en la receta. Acá las recetas se **compilan**.
              """,
              sugiere="`printf(\"…\");` muestra el texto entre comillas. `\\n` al final baja a la línea siguiente. " + EJECUTAR,
              desafio="Completá la instrucción para que Kira se presente.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      ___("Me llamo Kira y vengo de muy lejos.\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("Me llamo Kira y vengo de muy lejos.\\n");
                      return 0;
                  }
              ''',
              al_superar="Ferrum lee la receta compilada y asiente una sola vez. —De muy lejos. Ya se nota. —Mira la espada que Kira tiene en la mano, y no dice nada más.",
              imagen=["La boca de las Forjas de Hierro de noche: un portón de hierro enorme, chimeneas y ríos de lava al fondo, un vitral apagado en el piso.",
                      KIRA + " se levanta del piso con una espada de aprendiz en la mano.",
                      FERRUM + " la mira con los brazos cruzados.",
                      "Gheco, un gecko cian con antiparras, aparece sobre el hombro de Kira."]),
            m(id="R00-N01-P2", titulo="Tres líneas, un solo printf",
              lugar=BOCA, personajes="Kira, Gheco, Maese Ferrum",
              carta="Secuencias de escape | \\n salto de línea · \\t tabulación · \\\" comillas · %% un signo %",
              recompensa="xp 10, oro 10",
              escena="—La ficha de entrada va en tres renglones —dice Ferrum—: nombre, oficio y \"lo que trae\". Con comillas, como se debe.",
              sugiere="Dentro del texto, `\\n` baja de línea, `\\t` deja una tabulación y `\\\"` escribe unas comillas sin cerrar el texto.",
              desafio="Escribí las secuencias que faltan para que la ficha quede en tres líneas y con comillas.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("Nombre:\\tKira___Oficio:\\tespadachina___Trae:\\t___una espada___\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("Nombre:\\tKira\\nOficio:\\tespadachina\\nTrae:\\t\\"una espada\\"\\n");
                      return 0;
                  }
              ''',
              al_superar="Ferrum tacha «espada» y escribe arriba «espada (rajada)». Kira no le dice nada. Todavía.",
              imagen=["Una ficha de hierro con tres renglones grabados en luz cian: Nombre, Oficio, Trae.",
                      FERRUM + " corrige la ficha con una tiza."]),
            m(id="R00-N01-P3", titulo="El punto y coma olvidado",
              lugar=BOCA, personajes="Kira, Gheco, Tizón",
              criatura="slime",
              carta="Error de compilación | el Horno revisa ANTES de ejecutar · expected ';' : falta un punto y coma · arreglá el primer error y volvé a compilar",
              recompensa="xp 10, oro 10",
              escena="""
                  Un enano joven con un calibre colgado del cuello se acerca a mirar la receta de Kira: **Tizón**. Del renglón dos gotea un **slime**.
                  —El Horno no la quiere —dice, midiéndole el renglón—. Le falta algo. Chiquito.
              """,
              sugiere="Un **error de compilación** frena todo antes de ejecutar. `expected ';' before …` quiere decir que falta un punto y coma al final de la línea anterior a la que marca.",
              desafio="Arreglá la receta para que el Horno la acepte.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("Kira conoce a Tizon.\\n")
                      printf("Tizon mide todo.\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("Kira conoce a Tizon.\\n");
                      printf("Tizon mide todo.\\n");
                      return 0;
                  }
              ''',
              al_superar="El slime se evapora con un *plop*. Tizón anota en su libreta: «Punto y coma: 1 mm. Importancia: enorme».",
              imagen=["Una receta de pergamino con una marca roja en un renglón, de la que gotea un slime verde.",
                      TIZON + " mide el renglón con el calibre."]),
            m(id="R00-N01-P4", titulo="Lo que el Horno ignora",
              lugar=BOCA, personajes="Kira, Gheco, Tizón",
              carta="Comentarios | /* … */ ocupa varias líneas · // hasta el final de la línea · el compilador los ignora",
              recompensa="xp 10, oro 10",
              escena="Tizón deja notas para sí mismo en todas partes, incluso adentro de las recetas. El problema es que el Horno intenta leerlas como si fueran C.",
              sugiere="Los **comentarios** son para las personas: `/* … */` puede ocupar varias líneas y `//` llega hasta el final de la línea. El compilador los saltea.",
              desafio="Convertí las notas de Tizón en comentarios para que la receta compile y muestre solo los dos saludos.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      Nota de Tizon: medir antes de pegar
                      printf("Hola, Forjas.\\n");
                      recordar: el cajon de clavos llega hasta 255
                      printf("Hola, Horno.\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      /* Nota de Tizon: medir antes de pegar */
                      printf("Hola, Forjas.\\n");
                      // recordar: el cajon de clavos llega hasta 255
                      printf("Hola, Horno.\\n");
                      return 0;
                  }
              ''',
              al_superar="Las notas de Tizón quedan en la receta, pero el Horno ya no se atraganta con ellas. —Así las leo yo y no él —dice Tizón, satisfecho.",
              imagen=["Una receta llena de notas a mano en los márgenes, algunas encerradas en /* */ que brillan en gris.",
                      TIZON + " escribe una nota más con un lápiz detrás de la oreja."]),
            m(id="R00-N01-P5", titulo="El portón se abre tirando",
              lugar=BOCA, personajes="Kira, Gheco, Maese Ferrum, Tizón",
              carta="La anatomía | #include <stdio.h> trae printf · int main(void) { … } es donde empieza · return 0; avisa que todo salió bien",
              recompensa="xp 15, oro 15",
              item="Espada Rajada",
              escena="""
                  Kira toma carrera y le da un espadazo al portón. La espada **se raja** de punta a mango; el portón ni se entera. Ferrum lo abre **tirando** de la manija.
                  —Acá nada se abre a golpes. Escribí la receta entera, de punta a punta: lo que se trae, dónde empieza y cómo termina.
              """,
              sugiere="Todo programa de C trae `#include <stdio.h>` para usar `printf`, empieza en `int main(void)` (entre llaves) y termina con `return 0;`.",
              desafio="A la receta le falta el comienzo de `main` y el final. Completala.",
              inicial='''
                  #include <stdio.h>

                  ___
                  {
                      printf("El porton se abre tirando.\\n");
                      printf("Kira guarda la espada rajada.\\n");
                      ___
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("El porton se abre tirando.\\n");
                      printf("Kira guarda la espada rajada.\\n");
                      return 0;
                  }
              ''',
              al_superar="El portón se abre de par en par. Ferrum le devuelve la espada rajada. —Guardala. Algún día vas a querer acordarte de esto. —La **Espada Rajada** va a tu mochila. En la pared de la entrada, alguien escribe con tiza: «Espadazos: 1».",
              imagen=[KIRA + " mira su espada rajada de punta a mango, frente a un portón de hierro intacto.",
                      FERRUM + " abre el portón tirando de la manija, sin esfuerzo.",
                      TIZON + " se ríe por lo bajo detrás de él."]),
        ],
    },
    {
        "titulo": "R01-N01 · Variables y tipos",
        "misiones": [
            m(id="R01-N01-P1", titulo="Cada cosa en su cajón",
              lugar="El depósito de la Forja", personajes="Kira, Gheco, Tizón",
              criatura="goblin",
              carta="Variables | tipo nombre = valor; · int para enteros · double para decimales · char para un carácter",
              recompensa="xp 10, oro 10",
              escena="En el depósito cada material va en un cajón con etiqueta. Tizón le da a Kira tres cajones vacíos: uno para la cantidad de clavos, uno para el peso del lingote y uno para la letra del sello.",
              sugiere="Una variable se declara con su **tipo**: `int` (enteros), `double` (decimales) o `char` (un carácter, entre comillas simples: `'K'`). Se muestran con `%d`, `%.1f` y `%c`.",
              desafio="Declará las tres variables con el tipo correcto.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      ___ clavos = 120;
                      ___ peso = 2.5;
                      ___ sello = 'K';
                      printf("clavos: %d\\n", clavos);
                      printf("peso: %.1f kg\\n", peso);
                      printf("sello: %c\\n", sello);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int clavos = 120;
                      double peso = 2.5;
                      char sello = 'K';
                      printf("clavos: %d\\n", clavos);
                      printf("peso: %.1f kg\\n", peso);
                      printf("sello: %c\\n", sello);
                      return 0;
                  }
              ''',
              al_superar="Tres cajones, tres etiquetas. Tizón los mide uno por uno y los aprueba con un gruñido muy parecido al de Ferrum.",
              imagen=["Un depósito de piedra con cajones de hierro etiquetados: clavos, peso, sello.",
                      KIRA + " guarda una letra K de bronce en un cajón chiquito.", TIZON + " anota en su libreta."]),
            m(id="R01-N01-P2", titulo="El clavo 256",
              lugar="El depósito de la Forja", personajes="Kira, Gheco, Tizón",
              criatura="ogro",
              carta="Desborde | unsigned char va de 0 a 255 · si se pasa, vuelve a 0 sin avisar · elegí un tipo con lugar de sobra",
              recompensa="xp 10, oro 10",
              escena="""
                  Kira guarda clavos en el cajón chiquito: 254, 255… y el 256. El cajón hace *clic* y queda **vacío**.
                  —¡Los había contado uno por uno! —se agarra la cabeza Tizón.
              """,
              sugiere="Un `unsigned char` guarda de 0 a 255: si se pasa, **vuelve a 0** sin avisar. Un `int` tiene lugar de sobra (más de dos mil millones).",
              desafio="Cambiá el tipo del cajón para que entren 256 clavos.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      unsigned char cajon = 255;
                      cajon = cajon + 1;
                      printf("clavos en el cajon: %d\\n", cajon);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int cajon = 255;
                      cajon = cajon + 1;
                      printf("clavos en el cajon: %d\\n", cajon);
                      return 0;
                  }
              ''',
              al_superar="256 clavos, ni uno menos. Tizón le perdona a Kira el susto, pero le dedica una mirada larguísima.",
              imagen=["Un cajón chiquito de hierro con un 255 grabado, que se vacía con un destello.",
                      TIZON + " se agarra la cabeza; " + KIRA + " sostiene el clavo 256 con cara de culpa."]),
            m(id="R01-N01-P3", titulo="Cuánto ocupa cada cajón",
              lugar="El depósito de la Forja", personajes="Kira, Gheco, Tizón",
              carta="sizeof | sizeof(tipo) dice cuántos bytes ocupa · se muestra con %zu · char 1, int 4, double 8",
              recompensa="xp 10, oro 10",
              escena="Tizón quiere medir los cajones por dentro, pero el calibre no entra. Gheco le muestra una herramienta mejor.",
              sugiere="`sizeof(tipo)` devuelve cuántos **bytes** ocupa ese tipo. Su valor se muestra con `%zu`.",
              desafio="Completá con `sizeof` para mostrar cuánto ocupa cada tipo.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("char:   %zu byte\\n", ___(char));
                      printf("int:    %zu bytes\\n", ___(int));
                      printf("double: %zu bytes\\n", ___(double));
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("char:   %zu byte\\n", sizeof(char));
                      printf("int:    %zu bytes\\n", sizeof(int));
                      printf("double: %zu bytes\\n", sizeof(double));
                      return 0;
                  }
              ''',
              al_superar="Tizón copia los tres números en la tapa de la libreta, con letra grande. Es la primera vez que algo lo mide a él primero.",
              imagen=["Tres cajones de distinto tamaño, con números luminosos 1, 4 y 8 encima.", TIZON + " guarda el calibre, sorprendido."]),
            m(id="R01-N01-P4", titulo="El precio con decimales",
              lugar="El depósito de la Forja", personajes="Kira, Gheco, Chispa",
              criatura="goblin",
              carta="Conversión | int / int da un entero · (double) convierte antes de dividir · el cast va delante del valor",
              recompensa="xp 15, oro 15",
              escena="Chispa reparte el precio de 7 lingotes entre 2 compradores y le da **3** a cada uno. —Sobra uno, que me lo quedo yo —sonríe con el diente de oro.",
              sugiere="Si los dos números son `int`, la división **descarta** los decimales. Con `(double)` delante de uno, la cuenta se hace con decimales.",
              desafio="Convertí la cuenta para que el reparto sea justo.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int lingotes = 7;
                      int compradores = 2;
                      double cada_uno = lingotes / compradores;
                      printf("cada uno paga %.1f lingotes\\n", cada_uno);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int lingotes = 7;
                      int compradores = 2;
                      double cada_uno = (double) lingotes / compradores;
                      printf("cada uno paga %.1f lingotes\\n", cada_uno);
                      return 0;
                  }
              ''',
              al_superar="3,5 cada uno. Chispa devuelve el lingote que «sobraba» con una sonrisa que no engaña a nadie.",
              imagen=[CHISPA + " reparte siete lingotes en dos pilas desparejas.", "Un goblin se escapa con medio lingote bajo el brazo."]),
        ],
    },
    {
        "titulo": "R01-N02 · Operadores",
        "misiones": [
            m(id="R01-N02-P1", titulo="Cajas completas y sobrantes",
              lugar="El mostrador de la Forja", personajes="Kira, Gheco, Chispa",
              carta="División entera y resto | 17 / 5 da 3 · 17 % 5 da 2 (lo que sobra) · solo con enteros",
              recompensa="xp 10, oro 10",
              escena="Chispa trae 17 herraduras y las quiere vender en cajas de 5. —¿Cuántas cajas armo y cuántas me sobran para vender sueltas, que salen más caras?",
              sugiere="Con enteros, `/` da cuántas veces entra y `%` (el **resto**) da lo que sobra.",
              desafio="Completá los dos operadores.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int herraduras = 17;
                      int por_caja = 5;
                      printf("cajas: %d\\n", herraduras ___ por_caja);
                      printf("sueltas: %d\\n", herraduras ___ por_caja);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int herraduras = 17;
                      int por_caja = 5;
                      printf("cajas: %d\\n", herraduras / por_caja);
                      printf("sueltas: %d\\n", herraduras % por_caja);
                      return 0;
                  }
              ''',
              al_superar="Tres cajas y dos sueltas. Chispa le pone a las sueltas el doble de precio. Tizón lo anota, por las dudas.",
              imagen=["Tres cajas con cinco herraduras cada una y dos herraduras sueltas sobre un mostrador.", CHISPA + " les pega una etiqueta de precio enorme a las sueltas."]),
            m(id="R01-N02-P2", titulo="El orden de las cuentas",
              lugar="El mostrador de la Forja", personajes="Kira, Gheco, Chispa, Tizón",
              criatura="ogro",
              carta="Precedencia | * / % antes que + - · los paréntesis mandan · ante la duda, paréntesis",
              recompensa="xp 10, oro 10",
              escena="""
                  Chispa cobra tres herraduras de 2 lingotes más 1 de envío. Le da **7**. Tizón hace la cuenta en la libreta: le da **9**.
                  —El envío es **por herradura** —dice Tizón—. Y la cuenta de Chispa lo cobra una sola vez.
              """,
              sugiere="C hace `*` antes que `+`: `3 * 2 + 1` es 7. Para que la suma vaya primero, se encierra entre **paréntesis**.",
              desafio="Agregá los paréntesis para que el envío se cobre por cada herradura.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int herraduras = 3;
                      int precio = 2;
                      int envio = 1;
                      int total = herraduras * precio + envio;
                      printf("total: %d lingotes\\n", total);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int herraduras = 3;
                      int precio = 2;
                      int envio = 1;
                      int total = herraduras * (precio + envio);
                      printf("total: %d lingotes\\n", total);
                      return 0;
                  }
              ''',
              al_superar="Nueve lingotes. Chispa, que esta vez se había cobrado de menos, mira a Tizón con respeto nuevo.",
              imagen=["Una pizarra con dos cuentas: 3 * 2 + 1 tachada y 3 * (2 + 1) encerrada en un círculo.", TIZON + " señala la pizarra; " + CHISPA + " se rasca la cabeza."]),
            m(id="R01-N02-P3", titulo="Un golpe más, un golpe menos",
              lugar="El yunque de la Forja", personajes="Kira, Gheco, Maese Ferrum",
              carta="Incremento y asignación compuesta | x++ suma 1 · x-- resta 1 · x += 5 es x = x + 5 · también -=, *=, /=",
              recompensa="xp 10, oro 10",
              escena="Ferrum cuenta los martillazos de Kira en voz alta, de muy mal humor: uno, otro más, cinco de golpe en un ataque de impaciencia, y después se le cae el martillo y pierde la cuenta de dos.",
              sugiere="`golpes++` suma 1. `golpes += 5` suma 5. `golpes -= 2` resta 2. Son formas cortas de `golpes = golpes + …`.",
              desafio="Completá con los operadores cortos para que la cuenta termine en 5.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int golpes = 0;
                      golpes___;          /* uno */
                      golpes___;          /* otro mas */
                      golpes ___ 5;       /* cinco de golpe */
                      golpes ___ 2;       /* se perdieron dos */
                      printf("golpes contados: %d\\n", golpes);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int golpes = 0;
                      golpes++;           /* uno */
                      golpes++;           /* otro mas */
                      golpes += 5;        /* cinco de golpe */
                      golpes -= 2;        /* se perdieron dos */
                      printf("golpes contados: %d\\n", golpes);
                      return 0;
                  }
              ''',
              al_superar="Cinco golpes. Ferrum los anota en la pared, al lado de la cuenta de espadazos. Kira prefiere no mirar.",
              imagen=[FERRUM + " cuenta con los dedos al lado de un yunque.", KIRA + " sostiene un martillo demasiado grande."]),
            m(id="R01-N02-P4", titulo="¿Alcanza el carbón?",
              lugar="El horno de la Forja", personajes="Kira, Gheco, Tizón",
              carta="Comparaciones | == != < > <= >= dan 1 (verdadero) o 0 (falso) · = guarda, == compara",
              recompensa="xp 15, oro 15",
              escena="Para templar una espada hacen falta 12 bolsas de carbón. Hay 9 en el depósito. Tizón quiere la respuesta en números, como todo.",
              sugiere="Una comparación da **1** si es verdadera y **0** si es falsa. Ojo: `=` guarda un valor; `==` pregunta si son iguales.",
              desafio="Completá las comparaciones.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int hay = 9;
                      int hacen_falta = 12;
                      printf("alcanza: %d\\n", hay ___ hacen_falta);
                      printf("faltan exactamente 3: %d\\n", hacen_falta - hay ___ 3);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int hay = 9;
                      int hacen_falta = 12;
                      printf("alcanza: %d\\n", hay >= hacen_falta);
                      printf("faltan exactamente 3: %d\\n", hacen_falta - hay == 3);
                      return 0;
                  }
              ''',
              al_superar="No alcanza, y faltan justo tres. Tizón sale corriendo a buscar carbón. Vuelve con cuatro bolsas, «por si acaso».",
              imagen=["Un horno apagado con nueve bolsas de carbón al lado y tres huecos marcados con tiza.", TIZON + " carga bolsas de carbón."]),
        ],
    },
    {
        "titulo": "R01-N03 · Operadores de bits",
        "misiones": [
            m(id="R01-N03-P1", titulo="Las ocho palancas",
              lugar="El pañol de la Forja", personajes="Kira, Gheco, Tizón",
              carta="Hexadecimal | %x muestra en hexa · 0xFF = 255 = ocho bits en 1 · cada cifra hexa son 4 bits",
              recompensa="xp 10, oro 10",
              escena="La cerradura del pañol tiene ocho palancas. Kira la intenta abrir a patadas; no se mueve. Tizón le muestra el número de la combinación, pero escrito raro: en **hexadecimal**.",
              sugiere="`%x` muestra un número en hexadecimal (base 16) y `%d`, en decimal. `0x` delante de un número dice que está escrito en hexa.",
              desafio="Mostrá la combinación en hexadecimal y el número `0xFF` en decimal.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int combinacion = 173;
                      printf("combinacion en hexa: %___\\n", combinacion);
                      printf("0xFF en decimal: %___\\n", 0xFF);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int combinacion = 173;
                      printf("combinacion en hexa: %x\\n", combinacion);
                      printf("0xFF en decimal: %d\\n", 0xFF);
                      return 0;
                  }
              ''',
              al_superar="«ad». Tizón mueve las palancas siguiendo las dos cifras. *Clac*. Kira dice que fue suerte.",
              imagen=["Una cerradura de hierro con ocho palancas, algunas arriba y otras abajo, y los caracteres 0xAD brillando encima.",
                      KIRA + " con el pie todavía levantado.", TIZON + " con la mano en una palanca."]),
            m(id="R01-N03-P2", titulo="Encender una bandera",
              lugar="El tablero de los aprendices", personajes="Kira, Gheco, Maese Ferrum",
              carta="OR de bits | estado | BANDERA enciende ese bit · los demás no cambian · 1 << n es el bit n",
              recompensa="xp 10, oro 10",
              escena="En la pared hay un tablero con los estados de cada aprendiz: dormido, quemado, bendecido… Kira se quemó con el horno (otra vez). Ferrum le pide que lo anote **sin borrar** lo demás.",
              sugiere="Cada estado es un bit. `estado | QUEMADO` enciende ese bit y deja los otros como estaban. `1 << 2` es el bit 2 (vale 4).",
              desafio="Encendé el bit de QUEMADO en el estado de Kira.",
              inicial='''
                  #include <stdio.h>

                  #define DORMIDO   (1 << 0)
                  #define BENDECIDO (1 << 1)
                  #define QUEMADO   (1 << 2)

                  int main(void)
                  {
                      int estado = BENDECIDO;
                      estado = ___;
                      printf("estado de Kira: %d\\n", estado);
                      printf("bendecida: %d, quemada: %d\\n", (estado & BENDECIDO) != 0, (estado & QUEMADO) != 0);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define DORMIDO   (1 << 0)
                  #define BENDECIDO (1 << 1)
                  #define QUEMADO   (1 << 2)

                  int main(void)
                  {
                      int estado = BENDECIDO;
                      estado = estado | QUEMADO;
                      printf("estado de Kira: %d\\n", estado);
                      printf("bendecida: %d, quemada: %d\\n", (estado & BENDECIDO) != 0, (estado & QUEMADO) != 0);
                      return 0;
                  }
              ''',
              al_superar="Bendecida **y** quemada. Ferrum le pasa un ungüento. —Lo de bendecida no te salvó de nada, ¿no?",
              imagen=["Un tablero de clavijas en la pared con tres luces: una apagada y dos encendidas.", KIRA + " con una mano vendada.", FERRUM + " le pasa un frasco de ungüento."]),
            m(id="R01-N03-P3", titulo="Apagar sin tocar lo demás",
              lugar="El tablero de los aprendices", personajes="Kira, Gheco, Tizón",
              carta="AND con NOT | estado & ~BANDERA apaga ese bit · ~ invierte todos los bits · & deja pasar solo los que están en 1 en los dos",
              recompensa="xp 10, oro 10",
              escena="Tizón se pasó la noche durmiendo en la libreta. Hay que apagar su bit de DORMIDO, pero sin apagarle el de BENDECIDO, que le costó muchísimo conseguir.",
              sugiere="`~DORMIDO` tiene todos los bits en 1 **menos** el de DORMIDO. Con `estado & ~DORMIDO` se apaga solo ese.",
              desafio="Apagá solo el bit DORMIDO.",
              inicial='''
                  #include <stdio.h>

                  #define DORMIDO   (1 << 0)
                  #define BENDECIDO (1 << 1)

                  int main(void)
                  {
                      int estado = DORMIDO | BENDECIDO;
                      printf("antes: %d\\n", estado);
                      estado = estado & ___;
                      printf("despues: %d\\n", estado);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  #define DORMIDO   (1 << 0)
                  #define BENDECIDO (1 << 1)

                  int main(void)
                  {
                      int estado = DORMIDO | BENDECIDO;
                      printf("antes: %d\\n", estado);
                      estado = estado & ~DORMIDO;
                      printf("despues: %d\\n", estado);
                      return 0;
                  }
              ''',
              al_superar="Tizón se despierta de un salto, bendecido y descansado, y mide el tablero para asegurarse de que no le tocaron nada más.",
              imagen=[TIZON + " dormido sobre la libreta abierta, con baba en una página llena de números.", "Una luz del tablero que se apaga mientras otra sigue encendida."]),
            m(id="R01-N03-P4", titulo="Duplicar con un empujón",
              lugar="El horno de la Forja", personajes="Kira, Gheco, Tizón",
              carta="Desplazamientos | x << 1 duplica · x >> 1 divide por 2 (entero) · mueven los bits a la izquierda o a la derecha",
              recompensa="xp 15, oro 15",
              escena="Cada vez que Tizón sopla el fuelle, la temperatura del horno se duplica (eso dice él). Kira quiere comprobarlo sin multiplicar.",
              sugiere="`x << 1` corre todos los bits un lugar a la izquierda: es multiplicar por 2. `x >> 1` es dividir por 2 (sin decimales).",
              desafio="Completá los desplazamientos.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int grados = 100;
                      printf("un soplido: %d\\n", grados ___ 1);
                      printf("tres soplidos: %d\\n", grados ___ 3);
                      printf("se enfria a la mitad: %d\\n", grados ___ 1);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int grados = 100;
                      printf("un soplido: %d\\n", grados << 1);
                      printf("tres soplidos: %d\\n", grados << 3);
                      printf("se enfria a la mitad: %d\\n", grados >> 1);
                      return 0;
                  }
              ''',
              al_superar="800 grados con tres soplidos. Tizón, rojo de orgullo y de calor, se sienta a descansar lejos del horno.",
              imagen=["Un horno con un termómetro de cobre que marca 100, 200, 800.", TIZON + " sopla un fuelle con las mejillas infladas."]),
        ],
    },
    {
        "titulo": "R01-N04 · Entrada y salida",
        "misiones": [
            m(id="R01-N04-P1", titulo="La tabla torcida",
              lugar="El mostrador de pedidos", personajes="Kira, Gheco, Tizón",
              carta="Ancho en printf | %-8s texto a la izquierda en 8 lugares · %5d número a la derecha en 5 · %8.2f decimal en 8 con 2 decimales",
              recompensa="xp 10, oro 10",
              escena="Kira clava la tabla de precios en la pared. Tizón llega con el calibre: —Esta columna está corrida. Y esta otra. Y este precio tiene un decimal de más.",
              sugiere="Entre el `%` y la letra va el **ancho**: `%-8s` ocupa 8 lugares alineado a la izquierda; `%5d` y `%8.2f`, a la derecha.",
              desafio="Completá los formatos para que la tabla quede alineada.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("%-8s %5s %8s\\n", "pieza", "stock", "precio");
                      printf("%___ %___ %___\\n", "espada", 3, 45.5);
                      printf("%___ %___ %___\\n", "escudo", 12, 30.0);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      printf("%-8s %5s %8s\\n", "pieza", "stock", "precio");
                      printf("%-8s %5d %8.2f\\n", "espada", 3, 45.5);
                      printf("%-8s %5d %8.2f\\n", "escudo", 12, 30.0);
                      return 0;
                  }
              ''',
              al_superar="Tizón pasa el calibre por cada columna. Esta vez no encuentra nada. Se queda un rato mirando la tabla, casi decepcionado.",
              imagen=["Una tabla de precios clavada en la pared, con columnas perfectamente alineadas.", TIZON + " mide una columna con el calibre."]),
            m(id="R01-N04-P2", titulo="La edad en números",
              lugar="La ventanilla de la Forja", personajes="Kira, Gheco, Chispa",
              criatura="goblin",
              carta="scanf | scanf(\"%d\", &edad) lee un entero · el & dice DÓNDE guardarlo · sin &, el goblin se roba el número",
              recompensa="xp 10, oro 10",
              escena="""
                  El escriba de la ventanilla le pregunta la edad a Chispa. El programa lee… y no guarda nada. Un **goblin** sale corriendo con el número bajo el brazo.
                  —Le faltó decirle **dónde** guardarlo —dice Gheco.
              """,
              sugiere="`scanf(\"%d\", &edad)` lee un entero y lo guarda **en** `edad`: el `&` es la dirección de la variable. Sin `&`, `scanf` no sabe dónde escribir.",
              desafio="Completá el `scanf` para que lea la edad (la entrada ya está cargada).",
              entrada="30\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int edad = 0;
                      scanf("%d", ___);
                      printf("Edad de Chispa: %d\\n", edad);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int edad = 0;
                      scanf("%d", &edad);
                      printf("Edad de Chispa: %d\\n", edad);
                      return 0;
                  }
              ''',
              al_superar="Treinta. —Treinta y pico —corrige Chispa, que nunca da un número exacto si puede evitarlo.",
              imagen=["Una ventanilla de madera con un escriba enano detrás de una pila de fichas.", "Un goblin huye con un número 30 brillante.", CHISPA + " apoyado en la ventanilla."]),
            m(id="R01-N04-P3", titulo="Dos datos en una línea",
              lugar="La ventanilla de la Forja", personajes="Kira, Gheco, Tizón",
              carta="scanf con varios | scanf(\"%d %lf\", &a, &b) · %lf para leer un double · devuelve cuántos leyó",
              recompensa="xp 10, oro 10",
              escena="Tizón trae los datos de un pedido en una sola línea: cantidad de piezas y peso de cada una. Kira tiene que calcular el peso total.",
              sugiere="Un `scanf` puede leer varios datos: `%d` para un `int` y `%lf` para un `double` (en `scanf`, **con l**). Cada variable con su `&`.",
              desafio="Completá el formato y las direcciones.",
              entrada="4 2.5\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int piezas;
                      double peso;
                      scanf("___", ___, ___);
                      printf("%d piezas de %.1f kg: %.1f kg en total\\n", piezas, peso, piezas * peso);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int piezas;
                      double peso;
                      scanf("%d %lf", &piezas, &peso);
                      printf("%d piezas de %.1f kg: %.1f kg en total\\n", piezas, peso, piezas * peso);
                      return 0;
                  }
              ''',
              al_superar="Diez kilos. Tizón los pesa en la balanza de verdad, por las dudas: diez kilos y tres gramos. Se lo perdona.",
              imagen=["Una balanza de bronce con cuatro piezas de hierro.", TIZON + " compara la balanza con la libreta."]),
            m(id="R01-N04-P4", titulo="La entrada que no es un número",
              lugar="La ventanilla de la Forja", personajes="Kira, Gheco, Chispa",
              criatura="goblin",
              carta="Leer seguro | fgets lee la línea entera · sscanf la interpreta · si devuelve 1, era un número",
              recompensa="xp 15, oro 15",
              escena="Le piden a Chispa la altura y contesta «uno ochenta». El programa queda con cualquier cosa. Ferrum, desde lejos: —Si no revisás lo que te dan, forjás basura.",
              sugiere="La receta segura: `fgets` lee la línea entera y `sscanf` intenta sacar el número. `sscanf` devuelve cuántos datos pudo leer: si es 1, era un número.",
              desafio="Completá la condición para avisar cuando lo que llega no es un número.",
              entrada="uno ochenta\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[50];
                      int altura;
                      fgets(linea, sizeof linea, stdin);
                      if (sscanf(linea, "%d", &altura) ___) {
                          printf("Eso no es una altura: %s", linea);
                      } else {
                          printf("Altura: %d cm\\n", altura);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[50];
                      int altura;
                      fgets(linea, sizeof linea, stdin);
                      if (sscanf(linea, "%d", &altura) != 1) {
                          printf("Eso no es una altura: %s", linea);
                      } else {
                          printf("Altura: %d cm\\n", altura);
                      }
                      return 0;
                  }
              ''',
              al_superar="La ventanilla rechaza el «uno ochenta». Chispa lo vuelve a intentar con «alto». Tampoco. Al final escribe 180, resignado.",
              imagen=["Una ficha de papel con «uno ochenta» tachado en rojo.", CHISPA + " escribe en la ficha, resignado."]),
        ],
    },
    {
        "titulo": "R01-N05 · Condicionales",
        "misiones": [
            m(id="R01-N05-P1", titulo="El horno que se derrite",
              lugar="El horno de tres temperaturas", personajes="Kira, Gheco, Tizón",
              carta="if y else | if (condición) { … } else { … } · cada camino escrito · las llaves marcan qué va en cada uno",
              recompensa="xp 10, oro 10",
              escena="Kira escribió «si hace calor, más fuego» y nada más. El horno está blanco y la pizarra humea. Tizón llega con un balde de agua.",
              sugiere="Con `if … else` hay **dos caminos**: uno si la condición es verdadera, el otro si no. Sin `else`, cuando la condición es falsa no pasa nada.",
              desafio="Agregá el `else` para que, si el horno ya está muy caliente, se baje el fuego.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int grados = 1300;
                      if (grados < 1000) {
                          printf("mas fuego\\n");
                      } ___ {
                          printf("bajar el fuego\\n");
                      }
                      printf("horno a %d grados\\n", grados);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int grados = 1300;
                      if (grados < 1000) {
                          printf("mas fuego\\n");
                      } else {
                          printf("bajar el fuego\\n");
                      }
                      printf("horno a %d grados\\n", grados);
                      return 0;
                  }
              ''',
              al_superar="El horno baja a rojo. La pizarra deja de humear. Ferrum pasa, ve el balde de Tizón y no pregunta.",
              imagen=["Un horno al blanco vivo y una pizarra que humea.", TIZON + " corre con un balde de agua.", KIRA + " con cara de culpa."]),
            m(id="R01-N05-P2", titulo="El portero de los tres pisos",
              lugar="El horno de tres temperaturas", personajes="Kira, Gheco, Maese Ferrum",
              carta="else if | varios caminos en orden · se ejecuta el primero que se cumpla · el último else es «todo lo demás»",
              recompensa="xp 10, oro 10",
              escena="La Forja tiene tres pisos: brasas para los aprendices (menos de 50 piezas), yunques para los oficiales (hasta 200) y la cámara del maestro para el resto.",
              sugiere="Con `else if` se encadenan condiciones: C prueba la primera, si no se cumple la segunda, y así. El `else` final atrapa todo lo que sobra.",
              desafio="Completá las condiciones para mandar a Kira (140 piezas forjadas) a su piso.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int piezas = 140;
                      if (piezas ___ 50) {
                          printf("Piso de las brasas\\n");
                      } else if (piezas ___ 200) {
                          printf("Piso de los yunques\\n");
                      } else {
                          printf("Camara del maestro\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int piezas = 140;
                      if (piezas < 50) {
                          printf("Piso de las brasas\\n");
                      } else if (piezas <= 200) {
                          printf("Piso de los yunques\\n");
                      } else {
                          printf("Camara del maestro\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="Piso de los yunques. Kira esperaba la cámara del maestro. Ferrum: —Ciento cuarenta piezas y cuarenta y una a espadazos. Yunques.",
              imagen=["Una escalera de piedra con tres pisos iluminados: brasas, yunques y una cámara dorada arriba.", FERRUM + " señala el piso del medio."]),
            m(id="R01-N05-P3", titulo="Dos condiciones a la vez",
              lugar="El horno de tres temperaturas", personajes="Kira, Gheco, Tizón",
              carta="Lógicos | && (y) exige las dos · || (o) alcanza con una · ! niega",
              recompensa="xp 10, oro 10",
              escena="Para templar, el horno tiene que estar entre 800 y 1000 grados **y** tiene que haber agua en el balde. Tizón revisa las dos cosas antes de dejar entrar a Kira.",
              sugiere="`a && b` es verdadero solo si **las dos** lo son. `a || b`, si **alguna** lo es. `!a` niega.",
              desafio="Completá la condición: entre 800 y 1000 grados, y con agua.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int grados = 920;
                      int hay_agua = 1;
                      if (grados >= 800 ___ grados <= 1000 ___ hay_agua) {
                          printf("Se puede templar\\n");
                      } else {
                          printf("Todavia no\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int grados = 920;
                      int hay_agua = 1;
                      if (grados >= 800 && grados <= 1000 && hay_agua) {
                          printf("Se puede templar\\n");
                      } else {
                          printf("Todavia no\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="Se puede. Tizón le abre paso a Kira con una reverencia exagerada, y le recuerda que el agua es para el metal, no para él.",
              imagen=["Un balde de agua junto a un horno con un termómetro que marca 920.", TIZON + " hace una reverencia exagerada."]),
            m(id="R01-N05-P4", titulo="El menú del herrero",
              lugar="El mostrador de pedidos", personajes="Kira, Gheco, Chispa",
              carta="switch | switch (opción) { case 1: … break; } · default para lo que no está · sin break, sigue de largo",
              recompensa="xp 15, oro 15",
              escena="Chispa elige siempre la opción 2 del menú del herrero, y siempre le sale la 2 **y** la 3, y paga las dos. Sospecha de una estafa. Es un `break` que falta.",
              sugiere="En un `switch`, cada `case` necesita su `break;` al final: si no, sigue ejecutando el `case` de abajo.",
              desafio="Agregá el `break` que falta para que Chispa pague solo lo que pidió.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int opcion = 2;
                      switch (opcion) {
                      case 1:
                          printf("Afilar: 3 lingotes\\n");
                          break;
                      case 2:
                          printf("Templar: 5 lingotes\\n");
                      case 3:
                          printf("Pulir: 2 lingotes\\n");
                          break;
                      default:
                          printf("Esa opcion no existe\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int opcion = 2;
                      switch (opcion) {
                      case 1:
                          printf("Afilar: 3 lingotes\\n");
                          break;
                      case 2:
                          printf("Templar: 5 lingotes\\n");
                          break;
                      case 3:
                          printf("Pulir: 2 lingotes\\n");
                          break;
                      default:
                          printf("Esa opcion no existe\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="Cinco lingotes, solo templar. Chispa reclama los pulidos que pagó de más en todas las visitas anteriores. Ferrum le contesta con el martillo en la mano.",
              imagen=["Un cartel de madera con un menú: 1 Afilar, 2 Templar, 3 Pulir.", CHISPA + " reclama con una lista larguísima de recibos.", FERRUM + " con el martillo al hombro."]),
        ],
    },
]
