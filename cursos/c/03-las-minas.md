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

Bajo la Forja se abren **las Minas**: galerías que se cavan a medida que hacen falta. {mentor} te da una lámpara y una advertencia:

—Acá la memoria se pide y se **devuelve** a mano, {heroe}. Lo que pedís y no devolvés, se lo queda la **Sanguijuela**, que vive en el fondo y engorda con cada byte olvidado. Un día no queda lugar para nadie.

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

```bash
gcc -std=c11 -Wall -Wextra -o programa main.c
echo 3 | ./programa
```

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

En la galería de las Minas, la horda de enemigos no para de crecer: hoy son dos, mañana cinco, pasado veinte. El estante de piedra donde {mentor} anota a cada uno se queda chico todo el tiempo.

—No se cava una galería nueva por cada enemigo, {heroe} —dice—. Cuando se llena, se cava una **del doble**. Y se muda todo de una sola vez.

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

```bash
gcc -std=c11 -Wall -Wextra -o programa main.c && ./programa
```

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

Más abajo, las galerías de las Minas no están en fila: cada túnel termina en una puerta con una **cadena** que lleva al túnel siguiente. Para agregar uno no hay que mudar nada: se cava y se engancha.

—Pero cuidado, {heroe} —dice {mentor}—. Si soltás una cadena antes de agarrar la que sigue, todo lo que venía detrás queda perdido en la oscuridad. Para siempre.

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

#### ¿Lista o array dinámico?

| | Array dinámico (18) | Lista enlazada |
|---|---|---|
| Acceder al elemento 500 | inmediato: `v[500]` | recorrer 500 nodos |
| Insertar o quitar al frente | mover todos | inmediato |
| Memoria | un bloque (a veces sobra capacidad) | un bloque por nodo, más el puntero |

En la práctica, el array dinámico se usa más; la lista brilla cuando se insertan y quitan elementos en cualquier lugar todo el tiempo (y es la base de colas, pilas y grafos).

#### Cómo compilarlo y ejecutarlo

```bash
gcc -std=c11 -Wall -Wextra -g -fsanitize=address -o programa main.c && ./programa
```

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

## R03-N04 · Punteros a función

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: esqueleto
temas: mem.punteros-funcion, func.orden-superior
```

### Crónica

En el taller de las Minas hay un tablero con palancas. Cada palanca no hace nada por sí misma: **señala** a una máquina (la bomba de agua, el montacargas, el fuelle). Cambiás a qué máquina apunta y la misma palanca hace otra cosa.

—Así se escriben los hechizos que eligen **qué hacer** mientras el programa corre —dice {mentor}—. El autómata de bronce que ordenaba el estante funcionaba así, {heroe}: vos le dabas la palanca.

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

```bash
gcc -std=c11 -Wall -Wextra -o programa main.c && ./programa
```

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

### Misión R03-N04-M1 · El filtro de la horda

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

### Misión R03-N04-M2 · El libro de hechizos de Mia

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Mia (vida 40, maná 20) lee órdenes, una por línea: `fuego` (cuesta 10), `curar` (cuesta 5, +15 de vida) y `meditar` (gratis, +8 de maná). Guardá los hechizos en una **tabla** de structs con la orden, el costo y la función. Para cada orden: si no existe, avisá; si no alcanza el maná, avisá; si no, ejecutá la función. Mostrá vida y maná después de cada orden.

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
  Mia no conoce ese hechizo.
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
    Mago mia = { 40, 20 };
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
            printf("  Mia no conoce ese hechizo.\n");
        } else if (mia.mana < h->costo) {
            printf("  No alcanza el maná (%d).\n", mia.mana);
        } else {
            h->hacer(&mia);
        }
        printf("  vida %d, maná %d\n", mia.vida, mia.mana);
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
  Mia no conoce ese hechizo.
  vida 40, maná 20
> volar
  Mia no conoce ese hechizo.
  vida 40, maná 20
```

### Misión R03-N04-M3 · Ordenar de muchas formas

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


### Encargo R03-N04-E1 · La calculadora del Gremio

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

## R03-N05 · Jefe: la Sanguijuela de las Minas

```meta
tipo: jefe
padre: R03-N04
precio: 10
criatura: dragon
insignia: Sello de la Sanguijuela
insignia_descripcion: Venciste a la Sanguijuela de las Minas: pedís y devolvés la memoria sin perder un byte.
usa: mem.dinamica, alg.listas-enlazadas, cal.depuracion
```

### Crónica

En lo más hondo de las Minas, algo enorme y blando se arrastra entre los túneles: la **Sanguijuela**. Cada byte que alguien pidió y nunca devolvió la hizo crecer. Ya casi no queda lugar para cavar.

—Hoy no alcanza con que el programa funcione, {heroe} —dice {mentor}, y te da una lámpara que brilla distinto: el **sanitizador**—. Tiene que funcionar **y** devolver todo lo que pidió. Con esta luz, la Sanguijuela no se puede esconder.

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

### Misión R03-N05-M1 · El registro de la horda

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

### Misión R03-N05-M2 · La mordida de la Sanguijuela

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

### Encargo R03-N05-E1 · El historial del Gremio

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
