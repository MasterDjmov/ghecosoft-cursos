# RAMA R04 · El Archivo de la Forja: archivos y programas completos

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · Archivos de texto

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: goblin
temas: arch.texto, arch.csv
```

### Crónica

Al subir de las Minas llegás al **Archivo de la Forja**: estantes y estantes de libros donde se anota todo lo que se forja. Lo que no se anota, se pierde cuando se apaga el horno.

—La memoria del programa es como el calor del metal, {heroe} —dice {mentor}—: se va cuando terminás. Lo que querés guardar va al papel. Y el papel hay que leerlo con cuidado: siempre hay alguien que escribió mal una línea.

### Objetivos

- Abrir, escribir, leer y cerrar archivos de texto con `fopen`, `fprintf`, `fgets` y `fclose`.
- Elegir el modo correcto (`"r"`, `"w"`, `"a"`) y detectar cuándo `fopen` falla, con `perror`.
- Leer un archivo CSV línea por línea, validando cada dato con `sscanf`.

### Antes de empezar

- Entrada y salida con `fgets` + `sscanf` (05).
- Strings (11) y punteros (13).

### Explicación

#### Abrir y cerrar

```c
FILE *f = fopen("aprendices.csv", "r");
if (f == NULL) {
    perror("aprendices.csv");    /* "aprendices.csv: No such file or directory" */
    return 1;
}
...
fclose(f);
```

`FILE *` es un puntero a un struct que maneja la biblioteca. **Siempre** se revisa el `NULL`: el archivo puede no existir, o no tener permiso.

| Modo | Qué hace | Si no existe |
|---|---|---|
| `"r"` | leer | falla (`NULL`) |
| `"w"` | escribir desde cero (**borra** lo que había) | lo crea |
| `"a"` | agregar al final | lo crea |
| `"r+"` | leer y escribir sin borrar | falla |

#### Escribir y leer

Son las mismas funciones que ya conocés, con una `f` y el archivo:

| Pantalla / teclado | Archivo |
|---|---|
| `printf(...)` | `fprintf(f, ...)` |
| `fgets(linea, tam, stdin)` | `fgets(linea, tam, f)` |
| `putchar(c)` / `getchar()` | `fputc(c, f)` / `fgetc(f)` |

La receta de lectura es la de siempre: una línea con `fgets`, los datos con `sscanf`. `fgets` devuelve `NULL` cuando se termina el archivo:

```c
while (fgets(linea, sizeof(linea), f) != NULL) {
    ...
}
```

#### Leer un CSV

En un CSV cada línea es un registro y los datos van separados por `;` (o `,`). Con `sscanf`, `%19[^;]` significa "hasta 19 caracteres que **no** sean `;`":

```c
char nombre[20];
int nivel, oro;
if (sscanf(linea, "%19[^;];%d;%d", nombre, &nivel, &oro) == 3) {
    /* línea válida */
}
```

Si `sscanf` no convierte los 3 datos, la línea está mal: se informa **con su número** y se sigue con la siguiente. Un archivo con una línea rota no tiene que tirar abajo el programa.

#### Borrar

`remove("archivo.txt")` borra un archivo. En los ejemplos se usa al final para que cada ejecución arranque igual.

#### Cómo compilarlo y ejecutarlo

```bash
gcc -std=c11 -Wall -Wextra -o programa main.c && ./programa
```

Los archivos se crean en la carpeta desde donde ejecutás el programa.

### Código de ejemplo

```c
/*
 * 21 - Archivos de texto: escribir, leer linea por linea y validar.
 */
#include <stdio.h>
#include <string.h>

#define RUTA "aprendices.csv"

int main(void)
{
    /* 1) Escribir: "w" crea el archivo (o lo vacia si ya existia). */
    FILE *f = fopen(RUTA, "w");
    if (f == NULL) {
        perror(RUTA);                          /* explica por que fallo */
        return 1;
    }
    fprintf(f, "nombre;nivel;oro\n");
    fprintf(f, "Kira;6;250\n");
    fprintf(f, "Bron;9;1200\n");
    fprintf(f, "Zed;siete;80\n");              /* una linea rota, a proposito */
    fprintf(f, "Mia;5;430\n");
    fclose(f);

    /* 2) Leer: "r". Cada linea con fgets, cada dato con sscanf. */
    f = fopen(RUTA, "r");
    if (f == NULL) {
        perror(RUTA);
        return 1;
    }
    char linea[100];
    int numero = 0, validas = 0, oro_total = 0;
    while (fgets(linea, sizeof(linea), f) != NULL) {
        numero++;
        if (numero == 1) {
            continue;                          /* el encabezado */
        }
        char nombre[20];
        int nivel, oro;
        if (sscanf(linea, "%19[^;];%d;%d", nombre, &nivel, &oro) == 3) {
            printf("%-6s nivel %2d  %5d de oro\n", nombre, nivel, oro);
            validas++;
            oro_total += oro;
        } else {
            linea[strcspn(linea, "\n")] = '\0';
            printf("línea %d con error: \"%s\"\n", numero, linea);
        }
    }
    fclose(f);
    printf("%d aprendices, %d de oro en total\n", validas, oro_total);

    /* 3) Un archivo que no existe: fopen devuelve NULL y perror dice por que. */
    if (fopen("no_existe.txt", "r") == NULL) {
        perror("no_existe.txt");
    }
    remove(RUTA);                              /* limpiar: la proxima vez arranca igual */
    return 0;
}
```

### Salida esperada

```
Kira   nivel  6    250 de oro
Bron   nivel  9   1200 de oro
línea 4 con error: "Zed;siete;80"
Mia    nivel  5    430 de oro
3 aprendices, 1880 de oro en total
```

### ¿Para qué sirve?

Los archivos de texto son la forma más simple de que los datos sobrevivan: la configuración de un programa, los registros (*logs*) de un servidor, las planillas exportadas como CSV, los archivos de puntajes de un juego. Validar cada línea es fundamental: los archivos los editan personas, llegan cortados o vienen de otros sistemas con otro formato.

### Errores habituales

**Orco: `fopen` sin revisar.** Si el archivo no existe, `f` es `NULL` y el primer `fgets(linea, 100, f)` corta el programa (`Segmentation fault`).

**Ogro: `"w"` en lugar de `"a"`.** Abrir con `"w"` **borra** el archivo: el diario pierde todas las entradas anteriores.

**Troll: olvidar `fclose`.** Lo escrito puede quedar en memoria y no llegar al archivo (y se desperdicia un recurso del sistema).

**Goblin: `%s` en un CSV.** `%s` lee hasta el espacio, no hasta el `;`: `"Kira;6;250"` entra entero en el nombre. Se usa `%19[^;]`.

**Ogro: `while (!feof(f))`.** Un clásico que procesa la última línea dos veces: `feof` recién es verdadero **después** de un intento fallido. Se controla con lo que devuelve `fgets`.

### Misión R04-N01-M1 · El diario de la Forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

1. Escribí `int agregar(const char *texto)`, que abre `diario.txt` en modo **agregar**, escribe el texto en una línea y lo cierra. Devuelve 0 si no pudo abrirlo.
2. Borrá el diario al empezar (para que cada prueba arranque igual) y agregá tres entradas: `Día 1: templé mi primera hoja.`, `Día 2: Ferrum dice que está torcida.` y `Día 3: la enderecé. Casi.`.
3. Leé el diario y mostralo con cada línea numerada (`%2d | `).

#### Criterio de aprobación

- Usa el modo `"a"` para agregar.
- Revisa el `NULL` de `fopen` y cierra cada archivo.
- Muestra las tres entradas numeradas.

#### Salida esperada

```
 1 | Día 1: templé mi primera hoja.
 2 | Día 2: Ferrum dice que está torcida.
 3 | Día 3: la enderecé. Casi.
```

#### Solución de referencia

```c
/* Mision 1 - El diario de la Forja: agregar con "a" y leer numerado. */
#include <stdio.h>

#define RUTA "diario.txt"

int agregar(const char *texto)
{
    FILE *f = fopen(RUTA, "a");               /* "a": escribe al final, sin borrar */
    if (f == NULL) {
        perror(RUTA);
        return 0;
    }
    fprintf(f, "%s\n", texto);
    fclose(f);
    return 1;
}

int main(void)
{
    remove(RUTA);                             /* para que cada prueba arranque igual */
    agregar("Día 1: templé mi primera hoja.");
    agregar("Día 2: Ferrum dice que está torcida.");
    agregar("Día 3: la enderecé. Casi.");

    FILE *f = fopen(RUTA, "r");
    if (f == NULL) {
        perror(RUTA);
        return 1;
    }
    char linea[120];
    int n = 0;
    while (fgets(linea, sizeof(linea), f) != NULL) {
        printf("%2d | %s", ++n, linea);
    }
    fclose(f);
    remove(RUTA);
    return 0;
}
```

### Misión R04-N01-M2 · Contar como wc

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí en `cancion.txt` estas cuatro líneas y después leelo **de a un carácter** con `fgetc` para contar líneas, palabras y bytes, como el comando `wc` de Linux:

```
En las Forjas de Hierro
el martillo no descansa,
  cada golpe es una runa
y cada runa, una espada.
```

Una palabra empieza cuando aparece un carácter que no es espacio después de uno que sí lo es (usá `isspace`).

#### Criterio de aprobación

- Lee con `fgetc` hasta `EOF` (en una variable `int`).
- Cuenta bien las palabras aunque haya varios espacios seguidos.
- Da el mismo resultado que `wc` sobre el archivo.

#### Salida esperada

```
líneas: 4, palabras: 19, bytes: 99
```

#### Solución de referencia

```c
/* Mision 2 - Contar como wc: lineas, palabras y caracteres, leyendo de a un caracter. */
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

int main(void)
{
    FILE *f = fopen("cancion.txt", "w");
    if (f == NULL) {
        perror("cancion.txt");
        return 1;
    }
    fputs("En las Forjas de Hierro\nel martillo no descansa,\n  cada golpe es una runa\ny cada runa, una espada.\n", f);
    fclose(f);

    f = fopen("cancion.txt", "r");
    if (f == NULL) {
        perror("cancion.txt");
        return 1;
    }
    int lineas = 0, palabras = 0, bytes = 0;
    bool en_palabra = false;
    int c;
    while ((c = fgetc(f)) != EOF) {
        bytes++;
        if (c == '\n') {
            lineas++;
        }
        if (isspace(c)) {
            en_palabra = false;
        } else if (!en_palabra) {
            en_palabra = true;
            palabras++;
        }
    }
    fclose(f);
    remove("cancion.txt");
    printf("líneas: %d, palabras: %d, bytes: %d\n", lineas, palabras, bytes);
    return 0;
}
```

### Misión R04-N01-M3 · El CSV de precios

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `precios.csv` con este contenido:

```
producto;precio;stock
Clavo;4.50;300
Martillo;;12
Tenaza;38.00;7
Yunque;950;-2
Lima;22.75;15
Fuelle;120.5
```

Leelo salteando el encabezado. Cada línea tiene que tener exactamente 3 datos (usá un `%c` extra para detectar lo que sobra), precio positivo y stock no negativo. Informá cada línea con error y su número, y mostrá el valor total del stock válido (precio × stock).

#### Criterio de aprobación

- Valida la cantidad de datos con lo que devuelve `sscanf`.
- Valida los rangos por separado.
- Informa cada error con su número de línea y sigue con la siguiente.
- Calcula el valor del stock válido.

#### Salida esperada

```
línea 3: formato inválido ("Martillo;;12")
línea 5: valores fuera de rango ("Yunque;950;-2")
línea 7: formato inválido ("Fuelle;120.5")
Valor del stock válido: $1957.25 (3 líneas con error)
```

#### Solución de referencia

```c
/* Mision 3 - El CSV de precios: validar cada linea e informar los errores con su numero. */
#include <stdio.h>
#include <string.h>

int main(void)
{
    FILE *f = fopen("precios.csv", "w");
    if (f == NULL) {
        perror("precios.csv");
        return 1;
    }
    fputs("producto;precio;stock\n"
          "Clavo;4.50;300\n"
          "Martillo;;12\n"
          "Tenaza;38.00;7\n"
          "Yunque;950;-2\n"
          "Lima;22.75;15\n"
          "Fuelle;120.5\n", f);
    fclose(f);

    f = fopen("precios.csv", "r");
    if (f == NULL) {
        perror("precios.csv");
        return 1;
    }
    char linea[100];
    int numero = 0, errores = 0;
    double valor = 0;
    fgets(linea, sizeof(linea), f);          /* encabezado */
    numero++;
    while (fgets(linea, sizeof(linea), f) != NULL) {
        numero++;
        linea[strcspn(linea, "\n")] = '\0';
        char producto[30];
        double precio;
        int stock;
        char sobra;
        if (sscanf(linea, "%29[^;];%lf;%d%c", producto, &precio, &stock, &sobra) != 3) {
            printf("línea %d: formato inválido (\"%s\")\n", numero, linea);
            errores++;
        } else if (precio <= 0 || stock < 0) {
            printf("línea %d: valores fuera de rango (\"%s\")\n", numero, linea);
            errores++;
        } else {
            valor += precio * stock;
        }
    }
    fclose(f);
    remove("precios.csv");
    printf("Valor del stock válido: $%.2f (%d líneas con error)\n", valor, errores);
    return 0;
}
```

### Encargo R04-N01-E1 · El informe de notas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La escuela del Gremio tiene las notas en `notas.csv` (`Ana;8;9;7`, `Beto;5;6;4`, `Caro;10;9;9`, `Dani;6;5;7`). Leelo, calculá el promedio de cada alumno y escribí `informe.txt` con una tabla (alumno, promedio con 2 decimales, "aprobado" desde 6 o "recupera") y una línea final con cuántos aprobaron. Después mostrá el informe leyéndolo del archivo.

#### Criterio de aprobación

- Lee un archivo y escribe otro, revisando los dos `fopen`.
- Calcula los promedios con decimales.
- Muestra el informe leyéndolo del archivo escrito.

#### Salida esperada

```
Alumno Promedio  Estado
Ana        8.00  aprobado
Beto       5.00  recupera
Caro       9.33  aprobado
Dani       6.00  aprobado
Aprobaron 3 de 4
```

#### Solución de referencia

```c
/* Encargo - El informe de notas: leer un CSV, calcular y escribir otro archivo. */
#include <stdio.h>

int main(void)
{
    FILE *f = fopen("notas.csv", "w");
    if (f == NULL) {
        perror("notas.csv");
        return 1;
    }
    fputs("Ana;8;9;7\nBeto;5;6;4\nCaro;10;9;9\nDani;6;5;7\n", f);
    fclose(f);

    FILE *entrada = fopen("notas.csv", "r");
    FILE *salida = fopen("informe.txt", "w");
    if (entrada == NULL || salida == NULL) {
        perror("abrir");
        if (entrada) fclose(entrada);
        if (salida) fclose(salida);
        return 1;
    }
    char linea[100];
    int aprobados = 0, total = 0;
    fprintf(salida, "%-6s %8s  %s\n", "Alumno", "Promedio", "Estado");
    while (fgets(linea, sizeof(linea), entrada) != NULL) {
        char nombre[20];
        int a, b, c;
        if (sscanf(linea, "%19[^;];%d;%d;%d", nombre, &a, &b, &c) != 4) {
            continue;
        }
        double promedio = (a + b + c) / 3.0;
        total++;
        if (promedio >= 6) {
            aprobados++;
        }
        fprintf(salida, "%-6s %8.2f  %s\n", nombre, promedio, promedio >= 6 ? "aprobado" : "recupera");
    }
    fprintf(salida, "Aprobaron %d de %d\n", aprobados, total);
    fclose(entrada);
    fclose(salida);

    /* Mostrar el informe tal como quedo en el archivo. */
    salida = fopen("informe.txt", "r");
    if (salida == NULL) {
        perror("informe.txt");
        return 1;
    }
    while (fgets(linea, sizeof(linea), salida) != NULL) {
        fputs(linea, stdout);
    }
    fclose(salida);
    remove("notas.csv");
    remove("informe.txt");
    return 0;
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre abrir con `"w"` y con `"a"`?

`"w"` borra el contenido y escribe desde cero; `"a"` agrega al final y conserva lo anterior. Los dos crean el archivo si no existe.

#### ¿Qué devuelve `fopen` si el archivo no existe y lo abrís con `"r"`? ¿Qué hace `perror`?

Devuelve `NULL`. `perror` muestra en `stderr` el texto que le pasás y el motivo del error del sistema.

#### ¿Qué significa `%19[^;]` en `sscanf`?

Hasta 19 caracteres que no sean `;`: lee un campo del CSV sin pasarse del tamaño del array.

#### ¿Por qué no conviene `while (!feof(f))`?

Porque `feof` recién es verdadero después de una lectura que falló: la última línea se procesa dos veces. Se controla con el valor de `fgets`.

#### ¿Qué pasa si no hacés `fclose`?

Lo escrito puede no llegar al archivo y queda un recurso del sistema abierto hasta que termina el programa.

### Soluciones (docente)

Reescrita desde cero a partir de `02-C-Intermedio/21-ArchivosTexto` (formato viejo).

## R04-N02 · Archivos binarios

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: troll
temas: arch.binarios
usa: col.registros
```

### Crónica

En el fondo del Archivo, {mentor} abre un cofre de hierro. Adentro no hay libros: hay **moldes**. Cada molde guarda una pieza exactamente como es, byte por byte, sin traducirla a letras.

—Los libros los lee cualquiera, {heroe}. Los moldes, solo la Forja que los hizo. Pero son rápidos, justos y no se equivocan al copiar. Así se guarda una partida.

### Objetivos

- Guardar y cargar structs completos con `fwrite` y `fread` en modo binario.
- Moverse dentro de un archivo con `fseek`, `ftell` y `rewind`, y modificar un registro en el lugar.
- Saber qué problemas tiene un archivo binario (portabilidad, relleno, versiones).

### Antes de empezar

- Archivos de texto (R04-N01).
- Structs (12) y arrays de structs (15); `sizeof` (02).

### Explicación

#### Escribir la memoria tal cual

```c
Heroe grupo[3] = { ... };
FILE *f = fopen("partida.dat", "wb");        /* la "b" es de binario */
size_t escritos = fwrite(grupo, sizeof grupo[0], 3, f);
fclose(f);
```

`fwrite(dirección, tamaño de uno, cuántos, archivo)` copia los bytes tal como están en la memoria. `fread` hace lo contrario y **devuelve cuántos elementos pudo leer**: si da menos de los pedidos, se terminó el archivo (o hubo un error).

```c
Heroe leidos[10];
size_t cuantos = fread(leidos, sizeof leidos[0], 10, f);   /* puede ser menos de 10 */
```

#### Moverse dentro del archivo

Como cada registro ocupa `sizeof(Heroe)` bytes, el registro `k` empieza en `k * sizeof(Heroe)`:

```c
fseek(f, k * (long) sizeof(Heroe), SEEK_SET);   /* ir al registro k */
fread(&h, sizeof h, 1, f);
```

| Llamada | Qué hace |
|---|---|
| `fseek(f, n, SEEK_SET)` | ir al byte `n` desde el principio |
| `fseek(f, 0, SEEK_END)` | ir al final |
| `ftell(f)` | en qué byte estás (al final: el tamaño del archivo) |
| `rewind(f)` | volver al principio |

Con `"r+b"` se puede **leer y escribir** sin borrar: se lee un registro, se cambia, se vuelve con `fseek` a su principio y se escribe encima.

#### Texto o binario

| | Texto | Binario |
|---|---|---|
| Se lee con un editor | sí | no |
| Tamaño | variable (depende de las cifras) | fijo por registro |
| Ir al registro 500 | recorrer 500 líneas | un `fseek` |
| Entre máquinas distintas | funciona | puede fallar |

**Portabilidad**: un archivo binario depende del tamaño de los tipos, del **relleno** del struct (12) y del orden de los bytes de la máquina. Un `.dat` guardado en una compu puede no leerse bien en otra, o después de agregar un campo al struct. Por eso los formatos serios guardan una **versión** al principio del archivo.

#### Cómo compilarlo y ejecutarlo

```bash
gcc -std=c11 -Wall -Wextra -o programa main.c && ./programa
```

### Código de ejemplo

```c
/*
 * 22 - Archivos binarios: guardar la partida tal como esta en memoria.
 */
#include <stdio.h>
#include <string.h>

typedef struct {
    char nombre[16];
    int nivel;
    int vida;
    int oro;
} Heroe;

#define RUTA "partida.dat"

int main(void)
{
    Heroe grupo[] = {
        { "Kira", 6, 48, 250 },
        { "Bron", 9, 90, 1200 },
        { "Mia", 5, 35, 430 },
    };
    int n = sizeof(grupo) / sizeof(grupo[0]);

    /* Guardar: "wb" y fwrite(direccion, tamanio de uno, cuantos, archivo). */
    FILE *f = fopen(RUTA, "wb");
    if (f == NULL) {
        perror(RUTA);
        return 1;
    }
    size_t escritos = fwrite(grupo, sizeof grupo[0], n, f);
    fclose(f);
    printf("Guardados %zu héroes de %zu bytes cada uno\n", escritos, sizeof(Heroe));

    /* Cargar: "rb" y fread. Devuelve cuantos pudo leer. */
    Heroe leidos[10];
    f = fopen(RUTA, "rb");
    if (f == NULL) {
        perror(RUTA);
        return 1;
    }
    size_t cuantos = fread(leidos, sizeof leidos[0], 10, f);

    /* El tamanio del archivo: ir al final y preguntar la posicion. */
    fseek(f, 0, SEEK_END);
    long bytes = ftell(f);

    /* Leer solo el segundo registro: saltar directo a su posicion. */
    Heroe segundo;
    fseek(f, 1 * (long) sizeof(Heroe), SEEK_SET);
    fread(&segundo, sizeof segundo, 1, f);
    fclose(f);

    printf("Leídos %zu héroes (%ld bytes en el archivo)\n", cuantos, bytes);
    for (size_t i = 0; i < cuantos; i++) {
        printf("  %-5s nivel %d, vida %d, oro %d\n", leidos[i].nombre, leidos[i].nivel, leidos[i].vida, leidos[i].oro);
    }
    printf("Registro 1 leído directo: %s\n", segundo.nombre);
    printf("¿Iguales? %s\n", memcmp(grupo, leidos, sizeof grupo) == 0 ? "sí" : "no");
    remove(RUTA);
    return 0;
}
```

### Salida esperada

```
Guardados 3 héroes de 28 bytes cada uno
Leídos 3 héroes (84 bytes en el archivo)
  Kira  nivel 6, vida 48, oro 250
  Bron  nivel 9, vida 90, oro 1200
  Mia   nivel 5, vida 35, oro 430
Registro 1 leído directo: Bron
¿Iguales? sí
```

### ¿Para qué sirve?

Los archivos binarios guardan casi todo lo que no está pensado para leer una persona: las partidas guardadas de los juegos, las imágenes (PNG, JPG), la música, los ejecutables y las bases de datos, que usan exactamente el truco de `fseek` para ir directo a un registro sin leer los anteriores. Entender el formato binario es también lo que permite leer archivos de otros programas o de dispositivos (un sensor, una cámara).

### Errores habituales

**Ogro: olvidar la `b`.** En Linux da igual, pero en Windows `"r"` transforma los saltos de línea y rompe los datos binarios. Siempre `"rb"` y `"wb"`.

**Orco: no mirar lo que devuelve `fread`.** Si el archivo tiene menos registros, los que no se leyeron quedan con basura.

**Troll: guardar punteros.** Un struct con `char *nombre` guarda la **dirección**, no el texto: al cargarlo en otra ejecución apunta a cualquier lado. En binario se guardan arrays (`char nombre[16]`), nunca punteros.

**Ogro: cambiar el struct.** Agregar un campo cambia `sizeof`: los archivos viejos se leen corridos.

**Ogro: escribir sin volver.** Después de `fread`, el archivo quedó **al final** del registro: para reescribirlo hay que volver con `fseek`.

### Misión R04-N02-M1 · Guardar y cargar el progreso

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con un struct `Progreso` (nombre de 16, nivel, oro, x, y), escribí `bool guardar(const Progreso *p, const char *ruta)` y `bool cargar(Progreso *p, const char *ruta)`, que devuelven `false` si algo falla (el archivo no abre o no se escribió/leyó el registro completo). Guardá el progreso de Kira (nivel 7, 380 de oro, en 12, 4), cargalo en otra variable, mostralo, e intentá cargar un archivo que no existe.

#### Criterio de aprobación

- Usa `"wb"` y `"rb"`.
- Revisa lo que devuelven `fwrite` y `fread`.
- Informa el fallo al cargar un archivo que no existe.

#### Salida esperada

```
en juego: Kira, nivel 7, 380 de oro, en (12, 4)
guardar: ok
cargar: ok
cargado: Kira, nivel 7, 380 de oro, en (12, 4)
cargar otro: falló
```

#### Solución de referencia

```c
/* Mision 1 - Guardar y cargar el progreso, con funciones que avisan si fallaron. */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    char nombre[16];
    int nivel;
    int oro;
    int x, y;
} Progreso;

bool guardar(const Progreso *p, const char *ruta)
{
    FILE *f = fopen(ruta, "wb");
    if (f == NULL) {
        return false;
    }
    bool ok = fwrite(p, sizeof *p, 1, f) == 1;
    return fclose(f) == 0 && ok;
}

bool cargar(Progreso *p, const char *ruta)
{
    FILE *f = fopen(ruta, "rb");
    if (f == NULL) {
        return false;
    }
    bool ok = fread(p, sizeof *p, 1, f) == 1;
    fclose(f);
    return ok;
}

void mostrar(const char *titulo, const Progreso *p)
{
    printf("%s: %s, nivel %d, %d de oro, en (%d, %d)\n", titulo, p->nombre, p->nivel, p->oro, p->x, p->y);
}

int main(void)
{
    Progreso actual = { "Kira", 7, 380, 12, 4 };
    mostrar("en juego", &actual);
    printf("guardar: %s\n", guardar(&actual, "progreso.dat") ? "ok" : "falló");

    Progreso recuperado = { "", 0, 0, 0, 0 };
    printf("cargar: %s\n", cargar(&recuperado, "progreso.dat") ? "ok" : "falló");
    mostrar("cargado", &recuperado);

    printf("cargar otro: %s\n", cargar(&recuperado, "no_existe.dat") ? "ok" : "falló");
    remove("progreso.dat");
    return 0;
}
```

### Misión R04-N02-M2 · Directo al registro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

1. Guardá 10 enemigos (`numero` de 0 a 9, `vida` = 10 + número × 5) en `horda.dat`.
2. Abrilo con `"r+b"`, andá directo al registro 7 con `fseek` y mostralo.
3. Poné en 0 la vida del enemigo 3 **en el lugar**: leelo, cambialo, volvé a su posición y escribilo.
4. Con `rewind`, recorré todo el archivo y mostrá las vidas.

#### Criterio de aprobación

- Calcula la posición como `k * sizeof`.
- Vuelve con `fseek` antes de reescribir.
- Muestra el registro 7 y todas las vidas con el 3 en 0.

#### Salida esperada

```
registro 7: enemigo 7 con 45 de vida
vidas: 10 15 20 0 30 35 40 45 50 55
```

#### Solución de referencia

```c
/* Mision 2 - Ir directo al registro k y modificarlo en el lugar con "r+b". */
#include <stdio.h>

typedef struct {
    int numero;
    int vida;
} Enemigo;

int main(void)
{
    FILE *f = fopen("horda.dat", "wb");
    if (f == NULL) {
        return 1;
    }
    for (int i = 0; i < 10; i++) {
        Enemigo e = { i, 10 + i * 5 };
        fwrite(&e, sizeof e, 1, f);
    }
    fclose(f);

    f = fopen("horda.dat", "r+b");            /* leer y escribir, sin borrar */
    if (f == NULL) {
        return 1;
    }
    Enemigo e;
    fseek(f, 7 * (long) sizeof e, SEEK_SET);
    fread(&e, sizeof e, 1, f);
    printf("registro 7: enemigo %d con %d de vida\n", e.numero, e.vida);

    fseek(f, 3 * (long) sizeof e, SEEK_SET);
    fread(&e, sizeof e, 1, f);
    e.vida = 0;                               /* cae el enemigo 3 */
    fseek(f, 3 * (long) sizeof e, SEEK_SET);  /* volver al principio del registro */
    fwrite(&e, sizeof e, 1, f);

    rewind(f);
    printf("vidas:");
    while (fread(&e, sizeof e, 1, f) == 1) {
        printf(" %d", e.vida);
    }
    printf("\n");
    fclose(f);
    remove("horda.dat");
    return 0;
}
```

### Misión R04-N02-M3 · Texto o binario

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Guardá 1000 enteros (`i * 1234`) de dos formas: como texto (uno por línea con `fprintf`) y en binario (un solo `fwrite`). Medí el tamaño de cada archivo con `fseek` + `ftell` y mostralo. ¿Cuál ocupa menos? ¿Cuál podés abrir con un editor?

#### Criterio de aprobación

- Escribe los dos archivos.
- Mide el tamaño con `fseek(f, 0, SEEK_END)` y `ftell`.
- Explica la diferencia.

#### Salida esperada

```
texto:   7095 bytes
binario: 4000 bytes (4 por número)
El texto se puede leer con cualquier editor; el binario, solo con este programa.
```

#### Solución de referencia

```c
/* Mision 3 - Texto o binario: cuanto ocupan 1000 numeros de cada forma. */
#include <stdio.h>

long tamanio(const char *ruta)
{
    FILE *f = fopen(ruta, "rb");
    if (f == NULL) {
        return -1;
    }
    fseek(f, 0, SEEK_END);
    long t = ftell(f);
    fclose(f);
    return t;
}

int main(void)
{
    int numeros[1000];
    for (int i = 0; i < 1000; i++) {
        numeros[i] = i * 1234;
    }
    FILE *texto = fopen("numeros.txt", "w");
    FILE *binario = fopen("numeros.dat", "wb");
    if (texto == NULL || binario == NULL) {
        return 1;
    }
    for (int i = 0; i < 1000; i++) {
        fprintf(texto, "%d\n", numeros[i]);
    }
    fwrite(numeros, sizeof numeros[0], 1000, binario);
    fclose(texto);
    fclose(binario);

    printf("texto:   %ld bytes\n", tamanio("numeros.txt"));
    printf("binario: %ld bytes (%zu por número)\n", tamanio("numeros.dat"), sizeof(int));
    printf("El texto se puede leer con cualquier editor; el binario, solo con este programa.\n");
    remove("numeros.txt");
    remove("numeros.dat");
    return 0;
}
```

### Encargo R04-N02-E1 · La caja fuerte del banco

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El banco del Gremio guarda las cuentas (número, titular, saldo) en `cuentas.dat`. Creá el archivo con tres cuentas y escribí `bool depositar(int numero, double monto)`, que busca la cuenta recorriendo el archivo y la **actualiza en el lugar** (`"r+b"`). Rechazá montos no positivos y cuentas inexistentes. Mostrá el resultado de cada intento y el listado final.

#### Criterio de aprobación

- Busca la cuenta recorriendo registros con `fread`.
- Actualiza en el lugar volviendo con `fseek`.
- Rechaza montos inválidos y cuentas que no existen.

#### Salida esperada

```
depositar 200 en 102: ok
depositar 50 en 999: no
depositar -10 en 101: no
  101 Ana      $   1500.00
  102 Beto     $    520.50
  103 Caro     $      0.00
```

#### Solución de referencia

```c
/* Encargo - La caja fuerte del banco: cuentas en un archivo binario, actualizadas en el lugar. */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    int numero;
    char titular[20];
    double saldo;
} Cuenta;

#define RUTA "cuentas.dat"

bool depositar(int numero, double monto)
{
    FILE *f = fopen(RUTA, "r+b");
    if (f == NULL || monto <= 0) {
        if (f) fclose(f);
        return false;
    }
    Cuenta c;
    long posicion = 0;
    while (fread(&c, sizeof c, 1, f) == 1) {
        if (c.numero == numero) {
            c.saldo += monto;
            fseek(f, posicion, SEEK_SET);
            fwrite(&c, sizeof c, 1, f);
            fclose(f);
            return true;
        }
        posicion += sizeof c;
    }
    fclose(f);
    return false;
}

void listar(void)
{
    FILE *f = fopen(RUTA, "rb");
    if (f == NULL) {
        return;
    }
    Cuenta c;
    while (fread(&c, sizeof c, 1, f) == 1) {
        printf("  %d %-8s $%10.2f\n", c.numero, c.titular, c.saldo);
    }
    fclose(f);
}

int main(void)
{
    Cuenta iniciales[] = { { 101, "Ana", 1500 }, { 102, "Beto", 320.5 }, { 103, "Caro", 0 } };
    FILE *f = fopen(RUTA, "wb");
    if (f == NULL) {
        return 1;
    }
    fwrite(iniciales, sizeof iniciales[0], 3, f);
    fclose(f);

    printf("depositar 200 en 102: %s\n", depositar(102, 200) ? "ok" : "no");
    printf("depositar 50 en 999: %s\n", depositar(999, 50) ? "ok" : "no");
    printf("depositar -10 en 101: %s\n", depositar(101, -10) ? "ok" : "no");
    listar();
    remove(RUTA);
    return 0;
}
```

### Prueba del sello

#### ¿Qué devuelve `fread`? ¿Qué significa si es menor que lo pedido?

La cantidad de elementos que leyó. Si es menor, se terminó el archivo o hubo un error.

#### ¿En qué byte empieza el registro 5 de un archivo de structs `Heroe`?

En `5 * sizeof(Heroe)`.

#### ¿Por qué no se puede guardar en binario un struct con un `char *`?

Porque se guarda la dirección, no el texto: en otra ejecución esa dirección no significa nada.

#### ¿Cómo se obtiene el tamaño de un archivo?

Con `fseek(f, 0, SEEK_END)` y después `ftell(f)`.

#### ¿Qué ventaja y qué desventaja tiene el binario frente al texto?

Ventaja: tamaño fijo, rápido y acceso directo a un registro. Desventaja: no se puede leer ni editar a mano y depende de la máquina y de la versión del struct.

### Soluciones (docente)

Reescrita desde cero a partir de `02-C-Intermedio/22-ArchivosBinarios` (formato viejo).

## R04-N03 · Programas en varios archivos

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: esqueleto
temas: prog.modulos, cal.build
```

### Crónica

El Archivo tiene una sala para cada oficio: los planos de las espadas en un estante, los de las herraduras en otro. Nadie guarda todo en un solo libro gigante.

—Un programa grande se ordena igual, {heroe} —dice {mentor}—. Cada parte en su archivo, con una **tapa** que dice qué ofrece. Lo de adentro es asunto de cada taller.

### Objetivos

- Dividir un programa en **módulos**: un `.h` (qué ofrece) y un `.c` (cómo lo hace).
- Usar *include guards*, `static` para lo privado y `extern` para variables compartidas.
- Compilar por partes y automatizarlo con un `Makefile`.
- Usar el preprocesador: `#define`, macros con parámetros y compilación condicional.

### Antes de empezar

- Funciones y prototipos, variables `static` (08).
- Structs y `typedef` (12).

### Explicación

#### El `.h`: la tapa del módulo

Un archivo de cabecera **declara** lo que el módulo ofrece: prototipos, tipos y constantes. No tiene el código de las funciones.

```c
/* dado.h */
#ifndef DADO_H
#define DADO_H

void dado_sembrar(unsigned semilla);
int dado_tirar(int caras);

#endif
```

El `#ifndef ... #define ... #endif` es un **include guard**: si el `.h` se incluye dos veces (directa o indirectamente), la segunda se ignora y no hay definiciones repetidas.

#### El `.c`: el taller

```c
/* dado.c */
#include "dado.h"
#include <stdlib.h>

static int tiradas = 0;          /* privada de este archivo */

int dado_tirar(int caras)
{
    tiradas++;
    return rand() % caras + 1;
}
```

- `#include "dado.h"` con comillas busca en la carpeta del proyecto; `<stdio.h>` con signos, en las del sistema.
- **`static` afuera de una función** hace que la variable o la función exista **solo en ese archivo**: nadie de afuera puede tocarla. Es la forma de C de tener partes privadas.
- **`extern int dificultad;`** en un `.h` dice "esta variable existe, definida en algún `.c`". Se **define** (con su valor inicial) una sola vez. Las variables globales compartidas se usan poco: complican seguir quién cambia qué.

#### Compilar por partes

```bash
gcc -std=c11 -Wall -Wextra -c dado.c      # -> dado.o (código objeto, todavía sin main)
gcc -std=c11 -Wall -Wextra -c main.c      # -> main.o
gcc -o programa main.o dado.o             # el enlazador los une
```

Si cambiás solo `main.c`, alcanza con recompilar `main.o` y enlazar. O todo junto: `gcc -Wall -Wextra -o programa main.c dado.c`.

#### El `Makefile`

`make` lee un archivo `Makefile` con **reglas**: qué archivo se genera, de qué depende y qué comando lo arma. Solo recompila lo que cambió.

```make
programa: main.o dado.o
	gcc -o programa main.o dado.o

main.o: main.c dado.h
	gcc -std=c11 -Wall -Wextra -c main.c
```

Los comandos van con **tabulación** (no espacios) al principio.

#### El preprocesador

Antes de compilar, el preprocesador reemplaza texto:

```c
#define MAX_VIDA 100                     /* constante */
#define CUADRADO(x) ((x) * (x))          /* macro con parámetro: ¡todo entre paréntesis! */

#ifdef DEPURAR                           /* solo si se compila con -DDEPURAR */
    printf("valor = %d\n", valor);
#endif
```

Sin paréntesis, `CUADRADO(2 + 3)` se volvería `2 + 3 * 2 + 3` = 11.

#### Entregas de este nodo

Como son varios archivos, las misiones se entregan como **archivo**: un `.zip` con los `.c`, los `.h` y el `Makefile`.

### Código de ejemplo

`dado.h`

```c
#ifndef DADO_H
#define DADO_H

/* Lo que el resto del programa puede usar del modulo "dado". */
void dado_sembrar(unsigned semilla);
int dado_tirar(int caras);
int dado_tiradas(void);

#endif /* DADO_H */
```

`dado.c`

```c
#include "dado.h"

#include <stdlib.h>

/* static fuera de una funcion: solo existe en este archivo. */
static int tiradas = 0;

void dado_sembrar(unsigned semilla)
{
    srand(semilla);
    tiradas = 0;
}

int dado_tirar(int caras)
{
    tiradas++;
    return rand() % caras + 1;
}

int dado_tiradas(void)
{
    return tiradas;
}
```

`main.c`

```c
#include <stdio.h>

#include "dado.h"

int main(void)
{
    dado_sembrar(2026);
    printf("d6:");
    for (int i = 0; i < 5; i++) {
        printf(" %d", dado_tirar(6));
    }
    printf("\nd20: %d\n", dado_tirar(20));
    printf("tiradas: %d\n", dado_tiradas());
    return 0;
}
```

`Makefile`

```
programa: main.o dado.o
	gcc -o programa main.o dado.o

main.o: main.c dado.h
	gcc -std=c11 -Wall -Wextra -c main.c

dado.o: dado.c dado.h
	gcc -std=c11 -Wall -Wextra -c dado.c

clean:
	rm -f programa *.o
```

### Salida esperada

```
d6: 2 1 2 4 5
d20: 12
tiradas: 6
```

### ¿Para qué sirve?

Todo proyecto real de C está dividido en módulos: el kernel de Linux tiene decenas de miles de archivos `.c`, y cada biblioteca que usás (SDL, SQLite, zlib) se distribuye como uno o más `.h` para incluir y el código ya compilado para enlazar. Separar la interfaz (`.h`) de la implementación (`.c`) permite trabajar en equipo, recompilar rápido y cambiar cómo funciona algo por dentro sin tocar al resto del programa.

### Errores habituales

**Esqueleto: la función que no aparece al enlazar.** Declarada en el `.h` pero sin compilar su `.c`:

```
/usr/bin/ld: main.o: in function `main':
main.c:(.text+0x13): undefined reference to `dado_tirar'
collect2: error: ld returned 1 exit status
```

El compilador está conforme; el que protesta es el **enlazador** (`ld`). Faltó agregar `dado.c` al comando.

**Esqueleto: definición repetida.** Definir una variable en el `.h` (sin `extern`) y cargarlo en dos `.c`: `multiple definition of 'dificultad'`.

**Slime: el `.h` sin guard.** Incluido dos veces, repite los `typedef`: `conflicting types` o `redefinition`.

**Ogro: la macro sin paréntesis.** `#define DOBLE(x) x + x` hace que `3 * DOBLE(2)` dé 8 en lugar de 12.

**Slime: espacios en el `Makefile`.** `Makefile:2: *** missing separator. Stop.`: el comando tiene que empezar con tabulación.

### Misión R04-N03-M1 · Separar la herrería en módulos

```meta
entrega: archivo
entorno: local
monedas: 4
xp: 10
extensiones: zip, c, h
```

#### Consigna

El código inicial tiene todo en un solo archivo. Separalo en:

- `precios.h`: los prototipos de `precio_con_iva` y `precio_en_cuotas`, con include guard.
- `precios.c`: su código. `redondear` queda `static` (es un ayudante privado).
- `main.c`: solo el `main`, que incluye `"precios.h"`.
- Un `Makefile` que compile por partes.

La salida tiene que ser la misma que la del programa original. Entregá un `.zip` con los cuatro archivos.

#### Criterio de aprobación

- El `.h` tiene include guard y solo declaraciones.
- `redondear` es `static` en `precios.c`.
- El `Makefile` compila por partes y la salida no cambia.

#### Código inicial

```c
/* Un solo archivo: las cuentas de la herreria mezcladas con el main. Hay que separarlo en modulos. */
#include <stdio.h>

static double redondear(double x) { return (long) (x * 100 + 0.5) / 100.0; }

double precio_con_iva(double neto) { return redondear(neto * 1.21); }
double precio_en_cuotas(double total, int cuotas) { return redondear(total * (1 + 0.05 * cuotas) / cuotas); }

int main(void)
{
    double neto = 1000;
    double total = precio_con_iva(neto);
    printf("Neto: %.2f\nCon IVA: %.2f\n", neto, total);
    for (int c = 3; c <= 12; c *= 2) {
        printf("%2d cuotas de %.2f\n", c, precio_en_cuotas(total, c));
    }
    return 0;
}
```

#### Salida esperada

```
Neto: 1000.00
Con IVA: 1210.00
 3 cuotas de 463.83
 6 cuotas de 262.17
12 cuotas de 161.33
```

#### Solución de referencia

```c
/* ===== precios.h ===== */
#ifndef PRECIOS_H
#define PRECIOS_H

double precio_con_iva(double neto);
double precio_en_cuotas(double total, int cuotas);

#endif /* PRECIOS_H */

/* ===== precios.c ===== */
#include "precios.h"

/* Ayudante privado: nadie fuera de este archivo lo necesita. */
static double redondear(double x)
{
    return (long) (x * 100 + 0.5) / 100.0;
}

double precio_con_iva(double neto)
{
    return redondear(neto * 1.21);
}

double precio_en_cuotas(double total, int cuotas)
{
    return redondear(total * (1 + 0.05 * cuotas) / cuotas);
}

/* ===== main.c ===== */
#include <stdio.h>

#include "precios.h"

int main(void)
{
    double neto = 1000;
    double total = precio_con_iva(neto);
    printf("Neto: %.2f\nCon IVA: %.2f\n", neto, total);
    for (int c = 3; c <= 12; c *= 2) {
        printf("%2d cuotas de %.2f\n", c, precio_en_cuotas(total, c));
    }
    return 0;
}
```

### Misión R04-N03-M2 · La configuración compartida

```meta
entrega: archivo
entorno: local
monedas: 4
xp: 10
extensiones: zip, c, h
```

#### Consigna

Armá un programa de tres archivos más su cabecera:

- `config.h` declara con `extern` una variable `int dificultad` y un `const char *nombre_region`, y la función `subir_dificultad` (que no pasa de 5).
- `config.c` las **define** (dificultad empieza en 1; la región es `"Forjas de Hierro"`).
- `combate.c` tiene `describir_enemigo`, que muestra la región y una vida de `20 * dificultad`.
- `main.c` describe un enemigo, sube la dificultad dos veces, lo vuelve a describir y después intenta subirla 5 veces más.

#### Criterio de aprobación

- `extern` en el `.h` y una sola definición en `config.c`.
- Compila los tres `.c` juntos sin advertencias.
- `subir_dificultad` no pasa de 5.

#### Salida esperada

```
Enemigo de las Forjas de Hierro con 20 de vida
dificultad ahora: 3
Enemigo de las Forjas de Hierro con 60 de vida
dificultad máxima: 5
```

#### Solución de referencia

```c
/* ===== config.h ===== */
#ifndef CONFIG_H
#define CONFIG_H

/* extern: "esta variable existe, pero esta definida en otro archivo". */
extern int dificultad;
extern const char *nombre_region;

void subir_dificultad(void);

#endif

/* ===== config.c ===== */
#include "config.h"

int dificultad = 1;                       /* la definicion: una sola vez en todo el programa */
const char *nombre_region = "Forjas de Hierro";

void subir_dificultad(void)
{
    if (dificultad < 5) {
        dificultad++;
    }
}

/* ===== combate.c ===== */
#include <stdio.h>

#include "config.h"

void describir_enemigo(void)
{
    printf("Enemigo de las %s con %d de vida\n", nombre_region, 20 * dificultad);
}

/* ===== main.c ===== */
#include <stdio.h>

#include "config.h"

void describir_enemigo(void);

int main(void)
{
    describir_enemigo();
    subir_dificultad();
    subir_dificultad();
    printf("dificultad ahora: %d\n", dificultad);
    describir_enemigo();
    for (int i = 0; i < 5; i++) {
        subir_dificultad();
    }
    printf("dificultad máxima: %d\n", dificultad);
    return 0;
}
```

### Misión R04-N03-M3 · El modo depuración

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

1. Definí una macro `LOG(...)` que, si se compila con `-DDEPURAR`, muestre el mensaje en `stderr` con el prefijo `[depurar] `; si no, no haga nada (`((void) 0)`). Usá `__VA_ARGS__`.
2. Definí `MAX(a, b)` y `CUADRADO(x)` bien protegidas con paréntesis.
3. En `danio(ataque, defensa)` (mínimo 1) dejá un `LOG` con los valores. Mostrá dos daños y `CUADRADO(2 + 3)`.
4. Compilá con y sin `-DDEPURAR` y comparalo. La salida esperada es **sin** depuración.

#### Criterio de aprobación

- `LOG` solo produce salida con `-DDEPURAR`, y en `stderr`.
- Las macros tienen paréntesis en cada parámetro y alrededor.
- `CUADRADO(2 + 3)` da 25.

#### Salida esperada

```
daño: 11
daño: 1
área: 25
```

#### Solución de referencia

```c
/* Mision 3 - El modo depuracion: mensajes que solo aparecen al compilar con -DDEPURAR. */
#include <stdio.h>

#ifdef DEPURAR
#define LOG(...) fprintf(stderr, "[depurar] " __VA_ARGS__)
#else
#define LOG(...) ((void) 0)
#endif

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define CUADRADO(x) ((x) * (x))

int danio(int ataque, int defensa)
{
    int d = MAX(ataque - defensa, 1);
    LOG("danio(%d, %d) = %d\n", ataque, defensa, d);
    return d;
}

int main(void)
{
    LOG("arranca el programa\n");
    printf("daño: %d\n", danio(15, 4));
    printf("daño: %d\n", danio(3, 9));
    printf("área: %d\n", CUADRADO(2 + 3));   /* con parentesis en la macro: 25, no 11 */
    return 0;
}
```

### Encargo R04-N03-E1 · La biblioteca de fechas

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 15
extensiones: zip, c, h
```

#### Consigna

Convertí las fechas del Gremio (el encargo del nodo de structs) en un módulo reutilizable: `fecha.h` con el `typedef` y las funciones públicas (`fecha_valida`, `fecha_comparar`, `fecha_siguiente`, `fecha_mostrar`), y `fecha.c` con su código; `es_bisiesto` y `dias_del_mes` quedan `static`. Probalo desde un `main.c` con el 31/12/2025, el 28/02/2024, el 28/02/2026 y el 31/04/2026, y preguntando si el 10/03/2026 vence antes que el 28/02/2026.

#### Criterio de aprobación

- El `.h` expone solo lo público, con include guard.
- Los ayudantes son `static`.
- Las pruebas dan bien, incluida la fecha inválida.

#### Salida esperada

```
31/12/2025 -> 01/01/2026
28/02/2024 -> 29/02/2024
28/02/2026 -> 01/03/2026
31/04/2026 no es válida
¿Vence antes de hoy? no
```

#### Solución de referencia

```c
/* ===== fecha.h ===== */
#ifndef FECHA_H
#define FECHA_H

#include <stdbool.h>

typedef struct {
    int dia, mes, anio;
} Fecha;

bool fecha_valida(Fecha f);
int fecha_comparar(Fecha a, Fecha b);
Fecha fecha_siguiente(Fecha f);
void fecha_mostrar(Fecha f);

#endif /* FECHA_H */

/* ===== fecha.c ===== */
#include "fecha.h"

#include <stdio.h>

static bool es_bisiesto(int anio)
{
    return (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
}

static int dias_del_mes(int mes, int anio)
{
    static const int dias[] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
    return mes == 2 && es_bisiesto(anio) ? 29 : dias[mes - 1];
}

bool fecha_valida(Fecha f)
{
    return f.mes >= 1 && f.mes <= 12 && f.dia >= 1 && f.dia <= dias_del_mes(f.mes, f.anio);
}

int fecha_comparar(Fecha a, Fecha b)
{
    if (a.anio != b.anio) return a.anio - b.anio;
    if (a.mes != b.mes) return a.mes - b.mes;
    return a.dia - b.dia;
}

Fecha fecha_siguiente(Fecha f)
{
    if (++f.dia > dias_del_mes(f.mes, f.anio)) {
        f.dia = 1;
        if (++f.mes > 12) {
            f.mes = 1;
            f.anio++;
        }
    }
    return f;
}

void fecha_mostrar(Fecha f)
{
    printf("%02d/%02d/%04d", f.dia, f.mes, f.anio);
}

/* ===== main.c ===== */
#include <stdio.h>

#include "fecha.h"

int main(void)
{
    Fecha prueba[] = { { 31, 12, 2025 }, { 28, 2, 2024 }, { 28, 2, 2026 }, { 31, 4, 2026 } };
    for (int i = 0; i < 4; i++) {
        fecha_mostrar(prueba[i]);
        if (!fecha_valida(prueba[i])) {
            printf(" no es válida\n");
            continue;
        }
        printf(" -> ");
        fecha_mostrar(fecha_siguiente(prueba[i]));
        printf("\n");
    }
    Fecha vence = { 10, 3, 2026 }, hoy = { 28, 2, 2026 };
    printf("¿Vence antes de hoy? %s\n", fecha_comparar(vence, hoy) < 0 ? "sí" : "no");
    return 0;
}
```

### Prueba del sello

#### ¿Qué va en un `.h` y qué en un `.c`?

En el `.h`, las declaraciones: prototipos, tipos y constantes (lo que el módulo ofrece). En el `.c`, el código de las funciones y lo privado.

#### ¿Para qué sirve un include guard?

Para que, si el `.h` se incluye más de una vez, su contenido se procese una sola vez y no haya definiciones repetidas.

#### ¿Qué hace `static` delante de una función que está afuera de todo?

La hace visible solo dentro de ese archivo.

#### ¿Qué diferencia hay entre declarar con `extern` y definir una variable?

`extern` avisa que existe en otro lado; la definición reserva la memoria y se hace una sola vez en todo el programa.

#### Si aparece `undefined reference to ...`, ¿quién falla y qué falta?

El enlazador: falta compilar o enlazar el `.c` (o la biblioteca) que tiene esa función.

#### ¿Cuánto da `CUADRADO(2 + 3)` con `#define CUADRADO(x) x * x`?

11, porque queda `2 + 3 * 2 + 3`. Con paréntesis en todos lados da 25.

### Soluciones (docente)

Unidad nueva (en `02-C-Intermedio` estaba planificada como 23; había una carpeta `pendiente-23-ArenaMultiarchivo` incompleta). Las entregas de varios archivos van como `.zip`.

## R04-N04 · Argumentos de la línea de comandos

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: orco
temas: prog.argumentos
```

### Crónica

Los herreros viejos del Archivo no usan menús: le dan la orden a la herramienta **al encenderla**. "Templá a 900". "Contá las líneas de estos tres libros". Y la herramienta hace eso, sin preguntar nada.

—Así se escriben las herramientas de verdad, {heroe} —dice {mentor}—. Las que se pueden encadenar con otras, o dejar trabajando solas de noche.

### Objetivos

- Recibir los datos al ejecutar el programa con `int main(int argc, char *argv[])`.
- Convertir argumentos a números con `strtol`/`strtod` detectando errores.
- Procesar opciones como `-v` o `-n 3`, mostrar un mensaje de uso y devolver un **código de salida** correcto.

### Antes de empezar

- Strings (11), punteros y `strtol` (13).
- Archivos de texto (R04-N01).

### Explicación

#### `argc` y `argv`

```c
int main(int argc, char *argv[])
```

Si ejecutás `./forja templar 900`:

| | valor |
|---|---|
| `argc` | `3` (cuántos textos hay, **contando el nombre del programa**) |
| `argv[0]` | `"./forja"` |
| `argv[1]` | `"templar"` |
| `argv[2]` | `"900"` |
| `argv[3]` | `NULL` |

Todos los argumentos son **textos**: `"900"` no es el número 900.

#### Convertir con control

`atoi("9x")` devuelve 9 sin avisar que sobra la `x`. `strtol` sí avisa, porque deja en `fin` dónde terminó de leer:

```c
char *fin;
errno = 0;
long n = strtol(texto, &fin, 10);
if (fin == texto || *fin != '\0' || errno == ERANGE) {
    /* no era un número completo, o era demasiado grande */
}
```

Para decimales, `strtod` funciona igual.

#### Opciones

Las opciones empiezan con `-`. Se recorren los argumentos y se decide qué es cada uno:

```c
for (int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-v") == 0) {
        detallado = true;
    } else if (strcmp(argv[i], "-n") == 0 && i + 1 < argc) {
        veces = ...argv[i + 1]...;
        i++;                        /* ese argumento ya se usó */
    } else { ... }
}
```

#### El código de salida

Lo que devuelve `main` le dice a la terminal cómo terminó el programa: `EXIT_SUCCESS` (0) si todo bien, `EXIT_FAILURE` (1) si no. Los errores y el mensaje de uso van a **`stderr`**, así no se mezclan con la salida:

```bash
./forja templar hola ; echo "terminó con $?"
./forja templar 900 && echo "todo bien"      # && solo sigue si el anterior devolvió 0
```

#### Probarlo

Estos programas se prueban **escribiendo los argumentos** en la terminal. Por eso las misiones muestran ejemplos de uso en la consigna en lugar de una "entrada de ejemplo".

### Código de ejemplo

```c
/*
 * 24 - argc y argv: los datos que se escriben al ejecutar el programa.
 *   ./programa templar 900       ./programa -v templar 1300
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <stdbool.h>

/* Convierte un texto a entero con strtol, avisando si no es un numero completo. */
bool a_entero(const char *texto, long *resultado)
{
    char *fin;
    errno = 0;
    long n = strtol(texto, &fin, 10);
    if (fin == texto || *fin != '\0' || errno == ERANGE) {
        return false;
    }
    *resultado = n;
    return true;
}

void uso(const char *programa)
{
    fprintf(stderr, "Uso: %s [-v] templar GRADOS\n", programa);
}

int main(int argc, char *argv[])
{
    bool detallado = false;
    int i = 1;
    if (i < argc && strcmp(argv[i], "-v") == 0) {
        detallado = true;
        i++;
    }
    if (argc - i != 2 || strcmp(argv[i], "templar") != 0) {
        uso(argv[0]);
        return EXIT_FAILURE;                    /* 1: algo salio mal */
    }
    long grados;
    if (!a_entero(argv[i + 1], &grados) || grados < 0) {
        fprintf(stderr, "\"%s\" no es una temperatura válida\n", argv[i + 1]);
        return EXIT_FAILURE;
    }
    if (detallado) {
        printf("argc = %d\n", argc);
        for (int k = 0; k < argc; k++) {
            printf("argv[%d] = \"%s\"\n", k, argv[k]);
        }
    }
    printf("A %ld °C el hierro está %s.\n", grados, grados < 900 ? "demasiado frío" : grados <= 1200 ? "listo para forjar" : "a punto de fundirse");
    return EXIT_SUCCESS;                        /* 0: todo bien */
}
```

### ¿Para qué sirve?

Casi todas las herramientas de la terminal funcionan así: `ls -l carpeta`, `gcc -Wall -o programa main.c`, `git commit -m "mensaje"`, `ping -c 3 servidor`. Recibir argumentos permite automatizar: un script puede llamar a tu programa mil veces con datos distintos, y el código de salida le dice si cada llamada salió bien. Es la base de los scripts de instalación, de los servidores y de las tareas programadas.

### Errores habituales

**Orco: `argv[1]` sin argumentos.** Si se ejecuta sin nada, `argv[1]` es `NULL` y usarlo corta el programa. Siempre se revisa `argc` primero.

**Goblin: `atoi` que no avisa.** `atoi("12abc")` da 12 y `atoi("hola")` da 0, sin error. Con `strtol` se detecta.

**Ogro: el `*` de la terminal.** `./calc 3 * 4` no funciona: la terminal reemplaza `*` por los nombres de los archivos de la carpeta. Se escribe entre comillas: `./calc 3 '*' 4`.

**Ogro: el código de salida equivocado.** Devolver 0 después de un error hace que un script crea que todo salió bien.

**Ogro: el error en `stdout`.** El mensaje de uso con `printf` se mezcla con la salida real (y termina adentro de un archivo si se redirige con `>`).

### Misión R04-N04-M1 · La calculadora de la terminal

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una calculadora que recibe la cuenta como argumentos:

```
$ ./calc 12 + 30
42
$ ./calc 7.5 '*' 2
15
$ ./calc 3 / 0
No se puede dividir por cero          (en stderr, código de salida 1)
$ ./calc 3 +
Uso: ./calc NUMERO OPERADOR NUMERO    (en stderr, código de salida 1)
```

Convertí los números con `strtod` controlando que sean completos, aceptá `x` como sinónimo de `*`, y devolvé `EXIT_SUCCESS` o `EXIT_FAILURE`.

#### Criterio de aprobación

- Revisa `argc` antes de usar `argv`.
- Convierte con `strtod` y detecta textos que no son números.
- Los errores van a `stderr` con código de salida 1.

#### Solución de referencia

```c
/* Mision 1 - La calculadora de linea de comandos: ./calc 12 + 30 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <stdbool.h>

bool a_numero(const char *texto, double *resultado)
{
    char *fin;
    errno = 0;
    double x = strtod(texto, &fin);
    if (fin == texto || *fin != '\0' || errno == ERANGE) {
        return false;
    }
    *resultado = x;
    return true;
}

int main(int argc, char *argv[])
{
    if (argc != 4 || strlen(argv[2]) != 1) {
        fprintf(stderr, "Uso: %s NUMERO OPERADOR NUMERO   (el * va entre comillas: '*')\n", argv[0]);
        return EXIT_FAILURE;
    }
    double a, b;
    if (!a_numero(argv[1], &a) || !a_numero(argv[3], &b)) {
        fprintf(stderr, "Los dos operandos tienen que ser números\n");
        return EXIT_FAILURE;
    }
    double r;
    switch (argv[2][0]) {
    case '+': r = a + b; break;
    case '-': r = a - b; break;
    case 'x':
    case '*': r = a * b; break;
    case '/':
        if (b == 0) {
            fprintf(stderr, "No se puede dividir por cero\n");
            return EXIT_FAILURE;
        }
        r = a / b;
        break;
    default:
        fprintf(stderr, "Operador desconocido: %s\n", argv[2]);
        return EXIT_FAILURE;
    }
    printf("%g\n", r);
    return EXIT_SUCCESS;
}
```

### Misión R04-N04-M2 · Contar las líneas de los libros

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `contar`, que muestra cuántas líneas tiene cada archivo que recibe como argumento, y el total si son varios. Si no recibe ninguno, cuenta las líneas de la entrada estándar. Un archivo que no se puede abrir se informa con `perror` y se sigue con los demás (el programa termina con código 1).

```
$ ./contar diario.txt notas.csv
3 diario.txt
4 notas.csv
7 total
$ ./contar no_existe.txt diario.txt
no_existe.txt: No such file or directory
3 diario.txt
$ echo -e "a\nb" | ./contar
2 (entrada)
```

#### Criterio de aprobación

- Recorre `argv` desde 1.
- Sin argumentos, lee de `stdin`.
- Informa los archivos que no abren y sigue; devuelve 1 si hubo errores.

#### Solución de referencia

```c
/* Mision 2 - Contar lineas de los archivos que se pasan: ./contar a.txt b.txt (sin archivos: lee la entrada) */
#include <stdio.h>
#include <stdlib.h>

long contar(FILE *f)
{
    long lineas = 0;
    int c;
    while ((c = fgetc(f)) != EOF) {
        if (c == '\n') {
            lineas++;
        }
    }
    return lineas;
}

int main(int argc, char *argv[])
{
    if (argc == 1) {
        printf("%ld (entrada)\n", contar(stdin));
        return EXIT_SUCCESS;
    }
    int errores = 0;
    long total = 0;
    for (int i = 1; i < argc; i++) {
        FILE *f = fopen(argv[i], "r");
        if (f == NULL) {
            perror(argv[i]);
            errores++;
            continue;
        }
        long n = contar(f);
        fclose(f);
        printf("%ld %s\n", n, argv[i]);
        total += n;
    }
    if (argc > 2) {
        printf("%ld total\n", total);
    }
    return errores ? EXIT_FAILURE : EXIT_SUCCESS;
}
```

### Misión R04-N04-M3 · Opciones con guion

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `saludo [-m] [-n VECES] NOMBRE`: saluda al nombre, en mayúsculas con `-m` y la cantidad de veces que diga `-n` (por defecto 1). Las opciones pueden ir en cualquier orden. Informá opciones desconocidas, un `-n` sin número válido, argumentos que sobran y la falta del nombre.

```
$ ./saludo Kira
¡Salud, Kira!
$ ./saludo -n 2 -m Bron
¡Salud, BRON!
¡Salud, BRON!
$ ./saludo -x Mia
Opción desconocida: -x
```

#### Criterio de aprobación

- Procesa las opciones en cualquier orden.
- Salta el argumento que usó `-n`.
- Valida con `strtol` y avisa cada error en `stderr` con código 1.

#### Solución de referencia

```c
/* Mision 3 - Opciones con guion: ./saludo [-m] [-n VECES] NOMBRE */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[])
{
    int mayusculas = 0;
    long veces = 1;
    const char *nombre = NULL;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-m") == 0) {
            mayusculas = 1;
        } else if (strcmp(argv[i], "-n") == 0) {
            char *fin;
            if (i + 1 >= argc || (veces = strtol(argv[i + 1], &fin, 10)) < 1 || *fin != '\0') {
                fprintf(stderr, "-n necesita un número positivo\n");
                return EXIT_FAILURE;
            }
            i++;                                   /* el numero ya se uso */
        } else if (argv[i][0] == '-') {
            fprintf(stderr, "Opción desconocida: %s\n", argv[i]);
            return EXIT_FAILURE;
        } else if (nombre == NULL) {
            nombre = argv[i];
        } else {
            fprintf(stderr, "Sobra: %s\n", argv[i]);
            return EXIT_FAILURE;
        }
    }
    if (nombre == NULL) {
        fprintf(stderr, "Uso: %s [-m] [-n VECES] NOMBRE\n", argv[0]);
        return EXIT_FAILURE;
    }
    for (long k = 0; k < veces; k++) {
        printf("¡Salud, ");
        for (const char *p = nombre; *p; p++) {
            putchar(mayusculas ? toupper((unsigned char) *p) : *p);
        }
        printf("!\n");
    }
    return EXIT_SUCCESS;
}
```

### Encargo R04-N04-E1 · El cambio de monedas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La casa de cambio del Gremio quiere una herramienta: `cambio MONTO DESDE HACIA`, con las monedas USD, ARS (1200 por dólar), EUR (0.92) y BRL (5.4) guardadas en una tabla.

```
$ ./cambio 1500 ARS USD
1500.00 ARS = 1.25 USD
$ ./cambio 100 EUR BRL
100.00 EUR = 586.96 BRL
$ ./cambio diez USD ARS
Monto inválido: diez
```

#### Criterio de aprobación

- Busca las monedas en una tabla.
- Valida el monto con `strtod`.
- Errores en `stderr` con código de salida 1.

#### Solución de referencia

```c
/* Encargo - El conversor de monedas del Gremio: ./cambio 1500 ARS USD */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *codigo;
    double por_dolar;      /* cuanto vale un dolar en esta moneda */
} Moneda;

static const Moneda MONEDAS[] = { { "USD", 1 }, { "ARS", 1200 }, { "EUR", 0.92 }, { "BRL", 5.4 } };

const Moneda *buscar(const char *codigo)
{
    for (size_t i = 0; i < sizeof(MONEDAS) / sizeof(MONEDAS[0]); i++) {
        if (strcmp(MONEDAS[i].codigo, codigo) == 0) {
            return &MONEDAS[i];
        }
    }
    return NULL;
}

int main(int argc, char *argv[])
{
    if (argc != 4) {
        fprintf(stderr, "Uso: %s MONTO DESDE HACIA   (monedas: USD ARS EUR BRL)\n", argv[0]);
        return EXIT_FAILURE;
    }
    char *fin;
    double monto = strtod(argv[1], &fin);
    const Moneda *desde = buscar(argv[2]), *hacia = buscar(argv[3]);
    if (*fin != '\0' || fin == argv[1] || monto < 0) {
        fprintf(stderr, "Monto inválido: %s\n", argv[1]);
        return EXIT_FAILURE;
    }
    if (desde == NULL || hacia == NULL) {
        fprintf(stderr, "Moneda desconocida\n");
        return EXIT_FAILURE;
    }
    printf("%.2f %s = %.2f %s\n", monto, desde->codigo, monto / desde->por_dolar * hacia->por_dolar, hacia->codigo);
    return EXIT_SUCCESS;
}
```

### Prueba del sello

#### Si ejecutás `./juego -v nivel3`, ¿cuánto vale `argc` y qué hay en `argv[2]`?

`argc` vale 3 y `argv[2]` es `"nivel3"`.

#### ¿Qué ventaja tiene `strtol` sobre `atoi`?

Permite saber si el texto era un número completo (con el puntero `fin`) y si se pasó de rango (`errno`); `atoi` no avisa nada.

#### ¿Qué significan los códigos de salida 0 y 1? ¿Cómo se ven?

0 es éxito y distinto de 0 es error. Se ven con `echo $?` después de ejecutar.

#### ¿Por qué los mensajes de error van a `stderr`?

Para no mezclarse con la salida normal: si se redirige con `>`, el error sigue apareciendo en pantalla y el archivo queda limpio.

#### ¿Por qué `./calc 3 * 4` no funciona?

Porque la terminal reemplaza `*` por los archivos de la carpeta. Hay que escribirlo entre comillas.

### Soluciones (docente)

Unidad nueva (planificada como 24). Las salidas dependen de los argumentos: se muestran como ejemplos de uso en la consigna. En el súper test, el docente solo verifica que compile y no se corte.

## R04-N05 · El menú de consola

```meta
tipo: tema
padre: R04-N04
precio: 10
criatura: ogro
temas: prog.menu
```

### Crónica

En la posada de la Forja, el posadero tiene un cartel con opciones: descansar, entrenar, trabajar, comprar. Cada noche los aprendices eligen, algo cambia, y el cartel vuelve a aparecer.

—Esto es lo que late dentro de todo juego, {heroe} —dice {mentor}—. Mostrar cómo está el mundo, preguntar qué hacés, cambiar el mundo. Y otra vez. Y otra vez.

### Objetivos

- Escribir el **bucle de menú**: mostrar el estado, leer una opción válida, actuar y repetir.
- Guardar el estado del programa en un struct y cambiarlo con funciones.
- Terminar bien: con la opción de salir, con confirmación o cuando se termina la entrada.

### Antes de empezar

- Bucles y validación de la entrada (07), `switch` (06).
- Punteros a structs (14) y punteros a función (R03-N04).

### Explicación

#### La forma de todo programa interactivo

```c
Jugador kira = { ... };            /* 1) el estado */
bool jugando = true;
while (jugando) {
    mostrar_estado(&kira);         /* 2) mostrar */
    int opcion;
    if (!pedir_opcion(0, 4, &opcion)) {
        break;                     /* se terminó la entrada: salir ordenado */
    }
    switch (opcion) {              /* 3) actuar */
    case 1: ... break;
    case 0: jugando = false; break;
    }
}
```

Tres ideas:

- **El estado en un struct.** Todo lo que cambia (vida, oro, fuerza) vive en un lugar; las acciones reciben un puntero y lo modifican.
- **Una sola función de lectura** que no devuelve hasta tener una opción válida (o hasta que se termina la entrada).
- **Una salida ordenada**: la opción 0, o `fgets` que devuelve `NULL`. Un menú que no revisa el fin de la entrada se queda repitiendo para siempre.

#### Del `switch` a la tabla

Cuando las opciones crecen, el `switch` se vuelve larguísimo. Con los punteros a función de la rama anterior, el menú puede ser una **tabla** de `{ texto, función }`: mostrarlo es recorrerla y actuar es `MENU[opcion - 1].accion(&kira)`. Agregar una opción es agregar una fila.

#### Del menú al *game loop*

Un videojuego hace exactamente esto, 60 veces por segundo: leer la entrada (teclado, joystick), actualizar el estado, dibujar. La diferencia es que no se **espera** a que el usuario elija: si no tocó nada, el mundo sigue. Es lo que vas a ver si seguís la Senda de la Forja Viva.

#### Probarlo sin tipear

Guardá las opciones en un archivo, una por línea, y ejecutá `./programa < entrada.txt`. Como las respuestas no se muestran, en la salida las preguntas quedan pegadas a lo que sigue.

### Código de ejemplo

```c
/*
 * 25 - El menu de consola: estado + mostrar opciones + leer + actuar, en bucle.
 * Es la antesala del "game loop" de los videojuegos.
 */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int vida, vida_max, oro, fuerza;
} Jugador;

bool pedir_opcion(int minimo, int maximo, int *opcion)
{
    char linea[50];
    for (;;) {
        printf("Elegí: ");
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%d %c", opcion, &sobra) == 1 && *opcion >= minimo && *opcion <= maximo) {
            return true;
        }
        printf("\n  Opción inválida.\n");
    }
}

void mostrar_estado(const Jugador *j)
{
    printf("\n[vida %d/%d | oro %d | fuerza %d]\n", j->vida, j->vida_max, j->oro, j->fuerza);
    printf("1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir\n");
}

int main(void)
{
    Jugador kira = { 30, 50, 10, 5 };
    bool jugando = true;
    while (jugando) {
        mostrar_estado(&kira);
        int opcion;
        if (!pedir_opcion(0, 4, &opcion)) {
            break;                                   /* se termino la entrada */
        }
        printf("\n");
        switch (opcion) {
        case 1:
            kira.vida = kira.vida_max;
            printf("Dormís en la posada. Vida completa.\n");
            break;
        case 2:
            if (kira.vida <= 10) {
                printf("Estás demasiado cansada para entrenar.\n");
            } else {
                kira.vida -= 10;
                kira.fuerza++;
                printf("Entrenás con Bron. +1 de fuerza.\n");
            }
            break;
        case 3:
            kira.oro += 15;
            printf("Trabajás en la forja. +15 de oro.\n");
            break;
        case 4:
            if (kira.oro < 20) {
                printf("No te alcanza el oro.\n");
            } else {
                kira.oro -= 20;
                kira.vida_max += 5;
                printf("La poción fortalece: +5 de vida máxima.\n");
            }
            break;
        case 0:
            jugando = false;
            break;
        }
    }
    printf("\nHasta mañana. Fuerza final: %d, oro: %d.\n", kira.fuerza, kira.oro);
    return 0;
}
```

### Entrada de ejemplo

```
3
4
2
2
2
9
1
0
```

### Salida esperada

```
[vida 30/50 | oro 10 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Trabajás en la forja. +15 de oro.

[vida 30/50 | oro 25 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
La poción fortalece: +5 de vida máxima.

[vida 30/55 | oro 5 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Entrenás con Bron. +1 de fuerza.

[vida 20/55 | oro 5 | fuerza 6]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Entrenás con Bron. +1 de fuerza.

[vida 10/55 | oro 5 | fuerza 7]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Estás demasiado cansada para entrenar.

[vida 10/55 | oro 5 | fuerza 7]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
  Opción inválida.
Elegí: 
Dormís en la posada. Vida completa.

[vida 55/55 | oro 5 | fuerza 7]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 

Hasta mañana. Fuerza final: 7, oro: 5.
```

### ¿Para qué sirve?

El bucle de menú está en los cajeros automáticos, las terminales de autoservicio, los instaladores de programas, las herramientas de configuración de un router por consola y los sistemas de punto de venta. Y es la forma de todo videojuego: el *game loop* de cualquier motor (Unity, Godot, SDL) es este mismo bucle, sin esperar a que el jugador elija.

### Errores habituales

**Ogro: el bucle infinito al final de la entrada.** Sin revisar lo que devuelve `fgets`, cuando se termina la entrada el programa repite el menú para siempre.

**Ogro: el `break` que falta.** En el `switch`, una opción sin `break` ejecuta también la siguiente: entrenar y además trabajar.

**Goblin: `scanf("%d")` con letras.** Si el usuario escribe `dos`, las letras quedan en la entrada y el menú falla una y otra vez. Con `fgets` + `sscanf` no pasa.

**Ogro: el estado copiado.** Pasar el `Jugador` por valor a la acción: cambia la copia y el jugador sigue igual.

**Ogro: descontar sin revisar.** Comprar con oro insuficiente y quedar con oro negativo.

### Misión R04-N05-M1 · Apostar en la taberna

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Partiendo del ejemplo, agregá la opción `5) Apostar (10 oro)`: si no alcanza el oro, avisá; si no, con 50 % de probabilidad ganás 20 de oro y si no perdés 10. Usá `srand(5)` para poder probarlo siempre igual (y dejá comentado cómo sería con `time(NULL)`).

#### Criterio de aprobación

- El menú acepta la opción 5.
- Controla el oro antes de apostar.
- Usa `rand() % 2` con semilla fija.

#### Código inicial

```c
/*
 * 25 - El menu de consola: estado + mostrar opciones + leer + actuar, en bucle.
 * Es la antesala del "game loop" de los videojuegos.
 */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int vida, vida_max, oro, fuerza;
} Jugador;

bool pedir_opcion(int minimo, int maximo, int *opcion)
{
    char linea[50];
    for (;;) {
        printf("Elegí: ");
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%d %c", opcion, &sobra) == 1 && *opcion >= minimo && *opcion <= maximo) {
            return true;
        }
        printf("\n  Opción inválida.\n");
    }
}

void mostrar_estado(const Jugador *j)
{
    printf("\n[vida %d/%d | oro %d | fuerza %d]\n", j->vida, j->vida_max, j->oro, j->fuerza);
    printf("1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir\n");
}

int main(void)
{
    Jugador kira = { 30, 50, 10, 5 };
    bool jugando = true;
    while (jugando) {
        mostrar_estado(&kira);
        int opcion;
        if (!pedir_opcion(0, 4, &opcion)) {
            break;                                   /* se termino la entrada */
        }
        printf("\n");
        switch (opcion) {
        case 1:
            kira.vida = kira.vida_max;
            printf("Dormís en la posada. Vida completa.\n");
            break;
        case 2:
            if (kira.vida <= 10) {
                printf("Estás demasiado cansada para entrenar.\n");
            } else {
                kira.vida -= 10;
                kira.fuerza++;
                printf("Entrenás con Bron. +1 de fuerza.\n");
            }
            break;
        case 3:
            kira.oro += 15;
            printf("Trabajás en la forja. +15 de oro.\n");
            break;
        case 4:
            if (kira.oro < 20) {
                printf("No te alcanza el oro.\n");
            } else {
                kira.oro -= 20;
                kira.vida_max += 5;
                printf("La poción fortalece: +5 de vida máxima.\n");
            }
            break;
        case 0:
            jugando = false;
            break;
        }
    }
    printf("\nHasta mañana. Fuerza final: %d, oro: %d.\n", kira.fuerza, kira.oro);
    return 0;
}
```

#### Entrada de ejemplo

```
5
3
5
5
5
4
0
```

#### Salida esperada

```
[vida 30/50 | oro 10 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  5) Apostar (10 oro)  0) Salir
Elegí: 
Perdés la apuesta. -10 de oro.

[vida 30/50 | oro 0 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  5) Apostar (10 oro)  0) Salir
Elegí: 
Trabajás en la forja. +15 de oro.

[vida 30/50 | oro 15 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  5) Apostar (10 oro)  0) Salir
Elegí: 
Perdés la apuesta. -10 de oro.

[vida 30/50 | oro 5 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  5) Apostar (10 oro)  0) Salir
Elegí: 
No te alcanza para apostar.

[vida 30/50 | oro 5 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  5) Apostar (10 oro)  0) Salir
Elegí: 
No te alcanza para apostar.

[vida 30/50 | oro 5 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  5) Apostar (10 oro)  0) Salir
Elegí: 
No te alcanza el oro.

[vida 30/50 | oro 5 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  5) Apostar (10 oro)  0) Salir
Elegí: 

Hasta mañana. Fuerza final: 5, oro: 5.
```

#### Solución de referencia

```c
/*
 * Mision 1 - Apostar en la taberna: una opcion nueva con azar (semilla fija para probar).
 */
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct {
    int vida, vida_max, oro, fuerza;
} Jugador;

bool pedir_opcion(int minimo, int maximo, int *opcion)
{
    char linea[50];
    for (;;) {
        printf("Elegí: ");
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%d %c", opcion, &sobra) == 1 && *opcion >= minimo && *opcion <= maximo) {
            return true;
        }
        printf("\n  Opción inválida.\n");
    }
}

void mostrar_estado(const Jugador *j)
{
    printf("\n[vida %d/%d | oro %d | fuerza %d]\n", j->vida, j->vida_max, j->oro, j->fuerza);
    printf("1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  5) Apostar (10 oro)  0) Salir\n");
}

int main(void)
{
    srand(5);                 /* fija para probar; para jugar: srand(time(NULL)) */
    Jugador kira = { 30, 50, 10, 5 };
    bool jugando = true;
    while (jugando) {
        mostrar_estado(&kira);
        int opcion;
        if (!pedir_opcion(0, 5, &opcion)) {
            break;                                   /* se termino la entrada */
        }
        printf("\n");
        switch (opcion) {
        case 1:
            kira.vida = kira.vida_max;
            printf("Dormís en la posada. Vida completa.\n");
            break;
        case 2:
            if (kira.vida <= 10) {
                printf("Estás demasiado cansada para entrenar.\n");
            } else {
                kira.vida -= 10;
                kira.fuerza++;
                printf("Entrenás con Bron. +1 de fuerza.\n");
            }
            break;
        case 3:
            kira.oro += 15;
            printf("Trabajás en la forja. +15 de oro.\n");
            break;
        case 4:
            if (kira.oro < 20) {
                printf("No te alcanza el oro.\n");
            } else {
                kira.oro -= 20;
                kira.vida_max += 5;
                printf("La poción fortalece: +5 de vida máxima.\n");
            }
            break;
        case 5:
            if (kira.oro < 10) {
                printf("No te alcanza para apostar.\n");
            } else if (rand() % 2 == 0) {
                kira.oro += 20;
                printf("¡Ganás la apuesta! +20 de oro.\n");
            } else {
                kira.oro -= 10;
                printf("Perdés la apuesta. -10 de oro.\n");
            }
            break;
        case 0:
            jugando = false;
            break;
        }
    }
    printf("\nHasta mañana. Fuerza final: %d, oro: %d.\n", kira.fuerza, kira.oro);
    return 0;
}
```

### Misión R04-N05-M2 · El menú como tabla

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Reescribí el menú del ejemplo sin `switch`: cada acción es una función `void accion(Jugador *j)` y el menú es una **tabla** de structs `{ texto, función }`. El menú se muestra recorriendo la tabla y la opción elegida se ejecuta con `MENU[opcion - 1].accion(&kira)`. La cantidad de opciones sale de `sizeof` de la tabla.

#### Criterio de aprobación

- No usa `switch` para las acciones.
- El menú se arma recorriendo la tabla.
- Agregar una opción es agregar una fila (la validación usa el tamaño de la tabla).

#### Código inicial

```c
/*
 * 25 - El menu de consola: estado + mostrar opciones + leer + actuar, en bucle.
 * Es la antesala del "game loop" de los videojuegos.
 */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int vida, vida_max, oro, fuerza;
} Jugador;

bool pedir_opcion(int minimo, int maximo, int *opcion)
{
    char linea[50];
    for (;;) {
        printf("Elegí: ");
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%d %c", opcion, &sobra) == 1 && *opcion >= minimo && *opcion <= maximo) {
            return true;
        }
        printf("\n  Opción inválida.\n");
    }
}

void mostrar_estado(const Jugador *j)
{
    printf("\n[vida %d/%d | oro %d | fuerza %d]\n", j->vida, j->vida_max, j->oro, j->fuerza);
    printf("1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir\n");
}

int main(void)
{
    Jugador kira = { 30, 50, 10, 5 };
    bool jugando = true;
    while (jugando) {
        mostrar_estado(&kira);
        int opcion;
        if (!pedir_opcion(0, 4, &opcion)) {
            break;                                   /* se termino la entrada */
        }
        printf("\n");
        switch (opcion) {
        case 1:
            kira.vida = kira.vida_max;
            printf("Dormís en la posada. Vida completa.\n");
            break;
        case 2:
            if (kira.vida <= 10) {
                printf("Estás demasiado cansada para entrenar.\n");
            } else {
                kira.vida -= 10;
                kira.fuerza++;
                printf("Entrenás con Bron. +1 de fuerza.\n");
            }
            break;
        case 3:
            kira.oro += 15;
            printf("Trabajás en la forja. +15 de oro.\n");
            break;
        case 4:
            if (kira.oro < 20) {
                printf("No te alcanza el oro.\n");
            } else {
                kira.oro -= 20;
                kira.vida_max += 5;
                printf("La poción fortalece: +5 de vida máxima.\n");
            }
            break;
        case 0:
            jugando = false;
            break;
        }
    }
    printf("\nHasta mañana. Fuerza final: %d, oro: %d.\n", kira.fuerza, kira.oro);
    return 0;
}
```

#### Entrada de ejemplo

```
3
4
2
2
2
9
1
0
```

#### Salida esperada

```
[vida 30/50 | oro 10 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Trabajás en la forja. +15 de oro.

[vida 30/50 | oro 25 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
La poción fortalece: +5 de vida máxima.

[vida 30/55 | oro 5 | fuerza 5]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Entrenás con Bron. +1 de fuerza.

[vida 20/55 | oro 5 | fuerza 6]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Entrenás con Bron. +1 de fuerza.

[vida 10/55 | oro 5 | fuerza 7]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Estás demasiado cansada para entrenar.

[vida 10/55 | oro 5 | fuerza 7]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
  Opción inválida.
Elegí: 
Dormís en la posada. Vida completa.

[vida 55/55 | oro 5 | fuerza 7]
1) Descansar  2) Entrenar (-10 vida)  3) Trabajar en la forja (+15 oro)  4) Comprar poción (20 oro)  0) Salir
Elegí: 
Hasta mañana. Fuerza final: 7, oro: 5.
```

#### Solución de referencia

```c
/* Mision 2 - El menu como tabla: cada opcion es un texto y una funcion. Agregar una es agregar una fila. */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int vida, vida_max, oro, fuerza;
} Jugador;

void descansar(Jugador *j) { j->vida = j->vida_max; printf("Dormís en la posada. Vida completa.\n"); }
void entrenar(Jugador *j)
{
    if (j->vida <= 10) {
        printf("Estás demasiado cansada para entrenar.\n");
        return;
    }
    j->vida -= 10;
    j->fuerza++;
    printf("Entrenás con Bron. +1 de fuerza.\n");
}
void trabajar(Jugador *j) { j->oro += 15; printf("Trabajás en la forja. +15 de oro.\n"); }
void comprar(Jugador *j)
{
    if (j->oro < 20) {
        printf("No te alcanza el oro.\n");
        return;
    }
    j->oro -= 20;
    j->vida_max += 5;
    printf("La poción fortalece: +5 de vida máxima.\n");
}

typedef struct {
    const char *texto;
    void (*accion)(Jugador *);
} Opcion;

static const Opcion MENU[] = {
    { "Descansar", descansar },
    { "Entrenar (-10 vida)", entrenar },
    { "Trabajar en la forja (+15 oro)", trabajar },
    { "Comprar poción (20 oro)", comprar },
};
#define OPCIONES ((int) (sizeof(MENU) / sizeof(MENU[0])))

bool pedir_opcion(int *opcion)
{
    char linea[50];
    for (;;) {
        printf("Elegí: ");
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%d %c", opcion, &sobra) == 1 && *opcion >= 0 && *opcion <= OPCIONES) {
            return true;
        }
        printf("\n  Opción inválida.\n");
    }
}

int main(void)
{
    Jugador kira = { 30, 50, 10, 5 };
    for (;;) {
        printf("\n[vida %d/%d | oro %d | fuerza %d]\n", kira.vida, kira.vida_max, kira.oro, kira.fuerza);
        for (int i = 0; i < OPCIONES; i++) {
            printf("%d) %s  ", i + 1, MENU[i].texto);
        }
        printf("0) Salir\n");
        int opcion;
        if (!pedir_opcion(&opcion) || opcion == 0) {
            break;
        }
        printf("\n");
        MENU[opcion - 1].accion(&kira);
    }
    printf("\nHasta mañana. Fuerza final: %d, oro: %d.\n", kira.fuerza, kira.oro);
    return 0;
}
```

### Misión R04-N05-M3 · La tienda y la despedida

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí un menú con `1) Tienda`, `2) Trabajar (+15 oro)` y `0) Salir`:

- La tienda es un **submenú** propio (flechas ×10 por 5 de oro, poción por 20, `0) Volver`) que se repite hasta volver.
- Salir pide confirmación (`¿Seguro que querés salir? (s/n)`): solo sale con `s` o `S`.
- Si se termina la entrada en cualquier lugar, el programa termina ordenado.

#### Criterio de aprobación

- La tienda es una función con su propio bucle.
- Pide confirmación para salir.
- Termina ordenado si se acaba la entrada.

#### Entrada de ejemplo

```
1
1
2
3
0
2
0
n
1
2
0
0
s
```

#### Salida esperada

```
[vida 40 | oro 45 | flechas 0 | pociones 0]
1) Tienda  2) Trabajar (+15 oro)  0) Salir
Elegí: 
  -- Tienda (oro 45) --  1) Flechas x10 (5)  2) Poción (20)  0) Volver
  Elegí: 
  +10 flechas.

  -- Tienda (oro 40) --  1) Flechas x10 (5)  2) Poción (20)  0) Volver
  Elegí: 
  +1 poción.

  -- Tienda (oro 20) --  1) Flechas x10 (5)  2) Poción (20)  0) Volver
  Elegí: 
  Opción inválida.
  Elegí: 
[vida 40 | oro 20 | flechas 10 | pociones 1]
1) Tienda  2) Trabajar (+15 oro)  0) Salir
Elegí: 
Trabajás en la forja.

[vida 40 | oro 35 | flechas 10 | pociones 1]
1) Tienda  2) Trabajar (+15 oro)  0) Salir
Elegí: ¿Seguro que querés salir? (s/n): 

[vida 40 | oro 35 | flechas 10 | pociones 1]
1) Tienda  2) Trabajar (+15 oro)  0) Salir
Elegí: 
  -- Tienda (oro 35) --  1) Flechas x10 (5)  2) Poción (20)  0) Volver
  Elegí: 
  +1 poción.

  -- Tienda (oro 15) --  1) Flechas x10 (5)  2) Poción (20)  0) Volver
  Elegí: 
[vida 40 | oro 15 | flechas 10 | pociones 2]
1) Tienda  2) Trabajar (+15 oro)  0) Salir
Elegí: ¿Seguro que querés salir? (s/n): 

Chau. Te llevás 10 flechas y 2 pociones.
```

#### Solución de referencia

```c
/* Mision 3 - Salir con confirmacion y un submenu de tienda. */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int vida, oro, flechas, pociones;
} Jugador;

bool pedir_linea(const char *pregunta, char *linea, int tam)
{
    printf("%s", pregunta);
    return fgets(linea, tam, stdin) != NULL;
}

bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *opcion)
{
    char linea[50];
    for (;;) {
        if (!pedir_linea(pregunta, linea, sizeof(linea))) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%d %c", opcion, &sobra) == 1 && *opcion >= minimo && *opcion <= maximo) {
            return true;
        }
        printf("\n  Opción inválida.\n");
    }
}

void tienda(Jugador *j)
{
    for (;;) {
        printf("\n  -- Tienda (oro %d) --  1) Flechas x10 (5)  2) Poción (20)  0) Volver\n", j->oro);
        int op;
        if (!pedir_opcion("  Elegí: ", 0, 2, &op) || op == 0) {
            return;
        }
        int precio = op == 1 ? 5 : 20;
        printf("\n");
        if (j->oro < precio) {
            printf("  No alcanza.\n");
        } else if (op == 1) {
            j->oro -= precio;
            j->flechas += 10;
            printf("  +10 flechas.\n");
        } else {
            j->oro -= precio;
            j->pociones++;
            printf("  +1 poción.\n");
        }
    }
}

bool confirmar(void)
{
    char linea[20];
    if (!pedir_linea("¿Seguro que querés salir? (s/n): ", linea, sizeof(linea))) {
        return true;
    }
    printf("\n");
    return linea[0] == 's' || linea[0] == 'S';
}

int main(void)
{
    Jugador kira = { 40, 45, 0, 0 };
    for (;;) {
        printf("\n[vida %d | oro %d | flechas %d | pociones %d]\n", kira.vida, kira.oro, kira.flechas, kira.pociones);
        printf("1) Tienda  2) Trabajar (+15 oro)  0) Salir\n");
        int op;
        if (!pedir_opcion("Elegí: ", 0, 2, &op)) {
            break;
        }
        if (op == 1) {
            tienda(&kira);
        } else if (op == 2) {
            kira.oro += 15;
            printf("\nTrabajás en la forja.\n");
        } else if (confirmar()) {
            break;
        }
    }
    printf("\nChau. Te llevás %d flechas y %d pociones.\n", kira.flechas, kira.pociones);
    return 0;
}
```

### Encargo R04-N05-E1 · El cajero del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Escribí un cajero con saldo inicial de $5000 y las opciones: `1) Saldo`, `2) Depositar`, `3) Extraer`, `4) Movimientos` (los últimos 5, del más nuevo al más viejo, con signo) y `0) Salir`. Rechazá montos no positivos, extracciones mayores al saldo y opciones inexistentes.

#### Criterio de aprobación

- Guarda los últimos 5 movimientos (se cae el más viejo).
- Valida montos y saldo.
- Muestra los movimientos del más nuevo al más viejo.

#### Entrada de ejemplo

```
1
3
7000
3
1250.50
2
-3
2
800
4
9
0
```

#### Salida esperada

```
1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir
Opción: 
Saldo: $5000.00

1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir
Opción: 
Monto: 
Saldo insuficiente ($5000.00).

1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir
Opción: 
Monto: 
Listo. Saldo: $3749.50

1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir
Opción: 
Monto: 
El monto tiene que ser positivo.

1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir
Opción: 
Monto: 
Listo. Saldo: $4549.50

1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir
Opción: 
     +800.00
    -1250.50
    +5000.00

1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir
Opción: 
Opción inválida.

1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir
Opción: 
Gracias por usar el cajero del Gremio.
```

#### Solución de referencia

```c
/* Encargo - El cajero del Gremio: saldo, depositar, extraer y ultimos movimientos. */
#include <stdio.h>
#include <stdbool.h>

#define MOVIMIENTOS 5

typedef struct {
    double saldo;
    double ultimos[MOVIMIENTOS];     /* positivos: depositos; negativos: extracciones */
    int cantidad;
} Cuenta;

void registrar(Cuenta *c, double monto)
{
    if (c->cantidad == MOVIMIENTOS) {            /* se cae el mas viejo */
        for (int i = 1; i < MOVIMIENTOS; i++) {
            c->ultimos[i - 1] = c->ultimos[i];
        }
        c->cantidad--;
    }
    c->ultimos[c->cantidad++] = monto;
    c->saldo += monto;
}

bool pedir_numero(const char *pregunta, double *x)
{
    char linea[50];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%lf %c", x, &sobra) == 1) {
            return true;
        }
        printf("\n  Escribí un número.\n");
    }
}

int main(void)
{
    Cuenta c = { 0 };
    registrar(&c, 5000);
    for (;;) {
        printf("\n1) Saldo  2) Depositar  3) Extraer  4) Movimientos  0) Salir\n");
        double op, monto;
        if (!pedir_numero("Opción: ", &op) || op == 0) {
            break;
        }
        printf("\n");
        if (op == 1) {
            printf("Saldo: $%.2f\n", c.saldo);
        } else if (op == 2 || op == 3) {
            if (!pedir_numero("Monto: ", &monto)) {
                break;
            }
            printf("\n");
            if (monto <= 0) {
                printf("El monto tiene que ser positivo.\n");
            } else if (op == 3 && monto > c.saldo) {
                printf("Saldo insuficiente ($%.2f).\n", c.saldo);
            } else {
                registrar(&c, op == 2 ? monto : -monto);
                printf("Listo. Saldo: $%.2f\n", c.saldo);
            }
        } else if (op == 4) {
            for (int i = c.cantidad - 1; i >= 0; i--) {
                printf("  %+10.2f\n", c.ultimos[i]);
            }
        } else {
            printf("Opción inválida.\n");
        }
    }
    printf("\nGracias por usar el cajero del Gremio.\n");
    return 0;
}
```

### Prueba del sello

#### ¿Cuáles son las tres partes de cada vuelta de un menú?

Mostrar el estado y las opciones, leer una opción válida y actuar (cambiar el estado).

#### ¿Qué pasa si el menú no revisa lo que devuelve `fgets`?

Cuando se termina la entrada, sigue repitiendo para siempre con la última línea.

#### ¿Por qué las acciones reciben `Jugador *` y no `Jugador`?

Para modificar el jugador real y no una copia.

#### ¿Qué ventaja tiene el menú como tabla de funciones?

Agregar o sacar opciones es tocar una fila; el código que muestra y ejecuta no cambia.

#### ¿En qué se diferencia un *game loop* de este menú?

En que no espera a que el jugador elija: repite muchas veces por segundo leer la entrada, actualizar y dibujar, aunque no haya pasado nada.

### Soluciones (docente)

Reescrita desde cero a partir de `02-C-Intermedio/25-MenuConsola` (formato viejo).

## R04-N06 · Jefe: el Guardián del Archivo

```meta
tipo: jefe
padre: R04-N05
precio: 10
criatura: dragon
insignia: Sello del Archivo
insignia_descripcion: Venciste al Guardián del Archivo: tus programas guardan, cargan y se ordenan en módulos.
usa: prog.modulos, prog.menu, arch.binarios, mem.dinamica
```

### Crónica

En la puerta del último salón del Archivo espera el **Guardián**: una armadura vacía que no deja pasar a nadie que no sepa guardar lo suyo. Pide ver tu inventario, que lo guardes, que lo apagues todo… y que al volver esté exactamente igual.

—Es el examen de todo archivero, {heroe} —dice {mentor}—. Módulos ordenados, memoria que crece y se devuelve, un menú que no se rompe y archivos que no mienten.

### Objetivos

- Armar un programa completo en módulos (`.h` + `.c`) con un `Makefile`.
- Combinar memoria dinámica, menú de consola y archivos de texto y binarios.
- Diseñar funciones que no pierdan datos si algo falla (cargar sin pisar lo anterior).

### Antes de empezar

Todos los nodos de *El Archivo de la Forja*. Es un **proyecto integrador**: no hay teoría nueva.

### Explicación

#### El plano del proyecto

```
inventario.h   el tipo Inventario y sus funciones (la tapa)
inventario.c   cómo funcionan: array dinámico, buscar, guardar, cargar
main.c         el menú: solo usa lo que ofrece inventario.h
Makefile       cómo se compila
```

`main.c` **no sabe** cómo está hecho el inventario por dentro. Si mañana se cambia el array dinámico por una lista enlazada, `main.c` no se toca: esa es la ventaja de los módulos.

#### Cargar sin perder

Una carga puede fallar a la mitad (el archivo no existe, está cortado). Si se borra el inventario **antes** de leer, un error lo deja vacío. La forma segura:

1. Leer todo en un inventario **nuevo**.
2. Si salió bien, recién ahí liberar el viejo y reemplazarlo.

#### Probar sin tipear

```bash
make
./programa < entrada.txt
gcc -g -fsanitize=address -o programa main.c inventario.c && ./programa < entrada.txt   # sin fugas
```

#### La entrega

Un `.zip` con `inventario.h`, `inventario.c`, `main.c` y el `Makefile`.

### ¿Para qué sirve?

Es la estructura de cualquier sistema de gestión chico: el stock de un comercio, la biblioteca de una escuela, el inventario de un juego de rol, la lista de pacientes de un consultorio. Módulos separados, datos en memoria que se guardan en un archivo y un menú para operar: con esto ya se puede escribir software útil para alguien de verdad.

### Errores habituales

El Guardián combina a las criaturas de toda la rama:

- **Esqueleto**: `undefined reference` por no compilar `inventario.c`.
- **Troll**: cargar liberando primero el inventario viejo, y perderlo si el archivo no abre.
- **Goblin**: `%s` en lugar de `%23[^;]` al leer el CSV (el nombre se come los números).
- **Orco**: quitar más de lo que hay y quedar con cantidad negativa.
- **Troll**: olvidar `inv_liberar` al salir (fuga).
- **Ogro**: un archivo binario de otra versión leído como si fuera de esta.

### Misión R04-N06-M1 · El inventario del Archivo

```meta
entrega: archivo
entorno: local
monedas: 6
xp: 30
extensiones: zip, c, h
```

#### Consigna

Escribí el inventario en tres archivos:

- `inventario.h` con `Item` (nombre de 24, cantidad, valor), `Inventario` (array dinámico) y las funciones `inv_iniciar`, `inv_liberar`, `inv_agregar` (si el nombre ya existe suma la cantidad), `inv_quitar` (si llega a 0 lo saca; `false` si no existe o no alcanza), `inv_valor_total`, `inv_mostrar`, `inv_guardar` e `inv_cargar` (texto, `nombre;cantidad;valor`).
- `inventario.c` con su código (lo privado, `static`).
- `main.c` con el menú `1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir`, arrancando con 3 pociones (15 c/u) y 40 flechas (1 c/u), y usando `inventario.txt`.

`inv_cargar` no pierde el inventario si el archivo no abre. Todo se libera al salir. Sumá un `Makefile` y entregá un `.zip`.

#### Criterio de aprobación

- Tres archivos más `Makefile`; `main.c` solo usa lo del `.h`.
- Array dinámico que crece; `inv_agregar` suma si ya existe.
- Guardar y cargar en texto; cargar no pierde datos si falla.
- Sin fugas (`-fsanitize=address`).

#### Entrada de ejemplo

```
x
5
1
2
Espada
1
120
2
Flecha
10
1
4
3
Flecha
50
3
Pocion
3
1
5
1
0
```

#### Salida esperada

```
1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Número del 0 al 5.
Elegí: 
  No se pudo cargar.

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Pocion       x3     15 c/u  =    45
  Flecha       x40     1 c/u  =    40
  Valor total: 85 de oro

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Nombre:   Cantidad:   Valor: 
  Agregado.

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Nombre:   Cantidad:   Valor: 
  Agregado.

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Guardado en inventario.txt

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Nombre:   Cantidad: 
  Hecho.

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Nombre:   Cantidad: 
  Hecho.

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Espada       x1    120 c/u  =   120
  Valor total: 120 de oro

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Cargado desde inventario.txt

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
  Pocion       x3     15 c/u  =    45
  Flecha       x50     1 c/u  =    50
  Espada       x1    120 c/u  =   120
  Valor total: 215 de oro

1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir
Elegí: 
El Guardián sella el Archivo. Valor final: 215 de oro.
```

#### Solución de referencia

```c
/* ===== inventario.h ===== */
#ifndef INVENTARIO_H
#define INVENTARIO_H

#include <stdbool.h>

typedef struct {
    char nombre[24];
    int cantidad;
    int valor;              /* precio unitario en oro */
} Item;

typedef struct {
    Item *datos;
    int cantidad;
    int capacidad;
} Inventario;

void inv_iniciar(Inventario *inv);
void inv_liberar(Inventario *inv);

/* Si el item ya existe suma la cantidad; si no, lo agrega. false si no hay memoria. */
bool inv_agregar(Inventario *inv, const char *nombre, int cantidad, int valor);

/* Resta; si llega a 0 lo quita. false si no existe o no hay tanta cantidad. */
bool inv_quitar(Inventario *inv, const char *nombre, int cantidad);

int inv_valor_total(const Inventario *inv);
void inv_mostrar(const Inventario *inv);

/* Texto: una linea "nombre;cantidad;valor" por item. Devuelven false si fallan. */
bool inv_guardar(const Inventario *inv, const char *ruta);
bool inv_cargar(Inventario *inv, const char *ruta);

#endif /* INVENTARIO_H */

/* ===== inventario.c ===== */
#include "inventario.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void inv_iniciar(Inventario *inv)
{
    inv->datos = NULL;
    inv->cantidad = 0;
    inv->capacidad = 0;
}

void inv_liberar(Inventario *inv)
{
    free(inv->datos);
    inv_iniciar(inv);
}

static int buscar(const Inventario *inv, const char *nombre)
{
    for (int i = 0; i < inv->cantidad; i++) {
        if (strcmp(inv->datos[i].nombre, nombre) == 0) {
            return i;
        }
    }
    return -1;
}

bool inv_agregar(Inventario *inv, const char *nombre, int cantidad, int valor)
{
    int i = buscar(inv, nombre);
    if (i >= 0) {
        inv->datos[i].cantidad += cantidad;
        return true;
    }
    if (inv->cantidad == inv->capacidad) {
        int nueva = inv->capacidad == 0 ? 4 : inv->capacidad * 2;
        Item *tmp = realloc(inv->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        inv->datos = tmp;
        inv->capacidad = nueva;
    }
    Item *it = &inv->datos[inv->cantidad++];
    snprintf(it->nombre, sizeof(it->nombre), "%s", nombre);
    it->cantidad = cantidad;
    it->valor = valor;
    return true;
}

bool inv_quitar(Inventario *inv, const char *nombre, int cantidad)
{
    int i = buscar(inv, nombre);
    if (i < 0 || cantidad > inv->datos[i].cantidad) {
        return false;
    }
    inv->datos[i].cantidad -= cantidad;
    if (inv->datos[i].cantidad == 0) {
        for (int k = i; k < inv->cantidad - 1; k++) {
            inv->datos[k] = inv->datos[k + 1];
        }
        inv->cantidad--;
    }
    return true;
}

int inv_valor_total(const Inventario *inv)
{
    int total = 0;
    for (int i = 0; i < inv->cantidad; i++) {
        total += inv->datos[i].cantidad * inv->datos[i].valor;
    }
    return total;
}

void inv_mostrar(const Inventario *inv)
{
    if (inv->cantidad == 0) {
        printf("  (vacío)\n");
        return;
    }
    for (int i = 0; i < inv->cantidad; i++) {
        const Item *it = &inv->datos[i];
        printf("  %-12s x%-3d %4d c/u  = %5d\n", it->nombre, it->cantidad, it->valor, it->cantidad * it->valor);
    }
    printf("  Valor total: %d de oro\n", inv_valor_total(inv));
}

bool inv_guardar(const Inventario *inv, const char *ruta)
{
    FILE *f = fopen(ruta, "w");
    if (f == NULL) {
        return false;
    }
    for (int i = 0; i < inv->cantidad; i++) {
        fprintf(f, "%s;%d;%d\n", inv->datos[i].nombre, inv->datos[i].cantidad, inv->datos[i].valor);
    }
    return fclose(f) == 0;
}

bool inv_cargar(Inventario *inv, const char *ruta)
{
    FILE *f = fopen(ruta, "r");
    if (f == NULL) {
        return false;
    }
    Inventario nuevo;
    inv_iniciar(&nuevo);
    char linea[100];
    while (fgets(linea, sizeof(linea), f) != NULL) {
        char nombre[24];
        int cantidad, valor;
        if (sscanf(linea, "%23[^;];%d;%d", nombre, &cantidad, &valor) == 3 && cantidad > 0 && valor >= 0) {
            inv_agregar(&nuevo, nombre, cantidad, valor);
        }
    }
    fclose(f);
    inv_liberar(inv);            /* recien ahora se reemplaza: si fallaba antes, no se perdia nada */
    *inv = nuevo;
    return true;
}

/* ===== main.c ===== */
#include <stdio.h>
#include <string.h>

#include "inventario.h"

#define RUTA "inventario.txt"

static bool pedir_linea(const char *pregunta, char *linea, int tam)
{
    printf("%s", pregunta);
    if (fgets(linea, tam, stdin) == NULL) {
        return false;
    }
    linea[strcspn(linea, "\n")] = '\0';
    return true;
}

static bool pedir_entero(const char *pregunta, int minimo, int maximo, int *n)
{
    char linea[50];
    for (;;) {
        if (!pedir_linea(pregunta, linea, sizeof(linea))) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%d %c", n, &sobra) == 1 && *n >= minimo && *n <= maximo) {
            return true;
        }
        printf("\n  Número del %d al %d.\n", minimo, maximo);
    }
}

int main(void)
{
    Inventario inv;
    inv_iniciar(&inv);
    remove(RUTA);                           /* para que cada prueba arranque igual */
    inv_agregar(&inv, "Pocion", 3, 15);
    inv_agregar(&inv, "Flecha", 40, 1);

    for (;;) {
        printf("\n1) Listar  2) Agregar  3) Quitar  4) Guardar  5) Cargar  0) Salir\n");
        int op;
        if (!pedir_entero("Elegí: ", 0, 5, &op) || op == 0) {
            break;
        }
        printf("\n");
        char nombre[24];
        int cantidad, valor;
        switch (op) {
        case 1:
            inv_mostrar(&inv);
            break;
        case 2:
            if (pedir_linea("  Nombre: ", nombre, sizeof(nombre)) && nombre[0] != '\0'
                && pedir_entero("  Cantidad: ", 1, 999, &cantidad) && pedir_entero("  Valor: ", 0, 9999, &valor)) {
                printf("\n  %s\n", inv_agregar(&inv, nombre, cantidad, valor) ? "Agregado." : "Sin memoria.");
            }
            break;
        case 3:
            if (pedir_linea("  Nombre: ", nombre, sizeof(nombre)) && pedir_entero("  Cantidad: ", 1, 999, &cantidad)) {
                printf("\n  %s\n", inv_quitar(&inv, nombre, cantidad) ? "Hecho." : "No hay tanto de eso.");
            }
            break;
        case 4:
            printf("  %s\n", inv_guardar(&inv, RUTA) ? "Guardado en " RUTA : "No se pudo guardar.");
            break;
        case 5:
            printf("  %s\n", inv_cargar(&inv, RUTA) ? "Cargado desde " RUTA : "No se pudo cargar.");
            break;
        }
    }
    printf("\nEl Guardián sella el Archivo. Valor final: %d de oro.\n", inv_valor_total(&inv));
    inv_liberar(&inv);
    remove(RUTA);
    return 0;
}
```

### Misión R04-N06-M2 · Vender y ordenar

```meta
entrega: archivo
entorno: local
monedas: 6
xp: 30
extensiones: zip, c, h
```

#### Consigna

Agregale al módulo del inventario:

- `int inv_vender(Inventario *inv, const char *nombre, int cantidad)`: quita la cantidad y devuelve el oro ganado (valor × cantidad), o `-1` si no se pudo.
- `void inv_mostrar_por_valor(const Inventario *inv)`: muestra los items ordenados por **valor total** de mayor a menor, **sin cambiar** el inventario (ordená una copia con `qsort`).

Escribí un `main.c` con `1) Listar  2) Listar por valor  3) Vender  0) Salir` que muestre el oro acumulado, arrancando con 3 pociones (15), 40 flechas (1), 1 espada (120) y 2 escudos (45).

#### Criterio de aprobación

- `inv_vender` devuelve el oro o -1.
- `inv_mostrar_por_valor` ordena una copia y la libera.
- El orden original del inventario no cambia.

#### Entrada de ejemplo

```
2
3
Escudo
1
3
Espada
2
1
0
```

#### Salida esperada

```
[oro: 0]  1) Listar  2) Listar por valor  3) Vender  0) Salir
Elegí: 
  Espada       x1    120 c/u  =   120
  Escudo       x2     45 c/u  =    90
  Pocion       x3     15 c/u  =    45
  Flecha       x40     1 c/u  =    40
  Valor total: 295 de oro

[oro: 0]  1) Listar  2) Listar por valor  3) Vender  0) Salir
Elegí: 
  Nombre:   Cantidad: 
  Vendido por 45 de oro.

[oro: 45]  1) Listar  2) Listar por valor  3) Vender  0) Salir
Elegí: 
  Nombre:   Cantidad: 
  No tenés tanto de eso.

[oro: 45]  1) Listar  2) Listar por valor  3) Vender  0) Salir
Elegí: 
  Pocion       x3     15 c/u  =    45
  Flecha       x40     1 c/u  =    40
  Espada       x1    120 c/u  =   120
  Escudo       x1     45 c/u  =    45
  Valor total: 250 de oro

[oro: 45]  1) Listar  2) Listar por valor  3) Vender  0) Salir
Elegí: 
Terminás con 45 de oro.
```

#### Solución de referencia

```c
/* ===== inventario.h ===== */
#ifndef INVENTARIO_H
#define INVENTARIO_H

#include <stdbool.h>

typedef struct {
    char nombre[24];
    int cantidad;
    int valor;              /* precio unitario en oro */
} Item;

typedef struct {
    Item *datos;
    int cantidad;
    int capacidad;
} Inventario;

void inv_iniciar(Inventario *inv);
void inv_liberar(Inventario *inv);

/* Si el item ya existe suma la cantidad; si no, lo agrega. false si no hay memoria. */
bool inv_agregar(Inventario *inv, const char *nombre, int cantidad, int valor);

/* Resta; si llega a 0 lo quita. false si no existe o no hay tanta cantidad. */
bool inv_quitar(Inventario *inv, const char *nombre, int cantidad);

int inv_valor_total(const Inventario *inv);
void inv_mostrar(const Inventario *inv);

/* Texto: una linea "nombre;cantidad;valor" por item. Devuelven false si fallan. */
/* Vende: quita la cantidad y devuelve el oro ganado (valor * cantidad), o -1 si no se pudo. */
int inv_vender(Inventario *inv, const char *nombre, int cantidad);

/* Muestra los items ordenados por valor total, de mayor a menor (sin cambiar el inventario). */
void inv_mostrar_por_valor(const Inventario *inv);

bool inv_guardar(const Inventario *inv, const char *ruta);
bool inv_cargar(Inventario *inv, const char *ruta);

#endif /* INVENTARIO_H */

/* ===== inventario.c ===== */
#include "inventario.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void inv_iniciar(Inventario *inv)
{
    inv->datos = NULL;
    inv->cantidad = 0;
    inv->capacidad = 0;
}

void inv_liberar(Inventario *inv)
{
    free(inv->datos);
    inv_iniciar(inv);
}

static int buscar(const Inventario *inv, const char *nombre)
{
    for (int i = 0; i < inv->cantidad; i++) {
        if (strcmp(inv->datos[i].nombre, nombre) == 0) {
            return i;
        }
    }
    return -1;
}

bool inv_agregar(Inventario *inv, const char *nombre, int cantidad, int valor)
{
    int i = buscar(inv, nombre);
    if (i >= 0) {
        inv->datos[i].cantidad += cantidad;
        return true;
    }
    if (inv->cantidad == inv->capacidad) {
        int nueva = inv->capacidad == 0 ? 4 : inv->capacidad * 2;
        Item *tmp = realloc(inv->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        inv->datos = tmp;
        inv->capacidad = nueva;
    }
    Item *it = &inv->datos[inv->cantidad++];
    snprintf(it->nombre, sizeof(it->nombre), "%s", nombre);
    it->cantidad = cantidad;
    it->valor = valor;
    return true;
}

bool inv_quitar(Inventario *inv, const char *nombre, int cantidad)
{
    int i = buscar(inv, nombre);
    if (i < 0 || cantidad > inv->datos[i].cantidad) {
        return false;
    }
    inv->datos[i].cantidad -= cantidad;
    if (inv->datos[i].cantidad == 0) {
        for (int k = i; k < inv->cantidad - 1; k++) {
            inv->datos[k] = inv->datos[k + 1];
        }
        inv->cantidad--;
    }
    return true;
}

int inv_valor_total(const Inventario *inv)
{
    int total = 0;
    for (int i = 0; i < inv->cantidad; i++) {
        total += inv->datos[i].cantidad * inv->datos[i].valor;
    }
    return total;
}

void inv_mostrar(const Inventario *inv)
{
    if (inv->cantidad == 0) {
        printf("  (vacío)\n");
        return;
    }
    for (int i = 0; i < inv->cantidad; i++) {
        const Item *it = &inv->datos[i];
        printf("  %-12s x%-3d %4d c/u  = %5d\n", it->nombre, it->cantidad, it->valor, it->cantidad * it->valor);
    }
    printf("  Valor total: %d de oro\n", inv_valor_total(inv));
}

bool inv_guardar(const Inventario *inv, const char *ruta)
{
    FILE *f = fopen(ruta, "w");
    if (f == NULL) {
        return false;
    }
    for (int i = 0; i < inv->cantidad; i++) {
        fprintf(f, "%s;%d;%d\n", inv->datos[i].nombre, inv->datos[i].cantidad, inv->datos[i].valor);
    }
    return fclose(f) == 0;
}

bool inv_cargar(Inventario *inv, const char *ruta)
{
    FILE *f = fopen(ruta, "r");
    if (f == NULL) {
        return false;
    }
    Inventario nuevo;
    inv_iniciar(&nuevo);
    char linea[100];
    while (fgets(linea, sizeof(linea), f) != NULL) {
        char nombre[24];
        int cantidad, valor;
        if (sscanf(linea, "%23[^;];%d;%d", nombre, &cantidad, &valor) == 3 && cantidad > 0 && valor >= 0) {
            inv_agregar(&nuevo, nombre, cantidad, valor);
        }
    }
    fclose(f);
    inv_liberar(inv);            /* recien ahora se reemplaza: si fallaba antes, no se perdia nada */
    *inv = nuevo;
    return true;
}

int inv_vender(Inventario *inv, const char *nombre, int cantidad)
{
    int i = buscar(inv, nombre);
    if (i < 0 || cantidad > inv->datos[i].cantidad) {
        return -1;
    }
    int oro = inv->datos[i].valor * cantidad;
    inv_quitar(inv, nombre, cantidad);
    return oro;
}

static int por_valor_total(const void *a, const void *b)
{
    const Item *x = a, *y = b;
    int vx = x->cantidad * x->valor, vy = y->cantidad * y->valor;
    return (vy > vx) - (vy < vx);
}

void inv_mostrar_por_valor(const Inventario *inv)
{
    if (inv->cantidad == 0) {
        printf("  (vacío)\n");
        return;
    }
    Item *copia = malloc(inv->cantidad * sizeof *copia);      /* ordenar una copia */
    if (copia == NULL) {
        return;
    }
    memcpy(copia, inv->datos, inv->cantidad * sizeof *copia);
    qsort(copia, inv->cantidad, sizeof *copia, por_valor_total);
    Inventario vista = { copia, inv->cantidad, inv->cantidad };
    inv_mostrar(&vista);
    free(copia);
}

/* ===== main.c ===== */
#include <stdio.h>
#include <string.h>

#include "inventario.h"

static bool pedir_linea(const char *pregunta, char *linea, int tam)
{
    printf("%s", pregunta);
    if (fgets(linea, tam, stdin) == NULL) {
        return false;
    }
    linea[strcspn(linea, "\n")] = '\0';
    return true;
}

static bool pedir_entero(const char *pregunta, int minimo, int maximo, int *n)
{
    char linea[50];
    for (;;) {
        if (!pedir_linea(pregunta, linea, sizeof(linea))) {
            return false;
        }
        char sobra;
        if (sscanf(linea, "%d %c", n, &sobra) == 1 && *n >= minimo && *n <= maximo) {
            return true;
        }
        printf("\n  Número del %d al %d.\n", minimo, maximo);
    }
}

int main(void)
{
    Inventario inv;
    inv_iniciar(&inv);
    inv_agregar(&inv, "Pocion", 3, 15);
    inv_agregar(&inv, "Flecha", 40, 1);
    inv_agregar(&inv, "Espada", 1, 120);
    inv_agregar(&inv, "Escudo", 2, 45);
    int oro = 0;

    for (;;) {
        printf("\n[oro: %d]  1) Listar  2) Listar por valor  3) Vender  0) Salir\n", oro);
        int op;
        if (!pedir_entero("Elegí: ", 0, 3, &op) || op == 0) {
            break;
        }
        printf("\n");
        if (op == 1) {
            inv_mostrar(&inv);
        } else if (op == 2) {
            inv_mostrar_por_valor(&inv);
        } else {
            char nombre[24];
            int cantidad;
            if (pedir_linea("  Nombre: ", nombre, sizeof(nombre)) && pedir_entero("  Cantidad: ", 1, 999, &cantidad)) {
                int ganado = inv_vender(&inv, nombre, cantidad);
                if (ganado < 0) {
                    printf("\n  No tenés tanto de eso.\n");
                } else {
                    oro += ganado;
                    printf("\n  Vendido por %d de oro.\n", ganado);
                }
            }
        }
    }
    printf("\nTerminás con %d de oro.\n", oro);
    inv_liberar(&inv);
    return 0;
}
```

### Encargo R04-N06-E1 · El stock en binario

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

El Gremio quiere guardar su stock (código, descripción, stock, precio) en un archivo **binario**, pero sin sorpresas: al principio del archivo va un **encabezado** con una marca (`"STK"`), la versión del formato (2) y la cantidad de productos.

- `guardar` escribe el encabezado y los productos.
- `cargar` rechaza archivos que no tienen la marca o que son de otra versión, e informa por qué.

Probalo con tres productos (uno sin stock), con un archivo de texto cualquiera y con un encabezado de la versión 1.

#### Criterio de aprobación

- Escribe y valida el encabezado (marca y versión).
- Rechaza archivos ajenos y de otra versión con un mensaje.
- Muestra los productos cargados.

#### Salida esperada

```
guardar: ok
cargados: 3
  CLV-01  Clavos x100   40  $   850.00
  MAR-02  Martillo      12  $  5200.00
  LIM-07  Lima fina      0  $  2300.50  (sin stock)
  (no es un archivo de stock)
cargar otro.dat: -1
  (versión 1: este programa lee la 2)
cargar viejo.dat: -1
```

#### Solución de referencia

```c
/*
 * Jefe R04 - Encargo: el stock del Gremio en binario, con encabezado de version.
 * Si el archivo es de otra version (o no es nuestro), no se carga.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAGIA "STK"
#define VERSION 2

typedef struct {
    char codigo[8];
    char descripcion[24];
    int stock;
    double precio;
} Producto;

typedef struct {
    char magia[4];          /* "STK\0": para reconocer que el archivo es nuestro */
    int version;
    int cantidad;
} Encabezado;

bool guardar(const char *ruta, const Producto *p, int n)
{
    FILE *f = fopen(ruta, "wb");
    if (f == NULL) {
        return false;
    }
    Encabezado e = { MAGIA, VERSION, n };
    bool ok = fwrite(&e, sizeof e, 1, f) == 1 && fwrite(p, sizeof *p, n, f) == (size_t) n;
    return fclose(f) == 0 && ok;
}

int cargar(const char *ruta, Producto *p, int maximo)
{
    FILE *f = fopen(ruta, "rb");
    if (f == NULL) {
        return -1;
    }
    Encabezado e;
    if (fread(&e, sizeof e, 1, f) != 1 || memcmp(e.magia, MAGIA, sizeof e.magia) != 0) {   /* memcmp: lo leido no tiene por que terminar en \0 */
        fclose(f);
        printf("  (no es un archivo de stock)\n");
        return -1;
    }
    if (e.version != VERSION) {
        fclose(f);
        printf("  (versión %d: este programa lee la %d)\n", e.version, VERSION);
        return -1;
    }
    int n = e.cantidad < maximo ? e.cantidad : maximo;
    int leidos = (int) fread(p, sizeof *p, n, f);
    fclose(f);
    return leidos;
}

int main(void)
{
    Producto stock[] = {
        { "CLV-01", "Clavos x100", 40, 850.0 },
        { "MAR-02", "Martillo", 12, 5200.0 },
        { "LIM-07", "Lima fina", 0, 2300.5 },
    };
    printf("guardar: %s\n", guardar("stock.dat", stock, 3) ? "ok" : "falló");

    Producto leidos[10];
    int n = cargar("stock.dat", leidos, 10);
    printf("cargados: %d\n", n);
    for (int i = 0; i < n; i++) {
        printf("  %-7s %-12s %3d  $%9.2f%s\n", leidos[i].codigo, leidos[i].descripcion, leidos[i].stock, leidos[i].precio,
               leidos[i].stock == 0 ? "  (sin stock)" : "");
    }

    /* Un archivo que no es nuestro */
    FILE *f = fopen("otro.dat", "wb");
    if (f != NULL) {
        fputs("hola, esto es texto", f);
        fclose(f);
    }
    printf("cargar otro.dat: %d\n", cargar("otro.dat", leidos, 10));

    /* Un archivo de una version vieja */
    Encabezado viejo = { MAGIA, 1, 0 };
    f = fopen("viejo.dat", "wb");
    if (f != NULL) {
        fwrite(&viejo, sizeof viejo, 1, f);
        fclose(f);
    }
    printf("cargar viejo.dat: %d\n", cargar("viejo.dat", leidos, 10));
    remove("stock.dat");
    remove("otro.dat");
    remove("viejo.dat");
    return 0;
}
```

### Prueba del sello

#### ¿Por qué `main.c` no debería acceder directamente a `inv.datos[i]`?

Porque así depende de cómo está hecho el inventario por dentro. Usando solo las funciones del `.h`, se puede cambiar la implementación sin tocar `main.c`.

#### ¿Por qué `inv_cargar` lee en un inventario nuevo antes de reemplazar el viejo?

Para no perder los datos si la carga falla a la mitad.

#### ¿Por qué `inv_mostrar_por_valor` ordena una copia?

Para no cambiar el orden del inventario original: mostrar no debería modificar nada.

#### ¿Para qué sirve el encabezado con marca y versión en un archivo binario?

Para reconocer que el archivo es del programa y en qué formato está, y no leer basura si cambió el struct o es otro archivo.

#### ¿Qué comando compila el proyecto con detección de fugas?

`gcc -g -fsanitize=address -o programa main.c inventario.c` (o agregar esas opciones al `Makefile`).

### Soluciones (docente)

Reescrito a partir de `02-C-Intermedio/28-ProyectoInventario` (usaba `scanf`; ahora usa la receta `fgets` + `sscanf` del curso).
