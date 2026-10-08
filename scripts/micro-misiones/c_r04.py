from genc import m
from c_r01 import KIRA, TIZON, FERRUM, CHISPA
from c_r01b import HULDA

ARCHIVO = "El Archivo de la Forja"
ARCHIVERO = "el Archivero (enano viejísimo y encorvado, barba blanca enrollada en el cinturón, anteojos gruesos, túnica marrón con mangas de cuero, pantuflas)"
GUARDIAN = "El Guardián del Archivo (autómata de hierro con forma de archivador gigante, cajones en el pecho, un candado por cabeza con un ojo naranja)"

NODOS = [
    {
        "titulo": "R04-N01 · Archivos de texto",
        "misiones": [
            m(id="R04-N01-P1", titulo="Lo que no está escrito en disco",
              lugar=ARCHIVO, personajes="Kira, Gheco, el Archivero",
              carta="Escribir un archivo | FILE *f = fopen(\"nombre\", \"w\") · fprintf(f, …) escribe · fclose(f) cierra y guarda · si fopen da NULL, no se pudo",
              recompensa="xp 10, oro 10",
              escena="""
                  El Archivero busca sus anteojos (los tiene puestos) y, mientras tanto, le enseña a Kira la regla del Archivo: —Lo que no está escrito en disco, no pasó.
              """,
              sugiere="`fopen(\"pedidos.txt\", \"w\")` crea el archivo para escribir y devuelve un `FILE *` (o `NULL`). `fprintf(f, …)` escribe como `printf`, y `fclose(f)` cierra.",
              desafio="Completá la apertura, la escritura y el cierre.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      FILE *f = ___;
                      if (f == NULL) {
                          printf("no se pudo abrir\\n");
                          return 1;
                      }
                      ___(f, "herradura;12\\n");
                      ___(f, "espada;3\\n");
                      ___;
                      printf("pedidos guardados\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      FILE *f = fopen("pedidos.txt", "w");
                      if (f == NULL) {
                          printf("no se pudo abrir\\n");
                          return 1;
                      }
                      fprintf(f, "herradura;12\\n");
                      fprintf(f, "espada;3\\n");
                      fclose(f);
                      printf("pedidos guardados\\n");
                      return 0;
                  }
              ''',
              al_superar="Guardado. El Archivero palpa la mesa buscando los anteojos, encuentra el archivo y lo aprueba con la nariz pegada al papel.",
              imagen=["Un salón de estanterías de hierro con libros encadenados.", ARCHIVERO.capitalize() + " busca algo en la mesa, con los anteojos puestos.", KIRA + " escribe en un libro."]),
            m(id="R04-N01-P2", titulo="Leer línea por línea",
              lugar=ARCHIVO, personajes="Kira, Gheco, el Archivero",
              carta="Leer un archivo | fopen con \"r\" · while (fgets(linea, sizeof linea, f) != NULL) · fgets da NULL al terminar",
              recompensa="xp 10, oro 10",
              escena="El Archivero quiere leer el libro de pedidos que escribió Kira, renglón por renglón, numerado.",
              sugiere="Con `\"r\"` se abre para leer. `fgets` lee un renglón por vuelta y devuelve `NULL` cuando no quedan más.",
              desafio="Completá la apertura para leer y la condición del bucle.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      FILE *f = fopen("pedidos.txt", "w");
                      if (f == NULL) {
                          return 1;
                      }
                      fprintf(f, "herradura;12\\nespada;3\\nescudo;5\\n");
                      fclose(f);

                      f = fopen("pedidos.txt", ___);
                      if (f == NULL) {
                          return 1;
                      }
                      char linea[50];
                      int n = 0;
                      while (___) {
                          n++;
                          printf("%d: %s", n, linea);
                      }
                      fclose(f);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      FILE *f = fopen("pedidos.txt", "w");
                      if (f == NULL) {
                          return 1;
                      }
                      fprintf(f, "herradura;12\\nespada;3\\nescudo;5\\n");
                      fclose(f);

                      f = fopen("pedidos.txt", "r");
                      if (f == NULL) {
                          return 1;
                      }
                      char linea[50];
                      int n = 0;
                      while (fgets(linea, sizeof linea, f) != NULL) {
                          n++;
                          printf("%d: %s", n, linea);
                      }
                      fclose(f);
                      return 0;
                  }
              ''',
              al_superar="Tres renglones, numerados. El Archivero los copia en su libro grande con una pluma que tiene detrás de la oreja. La busca primero un rato.",
              imagen=["Un libro de pedidos abierto con renglones numerados que brillan.", ARCHIVERO.capitalize() + " copia en un libro enorme."]),
            m(id="R04-N01-P3", titulo="Separar los campos",
              lugar=ARCHIVO, personajes="Kira, Gheco, Tizón",
              carta="Interpretar una línea | sscanf(linea, \"%[^;];%d\", nombre, &cantidad) · %[^;] lee hasta el ; · devuelve cuántos campos leyó",
              recompensa="xp 10, oro 10",
              escena="Cada renglón dice «pieza;cantidad». Tizón quiere el total de piezas pedidas, y saber cuál es la que más se pide.",
              sugiere="`sscanf(linea, \"%19[^;];%d\", pieza, &cant)` lee hasta el `;` (como mucho 19 letras) y después un entero. Si devuelve 2, el renglón está bien.",
              desafio="Completá el formato del `sscanf`.",
              inicial='''
                  #include <stdio.h>
                  #include <string.h>

                  int main(void)
                  {
                      FILE *f = fopen("pedidos.txt", "w");
                      if (f == NULL) {
                          return 1;
                      }
                      fprintf(f, "herradura;12\\nespada;3\\nclavo;40\\n");
                      fclose(f);

                      f = fopen("pedidos.txt", "r");
                      if (f == NULL) {
                          return 1;
                      }
                      char linea[50], pieza[20], mas_pedida[20] = "";
                      int cant, total = 0, maximo = 0;
                      while (fgets(linea, sizeof linea, f) != NULL) {
                          if (sscanf(linea, "___", pieza, &cant) == 2) {
                              total += cant;
                              if (cant > maximo) {
                                  maximo = cant;
                                  strcpy(mas_pedida, pieza);
                              }
                          }
                      }
                      fclose(f);
                      printf("total: %d piezas, la mas pedida: %s (%d)\\n", total, mas_pedida, maximo);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <string.h>

                  int main(void)
                  {
                      FILE *f = fopen("pedidos.txt", "w");
                      if (f == NULL) {
                          return 1;
                      }
                      fprintf(f, "herradura;12\\nespada;3\\nclavo;40\\n");
                      fclose(f);

                      f = fopen("pedidos.txt", "r");
                      if (f == NULL) {
                          return 1;
                      }
                      char linea[50], pieza[20], mas_pedida[20] = "";
                      int cant, total = 0, maximo = 0;
                      while (fgets(linea, sizeof linea, f) != NULL) {
                          if (sscanf(linea, "%19[^;];%d", pieza, &cant) == 2) {
                              total += cant;
                              if (cant > maximo) {
                                  maximo = cant;
                                  strcpy(mas_pedida, pieza);
                              }
                          }
                      }
                      fclose(f);
                      printf("total: %d piezas, la mas pedida: %s (%d)\\n", total, mas_pedida, maximo);
                      return 0;
                  }
              ''',
              al_superar="Cincuenta y cinco piezas; los clavos ganan por lejos. Tizón anota que hay que fabricar más clavos. Después anota que hay que medir los clavos.",
              imagen=["Un renglón «clavo;40» que se separa en dos piezas de luz.", TIZON + " anota en la libreta."]),
            m(id="R04-N01-P4", titulo="El renglón mal escrito",
              lugar=ARCHIVO, personajes="Kira, Gheco, Chispa",
              criatura="goblin",
              carta="Validar al leer | si sscanf no lee todos los campos, el renglón está mal · avisar con el número de línea y seguir",
              recompensa="xp 15, oro 15",
              escena="Chispa agregó renglones al libro de pedidos, a su manera: «martillo;muchos» y «yunque». Kira tiene que leer el libro sin que esos renglones rompan la cuenta.",
              sugiere="Si `sscanf` devuelve menos de 2, el renglón está mal: se avisa con su número y se sigue con el próximo.",
              desafio="Completá la condición del renglón válido.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      FILE *f = fopen("pedidos.txt", "w");
                      if (f == NULL) {
                          return 1;
                      }
                      fprintf(f, "herradura;12\\nmartillo;muchos\\nyunque\\nespada;3\\n");
                      fclose(f);

                      f = fopen("pedidos.txt", "r");
                      if (f == NULL) {
                          return 1;
                      }
                      char linea[50], pieza[20];
                      int cant, total = 0, n = 0;
                      while (fgets(linea, sizeof linea, f) != NULL) {
                          n++;
                          if (___) {
                              total += cant;
                          } else {
                              printf("linea %d mal escrita\\n", n);
                          }
                      }
                      fclose(f);
                      printf("total valido: %d\\n", total);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      FILE *f = fopen("pedidos.txt", "w");
                      if (f == NULL) {
                          return 1;
                      }
                      fprintf(f, "herradura;12\\nmartillo;muchos\\nyunque\\nespada;3\\n");
                      fclose(f);

                      f = fopen("pedidos.txt", "r");
                      if (f == NULL) {
                          return 1;
                      }
                      char linea[50], pieza[20];
                      int cant, total = 0, n = 0;
                      while (fgets(linea, sizeof linea, f) != NULL) {
                          n++;
                          if (sscanf(linea, "%19[^;];%d", pieza, &cant) == 2) {
                              total += cant;
                          } else {
                              printf("linea %d mal escrita\\n", n);
                          }
                      }
                      fclose(f);
                      printf("total valido: %d\\n", total);
                      return 0;
                  }
              ''',
              al_superar="Dos renglones marcados. Chispa dice que «muchos» es una cantidad perfectamente clara en el comercio. El Archivero lo mira por arriba de los anteojos.",
              imagen=["Un libro de pedidos con dos renglones tachados en rojo.", CHISPA + " se defiende con las manos abiertas."]),
        ],
    },
    {
        "titulo": "R04-N02 · Archivos binarios",
        "misiones": [
            m(id="R04-N02-P1", titulo="La caja sellada",
              lugar="Las cajas selladas del Archivo", personajes="Kira, Gheco, Tizón",
              carta="fwrite y fread | fwrite(&x, sizeof x, 1, f) guarda el struct tal cual · fread lo lee igual · modos \"wb\" y \"rb\"",
              recompensa="xp 10, oro 10",
              escena="Tizón abre una caja sellada con un editor de texto y ve jeroglíficos; jura que es un idioma antiguo y empieza a traducirlo. El Archivero le saca la caja con delicadeza: así no se lee.",
              sugiere="`fwrite(&ficha, sizeof ficha, 1, f)` guarda el struct byte por byte. `fread(&ficha, sizeof ficha, 1, f)` lo vuelve a cargar. Los modos llevan `b`: `\"wb\"` y `\"rb\"`.",
              desafio="Completá la escritura y la lectura.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      char metal[12];
                      int stock;
                  } Lingote;

                  int main(void)
                  {
                      Lingote guardado = { 7, "plomo", 40 };
                      FILE *f = fopen("caja.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      ___;
                      fclose(f);

                      Lingote leido;
                      f = fopen("caja.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      ___;
                      fclose(f);
                      printf("codigo %d: %s, stock %d\\n", leido.codigo, leido.metal, leido.stock);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      char metal[12];
                      int stock;
                  } Lingote;

                  int main(void)
                  {
                      Lingote guardado = { 7, "plomo", 40 };
                      FILE *f = fopen("caja.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      fwrite(&guardado, sizeof guardado, 1, f);
                      fclose(f);

                      Lingote leido;
                      f = fopen("caja.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      fread(&leido, sizeof leido, 1, f);
                      fclose(f);
                      printf("codigo %d: %s, stock %d\\n", leido.codigo, leido.metal, leido.stock);
                      return 0;
                  }
              ''',
              al_superar="Plomo, código 7, stock 40. Tizón guarda su traducción de los jeroglíficos en la libreta igual, «por si algún día sirve».",
              imagen=["Una caja de hierro sellada con una ficha adentro que brilla.", TIZON + " con una hoja llena de jeroglíficos inventados."]),
            m(id="R04-N02-P2", titulo="Directo a la ficha",
              lugar="Las cajas selladas del Archivo", personajes="Kira, Gheco, el Archivero",
              carta="fseek | fseek(f, k * (long) sizeof x, SEEK_SET) va directo al registro k · sin leer los anteriores",
              recompensa="xp 10, oro 10",
              escena="El Archivero quiere la ficha número 3 de una caja con 5 fichas, sin leer las tres de adelante. —El tiempo de un archivero es sagrado —dice, y se duerme un segundo.",
              sugiere="Los registros miden todos `sizeof(Lingote)`: el registro `k` empieza en el byte `k * sizeof(Lingote)`. `fseek(f, k * (long) sizeof x, SEEK_SET)` va ahí.",
              desafio="Completá el `fseek` para ir al registro 3 (contando desde 0).",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      int stock;
                  } Lingote;

                  int main(void)
                  {
                      FILE *f = fopen("caja.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      for (int i = 0; i < 5; i++) {
                          Lingote l = { 100 + i, (i + 1) * 10 };
                          fwrite(&l, sizeof l, 1, f);
                      }
                      fclose(f);

                      f = fopen("caja.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      Lingote l;
                      fseek(f, ___, SEEK_SET);
                      fread(&l, sizeof l, 1, f);
                      fclose(f);
                      printf("registro 3: codigo %d, stock %d\\n", l.codigo, l.stock);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      int stock;
                  } Lingote;

                  int main(void)
                  {
                      FILE *f = fopen("caja.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      for (int i = 0; i < 5; i++) {
                          Lingote l = { 100 + i, (i + 1) * 10 };
                          fwrite(&l, sizeof l, 1, f);
                      }
                      fclose(f);

                      f = fopen("caja.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      Lingote l;
                      fseek(f, 3 * (long) sizeof l, SEEK_SET);
                      fread(&l, sizeof l, 1, f);
                      fclose(f);
                      printf("registro 3: codigo %d, stock %d\\n", l.codigo, l.stock);
                      return 0;
                  }
              ''',
              al_superar="Código 103, stock 40, sin leer nada más. El Archivero se despierta justo para aprobarlo.",
              imagen=["Una caja con cinco fichas en fila; una salta directo a la mano de Kira.", ARCHIVERO.capitalize() + " dormitando en una silla."]),
            m(id="R04-N02-P3", titulo="Corregir una sola ficha",
              lugar="Las cajas selladas del Archivo", personajes="Kira, Gheco, Hulda",
              carta="Actualizar en el lugar | abrir con \"r+b\" · leer, cambiar, volver con fseek(f, -(long) sizeof x, SEEK_CUR) y escribir encima",
              recompensa="xp 15, oro 15",
              escena="Hulda devolvió 15 lingotes de plomo: hay que sumarlos al stock del código 102, sin reescribir toda la caja.",
              sugiere="Con `\"r+b\"` se lee y se escribe. Se lee la ficha, se cambia, se **vuelve** al principio de esa ficha con `fseek(f, -(long) sizeof l, SEEK_CUR)` y se escribe encima.",
              desafio="Completá la vuelta atrás.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      int stock;
                  } Lingote;

                  int main(void)
                  {
                      FILE *f = fopen("caja.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      for (int i = 0; i < 4; i++) {
                          Lingote l = { 100 + i, 20 };
                          fwrite(&l, sizeof l, 1, f);
                      }
                      fclose(f);

                      f = fopen("caja.dat", "r+b");
                      if (f == NULL) {
                          return 1;
                      }
                      Lingote l;
                      while (fread(&l, sizeof l, 1, f) == 1) {
                          if (l.codigo == 102) {
                              l.stock += 15;
                              fseek(f, ___, SEEK_CUR);
                              fwrite(&l, sizeof l, 1, f);
                              break;
                          }
                      }
                      fclose(f);

                      f = fopen("caja.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      while (fread(&l, sizeof l, 1, f) == 1) {
                          printf("%d: %d\\n", l.codigo, l.stock);
                      }
                      fclose(f);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      int stock;
                  } Lingote;

                  int main(void)
                  {
                      FILE *f = fopen("caja.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      for (int i = 0; i < 4; i++) {
                          Lingote l = { 100 + i, 20 };
                          fwrite(&l, sizeof l, 1, f);
                      }
                      fclose(f);

                      f = fopen("caja.dat", "r+b");
                      if (f == NULL) {
                          return 1;
                      }
                      Lingote l;
                      while (fread(&l, sizeof l, 1, f) == 1) {
                          if (l.codigo == 102) {
                              l.stock += 15;
                              fseek(f, -(long) sizeof l, SEEK_CUR);
                              fwrite(&l, sizeof l, 1, f);
                              break;
                          }
                      }
                      fclose(f);

                      f = fopen("caja.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      while (fread(&l, sizeof l, 1, f) == 1) {
                          printf("%d: %d\\n", l.codigo, l.stock);
                      }
                      fclose(f);
                      return 0;
                  }
              ''',
              al_superar="El 102 queda en 35 y el resto, intacto. Hulda tacha la devolución de su tablilla. Por una vez, sin chistes.",
              imagen=["Una ficha que se levanta de una caja, cambia un número y vuelve a su lugar.", HULDA + " tacha una línea de su tablilla."]),
            m(id="R04-N02-P4", titulo="La B de bajado",
              lugar="Las cajas selladas del Archivo", personajes="Kira, Gheco, el Archivero",
              carta="Baja lógica | un campo estado: 'A' activo, 'B' de baja · dar de baja es cambiar el campo y reescribir · los listados muestran solo los activos",
              recompensa="xp 15, oro 15",
              escena="Hay que sacar del Archivo el lingote 101, que salió falso. El Archivero no deja borrar nada: —En el Archivo nada se tira. Ponele una **B**.",
              sugiere="La baja lógica cambia el estado a `'B'` y reescribe la ficha. Al listar, se muestran solo las que tienen `'A'`.",
              desafio="Completá la baja y el filtro del listado.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      char estado;
                  } Lingote;

                  int main(void)
                  {
                      FILE *f = fopen("caja.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      for (int i = 0; i < 3; i++) {
                          Lingote l = { 100 + i, 'A' };
                          fwrite(&l, sizeof l, 1, f);
                      }
                      fclose(f);

                      f = fopen("caja.dat", "r+b");
                      if (f == NULL) {
                          return 1;
                      }
                      Lingote l;
                      while (fread(&l, sizeof l, 1, f) == 1) {
                          if (l.codigo == 101) {
                              ___;
                              fseek(f, -(long) sizeof l, SEEK_CUR);
                              fwrite(&l, sizeof l, 1, f);
                              break;
                          }
                      }
                      fclose(f);

                      f = fopen("caja.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      printf("activos:");
                      while (fread(&l, sizeof l, 1, f) == 1) {
                          if (___) {
                              printf(" %d", l.codigo);
                          }
                      }
                      printf("\\n");
                      fclose(f);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      char estado;
                  } Lingote;

                  int main(void)
                  {
                      FILE *f = fopen("caja.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      for (int i = 0; i < 3; i++) {
                          Lingote l = { 100 + i, 'A' };
                          fwrite(&l, sizeof l, 1, f);
                      }
                      fclose(f);

                      f = fopen("caja.dat", "r+b");
                      if (f == NULL) {
                          return 1;
                      }
                      Lingote l;
                      while (fread(&l, sizeof l, 1, f) == 1) {
                          if (l.codigo == 101) {
                              l.estado = 'B';
                              fseek(f, -(long) sizeof l, SEEK_CUR);
                              fwrite(&l, sizeof l, 1, f);
                              break;
                          }
                      }
                      fclose(f);

                      f = fopen("caja.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      printf("activos:");
                      while (fread(&l, sizeof l, 1, f) == 1) {
                          if (l.estado == 'A') {
                              printf(" %d", l.codigo);
                          }
                      }
                      printf("\\n");
                      fclose(f);
                      return 0;
                  }
              ''',
              al_superar="El 101 sigue en la caja, con su B, pero ya no aparece. El Archivero asiente: —Nada se tira. Todo se recuerda. —Y se olvida dónde dejó la pluma.",
              imagen=["Una ficha con una B grande estampada en rojo, guardada entre otras fichas.", ARCHIVERO.capitalize() + " estampa el sello."]),
        ],
    },
    {
        "titulo": "R04-N03 · Programas en varios archivos",
        "misiones": [
            m(id="R04-N03-P1", titulo="La tapa del taller",
              lugar="Las salas del Archivo", personajes="Kira, Gheco, Tizón",
              carta="Prototipos en el .h | el .h promete qué funciones hay · el .c las cumple · main solo conoce la tapa",
              recompensa="xp 10, oro 10",
              escena="Cada taller tiene una **tapa** que dice qué ofrece. En este pergamino van las tres partes juntas, una abajo de la otra: la tapa (`dado.h`), el taller (`dado.c`) y quien lo usa (`main.c`).",
              sugiere="En un `.h` van los **prototipos**: la promesa de lo que hay. El `.c` del módulo escribe las funciones. Acá, como todo está en un solo archivo, la tapa va arriba.",
              desafio="Escribí en la «tapa» el prototipo de la función que usa `main`.",
              inicial='''
                  #include <stdio.h>

                  /* ---- dado.h: la tapa ---- */
                  ___

                  /* ---- main.c ---- */
                  int main(void)
                  {
                      printf("dado de 20 caras: %d\\n", cara_maxima(20));
                      return 0;
                  }

                  /* ---- dado.c: el taller ---- */
                  int cara_maxima(int caras)
                  {
                      return caras;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  /* ---- dado.h: la tapa ---- */
                  int cara_maxima(int caras);

                  /* ---- main.c ---- */
                  int main(void)
                  {
                      printf("dado de 20 caras: %d\\n", cara_maxima(20));
                      return 0;
                  }

                  /* ---- dado.c: el taller ---- */
                  int cara_maxima(int caras)
                  {
                      return caras;
                  }
              ''',
              al_superar="La tapa promete, el taller cumple, y main no necesita saber cómo. Tizón dibuja las tres salas en la libreta, con flechas.",
              imagen=["Tres salas del Archivo unidas por puertas: una tapa, un taller y una sala principal.", TIZON + " dibuja un diagrama con flechas."]),
            m(id="R04-N03-P2", titulo="Lo privado del taller",
              lugar="Las salas del Archivo", personajes="Kira, Gheco, Chispa",
              carta="static afuera de una función | la función o variable existe solo en su archivo · nadie de afuera la toca · es la parte privada del módulo",
              recompensa="xp 10, oro 10",
              escena="Chispa encontró la función interna del taller de dados que **carga** el dado, y la usa desde afuera para ganar en la taberna. Hay que esconderla.",
              sugiere="Una función `static` fuera de todas las funciones solo se puede usar **en ese archivo**. Es lo privado del módulo; lo público va en el `.h`.",
              desafio="Marcá como `static` la variable y la función internas del taller.",
              inicial='''
                  #include <stdio.h>

                  /* ---- dado.c: el taller ---- */
                  ___ int semilla = 7;

                  ___ int mezclar(void)
                  {
                      semilla = (semilla * 17 + 5) % 101;
                      return semilla;
                  }

                  int tirar(void)
                  {
                      return mezclar() % 6 + 1;
                  }

                  /* ---- main.c ---- */
                  int main(void)
                  {
                      int a = tirar();
                      int b = tirar();
                      int c = tirar();
                      printf("%d %d %d\\n", a, b, c);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  /* ---- dado.c: el taller ---- */
                  static int semilla = 7;

                  static int mezclar(void)
                  {
                      semilla = (semilla * 17 + 5) % 101;
                      return semilla;
                  }

                  int tirar(void)
                  {
                      return mezclar() % 6 + 1;
                  }

                  /* ---- main.c ---- */
                  int main(void)
                  {
                      int a = tirar();
                      int b = tirar();
                      int c = tirar();
                      printf("%d %d %d\\n", a, b, c);
                      return 0;
                  }
              ''',
              al_superar="La mezcla queda escondida en el taller. Chispa vuelve a perder en la taberna, como cualquiera. Dice que el dado está cargado. No lo está.",
              imagen=["Un taller con una puerta interna cerrada con candado.", CHISPA + " intenta espiar por la cerradura."]),
            m(id="R04-N03-P3", titulo="La tapa que se pega dos veces",
              lugar="Las salas del Archivo", personajes="Kira, Gheco, Tizón",
              carta="Guardas de inclusión | #ifndef DADO_H / #define DADO_H / … / #endif · la tapa se pega una sola vez aunque se incluya dos",
              recompensa="xp 15, oro 15",
              escena="Tizón y Kira incluyeron la misma tapa en dos lugares sin avisarse, y el Horno se queja: el struct `Dado` está **definido dos veces**.",
              sugiere="La guarda `#ifndef DADO_H` / `#define DADO_H` / `#endif` hace que el contenido se pegue **una sola vez**: la segunda, `DADO_H` ya está definido y se saltea.",
              desafio="Poné la guarda alrededor de la tapa (está pegada dos veces a propósito).",
              inicial='''
                  #include <stdio.h>

                  /* ---- dado.h (incluido por primera vez) ---- */
                  typedef struct {
                      int caras;
                  } Dado;

                  /* ---- dado.h (incluido otra vez, desde otro archivo) ---- */
                  typedef struct {
                      int caras;
                  } Dado;

                  int main(void)
                  {
                      Dado d = { 20 };
                      printf("dado de %d caras\\n", d.caras);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  /* ---- dado.h (incluido por primera vez) ---- */
                  #ifndef DADO_H
                  #define DADO_H
                  typedef struct {
                      int caras;
                  } Dado;
                  #endif

                  /* ---- dado.h (incluido otra vez, desde otro archivo) ---- */
                  #ifndef DADO_H
                  #define DADO_H
                  typedef struct {
                      int caras;
                  } Dado;
                  #endif

                  int main(void)
                  {
                      Dado d = { 20 };
                      printf("dado de %d caras\\n", d.caras);
                      return 0;
                  }
              ''',
              al_superar="Compila. La segunda copia de la tapa se saltea sola. Tizón y Kira se prometen avisarse. No lo van a cumplir, pero ya no importa.",
              imagen=["Dos copias de la misma tapa; una se desvanece al entrar al horno.", TIZON + " y " + KIRA + " se dan la mano."]),
            m(id="R04-N03-P4", titulo="La variable de todos",
              lugar="Las salas del Archivo", personajes="Kira, Gheco, Maese Ferrum",
              carta="extern | extern int x; dice «existe, definida en otro archivo» · se define UNA sola vez, con su valor · las globales compartidas, pocas",
              recompensa="xp 15, oro 15",
              escena="Ferrum quiere que todos los talleres sepan la dificultad de la temporada, sin pasarla por parámetro a cada función. Una sola variable, compartida.",
              sugiere="`extern int dificultad;` (en el `.h`) avisa que existe. Se **define** una sola vez en un `.c`: `int dificultad = 3;`. Acá, la declaración va arriba y la definición abajo.",
              desafio="Escribí la declaración `extern` y la definición.",
              inicial='''
                  #include <stdio.h>

                  /* ---- forja.h ---- */
                  ___

                  /* ---- taller.c ---- */
                  int danio_con_dificultad(int base)
                  {
                      return base * dificultad;
                  }

                  /* ---- main.c ---- */
                  int main(void)
                  {
                      printf("danio: %d\\n", danio_con_dificultad(10));
                      return 0;
                  }

                  /* ---- forja.c: la definicion, una sola vez ---- */
                  ___
              ''',
              solucion='''
                  #include <stdio.h>

                  /* ---- forja.h ---- */
                  extern int dificultad;

                  /* ---- taller.c ---- */
                  int danio_con_dificultad(int base)
                  {
                      return base * dificultad;
                  }

                  /* ---- main.c ---- */
                  int main(void)
                  {
                      printf("danio: %d\\n", danio_con_dificultad(10));
                      return 0;
                  }

                  /* ---- forja.c: la definicion, una sola vez ---- */
                  int dificultad = 3;
              ''',
              al_superar="Daño 30 en todos los talleres. Ferrum advierte: —Una global compartida es como un yunque en el medio del patio. Útil, y todos se lo llevan por delante.",
              imagen=["Un tablero en el patio con el número 3 grabado, visible desde todos los talleres.", FERRUM + " señala el tablero."]),
        ],
    },
    {
        "titulo": "R04-N04 · Argumentos de la línea de comandos",
        "misiones": [
            m(id="R04-N04-P1", titulo="La orden al encender",
              lugar="La ventanilla del Archivo", personajes="Kira, Gheco, Chispa",
              carta="argc y argv | int main(int argc, char *argv[]) · argv[0] es el programa · argv[1] en adelante, lo que se escribió después",
              recompensa="xp 10, oro 10",
              escena="""
                  Chispa grita sus pedidos desde la puerta, todo junto. Los herreros viejos le dan la orden a la herramienta **al encenderla**: `./forja templar 900`.
                  En el navegador no hay terminal: acá el `main` le pasa a `forja` un `argv` armado a mano, como si se hubiera escrito esa línea.
              """,
              sugiere="`argc` dice cuántos textos hay y `argv[i]` es cada uno. `argv[0]` es el nombre del programa; las palabras que se escribieron después empiezan en `argv[1]`.",
              desafio="Mostrá la orden y el valor recibidos.",
              inicial='''
                  #include <stdio.h>

                  int forja(int argc, char *argv[])
                  {
                      printf("%d palabras\\n", argc);
                      printf("orden: %s\\n", ___);
                      printf("valor: %s\\n", ___);
                      return 0;
                  }

                  int main(void)
                  {
                      char *argv[] = { "forja", "templar", "900" };
                      return forja(3, argv);
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int forja(int argc, char *argv[])
                  {
                      printf("%d palabras\\n", argc);
                      printf("orden: %s\\n", argv[1]);
                      printf("valor: %s\\n", argv[2]);
                      return 0;
                  }

                  int main(void)
                  {
                      char *argv[] = { "forja", "templar", "900" };
                      return forja(3, argv);
                  }
              ''',
              al_superar="«templar» y «900», separados. Chispa intenta gritar «templar novecientos tres veces la de siempre» como una sola palabra. No entra.",
              imagen=["Una terminal de hierro con la línea ./forja templar 900 escrita en luz cian.", CHISPA + " grita desde la puerta del Archivo."]),
            m(id="R04-N04-P2", titulo="El número que viene como texto",
              lugar="La ventanilla del Archivo", personajes="Kira, Gheco, Tizón",
              carta="Convertir argumentos | todo en argv es texto · strtol(s, &fin, 10) lo convierte · si *fin no es '\\0', había letras",
              recompensa="xp 15, oro 15",
              escena="Tizón quiere templar a «900» grados, pero el programa recibe el **texto** «900», no el número. Y Chispa una vez escribió «hola» como temperatura.",
              sugiere="`long t = strtol(argv[2], &fin, 10);` convierte el texto. Si `*fin != '\\0'`, quedaron letras sin convertir: no era un número.",
              desafio="Completá la comprobación de lo que sobró.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int forja(int argc, char *argv[])
                  {
                      if (argc != 3) {
                          printf("uso: forja templar GRADOS\\n");
                          return 1;
                      }
                      char *fin;
                      long grados = strtol(argv[2], &fin, 10);
                      if (___) {
                          printf("\\"%s\\" no es una temperatura\\n", argv[2]);
                          return 1;
                      }
                      printf("templando a %ld grados\\n", grados);
                      return 0;
                  }

                  int main(void)
                  {
                      char *bien[] = { "forja", "templar", "900" };
                      char *mal[] = { "forja", "templar", "hola" };
                      forja(3, bien);
                      forja(3, mal);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int forja(int argc, char *argv[])
                  {
                      if (argc != 3) {
                          printf("uso: forja templar GRADOS\\n");
                          return 1;
                      }
                      char *fin;
                      long grados = strtol(argv[2], &fin, 10);
                      if (*fin != '\\0' || fin == argv[2]) {
                          printf("\\"%s\\" no es una temperatura\\n", argv[2]);
                          return 1;
                      }
                      printf("templando a %ld grados\\n", grados);
                      return 0;
                  }

                  int main(void)
                  {
                      char *bien[] = { "forja", "templar", "900" };
                      char *mal[] = { "forja", "templar", "hola" };
                      forja(3, bien);
                      forja(3, mal);
                      return 0;
                  }
              ''',
              al_superar="Novecientos sí, «hola» no. Tizón le explica a Chispa la diferencia entre un número y un saludo. Chispa no está convencido.",
              imagen=["Dos papeles en la ventanilla: «900» aprobado y «hola» rechazado.", TIZON + " explica con el dedo en alto."]),
            m(id="R04-N04-P3", titulo="Las opciones con guion",
              lugar="La ventanilla del Archivo", personajes="Kira, Gheco, el Archivero",
              carta="Opciones | recorrer argv desde 1 · strcmp(argv[i], \"-n\") == 0 detecta la opción · su valor está en argv[i + 1]",
              recompensa="xp 15, oro 15",
              escena="El Archivero usa su herramienta con opciones: `contar -n 3 libro`. La `-n` dice cuántas veces. Si no está, es una vez.",
              sugiere="Se recorre `argv` desde 1: si `strcmp(argv[i], \"-n\") == 0` y hay un argumento más, se toma `argv[i + 1]` y se saltea (`i++`).",
              desafio="Completá la detección de `-n`.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  int contar(int argc, char *argv[])
                  {
                      int veces = 1;
                      const char *libro = "(ninguno)";
                      for (int i = 1; i < argc; i++) {
                          if (___ && i + 1 < argc) {
                              veces = atoi(argv[i + 1]);
                              i++;
                          } else {
                              libro = argv[i];
                          }
                      }
                      printf("contar %s, %d %s\\n", libro, veces, veces == 1 ? "vez" : "veces");
                      return 0;
                  }

                  int main(void)
                  {
                      char *a[] = { "contar", "-n", "3", "pedidos" };
                      char *b[] = { "contar", "planos" };
                      contar(4, a);
                      contar(2, b);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>
                  #include <string.h>

                  int contar(int argc, char *argv[])
                  {
                      int veces = 1;
                      const char *libro = "(ninguno)";
                      for (int i = 1; i < argc; i++) {
                          if (strcmp(argv[i], "-n") == 0 && i + 1 < argc) {
                              veces = atoi(argv[i + 1]);
                              i++;
                          } else {
                              libro = argv[i];
                          }
                      }
                      printf("contar %s, %d %s\\n", libro, veces, veces == 1 ? "vez" : "veces");
                      return 0;
                  }

                  int main(void)
                  {
                      char *a[] = { "contar", "-n", "3", "pedidos" };
                      char *b[] = { "contar", "planos" };
                      contar(4, a);
                      contar(2, b);
                      return 0;
                  }
              ''',
              al_superar="Tres veces los pedidos, una vez los planos. El Archivero cuenta igual a mano, «por costumbre», y le da lo mismo.",
              imagen=["Una herramienta del Archivo con una perilla marcada -n.", ARCHIVERO.capitalize() + " cuenta libros con el dedo."]),
            m(id="R04-N04-P4", titulo="Cómo terminó",
              lugar="La ventanilla del Archivo", personajes="Kira, Gheco, Tizón",
              carta="Código de salida | return EXIT_SUCCESS (0) si todo bien · EXIT_FAILURE (1) si no · los errores van a stderr con fprintf(stderr, …)",
              recompensa="xp 15, oro 15",
              escena="Tizón encadena herramientas: si la primera falla, la segunda no tiene que arrancar. Para eso, cada herramienta tiene que **decir cómo terminó**.",
              sugiere="`return EXIT_SUCCESS;` (0) avisa que salió bien y `return EXIT_FAILURE;` (1), que falló. Los dos están en `stdlib.h`.",
              desafio="Completá los dos códigos de salida.",
              inicial='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int templar(int grados)
                  {
                      if (grados < 600 || grados > 1200) {
                          return ___;
                      }
                      return ___;
                  }

                  int main(void)
                  {
                      int pruebas[3] = { 900, 50, 1100 };
                      for (int i = 0; i < 3; i++) {
                          int codigo = templar(pruebas[i]);
                          printf("templar %d -> codigo %d (%s)\\n", pruebas[i], codigo, codigo == EXIT_SUCCESS ? "sigue la siguiente" : "se corta la cadena");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <stdlib.h>

                  int templar(int grados)
                  {
                      if (grados < 600 || grados > 1200) {
                          return EXIT_FAILURE;
                      }
                      return EXIT_SUCCESS;
                  }

                  int main(void)
                  {
                      int pruebas[3] = { 900, 50, 1100 };
                      for (int i = 0; i < 3; i++) {
                          int codigo = templar(pruebas[i]);
                          printf("templar %d -> codigo %d (%s)\\n", pruebas[i], codigo, codigo == EXIT_SUCCESS ? "sigue la siguiente" : "se corta la cadena");
                      }
                      return 0;
                  }
              ''',
              al_superar="Cero, uno, cero. Tizón encadena tres herramientas y, cuando una falla, las otras se quedan quietas. Le parece hermoso. Lo dice en voz alta.",
              imagen=["Tres herramientas encadenadas por cables; la del medio con una luz roja.", TIZON + " emocionado frente a la cadena."]),
        ],
    },
    {
        "titulo": "R04-N05 · El menú de consola",
        "misiones": [
            m(id="R04-N05-P1", titulo="El cartel que vuelve",
              lugar="El mostrador del Archivero", personajes="Kira, Gheco, el Archivero",
              carta="Bucle de menú | do { mostrar; leer; hacer } while (opcion != 0); · cada vuelta cambia algo · 0 sale",
              recompensa="xp 10, oro 10",
              escena="El mostrador del Archivero tiene un cartel con opciones: 1 prestar, 2 devolver, 0 salir. Cada vez que alguien elige, algo cambia y el cartel vuelve a aparecer.",
              sugiere="Un menú es un `do … while` que muestra, lee la opción y la atiende con un `switch`, hasta que la opción sea 0.",
              desafio="Completá la condición del bucle.",
              entrada="1\n1\n2\n0\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int prestados = 0;
                      int opcion;
                      do {
                          printf("[1] prestar [2] devolver [0] salir\\n");
                          if (scanf("%d", &opcion) != 1) {
                              break;
                          }
                          switch (opcion) {
                          case 1: prestados++; break;
                          case 2: prestados--; break;
                          }
                          printf("prestados: %d\\n", prestados);
                      } while (___);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int prestados = 0;
                      int opcion;
                      do {
                          printf("[1] prestar [2] devolver [0] salir\\n");
                          if (scanf("%d", &opcion) != 1) {
                              break;
                          }
                          switch (opcion) {
                          case 1: prestados++; break;
                          case 2: prestados--; break;
                          }
                          printf("prestados: %d\\n", prestados);
                      } while (opcion != 0);
                      return 0;
                  }
              ''',
              al_superar="Uno prestado al cerrar. El Archivero lo anota en su libro, que también está prestado, aunque no se acuerda a quién.",
              imagen=["Un mostrador de madera con un cartel de opciones numeradas.", ARCHIVERO.capitalize() + " detrás del mostrador."]),
            m(id="R04-N05-P2", titulo="La opción 8",
              lugar="El mostrador del Archivero", personajes="Kira, Gheco, Chispa",
              criatura="goblin",
              carta="default y validación | default: atrapa las opciones que no existen · sin default, el menú hace nada en silencio",
              recompensa="xp 10, oro 10",
              escena="Chispa elige «8», que no existe, y el mostrador no dice nada: Chispa queda esperando, convencido de que pidió algo.",
              sugiere="El `default:` del `switch` atrapa todo lo que no es una opción válida, para avisar.",
              desafio="Agregá el `default` que avisa.",
              entrada="8\n1\n0\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int opcion;
                      do {
                          if (scanf("%d", &opcion) != 1) {
                              break;
                          }
                          switch (opcion) {
                          case 1: printf("prestado\\n"); break;
                          case 0: printf("chau\\n"); break;
                          ___: printf("la opcion %d no existe\\n", opcion);
                          }
                      } while (opcion != 0);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      int opcion;
                      do {
                          if (scanf("%d", &opcion) != 1) {
                              break;
                          }
                          switch (opcion) {
                          case 1: printf("prestado\\n"); break;
                          case 0: printf("chau\\n"); break;
                          default: printf("la opcion %d no existe\\n", opcion);
                          }
                      } while (opcion != 0);
                      return 0;
                  }
              ''',
              al_superar="«La opción 8 no existe». Chispa insiste en que la 8 era «lo de siempre». El mostrador, por suerte, no sabe qué es lo de siempre.",
              imagen=["Un cartel de opciones con un 8 escrito a mano por fuera, tachado.", CHISPA + " señala el 8."]),
            m(id="R04-N05-P3", titulo="Ni con letras",
              lugar="El mostrador del Archivero", personajes="Kira, Gheco, Chispa",
              criatura="goblin",
              carta="Menú a prueba de todo | leer con fgets · sscanf para la opción · una línea mala no traba el menú",
              recompensa="xp 15, oro 15",
              escena="Chispa escribe «hola» en lugar de un número. Con `scanf`, el menú se traba para siempre leyendo la misma letra. Kira arma un mostrador que no se traba con nada.",
              sugiere="Se lee la línea entera con `fgets` y se interpreta con `sscanf`. Si no es un número, se avisa y la línea ya se consumió: la próxima vuelta lee la siguiente.",
              desafio="Completá la lectura segura de la opción.",
              entrada="hola\n\n1\n0\n",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[30];
                      int opcion = -1;
                      while (opcion != 0 && fgets(linea, sizeof linea, stdin) != NULL) {
                          if (___) {
                              printf("eso no es una opcion\\n");
                              continue;
                          }
                          printf(opcion == 1 ? "prestado\\n" : opcion == 0 ? "chau\\n" : "no existe\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      char linea[30];
                      int opcion = -1;
                      while (opcion != 0 && fgets(linea, sizeof linea, stdin) != NULL) {
                          if (sscanf(linea, "%d", &opcion) != 1) {
                              printf("eso no es una opcion\\n");
                              continue;
                          }
                          printf(opcion == 1 ? "prestado\\n" : opcion == 0 ? "chau\\n" : "no existe\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="Ni con «hola», ni con un Enter vacío. Chispa lo intenta durante una hora. No lo rompe. Se va ofendido.",
              imagen=[CHISPA + " aporrea el mostrador con las dos manos, frustrado.", KIRA + " sonríe con los brazos cruzados."]),
            m(id="R04-N05-P4", titulo="Guardar al salir",
              lugar="El mostrador del Archivero", personajes="Kira, Gheco, el Archivero",
              carta="Persistir | cargar del archivo al empezar · guardar al salir · si el archivo no existe, se empieza de cero",
              recompensa="xp 15, oro 15",
              escena="Cada noche se apaga el horno y el mostrador se olvida de todo. El Archivero quiere que, al volver a abrir, los préstamos sigan ahí.",
              sugiere="Al empezar, si `fopen(…, \"r\")` funciona, se lee la cantidad guardada. Al salir, se abre con `\"w\"` y se escribe. Acá el programa se ejecuta dos veces seguidas (dos «días»).",
              desafio="Completá la carga y el guardado.",
              inicial='''
                  #include <stdio.h>

                  int cargar(void)
                  {
                      int prestados = 0;
                      FILE *f = fopen("mostrador.txt", "r");
                      if (f != NULL) {
                          ___;
                          fclose(f);
                      }
                      return prestados;
                  }

                  void guardar(int prestados)
                  {
                      FILE *f = fopen("mostrador.txt", "w");
                      if (f != NULL) {
                          ___;
                          fclose(f);
                      }
                  }

                  void un_dia(int dia, int nuevos)
                  {
                      int prestados = cargar();
                      prestados += nuevos;
                      printf("dia %d: %d prestados\\n", dia, prestados);
                      guardar(prestados);
                  }

                  int main(void)
                  {
                      remove("mostrador.txt");
                      un_dia(1, 3);
                      un_dia(2, 2);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int cargar(void)
                  {
                      int prestados = 0;
                      FILE *f = fopen("mostrador.txt", "r");
                      if (f != NULL) {
                          if (fscanf(f, "%d", &prestados) != 1) {
                              prestados = 0;
                          }
                          fclose(f);
                      }
                      return prestados;
                  }

                  void guardar(int prestados)
                  {
                      FILE *f = fopen("mostrador.txt", "w");
                      if (f != NULL) {
                          fprintf(f, "%d\\n", prestados);
                          fclose(f);
                      }
                  }

                  void un_dia(int dia, int nuevos)
                  {
                      int prestados = cargar();
                      prestados += nuevos;
                      printf("dia %d: %d prestados\\n", dia, prestados);
                      guardar(prestados);
                  }

                  int main(void)
                  {
                      remove("mostrador.txt");
                      un_dia(1, 3);
                      un_dia(2, 2);
                      return 0;
                  }
              ''',
              al_superar="Tres el primer día, cinco el segundo. El mostrador se acuerda. El Archivero, no, pero para eso está el mostrador.",
              imagen=["Un mostrador de noche, con el horno apagado, y un libro que brilla.", ARCHIVERO.capitalize() + " durmiendo sobre el mostrador."]),
        ],
    },
    {
        "titulo": "R04-N06 · Jefe: el Guardián del Archivo",
        "misiones": [
            m(id="R04-N06-P1", titulo="¿Abriste? ¿Cerraste?",
              lugar="La puerta de la bóveda", personajes="Kira, Gheco, Tizón",
              criatura="dragon",
              carta="Abrir y cerrar | cada fopen con su fclose · si fopen falla, avisar y no seguir · el Guardián cuenta",
              recompensa="xp 15, oro 15",
              escena="""
                  En la puerta de la bóveda espera el **Guardián del Archivo**: un autómata con forma de archivador gigante y un candado por cabeza. —¿Abriste? ¿Cerraste? —repite, con ruido de cajones.
                  Kira se olvida de cerrar un archivo y el Guardián le cierra el cajón en los dedos.
              """,
              sugiere="Cada `fopen` necesita su `fclose`. Si un archivo no se puede abrir (no existe), `fopen` da `NULL`: se avisa y no se usa.",
              desafio="Completá el cierre que falta y el aviso del archivo que no existe.",
              inicial='''
                  #include <stdio.h>

                  int main(void)
                  {
                      FILE *f = fopen("inventario.txt", "w");
                      if (f == NULL) {
                          return 1;
                      }
                      fprintf(f, "espada reforjada\\n");
                      ___;

                      FILE *g = fopen("no_existe.txt", "r");
                      if (___) {
                          printf("no_existe.txt: no se pudo abrir\\n");
                      } else {
                          fclose(g);
                      }
                      printf("el guardian cuenta: todo cerrado\\n");
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  int main(void)
                  {
                      FILE *f = fopen("inventario.txt", "w");
                      if (f == NULL) {
                          return 1;
                      }
                      fprintf(f, "espada reforjada\\n");
                      fclose(f);

                      FILE *g = fopen("no_existe.txt", "r");
                      if (g == NULL) {
                          printf("no_existe.txt: no se pudo abrir\\n");
                      } else {
                          fclose(g);
                      }
                      printf("el guardian cuenta: todo cerrado\\n");
                      return 0;
                  }
              ''',
              al_superar="Todo cerrado. El Guardián abre un cajón del pecho, el primero de muchos. Tizón le sopla los dedos a Kira.",
              imagen=[GUARDIAN + " frente a una puerta de bóveda.", KIRA + " se sopla los dedos.", TIZON + " a su lado."]),
            m(id="R04-N06-P2", titulo="El inventario que vuelve igual",
              lugar="La puerta de la bóveda", personajes="Kira, Gheco, el Archivero",
              carta="Guardar y cargar un array de structs | fwrite(v, sizeof v[0], n, f) guarda los n de una vez · fread devuelve cuántos leyó",
              recompensa="xp 15, oro 15",
              escena="El Guardián pide que Kira guarde su inventario, apague todo… y que al volver esté **exactamente** igual.",
              sugiere="`fwrite(v, sizeof v[0], n, f)` escribe los `n` structs de una vez. `fread(w, sizeof w[0], MAX, f)` lee hasta `MAX` y **devuelve cuántos** leyó.",
              desafio="Completá la escritura y la lectura del array.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      char item[20];
                      int cantidad;
                  } Item;

                  int main(void)
                  {
                      Item inventario[3] = { { "espada", 1 }, { "pocion", 4 }, { "amuleto", 1 } };
                      FILE *f = fopen("inventario.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      ___;
                      fclose(f);

                      Item vuelto[10];
                      f = fopen("inventario.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      int n = ___;
                      fclose(f);
                      for (int i = 0; i < n; i++) {
                          printf("%-8s x%d\\n", vuelto[i].item, vuelto[i].cantidad);
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      char item[20];
                      int cantidad;
                  } Item;

                  int main(void)
                  {
                      Item inventario[3] = { { "espada", 1 }, { "pocion", 4 }, { "amuleto", 1 } };
                      FILE *f = fopen("inventario.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      fwrite(inventario, sizeof inventario[0], 3, f);
                      fclose(f);

                      Item vuelto[10];
                      f = fopen("inventario.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      int n = (int) fread(vuelto, sizeof vuelto[0], 10, f);
                      fclose(f);
                      for (int i = 0; i < n; i++) {
                          printf("%-8s x%d\\n", vuelto[i].item, vuelto[i].cantidad);
                      }
                      return 0;
                  }
              ''',
              al_superar="Tres ítems, iguales que antes. El Guardián abre otro cajón. El Archivero aplaude con una sola mano: con la otra busca los anteojos.",
              imagen=["Una mochila de aventurera cuyos ítems se guardan en una caja de hierro y vuelven a salir iguales.", GUARDIAN + " abre un cajón del pecho."]),
            m(id="R04-N06-P3", titulo="El registro de la bóveda",
              lugar="La bóveda del Archivo", personajes="Kira, Gheco, el Archivero",
              carta="Buscar en un archivo | recorrer con fread hasta que devuelva 0 · comparar el campo clave · avisar si no está",
              recompensa="xp 15, oro 15",
              escena="Adentro de la bóveda, en una caja vieja, están todos los encargos de la Forja. Kira busca el que firmó el Vidriero: el código 777.",
              sugiere="`while (fread(&e, sizeof e, 1, f) == 1)` recorre todo el archivo. Si el código coincide, se muestra y se corta. Si termina sin encontrarlo, se avisa.",
              desafio="Completá la comparación.",
              inicial='''
                  #include <stdio.h>
                  #include <string.h>

                  typedef struct {
                      int codigo;
                      char detalle[40];
                  } Encargo;

                  int main(void)
                  {
                      Encargo encargos[3] = {
                          { 101, "herraduras para el Gremio" },
                          { 777, "plomo para un marco de 3 x 5 metros" },
                          { 205, "clavos de cobre" },
                      };
                      FILE *f = fopen("encargos.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      fwrite(encargos, sizeof encargos[0], 3, f);
                      fclose(f);

                      f = fopen("encargos.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      Encargo e;
                      int encontrado = 0;
                      while (fread(&e, sizeof e, 1, f) == 1) {
                          if (___) {
                              printf("encargo %d: %s\\n", e.codigo, e.detalle);
                              encontrado = 1;
                              break;
                          }
                      }
                      fclose(f);
                      if (!encontrado) {
                          printf("no esta\\n");
                      }
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>
                  #include <string.h>

                  typedef struct {
                      int codigo;
                      char detalle[40];
                  } Encargo;

                  int main(void)
                  {
                      Encargo encargos[3] = {
                          { 101, "herraduras para el Gremio" },
                          { 777, "plomo para un marco de 3 x 5 metros" },
                          { 205, "clavos de cobre" },
                      };
                      FILE *f = fopen("encargos.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      fwrite(encargos, sizeof encargos[0], 3, f);
                      fclose(f);

                      f = fopen("encargos.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      Encargo e;
                      int encontrado = 0;
                      while (fread(&e, sizeof e, 1, f) == 1) {
                          if (e.codigo == 777) {
                              printf("encargo %d: %s\\n", e.codigo, e.detalle);
                              encontrado = 1;
                              break;
                          }
                      }
                      fclose(f);
                      if (!encontrado) {
                          printf("no esta\\n");
                      }
                      return 0;
                  }
              ''',
              al_superar="«Plomo para un marco de 3 × 5 metros». El Archivero deja de buscar los anteojos de golpe. —Ese marco… —dice— yo lo vi dibujado. En un plano del **Imperio**.",
              imagen=["Una caja vieja abierta en la bóveda, con una ficha que brilla: 777.", ARCHIVERO.capitalize() + " se queda inmóvil, con los anteojos en la mano."]),
            m(id="R04-N06-P4", titulo="El último cajón",
              lugar="La bóveda del Archivo", personajes="Kira, Gheco, Tizón, el Archivero",
              criatura="dragon",
              carta="Todo junto | archivo binario + baja lógica + listado de activos · abrir, recorrer, cambiar en el lugar y cerrar",
              recompensa="xp 25, oro 30",
              item="Libro de Registros de Plomo",
              escena="""
                  El Guardián abre su último cajón y pone la última prueba: dar de baja los registros falsos que dejó Chispa (los que tienen stock negativo), sin borrarlos, y listar los que quedan activos.
              """,
              sugiere="Se abre con `\"r+b\"`, se recorre, y a cada registro con stock negativo se le pone `'B'` y se reescribe en su lugar. Después se listan los `'A'`.",
              desafio="Completá la condición de la baja y el filtro del listado.",
              inicial='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      int stock;
                      char estado;
                  } Registro;

                  int main(void)
                  {
                      Registro r[5] = { { 1, 40, 'A' }, { 2, -3, 'A' }, { 3, 12, 'A' }, { 4, -50, 'A' }, { 5, 7, 'A' } };
                      FILE *f = fopen("plomo.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      fwrite(r, sizeof r[0], 5, f);
                      fclose(f);

                      f = fopen("plomo.dat", "r+b");
                      if (f == NULL) {
                          return 1;
                      }
                      Registro x;
                      int bajas = 0;
                      while (fread(&x, sizeof x, 1, f) == 1) {
                          if (___) {
                              x.estado = 'B';
                              fseek(f, -(long) sizeof x, SEEK_CUR);
                              fwrite(&x, sizeof x, 1, f);
                              fseek(f, 0, SEEK_CUR);
                              bajas++;
                          }
                      }
                      fclose(f);

                      f = fopen("plomo.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      printf("bajas: %d\\nactivos:", bajas);
                      while (fread(&x, sizeof x, 1, f) == 1) {
                          if (___) {
                              printf(" %d", x.codigo);
                          }
                      }
                      printf("\\n");
                      fclose(f);
                      return 0;
                  }
              ''',
              solucion='''
                  #include <stdio.h>

                  typedef struct {
                      int codigo;
                      int stock;
                      char estado;
                  } Registro;

                  int main(void)
                  {
                      Registro r[5] = { { 1, 40, 'A' }, { 2, -3, 'A' }, { 3, 12, 'A' }, { 4, -50, 'A' }, { 5, 7, 'A' } };
                      FILE *f = fopen("plomo.dat", "wb");
                      if (f == NULL) {
                          return 1;
                      }
                      fwrite(r, sizeof r[0], 5, f);
                      fclose(f);

                      f = fopen("plomo.dat", "r+b");
                      if (f == NULL) {
                          return 1;
                      }
                      Registro x;
                      int bajas = 0;
                      while (fread(&x, sizeof x, 1, f) == 1) {
                          if (x.stock < 0 && x.estado == 'A') {
                              x.estado = 'B';
                              fseek(f, -(long) sizeof x, SEEK_CUR);
                              fwrite(&x, sizeof x, 1, f);
                              fseek(f, 0, SEEK_CUR);
                              bajas++;
                          }
                      }
                      fclose(f);

                      f = fopen("plomo.dat", "rb");
                      if (f == NULL) {
                          return 1;
                      }
                      printf("bajas: %d\\nactivos:", bajas);
                      while (fread(&x, sizeof x, 1, f) == 1) {
                          if (x.estado == 'A') {
                              printf(" %d", x.codigo);
                          }
                      }
                      printf("\\n");
                      fclose(f);
                      return 0;
                  }
              ''',
              al_superar="Dos bajas, tres activos. El Guardián se queda quieto, abre todos los cajones a la vez, y en el último hay un libro encadenado: **el Libro de Registros de Plomo**, con las medidas exactas del marco que encargó el Vidriero. Va a tu mochila. En la última página, una nota: «Fundido bajo la Montaña».",
              imagen=[GUARDIAN + " con todos los cajones abiertos.",
                      "Un libro encadenado con tapas de plomo que brilla en el último cajón.",
                      KIRA + " lo abre en la última página; " + TIZON + " y el Archivero miran por encima de su hombro."]),
        ],
    },
]
