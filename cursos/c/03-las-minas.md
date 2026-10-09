# RAMA R03 · Las Minas: memoria y estructuras

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · Memoria dinámica

```meta
tipo: tema
padre: R02-N07
precio: 10
criatura: troll
temas: mem.dinamica
usa: mem.punteros
```

### Crónica

Bajo la Forja se abren **las Minas**, y en la boca espera **Hulda**, la capataz, con el pico al hombro y una tablilla donde anota cada vagoneta. Kira le pide diez para sacar mineral. Devuelve nueve.

Hulda la frena con una mano del tamaño de una pala: —Vagoneta que sacás, vagoneta que devolvés. Las que no vuelven, se las come la **Sanguijuela** del fondo. —Y la hace contar un chiste malo **frente a toda la mina**, como interés. El chiste es tan malo que nadie en las Minas vuelve a olvidarse una vagoneta.

—Acá la memoria se pide y se **devuelve** a mano —dice {mentor} desde la entrada—. Lo que no devolvés, un día falta.

### Objetivos

- Distinguir la **pila** (variables locales) del **montón** (memoria que se pide mientras el programa corre).
- Pedir memoria con `malloc`, `calloc` y `realloc`, revisar el `NULL` y devolverla con `free`.
- Reconocer las tres maldiciones de la memoria: la **fuga**, el **uso después de liberar** y la **doble liberación**.
- Detectarlas con `-fsanitize=address` y `valgrind`.

### Antes de empezar

- Punteros (13) y punteros a structs (14).
- `sizeof` (02) y arrays (10).

### Explicación

#### Pila y montón

Las variables locales viven en la **pila**: aparecen al entrar en la función y desaparecen al salir, y su tamaño se decide **al compilar**. Pero muchas veces el tamaño se conoce recién **al ejecutar**: cuántos enemigos hay, cuántas líneas tiene un archivo. Para eso está el **montón** (*heap*): un depósito del que se pide memoria cuando hace falta, y que dura **hasta que la devolvés**.

#### Las cuatro herramientas (`<stdlib.h>`)

| Función | Qué hace |
|---|---|
| `malloc(bytes)` | pide un bloque **sin inicializar** (basura) |
| `calloc(cantidad, tamaño)` | pide `cantidad × tamaño` bytes, **todos en cero** |
| `realloc(p, bytes)` | agranda o achica el bloque; **puede moverlo** a otra dirección |
| `free(p)` | devuelve el bloque |

```c
int *vida = malloc(n * sizeof *vida);   /* n enteros */
if (vida == NULL) {                     /* sin memoria: siempre se revisa */
    return 1;
}
...
free(vida);
vida = NULL;                            /* que no quede apuntando a nada */
```

- `sizeof *vida` es "el tamaño de lo que apunta `vida`": si mañana cambiás el tipo, la cuenta sigue bien.
- `free(NULL)` no hace nada: es seguro.

#### `realloc` con cuidado

`realloc` puede **mover** el bloque. Si falla, devuelve `NULL`… y el bloque viejo **sigue siendo tuyo**. Por eso se guarda en un temporal:

```c
int *tmp = realloc(vida, nuevo * sizeof *tmp);
if (tmp == NULL) {
    /* vida sigue valiendo: se puede seguir usando o liberar */
} else {
    vida = tmp;
}
```

Escribir `vida = realloc(vida, ...)` directo pierde el bloque si falla: una fuga.

#### La regla de oro

**Cada `malloc`, `calloc` o `realloc` que salió bien tiene exactamente un `free`.**

- Olvidar el `free` → **fuga** (*memory leak*): el programa ocupa cada vez más.
- Usar el bloque después del `free` → **uso después de liberar**: comportamiento indefinido.
- Hacer `free` dos veces → **doble liberación**: suele cortar el programa.

#### Cómo encontrar a la Sanguijuela

```bash
gcc -Wall -Wextra -g -fsanitize=address -o programa main.c
./programa                 # si hay fuga o mal uso, lo informa con el número de línea
valgrind ./programa        # otra herramienta: "All heap blocks were freed" es lo que querés ver
```

(`valgrind` se instala con `sudo apt install valgrind`.)

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo (la entrada de ejemplo ya está en la pestaña **Entrada**).
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**; las respuestas se escriben en la consola.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`
  - Con las respuestas en un archivo: `./programa < main.entrada.txt` (Linux) o `programa.exe < main.entrada.txt` (Windows).
  - Para contestar sin escribir: `echo 3 | ./programa` (Linux) o `echo 3 | programa.exe` (Windows).

### Código de ejemplo

```c
/*
 * 17 - Memoria dinamica: pedir memoria mientras el programa corre.
 * La cantidad de enemigos la decide el usuario: no se sabe al compilar.
 */
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    char linea[50];
    int n = 0;
    printf("¿Cuántos enemigos hay en la galería? ");
    if (fgets(linea, sizeof(linea), stdin) == NULL || sscanf(linea, "%d", &n) != 1 || n < 1 || n > 1000) {
        printf("\nCantidad inválida.\n");
        return 1;
    }
    printf("\n");

    /* malloc: n enteros, sin inicializar. Siempre se revisa el NULL. */
    int *vida = malloc(n * sizeof *vida);
    if (vida == NULL) {
        fprintf(stderr, "No hay memoria.\n");
        return 1;
    }
    for (int i = 0; i < n; i++) {
        vida[i] = 20 + i * 5;
    }

    /* calloc: cant x tam, TODO en cero. */
    int *golpes = calloc(n, sizeof *golpes);
    if (golpes == NULL) {
        free(vida);
        return 1;
    }

    printf("Galería con %d enemigos:\n", n);
    for (int i = 0; i < n; i++) {
        printf("  enemigo %d: vida %2d, golpes recibidos %d\n", i, vida[i], golpes[i]);
    }

    /* realloc: llegan 2 mas. Se guarda en un temporal por si falla. */
    int *mas = realloc(vida, (n + 2) * sizeof *vida);
    if (mas == NULL) {
        free(vida);
        free(golpes);
        return 1;
    }
    vida = mas;
    vida[n] = 99;
    vida[n + 1] = 7;
    n += 2;
    printf("Llegaron 2 más. Vidas: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", vida[i]);
    }
    printf("\n");

    /* Regla de oro: un free por cada malloc/calloc/realloc que salio bien. */
    free(vida);
    free(golpes);
    vida = NULL;
    golpes = NULL;
    printf("Memoria devuelta. La Sanguijuela se queda con hambre.\n");
    return 0;
}
```

### Entrada de ejemplo

```
3
```

### Salida esperada

```
¿Cuántos enemigos hay en la galería? 
Galería con 3 enemigos:
  enemigo 0: vida 20, golpes recibidos 0
  enemigo 1: vida 25, golpes recibidos 0
  enemigo 2: vida 30, golpes recibidos 0
Llegaron 2 más. Vidas: 20 25 30 99 7 
Memoria devuelta. La Sanguijuela se queda con hambre.
```

### ¿Para qué sirve?

Todo programa que trabaja con datos de tamaño desconocido usa el montón: un editor de texto que abre archivos de cualquier largo, un navegador que carga páginas, un juego que crea y destruye enemigos, una base de datos. Las fugas de memoria son un problema real: servidores que se ponen lentos después de días encendidos, celulares que se quedan sin memoria, juegos que se traban después de una hora. Por eso existen herramientas como `valgrind` y los sanitizadores, y por eso otros lenguajes (Java, Python) tienen un recolector de basura que libera por vos.

### Errores habituales

**Troll: la fuga.** Un `malloc` sin su `free`. No da error: el programa funciona… y ocupa cada vez más. Con `-fsanitize=address`:

```
==1234==ERROR: LeakSanitizer: detected memory leaks
Direct leak of 20 byte(s) in 1 object(s) allocated from:
    #1 0x... in main main.c:18
```

**Troll: usar después de liberar.** `free(vida); printf("%d", vida[0]);` puede "funcionar" o mostrar basura. El sanitizador lo marca como `heap-use-after-free`. Por eso, después del `free`, el puntero va a `NULL`.

**Troll: doble liberación.** `free(p); free(p);` → `free(): double free detected` y el programa se corta.

**Orco: pedir de menos.** `malloc(n)` en lugar de `malloc(n * sizeof(int))` reserva `n` **bytes**, no `n` enteros: escribir el último se sale del bloque (`heap-buffer-overflow`).

**Ogro: `realloc` sin temporal.** `v = realloc(v, ...)` pierde el bloque si falla.

**Ogro: olvidar el `+ 1` del texto.** Para copiar un texto hacen falta `strlen + 1` bytes: el `'\0'` también ocupa.

### Micro-misión R03-N01-P1 · Las vagonetas prestadas

```meta
lugar: Las Minas
personajes: Kira, Gheco, Hulda
carta: malloc y free | malloc(n * sizeof *p) pide memoria · devuelve NULL si no hay · free(p) la devuelve
recompensa: xp 10, oro 10
```

#### Escena
En la boca de las Minas, Hulda presta vagonetas y las anota en su tablilla. Kira pide lugar para guardar el peso de 5 cargas.
—Vagoneta que sacás, vagoneta que devolvés —dice Hulda, con el pico al hombro.

#### Gheco sugiere
`int *cargas = malloc(5 * sizeof *cargas);` pide lugar para 5 enteros. Si devuelve `NULL`, no hubo lugar. Al terminar, `free(cargas);`.

#### Desafío
Pedí la memoria y devolvela al final.

#### Código inicial
```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *cargas = ___;
    if (cargas == NULL) {
        printf("no hay vagonetas\n");
        return 1;
    }
    for (int i = 0; i < 5; i++) {
        cargas[i] = (i + 1) * 100;
    }
    printf("la ultima carga pesa %d\n", cargas[4]);
    ___;
    printf("vagonetas devueltas\n");
    return 0;
}
```

#### Salida esperada
```
la ultima carga pesa 500
vagonetas devueltas
```

#### Solución
```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *cargas = malloc(5 * sizeof *cargas);
    if (cargas == NULL) {
        printf("no hay vagonetas\n");
        return 1;
    }
    for (int i = 0; i < 5; i++) {
        cargas[i] = (i + 1) * 100;
    }
    printf("la ultima carga pesa %d\n", cargas[4]);
    free(cargas);
    printf("vagonetas devueltas\n");
    return 0;
}
```

#### Al superarla
Hulda tacha las cinco vagonetas de la tablilla, una por una. —Así me gusta. Ni un chiste malo.

#### Imagen
- La boca de las Minas: vías que se pierden en la oscuridad y vagonetas en fila.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) anota en una tablilla.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) empuja una vagoneta de vuelta.

### Micro-misión R03-N01-P2 · Tantas como haga falta

```meta
lugar: Las Minas
personajes: Kira, Gheco, Tizón
carta: Tamaño en ejecución | el tamaño puede venir de la entrada · malloc(n * sizeof *v) · con un array fijo habría que adivinar
recompensa: xp 10, oro 10
```

#### Escena
Tizón no sabe cuántas cargas van a llegar hoy: se lo dicen al empezar el turno. Con un array fijo tendría que adivinar. Con las vagonetas de Hulda, pide justo las que hacen falta.

#### Gheco sugiere
Se lee `n` y se pide `malloc(n * sizeof *v)`. Después se usa `v[i]` como cualquier array.

#### Desafío
Pedí lugar para `n` cargas.

#### Código inicial
```c
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
    printf("%d cargas, %d kg en total\n", n, total);
    free(v);
    return 0;
}
```

#### Entrada
```
4
120 80 200 50
```

#### Salida esperada
```
4 cargas, 450 kg en total
```

#### Solución
```c
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
    printf("%d cargas, %d kg en total\n", n, total);
    free(v);
    return 0;
}
```

#### Al superarla
Cuatrocientos cincuenta kilos en cuatro vagonetas, ni una de más. Tizón calcula que se ahorraron seis vagonetas vacías. Lo celebra solo.

#### Imagen
- Cuatro vagonetas cargadas de mineral en fila.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) cuenta vagonetas con los dedos.

### Micro-misión R03-N01-P3 · El chiste malo de Kira

```meta
lugar: Las Minas
personajes: Kira, Gheco, Hulda
criatura: troll
carta: Fugas | cada malloc con su free · lo que no se devuelve se pierde hasta que el programa termina · en un bucle, la fuga crece
recompensa: xp 10, oro 10
```

#### Escena
Kira pidió vagonetas en cada vuelta del turno y no devolvió ninguna. Hulda la frena con una mano del tamaño de una pala y la hace contar un chiste malo **frente a toda la mina**.
El chiste es tan malo que nadie en las Minas vuelve a olvidarse una vagoneta.

#### Gheco sugiere
Si en cada vuelta se hace un `malloc`, en cada vuelta hace falta un `free` cuando ya no se usa. Si no, el **troll** se va comiendo la memoria.

#### Desafío
Devolvé la vagoneta al final de cada vuelta.

#### Código inicial
```c
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
        printf("turno %d: %d kg\n", turno, *carga);
    }
    printf("vagonetas devueltas: %d\n", devueltas);
    return 0;
}
```

#### Salida esperada
```
turno 1: 50 kg
turno 2: 100 kg
turno 3: 150 kg
vagonetas devueltas: 3
```

#### Solución
```c
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
        printf("turno %d: %d kg\n", turno, *carga);
        free(carga);
        devueltas++;
    }
    printf("vagonetas devueltas: %d\n", devueltas);
    return 0;
}
```

#### Al superarla
Tres de tres. Hulda borra a Kira de la lista de deudores. Kira jura no volver a contar ese chiste nunca más. Toda la mina lo repite igual.

#### Imagen
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) cuenta un chiste, colorada, frente a una fila de mineros que no se ríen.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) con los brazos cruzados.
- Un troll chiquito se escabulle con una vagoneta.

### Micro-misión R03-N01-P4 · El texto a medida

```meta
lugar: Las Minas
personajes: Kira, Gheco, Chispa
carta: Copia dinámica | malloc(strlen(s) + 1) · el +1 es para el '\0' · strcpy copia y free libera
recompensa: xp 15, oro 15
```

#### Escena
Chispa quiere guardar el nombre de cada cliente en una vagoneta del tamaño **justo**, ni una letra de más («la vagoneta se cobra por letra»).

#### Gheco sugiere
Para copiar un texto en memoria dinámica: `char *copia = malloc(strlen(s) + 1);` (el `+1` es el `'\0'`) y `strcpy(copia, s);`.

#### Desafío
Completá el tamaño justo.

#### Código inicial
```c
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
    printf("%s ocupa %zu bytes\n", cliente, strlen(cliente) + 1);
    free(cliente);
    return 0;
}
```

#### Salida esperada
```
Hulda ocupa 6 bytes
```

#### Solución
```c
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
    printf("%s ocupa %zu bytes\n", cliente, strlen(cliente) + 1);
    free(cliente);
    return 0;
}
```

#### Al superarla
Seis bytes justos. Chispa le cobra a Hulda seis lingotes «por la vagoneta». Hulda le cobra un chiste. Chispa paga los seis lingotes.

#### Imagen
- Una vagoneta chiquita con un nombre grabado letra por letra.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) le extiende la mano a Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro), que lo mira sin pestañear.

### Misión R03-N01-M1 · Copiar textos con memoria justa

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

1. Escribí `char *duplicar(const char *texto)`, que pide con `malloc` **exactamente** la memoria necesaria, copia el texto y devuelve la copia (o `NULL` si no hay memoria).
2. Escribí `char *unir(const char *a, const char *separador, const char *b)`, que devuelve un texto nuevo con los tres pegados.
3. Duplicá `"Kira"`, cambiale la primera letra a la copia (para comprobar que es independiente) y armá `"Kira de las Forjas"` con `unir`.
4. Mostrá los resultados y cuántos bytes pediste, y liberá todo.

#### Criterio de aprobación

- Pide `strlen + 1` bytes (el `'\0'` también ocupa).
- Revisa el `NULL` de cada `malloc`.
- Libera cada texto una vez.
- Compila sin advertencias y sin fugas (`-fsanitize=address`).

#### Salida esperada

```
copia modificada: Mira
título: Kira de las Forjas (18 letras, 19 bytes pedidos)
```

#### Solución de referencia

```c
/* Mision 1 - Copiar textos: duplicar y unir con memoria justa. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *duplicar(const char *texto)
{
    char *copia = malloc(strlen(texto) + 1);      /* +1 para el '\0' */
    if (copia != NULL) {
        strcpy(copia, texto);
    }
    return copia;
}

char *unir(const char *a, const char *separador, const char *b)
{
    size_t largo = strlen(a) + strlen(separador) + strlen(b) + 1;
    char *todo = malloc(largo);
    if (todo != NULL) {
        snprintf(todo, largo, "%s%s%s", a, separador, b);
    }
    return todo;
}

int main(void)
{
    char *nombre = duplicar("Kira");
    char *titulo = unir(nombre, " de ", "las Forjas");
    if (nombre == NULL || titulo == NULL) {
        free(nombre);
        free(titulo);
        return 1;
    }
    nombre[0] = 'M';   /* la copia es independiente del texto original */
    printf("copia modificada: %s\n", nombre);
    printf("título: %s (%zu letras, %zu bytes pedidos)\n", titulo, strlen(titulo), strlen(titulo) + 1);
    free(nombre);
    free(titulo);
    return 0;
}
```

### Misión R03-N01-M2 · El mapa de la mina

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

1. Pedí la cantidad de filas y de columnas (de 1 a 20).
2. Reservá **un solo bloque** de `filas × columnas` enteros. La celda de la fila `f` y la columna `c` está en la posición `f * columnas + c`.
3. Llená cada celda con `(f * 7 + c * 3) % 10` (el oro que hay) y mostrá el mapa y el oro total.
4. Liberá el bloque.

#### Criterio de aprobación

- Reserva un solo bloque con `malloc` y revisa el `NULL`.
- Calcula la posición con `f * columnas + c`.
- Muestra el mapa y el total; libera la memoria.

#### Entrada de ejemplo

```
3
5
```

#### Salida esperada

```
Filas: Columnas: 
 0 3 6 9 2
 7 0 3 6 9
 4 7 0 3 6
Oro en la mina: 65
```

#### Solución de referencia

```c
/* Mision 2 - El mapa de la mina: una matriz del tamanio que pida el usuario, en un solo bloque. */
#include <stdio.h>
#include <stdlib.h>

int pedir(const char *pregunta)
{
    char linea[50];
    int n;
    printf("%s", pregunta);
    if (fgets(linea, sizeof(linea), stdin) == NULL || sscanf(linea, "%d", &n) != 1 || n < 1 || n > 20) {
        return -1;
    }
    return n;
}

int main(void)
{
    int filas = pedir("Filas: ");
    int columnas = pedir("Columnas: ");
    printf("\n");
    if (filas < 0 || columnas < 0) {
        printf("Tamaño inválido.\n");
        return 1;
    }
    /* un bloque de filas * columnas; la celda (f, c) esta en f * columnas + c */
    int *mapa = malloc((size_t) filas * columnas * sizeof *mapa);
    if (mapa == NULL) {
        return 1;
    }
    int total = 0;
    for (int f = 0; f < filas; f++) {
        for (int c = 0; c < columnas; c++) {
            mapa[f * columnas + c] = (f * 7 + c * 3) % 10;   /* oro en cada celda */
            total += mapa[f * columnas + c];
        }
    }
    for (int f = 0; f < filas; f++) {
        for (int c = 0; c < columnas; c++) {
            printf("%2d", mapa[f * columnas + c]);
        }
        printf("\n");
    }
    printf("Oro en la mina: %d\n", total);
    free(mapa);
    return 0;
}
```

#### Pruebas

##### Una celda
```entrada
1
1
```
```salida
Filas: Columnas:
 0
Oro en la mina: 0
```

##### Máximo
```entrada
20
20
```
```salida
Filas: Columnas:
 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7
 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4
 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1
 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8
 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5
 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2
 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9
 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6
 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3
 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0
 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7
 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4
 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1
 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8
 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5
 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9 2
 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6 9
 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3 6
 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0 3
 3 6 9 2 5 8 1 4 7 0 3 6 9 2 5 8 1 4 7 0
Oro en la mina: 1800
```

##### Fuera de rango
```entrada
0
21
2
2
```
```salida
Filas: Columnas:
Tamaño inválido.
```

### Misión R03-N01-M3 · Achicar el cofre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

1. Reservá un array de 10 enteros y llenalo con `i * 3 + 1`.
2. Escribí `int *solo_pares(int *v, int *n)`, que deja solo los pares al principio, achica el bloque con `realloc` a la cantidad nueva y **devuelve el puntero** (que puede haber cambiado). La cantidad nueva queda en `*n`.
3. Si no queda ninguno, liberá el bloque y devolvé `NULL`. Si `realloc` falla, devolvé el bloque viejo (que sigue siendo válido).
4. Mostrá el array antes y después, y liberalo.

#### Criterio de aprobación

- Usa `realloc` con un puntero temporal.
- Devuelve el puntero nuevo y la cantidad por `*n`.
- Trata aparte el caso de cero elementos.
- Sin fugas.

#### Salida esperada

```
antes (10): 1 4 7 10 13 16 19 22 25 28
después (5): 4 10 16 22 28
```

#### Solución de referencia

```c
/* Mision 3 - Achicar el cofre: quedarse con los pares y devolver la memoria que sobra. */
#include <stdio.h>
#include <stdlib.h>

/* Deja solo los pares al principio y achica el bloque. Devuelve el puntero nuevo. */
int *solo_pares(int *v, int *n)
{
    int k = 0;
    for (int i = 0; i < *n; i++) {
        if (v[i] % 2 == 0) {
            v[k++] = v[i];
        }
    }
    if (k == 0) {                 /* realloc con 0 es ambiguo: mejor liberar a mano */
        free(v);
        *n = 0;
        return NULL;
    }
    int *chico = realloc(v, k * sizeof *v);
    if (chico == NULL) {          /* si falla, el bloque viejo sigue siendo valido */
        *n = k;
        return v;
    }
    *n = k;
    return chico;
}

int main(void)
{
    int n = 10;
    int *cofre = malloc(n * sizeof *cofre);
    if (cofre == NULL) {
        return 1;
    }
    for (int i = 0; i < n; i++) {
        cofre[i] = i * 3 + 1;
    }
    printf("antes (%d):", n);
    for (int i = 0; i < n; i++) {
        printf(" %d", cofre[i]);
    }
    cofre = solo_pares(cofre, &n);
    printf("\ndespués (%d):", n);
    for (int i = 0; i < n; i++) {
        printf(" %d", cofre[i]);
    }
    printf("\n");
    free(cofre);
    return 0;
}
```

### Encargo R03-N01-E1 · Las notas del curso

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La escuela del Gremio no sabe de antemano cuántas notas va a cargar. Pedí la cantidad, reservá un array de `double` de ese tamaño y leé las notas (de 0 a 10, lo inválido se vuelve a pedir). Mostrá el promedio y las notas que lo superan, y liberá la memoria.

#### Criterio de aprobación

- Reserva exactamente la cantidad pedida.
- Valida cada nota.
- Muestra el promedio y las que lo superan; libera la memoria.

#### Entrada de ejemplo

```
4
7
9.5
once
4
8
```

#### Salida esperada

```
¿Cuántas notas? Nota 1: Nota 2: Nota 3: (de 0 a 10) Nota 3: Nota 4: 
Promedio: 7.12
Arriba del promedio: 9.5 8.0
```

#### Solución de referencia

```c
/* Encargo - Las notas del curso: tantas como diga el profe, ni una mas. */
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    char linea[50];
    int n;
    printf("¿Cuántas notas? ");
    if (fgets(linea, sizeof(linea), stdin) == NULL || sscanf(linea, "%d", &n) != 1 || n < 1) {
        printf("\nCantidad inválida.\n");
        return 1;
    }
    double *notas = malloc(n * sizeof *notas);
    if (notas == NULL) {
        return 1;
    }
    double suma = 0;
    int leidas = 0;
    while (leidas < n) {
        printf("Nota %d: ", leidas + 1);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            break;
        }
        double x;
        if (sscanf(linea, "%lf", &x) == 1 && x >= 0 && x <= 10) {
            notas[leidas++] = x;
            suma += x;
        } else {
            printf("(de 0 a 10) ");
        }
    }
    printf("\n");
    if (leidas == 0) {
        free(notas);
        return 1;
    }
    double promedio = suma / leidas;
    printf("Promedio: %.2f\nArriba del promedio:", promedio);
    for (int i = 0; i < leidas; i++) {
        if (notas[i] > promedio) {
            printf(" %.1f", notas[i]);
        }
    }
    printf("\n");
    free(notas);
    return 0;
}
```

#### Pruebas

##### Una sola nota
```entrada
1
10
```
```salida
¿Cuántas notas? Nota 1:
Promedio: 10.00
Arriba del promedio:
```

##### Todas iguales
```entrada
3
5
5
5
```
```salida
¿Cuántas notas? Nota 1: Nota 2: Nota 3:
Promedio: 5.00
Arriba del promedio:
```

##### Notas en el borde
```entrada
2
0
10
```
```salida
¿Cuántas notas? Nota 1: Nota 2:
Promedio: 5.00
Arriba del promedio: 10.0
```

### Prueba del sello

#### ¿Qué diferencia hay entre una variable local y un bloque pedido con `malloc`?

La local vive en la pila y desaparece al salir de la función; su tamaño se fija al compilar. El bloque de `malloc` vive en el montón hasta que lo liberás, y su tamaño se decide al ejecutar.

#### ¿Qué diferencia hay entre `malloc(10 * sizeof(int))` y `calloc(10, sizeof(int))`?

Los dos piden lugar para 10 enteros; `calloc` además los pone en cero y `malloc` los deja con basura.

#### ¿Por qué no se escribe `v = realloc(v, nuevo);`?

Porque si `realloc` falla devuelve `NULL`: se pierde la única dirección del bloque viejo (fuga). Se usa un temporal.

#### ¿Cuántos bytes hay que pedir para copiar el texto `"Orco"`?

5: las 4 letras y el `'\0'` (`strlen + 1`).

#### ¿Qué es una fuga de memoria? ¿Cómo se detecta?

Memoria pedida que nunca se libera. Con `-fsanitize=address` (LeakSanitizer) o con `valgrind`.

#### ¿Por qué conviene poner el puntero en `NULL` después del `free`?

Para no usarlo por error (uso después de liberar) y porque `free(NULL)` no hace nada: un segundo `free` no rompe.

### Soluciones (docente)

Reescrita desde cero (la carpeta `02-C-Intermedio/17-MemoriaDinamica` tenía el formato viejo). Recomendar compilar las entregas con `-fsanitize=address` para ver fugas.

## R03-N02 · Un array que crece

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: troll
temas: col.listas
usa: mem.dinamica
```

### Crónica

En la galería de las Minas, los enemigos no paran de llegar: hoy dos, mañana cinco, pasado veinte. El estante de piedra donde Hulda los anota se llena todo el tiempo, y cada vez hay que cavar uno nuevo y mudar todo.

Tizón saca la libreta, hace cuentas en voz alta durante diez minutos y anuncia: —Conviene cavar uno **del doble** cada vez que se llena. —Por una vez, nadie le discute. Hulda le da una palmada que lo deja sin aire.

—No se cava una galería por cada enemigo —confirma {mentor}—. Cuando se llena, se agranda, y se muda todo de una sola vez.

### Objetivos

- Armar un **array dinámico**: un struct con `datos`, `cantidad` y `capacidad`.
- Agrandarlo duplicando la capacidad con `realloc`, sin perder los datos si falla.
- Escribir sus funciones: iniciar, agregar, quitar, mostrar y liberar.

### Antes de empezar

- Memoria dinámica (R03-N01).
- Arrays de structs (15) y punteros a structs (14).

### Explicación

#### Tres valores que van siempre juntos

```c
typedef struct {
    Enemigo *datos;     /* el bloque en el montón */
    int cantidad;       /* cuántos hay de verdad */
    int capacidad;      /* cuántos entran antes de tener que agrandar */
} Horda;
```

Es la misma idea de "capacidad y cantidad" del 10 y el 15, pero ahora la capacidad **cambia**.

#### Agregar: agrandar solo cuando hace falta

```c
bool horda_agregar(Horda *h, const char *nombre, int vida)
{
    if (h->cantidad == h->capacidad) {                       /* lleno */
        int nueva = h->capacidad == 0 ? 2 : h->capacidad * 2;
        Enemigo *tmp = realloc(h->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;                                    /* la horda sigue igual */
        }
        h->datos = tmp;
        h->capacidad = nueva;
    }
    h->datos[h->cantidad++] = ...;
    return true;
}
```

- **Duplicar** en lugar de sumar 1: con 1000 elementos, duplicar llama a `realloc` unas 10 veces; sumar 1, mil veces. Cada `realloc` puede copiar todo el bloque.
- `realloc(NULL, n)` funciona igual que `malloc(n)`: por eso la horda puede arrancar con `datos = NULL`.

#### Liberar y dejarlo usable

```c
void horda_liberar(Horda *h)
{
    free(h->datos);
    h->datos = NULL;
    h->cantidad = 0;
    h->capacidad = 0;
}
```

Después de liberar, la horda queda vacía y se puede volver a usar.

#### Cuidado con los punteros a elementos

Un puntero a `h->datos[3]` **deja de valer** cuando la horda crece: `realloc` pudo mover todo el bloque. Guardá la **posición** (el índice), no la dirección.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 18 - Un array que crece: datos + cantidad + capacidad.
 * Cuando se llena, se duplica la capacidad con realloc.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char nombre[16];
    int vida;
} Enemigo;

typedef struct {
    Enemigo *datos;
    int cantidad;
    int capacidad;
} Horda;

void horda_iniciar(Horda *h)
{
    h->datos = NULL;
    h->cantidad = 0;
    h->capacidad = 0;
}

bool horda_agregar(Horda *h, const char *nombre, int vida)
{
    if (h->cantidad == h->capacidad) {
        int nueva = h->capacidad == 0 ? 2 : h->capacidad * 2;
        Enemigo *tmp = realloc(h->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;                       /* la horda sigue como estaba */
        }
        h->datos = tmp;
        h->capacidad = nueva;
        printf("  (capacidad ampliada a %d)\n", nueva);
    }
    Enemigo *e = &h->datos[h->cantidad++];
    snprintf(e->nombre, sizeof(e->nombre), "%s", nombre);
    e->vida = vida;
    return true;
}

void horda_mostrar(const Horda *h)
{
    printf("Horda: %d de %d lugares\n", h->cantidad, h->capacidad);
    for (int i = 0; i < h->cantidad; i++) {
        printf("  %d. %-10s %3d\n", i, h->datos[i].nombre, h->datos[i].vida);
    }
}

void horda_liberar(Horda *h)
{
    free(h->datos);
    horda_iniciar(h);                          /* queda vacia y usable */
}

int main(void)
{
    Horda h;
    horda_iniciar(&h);
    const char *nombres[] = { "Slime", "Goblin", "Orco", "Esqueleto", "Troll" };
    for (int i = 0; i < 5; i++) {
        printf("Llega %s\n", nombres[i]);
        if (!horda_agregar(&h, nombres[i], 10 + i * 15)) {
            fprintf(stderr, "Sin memoria\n");
            break;
        }
    }
    horda_mostrar(&h);
    horda_liberar(&h);
    printf("Después de liberar: %d de %d\n", h.cantidad, h.capacidad);
    return 0;
}
```

### Salida esperada

```
Llega Slime
  (capacidad ampliada a 2)
Llega Goblin
Llega Orco
  (capacidad ampliada a 4)
Llega Esqueleto
Llega Troll
  (capacidad ampliada a 8)
Horda: 5 de 8 lugares
  0. Slime       10
  1. Goblin      25
  2. Orco        40
  3. Esqueleto   55
  4. Troll       70
Después de liberar: 0 de 0
```

### ¿Para qué sirve?

Es la estructura de datos más usada del mundo: el `list` de Python, el `ArrayList` de Java y el `std::vector` de C++ son exactamente esto, con la misma estrategia de duplicar. Sirve para cualquier colección que crece: los mensajes de un chat, las líneas de un archivo, las partículas de un efecto en un juego, los productos de un carrito de compras.

### Errores habituales

**Troll: el puntero viejo.** Guardar `Enemigo *jefe = &h->datos[0];`, agregar enemigos y usar `jefe`: si `realloc` movió el bloque, `jefe` apunta a memoria liberada.

**Ogro: olvidar actualizar la capacidad.** Agrandar el bloque sin cambiar `capacidad` (o al revés) hace que el próximo `agregar` escriba fuera.

**Orco: `cantidad` fuera de rango.** Quitar o leer con un índice sin revisar `0 <= i < cantidad`.

**Troll: `realloc` sin temporal.** Otra vez: si falla, se pierde todo.

**Ogro: liberar sin reiniciar.** Después del `free`, si `datos` sigue apuntando al bloque viejo y `cantidad` no vuelve a 0, el próximo uso es un uso después de liberar.

### Micro-misión R03-N02-P1 · Cavar del doble

```meta
lugar: Las Minas
personajes: Kira, Gheco, Tizón
carta: realloc | realloc(p, nuevo_tamaño) agranda y muda los datos · guardar en un auxiliar por si da NULL · duplicar la capacidad
recompensa: xp 10, oro 10
```

#### Escena
La galería donde Hulda anota a los enemigos se llena todo el tiempo. Tizón hace cuentas diez minutos y anuncia: —Conviene cavar una **del doble** cada vez. —Por una vez, nadie le discute.

#### Gheco sugiere
`int *nuevo = realloc(v, nueva_cap * sizeof *v);` pide un lugar más grande y muda los datos. Si da `NULL`, el viejo sigue sano: por eso se guarda primero en `nuevo`.

#### Desafío
Completá la nueva capacidad (el doble) y el `realloc`.

#### Código inicial
```c
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
            printf("galeria agrandada a %d\n", cap);
        }
        v[n++] = enemigo * 10;
    }
    printf("%d enemigos, capacidad %d\n", n, cap);
    free(v);
    return 0;
}
```

#### Salida esperada
```
galeria agrandada a 4
galeria agrandada a 8
5 enemigos, capacidad 8
```

#### Solución
```c
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
            printf("galeria agrandada a %d\n", cap);
        }
        v[n++] = enemigo * 10;
    }
    printf("%d enemigos, capacidad %d\n", n, cap);
    free(v);
    return 0;
}
```

#### Al superarla
De 2 a 4 y de 4 a 8: dos mudanzas en lugar de cuatro. Hulda le da a Tizón una palmada que lo deja sin aire.

#### Imagen
- Una galería de mina que se ensancha al doble, con mineros mudando cajas.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) le da una palmada en la espalda a Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello).

### Micro-misión R03-N02-P2 · La lista de la galería

```meta
lugar: Las Minas
personajes: Kira, Gheco, Hulda
carta: Agregar al final | si está lleno, agrandar · después v[n++] = valor · la función recibe punteros a v, n y cap
recompensa: xp 10, oro 10
```

#### Escena
Hulda quiere una función `agregar` que haga todo sola: si hay lugar, guarda; si no, agranda y guarda. Las cargas llegan hasta un 0.

#### Gheco sugiere
`agregar(&v, &n, &cap, valor)` recibe las **direcciones** porque las cambia. Adentro, `*n`, `*cap` y `*v` son las variables de afuera.

#### Desafío
Completá la línea que guarda el valor.

#### Código inicial
```c
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
    printf("\n");
    free(v);
    return 0;
}
```

#### Entrada
```
30 15 40 22 8 0
```

#### Salida esperada
```
5 cargas (capacidad 8): 30 15 40 22 8
```

#### Solución
```c
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
    printf("\n");
    free(v);
    return 0;
}
```

#### Al superarla
Cinco cargas en una galería de ocho. Hulda guarda la función en su tablilla, «para la próxima temporada».

#### Imagen
- Una tablilla de minera con una lista de cargas que se alarga sola.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) la mira satisfecha.

### Micro-misión R03-N02-P3 · Achicar al terminar

```meta
lugar: Las Minas
personajes: Kira, Gheco, Tizón
carta: Achicar | realloc también achica · al terminar de cargar, dejar la capacidad justa · no se pierde ningún dato
recompensa: xp 10, oro 10
```

#### Escena
Terminó el turno: la galería tiene lugar para 8 y hay 5 cargas. Tizón quiere devolver los 3 lugares que sobran, «para que el troll no se los coma».

#### Gheco sugiere
`realloc(v, n * sizeof *v)` con `n` menor que la capacidad **achica** el bloque y conserva los primeros `n` datos.

#### Desafío
Achicá el bloque a la cantidad justa.

#### Código inicial
```c
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
    printf("capacidad %d, ultimo dato %d\n", cap, v[n - 1]);
    free(v);
    return 0;
}
```

#### Salida esperada
```
capacidad 5, ultimo dato 35
```

#### Solución
```c
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
    printf("capacidad %d, ultimo dato %d\n", cap, v[n - 1]);
    free(v);
    return 0;
}
```

#### Al superarla
Capacidad 5, ni un lugar vacío. Tizón tapa los tres huecos de la galería con piedras y los mide, por las dudas.

#### Imagen
- Una galería que se achica, con piedras tapando el final.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) coloca la última piedra.

### Micro-misión R03-N02-P4 · Los enemigos con nombre

```meta
lugar: Las Minas
personajes: Kira, Gheco, Hulda
carta: Array dinámico de structs | Enemigo *v = malloc(cap * sizeof *v) · v[i].vida · se agranda igual que uno de int
recompensa: xp 15, oro 15
```

#### Escena
Hulda no quiere solo números: quiere cada enemigo con su nombre y su vida, y que la lista crezca sola. Llegan de a uno por línea hasta «fin».

#### Gheco sugiere
Un array dinámico de structs funciona igual: `realloc` con `sizeof *v`, que ahora es el tamaño de un `Enemigo`.

#### Desafío
Completá el `realloc` del array de structs.

#### Código inicial
```c
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
        printf("%-7s %3d\n", v[i].nombre, v[i].vida);
    }
    printf("capacidad final: %d\n", cap);
    free(v);
    return 0;
}
```

#### Entrada
```
goblin 12
orco 30
slime 5
fin
```

#### Salida esperada
```
goblin   12
orco     30
slime     5
capacidad final: 4
```

#### Solución
```c
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
        printf("%-7s %3d\n", v[i].nombre, v[i].vida);
    }
    printf("capacidad final: %d\n", cap);
    free(v);
    return 0;
}
```

#### Al superarla
Tres enemigos con nombre y vida. Hulda los clava en el tablero de la mina. El slime, ofendido por su vida de 5, se va a llorar a un rincón.

#### Imagen
- Un tablero de la mina con fichas de enemigos: goblin, orco, slime.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) clava la última ficha con el pico.
- Un slime llorando en un rincón.

### Misión R03-N02-M1 · Quitar de la horda

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Partiendo de la horda del ejemplo, escribí `bool horda_quitar(Horda *h, int indice)`: borra el enemigo de esa posición moviendo los de atrás un lugar hacia adelante, baja la `cantidad` y devuelve `false` si el índice no es válido.

Agregá cuatro enemigos (Slime 10, Goblin 25, Orco 40, Troll 70), quitá el de la posición 1 y probá quitar la posición 7. Mostrá la horda.

#### Criterio de aprobación

- Valida `0 <= indice < cantidad`.
- Corre los de atrás un lugar y baja la cantidad.
- No cambia la capacidad; libera al final.

#### Código inicial

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char nombre[16];
    int vida;
} Enemigo;

typedef struct {
    Enemigo *datos;
    int cantidad;
    int capacidad;
} Horda;

void horda_iniciar(Horda *h)
{
    h->datos = NULL;
    h->cantidad = 0;
    h->capacidad = 0;
}

bool horda_agregar(Horda *h, const char *nombre, int vida)
{
    if (h->cantidad == h->capacidad) {
        int nueva = h->capacidad == 0 ? 2 : h->capacidad * 2;
        Enemigo *tmp = realloc(h->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        h->datos = tmp;
        h->capacidad = nueva;
    }
    Enemigo *e = &h->datos[h->cantidad++];
    snprintf(e->nombre, sizeof(e->nombre), "%s", nombre);
    e->vida = vida;
    return true;
}

void horda_mostrar(const Horda *h)
{
    printf("Horda: %d de %d lugares\n", h->cantidad, h->capacidad);
    for (int i = 0; i < h->cantidad; i++) {
        printf("  %d. %-10s %3d\n", i, h->datos[i].nombre, h->datos[i].vida);
    }
}

void horda_liberar(Horda *h)
{
    free(h->datos);
    horda_iniciar(h);
}

int main(void)
{
    Horda h;
    horda_iniciar(&h);
    /* ... */
    horda_liberar(&h);
    return 0;
}
```

#### Salida esperada

```
quitar 1: sí
quitar 7: no
Horda: 3 de 4 lugares
  0. Slime       10
  1. Orco        40
  2. Troll       70
```

#### Solución de referencia

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char nombre[16];
    int vida;
} Enemigo;

typedef struct {
    Enemigo *datos;
    int cantidad;
    int capacidad;
} Horda;

void horda_iniciar(Horda *h)
{
    h->datos = NULL;
    h->cantidad = 0;
    h->capacidad = 0;
}

bool horda_agregar(Horda *h, const char *nombre, int vida)
{
    if (h->cantidad == h->capacidad) {
        int nueva = h->capacidad == 0 ? 2 : h->capacidad * 2;
        Enemigo *tmp = realloc(h->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        h->datos = tmp;
        h->capacidad = nueva;
    }
    Enemigo *e = &h->datos[h->cantidad++];
    snprintf(e->nombre, sizeof(e->nombre), "%s", nombre);
    e->vida = vida;
    return true;
}

void horda_mostrar(const Horda *h)
{
    printf("Horda: %d de %d lugares\n", h->cantidad, h->capacidad);
    for (int i = 0; i < h->cantidad; i++) {
        printf("  %d. %-10s %3d\n", i, h->datos[i].nombre, h->datos[i].vida);
    }
}

void horda_liberar(Horda *h)
{
    free(h->datos);
    horda_iniciar(h);
}

/* Mision 1 - Quitar un enemigo: los de atras se corren un lugar. */
bool horda_quitar(Horda *h, int indice)
{
    if (indice < 0 || indice >= h->cantidad) {
        return false;
    }
    for (int i = indice; i < h->cantidad - 1; i++) {
        h->datos[i] = h->datos[i + 1];
    }
    h->cantidad--;
    return true;
}

int main(void)
{
    Horda h;
    horda_iniciar(&h);
    horda_agregar(&h, "Slime", 10);
    horda_agregar(&h, "Goblin", 25);
    horda_agregar(&h, "Orco", 40);
    horda_agregar(&h, "Troll", 70);
    printf("quitar 1: %s\n", horda_quitar(&h, 1) ? "sí" : "no");
    printf("quitar 7: %s\n", horda_quitar(&h, 7) ? "sí" : "no");
    horda_mostrar(&h);
    horda_liberar(&h);
    return 0;
}
```

### Misión R03-N02-M2 · Duplicar o sumar 4

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `int llenar(int elementos, int duplicar, int mostrar)`: agrega `elementos` enteros a un array dinámico y cuenta cuántas veces tuvo que ampliar. Si `duplicar` es verdadero, la capacidad pasa a `capacidad * 2` (empezando en 2); si no, a `capacidad + 4`.

Si `mostrar` es verdadero, muestra la capacidad final y las ampliaciones. Probalo con 20 elementos con cada estrategia y después compará las ampliaciones para 1000. ¿Qué conviene?

#### Criterio de aprobación

- Cuenta las ampliaciones de cada estrategia.
- Muestra los resultados para 20 y para 1000 elementos.
- Libera la memoria en cada prueba.

#### Salida esperada

```
duplicar:  capacidad final 32, ampliaciones 5
sumar 4:   capacidad final 20, ampliaciones 5
Con 1000 elementos: duplicar 10, sumar 4 250
```

#### Solución de referencia

```c
/* Mision 2 - Duplicar o sumar 4: cuantas veces se llama a realloc para 20 elementos. */
#include <stdio.h>
#include <stdlib.h>

int llenar(int elementos, int duplicar, int mostrar)
{
    int *datos = NULL;
    int cantidad = 0, capacidad = 0, ampliaciones = 0;
    for (int i = 0; i < elementos; i++) {
        if (cantidad == capacidad) {
            int nueva = duplicar ? (capacidad == 0 ? 2 : capacidad * 2) : capacidad + 4;
            int *tmp = realloc(datos, nueva * sizeof *tmp);
            if (tmp == NULL) {
                free(datos);
                return -1;
            }
            datos = tmp;
            capacidad = nueva;
            ampliaciones++;
        }
        datos[cantidad++] = i;
    }
    if (mostrar) {
        printf("%-10s capacidad final %2d, ampliaciones %d\n", duplicar ? "duplicar:" : "sumar 4:", capacidad, ampliaciones);
    }
    free(datos);
    return ampliaciones;
}

int main(void)
{
    llenar(20, 1, 1);
    llenar(20, 0, 1);
    /* primero se calculan y despues se muestran: el orden de los argumentos de printf no esta definido */
    int con_duplicar = llenar(1000, 1, 0);
    int con_sumar = llenar(1000, 0, 0);
    printf("Con 1000 elementos: duplicar %d, sumar 4 %d\n", con_duplicar, con_sumar);
    return 0;
}
```

### Misión R03-N02-M3 · Encoger la horda

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `bool horda_encoger(Horda *h)`, que achica el bloque para que la capacidad sea igual a la cantidad (si está vacía, la libera). Agregá 5 goblins, mostrá la horda, encogela, mostrala y agregá un orco para ver que vuelve a crecer.

#### Criterio de aprobación

- Usa `realloc` con temporal para achicar.
- Trata aparte la horda vacía.
- La horda sigue funcionando después de encogerla.

#### Código inicial

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char nombre[16];
    int vida;
} Enemigo;

typedef struct {
    Enemigo *datos;
    int cantidad;
    int capacidad;
} Horda;

void horda_iniciar(Horda *h)
{
    h->datos = NULL;
    h->cantidad = 0;
    h->capacidad = 0;
}

bool horda_agregar(Horda *h, const char *nombre, int vida)
{
    if (h->cantidad == h->capacidad) {
        int nueva = h->capacidad == 0 ? 2 : h->capacidad * 2;
        Enemigo *tmp = realloc(h->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        h->datos = tmp;
        h->capacidad = nueva;
    }
    Enemigo *e = &h->datos[h->cantidad++];
    snprintf(e->nombre, sizeof(e->nombre), "%s", nombre);
    e->vida = vida;
    return true;
}

void horda_mostrar(const Horda *h)
{
    printf("Horda: %d de %d lugares\n", h->cantidad, h->capacidad);
    for (int i = 0; i < h->cantidad; i++) {
        printf("  %d. %-10s %3d\n", i, h->datos[i].nombre, h->datos[i].vida);
    }
}

void horda_liberar(Horda *h)
{
    free(h->datos);
    horda_iniciar(h);
}

int main(void)
{
    Horda h;
    horda_iniciar(&h);
    /* ... */
    horda_liberar(&h);
    return 0;
}
```

#### Salida esperada

```
Horda: 5 de 8 lugares
  0. Goblin      20
  1. Goblin      21
  2. Goblin      22
  3. Goblin      23
  4. Goblin      24
Horda: 5 de 5 lugares
  0. Goblin      20
  1. Goblin      21
  2. Goblin      22
  3. Goblin      23
  4. Goblin      24
Horda: 6 de 10 lugares
  0. Goblin      20
  1. Goblin      21
  2. Goblin      22
  3. Goblin      23
  4. Goblin      24
  5. Orco        50
```

#### Solución de referencia

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char nombre[16];
    int vida;
} Enemigo;

typedef struct {
    Enemigo *datos;
    int cantidad;
    int capacidad;
} Horda;

void horda_iniciar(Horda *h)
{
    h->datos = NULL;
    h->cantidad = 0;
    h->capacidad = 0;
}

bool horda_agregar(Horda *h, const char *nombre, int vida)
{
    if (h->cantidad == h->capacidad) {
        int nueva = h->capacidad == 0 ? 2 : h->capacidad * 2;
        Enemigo *tmp = realloc(h->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        h->datos = tmp;
        h->capacidad = nueva;
    }
    Enemigo *e = &h->datos[h->cantidad++];
    snprintf(e->nombre, sizeof(e->nombre), "%s", nombre);
    e->vida = vida;
    return true;
}

void horda_mostrar(const Horda *h)
{
    printf("Horda: %d de %d lugares\n", h->cantidad, h->capacidad);
    for (int i = 0; i < h->cantidad; i++) {
        printf("  %d. %-10s %3d\n", i, h->datos[i].nombre, h->datos[i].vida);
    }
}

void horda_liberar(Horda *h)
{
    free(h->datos);
    horda_iniciar(h);
}

/* Mision 3 - Encoger: que la capacidad sea exactamente la cantidad. */
bool horda_encoger(Horda *h)
{
    if (h->cantidad == h->capacidad) {
        return true;
    }
    if (h->cantidad == 0) {
        horda_liberar(h);
        return true;
    }
    Enemigo *tmp = realloc(h->datos, h->cantidad * sizeof *tmp);
    if (tmp == NULL) {
        return false;
    }
    h->datos = tmp;
    h->capacidad = h->cantidad;
    return true;
}

int main(void)
{
    Horda h;
    horda_iniciar(&h);
    for (int i = 0; i < 5; i++) {
        horda_agregar(&h, "Goblin", 20 + i);
    }
    horda_mostrar(&h);
    horda_encoger(&h);
    horda_mostrar(&h);
    horda_agregar(&h, "Orco", 50);
    horda_mostrar(&h);
    horda_liberar(&h);
    return 0;
}
```

### Encargo R03-N02-E1 · La lista de compras que crece

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La proveeduría del Gremio anota los pedidos de a uno por línea, sin saber cuántos van a ser. Leé líneas hasta que se termine la entrada (saltando las vacías) y guardá cada una en un **array dinámico de textos** (`char **`), donde cada texto tiene su propia memoria justa. Mostrá la lista numerada y liberá todo: primero cada texto y después el array.

#### Criterio de aprobación

- El array de punteros crece duplicando con `realloc`.
- Cada texto se copia con `strlen + 1` bytes.
- Libera cada texto y después el array.

#### Entrada de ejemplo

```
Harina 0000

Levadura
Aceite de oliva
Sal gruesa
Tomate triturado
```

#### Salida esperada

```
Lista de compras (5):
 1. Harina 0000
 2. Levadura
 3. Aceite de oliva
 4. Sal gruesa
 5. Tomate triturado
```

#### Solución de referencia

```c
/* Encargo - La lista de compras que crece: cada renglon es un texto con su propia memoria. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    char **items = NULL;
    int cantidad = 0, capacidad = 0;
    char linea[100];

    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        if (linea[0] == '\0') {
            continue;
        }
        if (cantidad == capacidad) {
            int nueva = capacidad == 0 ? 4 : capacidad * 2;
            char **tmp = realloc(items, nueva * sizeof *tmp);
            if (tmp == NULL) {
                break;
            }
            items = tmp;
            capacidad = nueva;
        }
        items[cantidad] = malloc(strlen(linea) + 1);
        if (items[cantidad] == NULL) {
            break;
        }
        strcpy(items[cantidad], linea);
        cantidad++;
    }

    printf("Lista de compras (%d):\n", cantidad);
    for (int i = 0; i < cantidad; i++) {
        printf("%2d. %s\n", i + 1, items[i]);
    }
    for (int i = 0; i < cantidad; i++) {   /* primero cada texto... */
        free(items[i]);
    }
    free(items);                           /* ...y despues el array de punteros */
    return 0;
}
```

#### Pruebas

##### Una sola línea
```entrada
Pan
```
```salida
Lista de compras (1):
 1. Pan
```

##### Solo líneas vacías
```entrada
```
```salida
Lista de compras (0):
```

##### Línea larga
```entrada
Queso rallado de campo estacionado doce meses
```
```salida
Lista de compras (1):
 1. Queso rallado de campo estacionado doce meses
```

### Prueba del sello

#### ¿Qué diferencia hay entre `cantidad` y `capacidad`?

La cantidad es cuántos elementos hay; la capacidad, cuántos entran en el bloque actual antes de tener que agrandarlo.

#### ¿Por qué se duplica la capacidad en lugar de sumar 1?

Para llamar pocas veces a `realloc`, que puede copiar todo el bloque: duplicando son unas pocas ampliaciones aunque haya miles de elementos.

#### ¿Por qué puede fallar un puntero a `h->datos[2]` guardado antes de agregar elementos?

Porque `realloc` pudo mover el bloque a otra dirección: el puntero viejo apunta a memoria liberada.

#### ¿Qué hace `realloc(NULL, n)`?

Lo mismo que `malloc(n)`.

#### En la lista de compras, ¿por qué hay que liberar cada texto antes que el array?

Porque las direcciones de los textos están guardadas en el array: si se libera primero el array, se pierden y quedan fugas.

### Soluciones (docente)

Reescrita desde cero a partir de `02-C-Intermedio/18-ArrayDinamico` (formato viejo).

## R03-N03 · Lista enlazada

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: troll
temas: alg.listas-enlazadas
usa: mem.dinamica
```

### Crónica

Más abajo, las galerías no están en fila: los **vagones** van enganchados uno detrás de otro con cadenas. Para agregar uno no hay que mudar nada: se engancha y listo.

Kira engancha los vagones a la velocidad del rayo, en cualquier orden, y el tren de la mina sale **marcha atrás** y con el vagón más pesado adelante. Hulda le explica, con mucha calma y bastante volumen, que se enganchan **ordenados por peso**. Y que si se suelta una cadena antes de agarrar la siguiente, todo lo de atrás se pierde en la oscuridad.

Al final de una vía muerta, iluminada por el farol, Kira encuentra una veta distinta, gris y brillante: **plomo**. En la roca, alguien grabó un vitral chiquito. El plomo del pedido salió de acá.

### Objetivos

- Armar una **lista enlazada**: nodos en el montón unidos por un puntero `siguiente`, terminada en `NULL`.
- Insertar al frente y al final, recorrer, buscar y quitar un nodo.
- Liberar toda la lista sin perder ningún nodo.
- Saber cuándo conviene una lista y cuándo un array dinámico.

### Antes de empezar

- Memoria dinámica (R03-N01) y el array que crece (R03-N02).
- Punteros a structs y la flecha `->` (14).

### Explicación

#### El nodo

```c
typedef struct Nodo {
    char item[20];
    struct Nodo *siguiente;     /* el próximo nodo, o NULL si es el último */
} Nodo;
```

Adentro del struct se escribe `struct Nodo *` y no `Nodo *` porque el `typedef` todavía no terminó. La lista entera se maneja con **un puntero al primer nodo**: la **cabeza**. Una lista vacía es `Nodo *cabeza = NULL;`.

#### Recorrer

```c
for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
    printf("%s\n", p->item);
}
```

#### Insertar al frente

```c
Nodo *n = nodo_nuevo(item);    /* malloc + copiar el item + siguiente = NULL */
n->siguiente = cabeza;         /* el nuevo apunta al que era primero */
return n;                      /* y pasa a ser la cabeza */
```

Como la cabeza cambia, la función **devuelve** la cabeza nueva y se usa así: `cabeza = insertar_frente(cabeza, "Espada");`.

#### Quitar

Para sacar un nodo hay que reconectar al **anterior** con el **siguiente**:

```
antes:   A -> B -> C          quitar B:   A -----> C     (y free(B))
```

Si el que se quita es la cabeza, no hay anterior: la cabeza nueva es `cabeza->siguiente`.

#### Liberar

```c
while (cabeza != NULL) {
    Nodo *siguiente = cabeza->siguiente;   /* guardarlo ANTES del free */
    free(cabeza);
    cabeza = siguiente;
}
```

Después del `free(cabeza)`, `cabeza->siguiente` ya no se puede leer: por eso se guarda antes.

#### Insertar ordenado
En lugar de ordenar al final, cada nodo se engancha **en su lugar** al
insertarlo, y la lista queda ordenada siempre. Hay dos casos:
1. va **primero** (la lista está vacía o es menor que la cabeza): se engancha
   adelante y pasa a ser la cabeza;
2. va **después** de alguno: se avanza mientras el **siguiente** sea menor, y se
   engancha entre ese nodo y su siguiente (si es el último, su siguiente es
   `NULL`, y el caso es el mismo).
```c
Nodo *insertar_ordenado(Nodo *cabeza, Nodo *n)
{
    if (cabeza == NULL || strcmp(n->item, cabeza->item) <= 0) {
        n->siguiente = cabeza;                 /* caso 1: va primero */
        return n;
    }
    Nodo *p = cabeza;
    while (p->siguiente != NULL && strcmp(p->siguiente->item, n->item) < 0) {
        p = p->siguiente;
    }
    n->siguiente = p->siguiente;               /* caso 2: entre p y su siguiente */
    p->siguiente = n;
    return cabeza;
}
```

#### Recorrer de ida y de vuelta
Una lista también se recorre con una función **recursiva**: mostrar el nodo y
llamarse con el siguiente. Si se muestra **después** de la llamada, la lista
sale **al revés**, sin ningún array extra:
```c
void mostrar_al_reves(const Nodo *p)
{
    if (p == NULL) return;          /* caso base: fin de la lista */
    mostrar_al_reves(p->siguiente);
    printf("%s\n", p->item);        /* se muestra a la vuelta */
}
```

#### Una lista sin `malloc`
En lenguajes (o placas) sin memoria dinámica, una lista se arma en un **array de
structs**: el «puntero» al siguiente es el **índice** del siguiente, y `-1` hace
de `NULL`. Los lugares libres se marcan (por ejemplo, con un campo `usado`). Es
lo mismo que hace el sistema operativo con la memoria, a mano.
```c
typedef struct { char item[20]; int siguiente; bool usado; } Casilla;
Casilla mina[10];
int cabeza = -1;                    /* lista vacía */
```

#### ¿Lista o array dinámico?

| | Array dinámico (18) | Lista enlazada |
|---|---|---|
| Acceder al elemento 500 | inmediato: `v[500]` | recorrer 500 nodos |
| Insertar o quitar al frente | mover todos | inmediato |
| Memoria | un bloque (a veces sobra capacidad) | un bloque por nodo, más el puntero |

En la práctica, el array dinámico se usa más; la lista brilla cuando se insertan y quitan elementos en cualquier lugar todo el tiempo (y es la base de colas, pilas y grafos).

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`
  - Con los detectores de memoria, solo en Linux: agregá `-g -fsanitize=address`. En Windows (MinGW) no existe: usá `-fsanitize=undefined`.

### Código de ejemplo

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Nodo {
    char item[20];
    struct Nodo *siguiente;
} Nodo;

Nodo *nodo_nuevo(const char *item)
{
    Nodo *n = malloc(sizeof *n);
    if (n != NULL) {
        snprintf(n->item, sizeof(n->item), "%s", item);
        n->siguiente = NULL;
    }
    return n;
}

/* Inserta al frente y devuelve la cabeza nueva. */
Nodo *insertar_frente(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    n->siguiente = cabeza;
    return n;
}

void mostrar(const Nodo *cabeza)
{
    printf("[");
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        printf("%s%s", p->item, p->siguiente ? " -> " : "");
    }
    printf("]\n");
}

void liberar(Nodo *cabeza)
{
    while (cabeza != NULL) {
        Nodo *siguiente = cabeza->siguiente;   /* guardarlo ANTES del free */
        free(cabeza);
        cabeza = siguiente;
    }
}

/* Inserta al final: hay que recorrer hasta el ultimo. */
Nodo *insertar_final(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    if (cabeza == NULL) {
        return n;
    }
    Nodo *p = cabeza;
    while (p->siguiente != NULL) {
        p = p->siguiente;
    }
    p->siguiente = n;
    return cabeza;
}

/* Quita el primer nodo con ese item. Devuelve la cabeza (puede cambiar). */
Nodo *quitar(Nodo *cabeza, const char *item)
{
    Nodo *anterior = NULL;
    for (Nodo *p = cabeza; p != NULL; anterior = p, p = p->siguiente) {
        if (strcmp(p->item, item) == 0) {
            if (anterior == NULL) {
                cabeza = p->siguiente;          /* era la cabeza */
            } else {
                anterior->siguiente = p->siguiente;
            }
            free(p);
            break;
        }
    }
    return cabeza;
}

int main(void)
{
    Nodo *mochila = NULL;                       /* lista vacia */
    mochila = insertar_frente(mochila, "Espada");
    mochila = insertar_frente(mochila, "Antorcha");
    mochila = insertar_final(mochila, "Llave");
    mochila = insertar_final(mochila, "Pocion");
    mostrar(mochila);

    mochila = quitar(mochila, "Llave");         /* del medio */
    mostrar(mochila);
    mochila = quitar(mochila, "Antorcha");      /* la cabeza */
    mostrar(mochila);
    mochila = quitar(mochila, "Dragon");        /* no esta: no pasa nada */
    mostrar(mochila);

    liberar(mochila);
    mochila = NULL;
    return 0;
}
```

### Salida esperada

```
[Antorcha -> Espada -> Llave -> Pocion]
[Antorcha -> Espada -> Pocion]
[Espada -> Pocion]
[Espada -> Pocion]
```

### ¿Para qué sirve?

Las listas enlazadas están por todos lados en los sistemas: el sistema operativo encadena los procesos que esperan turno, los navegadores guardan el historial de "atrás" y "adelante", los editores de texto encadenan las acciones de "deshacer", y las bibliotecas de juegos encadenan los objetos que hay que dibujar. Además, son la base de las colas (el primero que llega es el primero que sale) y de las pilas.

### Errores habituales

**Troll: soltar la cadena.** `free(p); p = p->siguiente;` lee un nodo ya liberado (`heap-use-after-free`). Guardá el siguiente antes.

**Orco: el `NULL` del final.** `p->siguiente->item` cuando `p` es el último nodo: `p->siguiente` es `NULL` y el programa se corta (`Segmentation fault`). Revisá antes de avanzar.

**Ogro: perder la cabeza.** Llamar a `insertar_frente(cabeza, ...)` sin guardar lo que devuelve: el nodo nuevo queda suelto (y es una fuga).

**Ogro: quitar la cabeza.** Olvidar el caso especial: si el nodo a quitar es el primero, no hay anterior que reconectar.

**Troll: la fuga de la lista.** Liberar solo la cabeza (`free(cabeza)`) deja todos los demás nodos perdidos.

### Micro-misión R03-N03-P1 · Enganchar adelante

```meta
lugar: Las vías de la mina
personajes: Kira, Gheco, Hulda
carta: Insertar al frente | el nuevo apunta a la cabeza · el nuevo pasa a ser la cabeza · la función devuelve la cabeza nueva
recompensa: xp 10, oro 10
```

#### Escena
Más abajo, los vagones van enganchados con cadenas. Para agregar uno no hay que mudar nada: se engancha adelante y listo. Hulda le muestra a Kira el primer enganche.

#### Gheco sugiere
Insertar al frente: `n->siguiente = cabeza;` y la cabeza pasa a ser `n`. La función devuelve la cabeza nueva: `cabeza = insertar(cabeza, …);`.

#### Desafío
Completá el enganche.

#### Código inicial
```c
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
    printf("\n");
    while (tren != NULL) {
        Vagon *sig = tren->siguiente;
        free(tren);
        tren = sig;
    }
    return 0;
}
```

#### Salida esperada
```
[450][120][300]
```

#### Solución
```c
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
    printf("\n");
    while (tren != NULL) {
        Vagon *sig = tren->siguiente;
        free(tren);
        tren = sig;
    }
    return 0;
}
```

#### Al superarla
Tres vagones enganchados, el último que llegó adelante. El tren sale marcha atrás. Hulda dice que para eso está la próxima lección.

#### Imagen
- Un tren de mina de tres vagones unidos por cadenas que brillan.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) ajusta un enganche.

### Micro-misión R03-N03-P2 · Engancharlos ordenados

```meta
lugar: Las vías de la mina
personajes: Kira, Gheco, Hulda
carta: Inserción ordenada | si va primero, se engancha adelante · si no, avanzar mientras el siguiente sea menor · enganchar entre p y su siguiente
recompensa: xp 15, oro 15
```

#### Escena
Kira enganchó los vagones en cualquier orden y el tren salió con el más pesado adelante. Hulda le explica, con mucha calma y bastante volumen, que se enganchan **ordenados por peso**.

#### Gheco sugiere
Si la lista está vacía o el nuevo es menor que la cabeza, va primero. Si no, se avanza con `p` mientras `p->siguiente` exista y sea menor, y se engancha entre `p` y su siguiente.

#### Desafío
Completá la condición del avance y el enganche del medio.

#### Código inicial
```c
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
    printf("\n");
    while (tren != NULL) {
        Vagon *sig = tren->siguiente;
        free(tren);
        tren = sig;
    }
    return 0;
}
```

#### Entrada
```
300 120 450 200 80
```

#### Salida esperada
```
[80][120][200][300][450]
```

#### Solución
```c
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
    printf("\n");
    while (tren != NULL) {
        Vagon *sig = tren->siguiente;
        free(tren);
        tren = sig;
    }
    return 0;
}
```

#### Al superarla
Del más liviano al más pesado. El tren sale derecho, sin chirriar. Hulda baja el volumen.

#### Imagen
- Un tren de mina ordenado de vagones chicos a grandes.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) asiente con los brazos cruzados.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) suelta el último enganche.

### Micro-misión R03-N03-P3 · Soltar sin perder

```meta
lugar: Las vías de la mina
personajes: Kira, Gheco, Tizón
criatura: troll
carta: Quitar un nodo | buscar el ANTERIOR · anterior->siguiente = a_quitar->siguiente · después free · si es la cabeza, la cabeza cambia
recompensa: xp 15, oro 15
```

#### Escena
Hay que desenganchar el vagón de 200 kg del medio del tren sin perder los de atrás. —Si soltás la cadena antes de agarrar la siguiente —advierte Tizón—, todo lo de atrás se pierde en la oscuridad.

#### Gheco sugiere
Para quitar, se busca el nodo **anterior** al que sale y se lo une con el que sigue: `ant->siguiente = sale->siguiente;` y recién ahí `free(sale)`.

#### Desafío
Completá la unión y la liberación.

#### Código inicial
```c
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
    printf("\n");
    while (tren != NULL) {
        Vagon *sig = tren->siguiente;
        free(tren);
        tren = sig;
    }
    return 0;
}
```

#### Salida esperada
```
[120][450]
```

#### Solución
```c
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
    printf("\n");
    while (tren != NULL) {
        Vagon *sig = tren->siguiente;
        free(tren);
        tren = sig;
    }
    return 0;
}
```

#### Al superarla
El vagón del medio sale y el tren sigue entero. Tizón respira de nuevo: había contenido el aire todo el tiempo.

#### Imagen
- Un vagón que se desengancha del medio de un tren mientras los otros dos se unen.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) aguanta la respiración con las mejillas infladas.

### Micro-misión R03-N03-P4 · La veta del plomo

```meta
lugar: La vía muerta
personajes: Kira, Gheco, Hulda
carta: Recorrer de vuelta | una función recursiva que se llama con el siguiente · si muestra DESPUÉS de llamarse, la lista sale al revés
recompensa: xp 15, oro 15
```

#### Escena
Al final de una vía muerta hay un tren viejo, abandonado. Hulda quiere leer sus vagones **desde el último**, que es el más cercano a la pared de roca.

#### Gheco sugiere
`al_reves(p)`: si `p` es `NULL`, termina; si no, se llama con `p->siguiente` y **después** muestra `p`. Así se muestra a la vuelta, del último al primero.

#### Desafío
Completá la llamada recursiva.

#### Código inicial
```c
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
    printf("%s\n", p->contenido);
}

int main(void)
{
    Vagon c = { "plomo con un vitral grabado", NULL };
    Vagon b = { "carbon", &c };
    Vagon a = { "piedras", &b };
    al_reves(&a);
    return 0;
}
```

#### Salida esperada
```
plomo con un vitral grabado
carbon
piedras
```

#### Solución
```c
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
    printf("%s\n", p->contenido);
}

int main(void)
{
    Vagon c = { "plomo con un vitral grabado", NULL };
    Vagon b = { "carbon", &c };
    Vagon a = { "piedras", &b };
    al_reves(&a);
    return 0;
}
```

#### Al superarla
El último vagón está lleno de **plomo**, gris y brillante, y en la roca de atrás alguien grabó un vitral chiquito. El plomo del pedido salió de acá. Hulda se saca el casco, despacio.

#### Imagen
- Una vía muerta que termina en una pared de roca con una veta de plomo brillante y un vitral chiquito grabado.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) se saca el casco, sorprendida.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) ilumina la veta con el farol.

### Misión R03-N03-M1 · Contar y buscar

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `int contar(const Nodo *cabeza)` y `bool contiene(const Nodo *cabeza, const char *item)`. Probalas con la lista vacía y con una mochila de tres objetos, buscando uno que está y otro que no.

#### Criterio de aprobación

- Recorre con un puntero hasta `NULL`, sin modificar la lista (`const`).
- Funciona con la lista vacía.
- Libera la lista al final.

#### Código inicial

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Nodo {
    char item[20];
    struct Nodo *siguiente;
} Nodo;

Nodo *nodo_nuevo(const char *item)
{
    Nodo *n = malloc(sizeof *n);
    if (n != NULL) {
        snprintf(n->item, sizeof(n->item), "%s", item);
        n->siguiente = NULL;
    }
    return n;
}

/* Inserta al frente y devuelve la cabeza nueva. */
Nodo *insertar_frente(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    n->siguiente = cabeza;
    return n;
}

void mostrar(const Nodo *cabeza)
{
    printf("[");
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        printf("%s%s", p->item, p->siguiente ? " -> " : "");
    }
    printf("]\n");
}

void liberar(Nodo *cabeza)
{
    while (cabeza != NULL) {
        Nodo *siguiente = cabeza->siguiente;   /* guardarlo ANTES del free */
        free(cabeza);
        cabeza = siguiente;
    }
}

int main(void)
{
    Nodo *mochila = NULL;
    mochila = insertar_frente(mochila, "Pocion");
    mochila = insertar_frente(mochila, "Llave");
    mochila = insertar_frente(mochila, "Espada");
    /* ... */
    liberar(mochila);
    return 0;
}
```

#### Salida esperada

```
vacía: 0 elementos
[Espada -> Llave -> Pocion]
elementos: 3
¿tiene Llave? sí
¿tiene Mapa? no
```

#### Solución de referencia

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Nodo {
    char item[20];
    struct Nodo *siguiente;
} Nodo;

Nodo *nodo_nuevo(const char *item)
{
    Nodo *n = malloc(sizeof *n);
    if (n != NULL) {
        snprintf(n->item, sizeof(n->item), "%s", item);
        n->siguiente = NULL;
    }
    return n;
}

/* Inserta al frente y devuelve la cabeza nueva. */
Nodo *insertar_frente(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    n->siguiente = cabeza;
    return n;
}

void mostrar(const Nodo *cabeza)
{
    printf("[");
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        printf("%s%s", p->item, p->siguiente ? " -> " : "");
    }
    printf("]\n");
}

void liberar(Nodo *cabeza)
{
    while (cabeza != NULL) {
        Nodo *siguiente = cabeza->siguiente;   /* guardarlo ANTES del free */
        free(cabeza);
        cabeza = siguiente;
    }
}

/* Mision 1 - Contar y buscar. */
int contar(const Nodo *cabeza)
{
    int n = 0;
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        n++;
    }
    return n;
}

bool contiene(const Nodo *cabeza, const char *item)
{
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        if (strcmp(p->item, item) == 0) {
            return true;
        }
    }
    return false;
}

int main(void)
{
    Nodo *mochila = NULL;
    printf("vacía: %d elementos\n", contar(mochila));
    mochila = insertar_frente(mochila, "Pocion");
    mochila = insertar_frente(mochila, "Llave");
    mochila = insertar_frente(mochila, "Espada");
    mostrar(mochila);
    printf("elementos: %d\n", contar(mochila));
    printf("¿tiene Llave? %s\n", contiene(mochila, "Llave") ? "sí" : "no");
    printf("¿tiene Mapa? %s\n", contiene(mochila, "Mapa") ? "sí" : "no");
    liberar(mochila);
    return 0;
}
```

### Misión R03-N03-M2 · Dar vuelta la cadena

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `Nodo *invertir(Nodo *cabeza)`, que da vuelta la lista **sin crear nodos nuevos**: solo reacomoda los punteros `siguiente` y devuelve la cabeza nueva. Probala con cuatro objetos y con la lista vacía.

#### Criterio de aprobación

- No usa `malloc`: reacomoda los punteros con tres variables (anterior, actual, siguiente).
- Devuelve la cabeza nueva.
- Funciona con la lista vacía.

#### Código inicial

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Nodo {
    char item[20];
    struct Nodo *siguiente;
} Nodo;

Nodo *nodo_nuevo(const char *item)
{
    Nodo *n = malloc(sizeof *n);
    if (n != NULL) {
        snprintf(n->item, sizeof(n->item), "%s", item);
        n->siguiente = NULL;
    }
    return n;
}

/* Inserta al frente y devuelve la cabeza nueva. */
Nodo *insertar_frente(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    n->siguiente = cabeza;
    return n;
}

void mostrar(const Nodo *cabeza)
{
    printf("[");
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        printf("%s%s", p->item, p->siguiente ? " -> " : "");
    }
    printf("]\n");
}

void liberar(Nodo *cabeza)
{
    while (cabeza != NULL) {
        Nodo *siguiente = cabeza->siguiente;   /* guardarlo ANTES del free */
        free(cabeza);
        cabeza = siguiente;
    }
}

int main(void)
{
    Nodo *mochila = NULL;
    mochila = insertar_frente(mochila, "Pocion");
    mochila = insertar_frente(mochila, "Llave");
    mochila = insertar_frente(mochila, "Espada");
    /* ... */
    liberar(mochila);
    return 0;
}
```

#### Salida esperada

```
[Antorcha -> Espada -> Llave -> Pocion]
[Pocion -> Llave -> Espada -> Antorcha]
[]
```

#### Solución de referencia

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Nodo {
    char item[20];
    struct Nodo *siguiente;
} Nodo;

Nodo *nodo_nuevo(const char *item)
{
    Nodo *n = malloc(sizeof *n);
    if (n != NULL) {
        snprintf(n->item, sizeof(n->item), "%s", item);
        n->siguiente = NULL;
    }
    return n;
}

/* Inserta al frente y devuelve la cabeza nueva. */
Nodo *insertar_frente(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    n->siguiente = cabeza;
    return n;
}

void mostrar(const Nodo *cabeza)
{
    printf("[");
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        printf("%s%s", p->item, p->siguiente ? " -> " : "");
    }
    printf("]\n");
}

void liberar(Nodo *cabeza)
{
    while (cabeza != NULL) {
        Nodo *siguiente = cabeza->siguiente;   /* guardarlo ANTES del free */
        free(cabeza);
        cabeza = siguiente;
    }
}

/* Mision 2 - Dar vuelta la lista reacomodando punteros, sin crear nodos. */
Nodo *invertir(Nodo *cabeza)
{
    Nodo *anterior = NULL;
    while (cabeza != NULL) {
        Nodo *siguiente = cabeza->siguiente;
        cabeza->siguiente = anterior;
        anterior = cabeza;
        cabeza = siguiente;
    }
    return anterior;
}

int main(void)
{
    Nodo *mochila = NULL;
    const char *cosas[] = { "Pocion", "Llave", "Espada", "Antorcha" };
    for (int i = 0; i < 4; i++) {
        mochila = insertar_frente(mochila, cosas[i]);
    }
    mostrar(mochila);
    mochila = invertir(mochila);
    mostrar(mochila);
    mostrar(invertir(NULL));
    liberar(mochila);
    return 0;
}
```

### Misión R03-N03-M3 · El inventario en orden

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `Nodo *insertar_ordenado(Nodo *cabeza, const char *item)`, que inserta cada objeto en su lugar alfabético. Leé objetos (uno por línea, hasta que se termine la entrada), insertalos y mostrá la lista después de cada uno.

#### Criterio de aprobación

- Inserta al frente cuando corresponde (antes de la cabeza o lista vacía).
- Si no, busca el nodo después del cual va.
- La lista queda ordenada siempre; se libera al final.

#### Código inicial

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Nodo {
    char item[20];
    struct Nodo *siguiente;
} Nodo;

Nodo *nodo_nuevo(const char *item)
{
    Nodo *n = malloc(sizeof *n);
    if (n != NULL) {
        snprintf(n->item, sizeof(n->item), "%s", item);
        n->siguiente = NULL;
    }
    return n;
}

/* Inserta al frente y devuelve la cabeza nueva. */
Nodo *insertar_frente(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    n->siguiente = cabeza;
    return n;
}

void mostrar(const Nodo *cabeza)
{
    printf("[");
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        printf("%s%s", p->item, p->siguiente ? " -> " : "");
    }
    printf("]\n");
}

void liberar(Nodo *cabeza)
{
    while (cabeza != NULL) {
        Nodo *siguiente = cabeza->siguiente;   /* guardarlo ANTES del free */
        free(cabeza);
        cabeza = siguiente;
    }
}

int main(void)
{
    Nodo *mochila = NULL;
    mochila = insertar_frente(mochila, "Pocion");
    mochila = insertar_frente(mochila, "Llave");
    mochila = insertar_frente(mochila, "Espada");
    /* ... */
    liberar(mochila);
    return 0;
}
```

#### Entrada de ejemplo

```
Pocion
Arco
Llave
Zafiro
Espada
```

#### Salida esperada

```
[Pocion]
[Arco -> Pocion]
[Arco -> Llave -> Pocion]
[Arco -> Llave -> Pocion -> Zafiro]
[Arco -> Espada -> Llave -> Pocion -> Zafiro]
```

#### Solución de referencia

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Nodo {
    char item[20];
    struct Nodo *siguiente;
} Nodo;

Nodo *nodo_nuevo(const char *item)
{
    Nodo *n = malloc(sizeof *n);
    if (n != NULL) {
        snprintf(n->item, sizeof(n->item), "%s", item);
        n->siguiente = NULL;
    }
    return n;
}

/* Inserta al frente y devuelve la cabeza nueva. */
Nodo *insertar_frente(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    n->siguiente = cabeza;
    return n;
}

void mostrar(const Nodo *cabeza)
{
    printf("[");
    for (const Nodo *p = cabeza; p != NULL; p = p->siguiente) {
        printf("%s%s", p->item, p->siguiente ? " -> " : "");
    }
    printf("]\n");
}

void liberar(Nodo *cabeza)
{
    while (cabeza != NULL) {
        Nodo *siguiente = cabeza->siguiente;   /* guardarlo ANTES del free */
        free(cabeza);
        cabeza = siguiente;
    }
}

/* Mision 3 - Insertar en orden alfabetico. */
Nodo *insertar_ordenado(Nodo *cabeza, const char *item)
{
    Nodo *n = nodo_nuevo(item);
    if (n == NULL) {
        return cabeza;
    }
    if (cabeza == NULL || strcmp(item, cabeza->item) < 0) {
        n->siguiente = cabeza;
        return n;
    }
    Nodo *p = cabeza;
    while (p->siguiente != NULL && strcmp(p->siguiente->item, item) <= 0) {
        p = p->siguiente;
    }
    n->siguiente = p->siguiente;
    p->siguiente = n;
    return cabeza;
}

int main(void)
{
    Nodo *lista = NULL;
    char linea[40];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        if (linea[0] != '\0') {
            lista = insertar_ordenado(lista, linea);
            mostrar(lista);
        }
    }
    liberar(lista);
    return 0;
}
```

#### Pruebas

##### Ya ordenados
```entrada
A
B
C
```
```salida
[A]
[A -> B]
[A -> B -> C]
```

##### Al revés
```entrada
Z
M
A
```
```salida
[Z]
[M -> Z]
[A -> M -> Z]
```

##### Repetidos
```entrada
Llave
Llave
```
```salida
[Llave]
[Llave -> Llave]
```

### Encargo R03-N03-E1 · La fila del correo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El correo del Gremio atiende por orden de llegada: una **cola**. Implementala con una lista enlazada que guarda punteros al **primero** y al **último** (así agregar al final es inmediato). Procesá órdenes `llega Nombre` y `atender`, mostrando qué pasa y cuántos quedan. Al terminar la entrada, el correo cierra y los que quedan vuelven mañana (liberá todo).

#### Criterio de aprobación

- Encola al final en tiempo constante (puntero al último).
- Atiende desde el principio y avisa si la fila está vacía.
- Actualiza el último cuando la fila queda vacía.
- Libera todos los nodos.

#### Entrada de ejemplo

```
llega Ana
llega Beto
atender
llega Caro
atender
atender
atender
llega Dani
llega Eli
```

#### Salida esperada

```
Llega Ana (1 en la fila)
Llega Beto (2 en la fila)
Se atiende a Ana (1 en la fila)
Llega Caro (2 en la fila)
Se atiende a Beto (1 en la fila)
Se atiende a Caro (0 en la fila)
No hay nadie en la fila
Llega Dani (1 en la fila)
Llega Eli (2 en la fila)
Cierra el correo: Dani vuelve mañana
Cierra el correo: Eli vuelve mañana
```

#### Solución de referencia

```c
/* Encargo - La fila del correo: una cola con cabeza y cola (el primero en llegar es el primero en salir). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Cliente {
    char nombre[30];
    struct Cliente *siguiente;
} Cliente;

typedef struct {
    Cliente *primero;
    Cliente *ultimo;
    int cantidad;
} Fila;

void encolar(Fila *f, const char *nombre)
{
    Cliente *c = malloc(sizeof *c);
    if (c == NULL) {
        return;
    }
    snprintf(c->nombre, sizeof(c->nombre), "%s", nombre);
    c->siguiente = NULL;
    if (f->ultimo == NULL) {
        f->primero = c;
    } else {
        f->ultimo->siguiente = c;
    }
    f->ultimo = c;
    f->cantidad++;
}

/* Copia el nombre del que sale en `nombre` y lo saca de la fila. */
int atender(Fila *f, char *nombre, size_t tam)
{
    if (f->primero == NULL) {
        return 0;
    }
    Cliente *c = f->primero;
    snprintf(nombre, tam, "%s", c->nombre);
    f->primero = c->siguiente;
    if (f->primero == NULL) {
        f->ultimo = NULL;
    }
    free(c);
    f->cantidad--;
    return 1;
}

int main(void)
{
    Fila fila = { NULL, NULL, 0 };
    char linea[60];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        char nombre[30];
        if (strncmp(linea, "llega ", 6) == 0) {
            encolar(&fila, linea + 6);
            printf("Llega %s (%d en la fila)\n", linea + 6, fila.cantidad);
        } else if (strcmp(linea, "atender") == 0) {
            if (atender(&fila, nombre, sizeof(nombre))) {
                printf("Se atiende a %s (%d en la fila)\n", nombre, fila.cantidad);
            } else {
                printf("No hay nadie en la fila\n");
            }
        }
    }
    char nombre[30];
    while (atender(&fila, nombre, sizeof(nombre))) {
        printf("Cierra el correo: %s vuelve mañana\n", nombre);
    }
    return 0;
}
```

#### Pruebas

##### Atender sin nadie
```entrada
atender
atender
```
```salida
No hay nadie en la fila
No hay nadie en la fila
```

##### Nadie queda
```entrada
llega Ana
atender
```
```salida
Llega Ana (1 en la fila)
Se atiende a Ana (0 en la fila)
```


### Prueba del sello

#### ¿Qué representa `NULL` en una lista enlazada?

El final de la lista (el `siguiente` del último nodo) o, en la cabeza, una lista vacía.

#### ¿Por qué `insertar_frente` devuelve un `Nodo *`?

Porque la cabeza cambia: el nodo nuevo pasa a ser el primero y quien llama tiene que guardarlo.

#### Para quitar un nodo del medio, ¿qué puntero hay que cambiar?

El `siguiente` del nodo **anterior**, que pasa a apuntar al que venía después del quitado.

#### ¿Qué pasa si en `liberar` hacés `free(p)` y después `p = p->siguiente`?

Leés memoria ya liberada: comportamiento indefinido. Hay que guardar el siguiente antes del `free`.

#### ¿Cuándo conviene una lista enlazada en lugar de un array dinámico?

Cuando se insertan y quitan elementos todo el tiempo al principio o en el medio, y no hace falta acceder por posición.

### Soluciones (docente)

Reescrita desde cero a partir de `02-C-Intermedio/19-ListaEnlazada` (formato viejo). Las misiones 1 a 3 parten del mismo código inicial.

## R03-N04 · Pilas y colas

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: troll
temas: col.pilas-colas
usa: alg.listas-enlazadas, mem.dinamica
```

### Crónica

En las Minas hay dos máquinas que Hulda cuida como a sus hijas.

El **montacargas**: las bolsas se apilan una encima de otra y, arriba, la última que se subió es la **primera que baja**. Tizón subió su almuerzo primero, abajo de todo, y se queda sin comer hasta la noche. —Es una **pila** —le explica Hulda sin una gota de compasión—. Último en entrar, primero en salir.

La **fila de las vagonetas**: la primera que llega a la boca de la mina es la **primera que sale**. Chispa intenta meter su vagoneta adelante de todas, sonriendo con el diente de oro. Hulda ni lo mira: —Es una **cola**, mercader. Al fondo.

Kira, que siempre quiere pasar primero, se pone al fondo sin que nadie se lo diga. Ferrum, que la vio desde lejos, golpea el yunque dos veces.

### Objetivos

- Entender una **pila** (el último que entra es el primero que sale) y una **cola** (el primero que entra es el primero que sale).
- Implementarlas **con un array** y **con nodos enlazados**, guardando structs.
- Controlar los dos errores clásicos: sacar de una vacía y meter en una llena.
- Reconocer dónde se usan: deshacer, paréntesis balanceados, turnos y pedidos.

### Antes de empezar

- Lista enlazada (R03-N03): una pila con nodos es insertar y quitar **al frente**.
- Arrays de structs (R02-N06).

### Explicación

#### La pila (LIFO)
Una **pila** (*stack*) solo deja tocar el **tope**:
- **apilar** (*push*): poner arriba;
- **desapilar** (*pop*): sacar el de arriba;
- **ver el tope** sin sacarlo, y saber si está **vacía**.

Con un **array**, alcanza con el array y un contador que dice cuántos hay:
```c
#define MAX 10
typedef struct {
    Bolsa datos[MAX];
    int cantidad;               /* el tope es datos[cantidad - 1] */
} Pila;

bool apilar(Pila *p, Bolsa b)
{
    if (p->cantidad == MAX) return false;     /* llena: overflow */
    p->datos[p->cantidad++] = b;
    return true;
}

bool desapilar(Pila *p, Bolsa *sale)
{
    if (p->cantidad == 0) return false;       /* vacía: underflow */
    *sale = p->datos[--p->cantidad];
    return true;
}
```
Las funciones reciben la pila **por puntero** (`Pila *p`) porque la modifican, y
devuelven `bool` para avisar si pudieron. Lo que sale se entrega por un puntero
(`Bolsa *sale`).

Con **nodos**, apilar es insertar al frente de una lista, y desapilar es quitar
el primero: no hay límite de tamaño (solo la memoria).

#### La cola (FIFO)
Una **cola** (*queue*) se llena por el **fondo** y se vacía por el **frente**:
- **encolar**: agregar al fondo;
- **desencolar**: sacar el del frente.

Con **nodos**, se guardan **dos** punteros, al frente y al fondo, para no
recorrer toda la lista en cada encolar:
```c
typedef struct {
    NodoV *frente;          /* de acá sale */
    NodoV *fondo;           /* acá se engancha el que llega */
} Cola;

void encolar(Cola *c, NodoV *n)
{
    n->siguiente = NULL;
    if (c->fondo == NULL) c->frente = n;      /* estaba vacía: es el único */
    else c->fondo->siguiente = n;
    c->fondo = n;
}
```
Al desencolar el último, **también** el fondo vuelve a `NULL`: es el error más
común de las colas.

Con un **array**, la cola es **circular**: el frente avanza y, al llegar al
final del array, vuelve al principio con `%`:
```c
int pos = (c->frente + c->cantidad) % MAX;    /* dónde entra el próximo */
c->frente = (c->frente + 1) % MAX;            /* después de sacar uno */
```
Así no hace falta correr todos los elementos cada vez que sale uno.

#### ¿Pila o cola?
| Problema | Estructura | Por qué |
|---|---|---|
| deshacer (Ctrl+Z) | pila | lo último que hiciste es lo primero que se deshace |
| revisar que `( [ { } ] )` cierre bien | pila | el último que abrió es el primero que tiene que cerrar |
| turnos, pedidos, impresora | cola | se atiende por orden de llegada |
| recorrer un laberinto a lo ancho | cola | primero lo más cercano |

#### Cómo compilarlo y ejecutarlo
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **VS Code** o la terminal:
  - Linux: `gcc -Wall -Wextra -g main.c -o programa` y `./programa`; con
    `-fsanitize=address` se ven las fugas y los punteros perdidos.
  - Windows (MSYS2): `gcc -Wall -Wextra -g main.c -o programa.exe` y
    `programa.exe`. El sanitizador de direcciones no está en MinGW: usá
    `-fsanitize=undefined` o, para las fugas, contá cada `malloc` con su `free`.
- Con entrada desde un archivo: `./programa < entrada.txt` (Linux) o
  `programa.exe < entrada.txt` (Windows, en la terminal).

### Código de ejemplo

```c
/*
 * R03-N04 - Pilas y colas: el montacargas (una pila con array de structs) y
 * la fila de vagonetas (una cola con nodos enlazados, con frente y fondo).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX 4

/* ---------- La pila: el montacargas ---------- */
typedef struct {
    char duenio[12];
    int kilos;
} Bolsa;

typedef struct {
    Bolsa datos[MAX];
    int cantidad;
} Pila;

bool apilar(Pila *p, const char *duenio, int kilos)
{
    if (p->cantidad == MAX) {
        return false;                           /* llena */
    }
    Bolsa *b = &p->datos[p->cantidad++];
    strcpy(b->duenio, duenio);
    b->kilos = kilos;
    return true;
}

bool desapilar(Pila *p, Bolsa *sale)
{
    if (p->cantidad == 0) {
        return false;                           /* vacia */
    }
    *sale = p->datos[--p->cantidad];
    return true;
}

/* ---------- La cola: la fila de vagonetas ---------- */
typedef struct NodoV {
    int numero;
    int carga;
    struct NodoV *siguiente;
} NodoV;

typedef struct {
    NodoV *frente;
    NodoV *fondo;
} Cola;

void encolar(Cola *c, int numero, int carga)
{
    NodoV *n = malloc(sizeof *n);
    if (n == NULL) {
        exit(1);
    }
    n->numero = numero;
    n->carga = carga;
    n->siguiente = NULL;
    if (c->fondo == NULL) {
        c->frente = n;                          /* estaba vacia */
    } else {
        c->fondo->siguiente = n;
    }
    c->fondo = n;
}

bool desencolar(Cola *c, int *numero, int *carga)
{
    if (c->frente == NULL) {
        return false;
    }
    NodoV *sale = c->frente;
    *numero = sale->numero;
    *carga = sale->carga;
    c->frente = sale->siguiente;
    if (c->frente == NULL) {
        c->fondo = NULL;                        /* se vacio: el fondo tambien */
    }
    free(sale);
    return true;
}

int main(void)
{
    Pila montacargas = { .cantidad = 0 };
    const char *duenios[] = { "Tizon", "Kira", "Hulda", "Chispa", "Ferrum" };
    int kilos[] = { 3, 12, 20, 7, 30 };

    printf("== El montacargas (pila) ==\n");
    for (int i = 0; i < 5; i++) {
        if (apilar(&montacargas, duenios[i], kilos[i])) {
            printf("sube la bolsa de %s (%d kg)\n", duenios[i], kilos[i]);
        } else {
            printf("no entra la bolsa de %s: el montacargas esta lleno\n", duenios[i]);
        }
    }
    Bolsa b;
    while (desapilar(&montacargas, &b)) {
        printf("baja la bolsa de %s\n", b.duenio);
    }
    printf("el almuerzo de Tizon bajo ultimo\n");

    printf("\n== La fila de vagonetas (cola) ==\n");
    Cola fila = { NULL, NULL };
    encolar(&fila, 1, 300);
    encolar(&fila, 2, 120);
    encolar(&fila, 3, 450);
    int numero, carga;
    while (desencolar(&fila, &numero, &carga)) {
        printf("sale la vagoneta %d con %d kg\n", numero, carga);
    }
    printf("fila vacia: frente %s, fondo %s\n",
           fila.frente == NULL ? "NULL" : "ocupado", fila.fondo == NULL ? "NULL" : "ocupado");
    return 0;
}
```

### Salida esperada

```
== El montacargas (pila) ==
sube la bolsa de Tizon (3 kg)
sube la bolsa de Kira (12 kg)
sube la bolsa de Hulda (20 kg)
sube la bolsa de Chispa (7 kg)
no entra la bolsa de Ferrum: el montacargas esta lleno
baja la bolsa de Chispa
baja la bolsa de Hulda
baja la bolsa de Kira
baja la bolsa de Tizon
el almuerzo de Tizon bajo ultimo

== La fila de vagonetas (cola) ==
sale la vagoneta 1 con 300 kg
sale la vagoneta 2 con 120 kg
sale la vagoneta 3 con 450 kg
fila vacia: frente NULL, fondo NULL
```

### ¿Para qué sirve?

Las pilas están adentro de todo programa: cada vez que se llama a una función, se apila (la **pila de llamadas** que muestra el sanitizador). También son el «deshacer» de cualquier editor y la forma de revisar que un código abra y cierre bien sus llaves. Las colas ordenan todo lo que se atiende por turno: los pedidos de un servidor, las impresiones, los mensajes. En C++ ya vienen hechas (`std::stack`, `std::queue`); en C se escriben a mano, y los parciales lo piden.

### Errores habituales

**Troll: desapilar de una pila vacía.** Con `p->datos[--p->cantidad]` y la pila
vacía, se lee `datos[-1]`: memoria ajena. Siempre preguntar antes si está
vacía (y devolver `false`).

**Orco: apilar en una pila llena.** Con array, `datos[MAX]` ya está fuera del
array. Con `-fsanitize=address` (Linux):
```
==ERROR: AddressSanitizer: stack-buffer-overflow on address ...
WRITE of size 4 ...
```

**Troll: la cola que se vació y el fondo que sigue apuntando.** Si al sacar el
último no se pone `fondo = NULL`, el próximo `encolar` engancha el nodo nuevo
a uno que ya se liberó.

**Ogro: confundir el orden.** Si la consigna dice «por orden de llegada», es una
cola; si dice «el último primero», una pila. Probá con tres elementos en papel
antes de programar.

**Troll: no liberar.** Al terminar, hay que desencolar (o desapilar) todo lo que
quede para hacer el `free` de cada nodo.

### Micro-misión R03-N04-P1 · El almuerzo de Tizón

```meta
lugar: El montacargas
personajes: Kira, Gheco, Tizón, Hulda
carta: Pila | apilar arriba, desapilar de arriba · el último que entra es el primero que sale · con array: datos y cantidad
recompensa: xp 10, oro 10
```

#### Escena
En el montacargas, las bolsas se apilan una encima de otra. Tizón subió su almuerzo **primero**, abajo de todo. Hulda descarga desde arriba, sin una gota de compasión.

#### Gheco sugiere
Una pila con array: `apilar` guarda en `datos[cantidad++]` y `desapilar` saca `datos[--cantidad]`. Sale primero lo último que entró.

#### Desafío
Completá apilar y desapilar.

#### Código inicial
```c
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
    printf("baja la bolsa %d\n", desapilar(&montacargas));
    printf("baja la bolsa %d\n", desapilar(&montacargas));
    printf("baja la bolsa %d (el almuerzo de Tizon)\n", desapilar(&montacargas));
    return 0;
}
```

#### Salida esperada
```
baja la bolsa 3
baja la bolsa 2
baja la bolsa 1 (el almuerzo de Tizon)
```

#### Solución
```c
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
    printf("baja la bolsa %d\n", desapilar(&montacargas));
    printf("baja la bolsa %d\n", desapilar(&montacargas));
    printf("baja la bolsa %d (el almuerzo de Tizon)\n", desapilar(&montacargas));
    return 0;
}
```

#### Al superarla
El almuerzo de Tizón baja último, frío. —Es una pila —le dice Hulda—. Último en entrar, primero en salir. —Tizón come en silencio, apuntando algo en la libreta.

#### Imagen
- Un montacargas de mina con bolsas apiladas.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) mira su almuerzo frío.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) descarga una bolsa.

### Micro-misión R03-N04-P2 · Al fondo, mercader

```meta
lugar: La fila de vagonetas
personajes: Kira, Gheco, Chispa, Hulda
carta: Cola | se encola al fondo, se desencola del frente · el primero que llega es el primero que sale · con nodos: punteros al frente y al fondo
recompensa: xp 10, oro 10
```

#### Escena
Chispa intenta meter su vagoneta adelante de todas, sonriendo con el diente de oro. Hulda ni lo mira: —Es una **cola**, mercader. Al fondo.

#### Gheco sugiere
Al encolar con nodos: si la cola está vacía, el nuevo es el frente; si no, se engancha detrás del fondo (`fondo->siguiente = n`). En los dos casos, el nuevo pasa a ser el fondo.

#### Desafío
Completá el enganche al fondo.

#### Código inicial
```c
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
        printf("sale %s\n", p->duenio);
    }
    return 0;
}
```

#### Salida esperada
```
sale Kira
sale Tizon
sale Chispa
```

#### Solución
```c
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
        printf("sale %s\n", p->duenio);
    }
    return 0;
}
```

#### Al superarla
Kira, Tizón y, al final, Chispa. Kira, que siempre quiere pasar primero, se puso al fondo sin que nadie se lo dijera. Ferrum, desde lejos, golpea el yunque dos veces.

#### Imagen
- Una fila de vagonetas en la boca de la mina.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) empuja su vagoneta al final de la fila, resignado.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) con el pico al hombro.

### Micro-misión R03-N04-P3 · Las llaves que cierran

```meta
lugar: El Archivo de planos
personajes: Kira, Gheco, Chispa
carta: Pila de char | cada apertura se apila · cada cierre tiene que coincidir con el tope · al final, la pila vacía
recompensa: xp 15, oro 15
```

#### Escena
El Archivero desconfía de los planos de Chispa: dice que nunca cierra lo que abre. Kira revisa cada plano con una pila.

#### Gheco sugiere
Con una pila de `char`: `(` y `[` se apilan; `)` exige que el tope sea `(` y `]` que sea `[`. Si no coincide o al final queda algo, no cierra.

#### Desafío
Completá el carácter de apertura que espera cada cierre.

#### Código inicial
```c
#include <stdio.h>
#include <string.h>

int cierra(const char *s)
{
    char pila[50];
    int n = 0;
    for (int i = 0; s[i] != '\0'; i++) {
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
        linea[strcspn(linea, "\n")] = '\0';
        printf("%-8s %s\n", linea, cierra(linea) ? "cierra" : "no cierra");
    }
    return 0;
}
```

#### Entrada
```
([()])
([)]
((
```

#### Salida esperada
```
([()])   cierra
([)]     no cierra
((       no cierra
```

#### Solución
```c
#include <stdio.h>
#include <string.h>

int cierra(const char *s)
{
    char pila[50];
    int n = 0;
    for (int i = 0; s[i] != '\0'; i++) {
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
        linea[strcspn(linea, "\n")] = '\0';
        printf("%-8s %s\n", linea, cierra(linea) ? "cierra" : "no cierra");
    }
    return 0;
}
```

#### Al superarla
Uno cierra, dos no. El Archivero devuelve los dos planos de Chispa con una nota: «Cierre lo que abre». Chispa guarda la nota en un bolsillo y se olvida para siempre.

#### Imagen
- Tres planos con paréntesis y corchetes; dos tienen marcas rojas.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) recibe los planos devueltos con una nota.

### Micro-misión R03-N04-P4 · La cola que da la vuelta

```meta
lugar: El horno grande
personajes: Kira, Gheco, Tizón
carta: Cola circular | posición = (frente + cantidad) % MAX · al sacar, frente = (frente + 1) % MAX · se aprovechan los lugares que se liberan
recompensa: xp 15, oro 15
```

#### Escena
El horno grande tiene lugar para 3 piezas esperando, en un riel que da la vuelta. Tizón no entiende cómo la pieza nueva va a parar al lugar 0 si ya pasó por ahí.

#### Gheco sugiere
En una cola circular con array, el próximo lugar es `(frente + cantidad) % MAX`: al pasarse del final, el `%` lo vuelve al principio.

#### Desafío
Completá la posición donde entra cada pieza.

#### Código inicial
```c
#include <stdio.h>

#define MAX 3

int main(void)
{
    int riel[MAX];
    int frente = 0, cantidad = 0;
    int piezas[5] = { 10, 11, 12, 13, 14 };
    for (int i = 0; i < 5; i++) {
        if (cantidad == MAX) {
            printf("sale la pieza %d del lugar %d\n", riel[frente], frente);
            frente = (frente + 1) % MAX;
            cantidad--;
        }
        int pos = ___;
        riel[pos] = piezas[i];
        cantidad++;
        printf("entra la pieza %d en el lugar %d\n", piezas[i], pos);
    }
    return 0;
}
```

#### Salida esperada
```
entra la pieza 10 en el lugar 0
entra la pieza 11 en el lugar 1
entra la pieza 12 en el lugar 2
sale la pieza 10 del lugar 0
entra la pieza 13 en el lugar 0
sale la pieza 11 del lugar 1
entra la pieza 14 en el lugar 1
```

#### Solución
```c
#include <stdio.h>

#define MAX 3

int main(void)
{
    int riel[MAX];
    int frente = 0, cantidad = 0;
    int piezas[5] = { 10, 11, 12, 13, 14 };
    for (int i = 0; i < 5; i++) {
        if (cantidad == MAX) {
            printf("sale la pieza %d del lugar %d\n", riel[frente], frente);
            frente = (frente + 1) % MAX;
            cantidad--;
        }
        int pos = (frente + cantidad) % MAX;
        riel[pos] = piezas[i];
        cantidad++;
        printf("entra la pieza %d en el lugar %d\n", piezas[i], pos);
    }
    return 0;
}
```

#### Al superarla
Las piezas 13 y 14 vuelven a los lugares 0 y 1. Tizón dibuja el riel en la libreta como un reloj y por fin lo entiende. Lo dibuja diez veces más, por gusto.

#### Imagen
- Un riel circular frente a un horno, con tres lugares numerados 0, 1 y 2.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) dibuja un reloj en la libreta.

### Misión R03-N04-M1 · El montacargas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Implementá una **pila con array** de hasta 3 `Bolsa` (dueño y kilos) con
`apilar`, `desapilar`, `tope` y `vacia`. Apilá las bolsas de Kira (12 kg),
Hulda (20 kg), Chispa (7 kg) y Ferrum (30 kg) —la última no entra—, mostrá el
tope, desapilá todo mostrando cada una y, al final, intentá desapilar una vez
más con la pila vacía.

#### Criterio de aprobación

- La pila es un struct con el array y la cantidad; las funciones la reciben por puntero.
- `apilar` avisa cuando está llena y `desapilar` cuando está vacía, sin salirse del array.
- Las bolsas bajan en el orden inverso al que subieron.

#### Salida esperada

```
apilada: Kira (12 kg)
apilada: Hulda (20 kg)
apilada: Chispa (7 kg)
llena: no entra la de Ferrum
arriba de todo: Chispa
baja: Chispa (7 kg)
baja: Hulda (20 kg)
baja: Kira (12 kg)
vacia: no hay nada para bajar
```

#### Solución de referencia

```c
/*
 * Mision 1 - El montacargas: una pila con array de structs.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX 3

typedef struct {
    char duenio[12];
    int kilos;
} Bolsa;

typedef struct {
    Bolsa datos[MAX];
    int cantidad;
} Pila;

bool vacia(const Pila *p)
{
    return p->cantidad == 0;
}

bool apilar(Pila *p, const char *duenio, int kilos)
{
    if (p->cantidad == MAX) {
        return false;
    }
    strcpy(p->datos[p->cantidad].duenio, duenio);
    p->datos[p->cantidad].kilos = kilos;
    p->cantidad++;
    return true;
}

bool desapilar(Pila *p, Bolsa *sale)
{
    if (vacia(p)) {
        return false;
    }
    p->cantidad--;
    *sale = p->datos[p->cantidad];
    return true;
}

const Bolsa *tope(const Pila *p)
{
    return vacia(p) ? NULL : &p->datos[p->cantidad - 1];
}

int main(void)
{
    Pila p = { .cantidad = 0 };
    const char *duenios[] = { "Kira", "Hulda", "Chispa", "Ferrum" };
    int kilos[] = { 12, 20, 7, 30 };
    for (int i = 0; i < 4; i++) {
        if (apilar(&p, duenios[i], kilos[i])) {
            printf("apilada: %s (%d kg)\n", duenios[i], kilos[i]);
        } else {
            printf("llena: no entra la de %s\n", duenios[i]);
        }
    }
    printf("arriba de todo: %s\n", tope(&p)->duenio);

    Bolsa b;
    while (desapilar(&p, &b)) {
        printf("baja: %s (%d kg)\n", b.duenio, b.kilos);
    }
    if (!desapilar(&p, &b)) {
        printf("vacia: no hay nada para bajar\n");
    }
    return 0;
}
```

### Misión R03-N04-M2 · Las llaves que cierran

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El Archivero desconfía de los planos de Chispa: dice que nunca cierra lo que
abre. Leé líneas hasta el final de la entrada y, para cada una, decí si sus
`( )`, `[ ]` y `{ }` están **balanceados**, usando una **pila de char**: cada
apertura se apila; cada cierre tiene que coincidir con el tope.

#### Criterio de aprobación

- Usa una pila de `char` (con array) para las aperturas.
- Un cierre que no coincide con el tope, o una pila con algo al final, es «no cierra».
- Ignora los demás caracteres y muestra el resultado de cada línea.

#### Entrada de ejemplo

```
int v[3] = { 1, 2, (3) };
if (a[0] > 2) { b = (c + d]; }
{ [ ( ) ] }
((((
```

#### Salida esperada

```
línea 1: cierra
línea 2: no cierra
línea 3: cierra
línea 4: no cierra
```

#### Solución de referencia

```c
/*
 * Mision 2 - Las llaves que cierran: una pila de char revisa que cada
 * apertura cierre en el orden correcto.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX 100

bool balanceada(const char *linea)
{
    char pila[MAX];
    int cantidad = 0;
    for (int i = 0; linea[i] != '\0'; i++) {
        char c = linea[i];
        if (c == '(' || c == '[' || c == '{') {
            if (cantidad == MAX) {
                return false;
            }
            pila[cantidad++] = c;
        } else if (c == ')' || c == ']' || c == '}') {
            char espera = c == ')' ? '(' : c == ']' ? '[' : '{';
            if (cantidad == 0 || pila[cantidad - 1] != espera) {
                return false;
            }
            cantidad--;
        }
    }
    return cantidad == 0;
}

int main(void)
{
    char linea[200];
    int n = 0;
    while (fgets(linea, sizeof linea, stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        n++;
        printf("línea %d: %s\n", n, balanceada(linea) ? "cierra" : "no cierra");
    }
    return 0;
}
```

#### Pruebas

##### Sin llaves
```entrada
sin llaves ni nada
x = 3 + 4;
```
```salida
línea 1: cierra
línea 2: cierra
```

##### Cierra de más
```entrada
())
[)
```
```salida
línea 1: no cierra
línea 2: no cierra
```

### Misión R03-N04-M3 · La fila de vagonetas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Implementá una **cola con nodos** (frente y fondo) de vagonetas (número y
carga). Leé órdenes, una por línea: `llega N KG` encola, `sale` desencola y
muestra cuál salió (o «no hay vagonetas»), `fin` termina. Al terminar, mostrá
cuántas quedaron en la fila y liberalas.

#### Criterio de aprobación

- La cola tiene punteros al frente y al fondo; encolar no recorre la lista.
- Al sacar la última, el fondo también vuelve a `NULL`.
- Salen por orden de llegada y al final se liberan todos los nodos.

#### Entrada de ejemplo

```
llega 1 300
llega 2 120
sale
llega 3 450
sale
sale
sale
llega 4 80
fin
```

#### Salida esperada

```
llega la vagoneta 1 (300 kg)
llega la vagoneta 2 (120 kg)
sale la vagoneta 1 con 300 kg
llega la vagoneta 3 (450 kg)
sale la vagoneta 2 con 120 kg
sale la vagoneta 3 con 450 kg
no hay vagonetas
llega la vagoneta 4 (80 kg)
quedan 1 en la fila
```

#### Solución de referencia

```c
/*
 * Mision 3 - La fila de vagonetas: una cola con nodos, frente y fondo.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct NodoV {
    int numero;
    int carga;
    struct NodoV *siguiente;
} NodoV;

typedef struct {
    NodoV *frente;
    NodoV *fondo;
    int cantidad;
} Cola;

void encolar(Cola *c, int numero, int carga)
{
    NodoV *n = malloc(sizeof *n);
    if (n == NULL) {
        exit(1);
    }
    n->numero = numero;
    n->carga = carga;
    n->siguiente = NULL;
    if (c->fondo == NULL) {
        c->frente = n;
    } else {
        c->fondo->siguiente = n;
    }
    c->fondo = n;
    c->cantidad++;
}

bool desencolar(Cola *c, NodoV *sale)
{
    if (c->frente == NULL) {
        return false;
    }
    NodoV *primero = c->frente;
    *sale = *primero;
    c->frente = primero->siguiente;
    if (c->frente == NULL) {
        c->fondo = NULL;
    }
    free(primero);
    c->cantidad--;
    return true;
}

int main(void)
{
    Cola fila = { NULL, NULL, 0 };
    char orden[10];
    while (scanf("%9s", orden) == 1) {
        if (orden[0] == 'f') {
            break;
        } else if (orden[0] == 'l') {
            int numero, carga;
            if (scanf("%d %d", &numero, &carga) == 2) {
                encolar(&fila, numero, carga);
                printf("llega la vagoneta %d (%d kg)\n", numero, carga);
            }
        } else {
            NodoV v;
            if (desencolar(&fila, &v)) {
                printf("sale la vagoneta %d con %d kg\n", v.numero, v.carga);
            } else {
                printf("no hay vagonetas\n");
            }
        }
    }
    printf("quedan %d en la fila\n", fila.cantidad);
    NodoV v;
    while (desencolar(&fila, &v)) {
        /* libera cada nodo al sacarlo */
    }
    return 0;
}
```

### Encargo R03-N04-E1 · La cola circular del horno

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El horno grande tiene lugar para **4 piezas** esperando. Implementá una **cola
circular con array** (frente, cantidad y `% MAX`) de piezas (código y
temperatura) con `encolar` y `desencolar`. Simulá: entran las piezas 10, 11, 12
y 13; la 14 no entra; salen dos; entran la 14 y la 15 (dan la vuelta al
array); salen todas. Mostrá en cada paso en qué posición del array quedó cada
pieza.

#### Criterio de aprobación

- La cola usa un array de structs con `frente` y `cantidad`, y avanza con `% MAX`.
- Avisa cuando está llena o vacía, sin salirse del array.
- Muestra que las piezas 14 y 15 ocupan las posiciones 0 y 1 al dar la vuelta.

#### Salida esperada

```
entra la pieza 10 en la posición 0
entra la pieza 11 en la posición 1
entra la pieza 12 en la posición 2
entra la pieza 13 en la posición 3
lleno: la pieza 14 espera afuera
sale la pieza 10 de la posición 0 (800 grados)
sale la pieza 11 de la posición 1 (850 grados)
entra la pieza 14 en la posición 0
entra la pieza 15 en la posición 1
sale la pieza 12 de la posición 2 (900 grados)
sale la pieza 13 de la posición 3 (950 grados)
sale la pieza 14 de la posición 0 (1000 grados)
sale la pieza 15 de la posición 1 (1050 grados)
horno vacío
```

#### Solución de referencia

```c
/*
 * Encargo - La cola circular del horno: una cola con array que da la vuelta
 * con % MAX, sin correr los elementos.
 */
#include <stdio.h>
#include <stdbool.h>

#define MAX 4

typedef struct {
    int codigo;
    int grados;
} Pieza;

typedef struct {
    Pieza datos[MAX];
    int frente;
    int cantidad;
} Cola;

bool encolar(Cola *c, Pieza p)
{
    if (c->cantidad == MAX) {
        printf("lleno: la pieza %d espera afuera\n", p.codigo);
        return false;
    }
    int pos = (c->frente + c->cantidad) % MAX;
    c->datos[pos] = p;
    c->cantidad++;
    printf("entra la pieza %d en la posición %d\n", p.codigo, pos);
    return true;
}

bool desencolar(Cola *c, Pieza *sale)
{
    if (c->cantidad == 0) {
        return false;
    }
    *sale = c->datos[c->frente];
    printf("sale la pieza %d de la posición %d (%d grados)\n", sale->codigo, c->frente, sale->grados);
    c->frente = (c->frente + 1) % MAX;
    c->cantidad--;
    return true;
}

int main(void)
{
    Cola horno = { .frente = 0, .cantidad = 0 };
    Pieza sale;
    for (int codigo = 10; codigo <= 14; codigo++) {
        encolar(&horno, (Pieza){ codigo, 800 + (codigo - 10) * 50 });
    }
    desencolar(&horno, &sale);
    desencolar(&horno, &sale);
    encolar(&horno, (Pieza){ 14, 1000 });
    encolar(&horno, (Pieza){ 15, 1050 });
    while (desencolar(&horno, &sale)) {
        /* sale todo */
    }
    printf("horno vacío\n");
    return 0;
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre una pila y una cola?

En la pila sale primero el **último** que entró (LIFO); en la cola sale primero el **primero** que entró (FIFO).

#### Si apilás 1, 2 y 3 y desapilás dos veces, ¿qué queda? ¿Y si fuera una cola?

En la pila queda el 1 (salieron 3 y 2). En la cola queda el 3 (salieron 1 y 2).

#### ¿Por qué `apilar` y `desapilar` reciben la pila por puntero?

Porque la modifican: con una copia, el cambio se perdería al volver.

#### ¿Para qué guarda la cola enlazada un puntero al fondo?

Para encolar sin recorrer toda la lista hasta el último nodo.

#### ¿Qué hay que hacer con el fondo cuando se saca el último elemento?

Ponerlo en `NULL`: si sigue apuntando al nodo liberado, el próximo `encolar` lo usa.

#### ¿Para qué sirve el `% MAX` en la cola circular?

Para que, al llegar al final del array, la posición vuelva a 0 y se aprovechen los lugares que dejaron libres los que salieron.

### Soluciones (docente)

Nodo nuevo (2026-10-08): los parciales de la UNLaR y la UTN piden listas, pilas y colas con estructuras. Del apunte de Programación I (Camargo), «Listas» (pp. 63–70), en C estándar.

## R03-N05 · Punteros a función

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: esqueleto
temas: mem.punteros-funcion, func.orden-superior
```

### Crónica

En el taller de las Minas hay un tablero con **palancas**. Cada palanca no hace nada por sí misma: señala a una máquina (la bomba de agua, el montacargas, el fuelle). Se cambia a qué máquina apunta y la misma palanca hace otra cosa.

Chispa, aprovechando un descuido, instala una palanca nueva que manda **todos** los trenes a su puesto de ventas. Tizón la encuentra en cinco minutos (Chispa la había etiquetado «NO TOCAR, NO ES DE CHISPA»).

—Así se escriben los hechizos que eligen **qué hacer** mientras el programa corre —dice {mentor}—. El autómata que ordenaba el cuadro de honor funcionaba así: vos le dabas la palanca.

### Objetivos

- Declarar y usar **punteros a función**, con y sin `typedef`.
- Pasar una función como parámetro (*callback*), como hace `qsort`.
- Armar **tablas de acciones**: un array de structs con un nombre y una función.

### Antes de empezar

- Funciones (08), punteros (13) y arrays de structs con `qsort` (15).

### Explicación

#### Una función también tiene dirección

Así como una variable está en algún lugar de la memoria, el código de una función también. Un **puntero a función** guarda esa dirección y permite llamarla:

```c
int doble(int x) { return x * 2; }

int (*f)(int) = doble;     /* f apunta a una función que recibe int y devuelve int */
printf("%d\n", f(21));     /* 42: se llama como a la función */
```

- El nombre de la función **sin paréntesis** es su dirección: `doble`, no `doble()`.
- Los paréntesis de `(*f)` son obligatorios: `int *f(int)` sería una función que devuelve un puntero.

#### `typedef`: ponerle nombre al tipo

La sintaxis es difícil de leer; con `typedef` queda clara:

```c
typedef int (*Transformacion)(int);

void aplicar(int *v, int n, Transformacion f)
{
    for (int i = 0; i < n; i++) {
        v[i] = f(v[i]);
    }
}

aplicar(vidas, n, doble);  /* la misma función aplica lo que le pasen */
```

Esto se llama **callback**: le pasás a una función *qué hacer* y ella decide *cuándo*. Es exactamente lo que hace `qsort` con la función de comparación (15).

#### Tablas de acciones

Un array de structs con un nombre y una función reemplaza a un `if`/`else` larguísimo:

```c
typedef struct {
    const char *nombre;
    Transformacion accion;
} Hechizo;

Hechizo libro[] = { { "fuerza", doble }, { "debilidad", mitad } };

for (size_t i = 0; i < 2; i++) {
    if (strcmp(libro[i].nombre, pedido) == 0) {
        aplicar(vidas, n, libro[i].accion);
    }
}
```

Agregar un hechizo nuevo es agregar **una línea** a la tabla.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 20 - Punteros a funcion: guardar "que hacer" en una variable.
 */
#include <stdio.h>
#include <string.h>

typedef int (*Transformacion)(int);    /* una funcion que recibe un int y devuelve un int */

int doble(int x) { return x * 2; }
int mitad(int x) { return x / 2; }
int curar(int x) { return x + 10; }

/* Aplica la funcion que le pasen a cada elemento. */
void aplicar(int *v, int n, Transformacion f)
{
    for (int i = 0; i < n; i++) {
        v[i] = f(v[i]);
    }
}

void mostrar(const char *titulo, const int *v, int n)
{
    printf("%-10s", titulo);
    for (int i = 0; i < n; i++) {
        printf(" %3d", v[i]);
    }
    printf("\n");
}

/* Una tabla de acciones: nombre + funcion. */
typedef struct {
    const char *nombre;
    Transformacion accion;
} Hechizo;

int main(void)
{
    int vidas[] = { 30, 12, 45, 8 };
    int n = sizeof(vidas) / sizeof(vidas[0]);
    mostrar("inicio", vidas, n);

    Transformacion f = doble;          /* sin parentesis: la funcion, no su resultado */
    aplicar(vidas, n, f);
    mostrar("doble", vidas, n);
    aplicar(vidas, n, mitad);
    mostrar("mitad", vidas, n);

    Hechizo libro[] = {
        { "fuerza", doble },
        { "debilidad", mitad },
        { "curacion", curar },
    };
    const char *pedido = "curacion";
    for (size_t i = 0; i < sizeof(libro) / sizeof(libro[0]); i++) {
        if (strcmp(libro[i].nombre, pedido) == 0) {
            aplicar(vidas, n, libro[i].accion);
            mostrar(pedido, vidas, n);
        }
    }
    return 0;
}
```

### Salida esperada

```
inicio      30  12  45   8
doble       60  24  90  16
mitad       30  12  45   8
curacion    40  22  55  18
```

### ¿Para qué sirve?

Los punteros a función son la forma de C de tener "comportamiento intercambiable": `qsort` y `bsearch` los usan para comparar, las bibliotecas gráficas (SDL, GTK) para avisarte de un clic o una tecla, los intérpretes de comandos para mapear cada orden a su función, y los sistemas embebidos para las interrupciones (qué hacer cuando se aprieta un botón). Los objetos de C++ y las funciones de Python que se pasan como parámetro son la misma idea.

### Errores habituales

**Esqueleto: llamar en lugar de pasar.** `aplicar(v, n, doble(3))` pasa el **resultado** (un `int`), no la función. El compilador avisa:

```
warning: passing argument 3 of 'aplicar' makes pointer from integer without a cast
```

**Goblin: firmas que no coinciden.** Pasar una función `double f(double)` donde se espera `int (*)(int)`:

```
warning: passing argument 3 of 'aplicar' from incompatible pointer type
```

Nunca se "arregla" con un cast: la función tiene que tener la firma exacta.

**Orco: puntero a función `NULL`.** Buscar en la tabla, no encontrar nada y llamar igual: el programa se corta. Revisá antes de llamar.

**Ogro: restar `double` en un comparador.** `return a->peso - b->peso;` convierte a `int` y `0.5` pasa a ser `0`: el orden sale mal. Se usa `(a > b) - (a < b)`.

### Micro-misión R03-N05-P1 · La palanca que señala

```meta
lugar: El tablero de palancas
personajes: Kira, Gheco, Hulda
carta: Puntero a función | int (*accion)(int) = doble; · se llama accion(5) · cambia la función a la que apunta y cambia lo que hace
recompensa: xp 10, oro 10
```

#### Escena
En el taller de las Minas hay un tablero de palancas. Cada palanca no hace nada sola: **señala** una máquina. Cambiando adónde señala, la misma palanca hace otra cosa.

#### Gheco sugiere
`int (*palanca)(int) = bomba;` guarda la función `bomba`. `palanca(10)` la llama. Después, `palanca = fuelle;` y la misma línea hace otra cosa.

#### Desafío
Hacé que la palanca señale primero a `bomba` y después a `fuelle`.

#### Código inicial
```c
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
    printf("la palanca da %d\n", palanca(10));
    palanca = ___;
    printf("la palanca da %d\n", palanca(10));
    return 0;
}
```

#### Salida esperada
```
la palanca da 20
la palanca da 110
```

#### Solución
```c
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
    printf("la palanca da %d\n", palanca(10));
    palanca = fuelle;
    printf("la palanca da %d\n", palanca(10));
    return 0;
}
```

#### Al superarla
Veinte litros de agua, y después ciento diez grados. Hulda deja la palanca en «bomba»: la mina se estaba inundando un poquito.

#### Imagen
- Un tablero de palancas de hierro, cada una unida por un cable a una máquina distinta.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) mueve una palanca.

### Micro-misión R03-N05-P2 · La palanca de Chispa

```meta
lugar: El tablero de palancas
personajes: Kira, Gheco, Chispa, Tizón
carta: Tabla de funciones | un array de punteros a función · la opción elige el índice · menos if, más orden
recompensa: xp 15, oro 15
```

#### Escena
Chispa instaló una palanca nueva que manda **todos** los trenes a su puesto de ventas. Tizón la encontró en cinco minutos: estaba etiquetada «NO TOCAR, NO ES DE CHISPA». Kira arma un tablero honesto.

#### Gheco sugiere
Un array de punteros a función: `Destino destinos[3] = { a_la_forja, a_la_mina, al_archivo };` y se llama `destinos[opcion](tren)`.

#### Desafío
Completá la llamada con la tabla.

#### Código inicial
```c
#include <stdio.h>

typedef void (*Destino)(int);

void a_la_forja(int tren) { printf("tren %d a la forja\n", tren); }
void a_la_mina(int tren) { printf("tren %d a la mina\n", tren); }
void al_archivo(int tren) { printf("tren %d al archivo\n", tren); }

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
```

#### Entrada
```
0 2 1
```

#### Salida esperada
```
tren 1 a la forja
tren 2 al archivo
tren 3 a la mina
```

#### Solución
```c
#include <stdio.h>

typedef void (*Destino)(int);

void a_la_forja(int tren) { printf("tren %d a la forja\n", tren); }
void a_la_mina(int tren) { printf("tren %d a la mina\n", tren); }
void al_archivo(int tren) { printf("tren %d al archivo\n", tren); }

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
```

#### Al superarla
Ningún tren al puesto de Chispa. Chispa propone agregar un cuarto destino, «el comercio local». Votan en contra todos, incluso el slime.

#### Imagen
- Un tablero de palancas con tres destinos tallados: forja, mina, archivo.
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) señala un cuarto lugar vacío en el tablero.

### Micro-misión R03-N05-P3 · Contar los que cumplen

```meta
lugar: El tablero de palancas
personajes: Kira, Gheco, Tizón
carta: Funciones como parámetro | contar(v, n, criterio) · el criterio es una función que dice sí o no · la misma cuenta sirve para cualquier pregunta
recompensa: xp 15, oro 15
```

#### Escena
Tizón escribe una función para contar las cargas pesadas, otra para las livianas, otra para las pares… Kira le muestra que con **una sola** alcanza, si se le pasa la pregunta.

#### Gheco sugiere
`int contar(const int v[], int n, int (*criterio)(int))` recorre y suma 1 cada vez que `criterio(v[i])` es verdadero. Se llama `contar(cargas, 6, es_pesada)`.

#### Desafío
Completá la pregunta dentro de `contar`.

#### Código inicial
```c
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
    printf("pesadas: %d\n", contar(cargas, 6, es_pesada));
    printf("pares: %d\n", contar(cargas, 6, es_par));
    return 0;
}
```

#### Salida esperada
```
pesadas: 3
pares: 5
```

#### Solución
```c
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
    printf("pesadas: %d\n", contar(cargas, 6, es_pesada));
    printf("pares: %d\n", contar(cargas, 6, es_par));
    return 0;
}
```

#### Al superarla
Tres pesadas, cinco pares, una sola función. Tizón tacha cinco páginas de la libreta. Le duele, pero las tacha.

#### Imagen
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) tacha páginas enteras de la libreta, con lágrimas en los ojos.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) le da una palmadita.

### Micro-misión R03-N05-P4 · El ordenador que pide cómo

```meta
lugar: El tablero de palancas
personajes: Kira, Gheco, Maese Ferrum
carta: qsort de mayor a menor | la comparación decide el orden · b - a ordena de mayor a menor · el autómata no sabe: vos le explicás
recompensa: xp 15, oro 15
```

#### Escena
El autómata de bronce que ordenaba el cuadro de honor funcionaba así: vos le dabas la palanca. Ferrum quiere las cargas de **mayor a menor**, para mandar primero las pesadas.

#### Gheco sugiere
`qsort` llama a tu comparación con dos punteros. Para ordenar de **mayor a menor**, se devuelve `*y - *x` (al revés que de menor a mayor).

#### Desafío
Completá la comparación de mayor a menor.

#### Código inicial
```c
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
    printf("\n");
    return 0;
}
```

#### Salida esperada
```
400 350 210 120 90 75
```

#### Solución
```c
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
    printf("\n");
    return 0;
}
```

#### Al superarla
Cuatrocientos primero. El autómata de bronce hace su reverencia. Ferrum le da una palmadita en la cabeza, cuando cree que nadie lo ve.

#### Imagen
- Un autómata de bronce chiquito ordenando bolsas de mayor a menor.
- Maese Ferrum (herrero enorme, más alto y ancho que Kira, pelo gris peinado hacia atrás, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) le da una palmadita en la cabeza.

### Misión R03-N05-M1 · El filtro de la horda

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

1. Con un array de `Enemigo` (nombre, vida, ataque), escribí condiciones `esta_vivo`, `es_peligroso` (ataque 10 o más) y `esta_herido` (vivo con menos de 20 de vida), todas con la forma `bool (*)(const Enemigo *)`.
2. Escribí `int filtrar(const Enemigo *v, int n, Condicion cumple, const Enemigo **salida)`, que guarda en `salida` punteros a los que cumplen y devuelve cuántos son.
3. Listá los vivos, los peligrosos y los heridos de la horda `Slime (0, 2)`, `Goblin (15, 6)`, `Orco (40, 12)`, `Troll (8, 15)` y `Esqueleto (25, 9)`.

#### Criterio de aprobación

- Define un `typedef` para la condición.
- Una sola función `filtrar` sirve para las tres condiciones.
- Muestra los tres listados.

#### Salida esperada

```
vivos        (4): Goblin Orco Troll Esqueleto
peligrosos   (2): Orco Troll
heridos      (2): Goblin Troll
```

#### Solución de referencia

```c
/* Mision 1 - El filtro de la horda: una funcion que filtra segun la condicion que le pasen. */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    const char *nombre;
    int vida;
    int ataque;
} Enemigo;

typedef bool (*Condicion)(const Enemigo *);

bool esta_vivo(const Enemigo *e) { return e->vida > 0; }
bool es_peligroso(const Enemigo *e) { return e->ataque >= 10; }
bool esta_herido(const Enemigo *e) { return e->vida > 0 && e->vida < 20; }

int filtrar(const Enemigo *v, int n, Condicion cumple, const Enemigo **salida)
{
    int k = 0;
    for (int i = 0; i < n; i++) {
        if (cumple(&v[i])) {
            salida[k++] = &v[i];
        }
    }
    return k;
}

void listar(const char *titulo, const Enemigo *v, int n, Condicion c)
{
    const Enemigo *elegidos[10];
    int k = filtrar(v, n, c, elegidos);
    printf("%-12s (%d):", titulo, k);
    for (int i = 0; i < k; i++) {
        printf(" %s", elegidos[i]->nombre);
    }
    printf("\n");
}

int main(void)
{
    Enemigo horda[] = {
        { "Slime", 0, 2 }, { "Goblin", 15, 6 }, { "Orco", 40, 12 },
        { "Troll", 8, 15 }, { "Esqueleto", 25, 9 },
    };
    int n = sizeof(horda) / sizeof(horda[0]);
    listar("vivos", horda, n, esta_vivo);
    listar("peligrosos", horda, n, es_peligroso);
    listar("heridos", horda, n, esta_herido);
    return 0;
}
```

### Misión R03-N05-M2 · Los conjuros de mina de Hulda

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hulda (vida 40, maná 20) lee órdenes, una por línea: `fuego` (cuesta 10), `curar` (cuesta 5, +15 de vida) y `meditar` (gratis, +8 de maná). Guardá los hechizos en una **tabla** de structs con la orden, el costo y la función. Para cada orden: si no existe, avisá; si no alcanza el maná, avisá; si no, ejecutá la función. Mostrá vida y maná después de cada orden.

#### Criterio de aprobación

- Usa una tabla de structs con un puntero a función.
- No usa un `if` por hechizo para decidir qué hacer.
- Controla el maná antes de ejecutar y avisa las órdenes desconocidas.

#### Entrada de ejemplo

```
fuego
curar
volar
fuego
meditar
fuego
```

#### Salida esperada

```
> fuego
  ¡Bola de fuego! (-10 maná)
  vida 40, maná 10
> curar
  Te curás 15 (-5 maná)
  vida 55, maná 5
> volar
  Hulda no conoce ese hechizo.
  vida 55, maná 5
> fuego
  No alcanza el maná (5).
  vida 55, maná 5
> meditar
  Meditás (+8 maná)
  vida 55, maná 13
> fuego
  ¡Bola de fuego! (-10 maná)
  vida 55, maná 3
```

#### Solución de referencia

```c
/* Mision 2 - El libro de hechizos: cada orden se busca en una tabla de nombre + funcion. */
#include <stdio.h>
#include <string.h>

typedef struct {
    int vida;
    int mana;
} Mago;

typedef void (*Accion)(Mago *);

void bola_de_fuego(Mago *m) { m->mana -= 10; printf("  ¡Bola de fuego! (-10 maná)\n"); }
void curarse(Mago *m) { m->mana -= 5; m->vida += 15; printf("  Te curás 15 (-5 maná)\n"); }
void meditar(Mago *m) { m->mana += 8; printf("  Meditás (+8 maná)\n"); }

typedef struct {
    const char *orden;
    int costo;
    Accion hacer;
} Hechizo;

static const Hechizo LIBRO[] = {
    { "fuego", 10, bola_de_fuego },
    { "curar", 5, curarse },
    { "meditar", 0, meditar },
};

int main(void)
{
    Mago hulda = { 40, 20 };
    char linea[40];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        const Hechizo *h = NULL;
        for (size_t i = 0; i < sizeof(LIBRO) / sizeof(LIBRO[0]); i++) {
            if (strcmp(LIBRO[i].orden, linea) == 0) {
                h = &LIBRO[i];
            }
        }
        printf("> %s\n", linea);
        if (h == NULL) {
            printf("  Hulda no conoce ese hechizo.\n");
        } else if (hulda.mana < h->costo) {
            printf("  No alcanza el maná (%d).\n", hulda.mana);
        } else {
            h->hacer(&hulda);
        }
        printf("  vida %d, maná %d\n", hulda.vida, hulda.mana);
    }
    return 0;
}
```

#### Pruebas

##### Medita mucho
```entrada
meditar
meditar
fuego
fuego
fuego
```
```salida
> meditar
  Meditás (+8 maná)
  vida 40, maná 28
> meditar
  Meditás (+8 maná)
  vida 40, maná 36
> fuego
  ¡Bola de fuego! (-10 maná)
  vida 40, maná 26
> fuego
  ¡Bola de fuego! (-10 maná)
  vida 40, maná 16
> fuego
  ¡Bola de fuego! (-10 maná)
  vida 40, maná 6
```

##### Sin maná para curar
```entrada
fuego
fuego
curar
```
```salida
> fuego
  ¡Bola de fuego! (-10 maná)
  vida 40, maná 10
> fuego
  ¡Bola de fuego! (-10 maná)
  vida 40, maná 0
> curar
  No alcanza el maná (0).
  vida 40, maná 0
```

##### Hechizos desconocidos
```entrada
rayo
volar
```
```salida
> rayo
  Hulda no conoce ese hechizo.
  vida 40, maná 20
> volar
  Hulda no conoce ese hechizo.
  vida 40, maná 20
```

### Misión R03-N05-M3 · Ordenar de muchas formas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con un array de armas (nombre, daño, peso), escribí tres comparadores para `qsort`: por nombre, por daño de mayor a menor y por peso de menor a mayor (sin restar `double`). Guardalos en un **array de punteros a función** y, por cada número que se lea (1, 2 o 3), ordená con el comparador elegido y mostrá el resultado.

#### Criterio de aprobación

- Guarda los tres comparadores en un array.
- El comparador por peso no resta `double`.
- Valida la opción.

#### Entrada de ejemplo

```
2
1
7
3
```

#### Salida esperada

```
por daño: Hacha(14, 4.5) Espada(11, 3.2) Arco(9, 1.5) Daga(6, 0.8)
por nombre: Arco(9, 1.5) Daga(6, 0.8) Espada(11, 3.2) Hacha(14, 4.5)
Elegí 1, 2 o 3.
por peso: Daga(6, 0.8) Arco(9, 1.5) Espada(11, 3.2) Hacha(14, 4.5)
```

#### Solución de referencia

```c
/* Mision 3 - Ordenar de muchas formas: la forma de comparar se elige de un array de funciones. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char nombre[12];
    int danio;
    double peso;
} Arma;

int por_nombre(const void *a, const void *b)
{
    return strcmp(((const Arma *) a)->nombre, ((const Arma *) b)->nombre);
}

int por_danio(const void *a, const void *b)
{
    return ((const Arma *) b)->danio - ((const Arma *) a)->danio;   /* de mayor a menor */
}

int por_peso(const void *a, const void *b)
{
    double pa = ((const Arma *) a)->peso, pb = ((const Arma *) b)->peso;
    return (pa > pb) - (pa < pb);                                    /* sin restar doubles */
}

typedef int (*Comparador)(const void *, const void *);

int main(void)
{
    Arma armas[] = { { "Hacha", 14, 4.5 }, { "Daga", 6, 0.8 }, { "Espada", 11, 3.2 }, { "Arco", 9, 1.5 } };
    int n = sizeof(armas) / sizeof(armas[0]);
    Comparador formas[] = { por_nombre, por_danio, por_peso };
    const char *titulos[] = { "por nombre", "por daño", "por peso" };

    char linea[20];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        int op;
        if (sscanf(linea, "%d", &op) != 1 || op < 1 || op > 3) {
            printf("Elegí 1, 2 o 3.\n");
            continue;
        }
        qsort(armas, n, sizeof armas[0], formas[op - 1]);
        printf("%s:", titulos[op - 1]);
        for (int i = 0; i < n; i++) {
            printf(" %s(%d, %.1f)", armas[i].nombre, armas[i].danio, armas[i].peso);
        }
        printf("\n");
    }
    return 0;
}
```

#### Pruebas

##### Todas las formas
```entrada
1
2
3
```
```salida
por nombre: Arco(9, 1.5) Daga(6, 0.8) Espada(11, 3.2) Hacha(14, 4.5)
por daño: Hacha(14, 4.5) Espada(11, 3.2) Arco(9, 1.5) Daga(6, 0.8)
por peso: Daga(6, 0.8) Arco(9, 1.5) Espada(11, 3.2) Hacha(14, 4.5)
```

##### Inválidos
```entrada
0
4
x
```
```salida
Elegí 1, 2 o 3.
Elegí 1, 2 o 3.
Elegí 1, 2 o 3.
```


### Encargo R03-N05-E1 · La calculadora del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Leé cuentas como `12.5 * 4`, una por línea. Cada operador (`+`, `-`, `*`, `x`, `/`) tiene su función en una tabla de `{ símbolo, función }`. Las funciones devuelven `bool` (si se pudo calcular) y dejan el resultado en un `double *`. Avisá las cuentas mal escritas, los operadores desconocidos y la división por cero.

#### Criterio de aprobación

- Tabla de operadores con punteros a función.
- La división por cero la detecta la función y lo informa.
- Avisa las líneas mal escritas y los operadores desconocidos.

#### Entrada de ejemplo

```
12.5 * 4
7 / 0
3 ^ 2
hola
10 x 3
9 - 12
```

#### Salida esperada

```
12.5 * 4 = 50
7 / 0: no se puede dividir por cero
Operador desconocido: ^
No entiendo la cuenta.
10 x 3 = 30
9 - 12 = -3
```

#### Solución de referencia

```c
/* Encargo - La calculadora del Gremio: cada operador tiene su funcion en una tabla. */
#include <stdio.h>
#include <stdbool.h>

typedef bool (*Operacion)(double, double, double *);

bool sumar(double a, double b, double *r) { *r = a + b; return true; }
bool restar(double a, double b, double *r) { *r = a - b; return true; }
bool multiplicar(double a, double b, double *r) { *r = a * b; return true; }
bool dividir(double a, double b, double *r)
{
    if (b == 0) {
        return false;
    }
    *r = a / b;
    return true;
}

typedef struct {
    char simbolo;
    Operacion calcular;
} Operador;

static const Operador OPERADORES[] = {
    { '+', sumar }, { '-', restar }, { '*', multiplicar }, { 'x', multiplicar }, { '/', dividir },
};

int main(void)
{
    char linea[80];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        double a, b, r;
        char op;
        if (sscanf(linea, "%lf %c %lf", &a, &op, &b) != 3) {
            printf("No entiendo la cuenta.\n");
            continue;
        }
        Operacion f = NULL;
        for (size_t i = 0; i < sizeof(OPERADORES) / sizeof(OPERADORES[0]); i++) {
            if (OPERADORES[i].simbolo == op) {
                f = OPERADORES[i].calcular;
            }
        }
        if (f == NULL) {
            printf("Operador desconocido: %c\n", op);
        } else if (!f(a, b, &r)) {
            printf("%g %c %g: no se puede dividir por cero\n", a, op, b);
        } else {
            printf("%g %c %g = %g\n", a, op, b, r);
        }
    }
    return 0;
}
```

#### Pruebas

##### Negativos y decimales
```entrada
-2.5 * 4
0.1 + 0.2
```
```salida
-2.5 * 4 = -10
0.1 + 0.2 = 0.3
```

##### Mal escritas
```entrada
5 +
* 3
```
```salida
No entiendo la cuenta.
No entiendo la cuenta.
```

##### División con resto
```entrada
10 / 4
```
```salida
10 / 4 = 2.5
```

### Prueba del sello

#### ¿Qué diferencia hay entre `doble` y `doble(3)`?

`doble` es la función (su dirección); `doble(3)` es llamarla y da un `int`.

#### ¿Qué declara `int (*f)(int);`? ¿Y `int *f(int);`?

El primero, un puntero a una función que recibe un `int` y devuelve un `int`. El segundo, una función que devuelve un `int *`.

#### ¿Qué es un *callback*?

Una función que se le pasa a otra para que la llame cuando corresponda, como la comparación de `qsort`.

#### ¿Qué ventaja tiene una tabla de acciones sobre un `if`/`else` largo?

Agregar una acción es agregar una fila; el código que busca y ejecuta no cambia.

#### ¿Por qué no conviene `return a->peso - b->peso;` en un comparador de `double`?

Porque el resultado se convierte a `int`: una diferencia de 0.5 da 0 y el orden sale mal.

### Soluciones (docente)

Unidad nueva (en `02-C-Intermedio` estaba planificada como 20, sin escribir).

## R03-N06 · Jefe: la Sanguijuela de las Minas

```meta
tipo: jefe
padre: R03-N05
precio: 10
criatura: dragon
insignia: Sello de la Sanguijuela
insignia_descripcion: Venciste a la Sanguijuela de las Minas: pedís y devolvés la memoria sin perder un byte.
usa: mem.dinamica, alg.listas-enlazadas, cal.depuracion
```

### Crónica

En lo más hondo de las Minas, algo enorme y blando se arrastra entre los túneles: la **Sanguijuela**. Cada vagoneta que alguien pidió y nunca devolvió la hizo crecer, y está gordísima. Hulda revisa la tablilla: casi todas las vagonetas que se comió son de Chispa.

Chispa silba mirando para otro lado.

—Hoy no alcanza con que el programa ande —dice {mentor}, y Hulda le da a Kira una lámpara que brilla distinto: el **sanitizador**—. Tiene que andar **y** devolver todo lo que pidió. Con esta luz, la Sanguijuela no se puede esconder.

### Objetivos

- Escribir un programa completo con memoria dinámica que no pierda ni un byte.
- Combinar array dinámico, textos con memoria propia, listas y punteros a función.
- Encontrar y corregir errores de memoria con `-fsanitize=address`.

### Antes de empezar

Todos los nodos de *Las Minas*. Es un **proyecto integrador**: no hay teoría nueva.

### Explicación

#### El sanitizador, tu lámpara

Para este jefe, compilá **siempre** así:

```bash
gcc -std=c11 -Wall -Wextra -g -fsanitize=address -o programa main.c
./programa < entrada.txt
```

- `-g` agrega los números de línea a los mensajes.
- `-fsanitize=address` vigila cada acceso a memoria. Si leés fuera de un bloque, usás uno liberado o te olvidás un `free`, el programa se corta (o avisa al terminar) diciendo **qué** pasó y **en qué línea**.

Un informe típico se lee de arriba hacia abajo:

```
==4321==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010
READ of size 8 at 0x602000000010 thread T0
    #0 0x401234 in derrumbar main.c:43        <- dónde se usó mal
freed by thread T0 here:
    #1 0x401222 in derrumbar main.c:44        <- dónde se liberó
```

#### Quién es dueño de cada bloque

En un programa grande, la pregunta clave es **quién libera cada cosa**. Una regla simple:

- Si un struct tiene un puntero a memoria propia (como `char *nombre`), la función que **destruye** el struct libera primero ese puntero y después el struct.
- Si se quita un elemento del medio, se liberan **sus** partes antes de pisarlo.

#### Ordenes por línea

Los programas del jefe leen órdenes como `agregar Orco 40 12`. `sscanf` con `%*s` **saltea** una palabra sin guardarla:

```c
char nombre[40];
int vida, ataque;
if (sscanf(linea, "%*s %39s %d %d", nombre, &vida, &ataque) == 3) { ... }
```

El `%39s` lee una palabra de hasta 39 letras: nunca desborda `nombre`.

### ¿Para qué sirve?

Los programas que corren durante días (servidores, bases de datos, el sistema operativo, el firmware de un router) no pueden perder memoria: una fuga de pocos bytes por pedido, multiplicada por millones de pedidos, los termina tirando abajo. Por eso los equipos profesionales compilan sus pruebas con sanitizadores y usan `valgrind` antes de publicar una versión, y buena parte de los errores de seguridad graves son justamente errores de memoria como los de este jefe.

### Errores habituales

La Sanguijuela es la reina de los trolls de memoria:

- **Troll**: liberar el struct y no su `nombre` (fuga).
- **Troll**: leer `t->siguiente` después de `free(t)` (uso después de liberar).
- **Orco**: `malloc(strlen(nombre))` sin el `+ 1` (`heap-buffer-overflow`).
- **Troll**: al quitar un enemigo, pisarlo con el de atrás sin liberar su nombre.
- **Ogro**: no revisar el `NULL` de un `malloc`.
- **Orco**: `%s` sin ancho en `sscanf`: un nombre largo desborda el array.

### Micro-misión R03-N06-P1 · La tablilla de las deudas

```meta
lugar: Lo más hondo de las Minas
personajes: Kira, Gheco, Hulda
criatura: dragon
carta: Contar lo pedido y lo devuelto | un contador sube en cada malloc y baja en cada free · al final tiene que dar 0
recompensa: xp 15, oro 15
```

#### Escena
En lo más hondo, algo enorme y blando se arrastra entre los túneles: la **Sanguijuela**, gordísima. Hulda revisa la tablilla: casi todas las vagonetas que se comió son de Chispa.
Chispa silba mirando para otro lado.

#### Gheco sugiere
Se envuelven `malloc` y `free` en funciones que cuentan: `pedir()` suma 1 y `devolver()` resta 1. Si al final queda algo, hay fuga.

#### Desafío
Completá las dos cuentas.

#### Código inicial
```c
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
    printf("sin devolver: %d\n", prestadas);
    devolver(b);
    printf("sin devolver: %d\n", prestadas);
    return 0;
}
```

#### Salida esperada
```
sin devolver: 1
sin devolver: 0
```

#### Solución
```c
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
    printf("sin devolver: %d\n", prestadas);
    devolver(b);
    printf("sin devolver: %d\n", prestadas);
    return 0;
}
```

#### Al superarla
Cero sin devolver. La Sanguijuela se da vuelta, molesta: por ese lado no le queda nada para comer.

#### Imagen
- La Sanguijuela de las Minas (sanguijuela enorme y translúcida, violeta oscura, con vagonetas tragadas que se ven dentro de su cuerpo) enroscada en las vías.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) sostiene una tablilla con una cuenta que llega a cero.

### Micro-misión R03-N06-P2 · Liberar toda la cadena

```meta
lugar: Lo más hondo de las Minas
personajes: Kira, Gheco, Tizón
criatura: troll
carta: Liberar una lista | guardar el siguiente ANTES del free · después del free, el nodo ya no se puede leer
recompensa: xp 15, oro 15
```

#### Escena
La Sanguijuela se enrosca en un tren abandonado de cinco vagones. Para dejarla sin comida, hay que liberar los cinco… sin leer ningún vagón ya liberado.

#### Gheco sugiere
En el bucle: `Vagon *sig = p->siguiente;` **antes** de `free(p)`, y después `p = sig;`.

#### Desafío
Completá la liberación segura.

#### Código inicial
```c
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
    printf("vagones liberados: %d\n", liberados);
    return 0;
}
```

#### Salida esperada
```
vagones liberados: 5
```

#### Solución
```c
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
    printf("vagones liberados: %d\n", liberados);
    return 0;
}
```

#### Al superarla
Cinco vagones liberados, ni uno perdido. La Sanguijuela se queda sin el tren y empieza a achicarse.

#### Imagen
- Un tren de cinco vagones que se desarma de a uno, en orden.
- La Sanguijuela, más flaca, se aleja.

### Micro-misión R03-N06-P3 · La lámpara que no deja esconderse

```meta
lugar: Lo más hondo de las Minas
personajes: Kira, Gheco, Hulda
carta: El orden de los free | primero lo de adentro, después lo de afuera · un struct con un puntero a memoria pedida necesita dos free
recompensa: xp 15, oro 15
```

#### Escena
Hulda le da a Kira una lámpara que brilla distinto, y con esa luz se ve el truco: cada minero tiene un **nombre** pedido aparte. Liberar la ficha sin liberar el nombre deja comida para la Sanguijuela.

#### Gheco sugiere
Si un struct pedido con `malloc` tiene adentro otro bloque pedido (el nombre), primero se libera el de **adentro** (`free(m->nombre)`) y después el de afuera (`free(m)`).

#### Desafío
Completá los dos `free` en el orden correcto.

#### Código inicial
```c
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
    printf("%s con %d de vida\n", m->nombre, m->vida);
    destruir(m);
    printf("ficha y nombre devueltos\n");
    return 0;
}
```

#### Salida esperada
```
Hulda con 120 de vida
ficha y nombre devueltos
```

#### Solución
```c
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
    printf("%s con %d de vida\n", m->nombre, m->vida);
    destruir(m);
    printf("ficha y nombre devueltos\n");
    return 0;
}
```

#### Al superarla
Con la lámpara encendida, la Sanguijuela ya no tiene dónde esconderse. Se encoge contra la pared de roca.

#### Imagen
- Una lámpara de minero que proyecta una luz cian sobre las paredes de la mina.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) se la entrega a Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian).

### Micro-misión R03-N06-P4 · La Sanguijuela, flaquita

```meta
lugar: Lo más hondo de las Minas
personajes: Kira, Gheco, Hulda, Chispa
criatura: dragon
carta: Todo junto | pedir, crecer, enganchar y devolver todo · contar lo que queda prestado · terminar en cero
recompensa: xp 25, oro 30
item: Lámpara del Minero
```

#### Escena
Última pelea. La Sanguijuela tiene en la panza las vagonetas de toda la temporada. Kira arma una cola de vagonetas, las saca una por una por la boca de la mina, y las devuelve todas. Si al final la tablilla da cero, la Sanguijuela no tiene de qué vivir.

#### Gheco sugiere
Encolar pide (`malloc`, suma 1), desencolar devuelve (`free`, resta 1). Al terminar, se desencola todo y la cuenta tiene que dar 0.

#### Desafío
Completá el desencolado y la cuenta.

#### Código inicial
```c
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
        printf("sale la vagoneta %d\n", sale->numero);
        free(sale);
        prestadas--;
    }
    printf("en la panza de la sanguijuela: %d\n", prestadas);
    while (frente != NULL) {
        Nodo *sale = frente;
        ___;
        ___;
        ___;
    }
    fondo = NULL;
    printf("en la panza de la sanguijuela: %d\n", prestadas);
    return 0;
}
```

#### Entrada
```
3
```

#### Salida esperada
```
sale la vagoneta 1
sale la vagoneta 2
sale la vagoneta 3
en la panza de la sanguijuela: 3
en la panza de la sanguijuela: 0
```

#### Solución
```c
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
        printf("sale la vagoneta %d\n", sale->numero);
        free(sale);
        prestadas--;
    }
    printf("en la panza de la sanguijuela: %d\n", prestadas);
    while (frente != NULL) {
        Nodo *sale = frente;
        frente = frente->siguiente;
        free(sale);
        prestadas--;
    }
    fondo = NULL;
    printf("en la panza de la sanguijuela: %d\n", prestadas);
    return 0;
}
```

#### Al superarla
Cero. La Sanguijuela queda flaquita y avergonzada, y se escurre por una grieta. Hulda le regala a Kira la lámpara: **la Lámpara del Minero**, que va a tu mochila. —Para que no se te esconda nada nunca más. —Chispa paga, por primera vez, todas sus vagonetas atrasadas. En chistes.

#### Imagen
- La Sanguijuela, flaquita y avergonzada, se escurre por una grieta.
- Hulda (enana fortísima, casco de minera con farol naranja, trenzas grises y negras, pico al hombro) le da una lámpara de minero a Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian).
- Chispa (mercader alto y flaco, sombrero de ala corta, chaqueta larga con muchos bolsillos, bufanda naranja, diente de oro) cuenta un chiste frente a toda la mina.

### Misión R03-N06-M1 · El registro de la horda

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Escribí un registro de enemigos que lee órdenes, una por línea, hasta que se termine la entrada (mostrá cada orden con `> ` antes de procesarla):

- `agregar Nombre vida ataque`: agrega al enemigo. El nombre se guarda en **memoria propia** (`char *`, `strlen + 1`). No se repiten nombres; los datos inválidos se avisan.
- `golpe Nombre daño`: le resta vida; si llega a 0 o menos, **cae** y se quita del registro (liberando su nombre).
- `ordenar vida|ataque|nombre`: ordena con `qsort` usando una **tabla de comparadores** (vida y ataque de mayor a menor) y muestra el registro.
- `mostrar`: muestra `N enemigos: Nombre(vida/ataque) ...`.
- Cualquier otra cosa: `Orden desconocida`.

El registro es un **array dinámico** que crece duplicando. Al terminar, mostrá cuántos quedan y liberá **todo**. Tiene que pasar `-fsanitize=address` sin avisos.

#### Criterio de aprobación

- Array dinámico que crece con `realloc` y temporal.
- Cada nombre tiene su propia memoria y se libera al quitar y al final.
- Ordena con una tabla de comparadores.
- Sin fugas ni errores con `-fsanitize=address`.

#### Entrada de ejemplo

```
agregar Orco 40 12
agregar Slime 8 2
agregar Troll 70 15
agregar Orco 5 5
agregar Goblin 22 16
golpe Slime 10
golpe Troll 25
ordenar vida
ordenar ataque
volar
golpe Dragon 3
ordenar nombre
```

#### Salida esperada

```
> agregar Orco 40 12
> agregar Slime 8 2
> agregar Troll 70 15
> agregar Orco 5 5
  Orco ya está en el registro
> agregar Goblin 22 16
> golpe Slime 10
  ¡Slime cae!
> golpe Troll 25
  Troll queda con 45
> ordenar vida
  3 enemigos: Troll(45/15) Orco(40/12) Goblin(22/16)
> ordenar ataque
  3 enemigos: Goblin(22/16) Troll(45/15) Orco(40/12)
> volar
  Orden desconocida
> golpe Dragon 3
  No hay nadie así
> ordenar nombre
  3 enemigos: Goblin(22/16) Orco(40/12) Troll(45/15)
Fin del registro: quedan 3. Se libera todo.
```

#### Solución de referencia

```c
/*
 * Jefe R03 - Mision 1: el registro de la horda.
 * Array dinamico de enemigos con nombre en memoria propia, ordenes por linea,
 * comparadores en una tabla y todo liberado al final.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char *nombre;          /* memoria propia: strlen + 1 */
    int vida;
    int ataque;
} Enemigo;

typedef struct {
    Enemigo *datos;
    int cantidad;
    int capacidad;
} Horda;

char *duplicar(const char *texto)
{
    char *copia = malloc(strlen(texto) + 1);
    if (copia != NULL) {
        strcpy(copia, texto);
    }
    return copia;
}

int buscar(const Horda *h, const char *nombre)
{
    for (int i = 0; i < h->cantidad; i++) {
        if (strcmp(h->datos[i].nombre, nombre) == 0) {
            return i;
        }
    }
    return -1;
}

bool agregar(Horda *h, const char *nombre, int vida, int ataque)
{
    if (h->cantidad == h->capacidad) {
        int nueva = h->capacidad == 0 ? 2 : h->capacidad * 2;
        Enemigo *tmp = realloc(h->datos, nueva * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        h->datos = tmp;
        h->capacidad = nueva;
    }
    char *copia = duplicar(nombre);
    if (copia == NULL) {
        return false;
    }
    h->datos[h->cantidad++] = (Enemigo) { copia, vida, ataque };
    return true;
}

void quitar(Horda *h, int i)
{
    free(h->datos[i].nombre);                  /* primero la memoria del nombre */
    for (int k = i; k < h->cantidad - 1; k++) {
        h->datos[k] = h->datos[k + 1];
    }
    h->cantidad--;
}

void liberar(Horda *h)
{
    for (int i = 0; i < h->cantidad; i++) {
        free(h->datos[i].nombre);
    }
    free(h->datos);
    h->datos = NULL;
    h->cantidad = h->capacidad = 0;
}

int por_vida(const void *a, const void *b) { return ((const Enemigo *) b)->vida - ((const Enemigo *) a)->vida; }
int por_ataque(const void *a, const void *b) { return ((const Enemigo *) b)->ataque - ((const Enemigo *) a)->ataque; }
int por_nombre(const void *a, const void *b) { return strcmp(((const Enemigo *) a)->nombre, ((const Enemigo *) b)->nombre); }

typedef struct {
    const char *campo;
    int (*comparar)(const void *, const void *);
} Orden;

static const Orden ORDENES[] = { { "vida", por_vida }, { "ataque", por_ataque }, { "nombre", por_nombre } };

void mostrar(const Horda *h)
{
    printf("  %d enemigos:", h->cantidad);
    for (int i = 0; i < h->cantidad; i++) {
        printf(" %s(%d/%d)", h->datos[i].nombre, h->datos[i].vida, h->datos[i].ataque);
    }
    printf("\n");
}

int main(void)
{
    Horda h = { NULL, 0, 0 };
    char linea[100];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        char orden[16], nombre[40];
        int a, b;
        printf("> %s\n", linea);

        if (sscanf(linea, "%15s", orden) != 1) {
            continue;
        }
        if (strcmp(orden, "agregar") == 0) {
            if (sscanf(linea, "%*s %39s %d %d", nombre, &a, &b) != 3 || a <= 0 || b < 0) {
                printf("  Uso: agregar Nombre vida ataque\n");
            } else if (buscar(&h, nombre) >= 0) {
                printf("  %s ya está en el registro\n", nombre);
            } else if (!agregar(&h, nombre, a, b)) {
                printf("  Sin memoria\n");
            }
        } else if (strcmp(orden, "golpe") == 0) {
            int i;
            if (sscanf(linea, "%*s %39s %d", nombre, &a) != 2 || (i = buscar(&h, nombre)) < 0) {
                printf("  No hay nadie así\n");
            } else {
                h.datos[i].vida -= a;
                if (h.datos[i].vida <= 0) {
                    printf("  ¡%s cae!\n", nombre);
                    quitar(&h, i);
                } else {
                    printf("  %s queda con %d\n", nombre, h.datos[i].vida);
                }
            }
        } else if (strcmp(orden, "ordenar") == 0) {
            const Orden *o = NULL;
            for (size_t k = 0; k < sizeof(ORDENES) / sizeof(ORDENES[0]); k++) {
                if (sscanf(linea, "%*s %39s", nombre) == 1 && strcmp(ORDENES[k].campo, nombre) == 0) {
                    o = &ORDENES[k];
                }
            }
            if (o == NULL) {
                printf("  Se ordena por vida, ataque o nombre\n");
            } else {
                qsort(h.datos, h.cantidad, sizeof h.datos[0], o->comparar);
                mostrar(&h);
            }
        } else if (strcmp(orden, "mostrar") == 0) {
            mostrar(&h);
        } else {
            printf("  Orden desconocida\n");
        }
    }
    printf("Fin del registro: quedan %d. Se libera todo.\n", h.cantidad);
    liberar(&h);
    return 0;
}
```

#### Pruebas

##### Registro vacío
```entrada
mostrar
ordenar vida
golpe Orco 5
```
```salida
> mostrar
  0 enemigos:
> ordenar vida
  0 enemigos:
> golpe Orco 5
  No hay nadie así
Fin del registro: quedan 0. Se libera todo.
```

##### Datos inválidos
```entrada
agregar Orco cero 10
agregar Troll 50
agregar
```
```salida
> agregar Orco cero 10
  Uso: agregar Nombre vida ataque
> agregar Troll 50
  Uso: agregar Nombre vida ataque
> agregar
  Uso: agregar Nombre vida ataque
Fin del registro: quedan 0. Se libera todo.
```

##### Crece más allá de la capacidad inicial
```entrada
agregar A 1 1
agregar B 2 2
agregar C 3 3
agregar D 4 4
agregar E 5 5
agregar F 6 6
agregar G 7 7
agregar H 8 8
agregar I 9 9
ordenar ataque
```
```salida
> agregar A 1 1
> agregar B 2 2
> agregar C 3 3
> agregar D 4 4
> agregar E 5 5
> agregar F 6 6
> agregar G 7 7
> agregar H 8 8
> agregar I 9 9
> ordenar ataque
  9 enemigos: I(9/9) H(8/8) G(7/7) F(6/6) E(5/5) D(4/4) C(3/3) B(2/2) A(1/1)
Fin del registro: quedan 9. Se libera todo.
```

### Misión R03-N06-M2 · La mordida de la Sanguijuela

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

El programa del código inicial cava tres túneles y los recorre. Parece que funciona… pero la Sanguijuela lo mordió: tiene **tres errores de memoria**.

1. Compilalo con `-g -fsanitize=address` y ejecutalo.
2. Leé cada informe, encontrá la línea y arreglá el error **de a uno**, volviendo a compilar cada vez.
3. Agregá además los controles de `NULL` que faltan.
4. En un comentario al principio, explicá los tres errores con tus palabras.

La salida tiene que ser la misma, pero ahora sin ningún aviso del sanitizador.

#### Criterio de aprobación

- Corrige el `malloc` al que le faltaba el byte del `'\0'`.
- Corrige `derrumbar`: guarda el siguiente antes del `free` y libera también el nombre.
- Revisa el `NULL` de cada `malloc`.
- Explica los tres errores en un comentario; sin avisos del sanitizador.

#### Código inicial

```c
/*
 * Jefe R03 - Mision 2: la mordida de la Sanguijuela.
 * Este programa "funciona", pero tiene TRES errores de memoria.
 * Compilalo con -g -fsanitize=address, encontralos y arreglalos.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Tunel {
    char *nombre;
    int oro;
    struct Tunel *siguiente;
} Tunel;

Tunel *cavar(Tunel *cabeza, const char *nombre, int oro)
{
    Tunel *t = malloc(sizeof *t);
    t->nombre = malloc(strlen(nombre));
    strcpy(t->nombre, nombre);
    t->oro = oro;
    t->siguiente = cabeza;
    return t;
}

void recorrer(const Tunel *t)
{
    int total = 0;
    for (; t != NULL; t = t->siguiente) {
        printf("  %-10s %3d de oro\n", t->nombre, t->oro);
        total += t->oro;
    }
    printf("  Total: %d\n", total);
}

void derrumbar(Tunel *cabeza)
{
    for (Tunel *t = cabeza; t != NULL; t = t->siguiente) {
        free(t);
    }
}

int main(void)
{
    Tunel *mina = NULL;
    mina = cavar(mina, "Norte", 12);
    mina = cavar(mina, "Pozo", 30);
    mina = cavar(mina, "Veta", 45);
    recorrer(mina);
    derrumbar(mina);
    return 0;
}
```

#### Salida esperada

```
  Veta        45 de oro
  Pozo        30 de oro
  Norte       12 de oro
  Total: 87
```

#### Solución de referencia

```c
/*
 * Jefe R03 - Mision 2: la mordida de la Sanguijuela, ya curada.
 *  1. malloc(strlen(nombre)) pedia un byte de menos: falta el '\0'.
 *  2. derrumbar leia t->siguiente DESPUES de free(t): uso despues de liberar.
 *  3. derrumbar liberaba el tunel pero no su nombre: fuga.
 * Ademas se revisa el NULL de cada malloc.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Tunel {
    char *nombre;
    int oro;
    struct Tunel *siguiente;
} Tunel;

Tunel *cavar(Tunel *cabeza, const char *nombre, int oro)
{
    Tunel *t = malloc(sizeof *t);
    if (t == NULL) {
        return cabeza;
    }
    t->nombre = malloc(strlen(nombre) + 1);
    if (t->nombre == NULL) {
        free(t);
        return cabeza;
    }
    strcpy(t->nombre, nombre);
    t->oro = oro;
    t->siguiente = cabeza;
    return t;
}

void recorrer(const Tunel *t)
{
    int total = 0;
    for (; t != NULL; t = t->siguiente) {
        printf("  %-10s %3d de oro\n", t->nombre, t->oro);
        total += t->oro;
    }
    printf("  Total: %d\n", total);
}

void derrumbar(Tunel *cabeza)
{
    while (cabeza != NULL) {
        Tunel *siguiente = cabeza->siguiente;
        free(cabeza->nombre);
        free(cabeza);
        cabeza = siguiente;
    }
}

int main(void)
{
    Tunel *mina = NULL;
    mina = cavar(mina, "Norte", 12);
    mina = cavar(mina, "Pozo", 30);
    mina = cavar(mina, "Veta", 45);
    recorrer(mina);
    derrumbar(mina);
    return 0;
}
```

### Encargo R03-N06-E1 · El historial del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

El escriba del Gremio quiere "deshacer". Guardá cada renglón escrito en una **pila** hecha con una lista enlazada (cada paso con su texto en memoria propia):

- `escribir texto`: apila el renglón.
- `deshacer`: saca el último (o avisa si no hay nada).
- `mostrar`: muestra el documento en el orden en que se escribió.

Al terminar, liberá todo lo que quede.

#### Criterio de aprobación

- La pila es una lista enlazada con memoria propia para cada texto.
- `mostrar` respeta el orden de escritura.
- Libera todo al final, sin fugas.

#### Entrada de ejemplo

```
escribir Pedido de clavos
escribir Pedido de herraduras
escribir Pedido de espadas
deshacer
escribir Pedido de escudos
mostrar
deshacer
deshacer
deshacer
deshacer
mostrar
```

#### Salida esperada

```
(deshecho: Pedido de espadas)
Documento:
  Pedido de clavos
  Pedido de herraduras
  Pedido de escudos
(deshecho: Pedido de escudos)
(deshecho: Pedido de herraduras)
(deshecho: Pedido de clavos)
(nada para deshacer)
Documento:
```

#### Solución de referencia

```c
/* Jefe R03 - Encargo: el historial del Gremio (una pila de "deshacer" con lista enlazada). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Paso {
    char *texto;
    struct Paso *anterior;      /* la pila crece hacia "atras" */
} Paso;

Paso *apilar(Paso *tope, const char *texto)
{
    Paso *p = malloc(sizeof *p);
    if (p == NULL) {
        return tope;
    }
    p->texto = malloc(strlen(texto) + 1);
    if (p->texto == NULL) {
        free(p);
        return tope;
    }
    strcpy(p->texto, texto);
    p->anterior = tope;
    return p;
}

Paso *desapilar(Paso *tope)
{
    Paso *debajo = tope->anterior;
    free(tope->texto);
    free(tope);
    return debajo;
}

void mostrar(const Paso *tope)
{
    /* el tope es lo ultimo escrito: se muestra de abajo hacia arriba con recursion */
    if (tope == NULL) {
        return;
    }
    mostrar(tope->anterior);
    printf("  %s\n", tope->texto);
}

int main(void)
{
    Paso *tope = NULL;
    char linea[120];
    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        linea[strcspn(linea, "\n")] = '\0';
        if (strncmp(linea, "escribir ", 9) == 0) {
            tope = apilar(tope, linea + 9);
        } else if (strcmp(linea, "deshacer") == 0) {
            if (tope == NULL) {
                printf("(nada para deshacer)\n");
            } else {
                printf("(deshecho: %s)\n", tope->texto);
                tope = desapilar(tope);
            }
        } else if (strcmp(linea, "mostrar") == 0) {
            printf("Documento:\n");
            mostrar(tope);
        }
    }
    while (tope != NULL) {
        tope = desapilar(tope);
    }
    return 0;
}
```

#### Pruebas

##### Deshacer sin nada
```entrada
deshacer
mostrar
```
```salida
(nada para deshacer)
Documento:
```

##### Escribir y mostrar
```entrada
escribir Uno
escribir Dos
mostrar
```
```salida
Documento:
  Uno
  Dos
```


### Prueba del sello

#### Si un struct tiene un `char *nombre` pedido con `malloc`, ¿en qué orden se libera?

Primero el nombre y después el struct: si se libera antes el struct, se pierde la dirección del nombre.

#### ¿Qué te dice un informe `heap-use-after-free`? ¿Y `heap-buffer-overflow`?

El primero, que se usó memoria ya liberada. El segundo, que se leyó o escribió fuera del bloque pedido (por ejemplo, un byte de más).

#### ¿Para qué sirve el `%*s` en `sscanf`?

Lee una palabra y la descarta, sin guardarla en ninguna variable.

#### ¿Por qué `%39s` y no `%s` para leer en un `char nombre[40]`?

Porque `%s` no tiene límite y un nombre largo desbordaría el array; con 39 queda lugar para el `'\0'`.

#### ¿Por qué un programa puede "funcionar" y tener igual errores de memoria?

Porque el comportamiento indefinido no siempre se nota: la memoria mal usada puede tener justo el valor esperado. El sanitizador los detecta aunque la salida sea correcta.

### Soluciones (docente)

Proyecto nuevo. Para corregir, compilar la entrega con `-g -fsanitize=address` y pasarle la entrada de ejemplo: no tiene que aparecer ningún informe.
