# RAMA R02 · Los pasillos numerados: arrays, textos, structs y punteros

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Arrays y matrices

```meta
tipo: tema
criatura: orco
padre: R01-N10
precio: 10
temas: col.arrays, col.matrices
```

### Crónica

Debajo de la Forja corren los **pasillos numerados**: una hilera de cajones de hierro, todos iguales, con un número grabado desde el **cero**.

—Pedí el cajón 3 y te lo doy —dice {mentor}—. Pedí el 5 en una hilera de cinco y también te doy algo… pero no es tuyo, {heroe}.

Al fondo del pasillo, algo se mueve entre las telarañas.

### Objetivos

Guardar muchos valores del mismo tipo en un **array**, recorrerlo con un `for`,
pasarlo a funciones y manejar arrays a medio llenar. Usar **matrices** (filas y
columnas) para representar un mapa. Entender por qué salirse del array es el
error más peligroso de C.

### Antes de empezar

- Bucles `for` (07).
- Funciones y paso por valor (08).
- `sizeof` y `#define` (02).

### Explicación

#### Qué es un array
Un array es una **hilera de variables del mismo tipo, una al lado de la otra en
la memoria**, con un solo nombre:
```c
int durezas[5] = { 42, 17, 99, 8, 55 };
```
```
índice:     [0]  [1]  [2]  [3]  [4]
durezas:    42   17   99    8   55
```
- Cada elemento se usa como una variable: `durezas[1] = 20;`,
  `printf("%d", durezas[0]);`.
- Los índices van de **0 a N-1**: el último de un array de 5 es `durezas[4]`.
- El tamaño es **fijo**: se decide al declararlo y no cambia. Conviene usar una
  constante (`#define CAPACIDAD 5`).

#### Inicializar
| Declaración | Contenido |
|---|---|
| `int a[4] = { 7, 3 };` | `7 3 0 0` (los que faltan quedan en 0) |
| `int a[4] = { 0 };` | todo en 0 |
| `int a[] = { 1, 2, 3 };` | el compilador cuenta: 3 elementos |
| `int a[4];` | **basura** (un array local sin inicializar tiene valores al azar) |

#### Cuántos elementos tiene: `sizeof`
`sizeof(durezas)` da los **bytes** de todo el array (5 × 4 = 20) y
`sizeof(durezas[0])`, los de uno. Dividiendo se obtiene la cantidad:
```c
int n = sizeof(durezas) / sizeof(durezas[0]);   /* 5 */
```
Esto funciona **solo donde se declaró el array**. Dentro de una función que lo
recibe, `sizeof` ya no sirve (ver abajo).

#### Recorrer
```c
for (int i = 0; i < n; i++) {        /* i < n, NO i <= n */
    suma += durezas[i];
}
```
Patrones que se repiten siempre: **sumar**, buscar el **máximo** (suponer que el
primero es el mayor y comparar con los demás), **contar** los que cumplen algo,
**buscar** un valor y devolver su posición o `-1` si no está.

#### Pasar un array a una función
```c
int sumar(const int valores[], int n);   /* el array y su cantidad */
...
int total = sumar(durezas, n);           /* sin corchetes al llamar */
```
- La función **no sabe** cuántos elementos tiene el array: hay que pasárselo en
  otro parámetro (`n`).
- **El array no se copia.** A diferencia de un `int` (08), la función recibe
  **dónde empieza** el array original, así que si lo modifica, cambia el de
  quien la llamó (`templar_todo`). El porqué se ve en el 13 (punteros).
- **`const`** en el parámetro promete que la función **no** lo modifica. Si lo
  intenta, el compilador da error. Ponelo siempre que solo leas.

#### Copiar y comparar
`b = a;` **no compila** con arrays, y `a == b` no compara el contenido (compara
dónde están). Para copiar o comparar, se recorre elemento por elemento.

#### Arrays a medio llenar
Muchas veces no se sabe cuántos datos van a llegar. Se reserva una
**capacidad** fija y se lleva aparte la **cantidad** usada:
```c
int botin[CAPACIDAD];
int cantidad = 0;
...
if (cantidad < CAPACIDAD) {
    botin[cantidad] = moneda;       /* el primer lugar libre */
    cantidad++;
}
```
Después se recorre hasta `cantidad`, no hasta `CAPACIDAD`. Es el mismo patrón que
usan el inventario, la lista de enemigos o el cofre del 15. (En el 18 el array va
a poder crecer.)

#### Matrices
Una matriz es un **array de arrays**: filas y columnas.
```c
int mapa[FILAS][COLUMNAS];
mapa[2][1] = 2;                    /* fila 2, columna 1 */
```
- Se recorre con dos `for` anidados: el de afuera por las filas y el de adentro
  por las columnas.
- Para pasarla a una función, hay que decir cuántas **columnas** tiene:
  `void dibujar_mapa(int mapa[][COLUMNAS], int filas)`.
- Detalle de C11: con matrices, no pongas `const` en el parámetro. Pasarle una
  matriz común a un parámetro `const int m[][N]` da una advertencia con
  `-Wpedantic` (se arregló recién en C23).

#### Salirse del array
**C no controla los índices.** `durezas[5]` en un array de 5 lee (o escribe) la
memoria que está justo después, que pertenece a otra cosa. No hay error ni
aviso: el programa sigue con un valor basura o, si escribe, rompe otra variable.
Es el **Orco** del bestiario en C, y la única forma de atraparlo es con los
sanitizadores (`make asan`).

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`
  - Con los detectores de memoria, solo en Linux: agregá `-g -fsanitize=address`. En Windows (MinGW) no existe: usá `-fsanitize=undefined`.

### Código de ejemplo

```c
/*
 * 10 - Arrays y matrices: declarar, recorrer, pasarlos a funciones,
 * arrays a medio llenar y matrices (tablas de filas y columnas).
 *
 *   make run
 */
#include <stdio.h>

#define FILAS    4
#define COLUMNAS 7
#define CAPACIDAD_BOTIN 5

void mostrar(const int valores[], int n);
int  sumar(const int valores[], int n);
int  posicion_del_maximo(const int valores[], int n);
void templar_todo(int valores[], int n, int extra);
void dibujar_mapa(int mapa[][COLUMNAS], int filas);
int  contar(int mapa[][COLUMNAS], int filas, int buscado);

int main(void)
{
    /* --- Declarar e inicializar --- */
    int durezas[5] = { 42, 17, 99, 8, 55 };        /* 5 enteros seguidos en memoria */
    int n = sizeof(durezas) / sizeof(durezas[0]);  /* bytes totales / bytes de uno = 5 */
    printf("El array ocupa %zu bytes: %d elementos de %zu bytes.\n",
           sizeof(durezas), n, sizeof(durezas[0]));

    printf("primero: %d   último: %d\n", durezas[0], durezas[n - 1]);
    durezas[1] = 20;                                /* se cambia como cualquier variable */

    int ceros[4] = { 0 };                           /* los que faltan quedan en 0 */
    int pocos[4] = { 7, 3 };                        /* 7 3 0 0 */
    printf("ceros: ");
    mostrar(ceros, 4);
    printf("pocos: ");
    mostrar(pocos, 4);

    /* --- Recorrer con funciones --- */
    printf("durezas: ");
    mostrar(durezas, n);
    int total = sumar(durezas, n);
    int pos = posicion_del_maximo(durezas, n);
    printf("suma %d, promedio %.1f, la más dura es la %d (%d)\n",
           total, (double) total / n, pos, durezas[pos]);

    /* --- Un array NO se copia al pasarlo: la funcion cambia el original --- */
    templar_todo(durezas, n, 5);
    printf("después de templar_todo: ");
    mostrar(durezas, n);

    /* --- Copiar un array: elemento por elemento (con = no se puede) --- */
    int copia[5];
    for (int i = 0; i < n; i++) {
        copia[i] = durezas[i];
    }
    copia[0] = 0;
    printf("copia con el primero en 0: ");
    mostrar(copia, n);
    printf("el original sigue igual:   ");
    mostrar(durezas, n);

    /* --- Array a medio llenar: capacidad fija, cantidad que cambia --- */
    int botin[CAPACIDAD_BOTIN];
    int cantidad = 0;
    int hallazgos[] = { 12, 30, 5, 18, 40, 25, 9 };   /* sin tamano: lo cuenta el compilador */
    int total_hallazgos = sizeof(hallazgos) / sizeof(hallazgos[0]);
    for (int i = 0; i < total_hallazgos; i++) {
        if (cantidad == CAPACIDAD_BOTIN) {
            printf("el cofre está lleno: quedan %d monedas afuera\n", hallazgos[i]);
            continue;
        }
        botin[cantidad] = hallazgos[i];
        cantidad++;
    }
    printf("botín (%d de %d lugares): ", cantidad, CAPACIDAD_BOTIN);
    mostrar(botin, cantidad);

    /* --- Matriz: FILAS x COLUMNAS. 0 = piso, 1 = pared, 2 = tesoro --- */
    int mapa[FILAS][COLUMNAS] = {
        { 1, 1, 1, 1, 1, 1, 1 },
        { 1, 0, 0, 2, 0, 0, 1 },
        { 1, 0, 1, 1, 0, 2, 1 },
        { 1, 1, 1, 1, 1, 1, 1 },
    };
    mapa[2][1] = 2;                                 /* fila 2, columna 1 */
    printf("\nMapa de la galería (%d x %d):\n", FILAS, COLUMNAS);
    dibujar_mapa(mapa, FILAS);
    printf("paredes: %d   tesoros: %d\n",
           contar(mapa, FILAS, 1), contar(mapa, FILAS, 2));
    return 0;
}

/* const: la funcion promete no modificar el array */
void mostrar(const int valores[], int n)
{
    for (int i = 0; i < n; i++) {
        printf("%d ", valores[i]);
    }
    printf("\n");
}

int sumar(const int valores[], int n)
{
    int suma = 0;
    for (int i = 0; i < n; i++) {
        suma += valores[i];
    }
    return suma;
}

int posicion_del_maximo(const int valores[], int n)
{
    int mejor = 0;                                  /* supongo que el primero es el mayor */
    for (int i = 1; i < n; i++) {
        if (valores[i] > valores[mejor]) {
            mejor = i;
        }
    }
    return mejor;
}

/* Sin const: esta funcion SI modifica el array de quien la llama */
void templar_todo(int valores[], int n, int extra)
{
    for (int i = 0; i < n; i++) {
        valores[i] += extra;
    }
}

/* En una matriz hay que indicar cuantas COLUMNAS tiene (las filas se pasan aparte).
   Sin const: en C11, pasar una matriz a un parametro const da una advertencia. */
void dibujar_mapa(int mapa[][COLUMNAS], int filas)
{
    for (int f = 0; f < filas; f++) {
        printf("  ");
        for (int c = 0; c < COLUMNAS; c++) {
            char simbolo = '.';
            if (mapa[f][c] == 1) {
                simbolo = '#';
            } else if (mapa[f][c] == 2) {
                simbolo = '$';
            }
            printf("%c", simbolo);
        }
        printf("\n");
    }
}

int contar(int mapa[][COLUMNAS], int filas, int buscado)
{
    int cuenta = 0;
    for (int f = 0; f < filas; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            if (mapa[f][c] == buscado) {
                cuenta++;
            }
        }
    }
    return cuenta;
}
```

### Salida esperada

```
El array ocupa 20 bytes: 5 elementos de 4 bytes.
primero: 42   último: 55
ceros: 0 0 0 0 
pocos: 7 3 0 0 
durezas: 42 20 99 8 55 
suma 224, promedio 44.8, la más dura es la 2 (99)
después de templar_todo: 47 25 104 13 60 
copia con el primero en 0: 0 25 104 13 60 
el original sigue igual:   47 25 104 13 60 
el cofre está lleno: quedan 25 monedas afuera
el cofre está lleno: quedan 9 monedas afuera
botín (5 de 5 lugares): 12 30 5 18 40 

Mapa de la galería (4 x 7):
  #######
  #..$..#
  #$##.$#
  #######
paredes: 20   tesoros: 3
```

### ¿Para qué sirve?

Un array es la estructura más usada de la programación: las muestras de audio de una canción, los píxeles de una imagen (una matriz), las notas de un curso, el tablero de un juego. En C, además, no hay red de seguridad: leer fuera del array no da error, lee memoria ajena. Muchas fallas de seguridad famosas empezaron exactamente así, y por eso aprender a respetar los límites es tan importante.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Orco: uno de más.** `for (int i = 0; i <= 5; i++)` sobre un array de 5. Sin
sanitizadores, el programa **no avisa**: muestra un número cualquiera y sigue.
```
1
2
3
4
5
32765
```
Con `make asan` sí se atrapa, y el informe dice la línea y la variable:
```
==994818==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x72212e200034 ...
READ of size 4 at 0x72212e200034 thread T0
    #0 0x563b1007c466 in main a1.c:6
  This frame has 1 object(s):
    [32, 52) 'vida' (line 4) <== Memory access at offset 52 overflows this variable
```
Si el índice es una constante y se compila con optimización (`-O2`), a veces
`gcc` lo ve venir:
```
a4.c:4:16: warning: array subscript 5 is above array bounds of ‘int[5]’ [-Warray-bounds=]
    4 |     return vida[5];
      |            ~~~~^~~
```

**Goblin: `sizeof` dentro de la función.** Da el tamaño de una dirección, no el
del array:
```
a2.c:4:18: warning: ‘sizeof’ on array function parameter ‘v’ will return size of ‘int *’ [-Wsizeof-array-argument]
    4 |     return sizeof(v) / sizeof(v[0]);
      |                  ^
```

**Goblin: copiar con `=`.**
```
a2.c:10:7: error: assignment to expression with array type
   10 |     b = a;
      |       ^
```

**Slime: más valores que lugares.**
```
a3.c:3:36: warning: excess elements in array initializer
    3 |     int vida[5] = { 1, 2, 3, 4, 5, 6 };
      |                                    ^
```

**Ogro: el array sin inicializar.** `int suma[5];` y después `suma[i] += x`:
empieza con basura. Inicializalo con `= { 0 }`.

### Misión R02-N01-M1 · Las temperaturas del horno

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé hasta 10 temperaturas (una por línea;
`fin` termina antes) validando cada una. Mostrá la mayor, la menor, el
promedio y cuántas lo superan.

#### Criterio de aprobación

- Lee hasta 10 temperaturas validando cada una; `fin` termina antes.
- Muestra la mayor, la menor, el promedio y cuántas lo superan.
- Nunca escribe fuera del array.

#### Entrada de ejemplo

```
850
920
mucho
1100
-5
760
980
fin
```

#### Salida esperada

```
Temperatura 1 (o "fin"): Temperatura 2 (o "fin"): Temperatura 3 (o "fin"):   no es una temperatura válida.
Temperatura 3 (o "fin"): Temperatura 4 (o "fin"):   no es una temperatura válida.
Temperatura 4 (o "fin"): Temperatura 5 (o "fin"): Temperatura 6 (o "fin"): 
5 temperaturas: mayor 1100, menor 760, promedio 922.0
2 superan el promedio
```

#### Solución de referencia

```c
/*
 * Mision 1 - Las temperaturas del horno: leer hasta 10 temperaturas (una por
 * linea, "fin" para terminar) y mostrar la mayor, la menor, el promedio y
 * cuantas superan el promedio.
 * Probar con:  ./sol < mision1_horno.entrada.txt
 */
#include <stdio.h>

#define MAXIMO 10

int main(void)
{
    int temperaturas[MAXIMO];
    int cantidad = 0;
    char linea[100];

    while (cantidad < MAXIMO) {
        printf("Temperatura %d (o \"fin\"): ", cantidad + 1);
        if (fgets(linea, sizeof(linea), stdin) == NULL || linea[0] == 'f') {
            break;
        }
        int t;
        char sobra;
        if (sscanf(linea, "%d %c", &t, &sobra) != 1 || t < 0) {
            printf("  no es una temperatura válida.\n");
            continue;
        }
        temperaturas[cantidad] = t;
        cantidad++;
    }
    printf("\n");

    if (cantidad == 0) {
        printf("No se cargó ninguna temperatura.\n");
        return 0;
    }

    int mayor = temperaturas[0];
    int menor = temperaturas[0];
    int suma = 0;
    for (int i = 0; i < cantidad; i++) {
        suma += temperaturas[i];
        if (temperaturas[i] > mayor) {
            mayor = temperaturas[i];
        }
        if (temperaturas[i] < menor) {
            menor = temperaturas[i];
        }
    }
    double promedio = (double) suma / cantidad;

    int arriba = 0;
    for (int i = 0; i < cantidad; i++) {
        if (temperaturas[i] > promedio) {
            arriba++;
        }
    }
    printf("%d temperaturas: mayor %d, menor %d, promedio %.1f\n",
           cantidad, mayor, menor, promedio);
    printf("%d superan el promedio\n", arriba);
    return 0;
}
```

#### Pruebas

##### Diez temperaturas
```entrada
100
200
300
400
500
600
700
800
900
1000
```
```salida
Temperatura 1 (o "fin"): Temperatura 2 (o "fin"): Temperatura 3 (o "fin"): Temperatura 4 (o "fin"): Temperatura 5 (o "fin"): Temperatura 6 (o "fin"): Temperatura 7 (o "fin"): Temperatura 8 (o "fin"): Temperatura 9 (o "fin"): Temperatura 10 (o "fin"):
10 temperaturas: mayor 1000, menor 100, promedio 550.0
5 superan el promedio
```

##### Ninguna válida
```entrada
-1
mucho
fin
```
```salida
Temperatura 1 (o "fin"):   no es una temperatura válida.
Temperatura 1 (o "fin"):   no es una temperatura válida.
Temperatura 1 (o "fin"):
No se cargó ninguna temperatura.
```

##### Una sola
```entrada
500
fin
```
```salida
Temperatura 1 (o "fin"): Temperatura 2 (o "fin"):
1 temperaturas: mayor 500, menor 500, promedio 500.0
0 superan el promedio
```

### Misión R02-N01-M2 · El espejo de la Forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `invertir(v, n)` (da vuelta el array sin
usar otro), `buscar(v, n, valor)` (posición o `-1`) y `rotar_izquierda(v, n)`
(el primero pasa al final).

#### Criterio de aprobación

- `invertir` da vuelta el array sin usar otro.
- `buscar` devuelve la posición o `-1`.
- `rotar_izquierda` pasa el primero al final.
- Cada función recibe el array y su cantidad.

#### Salida esperada

```
original:  3 1 4 1 5 9 2 
invertido: 2 9 5 1 4 1 3 
el 5 está en la posición 2; el 7, en la -1
rotado:    9 5 1 4 1 3 2 
```

#### Solución de referencia

```c
/*
 * Mision 2 - El espejo de la Forja: funciones que trabajan sobre arrays.
 *   invertir:        da vuelta el array en el lugar (sin otro array)
 *   buscar:          posicion del valor, o -1 si no esta
 *   rotar_izquierda: el primero pasa al final
 */
#include <stdio.h>

void mostrar(const int v[], int n);
void invertir(int v[], int n);
int  buscar(const int v[], int n, int buscado);
void rotar_izquierda(int v[], int n);

int main(void)
{
    int runas[] = { 3, 1, 4, 1, 5, 9, 2 };
    int n = sizeof(runas) / sizeof(runas[0]);

    printf("original:  ");
    mostrar(runas, n);
    invertir(runas, n);
    printf("invertido: ");
    mostrar(runas, n);
    printf("el 5 está en la posición %d; el 7, en la %d\n",
           buscar(runas, n, 5), buscar(runas, n, 7));
    rotar_izquierda(runas, n);
    printf("rotado:    ");
    mostrar(runas, n);
    return 0;
}

void mostrar(const int v[], int n)
{
    for (int i = 0; i < n; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");
}

void invertir(int v[], int n)
{
    for (int i = 0; i < n / 2; i++) {          /* solo hasta la mitad */
        int tmp = v[i];
        v[i] = v[n - 1 - i];
        v[n - 1 - i] = tmp;
    }
}

int buscar(const int v[], int n, int buscado)
{
    for (int i = 0; i < n; i++) {
        if (v[i] == buscado) {
            return i;
        }
    }
    return -1;
}

void rotar_izquierda(int v[], int n)
{
    if (n == 0) {
        return;
    }
    int primero = v[0];
    for (int i = 0; i < n - 1; i++) {
        v[i] = v[i + 1];
    }
    v[n - 1] = primero;
}
```

### Misión R02-N01-M3 · El mapa de la mina

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una matriz de 5 × 8 con paredes y tesoros. Kira
empieza en la fila 1, columna 1, y se mueve con `w`/`a`/`s`/`d` (una letra por
línea; `q` termina). Las paredes no la dejan pasar y los tesoros se juntan.
Al final, dibujá el mapa con Kira como `K`.

#### Criterio de aprobación

- Usa una matriz de 5 × 8 para el mapa.
- Las paredes frenan el movimiento y los tesoros se juntan.
- Al terminar dibuja el mapa con `K` en la posición final.

#### Entrada de ejemplo

```
d
d
d
s
d
d
w
d
x
s
a
s
s
d
q
```

#### Salida esperada

```
########
#K.$#.$#
#.#...##
#$#.#.$#
########
Movimiento (w/a/s/d, q para salir): 
Movimiento: 
  ¡tesoro! (llevás 1)
Movimiento: 
  ¡pared!
Movimiento: 
Movimiento: 
Movimiento: 
Movimiento: 
Movimiento: 
  ¡tesoro! (llevás 2)
Movimiento: 
  movimiento desconocido
Movimiento: 
  ¡pared!
Movimiento: 
Movimiento: 
Movimiento: 
Movimiento: 
  ¡tesoro! (llevás 3)
Movimiento: 
########
#...#..#
#.#...##
#$#.#.K#
########
Kira juntó 3 tesoros.
```

#### Solución de referencia

```c
/*
 * Mision 3 - El mapa de la mina: Kira se mueve por una matriz con w/a/s/d
 * (una letra por linea). Las paredes no la dejan pasar y junta los tesoros.
 * Probar con:  ./sol < mision3_mina.entrada.txt
 */
#include <stdio.h>

#define FILAS    5
#define COLUMNAS 8

void dibujar(int mapa[][COLUMNAS], int fila_kira, int col_kira);

int main(void)
{
    /* 0 = piso, 1 = pared, 2 = tesoro */
    int mapa[FILAS][COLUMNAS] = {
        { 1, 1, 1, 1, 1, 1, 1, 1 },
        { 1, 0, 0, 2, 1, 0, 2, 1 },
        { 1, 0, 1, 0, 0, 0, 1, 1 },
        { 1, 2, 1, 0, 1, 0, 2, 1 },
        { 1, 1, 1, 1, 1, 1, 1, 1 },
    };
    int fila = 1, col = 1;
    int tesoros = 0;
    char linea[100];

    dibujar(mapa, fila, col);
    printf("Movimiento (w/a/s/d, q para salir): ");
    while (fgets(linea, sizeof(linea), stdin) != NULL && linea[0] != 'q') {
        int nueva_fila = fila, nueva_col = col;
        switch (linea[0]) {
            case 'w': nueva_fila--; break;
            case 's': nueva_fila++; break;
            case 'a': nueva_col--;  break;
            case 'd': nueva_col++;  break;
            default:
                printf("\n  movimiento desconocido\n");
                printf("Movimiento: ");
                continue;
        }
        if (mapa[nueva_fila][nueva_col] == 1) {
            printf("\n  ¡pared!\n");
        } else {
            fila = nueva_fila;
            col = nueva_col;
            if (mapa[fila][col] == 2) {
                tesoros++;
                mapa[fila][col] = 0;
                printf("\n  ¡tesoro! (llevás %d)\n", tesoros);
            } else {
                printf("\n");
            }
        }
        printf("Movimiento: ");
    }
    printf("\n");
    dibujar(mapa, fila, col);
    printf("Kira juntó %d tesoros.\n", tesoros);
    return 0;
}

void dibujar(int mapa[][COLUMNAS], int fila_kira, int col_kira)
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            char simbolo = '.';
            if (f == fila_kira && c == col_kira) {
                simbolo = 'K';
            } else if (mapa[f][c] == 1) {
                simbolo = '#';
            } else if (mapa[f][c] == 2) {
                simbolo = '$';
            }
            printf("%c", simbolo);
        }
        printf("\n");
    }
}
```

#### Pruebas

##### Sale enseguida
```entrada
q
```
```salida
########
#K.$#.$#
#.#...##
#$#.#.$#
########
Movimiento (w/a/s/d, q para salir):
########
#K.$#.$#
#.#...##
#$#.#.$#
########
Kira juntó 0 tesoros.
```

##### Contra la pared
```entrada
w
a
a
q
```
```salida
########
#K.$#.$#
#.#...##
#$#.#.$#
########
Movimiento (w/a/s/d, q para salir):
  ¡pared!
Movimiento:
  ¡pared!
Movimiento:
  ¡pared!
Movimiento:
########
#K.$#.$#
#.#...##
#$#.#.$#
########
Kira juntó 0 tesoros.
```

##### Junta todos los tesoros que puede
```entrada
d
d
s
s
d
d
w
w
d
d
d
s
s
q
```
```salida
########
#K.$#.$#
#.#...##
#$#.#.$#
########
Movimiento (w/a/s/d, q para salir):
Movimiento:
  ¡tesoro! (llevás 1)
Movimiento:
Movimiento:
Movimiento:
  ¡pared!
Movimiento:
  ¡pared!
Movimiento:
Movimiento:
Movimiento:
  ¡pared!
Movimiento:
  ¡pared!
Movimiento:
  ¡pared!
Movimiento:
Movimiento:
Movimiento:
########
#...#.$#
#.#...##
#$#K#.$#
########
Kira juntó 1 tesoros.
```

### Encargo R02-N01-E1 · Las notas de la escuela

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La escuela del Gremio guarda las notas de **5 alumnos en 3 parciales** en una
matriz. Mostrá una tabla con las notas y el promedio de cada alumno
(aprueba con 6 o más), el promedio de cada parcial y cuántos aprobaron.

#### Criterio de aprobación

- Guarda las notas en una matriz de 5 × 3.
- Muestra el promedio de cada alumno y si aprueba (6 o más).
- Muestra el promedio de cada parcial y cuántos aprobaron.

#### Salida esperada

```
Alumno   P1  P2  P3   Promedio
  1       7   8   6    7.00  aprobado
  2       4   5   6    5.00  desaprobado
  3       9  10   8    9.00  aprobado
  4       6   4   7    5.67  desaprobado
  5       3   6   5    4.67  desaprobado
Prom.     5.8 6.6 6.4
Aprobaron 2 de 5.
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - Las notas del curso: 5 alumnos x 3 parciales en una
 * matriz. Promedio de cada alumno (aprueba con 6 o mas) y de cada parcial.
 */
#include <stdio.h>

#define ALUMNOS   5
#define PARCIALES 3

double promedio_alumno(int notas[][PARCIALES], int alumno);
double promedio_parcial(int notas[][PARCIALES], int alumnos, int parcial);

int main(void)
{
    int notas[ALUMNOS][PARCIALES] = {
        { 7, 8, 6 },
        { 4, 5, 6 },
        { 9, 10, 8 },
        { 6, 4, 7 },
        { 3, 6, 5 },
    };

    printf("Alumno   P1  P2  P3   Promedio\n");
    int aprobados = 0;
    for (int a = 0; a < ALUMNOS; a++) {
        printf("  %d    ", a + 1);
        for (int p = 0; p < PARCIALES; p++) {
            printf("%4d", notas[a][p]);
        }
        double prom = promedio_alumno(notas, a);
        printf("   %5.2f  %s\n", prom, prom >= 6 ? "aprobado" : "desaprobado");
        if (prom >= 6) {
            aprobados++;
        }
    }
    printf("Prom.    ");
    for (int p = 0; p < PARCIALES; p++) {
        printf("%4.1f", promedio_parcial(notas, ALUMNOS, p));
    }
    printf("\nAprobaron %d de %d.\n", aprobados, ALUMNOS);
    return 0;
}

double promedio_alumno(int notas[][PARCIALES], int alumno)
{
    int suma = 0;
    for (int p = 0; p < PARCIALES; p++) {
        suma += notas[alumno][p];
    }
    return (double) suma / PARCIALES;
}

double promedio_parcial(int notas[][PARCIALES], int alumnos, int parcial)
{
    int suma = 0;
    for (int a = 0; a < alumnos; a++) {
        suma += notas[a][parcial];
    }
    return (double) suma / alumnos;
}
```

### Prueba del sello

#### ¿Cuál es el último índice válido de `int a[8]`?

`7`.

#### ¿Qué contiene `int a[5] = { 4 };`?

`{4, 0, 0, 0, 0}`: los que no se nombran quedan en 0.

#### ¿Por qué una función que recibe un array necesita también su cantidad?

Porque el array llega como una dirección y no sabe cuántos elementos tiene.

#### Si una función hace `v[0] = 99` sobre el array que recibió, ¿cambia el original? ¿Y si recibe un `int` y hace `x = 99`?

Sí: el array no se copia, la función trabaja sobre el original. Con un `int` no: recibe una copia.

#### ¿Qué pasa al leer `a[10]` en un array de 10? ¿Cómo se detecta?

Es **comportamiento indefinido**: lee memoria que no es del array (basura, o se corta el programa). Se detecta con `-fsanitize=address` (`make asan`).

#### ¿Qué diferencia hay entre la capacidad y la cantidad de un array?

La capacidad es cuántos elementos entran (el tamaño declarado); la cantidad, cuántos se usan de verdad.

### Soluciones (docente)

Material original: `01-C/10-Arrays` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R02-N02 · Strings (textos)

```meta
tipo: tema
criatura: orco
padre: R02-N01
precio: 10
temas: prog.cadenas
usa: col.arrays
```

### Crónica

En la pared del pasillo, cada cajón tiene una placa con su nombre, letra por letra en casilleros de hierro. Notás que después de la última letra siempre hay un casillero con un **tapón**.

—Sin el tapón —explica {mentor}—, el que lee sigue de largo por los casilleros de al lado, y termina leyendo el nombre del vecino… o algo peor.

### Objetivos

Entender que en C un texto es un **array de `char` terminado en `'\0'`**. Usar
`<string.h>` para medir, comparar y buscar; copiar y armar textos **sin
desbordarlos** con `snprintf`; convertir entre textos y números; guardar listas
de textos, y saber por qué las letras con tilde ocupan más de un byte.

### Antes de empezar

- Arrays y cómo se pasan a funciones (10).
- `char` como número pequeño (02); `fgets` + `sscanf` (05); `ctype.h` (09).
- Operadores de bits `&` (04), para la parte de UTF-8.

### Explicación

#### Un texto es un array de `char` con tapón
```c
char nombre[16] = "Kira";
```
```
índice:  [0] [1] [2] [3] [4]  [5] ... [15]
         'K' 'i' 'r' 'a' '\0' (sin usar)
```
- El `'\0'` (el carácter de código 0) marca **dónde termina** el texto. Las
  comillas dobles lo agregan solas: `"Kira"` ocupa **5** bytes.
- `strlen(nombre)` cuenta los bytes **antes** del `'\0'`: 4. `sizeof(nombre)`
  es el tamaño del array: 16. (Los dos son `size_t`, que se muestra con `%zu`.)
- Por eso, en un `char x[N]` entran como máximo **N-1** letras.
- `'K'` (comillas simples) es **un** carácter; `"K"` (dobles) es un texto de
  dos bytes: `'K'` y `'\0'`.

#### Recorrer un texto
No hace falta la cantidad: se avanza hasta encontrar el tapón.
```c
for (int i = 0; texto[i] != '\0'; i++) { ... }
```
Una función que recibe un texto lo declara `const char texto[]` si solo lo lee,
o `char texto[]` si lo modifica. `const char *texto` (lo que se usó en el 08)
significa lo mismo; el `*` se explica en el 13.

#### Textos fijos y listas de textos
```c
const char *correo = "kira@forja.cx";               /* un texto fijo, que no se modifica */
const char *oficios[] = { "guerrera", "herrero" };  /* una lista de textos fijos */
char compania[4][8] = { "Kira", "Tizon", "Hulda", "Chispa" };  /* 4 textos de hasta 7 letras */
```
- Un `const char *` **no se puede modificar**: sirve para nombres, mensajes y
  opciones que no cambian.
- Una matriz de `char` (`compania`) es un array de textos **modificables**, cada
  uno con su tamaño máximo. `compania[1]` es `"Tizón"` y `compania[1][0]` es
  `'B'`.

#### `<string.h>`: lo básico
| Función | Qué hace |
|---|---|
| `strlen(s)` | largo en bytes, sin contar el `'\0'` |
| `strcmp(a, b)` | compara: **0** si son iguales, **negativo** si `a` va antes en orden alfabético, **positivo** si va después |
| `strncmp(a, b, n)` | igual, pero solo los primeros `n` (sirve para "¿empieza con…?") |
| `strcspn(s, "abc")` | posición del primer carácter de `s` que sea `a`, `b` o `c` (o el largo, si no hay ninguno) |
| `strchr(s, 'x')` / `strstr(s, "xy")` | buscan una letra / un texto; devuelven **`NULL`** si no está |

`strchr` y `strstr` devuelven **dónde** lo encontraron (un puntero, 13). Por
ahora alcanza con compararlos con `NULL` para saber si está o no.

#### Copiar y armar textos: `snprintf`
Un texto **no se asigna con `=`** (es un array, 10). Para copiar o armar un
texto se usa `snprintf`, que funciona como `printf` pero escribe en un array:
```c
snprintf(copia, sizeof(copia), "%s", nombre);             /* copiar */
snprintf(saludo, sizeof(saludo), "¡Hola, %s!", nombre);   /* armar */
snprintf(etiqueta, sizeof(etiqueta), "Espada +%d", 3);    /* número -> texto */
```
- **Nunca escribe más de `sizeof(destino)`** y siempre pone el `'\0'`. Si el
  texto no entra, lo **corta**.
- Devuelve cuántos bytes **habría** necesitado (sin el `'\0'`). Si es mayor o
  igual que el tamaño, se cortó: `if (necesita >= (int) sizeof(chico))`.

En libros y código viejo vas a ver `strcpy(destino, origen)` y
`strcat(destino, origen)`: copian y agregan **sin mirar el tamaño** del destino.
Si no entra, escriben fuera del array (ver el bestiario). `strncpy` parece la
versión segura pero tiene trampa: si el texto no entra, **no pone el `'\0'`**. En
este curso se usa `snprintf`.

#### Texto → número
`sscanf` (05) también sirve para **desarmar** un texto con formato conocido:
```c
sscanf("ataque=18 peso=4.5", "ataque=%d peso=%lf", &ataque, &peso);  /* devuelve 2 */
sscanf(linea, "%23[^;];%d", nombre, &nivel);   /* "Kira;7" -> "Kira" y 7 */
```
- Los caracteres del formato que no son `%` (como `ataque=`) tienen que
  aparecer tal cual en el texto.
- **`%23[^;]`** lee un texto **hasta el próximo `;`** (`[^;]` es "cualquier cosa
  menos `;`"), de hasta 23 letras. El número es `sizeof - 1`: deja lugar para el
  `'\0'`. Los textos van **sin `&`**: el nombre de un array ya indica dónde
  guardar (13).
- `atoi("42")` también convierte, pero si el texto no es un número devuelve
  `0` **sin avisar**: no se puede distinguir `"0"` de `"hola"`. Mejor `sscanf`.

#### Sacarle el Enter a lo que leyó `fgets`
La receta del 05, ahora completa:
```c
recluta[strcspn(recluta, "\n")] = '\0';
```
`strcspn` da la posición del `'\n'` (o el largo, si no había), y en esa posición
se pone el tapón: el texto termina ahí.

#### Tildes: letras de más de un byte
Los archivos del curso están en **UTF-8**: las letras comunes ocupan 1 byte,
pero `á`, `ñ`, `¡` o `°` ocupan **2**.
- `strlen("herrería")` es **9**, aunque tenga 8 letras.
- `printf("%-10s")` cuenta bytes: con tildes, la columna queda corrida.
- `toupper` e `isalpha` solo entienden letras sin tilde.
- Si `snprintf` corta un texto justo en el medio de una letra de 2 bytes, queda
  medio carácter (se ve como `�`).

Para **contar letras**: en UTF-8, los bytes que **continúan** una letra empiezan
con los bits `10` (`10xxxxxx`). Con la máscara del 04, `(c & 0xC0) != 0x80`
es verdadero solo para los bytes que **empiezan** una letra.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo (la entrada de ejemplo ya está en la pestaña **Entrada**).
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**; las respuestas se escriben en la consola.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`
  - Con las respuestas en un archivo: `./programa < main.entrada.txt` (Linux) o `programa.exe < main.entrada.txt` (Windows).

### Código de ejemplo

```c
/*
 * 11 - Strings: arrays de char terminados en '\0', <string.h> con sus
 * versiones seguras, texto <-> numero, arrays de textos y tildes en UTF-8.
 *
 *   make run
 *   ./programa < main.entrada.txt
 */
#include <stdio.h>
#include <string.h>    /* strlen, strcmp, strncmp, strcspn, strchr, strstr */
#include <ctype.h>     /* toupper */

void mostrar_bytes(const char texto[]);
void a_mayusculas(char texto[]);
int  contar_letras_utf8(const char texto[]);

int main(void)
{
    /* --- Un texto es un array de char que termina en '\0' --- */
    char nombre[16] = "Kira";                       /* K i r a \0 y 11 lugares libres */
    printf("\"%s\": strlen = %zu, sizeof = %zu bytes\n",
           nombre, strlen(nombre), sizeof(nombre));
    mostrar_bytes(nombre);

    /* --- Copiar y armar textos con snprintf: nunca se pasa del tamano --- */
    char copia[16];
    snprintf(copia, sizeof(copia), "%s", nombre);   /* copiar */
    char saludo[40];
    snprintf(saludo, sizeof(saludo), "¡Hola, %s! Nivel %d.", nombre, 7);
    printf("copia: %s | saludo: %s\n", copia, saludo);

    /* Si no entra, snprintf corta el texto y devuelve cuanto HABRIA ocupado */
    char chico[8];
    int necesita = snprintf(chico, sizeof(chico), "%s", saludo);
    if (necesita >= (int) sizeof(chico)) {
        printf("en 8 bytes solo entra \"%s\" (hacían falta %d bytes + el \\0)\n",
               chico, necesita);
    }

    /* --- Comparar: strcmp devuelve 0 si son iguales --- */
    printf("strcmp(\"Kira\", \"Kira\") = %d\n", strcmp(nombre, "Kira"));
    printf("\"Tizon\" va %s de \"Kira\" en el diccionario\n",
           strcmp("Tizon", "Kira") < 0 ? "antes" : "después");
    printf("¿\"Maese Ferrum\" empieza con \"Maese\"? %s\n",
           strncmp("Maese Ferrum", "Maese", 5) == 0 ? "sí" : "no");

    /* --- Buscar --- */
    const char *correo = "kira@forja.cx";
    size_t arroba = strcspn(correo, "@");           /* posicion del primer '@' */
    printf("el @ está en la posición %zu; ", arroba);
    printf("¿tiene \"forja\"? %s; ", strstr(correo, "forja") != NULL ? "sí" : "no");
    printf("¿tiene '#'? %s\n", strchr(correo, '#') != NULL ? "sí" : "no");

    /* --- Recorrer y modificar letra por letra --- */
    char grito[16];
    snprintf(grito, sizeof(grito), "%s", nombre);
    a_mayusculas(grito);
    printf("en mayúsculas: %s (el original: %s)\n", grito, nombre);

    /* --- Numero -> texto y texto -> numero --- */
    char etiqueta[24];
    snprintf(etiqueta, sizeof(etiqueta), "Espada +%d (%.1f kg)", 3, 2.5);
    printf("etiqueta: %s\n", etiqueta);
    int ataque = 0;
    double peso = 0;
    if (sscanf("ataque=18 peso=4.5", "ataque=%d peso=%lf", &ataque, &peso) == 2) {
        printf("leído del texto: ataque %d, peso %.1f\n", ataque, peso);
    }

    /* --- Leer una linea y sacarle el Enter --- */
    char recluta[32];
    printf("¿Cómo se llama el nuevo aprendiz? ");
    if (fgets(recluta, sizeof(recluta), stdin) == NULL) {
        recluta[0] = '\0';                          /* sin entrada: texto vacio */
    }
    recluta[strcspn(recluta, "\n")] = '\0';         /* pisa el '\n' con el fin de texto */
    printf("\nBienvenido, %s (strlen %zu)\n", recluta, strlen(recluta));

    /* --- Arrays de textos --- */
    char compania[4][8] = { "Kira", "Tizon", "Hulda", "Chispa" };  /* 4 textos de hasta 7 letras */
    const char *oficios[] = { "guerrera", "herrero", "minera", "mercader" };  /* textos fijos */
    for (int i = 0; i < 4; i++) {
        printf("  %-5s %s\n", compania[i], oficios[i]);
    }

    /* --- Tildes: en UTF-8 una letra puede ocupar mas de un byte --- */
    const char *palabra = "herrería";
    printf("\"%s\": strlen = %zu bytes, pero tiene %d letras\n",
           palabra, strlen(palabra), contar_letras_utf8(palabra));
    printf("[%-10s] [%-10s]  <- las dos con ancho 10: una queda corrida\n", "herrero", "herrería");
    return 0;
}

/* Muestra cada byte del texto, incluido el '\0' final */
void mostrar_bytes(const char texto[])
{
    printf("  en memoria:");
    for (int i = 0; texto[i] != '\0'; i++) {
        printf(" '%c'", texto[i]);
    }
    printf(" '\\0'\n");
}

void a_mayusculas(char texto[])
{
    for (int i = 0; texto[i] != '\0'; i++) {
        texto[i] = (char) toupper((unsigned char) texto[i]);
    }
}

/* En UTF-8, los bytes que CONTINUAN una letra empiezan con los bits 10xxxxxx.
   Contar letras = contar los bytes que no son de continuacion. */
int contar_letras_utf8(const char texto[])
{
    int letras = 0;
    for (int i = 0; texto[i] != '\0'; i++) {
        if ((texto[i] & 0xC0) != 0x80) {
            letras++;
        }
    }
    return letras;
}
```

### Entrada de ejemplo

```
Chispa el Veloz
```

### Salida esperada

```
"Kira": strlen = 4, sizeof = 16 bytes
  en memoria: 'K' 'i' 'r' 'a' '\0'
copia: Kira | saludo: ¡Hola, Kira! Nivel 7.
en 8 bytes solo entra "¡Hola," (hacían falta 22 bytes + el \0)
strcmp("Kira", "Kira") = 0
"Tizon" va después de "Kira" en el diccionario
¿"Maese Ferrum" empieza con "Maese"? sí
el @ está en la posición 4; ¿tiene "forja"? sí; ¿tiene '#'? no
en mayúsculas: KIRA (el original: Kira)
etiqueta: Espada +3 (2.5 kg)
leído del texto: ataque 18, peso 4.5
¿Cómo se llama el nuevo aprendiz?
Bienvenido, Chispa el Veloz (strlen 15)
  Kira  guerrera
  Tizon herrero
  Hulda minera
  Chispa mercader
"herrería": strlen = 9 bytes, pero tiene 8 letras
[herrero   ] [herrería ]  <- las dos con ancho 10: una queda corrida
```

### ¿Para qué sirve?

Casi todos los datos llegan como texto: formularios, archivos CSV, mensajes de red, comandos de un chat. En C, cada texto es un array de caracteres con un `'\0'` al final, y manejarlo con cuidado (sin pasarse del tamaño, validando formatos) es lo que evita los desbordes de buffer, una de las causas más comunes de fallas de seguridad en sistemas reales.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Goblin: asignar un texto con `=`.**
```
s1.c:6:12: error: assignment to expression with array type
    6 |     nombre = "Tizon";
      |            ^
```

**Ogro: comparar textos con `==`.** Compara **dónde están**, no qué dicen:
```
s1.c:7:16: warning: comparison with string literal results in unspecified behavior [-Waddress]
    7 |     if (nombre == "Kira") {
      |                ^~
```
Se compara con `strcmp(nombre, "Kira") == 0`.

**Goblin: comillas dobles para una letra.**
```
s1.c:10:18: warning: initialization of ‘char’ from ‘char *’ makes integer from pointer without a cast [-Wint-conversion]
   10 |     char letra = "K";
      |                  ^~~
```

**Orco: `strcpy` en un array chico.** Compila sin avisos, y con un texto largo
escribe fuera del array. Con `make asan`:
```
==1001557==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ddfc7900038 ...
WRITE of size 26 at 0x7ddfc7900038 thread T0
    #0 0x7ddfc9ca7922 in strcpy ../../../../src/libsanitizer/asan/asan_interceptors.cpp:563
    #1 0x56df279a032e in main s2.c:8
```
Es el error que usan muchos ataques informáticos (*buffer overflow*). Con
`snprintf` no puede pasar.

**Orco: el texto sin tapón.** `strncpy(titulo, "Maese", 4)` copia `Maes` y **no
pone el `'\0'`**; al mostrarlo, `printf` sigue leyendo fuera del array. `gcc` a
veces avisa:
```
s3.c:6:5: warning: ‘strncpy’ output truncated copying 4 bytes from a string of length 5 [-Wstringop-truncation]
```
y `make asan` lo atrapa (`stack-buffer-overflow ... READ of size 5 ... in puts`).

**Goblin: `snprintf` que no entra.** Si `gcc` ve que el texto se va a cortar, avisa:
```
m.c:32:52: warning: ‘%s’ directive output truncated writing 12 bytes into a region of size 8 [-Wformat-truncation=]
```
Agrandá el destino, o chequeá lo que devuelve `snprintf`.

**Ogro: `atoi` que no avisa.** `atoi("hola")` da `0`, igual que `atoi("0")`.

**Ogro: el Enter pegado.** Sin el `strcspn`, `strcmp(nombre, "Kira")` da
distinto: el texto es `"Kira\n"`.

### Misión R02-N02-M1 · El nombre del aprendiz

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí un nombre completo hasta que sea válido (no
vacío, solo letras y espacios). Poné mayúscula al principio de cada palabra y
minúscula en el resto (`kIRA del norte` → `Kira Del Norte`), y mostrá sus
iniciales (`K.D.N.`) en otro texto, sin pasarte de su tamaño.

#### Criterio de aprobación

- Vuelve a pedir el nombre hasta que no esté vacío y tenga solo letras y espacios.
- Pone mayúscula al principio de cada palabra y minúscula en el resto.
- Arma las iniciales en otro texto sin pasarse de su tamaño.

#### Entrada de ejemplo

```

k1ra
kIRA   del norte
```

#### Salida esperada

```
Nombre completo: 
  tiene que tener letras (sin números ni símbolos).
Nombre completo: 
  tiene que tener letras (sin números ni símbolos).
Nombre completo: 
Ficha: Kira   Del Norte (K.D.N.)
```

#### Solución de referencia

```c
/*
 * Mision 1 - El nombre del aprendiz: pedir un nombre hasta que sea valido
 * (no vacio, solo letras y espacios), ponerle mayuscula a cada palabra y
 * mostrar las iniciales.
 * Probar con:  ./sol < mision1_nombre.entrada.txt
 */
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

bool es_valido(const char texto[]);
void capitalizar(char texto[]);
void iniciales(const char texto[], char destino[], int tam);

int main(void)
{
    char nombre[64];
    for (;;) {
        printf("Nombre completo: ");
        if (fgets(nombre, sizeof(nombre), stdin) == NULL) {
            printf("\nSin nombre, no hay ficha.\n");
            return 1;
        }
        nombre[strcspn(nombre, "\n")] = '\0';
        if (es_valido(nombre)) {
            break;
        }
        printf("\n  tiene que tener letras (sin números ni símbolos).\n");
    }
    capitalizar(nombre);
    char ini[16];
    iniciales(nombre, ini, sizeof(ini));
    printf("\nFicha: %s (%s)\n", nombre, ini);
    return 0;
}

/* Valido: solo letras y espacios, y al menos una letra */
bool es_valido(const char texto[])
{
    bool hay_letra = false;
    for (int i = 0; texto[i] != '\0'; i++) {
        unsigned char c = (unsigned char) texto[i];
        if (isalpha(c)) {
            hay_letra = true;
        } else if (c != ' ') {
            return false;
        }
    }
    return hay_letra;
}

/* Mayuscula al principio de cada palabra, el resto en minuscula */
void capitalizar(char texto[])
{
    bool inicio_de_palabra = true;
    for (int i = 0; texto[i] != '\0'; i++) {
        unsigned char c = (unsigned char) texto[i];
        if (c == ' ') {
            inicio_de_palabra = true;
        } else if (inicio_de_palabra) {
            texto[i] = (char) toupper(c);
            inicio_de_palabra = false;
        } else {
            texto[i] = (char) tolower(c);
        }
    }
}

/* "Kira Del Norte" -> "K.D.N." (sin pasarse de tam) */
void iniciales(const char texto[], char destino[], int tam)
{
    int j = 0;
    for (int i = 0; texto[i] != '\0' && j + 2 < tam; i++) {
        if (texto[i] != ' ' && (i == 0 || texto[i - 1] == ' ')) {
            destino[j] = texto[i];
            destino[j + 1] = '.';
            j += 2;
        }
    }
    destino[j] = '\0';                  /* siempre cerrar el texto */
}
```

#### Pruebas

##### Nombre simple
```entrada
ana
```
```salida
Nombre completo:
Ficha: Ana (A.)
```

##### Todo en mayúsculas
```entrada
JUAN PEREZ
```
```salida
Nombre completo:
Ficha: Juan Perez (J.P.)
```

##### Inválidos hasta el final
```entrada
123
!!
```
```salida
Nombre completo:
  tiene que tener letras (sin números ni símbolos).
Nombre completo:
  tiene que tener letras (sin números ni símbolos).
Nombre completo:
Sin nombre, no hay ficha.
```

### Misión R02-N02-M2 · El registro de la Forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé líneas `nombre;nivel;oro` hasta que no haya
más entrada. Mostrá las válidas en columnas y el oro total; las mal formadas
(letras en el nivel, datos de menos o de más, nivel menor que 1) se informan
con su número de línea.

#### Criterio de aprobación

- Separa cada línea `nombre;nivel;oro` y valida los tres datos.
- Muestra las válidas en columnas y el oro total.
- Informa las mal formadas con su número de línea.

#### Entrada de ejemplo

```
Kira;7;350
Tizon;12;1200
Hulda;siete;80
Chispa;5
Ferrum;40;9000
Nadie;0;10
Hulda;6;80x
```

#### Salida esperada

```
Kira       nivel  7    350 de oro
Tizon      nivel 12   1200 de oro
línea 3 inválida: "Hulda;siete;80"
línea 4 inválida: "Chispa;5"
Ferrum     nivel 40   9000 de oro
línea 6 inválida: "Nadie;0;10"
línea 7 inválida: "Hulda;6;80x"
3 registros válidos, 10550 de oro en total
```

#### Solución de referencia

```c
/*
 * Mision 2 - El registro de la Forja: cada linea tiene "nombre;nivel;oro".
 * Se separa con sscanf y %[^;] ("todo hasta el proximo ;"). Las lineas
 * mal formadas se informan y se saltean.
 * Probar con:  ./sol < mision2_registro.entrada.txt
 */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char linea[100];
    int numero = 0;
    int validas = 0;
    int oro_total = 0;

    while (fgets(linea, sizeof(linea), stdin) != NULL) {
        numero++;
        linea[strcspn(linea, "\n")] = '\0';
        char nombre[24];
        int nivel, oro;
        char sobra;
        /* %23[^;]: hasta 23 letras que no sean ';' (deja lugar para el \0) */
        int leidos = sscanf(linea, "%23[^;];%d;%d %c", nombre, &nivel, &oro, &sobra);
        if (leidos != 3 || nivel < 1 || oro < 0) {
            printf("línea %d inválida: \"%s\"\n", numero, linea);
            continue;
        }
        printf("%-10s nivel %2d  %5d de oro\n", nombre, nivel, oro);
        validas++;
        oro_total += oro;
    }
    printf("%d registros válidos, %d de oro en total\n", validas, oro_total);
    return 0;
}
```

#### Pruebas

##### Todo válido
```entrada
Ana;1;0
Beto;99;5
```
```salida
Ana        nivel  1      0 de oro
Beto       nivel 99      5 de oro
2 registros válidos, 5 de oro en total
```

##### Separadores raros
```entrada
;5;10
Kira;;10
Kira;5;
```
```salida
línea 1 inválida: ";5;10"
línea 2 inválida: "Kira;;10"
línea 3 inválida: "Kira;5;"
0 registros válidos, 0 de oro en total
```

##### Sin registros
```entrada
```
```salida
0 registros válidos, 0 de oro en total
```

### Misión R02-N02-M3 · Las runas espejo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `es_palindromo(frase)`, que ignore los
espacios y las mayúsculas (`"Anita lava la tina"` sí lo es), recorriendo el
texto desde las dos puntas.

#### Criterio de aprobación

- `es_palindromo` ignora espacios y mayúsculas.
- Recorre el texto desde las dos puntas, sin copiarlo.
- Prueba con "Anita lava la tina" y con una frase que no lo sea.

#### Salida esperada

```
Neuquen              es palíndromo
Anita lava la tina   es palíndromo
Forja                no
Somos o no somos     es palíndromo
Ferrum               no
```

#### Solución de referencia

```c
/*
 * Mision 3 - Las runas espejo: una frase es palindromo si se lee igual al
 * derecho y al reves, sin contar espacios ni mayusculas.
 */
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

bool es_palindromo(const char frase[]);

int main(void)
{
    const char *runas[] = {
        "Neuquen", "Anita lava la tina", "Forja", "Somos o no somos", "Ferrum",
    };
    int n = sizeof(runas) / sizeof(runas[0]);
    for (int i = 0; i < n; i++) {
        printf("%-20s %s\n", runas[i], es_palindromo(runas[i]) ? "es palíndromo" : "no");
    }
    return 0;
}

bool es_palindromo(const char frase[])
{
    int izq = 0;
    int der = (int) strlen(frase) - 1;
    while (izq < der) {
        if (frase[izq] == ' ') {
            izq++;
        } else if (frase[der] == ' ') {
            der--;
        } else {
            if (tolower((unsigned char) frase[izq]) != tolower((unsigned char) frase[der])) {
                return false;
            }
            izq++;
            der--;
        }
    }
    return true;
}
```

### Encargo R02-N02-E1 · Las contraseñas del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El sistema del Gremio revisa las **contraseñas** nuevas: tienen que tener al
menos 8 caracteres, una mayúscula, una minúscula y un dígito. Para cada
contraseña de una lista, mostrá si es segura o **todo** lo que le falta.

#### Criterio de aprobación

- Revisa largo mínimo 8, mayúscula, minúscula y dígito.
- Para cada contraseña muestra si es segura o **todo** lo que le falta.

#### Salida esperada

```
hola       le falta: largo (tiene 4) mayúscula dígito
martillo   le falta: mayúscula dígito
Martillo   le falta: dígito
Martillo7  segura
12345678   le falta: mayúscula minúscula
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - Revisar contrasenias: al menos 8 caracteres, una
 * mayuscula, una minuscula y un digito. Se informa todo lo que falta.
 */
#include <stdio.h>
#include <string.h>
#include <ctype.h>

void revisar(const char clave[]);

int main(void)
{
    const char *claves[] = { "hola", "martillo", "Martillo", "Martillo7", "12345678" };
    int n = sizeof(claves) / sizeof(claves[0]);
    for (int i = 0; i < n; i++) {
        revisar(claves[i]);
    }
    return 0;
}

void revisar(const char clave[])
{
    int mayus = 0, minus = 0, digitos = 0;
    for (int i = 0; clave[i] != '\0'; i++) {
        unsigned char c = (unsigned char) clave[i];
        if (isupper(c)) {
            mayus++;
        } else if (islower(c)) {
            minus++;
        } else if (isdigit(c)) {
            digitos++;
        }
    }

    printf("%-10s ", clave);
    if (strlen(clave) >= 8 && mayus > 0 && minus > 0 && digitos > 0) {
        printf("segura\n");
        return;
    }
    printf("le falta:");
    if (strlen(clave) < 8) {
        printf(" largo (tiene %zu)", strlen(clave));
    }
    if (mayus == 0) {
        printf(" mayúscula");
    }
    if (minus == 0) {
        printf(" minúscula");
    }
    if (digitos == 0) {
        printf(" dígito");
    }
    printf("\n");
}
```

### Prueba del sello

#### ¿Cuántos bytes ocupa `"Hulda"`? ¿Cuántas letras entran en `char x[10]`?

`"Hulda"` ocupa 6 bytes (5 letras más el `'\0'`). En `char x[10]` entran 9 letras.

#### ¿Qué diferencia hay entre `'a'` y `"a"`?

`'a'` es un carácter (un número); `"a"` es un texto: la `a` más el `'\0'`.

#### ¿Qué devuelve `strcmp("Tizon", "Kira")`: cero, negativo o positivo?

Negativo: `"Tizon"` va antes que `"Kira"`.

#### ¿Por qué no se puede comparar textos con `==`?

Porque `==` compara las **direcciones** de los arrays, no las letras. Se usa `strcmp`.

#### ¿Qué ventaja tiene `snprintf` sobre `strcpy`? ¿Cómo sabés si cortó el texto?

Nunca escribe más allá del tamaño que le das. Devuelve cuántos caracteres **quería** escribir: si es mayor o igual que el tamaño, cortó.

#### ¿Qué hace `linea[strcspn(linea, "\n")] = '\0';`?

Busca el primer `\n` y lo reemplaza por el fin de texto: saca el Enter que deja `fgets`.

#### ¿Cuánto da `strlen("año")`? ¿Por qué?

`4`: en UTF-8 la ñ ocupa 2 bytes y `strlen` cuenta bytes, no letras.

### Soluciones (docente)

Material original: `01-C/11-Strings` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R02-N03 · Structs, enum, typedef y union

```meta
tipo: tema
criatura: esqueleto
padre: R02-N02
precio: 10
temas: col.registros, prog.enums
```

### Crónica

En el depósito de la Forja, cada aprendiz tiene una **ficha de hierro** con todo lo suyo: nombre, oficio, dónde está trabajando, su vida y su fuerza, y los tres huecos de su mochila.

—Antes teníamos una lista de nombres, otra de vidas, otra de posiciones —gruñe {mentor}—. Un día alguien ordenó una y no las otras. Kira quedó con la vida de Tizon durante una semana.

### Objetivos

Agrupar datos que van juntos en un **`struct`**; ponerle nombre al tipo con
**`typedef`**; usar **`enum`** para listas de opciones; anidar structs y
guardar arrays adentro; inicializar con **designadores**, y entender que un
struct se **copia** al asignarlo y al pasarlo a una función.

### Antes de empezar

- Arrays y textos (10 y 11).
- Funciones y paso por valor (08); `switch` (06).

### Explicación

#### `struct`: una ficha con campos
```c
typedef struct {
    int x;
    int y;
} Posicion;              /* ¡lleva punto y coma! */
```
- Un struct es un **tipo nuevo** formado por varios **campos**, cada uno con su
  tipo y su nombre.
- **`typedef ... Posicion;`** le da el nombre `Posicion` al tipo. Sin
  `typedef`, se escribe `struct Posicion { ... };` y hay que usarlo siempre
  como `struct Posicion p;`. En el curso se usa `typedef`.
- Por convención, los tipos van con **mayúscula** (`Posicion`, `Personaje`).
- A cada campo se llega con el **punto**: `p.x = 4;`,
  `printf("%d", p.y);`.

#### Inicializar
```c
Posicion yunque = { 4, 2 };                            /* por orden de los campos */
Personaje kira = {
    .nombre = "Kira",                                   /* designadores: por nombre */
    .pos    = { .x = 1, .y = 2 },
    .stats  = { .vida = 100, .vida_max = 100, .ataque = 18 },
};                                                      /* lo no nombrado queda en 0 */
```
Con **designadores** (`.campo = valor`) no importa el orden y se lee qué es cada
número. Lo que no se nombra queda en **0** (y los textos, vacíos). Un struct
local declarado **sin** inicializar tiene basura, igual que un array.

#### Structs anidados y arrays adentro
```c
typedef struct {
    char     nombre[16];
    Clase    clase;
    Posicion pos;                              /* un struct dentro de otro */
    Stats    stats;
    char     mochila[MAX_MOCHILA][LARGO_ITEM]; /* 3 textos */
    int      items;                            /* cuántos se usan (10) */
} Personaje;
```
Los puntos se encadenan: `kira.pos.x`, `kira.stats.vida`, `kira.mochila[0]`,
`kira.mochila[0][0]`.

#### `enum`: una lista de opciones con nombre
```c
typedef enum {
    CLASE_GUERRERA,      /* 0 */
    CLASE_MAGA,          /* 1 */
    CLASE_HERRERO        /* 2 */
} Clase;
```
- Cada nombre es una **constante entera**, empezando en 0. Se leen mucho mejor
  que un 0, 1 o 2 sueltos: `if (p.clase == CLASE_MAGA)`.
- Van muy bien con `switch`. Si falta un caso, `gcc -Wall` avisa (ver el
  bestiario).
- Para mostrarlo como texto hace falta una función (`nombre_clase`): `printf`
  con `%d` muestra el número.

#### Copiar, comparar y pasar a funciones
- **`=` copia el struct entero**, incluidos los arrays que tiene adentro. (Es la
  diferencia con un array suelto, que no se asigna.) La copia es independiente.
- **`==` no funciona** con structs: se comparan campo por campo
  (`misma_posicion`).
- Al pasarlo a una función, se pasa **por valor** (08): la función recibe una
  **copia**. Para que el cambio quede, la función devuelve el struct modificado
  y se guarda:
  ```c
  kira = mover(kira, 3, 0);
  ```
  Funciona, pero copia la ficha entera **dos veces** (92 bytes en el ejemplo)
  en cada llamada. En el 14 se ve la forma habitual: pasar la **dirección** del
  struct.

#### `sizeof` de un struct
Es **al menos** la suma de sus campos, y a veces algo más: el compilador puede
dejar bytes de **relleno** (*padding*) para que cada campo quede en una
dirección cómoda para el procesador. Por eso, para saber el tamaño se usa
siempre `sizeof(Personaje)`, nunca la cuenta a mano.

#### `union`: varias formas de leer el mismo lugar
Un `union` se escribe como un `struct`, pero sus campos **comparten la misma
memoria**: ocupa lo que ocupa el campo más grande, y guardar en uno pisa a los
demás. Sirve para leer los mismos bytes de dos maneras:
```c
#include <stdint.h>

union Dato {
    uint16_t numero;            /* 2 bytes vistos como un número */
    unsigned char bytes[2];     /* los mismos 2 bytes, de a uno */
};

union Dato x;
x.numero = 32767;               /* en binario: 0111 1111 1111 1111 */
printf("%u %u %u\n", x.numero, x.bytes[0], x.bytes[1]);   /* 32767 255 127 */
```
¿Por qué `bytes[0]` es 255 y no 127? Porque las PC (y el navegador) guardan los
números **al revés**: primero el byte de menor peso (`1111 1111` = 255) y
después el de mayor peso (`0111 1111` = 127). Se llama **little endian**; otras
máquinas usan **big endian** (al derecho). `sizeof(union Dato)` es 2: los dos
campos están en el mismo lugar.

Regla: en un `union` se lee el **mismo campo que se escribió último**, salvo que
justamente se quieran ver los bytes (como acá). Para guardar «una cosa u otra»
se acompaña de un `enum` que diga cuál está en uso.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 12 - Structs, enum y typedef: agrupar datos que van juntos.
 * Structs anidados, arrays dentro de structs, inicializacion con
 * designadores, copia y paso por valor.
 *
 *   make run
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_MOCHILA 3
#define LARGO_ITEM  16

/* enum: nombres para una lista de valores enteros (0, 1, 2...) */
typedef enum {
    CLASE_GUERRERA,
    CLASE_MAGA,
    CLASE_HERRERO
} Clase;

typedef struct {
    int x;
    int y;
} Posicion;

typedef struct {
    int vida;
    int vida_max;
    int ataque;
} Stats;

typedef struct {
    char     nombre[16];
    Clase    clase;
    Posicion pos;                                /* un struct dentro de otro */
    Stats    stats;
    char     mochila[MAX_MOCHILA][LARGO_ITEM];   /* un array de textos adentro */
    int      items;                              /* cuantos lugares estan usados */
} Personaje;

const char *nombre_clase(Clase c);
void      mostrar(Personaje p);
Personaje mover(Personaje p, int dx, int dy);
Personaje guardar(Personaje p, const char item[]);
bool      misma_posicion(Posicion a, Posicion b);

int main(void)
{
    /* --- Inicializar por orden: los valores van en el orden de los campos --- */
    Posicion yunque = { 4, 2 };

    /* --- Inicializar con designadores: se nombra cada campo; el resto queda en 0 --- */
    Personaje kira = {
        .nombre = "Kira",
        .clase  = CLASE_GUERRERA,
        .pos    = { .x = 1, .y = 2 },
        .stats  = { .vida = 100, .vida_max = 100, .ataque = 18 },
    };

    /* --- Campo por campo, con el punto --- */
    Personaje tizon;
    snprintf(tizon.nombre, sizeof(tizon.nombre), "%s", "Tizón");
    tizon.clase = CLASE_HERRERO;
    tizon.pos.x = 4;                              /* campo de un campo */
    tizon.pos.y = 2;
    tizon.stats.vida = 140;
    tizon.stats.vida_max = 140;
    tizon.stats.ataque = 12;
    tizon.items = 0;

    printf("sizeof(Posicion) = %zu, sizeof(Personaje) = %zu bytes\n",
           sizeof(Posicion), sizeof(Personaje));
    mostrar(kira);
    mostrar(tizon);

    /* --- Los structs se copian con = (los arrays sueltos no) --- */
    Personaje sombra = kira;
    snprintf(sombra.nombre, sizeof(sombra.nombre), "%s", "Sombra");
    sombra.stats.vida = 1;
    printf("\nla copia cambia sola: %s tiene %d de vida, %s sigue con %d\n",
           sombra.nombre, sombra.stats.vida, kira.nombre, kira.stats.vida);

    /* --- Paso por valor: la funcion recibe una copia y DEVUELVE la nueva --- */
    mover(kira, 3, 0);                           /* el resultado se pierde */
    printf("después de mover(kira) sin guardar: (%d, %d)\n", kira.pos.x, kira.pos.y);
    kira = mover(kira, 3, 0);                    /* ahora si */
    printf("después de kira = mover(kira): (%d, %d)\n", kira.pos.x, kira.pos.y);
    printf("¿Kira está en el yunque? %s\n", misma_posicion(kira.pos, yunque) ? "sí" : "no");

    /* --- Un array dentro de un struct --- */
    printf("\n");
    kira = guardar(kira, "Poción");
    kira = guardar(kira, "Llave");
    kira = guardar(kira, "Martillo");
    kira = guardar(kira, "Antorcha");            /* no entra */
    mostrar(kira);
    return 0;
}

const char *nombre_clase(Clase c)
{
    switch (c) {
        case CLASE_GUERRERA: return "guerrera";
        case CLASE_MAGA:     return "maga";
        case CLASE_HERRERO:  return "herrero";
    }
    return "?";
}

void mostrar(Personaje p)
{
    printf("%s (%s, clase n.º %d) en (%d, %d)  vida %d/%d  ataque %d\n",
           p.nombre, nombre_clase(p.clase), p.clase, p.pos.x, p.pos.y,
           p.stats.vida, p.stats.vida_max, p.stats.ataque);
    printf("  mochila:");
    for (int i = 0; i < p.items; i++) {
        printf(" [%s]", p.mochila[i]);
    }
    if (p.items == 0) {
        printf(" (vacía)");
    }
    printf("\n");
}

Personaje mover(Personaje p, int dx, int dy)
{
    p.pos.x += dx;                               /* cambia la copia... */
    p.pos.y += dy;
    return p;                                    /* ...y la devuelve */
}

Personaje guardar(Personaje p, const char item[])
{
    if (p.items == MAX_MOCHILA) {
        printf("la mochila de %s está llena: no entra %s\n", p.nombre, item);
        return p;
    }
    snprintf(p.mochila[p.items], LARGO_ITEM, "%s", item);
    p.items++;
    return p;
}

/* Dos structs no se comparan con ==: se comparan campo por campo */
bool misma_posicion(Posicion a, Posicion b)
{
    return a.x == b.x && a.y == b.y;
}
```

### Salida esperada

```
sizeof(Posicion) = 8, sizeof(Personaje) = 92 bytes
Kira (guerrera, clase n.º 0) en (1, 2)  vida 100/100  ataque 18
  mochila: (vacía)
Tizón (herrero, clase n.º 2) en (4, 2)  vida 140/140  ataque 12
  mochila: (vacía)

la copia cambia sola: Sombra tiene 1 de vida, Kira sigue con 100
después de mover(kira) sin guardar: (1, 2)
después de kira = mover(kira): (4, 2)
¿Kira está en el yunque? sí

la mochila de Kira está llena: no entra Antorcha
Kira (guerrera, clase n.º 0) en (4, 2)  vida 100/100  ataque 18
  mochila: [Poción] [Llave] [Martillo]
```

### ¿Para qué sirve?

Los structs son la forma de representar cosas del mundo real: un producto con su código, precio y stock; un paciente con sus datos; un paquete de red con su encabezado. Las bibliotecas de C (SDL, las de red, las del sistema operativo) están llenas de structs, y los `enum` le ponen nombre a los estados de una máquina: un semáforo, un pedido (pendiente, enviado, entregado) o el personaje de un juego.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Slime: falta el `;` después de la llave.** El error aparece en la línea
**siguiente**, y arrastra otros:
```
t1.c:6:9: error: expected ‘;’, identifier or ‘(’ before ‘struct’
    6 | typedef struct {
      |         ^~~~~~
```

**Esqueleto: `struct` sin `typedef`, usado sin la palabra `struct`.**
```
t1.c:11:5: error: unknown type name ‘Posicion’; use ‘struct’ keyword to refer to the type
   11 |     Posicion p = { 1, 2 };
      |     ^~~~~~~~
      |     struct
```

**Esqueleto: un campo mal escrito.**
```
t3.c:11:7: error: ‘Stats’ has no member named ‘vidaa’; did you mean ‘vida’?
   11 |     a.vidaa = 3;
      |       ^~~~~
      |       vida
```

**Goblin: comparar structs con `==`.**
```
t2.c:12:11: error: invalid operands to binary == (have ‘Stats’ and ‘Stats’)
   12 |     if (a == b) {
      |           ^~
```

**Ogro: el `switch` al que le falta un caso del `enum`.**
```
t2.c:9:5: warning: enumeration value ‘VERDE’ not handled in switch [-Wswitch]
    9 |     switch (c) {
      |     ^~~~~~
```

**Ogro: la copia que se pierde.** `mover(kira, 3, 0);` sin guardar el resultado
no mueve a nadie.

### Misión R02-N03-M1 · La ficha del arma

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un struct `Arma` con nombre, tipo (un `enum`: espada,
hacha, arco), daño, peso y durabilidad (0 a 100). Escribí `mostrar_arma`,
`danio_efectivo` (la mitad si la durabilidad es menor que 20), `usar(arma,
golpes)` y `reparar(arma)`, que devuelven el arma modificada.

#### Criterio de aprobación

- Define `Arma` con un `enum` para el tipo.
- `danio_efectivo` baja a la mitad con durabilidad menor que 20.
- `usar` y `reparar` devuelven el arma modificada (por valor).

#### Salida esperada

```
Filo del Alba  espada daño 20 (efectivo 20)  3.5 kg  durabilidad 100
Rompeyunques   hacha  daño 28 (efectivo 28)  6.0 kg  durabilidad  30

después de 12 golpes:
Rompeyunques   hacha  daño 28 (efectivo 14)  6.0 kg  durabilidad  18
después de pasar por la Forja:
Rompeyunques   hacha  daño 28 (efectivo 28)  6.0 kg  durabilidad 100
```

#### Solución de referencia

```c
/*
 * Mision 1 - La ficha del arma: un struct con un enum adentro y funciones
 * que reciben una copia y devuelven el arma modificada.
 */
#include <stdio.h>

typedef enum {
    ARMA_ESPADA,
    ARMA_HACHA,
    ARMA_ARCO
} TipoArma;

typedef struct {
    char     nombre[20];
    TipoArma tipo;
    int      danio;
    double   peso;
    int      durabilidad;        /* de 0 a 100 */
} Arma;

const char *nombre_tipo(TipoArma t);
void mostrar_arma(Arma a);
int  danio_efectivo(Arma a);
Arma usar(Arma a, int golpes);
Arma reparar(Arma a);

int main(void)
{
    Arma espada = { "Filo del Alba", ARMA_ESPADA, 20, 3.5, 100 };
    Arma hacha = { .nombre = "Rompeyunques", .tipo = ARMA_HACHA, .danio = 28, .peso = 6.0,
                   .durabilidad = 30 };

    mostrar_arma(espada);
    mostrar_arma(hacha);

    hacha = usar(hacha, 12);
    printf("\ndespués de 12 golpes:\n");
    mostrar_arma(hacha);

    hacha = reparar(hacha);
    printf("después de pasar por la Forja:\n");
    mostrar_arma(hacha);
    return 0;
}

const char *nombre_tipo(TipoArma t)
{
    switch (t) {
        case ARMA_ESPADA: return "espada";
        case ARMA_HACHA:  return "hacha";
        case ARMA_ARCO:   return "arco";
    }
    return "?";
}

void mostrar_arma(Arma a)
{
    printf("%-14s %-6s daño %2d (efectivo %2d)  %.1f kg  durabilidad %3d\n",
           a.nombre, nombre_tipo(a.tipo), a.danio, danio_efectivo(a), a.peso, a.durabilidad);
}

/* Un arma gastada (menos de 20 de durabilidad) pega la mitad */
int danio_efectivo(Arma a)
{
    return a.durabilidad < 20 ? a.danio / 2 : a.danio;
}

Arma usar(Arma a, int golpes)
{
    a.durabilidad -= golpes;
    if (a.durabilidad < 0) {
        a.durabilidad = 0;
    }
    return a;
}

Arma reparar(Arma a)
{
    a.durabilidad = 100;
    return a;
}
```

### Misión R02-N03-M2 · Las zonas de la Forja

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un struct `Rect` con una `Posicion` (la esquina de
arriba a la izquierda), ancho y alto. Escribí `contiene(rect, punto)` y
`se_tocan(a, b)`. (Es lo que hacen los juegos para detectar choques.)

#### Criterio de aprobación

- `Rect` contiene una `Posicion`.
- `contiene` y `se_tocan` responden bien, incluidos los bordes.
- Muestra pruebas con rectángulos que se tocan y que no.

#### Salida esperada

```
¿Kira está en el horno? sí
¿Kira está en el depósito? no
¿el horno toca el yunque? sí
¿el horno toca el depósito? no
```

#### Solución de referencia

```c
/*
 * Mision 2 - Las zonas de la Forja: rectangulos con un struct anidado.
 * Es la misma idea que usan los juegos (y SDL, en el cap. 06) para saber
 * si dos cosas se tocan.
 */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int x;
    int y;
} Posicion;

typedef struct {
    Posicion esquina;            /* esquina de arriba a la izquierda */
    int ancho;
    int alto;
} Rect;

bool contiene(Rect r, Posicion p);
bool se_tocan(Rect a, Rect b);

int main(void)
{
    Rect horno   = { { 0, 0 }, 4, 3 };
    Rect yunque  = { { 3, 2 }, 2, 2 };
    Rect deposito = { .esquina = { 10, 0 }, .ancho = 5, .alto = 5 };
    Posicion kira = { 2, 1 };

    printf("¿Kira está en el horno? %s\n", contiene(horno, kira) ? "sí" : "no");
    printf("¿Kira está en el depósito? %s\n", contiene(deposito, kira) ? "sí" : "no");
    printf("¿el horno toca el yunque? %s\n", se_tocan(horno, yunque) ? "sí" : "no");
    printf("¿el horno toca el depósito? %s\n", se_tocan(horno, deposito) ? "sí" : "no");
    return 0;
}

/* El punto esta adentro si queda entre los bordes (el borde derecho no cuenta) */
bool contiene(Rect r, Posicion p)
{
    return p.x >= r.esquina.x && p.x < r.esquina.x + r.ancho &&
           p.y >= r.esquina.y && p.y < r.esquina.y + r.alto;
}

/* Dos rectangulos se tocan si NINGUNO esta del todo a un costado del otro */
bool se_tocan(Rect a, Rect b)
{
    return a.esquina.x < b.esquina.x + b.ancho && b.esquina.x < a.esquina.x + a.ancho &&
           a.esquina.y < b.esquina.y + b.alto && b.esquina.y < a.esquina.y + a.alto;
}
```

### Misión R02-N03-M3 · La máquina de estados

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un `enum Estado` (quieto, caminando, atacando,
herido) y una función `siguiente(estado, evento)`: `m` camina, `a` ataca, `g`
lo deja herido y `p` lo frena. Estando herido no puede atacar. Procesá los
eventos `"mapgamgpa"` mostrando cada cambio.

#### Criterio de aprobación

- Usa un `enum Estado` y `siguiente(estado, evento)`.
- Estando herido no puede atacar.
- Procesa `"mapgamgpa"` mostrando cada cambio.

#### Salida esperada

```
empieza quieto
'm': quieto    -> caminando
'a': caminando -> atacando
'p': atacando  -> quieto
'g': quieto    -> herido
'a': herido    -> herido
'm': herido    -> caminando
'g': caminando -> herido
'p': herido    -> quieto
'a': quieto    -> atacando
```

#### Solución de referencia

```c
/*
 * Mision 3 - La maquina de estados del aprendiz: un enum para el estado y
 * una funcion que decide el siguiente segun el evento.
 *   eventos: 'm' mover, 'a' atacar, 'g' recibir golpe, 'p' parar
 */
#include <stdio.h>
#include <string.h>

typedef enum {
    QUIETO,
    CAMINANDO,
    ATACANDO,
    HERIDO
} Estado;

const char *nombre_estado(Estado e);
Estado siguiente(Estado actual, char evento);

int main(void)
{
    const char *eventos = "mapgamgpa";
    Estado estado = QUIETO;
    printf("empieza %s\n", nombre_estado(estado));
    for (int i = 0; eventos[i] != '\0'; i++) {
        Estado nuevo = siguiente(estado, eventos[i]);
        printf("'%c': %-9s -> %s\n", eventos[i], nombre_estado(estado), nombre_estado(nuevo));
        estado = nuevo;
    }
    return 0;
}

const char *nombre_estado(Estado e)
{
    switch (e) {
        case QUIETO:    return "quieto";
        case CAMINANDO: return "caminando";
        case ATACANDO:  return "atacando";
        case HERIDO:    return "herido";
    }
    return "?";
}

/* Reglas: herido no puede atacar (primero tiene que parar);
   un golpe siempre deja herido */
Estado siguiente(Estado actual, char evento)
{
    switch (evento) {
        case 'g':
            return HERIDO;
        case 'p':
            return QUIETO;
        case 'm':
            return CAMINANDO;
        case 'a':
            return actual == HERIDO ? HERIDO : ATACANDO;
        default:
            return actual;
    }
}
```

### Encargo R02-N03-E1 · Los vencimientos del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El Gremio lleva sus vencimientos con un struct `Fecha` (día, mes, año). Escribí
`es_bisiesto`, `es_valida` (meses de 28, 29, 30 o 31 días), `comparar(a, b)`
(negativo, 0 o positivo, como `strcmp`) y `dia_siguiente`. Probala con el
31/12, el 28/02 de un año bisiesto y de uno que no, y fechas inválidas.

#### Criterio de aprobación

- Escribe `es_bisiesto`, `es_valida`, `comparar` y `dia_siguiente` con un struct `Fecha`.
- Prueba con el 31/12, el 28/02 de un año bisiesto y de uno que no, y fechas inválidas.

#### Salida esperada

```
26/09/2026 -> 27/09/2026
31/12/2026 -> 01/01/2027
28/02/2028 -> 29/02/2028
28/02/2027 -> 01/03/2027
29/02/2027 no es válida
31/04/2026 no es válida
la entrega todavía no venció
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - Fechas: un struct Fecha, validarla, compararla y
 * calcular el dia siguiente (con anios bisiestos).
 */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int dia;
    int mes;
    int anio;
} Fecha;

bool es_bisiesto(int anio);
int  dias_del_mes(int mes, int anio);
bool es_valida(Fecha f);
int  comparar(Fecha a, Fecha b);
Fecha dia_siguiente(Fecha f);

int main(void)
{
    Fecha pruebas[] = {
        { 26, 9, 2026 }, { 31, 12, 2026 }, { 28, 2, 2028 }, { 28, 2, 2027 },
        { 29, 2, 2027 }, { 31, 4, 2026 },
    };
    int n = sizeof(pruebas) / sizeof(pruebas[0]);
    for (int i = 0; i < n; i++) {
        Fecha f = pruebas[i];
        printf("%02d/%02d/%d ", f.dia, f.mes, f.anio);
        if (!es_valida(f)) {
            printf("no es válida\n");
            continue;
        }
        Fecha s = dia_siguiente(f);
        printf("-> %02d/%02d/%d\n", s.dia, s.mes, s.anio);
    }

    Fecha entrega = { 15, 10, 2026 };
    Fecha hoy = { 26, 9, 2026 };
    int c = comparar(hoy, entrega);
    printf("la entrega %s\n", c < 0 ? "todavía no venció" : c == 0 ? "es hoy" : "ya venció");
    return 0;
}

bool es_bisiesto(int anio)
{
    return (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
}

int dias_del_mes(int mes, int anio)
{
    switch (mes) {
        case 2:
            return es_bisiesto(anio) ? 29 : 28;
        case 4: case 6: case 9: case 11:
            return 30;
        default:
            return 31;
    }
}

bool es_valida(Fecha f)
{
    return f.mes >= 1 && f.mes <= 12 && f.dia >= 1 && f.dia <= dias_del_mes(f.mes, f.anio);
}

/* Negativo si a es anterior, 0 si son iguales, positivo si es posterior (como strcmp) */
int comparar(Fecha a, Fecha b)
{
    if (a.anio != b.anio) {
        return a.anio - b.anio;
    }
    if (a.mes != b.mes) {
        return a.mes - b.mes;
    }
    return a.dia - b.dia;
}

Fecha dia_siguiente(Fecha f)
{
    f.dia++;
    if (f.dia > dias_del_mes(f.mes, f.anio)) {
        f.dia = 1;
        f.mes++;
        if (f.mes > 12) {
            f.mes = 1;
            f.anio++;
        }
    }
    return f;
}
```

### Prueba del sello

#### ¿Qué hace el `typedef` en `typedef struct { ... } Posicion;`?

Le da el nombre `Posicion` al struct, para escribir `Posicion p;` en lugar de `struct ... p;`.

#### ¿Cómo se llega al campo `x` de la posición de `kira`?

`kira.pos.x`.

#### ¿Qué valor tienen los campos no nombrados con designadores?

Cero.

#### ¿Cuánto vale `CLASE_HERRERO` en el `enum` del ejemplo?

`2`: los valores del `enum` empiezan en 0 y suben de a uno (`CLASE_GUERRERA` 0, `CLASE_MAGA` 1).

#### Si `b = a;` y después cambiás `b.nombre`, ¿cambia `a.nombre`?

No: `b = a` copia todo el struct (incluido el array del nombre).

#### ¿Por qué `mover(kira, 3, 0);` no mueve a Kira?

Porque `mover` recibe una **copia** de `kira`: mueve la copia. Hay que devolver el struct modificado o pasar un puntero (14).

#### ¿Por qué `sizeof` de un struct puede ser mayor que la suma de sus campos?

Por el **relleno** (*padding*): el compilador agrega bytes para alinear cada campo en la memoria.

#### ¿Cuánto ocupa un `union` con un `int` y un `char[2]`? ¿Qué pasa si se guarda en uno y se lee el otro?

Lo que el campo más grande (el `int`, 4 bytes): los campos comparten la memoria. Leer el otro campo muestra los mismos bytes vistos de otra forma (en las PC, el byte de menor peso primero: *little endian*).

### Soluciones (docente)

Material original: `01-C/12-Structs` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R02-N04 · Punteros

```meta
tipo: tema
criatura: troll
padre: R02-N03
precio: 10
temas: mem.punteros
```

### Crónica

En el fondo del pasillo vive la **Araña de las Direcciones**. No guarda cosas: guarda **dónde** están las cosas, en hilos que van de su tela a cada cajón. Tirando de un hilo, cambia lo que hay adentro sin moverse de su lugar.

—Es la criatura más útil y más peligrosa de la Forja, {heroe} —dice {mentor}—. Un hilo que apunta a un cajón vacío… y te cae el techo encima.

### Objetivos

Entender qué es una **dirección de memoria** y qué es un **puntero**; usar `&`
y `*`; pasar punteros a funciones para que modifiquen variables de afuera o
devuelvan varios resultados; usar `NULL`; entender la relación entre punteros y
arrays (y por qué pasaban las cosas raras del 10 y el 11); aritmética de
punteros, `const` y puntero a puntero.

### Antes de empezar

- Paso por valor (08): una función recibe **copias**.
- Arrays y textos, y cómo se pasan a funciones (10 y 11).

### Explicación

#### La memoria es una hilera de cajones numerados
Cada variable vive en algún lugar de la memoria, y ese lugar tiene un número:
su **dirección**.
```
dirección:   ...  1000   1004   1008  ...
contenido:        oro=10  ...    p=1000
```
- **`&oro`** es "la dirección de `oro`".
- Un **puntero** es una variable que guarda una dirección. Se declara con `*`:
  `int *p = &oro;` ("`p` es un puntero a `int`, y apunta a `oro`").
- **`*p`** es "lo que hay en la dirección que guarda `p`": leer `*p` da 10, y
  `*p = 42;` cambia `oro`. A esto se le dice **desreferenciar**.
- Un puntero ocupa **8 bytes** en una computadora de 64 bits, sin importar a qué
  apunte.
- `printf("%p", (void *) &oro)` muestra la dirección en hexa, por ejemplo
  `0x7fff28aaa084`. **Cambia en cada ejecución**, por eso el ejemplo no la
  muestra.

El `*` tiene dos usos que no hay que confundir: en la **declaración**
(`int *p`) dice "esto es un puntero"; en una **expresión** (`*p = 42`) dice
"andá a donde apunta".

#### Punteros como parámetros
Una función recibe copias (08)… pero si la copia es una **dirección**, la
función puede ir a esa dirección y cambiar la variable original:
```c
void duplicar(int *valor) { *valor = *valor * 2; }
...
duplicar(&oro);          /* le paso DÓNDE está oro */
```
Así se escriben funciones que:
- **modifican** variables de quien llama (`intercambiar(&a, &b)`);
- **devuelven varios resultados** (`dividir(100, 7, &cociente, &resto)`);
- devuelven si pudieron hacer algo (`bool`) y el dato por puntero.

Esto es lo que hace `sscanf(linea, "%d", &edad)` desde el 05: recibe la
dirección de `edad` para poder guardar ahí el número.

#### `NULL`
`NULL` es un puntero que **no apunta a nada**. Sirve para:
- inicializar un puntero que todavía no tiene destino (`int *objetivo = NULL;`);
- decir "no encontré nada" (`buscar` devuelve `NULL`, como `strchr` en el 11).

**Nunca** se desreferencia un puntero `NULL`: el programa se cae (ver el
bestiario). Antes de usar un puntero que puede ser `NULL`, se pregunta:
`if (hallado != NULL)`.

#### Punteros y arrays
El nombre de un array, usado en una expresión, se convierte en la **dirección de
su primer elemento**: `int *q = vidas;` es lo mismo que `int *q = &vidas[0];`.
Eso explica varias cosas de antes:
- Cuando se pasa un array a una función, **se pasa esa dirección**: por eso la
  función modifica el original (10), y por eso `sizeof` adentro da 8, el tamaño
  de un puntero (el Goblin del 10). En un parámetro, `int v[]` y `int *v` son lo
  mismo.
- Los textos se pasan a `sscanf` sin `&` (11): el nombre ya es una dirección.
- `const char *` (08, 11) es "puntero a caracteres que no se modifican".

#### Aritmética de punteros
Sumarle 1 a un puntero lo avanza **un elemento**, no un byte: `q + 1` está 4
bytes después si apunta a `int`.
| Expresión | Significa |
|---|---|
| `*(q + 2)` | el elemento 2: lo mismo que `q[2]` |
| `q++` | avanzar al siguiente elemento |
| `fin - inicio` | cuántos elementos hay entre dos punteros del mismo array |
| `p < vidas + n` | ¿`p` todavía está dentro del array? |

`vidas[i]` es, por definición, `*(vidas + i)`. Los corchetes son un atajo.

#### `const` con punteros
| Declaración | Qué no se puede |
|---|---|
| `const int *p` | cambiar **lo apuntado** (`*p = 5` da error); `p` sí puede apuntar a otro lado |
| `int *const p` | cambiar **a dónde apunta** `p`; lo apuntado sí se puede cambiar |

La primera es la que se usa todo el tiempo en los parámetros: "leo, pero no
toco".

#### Puntero a puntero
Una función que tiene que cambiar **a dónde apunta** un puntero de quien llama
recibe la dirección de ese puntero: un `int **`.
```c
void elegir_mas_debil(int *vida_a, int *vida_b, int **objetivo)
{
    *objetivo = (*vida_a <= *vida_b) ? vida_a : vida_b;
}
...
int *objetivo = NULL;
elegir_mas_debil(&vida_orco, &vida_troll, &objetivo);
*objetivo -= 10;
```
Es la misma regla de siempre: para que una función cambie una variable, se le
pasa su dirección. Si la variable es un `int *`, su dirección es un `int **`.

La biblioteca lo usa en **`strtol`**, que convierte un texto en número y deja en
`fin` **dónde terminó** de leer:
```c
char *fin;
long cantidad = strtol("25 flechas", &fin, 10);   /* 25; fin apunta a " flechas" */
```
Si `fin` quedó al principio del texto, no había ningún número.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 13 - Punteros: direcciones (&), desreferenciar (*), NULL, punteros como
 * parametros, punteros y arrays, aritmetica, const y puntero a puntero.
 *
 *   make run
 */
#include <stdio.h>
#include <stdlib.h>    /* strtol */
#include <string.h>    /* strchr */

void duplicar(int *valor);
void intercambiar(int *a, int *b);
void dividir(int total, int partes, int *cociente, int *resto);
int *buscar(int v[], int n, int buscado);
void sumar_todo(const int *v, int n, int *suma);
void elegir_mas_debil(int *vida_a, int *vida_b, int **objetivo);

int main(void)
{
    /* --- Direccion y desreferencia --- */
    int oro = 10;
    int *p = &oro;                               /* p guarda la direccion de oro */
    printf("oro = %d, *p = %d, ¿p == &oro? %s\n", oro, *p, p == &oro ? "sí" : "no");
    printf("un int ocupa %zu bytes; un puntero, %zu\n", sizeof(oro), sizeof(p));

    *p = 42;                                     /* cambia oro A TRAVES de p */
    printf("después de *p = 42: oro = %d\n", oro);

    /* --- Punteros como parametros: la funcion cambia la variable de afuera --- */
    duplicar(&oro);
    printf("después de duplicar(&oro): %d\n", oro);

    int a = 1, b = 9;
    intercambiar(&a, &b);
    printf("después de intercambiar: a = %d, b = %d\n", a, b);

    int cociente, resto;                         /* "devolver" dos resultados */
    dividir(100, 7, &cociente, &resto);
    printf("100 monedas para 7: %d a cada uno y sobran %d\n", cociente, resto);

    /* --- NULL: un puntero que no apunta a nada --- */
    int vidas[] = { 30, 0, 75, 12, 50 };
    int n = sizeof(vidas) / sizeof(vidas[0]);
    int *hallado = buscar(vidas, n, 75);
    if (hallado != NULL) {
        *hallado = 80;                           /* cambia el elemento del array */
        printf("encontré el 75 y lo cambié: vidas[2] = %d\n", vidas[2]);
    }
    if (buscar(vidas, n, 99) == NULL) {
        printf("el 99 no está: buscar devolvió NULL\n");
    }

    /* --- Punteros y arrays --- */
    int *q = vidas;                              /* el nombre del array = &vidas[0] */
    printf("\n*q = %d, *(q + 2) = %d, q[3] = %d\n", *q, *(q + 2), q[3]);
    printf("q + 1 está %d bytes después de q\n", (int) ((char *) (q + 1) - (char *) q));
    printf("recorrido con puntero:");
    for (int *r = vidas; r < vidas + n; r++) {
        printf(" %d", *r);
    }
    printf("\n");
    int total;
    sumar_todo(vidas, n, &total);
    printf("suma = %d\n", total);

    /* --- Los textos tambien: strchr devuelve DONDE encontro la letra --- */
    const char *correo = "kira@forja.cx";
    const char *arroba = strchr(correo, '@');
    if (arroba != NULL) {
        printf("usuario de %d letras, dominio: %s\n", (int) (arroba - correo), arroba + 1);
    }

    /* --- Puntero a puntero --- */
    int vida_orco = 40, vida_troll = 25;
    int *objetivo = NULL;
    elegir_mas_debil(&vida_orco, &vida_troll, &objetivo);
    *objetivo -= 10;                             /* golpea al que eligio */
    printf("\nKira golpea al más débil: orco %d, troll %d\n", vida_orco, vida_troll);

    char *fin;                                   /* strtol dice DONDE termino el numero */
    long cantidad = strtol("25 flechas", &fin, 10);
    printf("strtol leyó %ld y lo que sigue es \"%s\"\n", cantidad, fin);
    return 0;
}

void duplicar(int *valor)
{
    *valor = *valor * 2;
}

void intercambiar(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

void dividir(int total, int partes, int *cociente, int *resto)
{
    *cociente = total / partes;
    *resto = total % partes;
}

/* Devuelve la direccion del primer elemento igual a buscado, o NULL */
int *buscar(int v[], int n, int buscado)
{
    for (int i = 0; i < n; i++) {
        if (v[i] == buscado) {
            return &v[i];
        }
    }
    return NULL;
}

/* const int *v: se puede leer *v, pero no cambiarlo */
void sumar_todo(const int *v, int n, int *suma)
{
    *suma = 0;
    for (int i = 0; i < n; i++) {
        *suma += v[i];
    }
}

/* Cambia A DONDE apunta el puntero de quien llama: por eso recibe int ** */
void elegir_mas_debil(int *vida_a, int *vida_b, int **objetivo)
{
    if (*vida_a <= *vida_b) {
        *objetivo = vida_a;
    } else {
        *objetivo = vida_b;
    }
}
```

### Salida esperada

```
oro = 10, *p = 10, ¿p == &oro? sí
un int ocupa 4 bytes; un puntero, 8
después de *p = 42: oro = 42
después de duplicar(&oro): 84
después de intercambiar: a = 9, b = 1
100 monedas para 7: 14 a cada uno y sobran 2
encontré el 75 y lo cambié: vidas[2] = 80
el 99 no está: buscar devolvió NULL

*q = 30, *(q + 2) = 80, q[3] = 12
q + 1 está 4 bytes después de q
recorrido con puntero: 30 0 80 12 50
suma = 172
usuario de 4 letras, dominio: forja.cx

Kira golpea al más débil: orco 40, troll 15
strtol leyó 25 y lo que sigue es " flechas"
```

### ¿Para qué sirve?

Los punteros son la herramienta de C para trabajar con memoria de verdad: las funciones que cambian variables del que las llama (`scanf`, `strtol`), los textos y los arrays que se pasan sin copiarse, las estructuras que crecen (listas, árboles) y la comunicación con el hardware, donde una dirección de memoria **es** un pin o un registro. Todos los lenguajes los usan por dentro; C te los muestra.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Troll: desreferenciar `NULL`.** Compila sin avisos y el programa muere:
```
Violación de segmento  (`core' generado) ./u2
```
Con `make asan`, el informe dice que la dirección es 0 y en qué línea:
```
==1013771==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 ...
==1013771==The signal is caused by a WRITE memory access.
==1013771==Hint: address points to the zero page.
    #0 0x5e0b14c3b238 in main u2.c:5
```

**Troll: el puntero sin inicializar.** Apunta a cualquier lado:
```
u1.c:10:5: warning: ‘p’ is used uninitialized [-Wuninitialized]
   10 |     printf("%d\n", *p);
      |     ^~~~~~~~~~~~~~~~~~
```
Si todavía no tiene destino, inicializalo en `NULL`.

**Troll: devolver la dirección de una variable local.** La variable desaparece
al terminar la función, y el puntero queda **colgando**:
```
u1.c:5:12: warning: function returns address of local variable [-Wreturn-local-addr]
    5 |     return &vida;
      |            ^~~~~
```
(Por qué desaparece, y cómo crear datos que sobrevivan a la función, se ve en el
17.)

**Goblin: un puntero a otro tipo.**
```
u1.c:12:14: warning: initialization of ‘int *’ from incompatible pointer type ‘double *’ [-Wincompatible-pointer-types]
   12 |     int *q = &d;
      |              ^
```

**Goblin: olvidar el `&`.** Se guarda el **valor** como si fuera una dirección:
```
u1.c:14:14: warning: initialization of ‘int *’ from ‘int’ makes pointer from integer without a cast [-Wint-conversion]
   14 |     int *r = x;
      |              ^
```

**Ogro: olvidar el `*`.** En `void duplicar(int *valor) { valor = valor * 2; }`
se opera con la dirección, no con el número. Acá `gcc` da error, porque un
puntero no se puede multiplicar:
```
u4.c:1:43: error: invalid operands to binary * (have ‘int *’ and ‘int’)
    1 | void duplicar(int *valor) { valor = valor * 2; }
      |                                           ^
```
Pero `valor++` compila sin avisos: avanza el puntero y el número queda igual.

### Misión R02-N04-M1 · La receta de lectura

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Convertí el bucle de validación del 07 en una
función `bool pedir_entero(pregunta, minimo, maximo, int *resultado)`: vuelve
a preguntar hasta que el dato sea válido y devuelve `false` si se terminó la
entrada. Con ella, pedí tres durezas y ordenalas con
`ordenar_tres(&x, &y, &z)` (que usa `intercambiar`).

#### Criterio de aprobación

- `pedir_entero` vuelve a preguntar hasta un dato válido y devuelve `false` si se termina la entrada.
- Deja el resultado en `*resultado`.
- `ordenar_tres(&x, &y, &z)` usa `intercambiar`.

#### Entrada de ejemplo

```
70
cien
250
15
42
```

#### Salida esperada

```
Dureza del primer lingote (1-100): Dureza del segundo lingote (1-100): 
  tiene que ser un entero entre 1 y 100.
Dureza del segundo lingote (1-100): 
  tiene que ser un entero entre 1 y 100.
Dureza del segundo lingote (1-100): Dureza del tercer lingote (1-100): 
De menor a mayor: 15 42 70
```

#### Solución de referencia

```c
/*
 * Mision 1 - La receta de lectura, ahora como funcion: pedir_entero devuelve
 * si pudo leer (true/false) y deja el numero en *resultado. Despues se
 * ordenan tres valores con intercambiar.
 * Probar con:  ./sol < mision1_pedir.entrada.txt
 */
#include <stdio.h>
#include <stdbool.h>

bool pedir_entero(const char *pregunta, int minimo, int maximo, int *resultado);
void intercambiar(int *a, int *b);
void ordenar_tres(int *a, int *b, int *c);

int main(void)
{
    int x, y, z;
    if (!pedir_entero("Dureza del primer lingote (1-100): ", 1, 100, &x) ||
        !pedir_entero("Dureza del segundo lingote (1-100): ", 1, 100, &y) ||
        !pedir_entero("Dureza del tercer lingote (1-100): ", 1, 100, &z)) {
        printf("\nNo hay más entrada.\n");
        return 1;
    }
    ordenar_tres(&x, &y, &z);
    printf("\nDe menor a mayor: %d %d %d\n", x, y, z);
    return 0;
}

/* Vuelve a preguntar hasta que sea un entero en [minimo, maximo].
   Devuelve false si se termino la entrada. */
bool pedir_entero(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  tiene que ser un entero entre %d y %d.\n", minimo, maximo);
    }
}

void intercambiar(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

void ordenar_tres(int *a, int *b, int *c)
{
    if (*a > *b) {
        intercambiar(a, b);          /* a y b ya son direcciones: sin & */
    }
    if (*b > *c) {
        intercambiar(b, c);
    }
    if (*a > *b) {
        intercambiar(a, b);
    }
}
```

#### Pruebas

##### Ya ordenadas
```entrada
1
2
3
```
```salida
Dureza del primer lingote (1-100): Dureza del segundo lingote (1-100): Dureza del tercer lingote (1-100):
De menor a mayor: 1 2 3
```

##### Iguales
```entrada
50
50
50
```
```salida
Dureza del primer lingote (1-100): Dureza del segundo lingote (1-100): Dureza del tercer lingote (1-100):
De menor a mayor: 50 50 50
```

##### Se termina la entrada
```entrada
10
```
```salida
Dureza del primer lingote (1-100): Dureza del segundo lingote (1-100):
No hay más entrada.
```

### Misión R02-N04-M2 · Recorrer con punteros

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Sin usar índices: `contar_mayores(inicio, fin,
limite)` (cuenta desde `inicio` hasta antes de `fin`), `invertir(v, n)` con
dos punteros que se acercan desde las puntas y `mi_strlen(texto)`.

#### Criterio de aprobación

- No usa índices: recorre con punteros.
- `contar_mayores(inicio, fin, limite)` cuenta hasta antes de `fin`.
- `invertir` usa dos punteros desde las puntas; `mi_strlen` avanza hasta el `'\0'`.

#### Salida esperada

```
mayores que 30: 4
mayores que 30 en la primera mitad: 1
invertido: 90 31 55 7 40 12
mi_strlen("Ferrum") = 6
mi_strlen("") = 0
```

#### Solución de referencia

```c
/*
 * Mision 2 - Recorrer con punteros: sin indices, solo avanzando el puntero.
 */
#include <stdio.h>
#include <stddef.h>    /* size_t */

int    contar_mayores(const int *inicio, const int *fin, int limite);
void   invertir(int *v, int n);
size_t mi_strlen(const char *s);

int main(void)
{
    int durezas[] = { 12, 40, 7, 55, 31, 90 };
    int n = sizeof(durezas) / sizeof(durezas[0]);

    printf("mayores que 30: %d\n", contar_mayores(durezas, durezas + n, 30));
    printf("mayores que 30 en la primera mitad: %d\n",
           contar_mayores(durezas, durezas + n / 2, 30));

    invertir(durezas, n);
    printf("invertido:");
    for (const int *p = durezas; p < durezas + n; p++) {
        printf(" %d", *p);
    }
    printf("\n");

    printf("mi_strlen(\"Ferrum\") = %zu\n", mi_strlen("Ferrum"));
    printf("mi_strlen(\"\") = %zu\n", mi_strlen(""));
    return 0;
}

/* Cuenta desde inicio hasta ANTES de fin (fin no se lee) */
int contar_mayores(const int *inicio, const int *fin, int limite)
{
    int cuenta = 0;
    for (const int *p = inicio; p < fin; p++) {
        if (*p > limite) {
            cuenta++;
        }
    }
    return cuenta;
}

/* Dos punteros que se acercan desde las puntas */
void invertir(int *v, int n)
{
    int *izq = v;
    int *der = v + n - 1;
    while (izq < der) {
        int tmp = *izq;
        *izq = *der;
        *der = tmp;
        izq++;
        der--;
    }
}

size_t mi_strlen(const char *s)
{
    const char *p = s;
    while (*p != '\0') {
        p++;
    }
    return (size_t) (p - s);         /* la resta de punteros da la distancia */
}
```

### Misión R02-N04-M3 · Los extremos de la horda

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `extremos(v, n, int **menor, int
**mayor)`, que deja en `*menor` y `*mayor` la **dirección** de esos
elementos. Con ellas, dividí por 2 la vida del más fuerte y poné en 0 la del
más débil, y mostrá en qué posición estaban (resta de punteros).

#### Criterio de aprobación

- `extremos` recibe `int **menor` y `int **mayor` y deja las direcciones.
- Modifica la vida del más fuerte y del más débil a través de esos punteros.
- Muestra la posición con resta de punteros.

#### Salida esperada

```
vidas: 45 12 80 33 67
el más débil tiene 12 (posición 1); el más fuerte, 80 (posición 2)
vidas: 45 0 40 33 67
```

#### Solución de referencia

```c
/*
 * Mision 3 - Los extremos de la horda: extremos() deja en *menor y *mayor la
 * DIRECCION de esos elementos (por eso recibe int **). Con esas direcciones
 * se modifican los elementos del array.
 */
#include <stdio.h>

void extremos(int v[], int n, int **menor, int **mayor);
void mostrar(const int v[], int n);

int main(void)
{
    int vidas[] = { 45, 12, 80, 33, 67 };
    int n = sizeof(vidas) / sizeof(vidas[0]);
    int *menor = NULL;
    int *mayor = NULL;

    mostrar(vidas, n);
    extremos(vidas, n, &menor, &mayor);
    printf("el más débil tiene %d (posición %d); el más fuerte, %d (posición %d)\n",
           *menor, (int) (menor - vidas), *mayor, (int) (mayor - vidas));

    *mayor /= 2;                     /* el hechizo de Hulda al mas fuerte */
    *menor = 0;                      /* Kira remata al mas debil */
    mostrar(vidas, n);
    return 0;
}

void extremos(int v[], int n, int **menor, int **mayor)
{
    *menor = &v[0];
    *mayor = &v[0];
    for (int i = 1; i < n; i++) {
        if (v[i] < **menor) {
            *menor = &v[i];
        }
        if (v[i] > **mayor) {
            *mayor = &v[i];
        }
    }
}

void mostrar(const int v[], int n)
{
    printf("vidas:");
    for (int i = 0; i < n; i++) {
        printf(" %d", v[i]);
    }
    printf("\n");
}
```

### Encargo R02-N04-E1 · El reloj del taller

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El reloj del taller registra la entrada y la salida como `"hh:mm:ss"`. Escribí
`leer_hora(texto, &h, &m, &s)` (valida el formato y los rangos),
`a_segundos(h, m, s)` y `desde_segundos(total, &h, &m, &s)`, y calculá cuánto
trabajó cada empleado. Probala también con horas inválidas.

#### Criterio de aprobación

- `leer_hora` valida el formato `hh:mm:ss` y los rangos, y devuelve los valores por puntero.
- Convierte con `a_segundos` y `desde_segundos`.
- Muestra lo trabajado y rechaza horas inválidas.

#### Salida esperada

```
08:45:10 a 17:20:05: 30895 segundos = 8h 34m 55s
13:00:00 a 21:30:45: 30645 segundos = 8h 30m 45s
07:61:00 a 15:00:00: hora inválida
ocho     a 17:00:00: hora inválida
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - El reloj del taller: convertir entre "hh:mm:ss" y
 * segundos, con funciones que devuelven varios resultados por puntero.
 */
#include <stdio.h>
#include <stdbool.h>

bool leer_hora(const char *texto, int *h, int *m, int *s);
int  a_segundos(int h, int m, int s);
void desde_segundos(int total, int *h, int *m, int *s);

int main(void)
{
    const char *entradas[] = { "08:45:10", "13:00:00", "07:61:00", "ocho" };
    const char *salidas[]  = { "17:20:05", "21:30:45", "15:00:00", "17:00:00" };
    int n = sizeof(entradas) / sizeof(entradas[0]);

    for (int i = 0; i < n; i++) {
        int h1, m1, s1, h2, m2, s2;
        printf("%-8s a %-8s: ", entradas[i], salidas[i]);
        if (!leer_hora(entradas[i], &h1, &m1, &s1) || !leer_hora(salidas[i], &h2, &m2, &s2)) {
            printf("hora inválida\n");
            continue;
        }
        int trabajado = a_segundos(h2, m2, s2) - a_segundos(h1, m1, s1);
        int h, m, s;
        desde_segundos(trabajado, &h, &m, &s);
        printf("%d segundos = %dh %02dm %02ds\n", trabajado, h, m, s);
    }
    return 0;
}

bool leer_hora(const char *texto, int *h, int *m, int *s)
{
    char sobra;
    if (sscanf(texto, "%d:%d:%d %c", h, m, s, &sobra) != 3) {   /* h, m y s ya son direcciones */
        return false;
    }
    return *h >= 0 && *h < 24 && *m >= 0 && *m < 60 && *s >= 0 && *s < 60;
}

int a_segundos(int h, int m, int s)
{
    return h * 3600 + m * 60 + s;
}

void desde_segundos(int total, int *h, int *m, int *s)
{
    *h = total / 3600;
    *m = total % 3600 / 60;
    *s = total % 60;
}
```

### Prueba del sello

#### Si `int x = 5; int *p = &x;`, ¿qué valen `*p` y `p == &x`? ¿Qué hace `*p = 9`?

`*p` vale 5 y `p == &x` es verdadero. `*p = 9` cambia `x` a 9.

#### ¿Por qué `intercambiar(a, b)` no puede funcionar y `intercambiar(&a, &b)` sí?

Porque recibe **copias** de `a` y `b`. Con `&a` y `&b` recibe sus direcciones y puede cambiar los originales.

#### ¿Qué es `NULL` y cuándo se usa?

Un puntero que no apunta a nada. Se usa para inicializar punteros y como respuesta "no encontré".

#### ¿Qué relación hay entre `v[3]` y `*(v + 3)`?

Son lo mismo: `v[3]` es `*(v + 3)`.

#### Si `int *q` apunta a la dirección 1000, ¿a qué dirección apunta `q + 1`?

A 1004 (si `int` ocupa 4 bytes): avanza un elemento, no un byte.

#### ¿Qué diferencia hay entre `const int *p` e `int *const p`?

Con `const int *p` no se puede cambiar el valor apuntado; con `int *const p` no se puede cambiar a dónde apunta.

#### ¿Cuándo una función necesita recibir un `int **`?

Cuando tiene que cambiar **un puntero** del que la llama (por ejemplo, dejarle la dirección de algo).

### Soluciones (docente)

Material original: `01-C/13-Punteros` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R02-N05 · Punteros y structs

```meta
tipo: tema
criatura: troll
padre: R02-N04
precio: 10
temas: mem.punteros
usa: col.registros
```

### Crónica

Hasta ahora, cada vez que necesitabas que alguien cambiara tu ficha, hacías una copia, la mandabas al taller y esperabas que te la devolvieran.

—Es como fundir otra espada cada vez que querés afilarla —dice {mentor}, y te da un hilo de la Araña—. Mandá esto, {heroe}. Es el camino a tu ficha. El taller la cambia donde está.

### Objetivos

Pasar structs a funciones **por puntero** en lugar de por valor, usar el
operador **`->`**, marcar con **`const`** las funciones que solo leen y armar un
conjunto de funciones que operan sobre una entidad: la forma de trabajar en C
que después se convierte en los métodos de C++.

### Antes de empezar

- Structs y cómo se copian (12).
- Punteros: `&`, `*`, `NULL`, `const` (13).

### Explicación

#### Por valor o por puntero
| | Por valor: `void f(Personaje p)` | Por puntero: `void f(Personaje *p)` |
|---|---|---|
| Qué recibe | una **copia** de todo el struct | la **dirección** del original (8 bytes) |
| ¿Puede cambiar el original? | no | sí |
| Costo | copia `sizeof(Personaje)` bytes | copia 8 bytes |
| Cómo se llama | `f(kira)` | `f(&kira)` |

En el 12, para que un cambio quedara, la función devolvía el struct y había que
guardarlo (`kira = mover(kira, 3, 0)`). Por puntero, la función cambia el
original directamente: `curar(&kira, 30);`.

#### El operador `->`
Con un puntero a struct, se podría escribir `(*p).vida`: primero ir al struct y
después al campo. Los paréntesis hacen falta porque el `.` tiene más prioridad
que el `*`. Como es incómodo, C tiene un atajo:
```c
p->vida         /* es exactamente (*p).vida */
```
Regla: **con una variable struct, punto; con un puntero a struct, flecha**.
`kira.vida`, pero `p->vida`.

#### `const`: la función que solo mira
```c
bool esta_vivo(const Personaje *p);   /* lee, no modifica */
void curar(Personaje *p, int cantidad);    /* modifica */
```
Un `const Personaje *` dice que la función **no va a modificar** el
personaje, y el compilador lo hace cumplir. Así, leyendo solo el prototipo, se
sabe qué funciones pueden cambiar la ficha. En `atacar(const Personaje
*atacante, Personaje *objetivo)` se ve de un vistazo que el atacante no cambia y
el objetivo sí.

#### Punteros a un campo, y funciones que devuelven un puntero
- `mover(&kira.pos, 3, -1)` pasa la dirección de **solo la posición**. La
  función recibe un `Posicion *` y no puede tocar el resto de la ficha. (El `.`
  va antes que el `&`: es `&(kira.pos)`.)
- `mas_herido(&kira, &tizon)` devuelve la **dirección** de uno de los dos. Con
  ese puntero se trabaja sobre el original: `curar(herido, 40)`.
- Dentro de una función, un parámetro que ya es puntero se pasa **sin `&`**:
  en `atacar`, `recibir_danio(objetivo, ...)`.

#### Crear: devolver por valor está bien
`personaje_crear` arma un struct y lo devuelve por valor: se copia **una vez**,
al crearlo. Lo que conviene evitar es copiar la ficha **en cada operación**.

#### La regla práctica
| Situación | Parámetro |
|---|---|
| la función modifica el struct | `Tipo *p` |
| solo lo lee y es grande | `const Tipo *p` |
| solo lo lee y es chico (una `Posicion`, una `Fecha`) | `Tipo p` (por valor) también está bien |
| lo crea | devuelve `Tipo` |

#### El antecesor de los objetos
Un grupo de funciones que reciben un `Personaje *` como primer parámetro
(`curar`, `recibir_danio`, `pagar`, `esta_vivo`…) es la forma en que C modela un
"objeto": datos en un struct y operaciones en funciones. En C++ (cap. 03) esas
funciones pasan a estar **dentro** del struct y el puntero se vuelve
implícito: `kira.curar(30)` en lugar de `curar(&kira, 30)`.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 14 - Punteros y structs: pasar un struct por valor o por puntero, el
 * operador ->, const para solo lectura y funciones que "operan" sobre una
 * entidad (el antecesor de los metodos de C++).
 *
 *   make run
 */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    int x;
    int y;
} Posicion;

typedef struct {
    char     nombre[16];
    Posicion pos;
    int      vida;
    int      vida_max;
    int      ataque;
    int      oro;
} Personaje;

Personaje  personaje_crear(const char *nombre, int vida, int ataque, int oro);
void       intentar_curar(Personaje p, int cantidad);
void       curar(Personaje *p, int cantidad);
void       recibir_danio(Personaje *p, int cantidad);
void       atacar(const Personaje *atacante, Personaje *objetivo);
bool       pagar(Personaje *p, int monto);
bool       esta_vivo(const Personaje *p);
void       mover(Posicion *pos, int dx, int dy);
Personaje *mas_herido(Personaje *a, Personaje *b);
void       mostrar(const Personaje *p);

int main(void)
{
    Personaje kira = personaje_crear("Kira", 100, 18, 120);
    Personaje tizon = personaje_crear("Tizon", 140, 12, 300);
    printf("un Personaje ocupa %zu bytes; un puntero a él, %zu\n\n",
           sizeof(Personaje), sizeof(Personaje *));

    /* --- Por valor: la funcion trabaja sobre una COPIA --- */
    recibir_danio(&kira, 50);
    mostrar(&kira);
    intentar_curar(kira, 30);
    printf("después de intentar_curar (por valor):\n");
    mostrar(&kira);

    /* --- Por puntero: la funcion trabaja sobre el ORIGINAL --- */
    curar(&kira, 30);
    printf("después de curar (por puntero):\n");
    mostrar(&kira);

    /* --- (*p).campo y p->campo son lo mismo --- */
    Personaje *p = &kira;
    (*p).oro += 5;
    p->oro += 5;
    printf("\noro de Kira: %d (sumado dos veces por el puntero)\n", kira.oro);

    /* --- Un puntero a un campo: la funcion solo ve la posicion --- */
    mover(&kira.pos, 3, -1);
    printf("Kira se movió a (%d, %d)\n", kira.pos.x, kira.pos.y);

    /* --- Funciones que reciben dos entidades --- */
    printf("\n");
    atacar(&tizon, &kira);
    atacar(&kira, &tizon);
    printf("%s compra una espada de 200: %s\n", kira.nombre, pagar(&kira, 200) ? "sí" : "no le alcanza");
    printf("%s compra una espada de 200: %s\n", tizon.nombre, pagar(&tizon, 200) ? "sí" : "no le alcanza");

    /* --- Una funcion que devuelve un puntero a uno de los dos --- */
    Personaje *herido = mas_herido(&kira, &tizon);
    printf("Hulda cura al más herido: %s\n", herido->nombre);
    curar(herido, 40);
    mostrar(&kira);
    mostrar(&tizon);

    recibir_danio(&kira, 999);
    printf("¿Kira sigue en pie? %s\n", esta_vivo(&kira) ? "sí" : "no");
    return 0;
}

/* Crear e inicializar: devolver el struct por valor esta bien (se copia una vez) */
Personaje personaje_crear(const char *nombre, int vida, int ataque, int oro)
{
    Personaje p = { .vida = vida, .vida_max = vida, .ataque = ataque, .oro = oro };
    snprintf(p.nombre, sizeof(p.nombre), "%s", nombre);
    return p;
}

void intentar_curar(Personaje p, int cantidad)
{
    p.vida += cantidad;                          /* cambia la copia */
    printf("  (adentro de la función, la copia tiene %d)\n", p.vida);
}

void curar(Personaje *p, int cantidad)
{
    p->vida += cantidad;                         /* p->vida es (*p).vida */
    if (p->vida > p->vida_max) {
        p->vida = p->vida_max;
    }
}

void recibir_danio(Personaje *p, int cantidad)
{
    p->vida -= cantidad;
    if (p->vida < 0) {
        p->vida = 0;
    }
}

/* const en el atacante: se lee, no se modifica. El objetivo si cambia. */
void atacar(const Personaje *atacante, Personaje *objetivo)
{
    recibir_danio(objetivo, atacante->ataque);   /* objetivo ya es un puntero: sin & */
    printf("%s golpea a %s por %d (le queda %d)\n",
           atacante->nombre, objetivo->nombre, atacante->ataque, objetivo->vida);
}

bool pagar(Personaje *p, int monto)
{
    if (p->oro < monto) {
        return false;
    }
    p->oro -= monto;
    return true;
}

bool esta_vivo(const Personaje *p)
{
    return p->vida > 0;
}

void mover(Posicion *pos, int dx, int dy)
{
    pos->x += dx;
    pos->y += dy;
}

/* Devuelve la direccion del que tiene menos vida en proporcion a su maximo */
Personaje *mas_herido(Personaje *a, Personaje *b)
{
    if (a->vida * b->vida_max <= b->vida * a->vida_max) {
        return a;
    }
    return b;
}

void mostrar(const Personaje *p)
{
    printf("  %-5s vida %3d/%3d  ataque %2d  oro %3d%s\n",
           p->nombre, p->vida, p->vida_max, p->ataque, p->oro,
           esta_vivo(p) ? "" : "  (derrotado)");
}
```

### Salida esperada

```
un Personaje ocupa 40 bytes; un puntero a él, 8

  Kira  vida  50/100  ataque 18  oro 120
  (adentro de la función, la copia tiene 80)
después de intentar_curar (por valor):
  Kira  vida  50/100  ataque 18  oro 120
después de curar (por puntero):
  Kira  vida  80/100  ataque 18  oro 120

oro de Kira: 130 (sumado dos veces por el puntero)
Kira se movió a (3, -1)

Tizon golpea a Kira por 12 (le queda 68)
Kira golpea a Tizon por 18 (le queda 122)
Kira compra una espada de 200: no le alcanza
Tizon compra una espada de 200: sí
Hulda cura al más herido: Kira
  Kira  vida 100/100  ataque 18  oro 130
  Tizon vida 122/140  ataque 12  oro 100
¿Kira sigue en pie? no
```

### ¿Para qué sirve?

Pasar structs por puntero es como se trabaja en cualquier programa real en C: las funciones de SDL reciben `SDL_Window *`, las de archivos reciben `FILE *`, y un sistema de cuentas bancarias modifica la cuenta donde está en lugar de copiarla. El `const` en los parámetros documenta y hace cumplir quién puede modificar qué.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Goblin: punto con un puntero.** `gcc` sugiere la flecha:
```
v1.c:6:6: error: ‘p’ is a pointer; did you mean to use ‘->’?
    6 |     p.vida += 10;
      |      ^
      |      ->
```
Lo mismo con `*p.vida` sin paréntesis: el punto se aplica primero.

**Goblin: flecha con una variable struct.**
```
v1.c:17:6: error: invalid type argument of ‘->’ (have ‘Personaje’)
   17 |     k->vida = 3;
      |      ^~
```

**Goblin: olvidar el `&` al llamar.**
```
v1.c:18:11: error: incompatible type for argument 1 of ‘curar’
   18 |     curar(k);
      |           ^
      |           |
      |           Personaje
v1.c:4:23: note: expected ‘Personaje *’ but argument is of type ‘Personaje’
```

**Esqueleto (el bueno): modificar a través de un `const`.** El compilador
frena el cambio que la función prometió no hacer:
```
v1.c:11:13: error: assignment of member ‘vida’ in read-only object
   11 |     p->vida = 0;
      |             ^
```

**Ogro: pasar por valor cuando había que modificar.** `intentar_curar(kira, 30)`
compila y no cambia nada.

**Troll: devolver un puntero a un struct local.** Si `personaje_crear` devolviera
`&p` (un `Personaje *`), el puntero quedaría colgando (el Troll del 13). Para
crear, se devuelve por valor… o se reserva memoria que sobreviva (17).

### Misión R02-N05-M1 · La mochila por puntero

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Rehacé la mochila del 12 con funciones que
reciben `Personaje *`: `agregar` (devuelve `false` si está llena), `quitar`
(corre los objetos de atrás para tapar el hueco; `false` si no lo tenía) y
`tiene` (con `const`).

#### Criterio de aprobación

- `agregar`, `quitar` y `tiene` reciben `Personaje *` (`tiene` con `const`).
- `quitar` corre los objetos para tapar el hueco.
- Devuelven `false` cuando no se puede.

#### Salida esperada

```
no entra: Mapa
mochila de Kira (4/4): [Poción] [Llave] [Cuerda] [Antorcha]
¿tiene Llave? sí
usó la Llave. ¿tiene Llave? no
¿pudo quitar Espada? no
mochila de Kira (4/4): [Poción] [Cuerda] [Antorcha] [Mapa]
```

#### Solución de referencia

```c
/*
 * Mision 1 - La mochila por puntero: agregar, quitar y buscar objetos
 * modificando el personaje original (sin devolver copias como en el 12).
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_MOCHILA 4
#define LARGO_ITEM  16

typedef struct {
    char nombre[16];
    char mochila[MAX_MOCHILA][LARGO_ITEM];
    int  items;
} Personaje;

bool agregar(Personaje *p, const char *item);
bool quitar(Personaje *p, const char *item);
bool tiene(const Personaje *p, const char *item);
void mostrar(const Personaje *p);

int main(void)
{
    Personaje kira = { .nombre = "Kira" };

    const char *hallazgos[] = { "Poción", "Llave", "Cuerda", "Antorcha", "Mapa" };
    for (int i = 0; i < 5; i++) {
        if (!agregar(&kira, hallazgos[i])) {
            printf("no entra: %s\n", hallazgos[i]);
        }
    }
    mostrar(&kira);

    printf("¿tiene Llave? %s\n", tiene(&kira, "Llave") ? "sí" : "no");
    quitar(&kira, "Llave");
    printf("usó la Llave. ¿tiene Llave? %s\n", tiene(&kira, "Llave") ? "sí" : "no");
    printf("¿pudo quitar Espada? %s\n", quitar(&kira, "Espada") ? "sí" : "no");
    agregar(&kira, "Mapa");
    mostrar(&kira);
    return 0;
}

bool agregar(Personaje *p, const char *item)
{
    if (p->items == MAX_MOCHILA) {
        return false;
    }
    snprintf(p->mochila[p->items], LARGO_ITEM, "%s", item);
    p->items++;
    return true;
}

/* Busca el objeto y corre los de atras un lugar para tapar el hueco */
bool quitar(Personaje *p, const char *item)
{
    for (int i = 0; i < p->items; i++) {
        if (strcmp(p->mochila[i], item) == 0) {
            for (int j = i; j < p->items - 1; j++) {
                for (int k = 0; k < LARGO_ITEM; k++) {      /* copia el texto de atras */
                    p->mochila[j][k] = p->mochila[j + 1][k];
                }
            }
            p->items--;
            return true;
        }
    }
    return false;
}

bool tiene(const Personaje *p, const char *item)
{
    for (int i = 0; i < p->items; i++) {
        if (strcmp(p->mochila[i], item) == 0) {
            return true;
        }
    }
    return false;
}

void mostrar(const Personaje *p)
{
    printf("mochila de %s (%d/%d):", p->nombre, p->items, MAX_MOCHILA);
    for (int i = 0; i < p->items; i++) {
        printf(" [%s]", p->mochila[i]);
    }
    printf("\n");
}
```

### Misión R02-N05-M2 · El duelo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Dos `Luchador` (vida, ataque, defensa) pelean por turnos con
`srand(7)`: daño = ataque + tirada de 0 a 5 − defensa (mínimo 1; con 5, el
doble). `duelo(&a, &b)` devuelve un puntero al ganador. Para alternar
turnos, intercambiá dos punteros `atacante` y `defensor`.

#### Criterio de aprobación

- Usa `srand(7)` y la regla de daño (mínimo 1; el doble con 5).
- `duelo(&a, &b)` devuelve un puntero al ganador.
- Alterna turnos intercambiando los punteros `atacante` y `defensor`.

#### Salida esperada

```
ronda 1
  Kira pega 10 -> Gólem queda con 70
  Gólem pega 10 -> Kira queda con 50
ronda 2
  Kira pega 24 (¡crítico!) -> Gólem queda con 46
  Gólem pega  8 -> Kira queda con 42
ronda 3
  Kira pega 24 (¡crítico!) -> Gólem queda con 22
  Gólem pega 10 -> Kira queda con 32
ronda 4
  Kira pega  9 -> Gólem queda con 13
  Gólem pega  8 -> Kira queda con 24
ronda 5
  Kira pega  7 -> Gólem queda con 6
  Gólem pega  8 -> Kira queda con 16
ronda 6
  Kira pega 24 (¡crítico!) -> Gólem queda con 0
Gana Kira con 16 de vida.
```

#### Solución de referencia

```c
/*
 * Mision 2 - El duelo: dos personajes pelean por turnos con tiradas al
 * azar (semilla fija). duelo() devuelve un puntero al ganador.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    char nombre[16];
    int  vida;
    int  ataque;
    int  defensa;
} Luchador;

int  tirar(int minimo, int maximo);
void turno(const Luchador *atacante, Luchador *defensor);
const Luchador *duelo(Luchador *a, Luchador *b);

int main(void)
{
    srand(7);
    Luchador kira = { "Kira", 60, 14, 4 };
    Luchador golem = { "Gólem", 80, 11, 7 };

    const Luchador *ganador = duelo(&kira, &golem);
    printf("Gana %s con %d de vida.\n", ganador->nombre, ganador->vida);
    return 0;
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

/* Danio = ataque + tirada de 0 a 5 - defensa (minimo 1). Con 5 en la tirada, critico x2. */
void turno(const Luchador *atacante, Luchador *defensor)
{
    int tirada = tirar(0, 5);
    int danio = atacante->ataque + tirada - defensor->defensa;
    if (danio < 1) {
        danio = 1;
    }
    if (tirada == 5) {
        danio *= 2;
    }
    defensor->vida -= danio;
    if (defensor->vida < 0) {
        defensor->vida = 0;
    }
    printf("  %s pega %2d%s -> %s queda con %d\n", atacante->nombre, danio,
           tirada == 5 ? " (¡crítico!)" : "", defensor->nombre, defensor->vida);
}

const Luchador *duelo(Luchador *a, Luchador *b)
{
    Luchador *atacante = a;
    Luchador *defensor = b;
    int ronda = 1;
    while (a->vida > 0 && b->vida > 0) {
        if (atacante == a) {
            printf("ronda %d\n", ronda);
            ronda++;
        }
        turno(atacante, defensor);
        Luchador *tmp = atacante;      /* se turnan: se intercambian los punteros */
        atacante = defensor;
        defensor = tmp;
    }
    return a->vida > 0 ? a : b;
}
```

### Misión R02-N05-M3 · Subir de nivel

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

`ganar_experiencia(Personaje *p, int xp)` suma la
experiencia y sube de nivel cada vez que alcanza `nivel × 100` (más vida y
ataque). Devuelve cuántos niveles subió: puede ser más de uno de golpe.

#### Criterio de aprobación

- `ganar_experiencia` sube de nivel cada vez que alcanza `nivel × 100`.
- Puede subir más de un nivel de golpe (usa un bucle).
- Devuelve cuántos niveles subió.

#### Salida esperada

```
  Chispa nivel 1 (0/100 xp)  vida 50  ataque 8
+60 xp
  Chispa nivel 1 (60/100 xp)  vida 50  ataque 8
+150 xp -> ¡subió 1 nivel!
  Chispa nivel 2 (110/200 xp)  vida 60  ataque 10
+30 xp
  Chispa nivel 2 (140/200 xp)  vida 60  ataque 10
+400 xp -> ¡subió 2 niveles!
  Chispa nivel 4 (40/400 xp)  vida 80  ataque 14
```

#### Solución de referencia

```c
/*
 * Mision 3 - Subir de nivel: ganar_experiencia modifica al personaje y
 * devuelve cuantos niveles subio (puede ser mas de uno de golpe).
 */
#include <stdio.h>

typedef struct {
    char nombre[16];
    int  nivel;
    int  xp;
    int  vida_max;
    int  ataque;
} Personaje;

int  xp_para_subir(int nivel);
int  ganar_experiencia(Personaje *p, int xp);
void mostrar(const Personaje *p);

int main(void)
{
    Personaje chispa = { "Chispa", 1, 0, 50, 8 };
    int botines[] = { 60, 150, 30, 400 };

    mostrar(&chispa);
    for (int i = 0; i < 4; i++) {
        int subio = ganar_experiencia(&chispa, botines[i]);
        printf("+%d xp", botines[i]);
        if (subio > 0) {
            printf(" -> ¡subió %d nivel%s!", subio, subio > 1 ? "es" : "");
        }
        printf("\n");
        mostrar(&chispa);
    }
    return 0;
}

/* Cada nivel pide 100 xp mas que el anterior: 100, 200, 300... */
int xp_para_subir(int nivel)
{
    return nivel * 100;
}

int ganar_experiencia(Personaje *p, int xp)
{
    int niveles = 0;
    p->xp += xp;
    while (p->xp >= xp_para_subir(p->nivel)) {
        p->xp -= xp_para_subir(p->nivel);
        p->nivel++;
        p->vida_max += 10;
        p->ataque += 2;
        niveles++;
    }
    return niveles;
}

void mostrar(const Personaje *p)
{
    printf("  %s nivel %d (%d/%d xp)  vida %d  ataque %d\n", p->nombre, p->nivel, p->xp,
           xp_para_subir(p->nivel), p->vida_max, p->ataque);
}
```

### Encargo R02-N05-E1 · El banco del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El banco del Gremio necesita un struct `Cuenta` (titular, saldo, cantidad de
movimientos) y las funciones `depositar`, `extraer` (falla si no alcanza el
saldo o el monto no es positivo) y `transferir(origen, destino, monto)`, que
solo deposita si pudo extraer. Probá una transferencia que funcione y otra que
no.

#### Criterio de aprobación

- `Cuenta` con titular, saldo y movimientos.
- `extraer` falla si no alcanza o el monto no es positivo.
- `transferir` solo deposita si pudo extraer; prueba una que funciona y otra que no.

#### Salida esperada

```
Beto extrae 3000: saldo insuficiente
Ana transfiere 7500 a Beto: ok
Beto deposita -50: monto inválido
Beto transfiere 20000 a Ana: no
Ana Pérez: $12500.00 (2 movimientos)
Beto Gómez: $9500.00 (1 movimientos)
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - Cuentas del banco: depositar, extraer y transferir
 * modificando las cuentas por puntero. Las operaciones que pueden fallar
 * devuelven bool.
 */
#include <stdio.h>
#include <stdbool.h>

typedef struct {
    char   titular[24];
    double saldo;
    int    movimientos;
} Cuenta;

bool depositar(Cuenta *c, double monto);
bool extraer(Cuenta *c, double monto);
bool transferir(Cuenta *origen, Cuenta *destino, double monto);
void mostrar(const Cuenta *c);

int main(void)
{
    Cuenta ana = { "Ana Pérez", 15000, 0 };
    Cuenta beto = { "Beto Gómez", 2000, 0 };

    depositar(&ana, 5000);
    printf("Beto extrae 3000: %s\n", extraer(&beto, 3000) ? "ok" : "saldo insuficiente");
    printf("Ana transfiere 7500 a Beto: %s\n", transferir(&ana, &beto, 7500) ? "ok" : "no");
    printf("Beto deposita -50: %s\n", depositar(&beto, -50) ? "ok" : "monto inválido");
    printf("Beto transfiere 20000 a Ana: %s\n", transferir(&beto, &ana, 20000) ? "ok" : "no");
    mostrar(&ana);
    mostrar(&beto);
    return 0;
}

bool depositar(Cuenta *c, double monto)
{
    if (monto <= 0) {
        return false;
    }
    c->saldo += monto;
    c->movimientos++;
    return true;
}

bool extraer(Cuenta *c, double monto)
{
    if (monto <= 0 || monto > c->saldo) {
        return false;
    }
    c->saldo -= monto;
    c->movimientos++;
    return true;
}

/* Solo deposita si pudo extraer: la plata no aparece ni desaparece */
bool transferir(Cuenta *origen, Cuenta *destino, double monto)
{
    if (!extraer(origen, monto)) {
        return false;
    }
    depositar(destino, monto);
    return true;
}

void mostrar(const Cuenta *c)
{
    printf("%s: $%.2f (%d movimientos)\n", c->titular, c->saldo, c->movimientos);
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre `void f(Personaje p)` y `void f(Personaje *p)`?

La primera recibe una copia del struct; la segunda, su dirección: puede cambiar el original y no copia nada.

#### ¿Qué significa `p->oro`? ¿Por qué `*p.oro` no funciona?

El campo `oro` del struct al que apunta `p` (es `(*p).oro`). `*p.oro` no funciona porque el punto se aplica antes que el `*`.

#### ¿Cuándo va punto y cuándo va flecha?

Punto con un struct; flecha con un puntero a struct.

#### ¿Qué gana una función al recibir `const Personaje *` en lugar de `Personaje *`?

Promete (y el compilador lo hace cumplir) que no lo va a modificar, y acepta tanto datos modificables como constantes.

#### En `atacar(const Personaje *atacante, Personaje *objetivo)`, ¿por qué dentro se llama `recibir_danio(objetivo, ...)` sin `&`?

Porque `objetivo` ya es un puntero: se pasa tal cual.

#### ¿Por qué `personaje_crear` puede devolver el struct por valor sin problema?

Porque lo devuelve como una copia completa: el struct no depende de ninguna variable local que desaparezca.

### Soluciones (docente)

Material original: `01-C/14-PunterosYStructs` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R02-N06 · Arrays de structs

```meta
tipo: tema
criatura: orco
padre: R02-N05
precio: 10
temas: alg.busqueda, alg.ordenamiento
usa: col.registros, col.arrays
```

### Crónica

El registro de la Forja no es una ficha: es un **estante** de fichas, con lugar para cinco. Cuando llega alguien nuevo, va al primer hueco; cuando alguien se va, los de atrás se corren.

Cada tanto {mentor} pide el estante ordenado: por fuerza para armar la guardia, por nombre para pasar lista.

—No hace falta ordenar a mano cada vez —dice, y saca de un cajón un autómata de bronce que ordena cualquier cosa… si le explicás cómo comparar.

### Objetivos

Manejar una **colección de entidades** con un array de structs: agregar con
capacidad fija, buscar (devolviendo un puntero o `NULL`), quitar corriendo los
elementos, recorrer con un puntero, ordenar a mano y con **`qsort`**.

### Antes de empezar

- Arrays a medio llenar: capacidad y cantidad (10).
- Structs (12); punteros a struct y `->` (14).
- `strcmp` (11).

### Explicación

#### La colección y su cantidad, juntas
```c
typedef struct {
    Heroe miembros[MAX_MIEMBROS];
    int   cantidad;
} Compania;
```
El array y su cantidad van **siempre juntos**: si se pasan por separado, tarde o
temprano alguien actualiza uno y no el otro. Metiéndolos en un struct, cada
función recibe un solo `Compania *` y listo. `miembros[i]` es un `Heroe`, así
que se llega a sus campos con `c->miembros[i].nombre`.

#### Las cuatro operaciones
| Operación | Cómo |
|---|---|
| **agregar** | si `cantidad < MAX`, llenar `miembros[cantidad]` y sumar 1 |
| **buscar** | recorrer comparando; devolver `&miembros[i]` o `NULL` (13) |
| **quitar** | buscar la posición y correr **un lugar hacia adelante** todos los de atrás (`miembros[j] = miembros[j + 1]`, 12); restar 1 |
| **recorrer** | con índice, o con un puntero de `miembros` a `miembros + cantidad` |

`buscar` devuelve un **puntero** al elemento, no una copia: con él se modifica
el héroe que está en el array (`tizon->vida -= 60`). Ese puntero deja de ser
válido si después se quita o se ordena: los elementos cambian de lugar.

#### Ordenar a mano: selección
En cada vuelta se busca el **mayor** de lo que falta ordenar y se lo
**intercambia** con el primero de esa parte:
```
30 12 25 18  →  busca el mayor (30): ya está primero
30 | 12 25 18  →  el mayor de lo que falta es 25: intercambia con 12
30 25 | 12 18  →  18: intercambia con 12
30 25 18 12
```
Hacerlo una vez a mano ayuda a entender que ordenar no es magia. Para el día a
día, está `qsort`.

#### Ordenar a mano: burbuja
Se recorre el array comparando cada par **vecino**; si están al revés, se
intercambian. Después de cada pasada, el mayor «sube» hasta el final como una
burbuja. Si en una pasada no hubo ningún cambio, ya está ordenado:
```c
for (int pasada = 0; pasada < n - 1; pasada++) {
    bool cambio = false;
    for (int i = 0; i < n - 1 - pasada; i++) {
        if (v[i] > v[i + 1]) {
            int aux = v[i]; v[i] = v[i + 1]; v[i + 1] = aux;
            cambio = true;
        }
    }
    if (!cambio) break;
}
```
Con structs se intercambia el struct **entero** (`Heroe aux = h[i]; …`): así
cada nombre se mueve junto con sus datos.

#### Ordenar con desempate
Los parciales piden cosas como «por promedio **descendente** y, si empatan, por
nombre **ascendente**». Se escribe una función que diga si `a` va **antes** que
`b`, y se usa en la burbuja (o en la selección) en lugar del `>`:
```c
bool va_antes(const Alumno *a, const Alumno *b)
{
    if (a->promedio != b->promedio) {
        return a->promedio > b->promedio;          /* mayor promedio primero */
    }
    return strcmp(a->nombre, b->nombre) < 0;       /* empate: alfabético */
}
...
if (va_antes(&v[i + 1], &v[i])) { /* intercambiar */ }
```

#### Ordenar sin perder la referencia
Si se ordena un array suelto de promedios, se pierde **de quién** era cada uno.
Dos salidas:
- ordenar un array de **structs** `{máquina, promedio}` (el número viaja con su
  promedio);
- o ordenar un array de **índices** (`orden[] = {0, 1, 2, 3}`) comparando
  `promedio[orden[i]]`, sin tocar los datos originales.

#### `qsort`: el ordenador de la biblioteca
`qsort` (de `stdlib.h`) ordena **cualquier** array, de cualquier tipo. Como no
sabe qué hay adentro, le hay que decir cuatro cosas:
```c
qsort(compania.miembros,      /* 1) dónde empieza el array            */
      compania.cantidad,      /* 2) cuántos elementos                  */
      sizeof(Heroe),          /* 3) cuántos bytes ocupa cada uno       */
      comparar_por_nombre);   /* 4) una función que compara dos        */
```
El cuarto argumento es el **nombre de una función, sin paréntesis**: no se la
llama, se le **pasa** a `qsort` para que la llame ella cada vez que necesite
comparar dos elementos. (Pasar funciones como datos se ve a fondo en el 20.)

La función de comparación tiene que tener exactamente esta forma:
```c
int comparar_por_nombre(const void *a, const void *b)
{
    const Heroe *ha = a;          /* convertir al tipo real */
    const Heroe *hb = b;
    return strcmp(ha->nombre, hb->nombre);
}
```
- **`void *`** es un "puntero a cualquier cosa": `qsort` no sabe el tipo, así
  que le pasa las direcciones de los dos elementos como `const void *`. Lo
  primero es guardarlas en punteros del tipo real.
- Devuelve lo mismo que `strcmp`: **negativo** si `a` va antes, **0** si da
  igual, **positivo** si va después.
- Para ordenar **al revés**, se invierte el resultado (`y - x` en lugar de
  `x - y`).
- Para **dos criterios**, si el primero empata se compara el segundo (misión 2).
- Con números, `x - y` puede **desbordar** si son muy grandes o muy chicos, y
  con `double` los decimales se pierden al convertir a `int`. La forma segura es
  `(x > y) - (x < y)`, que da -1, 0 o 1.

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`

### Código de ejemplo

```c
/*
 * 15 - Arrays de structs: una coleccion de entidades con capacidad fija.
 * Agregar, buscar, quitar, recorrer con puntero, ordenar a mano y con qsort.
 *
 *   make run
 */
#include <stdio.h>
#include <stdlib.h>    /* qsort */
#include <string.h>
#include <stdbool.h>

#define MAX_MIEMBROS 5

typedef struct {
    char nombre[16];
    int  vida;
    int  ataque;
} Heroe;

/* La coleccion y su cantidad viajan juntas en un struct */
typedef struct {
    Heroe miembros[MAX_MIEMBROS];
    int   cantidad;
} Compania;

bool   agregar(Compania *c, const char *nombre, int vida, int ataque);
Heroe *buscar(Compania *c, const char *nombre);
bool   quitar(Compania *c, const char *nombre);
int    vida_total(const Compania *c);
void   ordenar_por_ataque(Compania *c);
int    comparar_enteros(const void *a, const void *b);
int    comparar_por_nombre(const void *a, const void *b);
void   mostrar(const Compania *c);

int main(void)
{
    Compania compania = { .cantidad = 0 };

    agregar(&compania, "Kira", 100, 18);
    agregar(&compania, "Hulda", 70, 25);
    agregar(&compania, "Tizon", 140, 12);
    agregar(&compania, "Chispa", 80, 30);
    agregar(&compania, "Ferrum", 160, 22);
    if (!agregar(&compania, "Nyx", 60, 20)) {
        printf("la compañía está completa: Nyx no entra\n");
    }
    mostrar(&compania);
    printf("vida total: %d\n", vida_total(&compania));

    /* --- Buscar: devuelve un puntero al elemento, o NULL --- */
    Heroe *tizon = buscar(&compania, "Tizon");
    if (tizon != NULL) {
        tizon->vida -= 60;                        /* cambia el que esta en el array */
        printf("\nBron recibe 60 de daño: le quedan %d\n", compania.miembros[2].vida);
    }
    printf("¿está Nyx? %s\n", buscar(&compania, "Nyx") != NULL ? "sí" : "no");

    /* --- Quitar: los de atras se corren un lugar --- */
    quitar(&compania, "Hulda");
    printf("\nMia vuelve a la torre:\n");
    mostrar(&compania);

    /* --- Ordenar a mano (seleccion) --- */
    ordenar_por_ataque(&compania);
    printf("\nordenada por ataque, de mayor a menor (a mano):\n");
    mostrar(&compania);

    /* --- Ordenar con qsort: primero un array de int... --- */
    int tiradas[] = { 14, 3, 20, 8, 11 };
    int n = sizeof(tiradas) / sizeof(tiradas[0]);
    qsort(tiradas, n, sizeof(tiradas[0]), comparar_enteros);
    printf("\ntiradas ordenadas con qsort:");
    for (int i = 0; i < n; i++) {
        printf(" %d", tiradas[i]);
    }
    printf("\n");

    /* --- ...y despues el array de structs, por nombre --- */
    qsort(compania.miembros, compania.cantidad, sizeof(Heroe), comparar_por_nombre);
    printf("ordenada por nombre (con qsort):\n");
    mostrar(&compania);
    return 0;
}

bool agregar(Compania *c, const char *nombre, int vida, int ataque)
{
    if (c->cantidad == MAX_MIEMBROS) {
        return false;
    }
    Heroe *nuevo = &c->miembros[c->cantidad];    /* el primer lugar libre */
    snprintf(nuevo->nombre, sizeof(nuevo->nombre), "%s", nombre);
    nuevo->vida = vida;
    nuevo->ataque = ataque;
    c->cantidad++;
    return true;
}

Heroe *buscar(Compania *c, const char *nombre)
{
    for (int i = 0; i < c->cantidad; i++) {
        if (strcmp(c->miembros[i].nombre, nombre) == 0) {
            return &c->miembros[i];
        }
    }
    return NULL;
}

bool quitar(Compania *c, const char *nombre)
{
    for (int i = 0; i < c->cantidad; i++) {
        if (strcmp(c->miembros[i].nombre, nombre) == 0) {
            for (int j = i; j < c->cantidad - 1; j++) {
                c->miembros[j] = c->miembros[j + 1];   /* los structs se copian con = */
            }
            c->cantidad--;
            return true;
        }
    }
    return false;
}

int vida_total(const Compania *c)
{
    int suma = 0;
    /* recorrer con un puntero: h va de &miembros[0] hasta el ultimo usado */
    for (const Heroe *h = c->miembros; h < c->miembros + c->cantidad; h++) {
        suma += h->vida;
    }
    return suma;
}

/* Seleccion: en cada vuelta, busca el mayor de lo que falta y lo trae adelante */
void ordenar_por_ataque(Compania *c)
{
    for (int i = 0; i < c->cantidad - 1; i++) {
        int mejor = i;
        for (int j = i + 1; j < c->cantidad; j++) {
            if (c->miembros[j].ataque > c->miembros[mejor].ataque) {
                mejor = j;
            }
        }
        if (mejor != i) {
            Heroe tmp = c->miembros[i];
            c->miembros[i] = c->miembros[mejor];
            c->miembros[mejor] = tmp;
        }
    }
}

/* qsort le pasa punteros a dos elementos como const void *.
   Hay que convertirlos al tipo real. Devuelve <0, 0 o >0 (como strcmp). */
int comparar_enteros(const void *a, const void *b)
{
    int x = *(const int *) a;
    int y = *(const int *) b;
    return (x > y) - (x < y);                   /* evita el desborde de x - y */
}

int comparar_por_nombre(const void *a, const void *b)
{
    const Heroe *ha = a;
    const Heroe *hb = b;
    return strcmp(ha->nombre, hb->nombre);
}

void mostrar(const Compania *c)
{
    for (int i = 0; i < c->cantidad; i++) {
        const Heroe *h = &c->miembros[i];
        printf("  %d. %-7s vida %3d  ataque %2d\n", i + 1, h->nombre, h->vida, h->ataque);
    }
}
```

### Salida esperada

```
la compañía está completa: Nyx no entra
  1. Kira    vida 100  ataque 18
  2. Hulda   vida  70  ataque 25
  3. Tizon   vida 140  ataque 12
  4. Chispa  vida  80  ataque 30
  5. Ferrum  vida 160  ataque 22
vida total: 550

Bron recibe 60 de daño: le quedan 80
¿está Nyx? no

Mia vuelve a la torre:
  1. Kira    vida 100  ataque 18
  2. Tizon   vida  80  ataque 12
  3. Chispa  vida  80  ataque 30
  4. Ferrum  vida 160  ataque 22

ordenada por ataque, de mayor a menor (a mano):
  1. Chispa  vida  80  ataque 30
  2. Ferrum  vida 160  ataque 22
  3. Kira    vida 100  ataque 18
  4. Tizon   vida  80  ataque 12

tiradas ordenadas con qsort: 3 8 11 14 20
ordenada por nombre (con qsort):
  1. Chispa  vida  80  ataque 30
  2. Ferrum  vida 160  ataque 22
  3. Kira    vida 100  ataque 18
  4. Tizon   vida  80  ataque 12
```

### ¿Para qué sirve?

Un array de structs es una tabla en memoria: los productos de una ferretería, los turnos de un consultorio, los enemigos de un nivel. Buscar, agregar sin repetir, quitar y ordenar son las operaciones de todo sistema de gestión, y `qsort` con una función de comparación es la misma idea que el "ordenar por columna" de una planilla.

### Errores habituales

Mensajes reales de `gcc` 13 con `-Wall -Wextra`.

**Goblin: la función de comparación con el tipo real en los parámetros.**
Tiene que recibir `const void *`:
```
w1.c:10:32: warning: passing argument 4 of ‘qsort’ from incompatible pointer type [-Wincompatible-pointer-types]
   10 |     qsort(h, 3, sizeof(Heroe), comparar);
      |                                ^~~~~~~~
      |                                |
      |                                int (*)(const Heroe *, const Heroe *)
/usr/include/stdlib.h:971:34: note: expected ‘__compar_fn_t’ {aka ‘int (*)(const void *, const void *)’} but argument is of type ‘int (*)(const Heroe *, const Heroe *)’
```
(`int (*)(...)` es como C escribe el tipo "puntero a función": se ve en el 20.)

**Goblin: llamar a la función en lugar de pasarla.** Con paréntesis, se la
llama en el acto:
```
w1.c:11:32: error: too few arguments to function ‘comparar’
   11 |     qsort(h, 3, sizeof(Heroe), comparar());
      |                                ^~~~~~~~
```

**Ogro: el tamaño equivocado.** `qsort(v, 4, sizeof(char), comparar)` sobre un
array de `int` compila sin avisos y **no ordena**: `qsort` cree que cada
elemento ocupa 1 byte.
```
5 2 9 1
```
Usá siempre `sizeof(v[0])` o `sizeof(Tipo)`.

**Ogro: quitar sin correr.** Si solo se resta `cantidad`, se pierde el
**último** elemento, no el que se quería quitar.

**Orco: agregar sin mirar la capacidad.** `miembros[cantidad]` con
`cantidad == MAX` escribe fuera del array (`make asan` lo atrapa).

**Troll: el puntero viejo.** Guardar el puntero que devolvió `buscar`, después
quitar u ordenar, y seguir usándolo: ahora apunta a **otro** héroe.

### Misión R02-N06-M1 · El tablero de récords

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Guardá los 5 mejores puntajes **siempre
ordenados** de mayor a menor. `insertar(&tablero, nombre, puntos)` busca la
posición, corre hacia atrás los de abajo (el último se cae si está lleno) y
devuelve el puesto, o `-1` si no entró.

#### Criterio de aprobación

- El tablero queda siempre ordenado de mayor a menor.
- `insertar` corre hacia atrás los de abajo; si está lleno, el último se cae.
- Devuelve el puesto o `-1`.

#### Salida esperada

```
Kira   420: entra en el puesto 1
Chispa 380: entra en el puesto 2
Hulda  510: entra en el puesto 1
Tizon  150: entra en el puesto 4
Nyx     90: entra en el puesto 5
Kira   600: entra en el puesto 1
Ferrum 200: entra en el puesto 5

  1. Kira    600
  2. Hulda   510
  3. Kira    420
  4. Chispa  380
  5. Ferrum  200
```

#### Solución de referencia

```c
/*
 * Mision 1 - El tablero de records: guarda los 5 mejores puntajes, siempre
 * ordenados de mayor a menor. Al insertar, los de abajo se corren y el
 * ultimo se cae del tablero.
 */
#include <stdio.h>

#define TOP 5

typedef struct {
    char nombre[12];
    int  puntos;
} Record;

typedef struct {
    Record lista[TOP];
    int    cantidad;
} Tablero;

int  insertar(Tablero *t, const char *nombre, int puntos);
void mostrar(const Tablero *t);

int main(void)
{
    Tablero tablero = { .cantidad = 0 };
    const char *nombres[] = { "Kira", "Chispa", "Hulda", "Tizon", "Nyx", "Kira", "Ferrum" };
    int puntos[] = { 420, 380, 510, 150, 90, 600, 200 };

    for (int i = 0; i < 7; i++) {
        int pos = insertar(&tablero, nombres[i], puntos[i]);
        if (pos == -1) {
            printf("%-6s %3d: no entra al tablero\n", nombres[i], puntos[i]);
        } else {
            printf("%-6s %3d: entra en el puesto %d\n", nombres[i], puntos[i], pos + 1);
        }
    }
    printf("\n");
    mostrar(&tablero);
    return 0;
}

/* Devuelve la posicion donde quedo, o -1 si no entro */
int insertar(Tablero *t, const char *nombre, int puntos)
{
    int pos = 0;
    while (pos < t->cantidad && t->lista[pos].puntos >= puntos) {
        pos++;
    }
    if (pos == TOP) {
        return -1;                            /* peor que todos, y el tablero esta lleno */
    }
    if (t->cantidad < TOP) {
        t->cantidad++;
    }
    for (int i = t->cantidad - 1; i > pos; i--) {
        t->lista[i] = t->lista[i - 1];        /* de atras hacia adelante */
    }
    snprintf(t->lista[pos].nombre, sizeof(t->lista[pos].nombre), "%s", nombre);
    t->lista[pos].puntos = puntos;
    return pos;
}

void mostrar(const Tablero *t)
{
    for (int i = 0; i < t->cantidad; i++) {
        printf("  %d. %-6s %4d\n", i + 1, t->lista[i].nombre, t->lista[i].puntos);
    }
}
```

### Misión R02-N06-M2 · La armería

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con un array de armas (nombre, daño, peso): mostrá las que
pesan menos de 3 kg, buscá la de mejor daño por kilo (devolviendo un
puntero) y ordenalas con `qsort` por daño de mayor a menor y, si empatan,
por nombre.

#### Criterio de aprobación

- Muestra las armas de menos de 3 kg.
- Devuelve un puntero a la de mejor daño por kilo.
- Ordena con `qsort` por daño de mayor a menor y, si empatan, por nombre.

#### Salida esperada

```
livianas (menos de 3 kg): Daga Estoque
mejor daño por kilo: Estoque (11.7)
por daño:
  Hacha    28  6.0 kg
  Espada   20  3.5 kg
  Maza     20  5.0 kg
  Lanza    18  3.0 kg
  Estoque  14  1.2 kg
  Daga      9  0.8 kg
```

#### Solución de referencia

```c
/*
 * Mision 2 - La armeria: filtrar, buscar la mejor relacion danio/peso y
 * ordenar con qsort por dos criterios (danio de mayor a menor y, si empatan,
 * por nombre).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char   nombre[16];
    int    danio;
    double peso;
} Arma;

int  comparar_armas(const void *a, const void *b);
const Arma *mejor_relacion(const Arma armas[], int n);

int main(void)
{
    Arma armas[] = {
        { "Hacha", 28, 6.0 }, { "Daga", 9, 0.8 },   { "Espada", 20, 3.5 },
        { "Maza", 20, 5.0 },  { "Lanza", 18, 3.0 }, { "Estoque", 14, 1.2 },
    };
    int n = sizeof(armas) / sizeof(armas[0]);

    printf("livianas (menos de 3 kg):");
    for (int i = 0; i < n; i++) {
        if (armas[i].peso < 3.0) {
            printf(" %s", armas[i].nombre);
        }
    }
    printf("\n");

    const Arma *mejor = mejor_relacion(armas, n);
    printf("mejor daño por kilo: %s (%.1f)\n", mejor->nombre, mejor->danio / mejor->peso);

    qsort(armas, n, sizeof(Arma), comparar_armas);
    printf("por daño:\n");
    for (int i = 0; i < n; i++) {
        printf("  %-8s %2d  %.1f kg\n", armas[i].nombre, armas[i].danio, armas[i].peso);
    }
    return 0;
}

int comparar_armas(const void *a, const void *b)
{
    const Arma *x = a;
    const Arma *y = b;
    if (x->danio != y->danio) {
        return y->danio - x->danio;           /* al reves: de mayor a menor */
    }
    return strcmp(x->nombre, y->nombre);      /* empate: alfabetico */
}

const Arma *mejor_relacion(const Arma armas[], int n)
{
    const Arma *mejor = &armas[0];
    for (int i = 1; i < n; i++) {
        if (armas[i].danio / armas[i].peso > mejor->danio / mejor->peso) {
            mejor = &armas[i];
        }
    }
    return mejor;
}
```

### Misión R02-N06-M3 · El registro con menú

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un menú que agrega (sin repetir nombres ni pasarse
de la capacidad), busca, quita y lista miembros de la compañía, validando
todo con `pedir_entero` (del 13) y un `pedir_texto` que no acepte líneas
vacías.

#### Criterio de aprobación

- Menú para agregar, buscar, quitar y listar.
- No repite nombres ni se pasa de la capacidad.
- Valida todo con `pedir_entero` y un `pedir_texto` que no acepta vacíos.

#### Entrada de ejemplo

```
1
Kira
7
1
Tizon
doce
12
1
Kira
3
9
1

Hulda
6
1
4
2
Tizon
3
Kira
3
Chispa
4
0
```

#### Salida esperada

```
1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: Nivel (1-99): Se sumó Kira.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: Nivel (1-99): 
  tiene que ser un número entre 1 y 99.
Nivel (1-99): Se sumó Tizon.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: Nivel (1-99): Kira ya está en la compañía.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: 
  tiene que ser un número entre 0 y 4.
Opción: Nombre: 
  no puede estar vacío.
Nombre: Nivel (1-99): Se sumó Hulda.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: La compañía está completa.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción:   1. Kira (nivel 7)
  2. Tizon (nivel 12)
  3. Hulda (nivel 6)

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: Tizon está en el puesto 2, nivel 12.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: Kira dejó la compañía.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: No hay nadie llamado Chispa.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción:   1. Tizon (nivel 12)
  2. Hulda (nivel 6)

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: ¡Hasta la próxima!
```

#### Solución de referencia

```c
/*
 * Mision 3 - El registro de la compania, con menu: agregar, buscar, quitar,
 * listar y salir. Todo validado con pedir_entero y pedir_texto.
 * Probar con:  ./sol < mision3_registro.entrada.txt
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_MIEMBROS 3

typedef struct {
    char nombre[16];
    int  nivel;
} Miembro;

typedef struct {
    Miembro miembros[MAX_MIEMBROS];
    int     cantidad;
} Compania;

bool pedir_entero(const char *pregunta, int minimo, int maximo, int *resultado);
bool pedir_texto(const char *pregunta, char destino[], int tam);
int  posicion(const Compania *c, const char *nombre);

int main(void)
{
    Compania c = { .cantidad = 0 };
    int opcion = -1;
    while (opcion != 0) {
        printf("\n1) agregar  2) buscar  3) quitar  4) listar  0) salir\n");
        if (!pedir_entero("Opción: ", 0, 4, &opcion)) {
            break;
        }
        char nombre[16];
        int nivel, pos;
        switch (opcion) {
            case 1:
                if (c.cantidad == MAX_MIEMBROS) {
                    printf("La compañía está completa.\n");
                } else if (pedir_texto("Nombre: ", nombre, sizeof(nombre)) &&
                           pedir_entero("Nivel (1-99): ", 1, 99, &nivel)) {
                    if (posicion(&c, nombre) != -1) {
                        printf("%s ya está en la compañía.\n", nombre);
                    } else {
                        Miembro *m = &c.miembros[c.cantidad];
                        snprintf(m->nombre, sizeof(m->nombre), "%s", nombre);
                        m->nivel = nivel;
                        c.cantidad++;
                        printf("Se sumó %s.\n", nombre);
                    }
                }
                break;
            case 2:
            case 3:
                if (!pedir_texto("Nombre: ", nombre, sizeof(nombre))) {
                    break;
                }
                pos = posicion(&c, nombre);
                if (pos == -1) {
                    printf("No hay nadie llamado %s.\n", nombre);
                } else if (opcion == 2) {
                    printf("%s está en el puesto %d, nivel %d.\n", nombre, pos + 1,
                           c.miembros[pos].nivel);
                } else {
                    for (int i = pos; i < c.cantidad - 1; i++) {
                        c.miembros[i] = c.miembros[i + 1];
                    }
                    c.cantidad--;
                    printf("%s dejó la compañía.\n", nombre);
                }
                break;
            case 4:
                if (c.cantidad == 0) {
                    printf("(vacía)\n");
                }
                for (int i = 0; i < c.cantidad; i++) {
                    printf("  %d. %s (nivel %d)\n", i + 1, c.miembros[i].nombre,
                           c.miembros[i].nivel);
                }
                break;
        }
    }
    printf("¡Hasta la próxima!\n");
    return 0;
}

bool pedir_entero(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  tiene que ser un número entre %d y %d.\n", minimo, maximo);
    }
}

/* Lee una linea no vacia, sin el Enter */
bool pedir_texto(const char *pregunta, char destino[], int tam)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        linea[strcspn(linea, "\n")] = '\0';
        if (linea[0] != '\0') {
            snprintf(destino, (size_t) tam, "%s", linea);
            return true;
        }
        printf("\n  no puede estar vacío.\n");
    }
}

int posicion(const Compania *c, const char *nombre)
{
    for (int i = 0; i < c->cantidad; i++) {
        if (strcmp(c->miembros[i].nombre, nombre) == 0) {
            return i;
        }
    }
    return -1;
}
```

#### Pruebas

##### Listar vacío y salir
```entrada
4
0
```
```salida
1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: (vacía)

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: ¡Hasta la próxima!
```

##### Buscar y quitar lo que no está
```entrada
2
Nadie
3
Nadie
0
```
```salida
1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: No hay nadie llamado Nadie.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: No hay nadie llamado Nadie.

1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: ¡Hasta la próxima!
```

##### Se termina la entrada
```entrada
1
Kira
```
```salida
1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: Nombre: Nivel (1-99):
1) agregar  2) buscar  3) quitar  4) listar  0) salir
Opción: ¡Hasta la próxima!
```

### Misión R02-N06-M4 · El cuadro de honor

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Ferrum quiere colgar en la pared el **cuadro de honor** de los aprendices.
Cargá en un array de structs a Kira (8, 9, 7), Tizon (9, 9, 6), Hulda (10, 6, 8),
Chispa (5, 6, 4) y Brasa (9, 9, 8), con sus tres notas de temple; calculá el
promedio de cada uno y ordená con **burbuja** por promedio **descendente** y, si
empatan, por nombre **ascendente**. Mostrá el cuadro numerado con el promedio
con dos decimales.

#### Criterio de aprobación

- Usa un array de structs (nombre, notas y promedio) y una función que calcula el promedio.
- Ordena con burbuja usando una función de comparación con desempate por nombre (`strcmp`).
- Kira, Hulda y Tizon empatan en 8.00 y quedan en orden alfabético.

#### Salida esperada

```
CUADRO DE HONOR DE LA FORJA
1. Brasa    8.67
2. Hulda    8.00
3. Kira     8.00
4. Tizon    8.00
5. Chispa   5.00
```

#### Solución de referencia

```c
/*
 * Mision 4 - El cuadro de honor: ordenar structs con burbuja, por promedio
 * descendente y, si empatan, por nombre ascendente.
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define CANT 5

typedef struct {
    char nombre[12];
    int notas[3];
    double promedio;
} Aprendiz;

double promedio(const int notas[3])
{
    return (notas[0] + notas[1] + notas[2]) / 3.0;
}

bool va_antes(const Aprendiz *a, const Aprendiz *b)
{
    if (a->promedio != b->promedio) {
        return a->promedio > b->promedio;
    }
    return strcmp(a->nombre, b->nombre) < 0;
}

void ordenar(Aprendiz v[], int n)
{
    for (int pasada = 0; pasada < n - 1; pasada++) {
        bool cambio = false;
        for (int i = 0; i < n - 1 - pasada; i++) {
            if (va_antes(&v[i + 1], &v[i])) {
                Aprendiz aux = v[i];
                v[i] = v[i + 1];
                v[i + 1] = aux;
                cambio = true;
            }
        }
        if (!cambio) {
            break;
        }
    }
}

int main(void)
{
    Aprendiz v[CANT] = {
        { "Kira", { 8, 9, 7 }, 0 }, { "Tizon", { 9, 9, 6 }, 0 }, { "Hulda", { 10, 6, 8 }, 0 },
        { "Chispa", { 5, 6, 4 }, 0 }, { "Brasa", { 9, 9, 8 }, 0 },
    };
    for (int i = 0; i < CANT; i++) {
        v[i].promedio = promedio(v[i].notas);
    }
    ordenar(v, CANT);
    printf("CUADRO DE HONOR DE LA FORJA\n");
    for (int i = 0; i < CANT; i++) {
        printf("%d. %-7s %5.2f\n", i + 1, v[i].nombre, v[i].promedio);
    }
    return 0;
}
```

### Encargo R02-N06-E1 · La ferretería del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La ferretería del Gremio guarda sus productos (código, descripción, precio,
stock) en un array. Calculá el valor total del inventario, listá los que no
tienen stock, buscá un producto por código (puntero o `NULL`) para aumentarle
un 10 %, y mostrá la lista ordenada por precio con `qsort`. (En la salida, la
columna de "Cinta métrica" queda corrida: es la tilde, el efecto de UTF-8 del
11.)

#### Criterio de aprobación

- Calcula el valor total del inventario y lista los que no tienen stock.
- Busca por código devolviendo un puntero o `NULL` y aumenta el precio un 10 %.
- Muestra la lista ordenada por precio con `qsort`.

#### Salida esperada

```
valor del inventario: $243200.00
sin stock: Clavos x100 (102) Cinta métrica (105)
el 103 (Serrucho) aumenta 10 %: $16830.00
el 999 no existe
por precio:
  102  Clavos x100     $  1200.00  stock  0
  104  Destornillador  $  3200.00  stock 25
  105  Cinta métrica  $  4100.00  stock  0
  101  Martillo        $  8500.00  stock 12
  103  Serrucho        $ 16830.00  stock  4
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - El stock de la ferreteria: productos con codigo,
 * descripcion, precio y stock. Valor del inventario, faltantes, busqueda por
 * codigo, aumento de precios y listado ordenado por precio con qsort.
 */
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int    codigo;
    char   descripcion[24];
    double precio;
    int    stock;
} Producto;

Producto *buscar(Producto productos[], int n, int codigo);
int comparar_precio(const void *a, const void *b);

int main(void)
{
    Producto productos[] = {
        { 101, "Martillo", 8500.0, 12 }, { 102, "Clavos x100", 1200.0, 0 },
        { 103, "Serrucho", 15300.0, 4 }, { 104, "Destornillador", 3200.0, 25 },
        { 105, "Cinta métrica", 4100.0, 0 },
    };
    int n = sizeof(productos) / sizeof(productos[0]);

    double valor = 0;
    for (int i = 0; i < n; i++) {
        valor += productos[i].precio * productos[i].stock;
    }
    printf("valor del inventario: $%.2f\n", valor);

    printf("sin stock:");
    for (int i = 0; i < n; i++) {
        if (productos[i].stock == 0) {
            printf(" %s (%d)", productos[i].descripcion, productos[i].codigo);
        }
    }
    printf("\n");

    Producto *p = buscar(productos, n, 103);
    if (p != NULL) {
        p->precio *= 1.10;
        printf("el %d (%s) aumenta 10 %%: $%.2f\n", p->codigo, p->descripcion, p->precio);
    }
    if (buscar(productos, n, 999) == NULL) {
        printf("el 999 no existe\n");
    }

    qsort(productos, n, sizeof(Producto), comparar_precio);
    printf("por precio:\n");
    for (int i = 0; i < n; i++) {
        printf("  %d  %-15s $%9.2f  stock %2d\n", productos[i].codigo,
               productos[i].descripcion, productos[i].precio, productos[i].stock);
    }
    return 0;
}

Producto *buscar(Producto productos[], int n, int codigo)
{
    for (int i = 0; i < n; i++) {
        if (productos[i].codigo == codigo) {
            return &productos[i];
        }
    }
    return NULL;
}

/* Con double no conviene restar: se compara */
int comparar_precio(const void *a, const void *b)
{
    const Producto *x = a;
    const Producto *y = b;
    return (x->precio > y->precio) - (x->precio < y->precio);
}
```

### Prueba del sello

#### ¿Por qué conviene guardar el array y su cantidad en el mismo struct?

Porque viajan juntos: una función que recibe el struct sabe cuántos elementos hay sin un parámetro aparte.

#### ¿Qué devuelve `buscar` si no encuentra nada? ¿Por qué devuelve un puntero y no una copia?

`NULL`. Devuelve un puntero para que se pueda modificar el elemento encontrado dentro del array (una copia no cambiaría el original).

#### Para quitar el elemento 1 de 4, ¿qué elementos se mueven y hacia dónde?

Se mueven los elementos 2 y 3, una posición hacia adelante (al 1 y al 2).

#### ¿Qué cuatro datos necesita `qsort`?

La dirección del array, la cantidad de elementos, el tamaño de cada uno y la función de comparación.

#### ¿Por qué la función de comparación recibe `const void *`? ¿Qué es lo primero que hace?

Porque `qsort` sirve para cualquier tipo. Lo primero que hace es convertir los punteros al tipo real (`const Arma *a = pa;`).

#### ¿Cómo se ordena de mayor a menor con `qsort`?

Invirtiendo la comparación: `b - a` en lugar de `a - b` (o devolviendo el signo contrario).

#### ¿Por qué `comparar_por_nombre` va sin paréntesis en la llamada a `qsort`?

Porque no se la llama: se pasa **la función** (su dirección) para que `qsort` la llame cuando necesite.

### Soluciones (docente)

Material original: `01-C/15-ArrayDeStructs` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

## R02-N07 · Jefe: la Araña de las Direcciones

```meta
tipo: jefe
criatura: dragon
padre: R02-N06
precio: 10
insignia: Sello de la Araña
insignia_descripcion: Venciste a la Araña de las Direcciones en la Arena: dominás arrays, textos, structs y punteros en C.
usa: mem.punteros, col.registros, prog.matematica-azar
```

### Crónica

Al final de los pasillos numerados está la **Arena**, donde los aprendices prueban lo que aprendieron. {mentor} te da una espada, un escudo y dos pociones.

—Cuatro rivales, {heroe}. El último es la **Araña de las Direcciones**. No le ganás con fuerza: le ganás sabiendo cuándo pegar, cuándo cubrirte y cuándo tomar la poción. Y cuidado con su red.

### Objetivos

Escribir un juego por turnos **completo** que usa todo el bloque: structs y
`enum`, funciones que reciben punteros a struct, un array de structs, textos,
azar con semilla y la entrada validada. Es un programa de unas 250 líneas en
**un solo archivo**; en el 23 se ve cómo partir un programa así en varios
archivos `.c` y `.h`.

### Antes de empezar

Todo el bloque 2 (10–15), más:
- `rand`/`srand` y `tirar(minimo, maximo)` (09);
- la validación con `"%d %c"` (07) convertida en función (`pedir_entero`, 13).

### Explicación

#### Cómo se juega

Kira enfrenta **cuatro oleadas**: un Slime, un Goblin, un Orco y la Araña. En
cada turno elige:

| Acción | Efecto |
|---|---|
| 1) atacar | ataque + tirada de 0 a 4 − defensa del rival (mínimo 1) |
| 2) golpe fuerte | 55 % de acertar; si acierta, el **doble** |
| 3) poción | +30 de vida (hay 2; si no quedan, pierde el turno) |
| 4) defender | el próximo golpe del rival hace la mitad |

Después de cada oleada, Ferrum ofrece una recompensa: +20 de vida máxima (y
curarse), +3 de ataque u otra poción. La **Araña** es la jefa: cada 3 turnos
teje una red y Kira pierde su próximo turno.

Atacando siempre, sin estrategia, Kira cae ante la Araña. Hay que elegir bien.

#### Cómo está armado el código

```
Accion   (enum)     las 4 acciones: ACCION_ATACAR = 1, ACCION_FUERTE, ...
Luchador (struct)   nombre, vida, vida_max, ataque, defensa, es_jefe
Partida  (struct)   la heroína + pociones, estados (defendiendo, atrapada)
                    y contadores (turnos, daño hecho)
oleadas[]           array de 4 Luchador, creado con crear(...)
```
| Función | Qué hace | Recibe |
|---|---|---|
| `crear` | arma un `Luchador` y lo devuelve por valor | datos sueltos |
| `mostrar` | la barra de vida `[#######---]` | `const Luchador *` |
| `pedir_opcion` | pregunta hasta que sea válido; `false` si no hay más entrada | un `int *` para el resultado |
| `golpear` | calcula el daño, se lo resta al defensor y lo devuelve | atacante `const`, defensor no |
| `turno_de_kira` | aplica la acción elegida (un `switch` sobre el `enum`) | `Partida *`, `Luchador *` |
| `turno_del_enemigo` | el rival pega (o la Araña teje su red) | `Partida *`, `Luchador *` |
| `pelear` | el bucle de una oleada; `true` si gana Kira | `Partida *`, `Luchador *` |
| `recompensa` | el menú entre oleadas | `Partida *` |

`main` queda como una receta corta: crear la partida y las oleadas, y recorrer
el array llamando a `pelear` con `&oleadas[i]`.

Tres decisiones para mirar:
- **La semilla es fija** (`#define SEMILLA 2026`): la partida se puede repetir,
  y por eso hay una salida esperada. Para jugar de verdad, cambiala por
  `srand(time(NULL))` (con `#include <time.h>`).
- **Si se termina la entrada**, `pedir_opcion` devuelve `false` y Kira ataca
  sola: el programa nunca queda preguntando para siempre.
- **La barra de vida muestra el nombre al final.** Con `%-5.5s` para alinear
  los nombres, "Araña" se cortaba en el medio de la `ñ` (11).

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo (la entrada de ejemplo ya está en la pestaña **Entrada**).
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**; las respuestas se escriben en la consola.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -std=c11 -Wall -Wextra main.c -o programa` y `./programa`
  - Windows: `gcc -std=c11 -Wall -Wextra main.c -o programa.exe` y `programa.exe`
  - Con las respuestas en un archivo: `./programa < main.entrada.txt` (Linux) o `programa.exe < main.entrada.txt` (Windows).
  - Con los detectores de memoria, solo en Linux: agregá `-g -fsanitize=address`. En Windows (MinGW) no existe: usá `-fsanitize=undefined`.

### Código de ejemplo

```c
/*
 * 16 - Proyecto del bloque 2: LA ARENA DE LAS FORJAS.
 *
 * Kira enfrenta cuatro oleadas por turnos. En cada turno elige una accion;
 * entre oleada y oleada elige una recompensa. La ultima rival es la Arania
 * de las Direcciones, jefa del bloque.
 *
 * Integra: structs y enum (12), punteros a struct (14), array de structs
 * (15), textos (11), azar (09) y la entrada validada (07, 13).
 *
 *   make run                          jugar
 *   ./programa < main.entrada.txt     partida grabada (la de la salida esperada)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define SEMILLA        2026    /* fija: la partida se puede repetir. Para jugar de verdad: time(NULL) */
#define POCIONES       2
#define CURA_POCION    30
#define TURNOS_DE_RED  3       /* la Arania teje su red cada tantos turnos */

typedef enum {
    ACCION_ATACAR = 1,
    ACCION_FUERTE,
    ACCION_POCION,
    ACCION_DEFENDER
} Accion;

typedef struct {
    char nombre[28];
    int  vida;
    int  vida_max;
    int  ataque;
    int  defensa;
    bool es_jefe;
} Luchador;

typedef struct {
    Luchador heroe;
    int      pociones;
    bool     defendiendo;
    bool     atrapada;                 /* en la red: pierde el proximo turno */
    int      turno_pelea;              /* se reinicia en cada oleada */
    int      turnos;                   /* de toda la partida */
    int      danio_hecho;
} Partida;

int  tirar(int minimo, int maximo);
Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe);
void mostrar(const Luchador *l);
bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado);
int  golpear(const Luchador *atacante, Luchador *defensor, int multiplicador);
void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion);
void turno_del_enemigo(Partida *p, Luchador *enemigo);
bool pelear(Partida *p, Luchador *enemigo);
void recompensa(Partida *p);

int main(void)
{
    srand(SEMILLA);
    Partida partida = {
        .heroe = crear("Kira", 90, 16, 3, false),
        .pociones = POCIONES,
    };
    Luchador oleadas[] = {
        crear("Slime de escoria", 30, 7, 0, false),
        crear("Goblin de la fragua", 45, 10, 2, false),
        crear("Orco del yunque", 60, 13, 4, false),
        crear("Araña de las Direcciones", 110, 17, 5, true),
    };
    int total = sizeof(oleadas) / sizeof(oleadas[0]);

    printf("=== LA ARENA DE LAS FORJAS ===\n");
    int vencidos = 0;
    for (int i = 0; i < total; i++) {
        printf("\n--- Oleada %d de %d: %s ---\n", i + 1, total, oleadas[i].nombre);
        if (!pelear(&partida, &oleadas[i])) {
            break;
        }
        vencidos++;
        printf("¡%s cae!\n", oleadas[i].nombre);
        if (i < total - 1) {
            recompensa(&partida);
        }
    }

    printf("\n=== RESULTADO ===\n");
    if (vencidos == total) {
        printf("¡Kira vence a la Araña de las Direcciones y gana la Arena!\n");
    } else {
        printf("Kira cae en la oleada %d. Ferrum la saca de la arena a la rastra.\n",
               vencidos + 1);
    }
    printf("oleadas vencidas: %d de %d | turnos: %d | daño hecho: %d | pociones sin usar: %d\n",
           vencidos, total, partida.turnos, partida.danio_hecho, partida.pociones);
    return 0;
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe)
{
    Luchador l = { .vida = vida, .vida_max = vida, .ataque = ataque,
                   .defensa = defensa, .es_jefe = es_jefe };
    snprintf(l.nombre, sizeof(l.nombre), "%s", nombre);
    return l;
}

/* Barra de vida de 10 segmentos:  [#######---] 63/90 Kira */
void mostrar(const Luchador *l)
{
    int llenos = l->vida * 10 / l->vida_max;
    printf("  [");
    for (int i = 0; i < 10; i++) {
        putchar(i < llenos ? '#' : '-');
    }
    printf("] %3d/%3d %s\n", l->vida, l->vida_max, l->nombre);
}

bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Elegí un número del %d al %d.\n", minimo, maximo);
    }
}

/* Danio = ataque + tirada de 0 a 4 - defensa (minimo 1), por el multiplicador */
int golpear(const Luchador *atacante, Luchador *defensor, int multiplicador)
{
    int danio = atacante->ataque + tirar(0, 4) - defensor->defensa;
    if (danio < 1) {
        danio = 1;
    }
    danio *= multiplicador;
    defensor->vida -= danio;
    if (defensor->vida < 0) {
        defensor->vida = 0;
    }
    return danio;
}

void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion)
{
    Luchador *kira = &p->heroe;
    int danio = 0;
    switch (accion) {
        case ACCION_ATACAR:
            danio = golpear(kira, enemigo, 1);
            printf("Kira ataca: %d de daño.\n", danio);
            break;
        case ACCION_FUERTE:
            if (tirar(1, 100) <= 55) {             /* 55 % de acertar */
                danio = golpear(kira, enemigo, 2);
                printf("¡Golpe fuerte! %d de daño.\n", danio);
            } else {
                printf("El golpe fuerte falla.\n");
            }
            break;
        case ACCION_POCION:
            if (p->pociones == 0) {
                printf("No quedan pociones: Kira pierde el turno buscando en la mochila.\n");
            } else {
                p->pociones--;
                kira->vida += CURA_POCION;
                if (kira->vida > kira->vida_max) {
                    kira->vida = kira->vida_max;
                }
                printf("Kira toma una poción (le quedan %d).\n", p->pociones);
            }
            break;
        case ACCION_DEFENDER:
            p->defendiendo = true;
            printf("Kira se cubre con el escudo.\n");
            break;
    }
    p->danio_hecho += danio;
}

void turno_del_enemigo(Partida *p, Luchador *enemigo)
{
    if (enemigo->es_jefe && p->turno_pelea % TURNOS_DE_RED == 0) {
        p->atrapada = true;
        printf("La Araña teje una red de hilos: ¡Kira queda atrapada!\n");
        return;
    }
    int danio = golpear(enemigo, &p->heroe, 1);
    if (p->defendiendo) {
        int bloqueado = danio / 2;             /* el escudo devuelve la mitad */
        p->heroe.vida += bloqueado;
        danio -= bloqueado;
        p->defendiendo = false;
    }
    printf("%s pega: %d de daño.\n", enemigo->nombre, danio);
}

/* Devuelve true si Kira gana esta pelea */
bool pelear(Partida *p, Luchador *enemigo)
{
    p->turno_pelea = 0;
    while (p->heroe.vida > 0 && enemigo->vida > 0) {
        p->turno_pelea++;
        p->turnos++;
        mostrar(&p->heroe);
        mostrar(enemigo);

        if (p->atrapada) {
            printf("Kira forcejea con la red y pierde el turno.\n");
            p->atrapada = false;
        } else {
            int opcion;
            if (!pedir_opcion("1) atacar  2) golpe fuerte  3) poción  4) defender: ",
                              1, 4, &opcion)) {
                opcion = ACCION_ATACAR;        /* sin entrada: ataca sola */
            }
            printf("\n");
            turno_de_kira(p, enemigo, (Accion) opcion);
        }
        if (enemigo->vida > 0) {
            turno_del_enemigo(p, enemigo);
        }
    }
    return p->heroe.vida > 0;
}

void recompensa(Partida *p)
{
    printf("Ferrum ofrece una recompensa:\n");
    int opcion;
    if (!pedir_opcion("1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: ",
                      1, 3, &opcion)) {
        opcion = 3;
    }
    printf("\n");
    switch (opcion) {
        case 1:
            p->heroe.vida_max += 20;
            p->heroe.vida = p->heroe.vida_max;
            printf("Kira recupera toda la vida: %d.\n", p->heroe.vida);
            break;
        case 2:
            p->heroe.ataque += 3;
            printf("El ataque de Kira sube a %d.\n", p->heroe.ataque);
            break;
        default:
            p->pociones++;
            printf("Kira guarda otra poción (tiene %d).\n", p->pociones);
            break;
    }
}
```

### Entrada de ejemplo

```
tres
9
1
1
vida
2
4
1
1
1
1
1
1
1
2
2
2
3
2
3
2
2
2
2
```

### Salida esperada

```
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender: 
  Elegí un número del 1 al 4.
1) atacar  2) golpe fuerte  3) poción  4) defender: 
  Elegí un número del 1 al 4.
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Slime de escoria pega: 6 de daño.
  [#########-]  84/ 90 Kira
  [####------]  12/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 19 de daño.
¡Slime de escoria cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
  Elegí un número del 1 al 3.
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
El ataque de Kira sube a 19.

--- Oleada 2 de 4: Goblin de la fragua ---
  [#########-]  84/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira se cubre con el escudo.
Goblin de la fragua pega: 6 de daño.
  [########--]  78/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Goblin de la fragua pega: 8 de daño.
  [#######---]  70/ 90 Kira
  [######----]  27/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 19 de daño.
Goblin de la fragua pega: 9 de daño.
  [######----]  61/ 90 Kira
  [#---------]   8/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 21 de daño.
¡Goblin de la fragua cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
Kira recupera toda la vida: 110.

--- Oleada 3 de 4: Orco del yunque ---
  [##########] 110/110 Kira
  [##########]  60/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Orco del yunque pega: 13 de daño.
  [########--]  97/110 Kira
  [#######---]  42/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 15 de daño.
Orco del yunque pega: 14 de daño.
  [#######---]  83/110 Kira
  [####------]  27/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 17 de daño.
Orco del yunque pega: 12 de daño.
  [######----]  71/110 Kira
  [#---------]  10/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 30 de daño.
¡Orco del yunque cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
El ataque de Kira sube a 22.

--- Oleada 4 de 4: Araña de las Direcciones ---
  [######----]  71/110 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 18 de daño.
  [####------]  53/110 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 1).
Araña de las Direcciones pega: 14 de daño.
  [######----]  69/110 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 38 de daño.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [######----]  69/110 Kira
  [######----]  72/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 15 de daño.
  [####------]  54/110 Kira
  [######----]  72/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 0).
Araña de las Direcciones pega: 16 de daño.
  [######----]  68/110 Kira
  [######----]  72/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 34 de daño.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [######----]  68/110 Kira
  [###-------]  38/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 14 de daño.
  [####------]  54/110 Kira
  [###-------]  38/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 16 de daño.
  [###-------]  38/110 Kira
  [###-------]  38/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 40 de daño.
¡Araña de las Direcciones cae!

=== RESULTADO ===
¡Kira vence a la Araña de las Direcciones y gana la Arena!
oleadas vencidas: 4 de 4 | turnos: 19 | daño hecho: 287 | pociones sin usar: 0
```

### ¿Para qué sirve?

Un proyecto así junta todo lo de la rama en un programa completo, como uno de verdad: datos en structs, un array de rivales, funciones que reciben punteros, entrada validada y un bucle principal. Es la misma estructura que un sistema de turnos, una máquina expendedora o cualquier juego por turnos: estado, reglas y un bucle que avanza.

### Errores habituales

Los que aparecieron escribiendo este proyecto:

**Ogro: el texto cortado en el medio de una letra.** `printf("%-5.5s")` corta
por **bytes**: "Araña" quedaba como "Arañ" más medio carácter.

**Ogro: el juego que no se puede probar.** Con `srand(time(NULL))`, cada
partida es distinta y no hay salida esperada contra la cual comparar. Semilla
fija para probar; la hora, para jugar.

**Ogro: el `switch` sobre un número que no es del `enum`.** `pedir_opcion`
asegura que la opción esté entre 1 y 4 antes de convertirla a `Accion`. Sin esa
validación, un 7 no entraría en ningún `case`.

**Troll: el puntero a la oleada equivocada.** `pelear(&partida, &oleadas[i])`
pasa la dirección de **esa** oleada. Si se pasara `oleadas` (sin índice), todas
las peleas serían contra el Slime.

**Orco: agregar más oleadas sin mirar el tamaño.** El total sale de
`sizeof(oleadas) / sizeof(oleadas[0])`: si se agrega un rival al array, el
bucle se ajusta solo.

### Misión R02-N07-M1 · El veneno del Goblin

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Cada golpe del Goblin envenena a Kira (si no lo
estaba). Envenenada, pierde 3 de vida al comienzo de sus próximos 3 turnos, y
una poción también cura el veneno. Hace falta un campo nuevo en `Partida`. (En la partida de la solución, el veneno se nota: Kira cae ante la Araña.)

#### Criterio de aprobación

- Agrega a `Partida` el campo para contar los turnos de veneno.
- Cada golpe del Goblin envenena si no lo estaba; envenenada, pierde 3 de vida al comienzo de sus próximos 3 turnos.
- La poción también cura el veneno.

#### Código inicial

```c
/*
 * 16 - Proyecto del bloque 2: LA ARENA DE LAS FORJAS.
 *
 * Kira enfrenta cuatro oleadas por turnos. En cada turno elige una accion;
 * entre oleada y oleada elige una recompensa. La ultima rival es la Arania
 * de las Direcciones, jefa del bloque.
 *
 * Integra: structs y enum (12), punteros a struct (14), array de structs
 * (15), textos (11), azar (09) y la entrada validada (07, 13).
 *
 *   make run                          jugar
 *   ./programa < main.entrada.txt     partida grabada (la de la salida esperada)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define SEMILLA        2026    /* fija: la partida se puede repetir. Para jugar de verdad: time(NULL) */
#define POCIONES       2
#define CURA_POCION    30
#define TURNOS_DE_RED  3       /* la Arania teje su red cada tantos turnos */

typedef enum {
    ACCION_ATACAR = 1,
    ACCION_FUERTE,
    ACCION_POCION,
    ACCION_DEFENDER
} Accion;

typedef struct {
    char nombre[28];
    int  vida;
    int  vida_max;
    int  ataque;
    int  defensa;
    bool es_jefe;
} Luchador;

typedef struct {
    Luchador heroe;
    int      pociones;
    bool     defendiendo;
    bool     atrapada;                 /* en la red: pierde el proximo turno */
    int      turno_pelea;              /* se reinicia en cada oleada */
    int      turnos;                   /* de toda la partida */
    int      danio_hecho;
} Partida;

int  tirar(int minimo, int maximo);
Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe);
void mostrar(const Luchador *l);
bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado);
int  golpear(const Luchador *atacante, Luchador *defensor, int multiplicador);
void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion);
void turno_del_enemigo(Partida *p, Luchador *enemigo);
bool pelear(Partida *p, Luchador *enemigo);
void recompensa(Partida *p);

int main(void)
{
    srand(SEMILLA);
    Partida partida = {
        .heroe = crear("Kira", 90, 16, 3, false),
        .pociones = POCIONES,
    };
    Luchador oleadas[] = {
        crear("Slime de escoria", 30, 7, 0, false),
        crear("Goblin de la fragua", 45, 10, 2, false),
        crear("Orco del yunque", 60, 13, 4, false),
        crear("Araña de las Direcciones", 110, 17, 5, true),
    };
    int total = sizeof(oleadas) / sizeof(oleadas[0]);

    printf("=== LA ARENA DE LAS FORJAS ===\n");
    int vencidos = 0;
    for (int i = 0; i < total; i++) {
        printf("\n--- Oleada %d de %d: %s ---\n", i + 1, total, oleadas[i].nombre);
        if (!pelear(&partida, &oleadas[i])) {
            break;
        }
        vencidos++;
        printf("¡%s cae!\n", oleadas[i].nombre);
        if (i < total - 1) {
            recompensa(&partida);
        }
    }

    printf("\n=== RESULTADO ===\n");
    if (vencidos == total) {
        printf("¡Kira vence a la Araña de las Direcciones y gana la Arena!\n");
    } else {
        printf("Kira cae en la oleada %d. Ferrum la saca de la arena a la rastra.\n",
               vencidos + 1);
    }
    printf("oleadas vencidas: %d de %d | turnos: %d | daño hecho: %d | pociones sin usar: %d\n",
           vencidos, total, partida.turnos, partida.danio_hecho, partida.pociones);
    return 0;
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe)
{
    Luchador l = { .vida = vida, .vida_max = vida, .ataque = ataque,
                   .defensa = defensa, .es_jefe = es_jefe };
    snprintf(l.nombre, sizeof(l.nombre), "%s", nombre);
    return l;
}

/* Barra de vida de 10 segmentos:  [#######---] 63/90 Kira */
void mostrar(const Luchador *l)
{
    int llenos = l->vida * 10 / l->vida_max;
    printf("  [");
    for (int i = 0; i < 10; i++) {
        putchar(i < llenos ? '#' : '-');
    }
    printf("] %3d/%3d %s\n", l->vida, l->vida_max, l->nombre);
}

bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Elegí un número del %d al %d.\n", minimo, maximo);
    }
}

/* Danio = ataque + tirada de 0 a 4 - defensa (minimo 1), por el multiplicador */
int golpear(const Luchador *atacante, Luchador *defensor, int multiplicador)
{
    int danio = atacante->ataque + tirar(0, 4) - defensor->defensa;
    if (danio < 1) {
        danio = 1;
    }
    danio *= multiplicador;
    defensor->vida -= danio;
    if (defensor->vida < 0) {
        defensor->vida = 0;
    }
    return danio;
}

void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion)
{
    Luchador *kira = &p->heroe;
    int danio = 0;
    switch (accion) {
        case ACCION_ATACAR:
            danio = golpear(kira, enemigo, 1);
            printf("Kira ataca: %d de daño.\n", danio);
            break;
        case ACCION_FUERTE:
            if (tirar(1, 100) <= 55) {             /* 55 % de acertar */
                danio = golpear(kira, enemigo, 2);
                printf("¡Golpe fuerte! %d de daño.\n", danio);
            } else {
                printf("El golpe fuerte falla.\n");
            }
            break;
        case ACCION_POCION:
            if (p->pociones == 0) {
                printf("No quedan pociones: Kira pierde el turno buscando en la mochila.\n");
            } else {
                p->pociones--;
                kira->vida += CURA_POCION;
                if (kira->vida > kira->vida_max) {
                    kira->vida = kira->vida_max;
                }
                printf("Kira toma una poción (le quedan %d).\n", p->pociones);
            }
            break;
        case ACCION_DEFENDER:
            p->defendiendo = true;
            printf("Kira se cubre con el escudo.\n");
            break;
    }
    p->danio_hecho += danio;
}

void turno_del_enemigo(Partida *p, Luchador *enemigo)
{
    if (enemigo->es_jefe && p->turno_pelea % TURNOS_DE_RED == 0) {
        p->atrapada = true;
        printf("La Araña teje una red de hilos: ¡Kira queda atrapada!\n");
        return;
    }
    int danio = golpear(enemigo, &p->heroe, 1);
    if (p->defendiendo) {
        int bloqueado = danio / 2;             /* el escudo devuelve la mitad */
        p->heroe.vida += bloqueado;
        danio -= bloqueado;
        p->defendiendo = false;
    }
    printf("%s pega: %d de daño.\n", enemigo->nombre, danio);
}

/* Devuelve true si Kira gana esta pelea */
bool pelear(Partida *p, Luchador *enemigo)
{
    p->turno_pelea = 0;
    while (p->heroe.vida > 0 && enemigo->vida > 0) {
        p->turno_pelea++;
        p->turnos++;
        mostrar(&p->heroe);
        mostrar(enemigo);

        if (p->atrapada) {
            printf("Kira forcejea con la red y pierde el turno.\n");
            p->atrapada = false;
        } else {
            int opcion;
            if (!pedir_opcion("1) atacar  2) golpe fuerte  3) poción  4) defender: ",
                              1, 4, &opcion)) {
                opcion = ACCION_ATACAR;        /* sin entrada: ataca sola */
            }
            printf("\n");
            turno_de_kira(p, enemigo, (Accion) opcion);
        }
        if (enemigo->vida > 0) {
            turno_del_enemigo(p, enemigo);
        }
    }
    return p->heroe.vida > 0;
}

void recompensa(Partida *p)
{
    printf("Ferrum ofrece una recompensa:\n");
    int opcion;
    if (!pedir_opcion("1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: ",
                      1, 3, &opcion)) {
        opcion = 3;
    }
    printf("\n");
    switch (opcion) {
        case 1:
            p->heroe.vida_max += 20;
            p->heroe.vida = p->heroe.vida_max;
            printf("Kira recupera toda la vida: %d.\n", p->heroe.vida);
            break;
        case 2:
            p->heroe.ataque += 3;
            printf("El ataque de Kira sube a %d.\n", p->heroe.ataque);
            break;
        default:
            p->pociones++;
            printf("Kira guarda otra poción (tiene %d).\n", p->pociones);
            break;
    }
}
```

#### Entrada de ejemplo

```
1
1
2
4
1
1
1
1
1
1
1
1
2
2
2
3
2
3
2
3
2
2
```

#### Salida esperada

```
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Slime de escoria pega: 6 de daño.
  [#########-]  84/ 90 Kira
  [####------]  12/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 19 de daño.
¡Slime de escoria cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
El ataque de Kira sube a 19.

--- Oleada 2 de 4: Goblin de la fragua ---
  [#########-]  84/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira se cubre con el escudo.
Goblin de la fragua pega: 6 de daño.
¡La daga estaba envenenada!
  [########--]  78/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
El veneno quema: -3 (turnos de veneno restantes: 2).
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Goblin de la fragua pega: 8 de daño.
  [#######---]  67/ 90 Kira
  [######----]  27/ 45 Goblin de la fragua
El veneno quema: -3 (turnos de veneno restantes: 1).
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 19 de daño.
Goblin de la fragua pega: 9 de daño.
  [######----]  55/ 90 Kira
  [#---------]   8/ 45 Goblin de la fragua
El veneno quema: -3 (turnos de veneno restantes: 0).
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 21 de daño.
¡Goblin de la fragua cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
Kira recupera toda la vida: 110.

--- Oleada 3 de 4: Orco del yunque ---
  [##########] 110/110 Kira
  [##########]  60/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Orco del yunque pega: 13 de daño.
  [########--]  97/110 Kira
  [#######---]  42/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 15 de daño.
Orco del yunque pega: 14 de daño.
  [#######---]  83/110 Kira
  [####------]  27/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 17 de daño.
Orco del yunque pega: 12 de daño.
  [######----]  71/110 Kira
  [#---------]  10/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 16 de daño.
¡Orco del yunque cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
El ataque de Kira sube a 22.

--- Oleada 4 de 4: Araña de las Direcciones ---
  [######----]  71/110 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 36 de daño.
Araña de las Direcciones pega: 18 de daño.
  [####------]  53/110 Kira
  [######----]  74/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 16 de daño.
  [###-------]  37/110 Kira
  [######----]  74/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 1).
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [######----]  67/110 Kira
  [######----]  74/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 16 de daño.
  [####------]  51/110 Kira
  [######----]  74/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 16 de daño.
  [###-------]  35/110 Kira
  [######----]  74/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 0).
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [#####-----]  65/110 Kira
  [######----]  74/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 16 de daño.
  [####------]  49/110 Kira
  [######----]  74/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 14 de daño.
  [###-------]  35/110 Kira
  [######----]  74/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
No quedan pociones: Kira pierde el turno buscando en la mochila.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [###-------]  35/110 Kira
  [######----]  74/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 15 de daño.
  [#---------]  20/110 Kira
  [######----]  74/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 16 de daño.
  [----------]   4/110 Kira
  [######----]  74/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [----------]   4/110 Kira
  [######----]  74/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 14 de daño.

=== RESULTADO ===
Kira cae en la oleada 4. Ferrum la saca de la arena a la rastra.
oleadas vencidas: 3 de 4 | turnos: 23 | daño hecho: 197 | pociones sin usar: 0
```

#### Solución de referencia

```c
/*
 * Mision 1 - El veneno del Goblin: cada golpe del Goblin envenena a Kira
 * (si no lo estaba). Envenenada, pierde 3 de vida al comienzo de cada uno
 * de sus proximos 3 turnos. Una pocion tambien cura el veneno.
 * Probar con:  ./sol < mision1_veneno.entrada.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define SEMILLA        2026    /* fija: la partida se puede repetir. Para jugar de verdad: time(NULL) */
#define POCIONES       2
#define CURA_POCION    30
#define TURNOS_DE_RED  3       /* la Arania teje su red cada tantos turnos */

typedef enum {
    ACCION_ATACAR = 1,
    ACCION_FUERTE,
    ACCION_POCION,
    ACCION_DEFENDER
} Accion;

typedef struct {
    char nombre[28];
    int  vida;
    int  vida_max;
    int  ataque;
    int  defensa;
    bool es_jefe;
} Luchador;

typedef struct {
    Luchador heroe;
    int      pociones;
    bool     defendiendo;
    bool     atrapada;                 /* en la red: pierde el proximo turno */
    int      veneno;                   /* turnos de veneno que quedan */
    int      turno_pelea;              /* se reinicia en cada oleada */
    int      turnos;                   /* de toda la partida */
    int      danio_hecho;
} Partida;

int  tirar(int minimo, int maximo);
Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe);
void mostrar(const Luchador *l);
bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado);
int  golpear(const Luchador *atacante, Luchador *defensor, int multiplicador);
void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion);
void turno_del_enemigo(Partida *p, Luchador *enemigo);
bool pelear(Partida *p, Luchador *enemigo);
void recompensa(Partida *p);

int main(void)
{
    srand(SEMILLA);
    Partida partida = {
        .heroe = crear("Kira", 90, 16, 3, false),
        .pociones = POCIONES,
    };
    Luchador oleadas[] = {
        crear("Slime de escoria", 30, 7, 0, false),
        crear("Goblin de la fragua", 45, 10, 2, false),
        crear("Orco del yunque", 60, 13, 4, false),
        crear("Araña de las Direcciones", 110, 17, 5, true),
    };
    int total = sizeof(oleadas) / sizeof(oleadas[0]);

    printf("=== LA ARENA DE LAS FORJAS ===\n");
    int vencidos = 0;
    for (int i = 0; i < total; i++) {
        printf("\n--- Oleada %d de %d: %s ---\n", i + 1, total, oleadas[i].nombre);
        if (!pelear(&partida, &oleadas[i])) {
            break;
        }
        vencidos++;
        printf("¡%s cae!\n", oleadas[i].nombre);
        if (i < total - 1) {
            recompensa(&partida);
        }
    }

    printf("\n=== RESULTADO ===\n");
    if (vencidos == total) {
        printf("¡Kira vence a la Araña de las Direcciones y gana la Arena!\n");
    } else {
        printf("Kira cae en la oleada %d. Ferrum la saca de la arena a la rastra.\n",
               vencidos + 1);
    }
    printf("oleadas vencidas: %d de %d | turnos: %d | daño hecho: %d | pociones sin usar: %d\n",
           vencidos, total, partida.turnos, partida.danio_hecho, partida.pociones);
    return 0;
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe)
{
    Luchador l = { .vida = vida, .vida_max = vida, .ataque = ataque,
                   .defensa = defensa, .es_jefe = es_jefe };
    snprintf(l.nombre, sizeof(l.nombre), "%s", nombre);
    return l;
}

/* Barra de vida de 10 segmentos:  [#######---] 63/90 Kira */
void mostrar(const Luchador *l)
{
    int llenos = l->vida * 10 / l->vida_max;
    printf("  [");
    for (int i = 0; i < 10; i++) {
        putchar(i < llenos ? '#' : '-');
    }
    printf("] %3d/%3d %s\n", l->vida, l->vida_max, l->nombre);
}

bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Elegí un número del %d al %d.\n", minimo, maximo);
    }
}

/* Danio = ataque + tirada de 0 a 4 - defensa (minimo 1), por el multiplicador */
int golpear(const Luchador *atacante, Luchador *defensor, int multiplicador)
{
    int danio = atacante->ataque + tirar(0, 4) - defensor->defensa;
    if (danio < 1) {
        danio = 1;
    }
    danio *= multiplicador;
    defensor->vida -= danio;
    if (defensor->vida < 0) {
        defensor->vida = 0;
    }
    return danio;
}

void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion)
{
    Luchador *kira = &p->heroe;
    int danio = 0;
    switch (accion) {
        case ACCION_ATACAR:
            danio = golpear(kira, enemigo, 1);
            printf("Kira ataca: %d de daño.\n", danio);
            break;
        case ACCION_FUERTE:
            if (tirar(1, 100) <= 55) {             /* 55 % de acertar */
                danio = golpear(kira, enemigo, 2);
                printf("¡Golpe fuerte! %d de daño.\n", danio);
            } else {
                printf("El golpe fuerte falla.\n");
            }
            break;
        case ACCION_POCION:
            if (p->pociones == 0) {
                printf("No quedan pociones: Kira pierde el turno buscando en la mochila.\n");
            } else {
                p->pociones--;
                kira->vida += CURA_POCION;
                if (kira->vida > kira->vida_max) {
                    kira->vida = kira->vida_max;
                }
                p->veneno = 0;
                printf("Kira toma una poción (le quedan %d).\n", p->pociones);
            }
            break;
        case ACCION_DEFENDER:
            p->defendiendo = true;
            printf("Kira se cubre con el escudo.\n");
            break;
    }
    p->danio_hecho += danio;
}

void turno_del_enemigo(Partida *p, Luchador *enemigo)
{
    if (enemigo->es_jefe && p->turno_pelea % TURNOS_DE_RED == 0) {
        p->atrapada = true;
        printf("La Araña teje una red de hilos: ¡Kira queda atrapada!\n");
        return;
    }
    int danio = golpear(enemigo, &p->heroe, 1);
    if (p->defendiendo) {
        int bloqueado = danio / 2;             /* el escudo devuelve la mitad */
        p->heroe.vida += bloqueado;
        danio -= bloqueado;
        p->defendiendo = false;
    }
    printf("%s pega: %d de daño.\n", enemigo->nombre, danio);
    if (strstr(enemigo->nombre, "Goblin") != NULL && p->veneno == 0) {
        p->veneno = 3;
        printf("¡La daga estaba envenenada!\n");
    }
}

/* Devuelve true si Kira gana esta pelea */
bool pelear(Partida *p, Luchador *enemigo)
{
    p->turno_pelea = 0;
    while (p->heroe.vida > 0 && enemigo->vida > 0) {
        p->turno_pelea++;
        p->turnos++;
        mostrar(&p->heroe);
        mostrar(enemigo);

        if (p->veneno > 0) {
            p->veneno--;
            p->heroe.vida -= 3;
            printf("El veneno quema: -3 (turnos de veneno restantes: %d).\n", p->veneno);
            if (p->heroe.vida <= 0) {
                p->heroe.vida = 0;
                break;
            }
        }
        if (p->atrapada) {
            printf("Kira forcejea con la red y pierde el turno.\n");
            p->atrapada = false;
        } else {
            int opcion;
            if (!pedir_opcion("1) atacar  2) golpe fuerte  3) poción  4) defender: ",
                              1, 4, &opcion)) {
                opcion = ACCION_ATACAR;        /* sin entrada: ataca sola */
            }
            printf("\n");
            turno_de_kira(p, enemigo, (Accion) opcion);
        }
        if (enemigo->vida > 0) {
            turno_del_enemigo(p, enemigo);
        }
    }
    return p->heroe.vida > 0;
}

void recompensa(Partida *p)
{
    printf("Ferrum ofrece una recompensa:\n");
    int opcion;
    if (!pedir_opcion("1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: ",
                      1, 3, &opcion)) {
        opcion = 3;
    }
    printf("\n");
    switch (opcion) {
        case 1:
            p->heroe.vida_max += 20;
            p->heroe.vida = p->heroe.vida_max;
            printf("Kira recupera toda la vida: %d.\n", p->heroe.vida);
            break;
        case 2:
            p->heroe.ataque += 3;
            printf("El ataque de Kira sube a %d.\n", p->heroe.ataque);
            break;
        default:
            p->pociones++;
            printf("Kira guarda otra poción (tiene %d).\n", p->pociones);
            break;
    }
}
```

#### Pruebas

##### Se rinde enseguida
```entrada
1
```
```salida
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
Slime de escoria pega: 6 de daño.
  [#########-]  84/ 90 Kira
  [####------]  12/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 19 de daño.
¡Slime de escoria cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 3).

--- Oleada 2 de 4: Goblin de la fragua ---
  [#########-]  84/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
Goblin de la fragua pega: 8 de daño.
¡La daga estaba envenenada!
  [########--]  76/ 90 Kira
  [######----]  27/ 45 Goblin de la fragua
El veneno quema: -3 (turnos de veneno restantes: 2).
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Goblin de la fragua pega: 9 de daño.
  [#######---]  64/ 90 Kira
  [##--------]  12/ 45 Goblin de la fragua
El veneno quema: -3 (turnos de veneno restantes: 1).
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
¡Goblin de la fragua cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 4).

--- Oleada 3 de 4: Orco del yunque ---
  [######----]  61/ 90 Kira
  [##########]  60/ 60 Orco del yunque
El veneno quema: -3 (turnos de veneno restantes: 0).
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Orco del yunque pega: 13 de daño.
  [#####-----]  45/ 90 Kira
  [#######---]  44/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Orco del yunque pega: 10 de daño.
  [###-------]  35/ 90 Kira
  [####------]  29/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Orco del yunque pega: 12 de daño.
  [##--------]  23/ 90 Kira
  [##--------]  13/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 14 de daño.
¡Orco del yunque cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 5).

--- Oleada 4 de 4: Araña de las Direcciones ---
  [##--------]  23/ 90 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 12 de daño.
Araña de las Direcciones pega: 14 de daño.
  [#---------]   9/ 90 Kira
  [########--]  98/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 12 de daño.
Araña de las Direcciones pega: 18 de daño.

=== RESULTADO ===
Kira cae en la oleada 4. Ferrum la saca de la arena a la rastra.
oleadas vencidas: 3 de 4 | turnos: 11 | daño hecho: 171 | pociones sin usar: 5
```

##### Defiende siempre
```entrada
4
4
4
4
4
4
4
4
4
4
```
```salida
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 3 de daño.
  [#########-]  87/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 3 de daño.
  [#########-]  84/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 4 de daño.
  [########--]  80/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 4 de daño.
  [########--]  76/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 3 de daño.
  [########--]  73/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 3 de daño.
  [#######---]  70/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 3 de daño.
  [#######---]  67/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 3 de daño.
  [#######---]  64/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 4 de daño.
  [######----]  60/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 4 de daño.
  [######----]  56/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 19 de daño.
Slime de escoria pega: 4 de daño.
  [#####-----]  52/ 90 Kira
  [###-------]  11/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 20 de daño.
¡Slime de escoria cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 3).

--- Oleada 2 de 4: Goblin de la fragua ---
  [#####-----]  52/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Goblin de la fragua pega: 9 de daño.
¡La daga estaba envenenada!
  [####------]  43/ 90 Kira
  [######----]  29/ 45 Goblin de la fragua
El veneno quema: -3 (turnos de veneno restantes: 2).
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Goblin de la fragua pega: 7 de daño.
  [###-------]  33/ 90 Kira
  [###-------]  14/ 45 Goblin de la fragua
El veneno quema: -3 (turnos de veneno restantes: 1).
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
¡Goblin de la fragua cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 4).

--- Oleada 3 de 4: Orco del yunque ---
  [###-------]  30/ 90 Kira
  [##########]  60/ 60 Orco del yunque
El veneno quema: -3 (turnos de veneno restantes: 0).
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Orco del yunque pega: 10 de daño.
  [#---------]  17/ 90 Kira
  [#######---]  44/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 14 de daño.
Orco del yunque pega: 12 de daño.
  [----------]   5/ 90 Kira
  [#####-----]  30/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 13 de daño.
Orco del yunque pega: 12 de daño.

=== RESULTADO ===
Kira cae en la oleada 3. Ferrum la saca de la arena a la rastra.
oleadas vencidas: 2 de 4 | turnos: 18 | daño hecho: 128 | pociones sin usar: 4
```

### Misión R02-N07-M2 · El oro y la tienda

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Cada rival deja oro (su vida máxima / 3). La
recompensa gratis se reemplaza por una **tienda**: poción (15), +2 de ataque
(25) o +15 de vida máxima (20), comprando varias cosas hasta elegir 0 y
avisando cuando no alcanza.

#### Criterio de aprobación

- Cada rival deja oro (su vida máxima / 3).
- La tienda vende poción (15), +2 de ataque (25) y +15 de vida máxima (20), varias veces hasta elegir 0.
- Avisa cuando no alcanza el oro.

#### Código inicial

```c
/*
 * 16 - Proyecto del bloque 2: LA ARENA DE LAS FORJAS.
 *
 * Kira enfrenta cuatro oleadas por turnos. En cada turno elige una accion;
 * entre oleada y oleada elige una recompensa. La ultima rival es la Arania
 * de las Direcciones, jefa del bloque.
 *
 * Integra: structs y enum (12), punteros a struct (14), array de structs
 * (15), textos (11), azar (09) y la entrada validada (07, 13).
 *
 *   make run                          jugar
 *   ./programa < main.entrada.txt     partida grabada (la de la salida esperada)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define SEMILLA        2026    /* fija: la partida se puede repetir. Para jugar de verdad: time(NULL) */
#define POCIONES       2
#define CURA_POCION    30
#define TURNOS_DE_RED  3       /* la Arania teje su red cada tantos turnos */

typedef enum {
    ACCION_ATACAR = 1,
    ACCION_FUERTE,
    ACCION_POCION,
    ACCION_DEFENDER
} Accion;

typedef struct {
    char nombre[28];
    int  vida;
    int  vida_max;
    int  ataque;
    int  defensa;
    bool es_jefe;
} Luchador;

typedef struct {
    Luchador heroe;
    int      pociones;
    bool     defendiendo;
    bool     atrapada;                 /* en la red: pierde el proximo turno */
    int      turno_pelea;              /* se reinicia en cada oleada */
    int      turnos;                   /* de toda la partida */
    int      danio_hecho;
} Partida;

int  tirar(int minimo, int maximo);
Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe);
void mostrar(const Luchador *l);
bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado);
int  golpear(const Luchador *atacante, Luchador *defensor, int multiplicador);
void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion);
void turno_del_enemigo(Partida *p, Luchador *enemigo);
bool pelear(Partida *p, Luchador *enemigo);
void recompensa(Partida *p);

int main(void)
{
    srand(SEMILLA);
    Partida partida = {
        .heroe = crear("Kira", 90, 16, 3, false),
        .pociones = POCIONES,
    };
    Luchador oleadas[] = {
        crear("Slime de escoria", 30, 7, 0, false),
        crear("Goblin de la fragua", 45, 10, 2, false),
        crear("Orco del yunque", 60, 13, 4, false),
        crear("Araña de las Direcciones", 110, 17, 5, true),
    };
    int total = sizeof(oleadas) / sizeof(oleadas[0]);

    printf("=== LA ARENA DE LAS FORJAS ===\n");
    int vencidos = 0;
    for (int i = 0; i < total; i++) {
        printf("\n--- Oleada %d de %d: %s ---\n", i + 1, total, oleadas[i].nombre);
        if (!pelear(&partida, &oleadas[i])) {
            break;
        }
        vencidos++;
        printf("¡%s cae!\n", oleadas[i].nombre);
        if (i < total - 1) {
            recompensa(&partida);
        }
    }

    printf("\n=== RESULTADO ===\n");
    if (vencidos == total) {
        printf("¡Kira vence a la Araña de las Direcciones y gana la Arena!\n");
    } else {
        printf("Kira cae en la oleada %d. Ferrum la saca de la arena a la rastra.\n",
               vencidos + 1);
    }
    printf("oleadas vencidas: %d de %d | turnos: %d | daño hecho: %d | pociones sin usar: %d\n",
           vencidos, total, partida.turnos, partida.danio_hecho, partida.pociones);
    return 0;
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe)
{
    Luchador l = { .vida = vida, .vida_max = vida, .ataque = ataque,
                   .defensa = defensa, .es_jefe = es_jefe };
    snprintf(l.nombre, sizeof(l.nombre), "%s", nombre);
    return l;
}

/* Barra de vida de 10 segmentos:  [#######---] 63/90 Kira */
void mostrar(const Luchador *l)
{
    int llenos = l->vida * 10 / l->vida_max;
    printf("  [");
    for (int i = 0; i < 10; i++) {
        putchar(i < llenos ? '#' : '-');
    }
    printf("] %3d/%3d %s\n", l->vida, l->vida_max, l->nombre);
}

bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Elegí un número del %d al %d.\n", minimo, maximo);
    }
}

/* Danio = ataque + tirada de 0 a 4 - defensa (minimo 1), por el multiplicador */
int golpear(const Luchador *atacante, Luchador *defensor, int multiplicador)
{
    int danio = atacante->ataque + tirar(0, 4) - defensor->defensa;
    if (danio < 1) {
        danio = 1;
    }
    danio *= multiplicador;
    defensor->vida -= danio;
    if (defensor->vida < 0) {
        defensor->vida = 0;
    }
    return danio;
}

void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion)
{
    Luchador *kira = &p->heroe;
    int danio = 0;
    switch (accion) {
        case ACCION_ATACAR:
            danio = golpear(kira, enemigo, 1);
            printf("Kira ataca: %d de daño.\n", danio);
            break;
        case ACCION_FUERTE:
            if (tirar(1, 100) <= 55) {             /* 55 % de acertar */
                danio = golpear(kira, enemigo, 2);
                printf("¡Golpe fuerte! %d de daño.\n", danio);
            } else {
                printf("El golpe fuerte falla.\n");
            }
            break;
        case ACCION_POCION:
            if (p->pociones == 0) {
                printf("No quedan pociones: Kira pierde el turno buscando en la mochila.\n");
            } else {
                p->pociones--;
                kira->vida += CURA_POCION;
                if (kira->vida > kira->vida_max) {
                    kira->vida = kira->vida_max;
                }
                printf("Kira toma una poción (le quedan %d).\n", p->pociones);
            }
            break;
        case ACCION_DEFENDER:
            p->defendiendo = true;
            printf("Kira se cubre con el escudo.\n");
            break;
    }
    p->danio_hecho += danio;
}

void turno_del_enemigo(Partida *p, Luchador *enemigo)
{
    if (enemigo->es_jefe && p->turno_pelea % TURNOS_DE_RED == 0) {
        p->atrapada = true;
        printf("La Araña teje una red de hilos: ¡Kira queda atrapada!\n");
        return;
    }
    int danio = golpear(enemigo, &p->heroe, 1);
    if (p->defendiendo) {
        int bloqueado = danio / 2;             /* el escudo devuelve la mitad */
        p->heroe.vida += bloqueado;
        danio -= bloqueado;
        p->defendiendo = false;
    }
    printf("%s pega: %d de daño.\n", enemigo->nombre, danio);
}

/* Devuelve true si Kira gana esta pelea */
bool pelear(Partida *p, Luchador *enemigo)
{
    p->turno_pelea = 0;
    while (p->heroe.vida > 0 && enemigo->vida > 0) {
        p->turno_pelea++;
        p->turnos++;
        mostrar(&p->heroe);
        mostrar(enemigo);

        if (p->atrapada) {
            printf("Kira forcejea con la red y pierde el turno.\n");
            p->atrapada = false;
        } else {
            int opcion;
            if (!pedir_opcion("1) atacar  2) golpe fuerte  3) poción  4) defender: ",
                              1, 4, &opcion)) {
                opcion = ACCION_ATACAR;        /* sin entrada: ataca sola */
            }
            printf("\n");
            turno_de_kira(p, enemigo, (Accion) opcion);
        }
        if (enemigo->vida > 0) {
            turno_del_enemigo(p, enemigo);
        }
    }
    return p->heroe.vida > 0;
}

void recompensa(Partida *p)
{
    printf("Ferrum ofrece una recompensa:\n");
    int opcion;
    if (!pedir_opcion("1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: ",
                      1, 3, &opcion)) {
        opcion = 3;
    }
    printf("\n");
    switch (opcion) {
        case 1:
            p->heroe.vida_max += 20;
            p->heroe.vida = p->heroe.vida_max;
            printf("Kira recupera toda la vida: %d.\n", p->heroe.vida);
            break;
        case 2:
            p->heroe.ataque += 3;
            printf("El ataque de Kira sube a %d.\n", p->heroe.ataque);
            break;
        default:
            p->pociones++;
            printf("Kira guarda otra poción (tiene %d).\n", p->pociones);
            break;
    }
}
```

#### Entrada de ejemplo

```
1
1
2
0
4
1
1
1
1
0
1
1
1
1
1
3
1
0
3
3
2
3
2
2
2
2
```

#### Salida esperada

```
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Slime de escoria pega: 6 de daño.
  [#########-]  84/ 90 Kira
  [####------]  12/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 19 de daño.
¡Slime de escoria cae! Deja 10 de oro (Kira tiene 10).
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir: 
No te alcanza: +2 de ataque cuesta 25.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir: 

--- Oleada 2 de 4: Goblin de la fragua ---
  [#########-]  84/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira se cubre con el escudo.
Goblin de la fragua pega: 6 de daño.
  [########--]  78/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 15 de daño.
Goblin de la fragua pega: 8 de daño.
  [#######---]  70/ 90 Kira
  [######----]  30/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 16 de daño.
Goblin de la fragua pega: 9 de daño.
  [######----]  61/ 90 Kira
  [###-------]  14/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
¡Goblin de la fragua cae! Deja 15 de oro (Kira tiene 25).
Tienda de Ferrum (tenés 25 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir: 
Compraste poción.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir: 

--- Oleada 3 de 4: Orco del yunque ---
  [######----]  61/ 90 Kira
  [##########]  60/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 15 de daño.
Orco del yunque pega: 13 de daño.
  [#####-----]  48/ 90 Kira
  [#######---]  45/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 12 de daño.
Orco del yunque pega: 14 de daño.
  [###-------]  34/ 90 Kira
  [#####-----]  33/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 14 de daño.
Orco del yunque pega: 12 de daño.
  [##--------]  22/ 90 Kira
  [###-------]  19/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 13 de daño.
Orco del yunque pega: 10 de daño.
  [#---------]  12/ 90 Kira
  [#---------]   6/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 13 de daño.
¡Orco del yunque cae! Deja 20 de oro (Kira tiene 30).
Tienda de Ferrum (tenés 30 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir: 
Compraste +15 de vida máxima.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir: 
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir: 

--- Oleada 4 de 4: Araña de las Direcciones ---
  [##--------]  27/105 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 2).
Araña de las Direcciones pega: 18 de daño.
  [###-------]  39/105 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 1).
Araña de las Direcciones pega: 14 de daño.
  [#####-----]  55/105 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 26 de daño.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [#####-----]  55/105 Kira
  [#######---]  84/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 15 de daño.
  [###-------]  40/105 Kira
  [#######---]  84/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 0).
Araña de las Direcciones pega: 16 de daño.
  [#####-----]  54/105 Kira
  [#######---]  84/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 22 de daño.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [#####-----]  54/105 Kira
  [#####-----]  62/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 14 de daño.
  [###-------]  40/105 Kira
  [#####-----]  62/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 16 de daño.
  [##--------]  24/105 Kira
  [#####-----]  62/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 28 de daño.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [##--------]  24/105 Kira
  [###-------]  34/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 14 de daño.
  [----------]  10/105 Kira
  [###-------]  34/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 30 de daño.
Araña de las Direcciones pega: 18 de daño.

=== RESULTADO ===
Kira cae en la oleada 4. Ferrum la saca de la arena a la rastra.
oleadas vencidas: 3 de 4 | turnos: 22 | daño hecho: 259 | pociones sin usar: 0
```

#### Solución de referencia

```c
/*
 * Mision 2 - El oro y la tienda: cada enemigo deja oro (su vida maxima / 3).
 * Entre oleadas, en lugar de la recompensa gratis, Kira compra en la tienda
 * de Ferrum: pocion (15), +2 de ataque (25) o +15 de vida maxima (20).
 * Puede comprar varias cosas hasta elegir 0.
 * Probar con:  ./sol < mision2_tienda.entrada.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define SEMILLA        2026    /* fija: la partida se puede repetir. Para jugar de verdad: time(NULL) */
#define POCIONES       2
#define CURA_POCION    30
#define TURNOS_DE_RED  3       /* la Arania teje su red cada tantos turnos */

typedef enum {
    ACCION_ATACAR = 1,
    ACCION_FUERTE,
    ACCION_POCION,
    ACCION_DEFENDER
} Accion;

typedef struct {
    char nombre[28];
    int  vida;
    int  vida_max;
    int  ataque;
    int  defensa;
    bool es_jefe;
} Luchador;

typedef struct {
    Luchador heroe;
    int      pociones;
    bool     defendiendo;
    bool     atrapada;                 /* en la red: pierde el proximo turno */
    int      turno_pelea;              /* se reinicia en cada oleada */
    int      turnos;                   /* de toda la partida */
    int      danio_hecho;
    int      oro;
} Partida;

int  tirar(int minimo, int maximo);
Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe);
void mostrar(const Luchador *l);
bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado);
int  golpear(const Luchador *atacante, Luchador *defensor, int multiplicador);
void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion);
void turno_del_enemigo(Partida *p, Luchador *enemigo);
bool pelear(Partida *p, Luchador *enemigo);
void tienda(Partida *p);

int main(void)
{
    srand(SEMILLA);
    Partida partida = {
        .heroe = crear("Kira", 90, 16, 3, false),
        .pociones = POCIONES,
    };
    Luchador oleadas[] = {
        crear("Slime de escoria", 30, 7, 0, false),
        crear("Goblin de la fragua", 45, 10, 2, false),
        crear("Orco del yunque", 60, 13, 4, false),
        crear("Araña de las Direcciones", 110, 17, 5, true),
    };
    int total = sizeof(oleadas) / sizeof(oleadas[0]);

    printf("=== LA ARENA DE LAS FORJAS ===\n");
    int vencidos = 0;
    for (int i = 0; i < total; i++) {
        printf("\n--- Oleada %d de %d: %s ---\n", i + 1, total, oleadas[i].nombre);
        if (!pelear(&partida, &oleadas[i])) {
            break;
        }
        vencidos++;
        int botin = oleadas[i].vida_max / 3;
        partida.oro += botin;
        printf("¡%s cae! Deja %d de oro (Kira tiene %d).\n", oleadas[i].nombre, botin, partida.oro);
        if (i < total - 1) {
            tienda(&partida);
        }
    }

    printf("\n=== RESULTADO ===\n");
    if (vencidos == total) {
        printf("¡Kira vence a la Araña de las Direcciones y gana la Arena!\n");
    } else {
        printf("Kira cae en la oleada %d. Ferrum la saca de la arena a la rastra.\n",
               vencidos + 1);
    }
    printf("oleadas vencidas: %d de %d | turnos: %d | daño hecho: %d | pociones sin usar: %d\n",
           vencidos, total, partida.turnos, partida.danio_hecho, partida.pociones);
    return 0;
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe)
{
    Luchador l = { .vida = vida, .vida_max = vida, .ataque = ataque,
                   .defensa = defensa, .es_jefe = es_jefe };
    snprintf(l.nombre, sizeof(l.nombre), "%s", nombre);
    return l;
}

/* Barra de vida de 10 segmentos:  [#######---] 63/90 Kira */
void mostrar(const Luchador *l)
{
    int llenos = l->vida * 10 / l->vida_max;
    printf("  [");
    for (int i = 0; i < 10; i++) {
        putchar(i < llenos ? '#' : '-');
    }
    printf("] %3d/%3d %s\n", l->vida, l->vida_max, l->nombre);
}

bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Elegí un número del %d al %d.\n", minimo, maximo);
    }
}

/* Danio = ataque + tirada de 0 a 4 - defensa (minimo 1), por el multiplicador */
int golpear(const Luchador *atacante, Luchador *defensor, int multiplicador)
{
    int danio = atacante->ataque + tirar(0, 4) - defensor->defensa;
    if (danio < 1) {
        danio = 1;
    }
    danio *= multiplicador;
    defensor->vida -= danio;
    if (defensor->vida < 0) {
        defensor->vida = 0;
    }
    return danio;
}

void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion)
{
    Luchador *kira = &p->heroe;
    int danio = 0;
    switch (accion) {
        case ACCION_ATACAR:
            danio = golpear(kira, enemigo, 1);
            printf("Kira ataca: %d de daño.\n", danio);
            break;
        case ACCION_FUERTE:
            if (tirar(1, 100) <= 55) {             /* 55 % de acertar */
                danio = golpear(kira, enemigo, 2);
                printf("¡Golpe fuerte! %d de daño.\n", danio);
            } else {
                printf("El golpe fuerte falla.\n");
            }
            break;
        case ACCION_POCION:
            if (p->pociones == 0) {
                printf("No quedan pociones: Kira pierde el turno buscando en la mochila.\n");
            } else {
                p->pociones--;
                kira->vida += CURA_POCION;
                if (kira->vida > kira->vida_max) {
                    kira->vida = kira->vida_max;
                }
                printf("Kira toma una poción (le quedan %d).\n", p->pociones);
            }
            break;
        case ACCION_DEFENDER:
            p->defendiendo = true;
            printf("Kira se cubre con el escudo.\n");
            break;
    }
    p->danio_hecho += danio;
}

void turno_del_enemigo(Partida *p, Luchador *enemigo)
{
    if (enemigo->es_jefe && p->turno_pelea % TURNOS_DE_RED == 0) {
        p->atrapada = true;
        printf("La Araña teje una red de hilos: ¡Kira queda atrapada!\n");
        return;
    }
    int danio = golpear(enemigo, &p->heroe, 1);
    if (p->defendiendo) {
        int bloqueado = danio / 2;             /* el escudo devuelve la mitad */
        p->heroe.vida += bloqueado;
        danio -= bloqueado;
        p->defendiendo = false;
    }
    printf("%s pega: %d de daño.\n", enemigo->nombre, danio);
}

/* Devuelve true si Kira gana esta pelea */
bool pelear(Partida *p, Luchador *enemigo)
{
    p->turno_pelea = 0;
    while (p->heroe.vida > 0 && enemigo->vida > 0) {
        p->turno_pelea++;
        p->turnos++;
        mostrar(&p->heroe);
        mostrar(enemigo);

        if (p->atrapada) {
            printf("Kira forcejea con la red y pierde el turno.\n");
            p->atrapada = false;
        } else {
            int opcion;
            if (!pedir_opcion("1) atacar  2) golpe fuerte  3) poción  4) defender: ",
                              1, 4, &opcion)) {
                opcion = ACCION_ATACAR;        /* sin entrada: ataca sola */
            }
            printf("\n");
            turno_de_kira(p, enemigo, (Accion) opcion);
        }
        if (enemigo->vida > 0) {
            turno_del_enemigo(p, enemigo);
        }
    }
    return p->heroe.vida > 0;
}

void tienda(Partida *p)
{
    const char *nombres[] = { "poción", "+2 de ataque", "+15 de vida máxima" };
    int precios[] = { 15, 25, 20 };
    for (;;) {
        printf("Tienda de Ferrum (tenés %d de oro):\n", p->oro);
        int opcion;
        if (!pedir_opcion("1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir: ",
                          0, 3, &opcion)) {
            opcion = 0;
        }
        printf("\n");
        if (opcion == 0) {
            return;
        }
        int precio = precios[opcion - 1];
        if (precio > p->oro) {
            printf("No te alcanza: %s cuesta %d.\n", nombres[opcion - 1], precio);
            continue;
        }
        p->oro -= precio;
        switch (opcion) {
            case 1:
                p->pociones++;
                break;
            case 2:
                p->heroe.ataque += 2;
                break;
            default:
                p->heroe.vida_max += 15;
                p->heroe.vida += 15;
                break;
        }
        printf("Compraste %s.\n", nombres[opcion - 1]);
    }
}
```

#### Pruebas

##### Se termina la entrada
```entrada
1
1
```
```salida
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
Slime de escoria pega: 6 de daño.
  [#########-]  84/ 90 Kira
  [####------]  12/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 19 de daño.
¡Slime de escoria cae! Deja 10 de oro (Kira tiene 10).
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:

--- Oleada 2 de 4: Goblin de la fragua ---
  [#########-]  84/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
Goblin de la fragua pega: 8 de daño.
  [########--]  76/ 90 Kira
  [######----]  27/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Goblin de la fragua pega: 9 de daño.
  [#######---]  67/ 90 Kira
  [##--------]  12/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
¡Goblin de la fragua cae! Deja 15 de oro (Kira tiene 25).
Tienda de Ferrum (tenés 25 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:

--- Oleada 3 de 4: Orco del yunque ---
  [#######---]  67/ 90 Kira
  [##########]  60/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Orco del yunque pega: 13 de daño.
  [######----]  54/ 90 Kira
  [#######---]  44/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Orco del yunque pega: 10 de daño.
  [####------]  44/ 90 Kira
  [####------]  29/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Orco del yunque pega: 12 de daño.
  [###-------]  32/ 90 Kira
  [##--------]  13/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 14 de daño.
¡Orco del yunque cae! Deja 20 de oro (Kira tiene 45).
Tienda de Ferrum (tenés 45 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:

--- Oleada 4 de 4: Araña de las Direcciones ---
  [###-------]  32/ 90 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 12 de daño.
Araña de las Direcciones pega: 14 de daño.
  [##--------]  18/ 90 Kira
  [########--]  98/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 12 de daño.
Araña de las Direcciones pega: 18 de daño.

=== RESULTADO ===
Kira cae en la oleada 4. Ferrum la saca de la arena a la rastra.
oleadas vencidas: 3 de 4 | turnos: 11 | daño hecho: 171 | pociones sin usar: 2
```

##### Ataca siempre
```entrada
1
1
1
1
1
1
1
1
1
1
1
1
```
```salida
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
Slime de escoria pega: 6 de daño.
  [#########-]  84/ 90 Kira
  [####------]  12/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 19 de daño.
¡Slime de escoria cae! Deja 10 de oro (Kira tiene 10).
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:
No te alcanza: poción cuesta 15.
Tienda de Ferrum (tenés 10 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:

--- Oleada 2 de 4: Goblin de la fragua ---
  [#########-]  84/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
Goblin de la fragua pega: 8 de daño.
  [########--]  76/ 90 Kira
  [######----]  27/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Goblin de la fragua pega: 9 de daño.
  [#######---]  67/ 90 Kira
  [##--------]  12/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
¡Goblin de la fragua cae! Deja 15 de oro (Kira tiene 25).
Tienda de Ferrum (tenés 25 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:

--- Oleada 3 de 4: Orco del yunque ---
  [#######---]  67/ 90 Kira
  [##########]  60/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Orco del yunque pega: 13 de daño.
  [######----]  54/ 90 Kira
  [#######---]  44/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Orco del yunque pega: 10 de daño.
  [####------]  44/ 90 Kira
  [####------]  29/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Orco del yunque pega: 12 de daño.
  [###-------]  32/ 90 Kira
  [##--------]  13/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 14 de daño.
¡Orco del yunque cae! Deja 20 de oro (Kira tiene 45).
Tienda de Ferrum (tenés 45 de oro):
1) poción 15  2) +2 ataque 25  3) +15 vida máx. 20  0) seguir:

--- Oleada 4 de 4: Araña de las Direcciones ---
  [###-------]  32/ 90 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 12 de daño.
Araña de las Direcciones pega: 14 de daño.
  [##--------]  18/ 90 Kira
  [########--]  98/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 12 de daño.
Araña de las Direcciones pega: 18 de daño.

=== RESULTADO ===
Kira cae en la oleada 4. Ferrum la saca de la arena a la rastra.
oleadas vencidas: 3 de 4 | turnos: 11 | daño hecho: 171 | pociones sin usar: 2
```

### Misión R02-N07-M3 · La crónica de la pelea

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Guardá cada golpe de Kira en un array de structs
(turno, rival, daño) dentro de `Partida` y, al final, mostrá los 3 más
fuertes ordenados con `qsort` (a igual daño, el más temprano primero).

#### Criterio de aprobación

- Guarda cada golpe de Kira (turno, rival, daño) en un array de structs dentro de `Partida`.
- Al final muestra los 3 más fuertes ordenados con `qsort`.
- A igual daño, el más temprano primero.

#### Código inicial

```c
/*
 * 16 - Proyecto del bloque 2: LA ARENA DE LAS FORJAS.
 *
 * Kira enfrenta cuatro oleadas por turnos. En cada turno elige una accion;
 * entre oleada y oleada elige una recompensa. La ultima rival es la Arania
 * de las Direcciones, jefa del bloque.
 *
 * Integra: structs y enum (12), punteros a struct (14), array de structs
 * (15), textos (11), azar (09) y la entrada validada (07, 13).
 *
 *   make run                          jugar
 *   ./programa < main.entrada.txt     partida grabada (la de la salida esperada)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define SEMILLA        2026    /* fija: la partida se puede repetir. Para jugar de verdad: time(NULL) */
#define POCIONES       2
#define CURA_POCION    30
#define TURNOS_DE_RED  3       /* la Arania teje su red cada tantos turnos */

typedef enum {
    ACCION_ATACAR = 1,
    ACCION_FUERTE,
    ACCION_POCION,
    ACCION_DEFENDER
} Accion;

typedef struct {
    char nombre[28];
    int  vida;
    int  vida_max;
    int  ataque;
    int  defensa;
    bool es_jefe;
} Luchador;

typedef struct {
    Luchador heroe;
    int      pociones;
    bool     defendiendo;
    bool     atrapada;                 /* en la red: pierde el proximo turno */
    int      turno_pelea;              /* se reinicia en cada oleada */
    int      turnos;                   /* de toda la partida */
    int      danio_hecho;
} Partida;

int  tirar(int minimo, int maximo);
Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe);
void mostrar(const Luchador *l);
bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado);
int  golpear(const Luchador *atacante, Luchador *defensor, int multiplicador);
void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion);
void turno_del_enemigo(Partida *p, Luchador *enemigo);
bool pelear(Partida *p, Luchador *enemigo);
void recompensa(Partida *p);

int main(void)
{
    srand(SEMILLA);
    Partida partida = {
        .heroe = crear("Kira", 90, 16, 3, false),
        .pociones = POCIONES,
    };
    Luchador oleadas[] = {
        crear("Slime de escoria", 30, 7, 0, false),
        crear("Goblin de la fragua", 45, 10, 2, false),
        crear("Orco del yunque", 60, 13, 4, false),
        crear("Araña de las Direcciones", 110, 17, 5, true),
    };
    int total = sizeof(oleadas) / sizeof(oleadas[0]);

    printf("=== LA ARENA DE LAS FORJAS ===\n");
    int vencidos = 0;
    for (int i = 0; i < total; i++) {
        printf("\n--- Oleada %d de %d: %s ---\n", i + 1, total, oleadas[i].nombre);
        if (!pelear(&partida, &oleadas[i])) {
            break;
        }
        vencidos++;
        printf("¡%s cae!\n", oleadas[i].nombre);
        if (i < total - 1) {
            recompensa(&partida);
        }
    }

    printf("\n=== RESULTADO ===\n");
    if (vencidos == total) {
        printf("¡Kira vence a la Araña de las Direcciones y gana la Arena!\n");
    } else {
        printf("Kira cae en la oleada %d. Ferrum la saca de la arena a la rastra.\n",
               vencidos + 1);
    }
    printf("oleadas vencidas: %d de %d | turnos: %d | daño hecho: %d | pociones sin usar: %d\n",
           vencidos, total, partida.turnos, partida.danio_hecho, partida.pociones);
    return 0;
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe)
{
    Luchador l = { .vida = vida, .vida_max = vida, .ataque = ataque,
                   .defensa = defensa, .es_jefe = es_jefe };
    snprintf(l.nombre, sizeof(l.nombre), "%s", nombre);
    return l;
}

/* Barra de vida de 10 segmentos:  [#######---] 63/90 Kira */
void mostrar(const Luchador *l)
{
    int llenos = l->vida * 10 / l->vida_max;
    printf("  [");
    for (int i = 0; i < 10; i++) {
        putchar(i < llenos ? '#' : '-');
    }
    printf("] %3d/%3d %s\n", l->vida, l->vida_max, l->nombre);
}

bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Elegí un número del %d al %d.\n", minimo, maximo);
    }
}

/* Danio = ataque + tirada de 0 a 4 - defensa (minimo 1), por el multiplicador */
int golpear(const Luchador *atacante, Luchador *defensor, int multiplicador)
{
    int danio = atacante->ataque + tirar(0, 4) - defensor->defensa;
    if (danio < 1) {
        danio = 1;
    }
    danio *= multiplicador;
    defensor->vida -= danio;
    if (defensor->vida < 0) {
        defensor->vida = 0;
    }
    return danio;
}

void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion)
{
    Luchador *kira = &p->heroe;
    int danio = 0;
    switch (accion) {
        case ACCION_ATACAR:
            danio = golpear(kira, enemigo, 1);
            printf("Kira ataca: %d de daño.\n", danio);
            break;
        case ACCION_FUERTE:
            if (tirar(1, 100) <= 55) {             /* 55 % de acertar */
                danio = golpear(kira, enemigo, 2);
                printf("¡Golpe fuerte! %d de daño.\n", danio);
            } else {
                printf("El golpe fuerte falla.\n");
            }
            break;
        case ACCION_POCION:
            if (p->pociones == 0) {
                printf("No quedan pociones: Kira pierde el turno buscando en la mochila.\n");
            } else {
                p->pociones--;
                kira->vida += CURA_POCION;
                if (kira->vida > kira->vida_max) {
                    kira->vida = kira->vida_max;
                }
                printf("Kira toma una poción (le quedan %d).\n", p->pociones);
            }
            break;
        case ACCION_DEFENDER:
            p->defendiendo = true;
            printf("Kira se cubre con el escudo.\n");
            break;
    }
    p->danio_hecho += danio;
}

void turno_del_enemigo(Partida *p, Luchador *enemigo)
{
    if (enemigo->es_jefe && p->turno_pelea % TURNOS_DE_RED == 0) {
        p->atrapada = true;
        printf("La Araña teje una red de hilos: ¡Kira queda atrapada!\n");
        return;
    }
    int danio = golpear(enemigo, &p->heroe, 1);
    if (p->defendiendo) {
        int bloqueado = danio / 2;             /* el escudo devuelve la mitad */
        p->heroe.vida += bloqueado;
        danio -= bloqueado;
        p->defendiendo = false;
    }
    printf("%s pega: %d de daño.\n", enemigo->nombre, danio);
}

/* Devuelve true si Kira gana esta pelea */
bool pelear(Partida *p, Luchador *enemigo)
{
    p->turno_pelea = 0;
    while (p->heroe.vida > 0 && enemigo->vida > 0) {
        p->turno_pelea++;
        p->turnos++;
        mostrar(&p->heroe);
        mostrar(enemigo);

        if (p->atrapada) {
            printf("Kira forcejea con la red y pierde el turno.\n");
            p->atrapada = false;
        } else {
            int opcion;
            if (!pedir_opcion("1) atacar  2) golpe fuerte  3) poción  4) defender: ",
                              1, 4, &opcion)) {
                opcion = ACCION_ATACAR;        /* sin entrada: ataca sola */
            }
            printf("\n");
            turno_de_kira(p, enemigo, (Accion) opcion);
        }
        if (enemigo->vida > 0) {
            turno_del_enemigo(p, enemigo);
        }
    }
    return p->heroe.vida > 0;
}

void recompensa(Partida *p)
{
    printf("Ferrum ofrece una recompensa:\n");
    int opcion;
    if (!pedir_opcion("1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: ",
                      1, 3, &opcion)) {
        opcion = 3;
    }
    printf("\n");
    switch (opcion) {
        case 1:
            p->heroe.vida_max += 20;
            p->heroe.vida = p->heroe.vida_max;
            printf("Kira recupera toda la vida: %d.\n", p->heroe.vida);
            break;
        case 2:
            p->heroe.ataque += 3;
            printf("El ataque de Kira sube a %d.\n", p->heroe.ataque);
            break;
        default:
            p->pociones++;
            printf("Kira guarda otra poción (tiene %d).\n", p->pociones);
            break;
    }
}
```

#### Entrada de ejemplo

```
tres
9
1
1
vida
2
4
1
1
1
1
1
1
1
2
2
2
3
2
3
2
2
2
2
```

#### Salida esperada

```
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender: 
  Elegí un número del 1 al 4.
1) atacar  2) golpe fuerte  3) poción  4) defender: 
  Elegí un número del 1 al 4.
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Slime de escoria pega: 6 de daño.
  [#########-]  84/ 90 Kira
  [####------]  12/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 19 de daño.
¡Slime de escoria cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
  Elegí un número del 1 al 3.
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
El ataque de Kira sube a 19.

--- Oleada 2 de 4: Goblin de la fragua ---
  [#########-]  84/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira se cubre con el escudo.
Goblin de la fragua pega: 6 de daño.
  [########--]  78/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Goblin de la fragua pega: 8 de daño.
  [#######---]  70/ 90 Kira
  [######----]  27/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 19 de daño.
Goblin de la fragua pega: 9 de daño.
  [######----]  61/ 90 Kira
  [#---------]   8/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 21 de daño.
¡Goblin de la fragua cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
Kira recupera toda la vida: 110.

--- Oleada 3 de 4: Orco del yunque ---
  [##########] 110/110 Kira
  [##########]  60/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 18 de daño.
Orco del yunque pega: 13 de daño.
  [########--]  97/110 Kira
  [#######---]  42/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 15 de daño.
Orco del yunque pega: 14 de daño.
  [#######---]  83/110 Kira
  [####------]  27/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira ataca: 17 de daño.
Orco del yunque pega: 12 de daño.
  [######----]  71/110 Kira
  [#---------]  10/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 30 de daño.
¡Orco del yunque cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: 
El ataque de Kira sube a 22.

--- Oleada 4 de 4: Araña de las Direcciones ---
  [######----]  71/110 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 18 de daño.
  [####------]  53/110 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 1).
Araña de las Direcciones pega: 14 de daño.
  [######----]  69/110 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 38 de daño.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [######----]  69/110 Kira
  [######----]  72/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 15 de daño.
  [####------]  54/110 Kira
  [######----]  72/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
Kira toma una poción (le quedan 0).
Araña de las Direcciones pega: 16 de daño.
  [######----]  68/110 Kira
  [######----]  72/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 34 de daño.
La Araña teje una red de hilos: ¡Kira queda atrapada!
  [######----]  68/110 Kira
  [###-------]  38/110 Araña de las Direcciones
Kira forcejea con la red y pierde el turno.
Araña de las Direcciones pega: 14 de daño.
  [####------]  54/110 Kira
  [###-------]  38/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
El golpe fuerte falla.
Araña de las Direcciones pega: 16 de daño.
  [###-------]  38/110 Kira
  [###-------]  38/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender: 
¡Golpe fuerte! 40 de daño.
¡Araña de las Direcciones cae!

=== RESULTADO ===
¡Kira vence a la Araña de las Direcciones y gana la Arena!
oleadas vencidas: 4 de 4 | turnos: 19 | daño hecho: 287 | pociones sin usar: 0

Los golpes más fuertes (de 12):
  1. 40 de daño a Araña de las Direcciones (turno 19)
  2. 38 de daño a Araña de las Direcciones (turno 13)
  3. 34 de daño a Araña de las Direcciones (turno 16)
```

#### Solución de referencia

```c
/*
 * Mision 3 - La cronica de la pelea: cada golpe que da Kira se guarda en un
 * array de structs (turno, enemigo, danio). Al final se muestran los 3 mas
 * fuertes, ordenados con qsort.
 * Probar con:  ./sol < mision3_cronica.entrada.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define SEMILLA        2026    /* fija: la partida se puede repetir. Para jugar de verdad: time(NULL) */
#define POCIONES       2
#define CURA_POCION    30
#define TURNOS_DE_RED  3       /* la Arania teje su red cada tantos turnos */
#define MAX_GOLPES     64

typedef enum {
    ACCION_ATACAR = 1,
    ACCION_FUERTE,
    ACCION_POCION,
    ACCION_DEFENDER
} Accion;

typedef struct {
    char nombre[28];
    int  vida;
    int  vida_max;
    int  ataque;
    int  defensa;
    bool es_jefe;
} Luchador;

typedef struct {
    int  turno;
    char enemigo[28];
    int  danio;
} Golpe;

typedef struct {
    Luchador heroe;
    int      pociones;
    bool     defendiendo;
    bool     atrapada;                 /* en la red: pierde el proximo turno */
    int      turno_pelea;              /* se reinicia en cada oleada */
    int      turnos;                   /* de toda la partida */
    int      danio_hecho;
    Golpe    golpes[MAX_GOLPES];
    int      cantidad_golpes;
} Partida;

int  tirar(int minimo, int maximo);
Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe);
void mostrar(const Luchador *l);
bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado);
int  golpear(const Luchador *atacante, Luchador *defensor, int multiplicador);
void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion);
void turno_del_enemigo(Partida *p, Luchador *enemigo);
bool pelear(Partida *p, Luchador *enemigo);
void recompensa(Partida *p);
int  comparar_golpes(const void *a, const void *b);

int main(void)
{
    srand(SEMILLA);
    Partida partida = {
        .heroe = crear("Kira", 90, 16, 3, false),
        .pociones = POCIONES,
    };
    Luchador oleadas[] = {
        crear("Slime de escoria", 30, 7, 0, false),
        crear("Goblin de la fragua", 45, 10, 2, false),
        crear("Orco del yunque", 60, 13, 4, false),
        crear("Araña de las Direcciones", 110, 17, 5, true),
    };
    int total = sizeof(oleadas) / sizeof(oleadas[0]);

    printf("=== LA ARENA DE LAS FORJAS ===\n");
    int vencidos = 0;
    for (int i = 0; i < total; i++) {
        printf("\n--- Oleada %d de %d: %s ---\n", i + 1, total, oleadas[i].nombre);
        if (!pelear(&partida, &oleadas[i])) {
            break;
        }
        vencidos++;
        printf("¡%s cae!\n", oleadas[i].nombre);
        if (i < total - 1) {
            recompensa(&partida);
        }
    }

    printf("\n=== RESULTADO ===\n");
    if (vencidos == total) {
        printf("¡Kira vence a la Araña de las Direcciones y gana la Arena!\n");
    } else {
        printf("Kira cae en la oleada %d. Ferrum la saca de la arena a la rastra.\n",
               vencidos + 1);
    }
    printf("oleadas vencidas: %d de %d | turnos: %d | daño hecho: %d | pociones sin usar: %d\n",
           vencidos, total, partida.turnos, partida.danio_hecho, partida.pociones);

    qsort(partida.golpes, partida.cantidad_golpes, sizeof(Golpe), comparar_golpes);
    printf("\nLos golpes más fuertes (de %d):\n", partida.cantidad_golpes);
    for (int i = 0; i < 3 && i < partida.cantidad_golpes; i++) {
        const Golpe *g = &partida.golpes[i];
        printf("  %d. %2d de daño a %s (turno %d)\n", i + 1, g->danio, g->enemigo, g->turno);
    }
    return 0;
}

/* De mayor a menor danio; si empatan, el turno mas temprano primero */
int comparar_golpes(const void *a, const void *b)
{
    const Golpe *x = a;
    const Golpe *y = b;
    if (x->danio != y->danio) {
        return y->danio - x->danio;
    }
    return x->turno - y->turno;
}

int tirar(int minimo, int maximo)
{
    return minimo + rand() % (maximo - minimo + 1);
}

Luchador crear(const char *nombre, int vida, int ataque, int defensa, bool es_jefe)
{
    Luchador l = { .vida = vida, .vida_max = vida, .ataque = ataque,
                   .defensa = defensa, .es_jefe = es_jefe };
    snprintf(l.nombre, sizeof(l.nombre), "%s", nombre);
    return l;
}

/* Barra de vida de 10 segmentos:  [#######---] 63/90 Kira */
void mostrar(const Luchador *l)
{
    int llenos = l->vida * 10 / l->vida_max;
    printf("  [");
    for (int i = 0; i < 10; i++) {
        putchar(i < llenos ? '#' : '-');
    }
    printf("] %3d/%3d %s\n", l->vida, l->vida_max, l->nombre);
}

bool pedir_opcion(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  Elegí un número del %d al %d.\n", minimo, maximo);
    }
}

/* Danio = ataque + tirada de 0 a 4 - defensa (minimo 1), por el multiplicador */
int golpear(const Luchador *atacante, Luchador *defensor, int multiplicador)
{
    int danio = atacante->ataque + tirar(0, 4) - defensor->defensa;
    if (danio < 1) {
        danio = 1;
    }
    danio *= multiplicador;
    defensor->vida -= danio;
    if (defensor->vida < 0) {
        defensor->vida = 0;
    }
    return danio;
}

void turno_de_kira(Partida *p, Luchador *enemigo, Accion accion)
{
    Luchador *kira = &p->heroe;
    int danio = 0;
    switch (accion) {
        case ACCION_ATACAR:
            danio = golpear(kira, enemigo, 1);
            printf("Kira ataca: %d de daño.\n", danio);
            break;
        case ACCION_FUERTE:
            if (tirar(1, 100) <= 55) {             /* 55 % de acertar */
                danio = golpear(kira, enemigo, 2);
                printf("¡Golpe fuerte! %d de daño.\n", danio);
            } else {
                printf("El golpe fuerte falla.\n");
            }
            break;
        case ACCION_POCION:
            if (p->pociones == 0) {
                printf("No quedan pociones: Kira pierde el turno buscando en la mochila.\n");
            } else {
                p->pociones--;
                kira->vida += CURA_POCION;
                if (kira->vida > kira->vida_max) {
                    kira->vida = kira->vida_max;
                }
                printf("Kira toma una poción (le quedan %d).\n", p->pociones);
            }
            break;
        case ACCION_DEFENDER:
            p->defendiendo = true;
            printf("Kira se cubre con el escudo.\n");
            break;
    }
    p->danio_hecho += danio;
    if (danio > 0 && p->cantidad_golpes < MAX_GOLPES) {
        Golpe *g = &p->golpes[p->cantidad_golpes];
        g->turno = p->turnos;
        snprintf(g->enemigo, sizeof(g->enemigo), "%s", enemigo->nombre);
        g->danio = danio;
        p->cantidad_golpes++;
    }
}

void turno_del_enemigo(Partida *p, Luchador *enemigo)
{
    if (enemigo->es_jefe && p->turno_pelea % TURNOS_DE_RED == 0) {
        p->atrapada = true;
        printf("La Araña teje una red de hilos: ¡Kira queda atrapada!\n");
        return;
    }
    int danio = golpear(enemigo, &p->heroe, 1);
    if (p->defendiendo) {
        int bloqueado = danio / 2;             /* el escudo devuelve la mitad */
        p->heroe.vida += bloqueado;
        danio -= bloqueado;
        p->defendiendo = false;
    }
    printf("%s pega: %d de daño.\n", enemigo->nombre, danio);
}

/* Devuelve true si Kira gana esta pelea */
bool pelear(Partida *p, Luchador *enemigo)
{
    p->turno_pelea = 0;
    while (p->heroe.vida > 0 && enemigo->vida > 0) {
        p->turno_pelea++;
        p->turnos++;
        mostrar(&p->heroe);
        mostrar(enemigo);

        if (p->atrapada) {
            printf("Kira forcejea con la red y pierde el turno.\n");
            p->atrapada = false;
        } else {
            int opcion;
            if (!pedir_opcion("1) atacar  2) golpe fuerte  3) poción  4) defender: ",
                              1, 4, &opcion)) {
                opcion = ACCION_ATACAR;        /* sin entrada: ataca sola */
            }
            printf("\n");
            turno_de_kira(p, enemigo, (Accion) opcion);
        }
        if (enemigo->vida > 0) {
            turno_del_enemigo(p, enemigo);
        }
    }
    return p->heroe.vida > 0;
}

void recompensa(Partida *p)
{
    printf("Ferrum ofrece una recompensa:\n");
    int opcion;
    if (!pedir_opcion("1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción: ",
                      1, 3, &opcion)) {
        opcion = 3;
    }
    printf("\n");
    switch (opcion) {
        case 1:
            p->heroe.vida_max += 20;
            p->heroe.vida = p->heroe.vida_max;
            printf("Kira recupera toda la vida: %d.\n", p->heroe.vida);
            break;
        case 2:
            p->heroe.ataque += 3;
            printf("El ataque de Kira sube a %d.\n", p->heroe.ataque);
            break;
        default:
            p->pociones++;
            printf("Kira guarda otra poción (tiene %d).\n", p->pociones);
            break;
    }
}
```

#### Pruebas

##### Sin golpes
```entrada
4
```
```salida
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira se cubre con el escudo.
Slime de escoria pega: 3 de daño.
  [#########-]  87/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
Slime de escoria pega: 7 de daño.
  [########--]  80/ 90 Kira
  [####------]  12/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 20 de daño.
¡Slime de escoria cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 3).

--- Oleada 2 de 4: Goblin de la fragua ---
  [########--]  80/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Goblin de la fragua pega: 8 de daño.
  [########--]  72/ 90 Kira
  [######----]  30/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Goblin de la fragua pega: 9 de daño.
  [#######---]  63/ 90 Kira
  [###-------]  14/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
¡Goblin de la fragua cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 4).

--- Oleada 3 de 4: Orco del yunque ---
  [#######---]  63/ 90 Kira
  [##########]  60/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Orco del yunque pega: 13 de daño.
  [#####-----]  50/ 90 Kira
  [#######---]  45/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 12 de daño.
Orco del yunque pega: 14 de daño.
  [####------]  36/ 90 Kira
  [#####-----]  33/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 14 de daño.
Orco del yunque pega: 12 de daño.
  [##--------]  24/ 90 Kira
  [###-------]  19/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 13 de daño.
Orco del yunque pega: 10 de daño.
  [#---------]  14/ 90 Kira
  [#---------]   6/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 13 de daño.
¡Orco del yunque cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 5).

--- Oleada 4 de 4: Araña de las Direcciones ---
  [#---------]  14/ 90 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Araña de las Direcciones pega: 14 de daño.

=== RESULTADO ===
Kira cae en la oleada 4. Ferrum la saca de la arena a la rastra.
oleadas vencidas: 3 de 4 | turnos: 12 | daño hecho: 169 | pociones sin usar: 5

Los golpes más fuertes (de 11):
  1. 20 de daño a Slime de escoria (turno 3)
  2. 18 de daño a Slime de escoria (turno 2)
  3. 18 de daño a Goblin de la fragua (turno 6)
```

##### Golpes fuertes
```entrada
2
2
2
2
2
2
```
```salida
=== LA ARENA DE LAS FORJAS ===

--- Oleada 1 de 4: Slime de escoria ---
  [##########]  90/ 90 Kira
  [##########]  30/ 30 Slime de escoria
1) atacar  2) golpe fuerte  3) poción  4) defender:
¡Golpe fuerte! 36 de daño.
¡Slime de escoria cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
El ataque de Kira sube a 19.

--- Oleada 2 de 4: Goblin de la fragua ---
  [##########]  90/ 90 Kira
  [##########]  45/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
¡Golpe fuerte! 42 de daño.
Goblin de la fragua pega: 8 de daño.
  [#########-]  82/ 90 Kira
  [----------]   3/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
El golpe fuerte falla.
Goblin de la fragua pega: 9 de daño.
  [########--]  73/ 90 Kira
  [----------]   3/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
El golpe fuerte falla.
Goblin de la fragua pega: 11 de daño.
  [######----]  62/ 90 Kira
  [----------]   3/ 45 Goblin de la fragua
1) atacar  2) golpe fuerte  3) poción  4) defender:
¡Golpe fuerte! 40 de daño.
¡Goblin de la fragua cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 3).

--- Oleada 3 de 4: Orco del yunque ---
  [######----]  62/ 90 Kira
  [##########]  60/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 15 de daño.
Orco del yunque pega: 14 de daño.
  [#####-----]  48/ 90 Kira
  [#######---]  45/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 17 de daño.
Orco del yunque pega: 12 de daño.
  [####------]  36/ 90 Kira
  [####------]  28/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Orco del yunque pega: 10 de daño.
  [##--------]  26/ 90 Kira
  [##--------]  12/ 60 Orco del yunque
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
¡Orco del yunque cae!
Ferrum ofrece una recompensa:
1) +20 de vida máxima y curarse  2) +3 de ataque  3) una poción:
Kira guarda otra poción (tiene 4).

--- Oleada 4 de 4: Araña de las Direcciones ---
  [##--------]  26/ 90 Kira
  [##########] 110/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 18 de daño.
Araña de las Direcciones pega: 14 de daño.
  [#---------]  12/ 90 Kira
  [########--]  92/110 Araña de las Direcciones
1) atacar  2) golpe fuerte  3) poción  4) defender:
Kira ataca: 16 de daño.
Araña de las Direcciones pega: 16 de daño.

=== RESULTADO ===
Kira cae en la oleada 4. Ferrum la saca de la arena a la rastra.
oleadas vencidas: 3 de 4 | turnos: 11 | daño hecho: 216 | pociones sin usar: 4

Los golpes más fuertes (de 9):
  1. 42 de daño a Goblin de la fragua (turno 2)
  2. 40 de daño a Goblin de la fragua (turno 5)
  3. 36 de daño a Slime de escoria (turno 1)
```

### Encargo R02-N07-E1 · La agenda del consultorio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

El consultorio del Gremio necesita una **agenda del día**: un menú para agregar
turnos (hora `hh:mm` validada, sin dos turnos a la misma hora, paciente no
vacío), ver la agenda **ordenada por hora** con `qsort`, marcar un turno como
atendido y listar los pendientes. Capacidad fija de 8 turnos.

#### Criterio de aprobación

- Menú para agregar turnos (hora `hh:mm` validada, sin repetir hora, paciente no vacío).
- Muestra la agenda ordenada por hora con `qsort`.
- Marca turnos como atendidos y lista los pendientes; capacidad fija de 8.

#### Entrada de ejemplo

```
1
10:30
Ana Pérez
1
9:00
Beto Gómez
1
25:10
1
10:30
1
11:15
Caro Díaz
2
3
9:00
3
12:00
cuatro
4
0
```

#### Salida esperada

```
1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Hora inválida.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Ya hay un turno a esa hora.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción:   09:00  Beto Gómez      pendiente
  10:30  Ana Pérez       pendiente
  11:15  Caro Díaz       pendiente

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora del turno atendido: Beto Gómez, atendido/a.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora del turno atendido: No hay turno a esa hora.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: 
  tiene que ser un número entre 0 y 4.
Opción:   10:30  Ana Pérez       pendiente
  11:15  Caro Díaz       pendiente

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Fin del día.
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - La agenda del consultorio: turnos del dia en un array
 * de structs, con menu. Agregar (hora "hh:mm" validada, sin repetir hora),
 * listar ordenado por hora con qsort, marcar como atendido y ver pendientes.
 * Probar con:  ./sol < gremio_consultorio.entrada.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_TURNOS 8

typedef struct {
    int  minutos;                  /* hora del turno, en minutos desde las 00:00 */
    char paciente[24];
    bool atendido;
} Turno;

typedef struct {
    Turno turnos[MAX_TURNOS];
    int   cantidad;
} Agenda;

bool   pedir_entero(const char *pregunta, int minimo, int maximo, int *resultado);
bool   pedir_texto(const char *pregunta, char destino[], int tam);
bool   leer_hora(const char *texto, int *minutos);
Turno *buscar(Agenda *a, int minutos);
int    comparar_hora(const void *x, const void *y);
void   listar(Agenda *a, bool solo_pendientes);

int main(void)
{
    Agenda agenda = { .cantidad = 0 };
    int opcion = -1;
    while (opcion != 0) {
        printf("\n1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir\n");
        if (!pedir_entero("Opción: ", 0, 4, &opcion)) {
            break;
        }
        char texto[24];
        int minutos;
        Turno *t;
        switch (opcion) {
            case 1:
                if (agenda.cantidad == MAX_TURNOS) {
                    printf("La agenda del día está completa.\n");
                    break;
                }
                if (!pedir_texto("Hora (hh:mm): ", texto, sizeof(texto))) {
                    break;
                }
                if (!leer_hora(texto, &minutos)) {
                    printf("Hora inválida.\n");
                    break;
                }
                if (buscar(&agenda, minutos) != NULL) {
                    printf("Ya hay un turno a esa hora.\n");
                    break;
                }
                t = &agenda.turnos[agenda.cantidad];
                if (!pedir_texto("Paciente: ", t->paciente, sizeof(t->paciente))) {
                    break;
                }
                t->minutos = minutos;
                t->atendido = false;
                agenda.cantidad++;
                printf("Turno agendado.\n");
                break;
            case 2:
            case 4:
                listar(&agenda, opcion == 4);
                break;
            case 3:
                if (!pedir_texto("Hora del turno atendido: ", texto, sizeof(texto))) {
                    break;
                }
                t = leer_hora(texto, &minutos) ? buscar(&agenda, minutos) : NULL;
                if (t == NULL) {
                    printf("No hay turno a esa hora.\n");
                } else {
                    t->atendido = true;
                    printf("%s, atendido/a.\n", t->paciente);
                }
                break;
        }
    }
    printf("Fin del día.\n");
    return 0;
}

bool pedir_entero(const char *pregunta, int minimo, int maximo, int *resultado)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        int n;
        char sobra;
        if (sscanf(linea, "%d %c", &n, &sobra) == 1 && n >= minimo && n <= maximo) {
            *resultado = n;
            return true;
        }
        printf("\n  tiene que ser un número entre %d y %d.\n", minimo, maximo);
    }
}

bool pedir_texto(const char *pregunta, char destino[], int tam)
{
    char linea[100];
    for (;;) {
        printf("%s", pregunta);
        if (fgets(linea, sizeof(linea), stdin) == NULL) {
            return false;
        }
        linea[strcspn(linea, "\n")] = '\0';
        if (linea[0] != '\0') {
            snprintf(destino, (size_t) tam, "%s", linea);
            return true;
        }
        printf("\n  no puede estar vacío.\n");
    }
}

bool leer_hora(const char *texto, int *minutos)
{
    int h, m;
    char sobra;
    if (sscanf(texto, "%d:%d %c", &h, &m, &sobra) != 2 || h < 0 || h > 23 || m < 0 || m > 59) {
        return false;
    }
    *minutos = h * 60 + m;
    return true;
}

Turno *buscar(Agenda *a, int minutos)
{
    for (int i = 0; i < a->cantidad; i++) {
        if (a->turnos[i].minutos == minutos) {
            return &a->turnos[i];
        }
    }
    return NULL;
}

int comparar_hora(const void *x, const void *y)
{
    const Turno *a = x;
    const Turno *b = y;
    return a->minutos - b->minutos;
}

/* Ordena la agenda por hora y la muestra */
void listar(Agenda *a, bool solo_pendientes)
{
    qsort(a->turnos, a->cantidad, sizeof(Turno), comparar_hora);
    int mostrados = 0;
    for (int i = 0; i < a->cantidad; i++) {
        const Turno *t = &a->turnos[i];
        if (solo_pendientes && t->atendido) {
            continue;
        }
        printf("  %02d:%02d  %-16s %s\n", t->minutos / 60, t->minutos % 60, t->paciente,
               t->atendido ? "atendido" : "pendiente");
        mostrados++;
    }
    if (mostrados == 0) {
        printf("  (no hay turnos)\n");
    }
}
```

#### Pruebas

##### Agenda vacía
```entrada
2
4
0
```
```salida
1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción:   (no hay turnos)

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción:   (no hay turnos)

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Fin del día.
```

##### Agenda llena
```entrada
1
08:00
A
1
08:10
B
1
08:20
C
1
08:30
D
1
08:40
E
1
08:50
F
1
09:00
G
1
09:10
H
1
09:20
I
2
0
```
```salida
1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: La agenda del día está completa.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción:
  tiene que ser un número entre 0 y 4.
Opción:
  tiene que ser un número entre 0 y 4.
Opción:   08:00  A                pendiente
  08:10  B                pendiente
  08:20  C                pendiente
  08:30  D                pendiente
  08:40  E                pendiente
  08:50  F                pendiente
  09:00  G                pendiente
  09:10  H                pendiente

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Fin del día.
```

##### Atender una hora sin turno
```entrada
1
10:00
Ana
3
10:01
3
10:00
3
10:00
0
```
```salida
1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora (hh:mm): Paciente: Turno agendado.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora del turno atendido: No hay turno a esa hora.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora del turno atendido: Ana, atendido/a.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Hora del turno atendido: Ana, atendido/a.

1) nuevo turno  2) agenda  3) atender  4) pendientes  0) salir
Opción: Fin del día.
```

### Prueba del sello

#### ¿Por qué `golpear` recibe el atacante como `const Luchador *` y el defensor como `Luchador *`?

Porque el atacante solo se lee (`const` lo garantiza) y el defensor se modifica: pierde vida.

#### ¿Qué pasaría si `pelear` recibiera el `Luchador` por valor?

Pelearía una copia: al terminar, el luchador original quedaría igual, sin el daño recibido.

#### ¿Para qué sirve el campo `atrapada`? ¿Quién lo pone en `true` y quién en `false`?

Para que Kira pierda su próximo turno. Lo pone en `true` la red de la Araña y lo vuelve a `false` el turno que se pierde.

#### ¿Qué hace el programa si se termina la entrada en el medio de una pelea?

`fgets` devuelve `NULL`, `pedir_opcion` devuelve `false` y la pelea termina: el programa cierra ordenado en lugar de repetir la pregunta para siempre.

#### ¿Cómo cambiarías el juego para que cada partida sea distinta?

Con `srand(time(NULL))` en lugar de una semilla fija.

#### ¿Qué habría que tocar para agregar una quinta oleada?

Agregar el rival al array de oleadas (y su cantidad): el bucle principal ya recorre la lista.

### Soluciones (docente)

Material original: `01-C/16-ProyectoArena` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

Es el proyecto del bloque 2 de `01-C`. La salida del ejemplo depende de `srand` con semilla fija y de glibc.
