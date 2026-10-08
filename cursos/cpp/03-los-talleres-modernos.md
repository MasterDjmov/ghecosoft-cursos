# RAMA R03 · Los Talleres Modernos: el C++ de hoy

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · auto, array y el for de rango

```meta
tipo: tema
padre: R02-N09
precio: 10
criatura: goblin
temas: col.arrays
usa: prog.bucles
```

### Crónica

Pasando la Arena, llegás a los **Talleres Modernos**: salas luminosas donde los artífices jóvenes trabajan rápido, con herramientas que en tiempos de Ferrum no existían.

—Acá se escribe el C++ de hoy —dice {mentor}—. El mismo lenguaje, pero con herramientas que te ahorran escribir lo obvio. La primera: dejar que el Taller **deduzca** los tipos. Con cuidado: un goblin se esconde en cada copia que no querías hacer.

### Objetivos

Usar `auto` para que el compilador deduzca tipos, recorrer con `for` de rango
eligiendo bien entre copia (`auto`), referencia (`auto&`) y lectura
(`const auto&`), separar structs y pares con *structured bindings*, y elegir entre
`std::array` (tamaño fijo) y `std::vector` (tamaño variable).

### Antes de empezar

- Vectores y el `for` de rango (rama 1).
- Structs y clases (rama 2).

### Explicación

#### `auto`: que el compilador deduzca
```cpp
auto torres = 12;                   // int
auto altura = 37.5;                 // double
auto nombre = std::string("Reloj"); // std::string
auto it = equipo.begin();           // std::vector<std::string>::iterator (¡largo!)
```
`auto` no es "cualquier tipo": el tipo se deduce **al compilar**, del valor inicial,
y queda fijo. Por eso `auto x;` sin valor no compila. Se usa sobre todo cuando el
tipo es largo o evidente. Cuando el tipo ayuda a entender, escribilo.

Ojo: `auto nombre = "Reloj";` deduce `const char*` (un texto de C), no
`std::string`. Para un `std::string`, escribilo explícito.

#### `auto` en el `for` de rango: la regla de oro
| Escribís | Qué es cada elemento | Úsalo para |
|---|---|---|
| `for (auto x : v)` | una **copia** | tipos chicos (`int`, `char`) que solo leés |
| `for (const auto& x : v)` | el original, **solo lectura** | leer cualquier cosa sin copiar (**el caso normal**) |
| `for (auto& x : v)` | el original, **modificable** | cambiar los elementos |

`auto e = caja[0];` también **copia**. Para tener el original: `auto& e = caja[0];`.

#### Structured bindings: ponerle nombre a las partes
```cpp
struct Punto { int x; int y; };
auto [x, y] = faro;                         // x = faro.x, y = faro.y
for (const auto& [px, py] : ruta) { ... }   // en un recorrido
```
Separa un struct, un par o una tupla en variables con nombre, en el orden de sus
campos. Vas a usarlo muchísimo con los `map` (nodo siguiente). También sirve para
**devolver varios valores**: la función devuelve un struct y quien llama escribe
`auto [maximo, minimo, promedio] = resumir(datos);`.

#### `std::array`: tamaño fijo
```cpp
std::array<int, 4> dano = {10, 12, 10, 8};    // exactamente 4 enteros
std::array<int, 7> temperaturas{};            // 7 ceros
dano.size();   dano.at(2);   dano.fill(0);
```
El tamaño es **parte del tipo** y no cambia: no hay `push_back`. Ventajas: no pide
memoria dinámica, sabe su tamaño y se copia, compara y pasa por referencia como
cualquier objeto. Regla práctica:
- tamaño fijo y conocido (los 7 días, las 4 direcciones, un tablero de 3×3) →
  `std::array`;
- el tamaño cambia → `std::vector`.

#### `using`: ponerle nombre a un tipo largo
```cpp
using Tablero = std::array<std::array<char, 3>, 3>;
Tablero t;
```

#### Más de `std::vector`
- `v.capacity()` ≥ `v.size()`: el vector reserva lugar de más para crecer rápido.
  `v.reserve(n)` reserva de antemano si sabés cuántos van a ser.
- `v.resize(n)` agranda (con ceros) o recorta.
- `std::accumulate(v.begin(), v.end(), 0)` (de `<numeric>`) suma todo. Ojo: el
  tipo del resultado es el del valor inicial; para sumar `double`, `0.0`.

> **Si venís de C.** `std::array<int, 4>` reemplaza a `int x[4]`, pero sabe su
> tamaño, se copia con `=` y no se "degrada" a puntero al pasarlo a una función.

### Código de ejemplo

```cpp
/*
 * auto, for de rango, structured bindings y std::array.
 */
#include <array>
#include <iostream>
#include <numeric>   // std::accumulate
#include <string>
#include <vector>

struct Punto {
    int x = 0;
    int y = 0;
};

int main()
{
    // auto: el compilador deduce el tipo del valor inicial (y queda fijo)
    auto torres = 12;               // int
    auto altura = 37.5;             // double
    auto nombre = std::string("Reloj");
    std::cout << nombre << ": " << torres << " torres de " << altura << " m\n";

    // En el for de rango: const auto& lee sin copiar; auto& permite modificar
    std::vector<std::string> equipo = {"Kira", "Bron", "Lyn"};
    for (const auto& n : equipo) {
        std::cout << "  - " << n << "\n";
    }
    std::vector<int> vidas = {100, 80, 140};
    for (auto& v : vidas) {
        v -= 10;
    }
    std::cout << "Vidas tras la trampa:";
    for (auto v : vidas) {
        std::cout << " " << v;
    }
    std::cout << "\n";

    // structured bindings: separar un struct (o un par) en variables con nombre
    Punto faro{7, -2};
    auto [x, y] = faro;
    std::cout << "El faro está en x=" << x << ", y=" << y << "\n";

    std::vector<Punto> ruta = {{0, 0}, {3, 4}, {6, 0}};
    for (const auto& [px, py] : ruta) {
        std::cout << "  (" << px << ", " << py << ")";
    }
    std::cout << "\n";

    // std::array: tamanio FIJO, conocido al compilar. Sabe su size() y no crece.
    std::array<int, 4> dano_por_direccion = {10, 12, 10, 8};    // arriba, derecha, abajo, izquierda
    int suma = std::accumulate(dano_por_direccion.begin(), dano_por_direccion.end(), 0);
    std::cout << "array de " << dano_por_direccion.size() << ", suma " << suma
              << ", abajo: " << dano_por_direccion.at(2) << "\n";

    // vector: tamanio variable. capacity() >= size(): reserva de mas para crecer rapido.
    std::vector<int> puntajes;
    for (int ronda = 1; ronda <= 5; ronda++) {
        puntajes.push_back(ronda * 100);
    }
    std::cout << "vector de " << puntajes.size() << ", suma "
              << std::accumulate(puntajes.begin(), puntajes.end(), 0) << "\n";
    puntajes.resize(3);
    std::cout << "tras resize(3):";
    for (auto p : puntajes) {
        std::cout << " " << p;
    }
    std::cout << "\n";
    return 0;
}
```

### Salida esperada

```
Reloj: 12 torres de 37.5 m
  - Kira
  - Bron
  - Lyn
Vidas tras la trampa: 90 70 130
El faro está en x=7, y=-2
  (0, 0)  (3, 4)  (6, 0)
array de 4, suma 40, abajo: 10
vector de 5, suma 1500
tras resize(3): 100 200 300
```

### ¿Para qué sirve?

El C++ moderno profesional se escribe así: `auto` para los tipos largos de la biblioteca, `const auto&` en cada recorrido, structured bindings para trabajar con pares y registros. `std::array` es ideal para datos de tamaño fijo muy usados: los píxeles de un color (RGBA), las coordenadas de un vector 3D, los días de la semana, el tablero de un juego.

### Errores habituales

**Slime: `auto` sin valor.**
```
main.cpp:1:14: error: declaration of ‘auto x’ has no initializer
```

**Goblin: la copia escondida.** `for (auto e : caja) e.dientes -= 2;` modifica
copias. Y con objetos grandes, `for (auto e : v)` copia cada uno: usá `const auto&`.

**Goblin: `auto` con un texto entre comillas.** `auto s = "hola"; s += "!";` no
compila: `s` es un `const char*`, no un `std::string`.

**Goblin: `std::accumulate` con el valor inicial entero.**
`std::accumulate(precios.begin(), precios.end(), 0)` con precios `double` **trunca
cada suma** a entero. Usá `0.0`.

**Orco: `std::array` fuera de rango.** Como en el vector: `a[7]` en un array de 7
no avisa; `a.at(7)` sí.

**Troll: guardar un `auto&` a un elemento de un vector que después crece.** Si
hacés `push_back`, el vector puede mudarse a otra memoria y la referencia queda
colgando.

### Misión R03-N01-M1 · La semana del faro

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé las 7 temperaturas de la semana en un `std::array<int, 7>`. Mostralas con el
nombre del día (otro `std::array` constante) y escribí una función
`resumir(const std::array<int, 7>&)` que devuelva un struct con máxima, mínima y
promedio. En `main`, recibilo con structured bindings.

#### Criterio de aprobación

- Usa `std::array` para los datos y los nombres.
- La función devuelve un struct y `main` lo separa con `auto [a, b, c]`.

#### Entrada de ejemplo

```
18 21 19 24 26 22 17
```

#### Salida esperada

```
lun: 18
mar: 21
mié: 19
jue: 24
vie: 26
sáb: 22
dom: 17
Máxima 26, mínima 17, promedio 21
```

#### Solución de referencia

```cpp
// Mision 1 - La semana del faro: std::array de 7 dias y structured bindings.
#include <array>
#include <iostream>
#include <numeric>
#include <string>

struct Resumen {
    int maximo;
    int minimo;
    double promedio;
};

Resumen resumir(const std::array<int, 7>& t)
{
    int maximo = t[0];
    int minimo = t[0];
    for (auto v : t) {
        if (v > maximo) {
            maximo = v;
        }
        if (v < minimo) {
            minimo = v;
        }
    }
    return {maximo, minimo, std::accumulate(t.begin(), t.end(), 0) / 7.0};
}

int main()
{
    const std::array<std::string, 7> dias = {"lun", "mar", "mié", "jue", "vie", "sáb", "dom"};
    std::array<int, 7> temperaturas{};
    for (auto& t : temperaturas) {
        std::cin >> t;
    }
    for (std::size_t i = 0; i < dias.size(); i++) {
        std::cout << dias[i] << ": " << temperaturas[i] << "\n";
    }
    auto [maximo, minimo, promedio] = resumir(temperaturas);
    std::cout << "Máxima " << maximo << ", mínima " << minimo << ", promedio " << promedio << "\n";
    return 0;
}
```

#### Pruebas

##### Todas iguales
```entrada
20 20 20 20 20 20 20
```
```salida
lun: 20
mar: 20
mié: 20
jue: 20
vie: 20
sáb: 20
dom: 20
Máxima 20, mínima 20, promedio 20
```

##### Bajo cero
```entrada
-5 -2 0 3 -8 1 -1
```
```salida
lun: -5
mar: -2
mié: 0
jue: 3
vie: -8
sáb: 1
dom: -1
Máxima 3, mínima -8, promedio -1.71429
```

### Misión R03-N01-M2 · El ta-te-ti del patio

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá el tablero como `using Tablero = std::array<std::array<char, 3>, 3>;` lleno
de `.`. Cada línea de la entrada es una jugada `fila columna`, alternando X y O
(empieza X). Una jugada fuera del tablero o en una casilla ocupada se anuncia y se
ignora. El juego termina cuando alguien gana, se llena el tablero o se acaba la
entrada. Mostrá el tablero y el resultado.

#### Criterio de aprobación

- Usa `std::array` anidado y `fill`.
- `ganador` revisa filas, columnas y diagonales.
- Recorre el tablero con `for` de rango (`const auto&`).

#### Entrada de ejemplo

```
1 1
0 0
1 1
2 2
0 2
2 0
1 0
1 2
2 1
0 1
```

#### Salida esperada

```
Jugada inválida: 1 1
OXO
OXX
XOX
Empate
```

#### Solución de referencia

```cpp
// Mision 2 - El tablero de ta-te-ti: un array de arrays y quien gano.
#include <array>
#include <iostream>

using Tablero = std::array<std::array<char, 3>, 3>;

char ganador(const Tablero& t)
{
    for (int i = 0; i < 3; i++) {
        if (t[i][0] != '.' && t[i][0] == t[i][1] && t[i][1] == t[i][2]) {
            return t[i][0];
        }
        if (t[0][i] != '.' && t[0][i] == t[1][i] && t[1][i] == t[2][i]) {
            return t[0][i];
        }
    }
    if (t[1][1] != '.' && ((t[0][0] == t[1][1] && t[1][1] == t[2][2]) || (t[0][2] == t[1][1] && t[1][1] == t[2][0]))) {
        return t[1][1];
    }
    return '.';
}

void mostrar(const Tablero& t)
{
    for (const auto& fila : t) {
        for (auto c : fila) {
            std::cout << c;
        }
        std::cout << "\n";
    }
}

int main()
{
    Tablero t;
    for (auto& fila : t) {
        fila.fill('.');
    }
    char turno = 'X';
    int f = 0, c = 0, jugadas = 0;
    while (ganador(t) == '.' && jugadas < 9 && std::cin >> f >> c) {
        if (f < 0 || f > 2 || c < 0 || c > 2 || t[f][c] != '.') {
            std::cout << "Jugada inválida: " << f << " " << c << "\n";
            continue;
        }
        t[f][c] = turno;
        jugadas++;
        turno = (turno == 'X') ? 'O' : 'X';
    }
    mostrar(t);
    char g = ganador(t);
    if (g != '.') {
        std::cout << "Gana " << g << "\n";
    } else {
        std::cout << (jugadas == 9 ? "Empate" : "Partida sin terminar") << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Gana X en diagonal
```entrada
0 0
0 1
1 1
0 2
2 2
```
```salida
XOO
.X.
..X
Gana X
```

##### Gana O en una columna
```entrada
0 0
0 2
1 1
1 2
2 1
2 2
```
```salida
X.O
.XO
.XO
Gana O
```

##### Jugadas fuera del tablero
```entrada
3 3
-1 0
0 0
```
```salida
Jugada inválida: 3 3
Jugada inválida: -1 0
X..
...
...
Partida sin terminar
```

##### Sin jugadas
```entrada
```
```salida
...
...
...
Partida sin terminar
```

### Misión R03-N01-M3 · Copia o referencia

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con un vector de engranajes (`nombre`, `dientes`): chico 12, mediano 24, grande 48.
1. Recorrelo con `for (auto e : caja)` restando 2 dientes, y mostrá los dientes.
2. Repetí con `for (auto& e : caja)`, y mostrá los dientes.
3. Hacé `auto primero = caja[0];` y `auto& ultimo = caja.back();`, cambiales el
   nombre a "COPIA" y "GIGANTE", y mostrá todo con structured bindings.

**Antes de ejecutar**, anotá qué esperás en cada paso.

#### Criterio de aprobación

- Los tres pasos muestran la diferencia entre copia y referencia.
- El último recorrido usa `const auto& [nombre, dientes]`.

#### Salida esperada

```
Tras 'auto': 12 24 48
Tras 'auto&': 10 22 46
chico(10) mediano(22) GIGANTE(46) 
```

#### Solución de referencia

```cpp
// Mision 3 - auto con cuidado: copia o referencia.
#include <iostream>
#include <string>
#include <vector>

struct Engranaje {
    std::string nombre;
    int dientes = 0;
};

int main()
{
    std::vector<Engranaje> caja = {{"chico", 12}, {"mediano", 24}, {"grande", 48}};

    for (auto e : caja) {            // copia: se lima la copia
        e.dientes -= 2;
    }
    std::cout << "Tras 'auto':";
    for (const auto& e : caja) {
        std::cout << " " << e.dientes;
    }
    std::cout << "\n";

    for (auto& e : caja) {           // referencia: se lima el original
        e.dientes -= 2;
    }
    std::cout << "Tras 'auto&':";
    for (const auto& e : caja) {
        std::cout << " " << e.dientes;
    }
    std::cout << "\n";

    auto primero = caja[0];          // copia
    auto& ultimo = caja.back();      // referencia
    primero.nombre = "COPIA";
    ultimo.nombre = "GIGANTE";
    for (const auto& [nombre, dientes] : caja) {
        std::cout << nombre << "(" << dientes << ") ";
    }
    std::cout << "\n";
    return 0;
}
```

### Encargo R03-N01-E1 · La boleta de luz

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La cooperativa eléctrica cobra por tramos: los primeros 150 kWh a $80, de 151 a 400
a $110, y el resto a $160. Leé los consumos de los 6 bimestres del año en un
`std::array<int, 6>`, mostrá el costo de cada bimestre y el total anual, con 2
decimales. Los topes y los precios van en `std::array` constantes.

#### Criterio de aprobación

- El cálculo por tramos está en una función.
- Los topes y los precios son `const std::array`.

#### Entrada de ejemplo

```
120 380 520 150 0 410
```

#### Salida esperada

```
Bimestre 1: 120 kWh -> $9600.00
Bimestre 2: 380 kWh -> $37300.00
Bimestre 3: 520 kWh -> $58700.00
Bimestre 4: 150 kWh -> $12000.00
Bimestre 5: 0 kWh -> $0.00
Bimestre 6: 410 kWh -> $41100.00
Total anual: $158700.00
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La boleta de luz: consumo por bimestre en un array y tarifa escalonada.
#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>

double costo(int kwh)
{
    // primeros 150 kWh a $80; de 151 a 400 a $110; el resto a $160
    const std::array<int, 2> TOPES = {150, 400};
    const std::array<double, 3> PRECIOS = {80, 110, 160};
    double total = 0;
    int anterior = 0;
    for (std::size_t i = 0; i < TOPES.size(); i++) {
        if (kwh > anterior) {
            int tramo = std::min(kwh, TOPES[i]) - anterior;
            total += tramo * PRECIOS[i];
        }
        anterior = TOPES[i];
    }
    if (kwh > anterior) {
        total += (kwh - anterior) * PRECIOS[2];
    }
    return total;
}

int main()
{
    std::array<int, 6> bimestres{};
    for (auto& b : bimestres) {
        std::cin >> b;
    }
    std::cout << std::fixed << std::setprecision(2);
    double anual = 0;
    for (std::size_t i = 0; i < bimestres.size(); i++) {
        double c = costo(bimestres[i]);
        anual += c;
        std::cout << "Bimestre " << i + 1 << ": " << bimestres[i] << " kWh -> $" << c << "\n";
    }
    std::cout << "Total anual: $" << anual << "\n";
    return 0;
}
```

#### Pruebas

##### Bordes de los tramos
```entrada
150 151 400 401 0 1
```
```salida
Bimestre 1: 150 kWh -> $12000.00
Bimestre 2: 151 kWh -> $12110.00
Bimestre 3: 400 kWh -> $39500.00
Bimestre 4: 401 kWh -> $39660.00
Bimestre 5: 0 kWh -> $0.00
Bimestre 6: 1 kWh -> $80.00
Total anual: $103350.00
```

##### Consumo alto todo el año
```entrada
1000 1000 1000 1000 1000 1000
```
```salida
Bimestre 1: 1000 kWh -> $135500.00
Bimestre 2: 1000 kWh -> $135500.00
Bimestre 3: 1000 kWh -> $135500.00
Bimestre 4: 1000 kWh -> $135500.00
Bimestre 5: 1000 kWh -> $135500.00
Bimestre 6: 1000 kWh -> $135500.00
Total anual: $813000.00
```

### Prueba del sello

#### ¿Qué tipo tiene `auto x = 3.0;`? ¿Puede cambiar después?

`double`, y no puede cambiar: se deduce al compilar.

#### ¿Qué diferencia hay entre `for (auto x : v)`, `for (const auto& x : v)` y `for (auto& x : v)`?

El primero copia cada elemento; el segundo lee el original sin copiar; el tercero permite modificarlo.

#### ¿Qué hace `auto [a, b] = par;`?

Separa el par (o struct) en dos variables con nombre, en el orden de sus campos.

#### ¿Cuándo usás `std::array` y cuándo `std::vector`?

`array` cuando el tamaño es fijo y se conoce al compilar; `vector` cuando cambia.

#### ¿Por qué `std::accumulate(v.begin(), v.end(), 0)` puede fallar con `double`?

Porque el acumulador toma el tipo del valor inicial (`int`) y trunca; hay que usar `0.0`.

### Soluciones (docente)

Material original: `04-C++-Moderno/01-Auto-RangeFor` y `02-Vector-Array` (con lo de `09-ConstRef-Nullptr` sobre cómo recibir parámetros, que ya se vio en la rama 1).

## R03-N02 · Textos a fondo

```meta
tipo: tema
padre: R03-N01
precio: 10
criatura: orco
temas: prog.cadenas
```

### Crónica

En la oficina de la Aduana de la Ciudadela, un escriba recibe planillas escritas de cualquier manera: "Kira;27;artífice", "bron ; 120 ;guerrero", nombres con espacios de más, extensiones raras.

—El mundo te va a dar texto sucio —dice {mentor}—. Antes de hacer nada con él, hay que **buscarlo, cortarlo y limpiarlo**. Y un número escrito como texto todavía no es un número.

### Objetivos

Trabajar con `std::string` a fondo: buscar (`find`, `rfind`), cortar (`substr`),
reemplazar, insertar y borrar; convertir entre números y texto (`std::stoi`,
`std::stod`, `std::to_string`); y partir y armar textos con `std::istringstream`
y `std::ostringstream`.

### Antes de empezar

- `std::string`, `getline` y lectura con `>>` (rama 1).
- `auto` y el `for` de rango (nodo anterior).

### Explicación

#### Buscar
```cpp
std::size_t pos = texto.find("Ciudadela");      // dónde empieza
if (pos == std::string::npos) { /* no está */ }
texto.find('x', desde);                          // buscar a partir de una posición
texto.rfind('.');                                // la ÚLTIMA aparición
texto.find_first_not_of(' ');                    // el primer carácter que no es espacio
```
`std::string::npos` es un valor especial (el número más grande posible) que
significa "no encontrado". **Siempre** compará con `npos` antes de usar la
posición.

C++20 agrega `texto.starts_with("x")`, `texto.ends_with(".png")` y
`texto.contains("x")` (C++23).

#### Cortar y modificar
| Operación | Qué hace |
|---|---|
| `s.substr(desde, cantidad)` | un pedazo nuevo (sin `cantidad`: hasta el final) |
| `s.replace(desde, cantidad, otro)` | reemplaza ese pedazo |
| `s.insert(desde, otro)` | inserta |
| `s.erase(desde, cantidad)` | borra |
| `s += otro` / `s + otro` | agrega / une |

#### Números y texto
```cpp
int n = std::stoi("42");          // texto -> int
double p = std::stod("1250.75");  // texto -> double
std::string t = std::to_string(7);
```
`std::stoi` de algo que no empieza con un número (`"hola"`) no devuelve 0: **lanza
una excepción** y, si nadie la atrapa, el programa se corta (vas a aprender a
atraparlas en la rama 5). Además, `std::stoi("12abc")` da 12 y se calla el resto.
Por eso conviene **validar antes** de convertir.

#### `std::istringstream`: leer desde un texto
Un `istringstream` (de `<sstream>`) es como `std::cin`, pero lee de un texto:
```cpp
std::istringstream entrada("Bron 120 guerrero");
entrada >> quien >> vida >> clase;
```
Y con `std::getline` y un **separador** parte un texto en campos:
```cpp
std::istringstream csv("engranaje;350;12");
std::string campo;
while (std::getline(csv, campo, ';')) { /* un campo por vuelta */ }
```
Es la forma estándar de leer formatos como CSV (campos separados por comas o
punto y coma).

#### `std::ostringstream`: armar un texto
```cpp
std::ostringstream armado;
armado << "Torre " << 7 << " de " << 12;
std::string resultado = armado.str();
```
Todo lo que sabe hacer `cout` (incluido `setw` y `setprecision`), pero guardado en
un texto.

#### Caracteres: `<cctype>`
`std::isdigit(c)`, `std::isalpha(c)`, `std::isspace(c)`, `std::toupper(c)`,
`std::tolower(c)`. Pasales el carácter como `static_cast<unsigned char>(c)`: con
letras acentuadas, un `char` puede ser negativo y eso es comportamiento indefinido.
(Solo funcionan bien con letras sin tilde.)

> **Si venís de C.** `find` reemplaza a `strstr`/`strchr`, `substr` a copiar a
> mano, `==` a `strcmp`, `std::stoi`/`std::to_string` a `atoi`/`sprintf`, y los
> `stringstream` a `sscanf`/`sprintf`. Todo sin tamaños fijos ni `free`.

### Código de ejemplo

```cpp
/*
 * std::string a fondo: buscar, cortar, reemplazar, convertir y partir con stringstream.
 */
#include <iostream>
#include <sstream>   // std::istringstream, std::ostringstream
#include <string>
#include <vector>

int main()
{
    std::string completo = "Kira de la Ciudadela";
    completo += "!";
    std::cout << completo << " (" << completo.size() << " caracteres)\n";

    // find: la posicion donde empieza, o std::string::npos si no esta
    std::size_t pos = completo.find("Ciudadela");
    if (pos != std::string::npos) {
        std::cout << "\"Ciudadela\" empieza en " << pos << "\n";
    }
    if (completo.find("Forjas") == std::string::npos) {
        std::cout << "No dice \"Forjas\"\n";
    }

    // substr(desde, cantidad)
    std::cout << "Primeras 4 letras: " << completo.substr(0, 4) << "\n";

    // rfind busca desde el final: separar la extension de un archivo
    std::string archivo = "planos/torre.norte.png";
    std::size_t punto = archivo.rfind('.');
    std::cout << "Nombre: " << archivo.substr(0, punto) << ", extensión: " << archivo.substr(punto + 1) << "\n";

    // replace, insert, erase
    std::string frase = "el plano viejo";
    frase.replace(frase.find("viejo"), 5, "nuevo");
    frase.insert(0, "¡");
    frase += "!";
    std::cout << frase << "\n";

    // C++20: starts_with / ends_with
    std::cout << std::boolalpha << "¿Termina en .png? " << archivo.ends_with(".png") << "\n";

    // Numeros <-> texto
    int nivel = std::stoi("42");
    double precio = std::stod("1250.75");
    std::string etiqueta = "nivel " + std::to_string(nivel + 1);
    std::cout << etiqueta << ", precio con IVA: " << precio * 1.21 << "\n";

    // istringstream: leer DESDE un texto como si fuera cin
    std::istringstream entrada("Bron 120 guerrero");
    std::string quien, clase;
    int vida = 0;
    entrada >> quien >> vida >> clase;
    std::cout << quien << " es " << clase << " con " << vida << " de vida\n";

    // getline con separador: partir "a;b;c"
    std::istringstream csv("engranaje;350;12");
    std::vector<std::string> campos;
    std::string campo;
    while (std::getline(csv, campo, ';')) {
        campos.push_back(campo);
    }
    std::cout << "Campos: " << campos.size() << " -> " << campos[0] << " | " << campos[1] << " | " << campos[2] << "\n";

    // ostringstream: armar un texto con << y sacarlo con .str()
    std::ostringstream armado;
    armado << "Torre " << 7 << " de " << 12;
    std::cout << "[" << armado.str() << "]\n";
    return 0;
}
```

### Salida esperada

```
Kira de la Ciudadela! (21 caracteres)
"Ciudadela" empieza en 11
No dice "Forjas"
Primeras 4 letras: Kira
Nombre: planos/torre.norte, extensión: png
¡el plano nuevo!
¿Termina en .png? true
nivel 43, precio con IVA: 1513.41
Bron es guerrero con 120 de vida
Campos: 3 -> engranaje | 350 | 12
[Torre 7 de 12]
```

### ¿Para qué sirve?

Casi todo lo que entra a un programa es texto: formularios, archivos CSV exportados de Excel, líneas de un log, comandos de un chat, rutas de archivos, respuestas de una API. Saber partir, validar y convertir texto es el primer paso para importar datos, procesar planillas, leer archivos de configuración o interpretar los comandos de un juego de texto.

### Errores habituales

**Orco: usar la posición de un `find` que no encontró nada.** `s.substr(s.find('.'))`
cuando no hay punto: `find` devuelve `npos` y `substr` se corta:
```
terminate called after throwing an instance of 'std::out_of_range'
  what():  basic_string::substr: __pos (which is 18446744073709551615) > this->size() (which is 5)
```
Ese número gigante **es** `npos`. Compará antes.

**Goblin: `std::stoi` de un texto que no es número.**
```
terminate called after throwing an instance of 'std::invalid_argument'
  what():  stoi
```

**Ogro: `std::stoi("12abc")` da 12 en silencio.** Si necesitás que **todo** el
texto sea un número, validalo carácter por carácter (o mirá cuántos caracteres usó,
con el segundo parámetro de `stoi`).

**Ogro: el bucle de reemplazo infinito.** Reemplazar "a" por "aa" buscando otra vez
desde el principio encuentra siempre la "a" recién puesta. Seguí buscando
**después** de lo que pusiste.

**Goblin: `toupper` con acentos.** `std::toupper('é')` no la cambia (y sin el
`unsigned char` puede ser indefinido). Para texto en español con tildes hacen falta
bibliotecas de Unicode.

### Misión R03-N02-M1 · Las rutas del archivo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea de la entrada es una ruta de archivo (se ignoran las vacías). Mostrá la
carpeta (o `.` si no tiene), el nombre sin extensión y la extensión (o
`(ninguna)`). Un archivo que empieza con punto, como `.config`, no tiene extensión.

#### Criterio de aprobación

- Usa `rfind` para la última `/` y el último `.`.
- Compara con `std::string::npos` antes de usar las posiciones.
- Contempla archivos sin carpeta, sin extensión y ocultos.

#### Entrada de ejemplo

```
planos/torre.norte.png
leeme
/home/kira/.config
informe.pdf
```

#### Salida esperada

```
planos/torre.norte.png
  carpeta: planos
  nombre: torre.norte
  extensión: png
leeme
  carpeta: .
  nombre: leeme
  extensión: (ninguna)
/home/kira/.config
  carpeta: /home/kira
  nombre: .config
  extensión: (ninguna)
informe.pdf
  carpeta: .
  nombre: informe
  extensión: pdf
```

#### Solución de referencia

```cpp
// Mision 2.1 - Rutas de archivos: carpeta, nombre y extension.
#include <iostream>
#include <string>

void partes(const std::string& ruta)
{
    std::size_t barra = ruta.rfind('/');
    std::string carpeta = (barra == std::string::npos) ? "." : ruta.substr(0, barra);
    std::string archivo = (barra == std::string::npos) ? ruta : ruta.substr(barra + 1);
    std::size_t punto = archivo.rfind('.');
    std::string nombre = archivo;
    std::string extension = "(ninguna)";
    if (punto != std::string::npos && punto != 0) {
        nombre = archivo.substr(0, punto);
        extension = archivo.substr(punto + 1);
    }
    std::cout << ruta << "\n  carpeta: " << carpeta << "\n  nombre: " << nombre << "\n  extensión: " << extension << "\n";
}

int main()
{
    std::string ruta;
    while (std::getline(std::cin, ruta)) {
        if (!ruta.empty()) {
            partes(ruta);
        }
    }
    return 0;
}
```

#### Pruebas

##### Rutas raras
```entrada
a/b/c/
archivo.
.oculto.txt
carpeta/.gitignore
```
```salida
a/b/c/
  carpeta: a/b/c
  nombre:
  extensión: (ninguna)
archivo.
  carpeta: .
  nombre: archivo
  extensión:
.oculto.txt
  carpeta: .
  nombre: .oculto
  extensión: txt
carpeta/.gitignore
  carpeta: carpeta
  nombre: .gitignore
  extensión: (ninguna)
```

##### Líneas vacías en el medio
```entrada
uno.txt

dos/tres.tar.gz
```
```salida
uno.txt
  carpeta: .
  nombre: uno
  extensión: txt
dos/tres.tar.gz
  carpeta: dos
  nombre: tres.tar
  extensión: gz
```

### Misión R03-N02-M2 · El censor de la Ciudadela

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La primera línea es una palabra a buscar y la segunda, con qué reemplazarla. Las
siguientes son el texto. Escribí `int reemplazar_todo(std::string& texto, const
std::string& buscar, const std::string& poner)`, que reemplaza **todas** las
apariciones y devuelve cuántas cambió. Mostrá cada línea reemplazada y el total.
Tiene que funcionar aunque `poner` contenga a `buscar` (por ejemplo, "gris" por
"grisáceo").

#### Criterio de aprobación

- Recibe el texto por referencia.
- Sigue buscando después de lo reemplazado (no queda en un bucle infinito).

#### Entrada de ejemplo

```
gris
grisáceo
la torre gris y el puente gris
nada que cambiar
grisgris
```

#### Salida esperada

```
la torre grisáceo y el puente grisáceo
nada que cambiar
grisáceogrisáceo
(4 reemplazos)
```

#### Solución de referencia

```cpp
// Mision 2 - El censor de la Ciudadela: reemplazar todas las apariciones de una palabra.
#include <iostream>
#include <string>

int reemplazar_todo(std::string& texto, const std::string& buscar, const std::string& poner)
{
    if (buscar.empty()) {
        return 0;
    }
    int cambios = 0;
    std::size_t pos = texto.find(buscar);
    while (pos != std::string::npos) {
        texto.replace(pos, buscar.size(), poner);
        cambios++;
        pos = texto.find(buscar, pos + poner.size());   // seguir DESPUES de lo puesto
    }
    return cambios;
}

int main()
{
    std::string buscar, poner, linea;
    std::getline(std::cin, buscar);
    std::getline(std::cin, poner);
    int total = 0;
    while (std::getline(std::cin, linea)) {
        total += reemplazar_todo(linea, buscar, poner);
        std::cout << linea << "\n";
    }
    std::cout << "(" << total << " reemplazos)\n";
    return 0;
}
```

#### Pruebas

##### Sin apariciones
```entrada
hierro
acero
la torre gris
el puente azul
```
```salida
la torre gris
el puente azul
(0 reemplazos)
```

##### Reemplazar por nada
```entrada
xx

axxbxxc
xxxx
```
```salida
abc

(4 reemplazos)
```

### Misión R03-N02-M3 · El registro de la aduana

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea trae `nombre;edad;oficio`. Escribí `partir(linea, separador)`, que
devuelve un vector de campos (con `std::istringstream` y `std::getline`), y
`es_numero(texto)`. Una línea es válida si tiene 3 campos, nombre no vacío y la edad
es un número. Mostrá las válidas y avisá cuáles no lo son. Al final, cuántos
registros válidos hay y la edad promedio.

#### Criterio de aprobación

- Parte las líneas con `std::getline(in, campo, ';')`.
- Valida antes de llamar a `std::stoi`.

#### Entrada de ejemplo

```
Kira;27;artífice
Bron;120;guerrero
;30;nadie
Lyn;veinte;arquera
Oto;64;relojero
solo;dos
```

#### Salida esperada

```
Kira (27), artífice
Bron (120), guerrero
Línea 3 inválida: ;30;nadie
Línea 4 inválida: Lyn;veinte;arquera
Oto (64), relojero
Línea 6 inválida: solo;dos
3 registros, edad promedio 70.3333
```

#### Solución de referencia

```cpp
// Mision 3 - El registro de la aduana: partir lineas "nombre;edad;oficio" y validar.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> partir(const std::string& linea, char sep)
{
    std::vector<std::string> campos;
    std::istringstream in(linea);
    std::string campo;
    while (std::getline(in, campo, sep)) {
        campos.push_back(campo);
    }
    return campos;
}

bool es_numero(const std::string& s)
{
    if (s.empty()) {
        return false;
    }
    for (char c : s) {
        if (c < '0' || c > '9') {
            return false;
        }
    }
    return true;
}

int main()
{
    std::string linea;
    int n = 0, validos = 0, suma_edades = 0;
    while (std::getline(std::cin, linea)) {
        n++;
        std::vector<std::string> c = partir(linea, ';');
        if (c.size() != 3 || c[0].empty() || !es_numero(c[1])) {
            std::cout << "Línea " << n << " inválida: " << linea << "\n";
            continue;
        }
        int edad = std::stoi(c[1]);
        validos++;
        suma_edades += edad;
        std::cout << c[0] << " (" << edad << "), " << c[2] << "\n";
    }
    if (validos > 0) {
        std::cout << validos << " registros, edad promedio " << static_cast<double>(suma_edades) / validos << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Todas inválidas
```entrada
a;b;c
;;
Lyn;;arquera
```
```salida
Línea 1 inválida: a;b;c
Línea 2 inválida: ;;
Línea 3 inválida: Lyn;;arquera
```

##### Una sola válida
```entrada
Kira;27;artífice
```
```salida
Kira (27), artífice
1 registros, edad promedio 27
```

##### Edad con signo
```entrada
Bron;-5;guerrero
Oto;+64;relojero
```
```salida
Línea 1 inválida: Bron;-5;guerrero
Línea 2 inválida: Oto;+64;relojero
```

### Encargo R03-N02-E1 · El validador de CUIT

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un CUIT tiene 11 dígitos (puede venir con guiones o espacios). El último es un
**dígito verificador**: se multiplican los 10 primeros por 5, 4, 3, 2, 7, 6, 5, 4,
3, 2, se suman, y el verificador es `11 − (suma % 11)`; si da 11 es 0, y si da 10 es
9. Cada línea de la entrada es un CUIT: si es válido, mostralo formateado como
`XX-XXXXXXXX-X`; si no, avisá.

#### Criterio de aprobación

- Limpia guiones y espacios, y rechaza otros caracteres.
- Calcula el verificador con los pesos.
- Formatea con `substr`.

#### Entrada de ejemplo

```
20-12345678-6
27 23456789 1
30123456789
20-1234567-8
20-12345678-5
```

#### Salida esperada

```
20-12345678-6: válido
27-23456789-1: válido
30123456789: inválido
20-1234567-8: inválido
20-12345678-5: inválido
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El validador de CUIT: 11 digitos con guiones y digito verificador.
#include <iostream>
#include <string>

std::string solo_digitos(const std::string& s)
{
    std::string r;
    for (char c : s) {
        if (c >= '0' && c <= '9') {
            r += c;
        } else if (c != '-' && c != ' ') {
            return "";                 // un caracter raro: invalido
        }
    }
    return r;
}

bool cuit_valido(const std::string& texto)
{
    std::string d = solo_digitos(texto);
    if (d.size() != 11) {
        return false;
    }
    const int PESOS[10] = {5, 4, 3, 2, 7, 6, 5, 4, 3, 2};
    int suma = 0;
    for (int i = 0; i < 10; i++) {
        suma += (d[i] - '0') * PESOS[i];
    }
    int verificador = 11 - suma % 11;
    if (verificador == 11) {
        verificador = 0;
    } else if (verificador == 10) {
        verificador = 9;
    }
    return verificador == d[10] - '0';
}

std::string formatear(const std::string& texto)
{
    std::string d = solo_digitos(texto);
    return d.substr(0, 2) + "-" + d.substr(2, 8) + "-" + d.substr(10);
}

int main()
{
    std::string linea;
    while (std::getline(std::cin, linea)) {
        if (cuit_valido(linea)) {
            std::cout << formatear(linea) << ": válido\n";
        } else {
            std::cout << linea << ": inválido\n";
        }
    }
    return 0;
}
```

#### Pruebas

##### Verificador 0 y 9
```entrada
20-00000000-1
23-45678901-9
```
```salida
20-00000000-1: válido
23-45678901-9: inválido
```

##### Cantidad de dígitos equivocada
```entrada
123
20-12345678-66
```
```salida
123: inválido
20-12345678-66: inválido
```

##### Con letras
```entrada
20-1234567A-6
```
```salida
20-1234567A-6: inválido
```

### Prueba del sello

#### ¿Qué devuelve `find` si no encuentra lo que busca?

`std::string::npos`.

#### ¿Qué hacen `substr(3)` y `substr(3, 2)`?

La primera devuelve desde la posición 3 hasta el final; la segunda, 2 caracteres desde la posición 3.

#### ¿Qué pasa con `std::stoi("hola")`?

Lanza una excepción (`std::invalid_argument`) y, si nadie la atrapa, el programa se corta.

#### ¿Cómo partís `"a;b;c"` en tres campos?

Con un `std::istringstream` y `std::getline(in, campo, ';')` en un bucle.

#### ¿Para qué sirve `std::ostringstream`?

Para armar un texto con `<<` (como `cout`) y obtenerlo con `.str()`.

### Soluciones (docente)

Material original: `04-C++-Moderno/03-String`, ampliado con `stringstream` (lo usa el Bestiario del jefe) y validación antes de `stoi`. Las excepciones se nombran pero se enseñan en la rama 5.

El CUIT de ejemplo 20-12345678-6 cumple el algoritmo (verificado).

## R03-N03 · Diccionarios y conjuntos

```meta
tipo: tema
padre: R03-N02
precio: 10
criatura: orco
temas: col.mapas, col.conjuntos
```

### Crónica

El archivista de la Ciudadela no busca los planos hoja por hoja. Tiene un fichero: buscás "reloj" y la ficha te dice "cajón 14". Y tiene otro libro, más fino, con solo una lista de nombres: los artífices que ya rindieron el examen. Nadie aparece dos veces.

—El fichero es un **mapa**: de una clave, a su valor —explica {mentor}—. El libro es un **conjunto**: solo sabe si algo está o no está. Con esos dos, casi cualquier problema de "buscar" se vuelve instantáneo.

### Objetivos

Guardar pares clave → valor con `std::map` y `std::unordered_map`, consultar sin
crear entradas por accidente, contar apariciones, y guardar colecciones sin
repetidos con `std::set`. Saber cuándo conviene cada uno.

### Antes de empezar

- Structured bindings (auto, array y el for de rango).
- Textos (nodo anterior).

### Explicación

#### `std::map<Clave, Valor>`
Un diccionario: a cada **clave** (única) le corresponde un **valor**.
```cpp
std::map<std::string, int> inventario;
inventario["poción"] = 3;       // crear o reemplazar
inventario["poción"] += 2;      // modificar
inventario.size();              // cuántas claves
inventario.erase("poción");     // borrar
```
Recorrerlo da **pares** (`first` es la clave, `second` el valor), en orden de
clave:
```cpp
for (const auto& [item, cantidad] : inventario) { ... }
```

#### La trampa de `[]`
`m[clave]` **crea** la clave (con valor 0, `""` o el que corresponda) si no
existía. Eso es comodísimo para contar (`veces[palabra]++`), pero peligroso para
consultar: `if (m["escudo"] == 0)` **agrega** un escudo con 0. Para consultar sin
crear:
| Forma | Da |
|---|---|
| `m.contains(k)` (C++20) | `true`/`false` |
| `m.count(k)` | 0 o 1 |
| `m.find(k)` | un iterador al par, o `m.end()`; el valor es `it->second` |
| `m.at(k)` | el valor; si no existe, el programa se corta con un error |

Además, `[]` no se puede usar sobre un `const std::map&` (porque podría modificarlo):
en funciones que solo leen, usá `find` o `at`.

#### `std::unordered_map`
La misma interfaz, pero **sin orden** (por dentro es una tabla *hash*). En general
es más rápido. Regla:
- necesitás recorrer en orden de clave → `std::map`;
- solo buscar, agregar y borrar → `std::unordered_map`.

#### `std::set<T>`: está o no está
Un conjunto **sin repetidos** y ordenado:
```cpp
std::set<std::string> visitados;
visitados.insert("celda");
visitados.insert("celda");        // ya estaba: no pasa nada
visitados.contains("celda");      // true
visitados.erase("celda");
```
Sirve para "¿ya vi esto?": casillas visitadas, logros desbloqueados, palabras
únicas. Si necesitás **cuántas veces**, eso es un `map<T, int>`. Existe también
`std::unordered_set` (sin orden, más rápido).

#### ¿Por qué no un vector y buscar?
Buscar en un vector es recorrerlo entero: con un millón de elementos, un millón de
comparaciones. En un `map` o `set` son unas 20 (van partiendo por la mitad); en un
`unordered_map`, casi siempre una. Para datos grandes, la diferencia es enorme.

#### Ordenar un map por valor
Un `map` siempre está ordenado por **clave**. Para ordenarlo por valor (un ranking),
se copia a un vector de pares y se ordena ese vector:
```cpp
std::vector<std::pair<std::string, double>> ranking(m.begin(), m.end());
std::sort(ranking.begin(), ranking.end(), [](const auto& a, const auto& b) { return a.second > b.second; });
```
(Esa función entre corchetes es una **lambda**: la vas a ver en detalle en unos
nodos. Por ahora: "ordená poniendo primero al de mayor `second`".)

> **Si venís de C.** C no trae nada de esto: había que escribir una tabla hash o
> un árbol a mano. En C++ son una línea.

### Código de ejemplo

```cpp
/*
 * std::map, std::unordered_map y std::set: diccionarios y conjuntos.
 */
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_map>

int main()
{
    // map: clave -> valor, ORDENADO por clave
    std::map<std::string, int> inventario;
    inventario["poción"] = 3;
    inventario["flecha"] = 40;
    inventario["llave"] = 1;
    inventario["poción"] += 2;          // modificar
    inventario["oro"] += 100;           // "oro" no existia: [] lo CREA con 0 y le suma

    std::cout << "Inventario (ordenado por nombre):\n";
    for (const auto& [item, cantidad] : inventario) {
        std::cout << "  " << item << " x" << cantidad << "\n";
    }

    // Consultar SIN crear: contains (C++20), count o find
    if (!inventario.contains("escudo")) {
        std::cout << "No hay escudo.\n";
    }
    auto it = inventario.find("flecha");
    if (it != inventario.end()) {
        std::cout << "Flechas: " << it->second << "\n";      // it->first es la clave
    }
    inventario.erase("llave");
    std::cout << "Tras usar la llave quedan " << inventario.size() << " tipos de ítem.\n";

    // unordered_map: la misma idea, SIN orden (tabla hash), mas rapido en general
    std::unordered_map<std::string, int> dano_por_arma = {{"espada", 18}, {"arco", 12}, {"hacha", 24}};
    std::cout << "Daño del hacha: " << dano_por_arma.at("hacha") << "\n";   // at: error si no existe

    // Contar apariciones: el uso clasico de map<algo, int>
    std::string texto = "engranaje";
    std::map<char, int> letras;
    for (char c : texto) {
        letras[c]++;
    }
    std::cout << "Letras de \"" << texto << "\":";
    for (const auto& [letra, veces] : letras) {
        std::cout << " " << letra << "=" << veces;
    }
    std::cout << "\n";

    // set: un conjunto SIN repetidos, ordenado
    std::set<std::string> puertas_abiertas;
    puertas_abiertas.insert("celda");
    puertas_abiertas.insert("armería");
    puertas_abiertas.insert("celda");   // repetido: se ignora
    puertas_abiertas.insert("torre");
    std::cout << "Puertas abiertas (" << puertas_abiertas.size() << "):";
    for (const auto& p : puertas_abiertas) {
        std::cout << " " << p;
    }
    std::cout << "\n";
    std::cout << "¿Está abierta la armería? " << (puertas_abiertas.contains("armería") ? "sí" : "no") << "\n";

    std::set<int> ids = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5};
    std::cout << "Ids únicos y ordenados:";
    for (int x : ids) {
        std::cout << " " << x;
    }
    std::cout << "\n";
    return 0;
}
```

### Salida esperada

```
Inventario (ordenado por nombre):
  flecha x40
  llave x1
  oro x100
  poción x5
No hay escudo.
Flechas: 40
Tras usar la llave quedan 3 tipos de ítem.
Daño del hacha: 24
Letras de "engranaje": a=2 e=2 g=1 j=1 n=2 r=1
Puertas abiertas (3): armería celda torre
¿Está abierta la armería? sí
Ids únicos y ordenados: 1 2 3 4 5 6 9
```

### ¿Para qué sirve?

Los diccionarios están en todas partes: el stock por código de producto, el precio por artículo, las notas por alumno, los usuarios por nombre, las traducciones por clave, los comandos de un juego de texto. Contar apariciones (palabras de un texto, ventas por vendedor, votos por candidato) es un `map<clave, int>`. Los conjuntos sirven para evitar duplicados: correos únicos de una lista, casillas visitadas por un algoritmo de búsqueda, permisos de un usuario.

### Errores habituales

**Ogro: consultar con `[]` y crear sin querer.** `if (m["x"] == 0)` agrega `"x"`. Después,
`m.size()` no da lo que esperabas. Consultá con `contains` o `find`.

**Goblin: `[]` sobre un map `const`.**
```
main.cpp:3:59: error: passing ‘const std::map<std::__cxx11::basic_string<char>, int>’ as ‘this’ argument discards qualifiers [-fpermissive]
```
El mensaje sigue con varias líneas de detalle del map; lo importante es la
primera. Usá `find` o `at`.

**Orco: `at` de una clave que no existe.**
```
terminate called after throwing an instance of 'std::out_of_range'
  what():  map::at
```

**Ogro: esperar orden en un `unordered_map`.** Recorrerlo da un orden que depende
de la implementación y puede cambiar. Si el orden importa, `map`.

**Ogro: usar `set` para contar.** Un `set` solo sabe si algo está: insertar tres
veces lo mismo deja uno. Para contar, `map<T, int>`.

### Misión R03-N03-M1 · Las palabras del manual

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé palabras hasta el final de la entrada. Limpialas (solo letras, en minúscula) y
contá cuántas veces aparece cada una con un `std::map<std::string, int>`. Mostrá
cada palabra con su cuenta (en orden alfabético), el total de palabras, cuántas
distintas hay y la más común (si hay empate, la primera en orden alfabético).

#### Criterio de aprobación

- Cuenta con `veces[palabra]++`.
- Descarta lo que queda vacío al limpiar.
- Recorre el map con structured bindings.

#### Entrada de ejemplo

```
El engranaje gira. El resorte empuja al engranaje,
y el engranaje, al fin, mueve la torre! 42
```

#### Salida esperada

```
al: 2
el: 3
empuja: 1
engranaje: 3
fin: 1
gira: 1
la: 1
mueve: 1
resorte: 1
torre: 1
y: 1
16 palabras, 11 distintas; la más común: el
```

#### Solución de referencia

```cpp
// Mision 1 - Las palabras del manual: cuantas veces aparece cada una.
#include <cctype>
#include <iostream>
#include <map>
#include <string>

std::string limpiar(const std::string& palabra)
{
    std::string r;
    for (char c : palabra) {
        if (std::isalpha(static_cast<unsigned char>(c))) {
            r += static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        }
    }
    return r;
}

int main()
{
    std::map<std::string, int> veces;
    std::string palabra;
    int total = 0;
    while (std::cin >> palabra) {
        std::string p = limpiar(palabra);
        if (!p.empty()) {
            veces[p]++;
            total++;
        }
    }
    std::string mas_comun;
    int maximo = 0;
    for (const auto& [p, n] : veces) {
        std::cout << p << ": " << n << "\n";
        if (n > maximo) {
            maximo = n;
            mas_comun = p;
        }
    }
    std::cout << total << " palabras, " << veces.size() << " distintas; la más común: " << mas_comun << "\n";
    return 0;
}
```

#### Pruebas

##### Empate en la más común
```entrada
b a b a
```
```salida
a: 2
b: 2
4 palabras, 2 distintas; la más común: a
```

##### Solo números y signos
```entrada
42 ... ¡!
```
```salida
0 palabras, 0 distintas; la más común:
```

##### Mayúsculas y minúsculas
```entrada
Torre TORRE torre Faro
```
```salida
faro: 1
torre: 3
4 palabras, 2 distintas; la más común: torre
```

### Misión R03-N03-M2 · La agenda de la Ciudadela

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Manejá una agenda con un `std::unordered_map<std::string, std::string>` (nombre →
teléfono). Órdenes: `alta nombre telefono` (agrega o actualiza: decí cuál de las
dos), `ver nombre` y `baja nombre`. Al final, cuántos contactos quedan. Ninguna
consulta puede crear contactos por accidente.

#### Criterio de aprobación

- `ver` usa `find` (no `[]`).
- `baja` usa el valor que devuelve `erase`.
- Distingue alta nueva de actualización.

#### Entrada de ejemplo

```
alta Kira 3804112233
alta Bron 3804556677
ver Kira
ver Lyn
alta Kira 3804999000
baja Lyn
baja Bron
ver Kira
```

#### Salida esperada

```
Agregado: Kira
Agregado: Bron
Kira: 3804112233
No está Lyn
Actualizado: Kira
No estaba: Lyn
Borrado: Bron
Kira: 3804999000
Contactos: 1
```

#### Solución de referencia

```cpp
// Mision 2 - La agenda de la Ciudadela: alta, consulta y baja con unordered_map.
#include <iostream>
#include <string>
#include <unordered_map>

int main()
{
    std::unordered_map<std::string, std::string> agenda;
    std::string orden, nombre;
    while (std::cin >> orden >> nombre) {
        if (orden == "alta") {
            std::string telefono;
            std::cin >> telefono;
            bool nuevo = !agenda.contains(nombre);
            agenda[nombre] = telefono;
            std::cout << (nuevo ? "Agregado: " : "Actualizado: ") << nombre << "\n";
        } else if (orden == "ver") {
            auto it = agenda.find(nombre);
            if (it != agenda.end()) {
                std::cout << nombre << ": " << it->second << "\n";
            } else {
                std::cout << "No está " << nombre << "\n";
            }
        } else if (orden == "baja") {
            std::cout << (agenda.erase(nombre) > 0 ? "Borrado: " : "No estaba: ") << nombre << "\n";
        }
    }
    std::cout << "Contactos: " << agenda.size() << "\n";
    return 0;
}
```

#### Pruebas

##### Todo sobre alguien que no está
```entrada
ver Lyn
baja Lyn
ver Lyn
```
```salida
No está Lyn
No estaba: Lyn
No está Lyn
Contactos: 0
```

##### Alta y baja de la misma persona
```entrada
alta Oto 111
baja Oto
alta Oto 222
ver Oto
```
```salida
Agregado: Oto
Borrado: Oto
Agregado: Oto
Oto: 222
Contactos: 1
```

### Misión R03-N03-M3 · Los visitantes de las torres

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea trae `torre visitante` (la torre es `norte` o `reloj`). Guardá los
visitantes de cada torre en un `std::set`. Mostrá los de cada torre, los que
visitaron **las dos**, los que visitaron **solo** la Norte y los que visitaron
**alguna**.

#### Criterio de aprobación

- Usa `std::set` para no repetir visitantes.
- Calcula intersección, diferencia y unión con `contains` e `insert`.

#### Entrada de ejemplo

```
norte Kira
reloj Bron
norte Lyn
reloj Kira
norte Kira
reloj Oto
norte Tesla
reloj Lyn
```

#### Salida esperada

```
Norte (3): Kira Lyn Tesla
Reloj (4): Bron Kira Lyn Oto
Las dos (2): Kira Lyn
Solo Norte (1): Tesla
Alguna (5): Bron Kira Lyn Oto Tesla
```

#### Solución de referencia

```cpp
// Mision 3 - Los visitantes de las torres: sets, interseccion y diferencia.
#include <iostream>
#include <set>
#include <string>

void mostrar(const std::string& titulo, const std::set<std::string>& s)
{
    std::cout << titulo << " (" << s.size() << "):";
    for (const auto& x : s) {
        std::cout << " " << x;
    }
    std::cout << "\n";
}

int main()
{
    std::set<std::string> norte, reloj;
    std::string torre, quien;
    while (std::cin >> torre >> quien) {
        if (torre == "norte") {
            norte.insert(quien);
        } else if (torre == "reloj") {
            reloj.insert(quien);
        }
    }
    std::set<std::string> ambas, solo_norte, alguna = norte;
    for (const auto& q : norte) {
        if (reloj.contains(q)) {
            ambas.insert(q);
        } else {
            solo_norte.insert(q);
        }
    }
    alguna.insert(reloj.begin(), reloj.end());
    mostrar("Norte", norte);
    mostrar("Reloj", reloj);
    mostrar("Las dos", ambas);
    mostrar("Solo Norte", solo_norte);
    mostrar("Alguna", alguna);
    return 0;
}
```

#### Pruebas

##### Nadie en común
```entrada
norte Kira
reloj Bron
```
```salida
Norte (1): Kira
Reloj (1): Bron
Las dos (0):
Solo Norte (1): Kira
Alguna (2): Bron Kira
```

##### Solo la Norte
```entrada
norte Kira
norte Kira
norte Lyn
```
```salida
Norte (2): Kira Lyn
Reloj (0):
Las dos (0):
Solo Norte (2): Kira Lyn
Alguna (2): Kira Lyn
```

##### Sin visitantes
```entrada
```
```salida
Norte (0):
Reloj (0):
Las dos (0):
Solo Norte (0):
Alguna (0):
```

### Encargo R03-N03-E1 · Las ventas por vendedor

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Cada línea es una venta: `vendedor monto`. Acumulá el total y la cantidad de ventas
de cada vendedor con dos `std::map`. Mostrá el resumen por vendedor (en orden
alfabético) y el ranking de mayor a menor total, pasando el map a un vector de
pares y ordenándolo.

#### Criterio de aprobación

- Acumula con `map[vendedor] += monto`.
- Ordena por valor copiando a un vector de pares.

#### Entrada de ejemplo

```
ana 1200
bruno 800
ana 300.5
celi 2500
bruno 1900
ana 50
```

#### Salida esperada

```
Por vendedor:
  ana: $1550.50 en 3 ventas
  bruno: $2700.00 en 2 ventas
  celi: $2500.00 en 1 ventas
Ranking:
  1. bruno
  2. celi
  3. ana
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Las ventas por vendedor: map<string, double> y el ranking.
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>

int main()
{
    std::map<std::string, double> por_vendedor;
    std::map<std::string, int> operaciones;
    std::string vendedor;
    double monto = 0;
    while (std::cin >> vendedor >> monto) {
        por_vendedor[vendedor] += monto;
        operaciones[vendedor]++;
    }
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Por vendedor:\n";
    for (const auto& [v, total] : por_vendedor) {
        std::cout << "  " << v << ": $" << total << " en " << operaciones[v] << " ventas\n";
    }
    // Pasar el map a un vector de pares para ordenarlo por monto
    std::vector<std::pair<std::string, double>> ranking(por_vendedor.begin(), por_vendedor.end());
    std::sort(ranking.begin(), ranking.end(), [](const auto& a, const auto& b) { return a.second > b.second; });
    std::cout << "Ranking:\n";
    for (std::size_t i = 0; i < ranking.size(); i++) {
        std::cout << "  " << i + 1 << ". " << ranking[i].first << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Un solo vendedor
```entrada
zoe 100
zoe 200.25
```
```salida
Por vendedor:
  zoe: $300.25 en 2 ventas
Ranking:
  1. zoe
```

##### Empate en el ranking
```entrada
ana 500
bruno 500
celi 100
```
```salida
Por vendedor:
  ana: $500.00 en 1 ventas
  bruno: $500.00 en 1 ventas
  celi: $100.00 en 1 ventas
Ranking:
  1. ana
  2. bruno
  3. celi
```

### Prueba del sello

#### ¿Qué pasa si hacés `m["x"]` y `"x"` no existía?

Se crea la clave `"x"` con el valor por defecto (0 para `int`).

#### ¿Cómo preguntás si una clave existe sin crearla?

Con `m.contains(k)`, `m.count(k)` o `m.find(k) != m.end()`.

#### ¿Qué diferencia hay entre `std::map` y `std::unordered_map`?

`map` mantiene las claves ordenadas; `unordered_map` no tiene orden pero en general es más rápido.

#### ¿Qué pasa si insertás dos veces lo mismo en un `std::set`?

La segunda no hace nada: el set no guarda repetidos.

#### ¿Por qué buscar en un map es más rápido que en un vector?

Porque no recorre todo: el map descarta la mitad en cada paso (y el `unordered_map` va casi directo).

### Soluciones (docente)

Material original: `04-C++-Moderno/04-Map` y `05-Set`. La lambda del ranking se presenta como receta; se explica en el nodo Lambdas.

## R03-N04 · Estados y valores que pueden faltar

```meta
tipo: tema
padre: R03-N03
precio: 10
criatura: ogro
temas: prog.enums, diseno.maquina-estados, err.opcionales
```

### Crónica

En la sala de control de la Ciudadela hay un tablero con luces: "apagado", "girando", "averiado". Antes, cada estado era un número pintado a mano: el 2 era "averiado"… o el 3, nadie se acordaba.

—Los números mágicos confunden a todos —dice {mentor}—. Los estados tienen **nombre**. Y cuando buscás algo que puede no estar, no inventes un −1: decí claramente "puede que no haya nada".

### Objetivos

Modelar estados con `enum class` y escribir **máquinas de estado** con `switch`;
convertir un estado a texto; y devolver valores que **pueden faltar** con
`std::optional`, sin números especiales como −1.

### Antes de empezar

- Decisiones y `switch` (rama 1).
- Structs, `auto` y textos (ramas 2 y 3).

### Explicación

#### `enum class`: un tipo con valores con nombre
```cpp
enum class Estado { Menu, Jugando, Pausa, Fin };
Estado e = Estado::Menu;
if (e == Estado::Pausa) { ... }
```
- Los valores se escriben con el nombre del tipo adelante: `Estado::Pausa`. Así no
  chocan con otros nombres del programa.
- **No** se convierten solos a `int`: `int x = e;` no compila (evita comparar un
  estado con un número por error). Si hace falta, `static_cast<int>(e)`.
- Tampoco se muestran solos con `cout`: se escribe una función `a_texto`.

Existe también el `enum` "plano" (sin `class`), heredado de C, que sí se convierte
a entero y mete sus nombres en el alcance de afuera. En código nuevo: **siempre
`enum class`**.

#### `switch` sobre un `enum class`
```cpp
switch (e) {
case Estado::Menu:    return "Menú";
case Estado::Jugando: return "Jugando";
case Estado::Pausa:   return "Pausa";
case Estado::Fin:     return "Fin";
}
```
Si el `switch` cubre todos los valores, **no pongas `default`**: así, el día que
agregues un valor nuevo al enum, `-Wall` te avisa en cada `switch` que no lo
maneja.

#### Máquinas de estado
Muchos programas son una **máquina de estados**: están en un estado, llega un
evento, y según el estado y el evento pasan a otro. Un semáforo, un pedido
(pendiente → pagado → enviado), un personaje (quieto, corriendo, saltando), las
pantallas de un juego (menú, jugando, pausa). Con `enum class` y una función
`siguiente(estado, evento)` quedan claras y fáciles de probar.

#### `std::optional<T>`: puede haber, o no
Una función que busca puede no encontrar. Las soluciones viejas (devolver −1,
`nullptr`, o un `bool` más un parámetro por referencia) son fáciles de olvidar.
`std::optional<T>` (de `<optional>`) pone el "puede faltar" **en el tipo**:
```cpp
std::optional<Enemigo> mas_debil(const std::vector<Enemigo>& v)
{
    if (v.empty()) return std::nullopt;   // no hay
    ...
    return elegido;                       // hay: se envuelve solo
}
```
Para usarlo, hay que **abrirlo**:
| Forma | Qué hace |
|---|---|
| `if (r)` o `r.has_value()` | ¿hay valor? |
| `*r` / `r->campo` | el valor (solo si hay) |
| `r.value()` | el valor; si no hay, el programa se corta con un error |
| `r.value_or(otro)` | el valor, o `otro` si no hay |

Una forma muy cómoda de declarar y preguntar a la vez:
```cpp
if (auto objetivo = mas_debil(horda)) {
    std::cout << objetivo->nombre;
}
```

#### ¿Cuándo `optional` y cuándo otra cosa?
`optional` es para "no hay resultado" **sin que sea un error**: buscar y no
encontrar, un campo opcional de un formulario. Si algo **falló** y hay que explicar
por qué (un archivo roto, un dato inválido), en la rama 5 vas a ver las
excepciones.

> **Si venís de C.** `enum class` es un `enum` que no se mezcla con los enteros.
> `optional` reemplaza al "devuelvo −1 si no lo encontré".

### Código de ejemplo

```cpp
/*
 * enum class (estados con nombre) y std::optional (un valor que puede faltar).
 */
#include <iostream>
#include <optional>
#include <string>
#include <vector>

enum class Estado { Menu, Jugando, Pausa, Fin };

std::string a_texto(Estado e)
{
    switch (e) {                     // sin default: si falta un caso, -Wall avisa
    case Estado::Menu:
        return "Menú";
    case Estado::Jugando:
        return "Jugando";
    case Estado::Pausa:
        return "Pausa";
    case Estado::Fin:
        return "Fin";
    }
    return "?";
}

// Una maquina de estados: segun el estado actual y la tecla, el siguiente.
Estado siguiente(Estado actual, char tecla)
{
    switch (actual) {
    case Estado::Menu:
        return tecla == 'j' ? Estado::Jugando : actual;
    case Estado::Jugando:
        if (tecla == 'p') {
            return Estado::Pausa;
        }
        return tecla == 'q' ? Estado::Fin : actual;
    case Estado::Pausa:
        return tecla == 'p' ? Estado::Jugando : actual;
    case Estado::Fin:
        return tecla == 'r' ? Estado::Menu : actual;
    }
    return actual;
}

struct Enemigo {
    std::string nombre;
    int vida = 0;
};

// Puede no haber respuesta: el "no hay" va en el tipo.
std::optional<Enemigo> mas_debil(const std::vector<Enemigo>& enemigos)
{
    if (enemigos.empty()) {
        return std::nullopt;
    }
    Enemigo elegido = enemigos.front();
    for (const auto& e : enemigos) {
        if (e.vida < elegido.vida) {
            elegido = e;
        }
    }
    return elegido;
}

std::optional<int> buscar_indice(const std::vector<std::string>& v, const std::string& x)
{
    for (std::size_t i = 0; i < v.size(); i++) {
        if (v[i] == x) {
            return static_cast<int>(i);
        }
    }
    return {};                        // lo mismo que std::nullopt
}

int main()
{
    Estado estado = Estado::Menu;
    std::cout << "Estado inicial: " << a_texto(estado) << "\n";
    for (char tecla : std::string("jxppq r")) {
        Estado antes = estado;
        estado = siguiente(estado, tecla);
        std::cout << "  '" << tecla << "' -> " << (estado != antes ? a_texto(estado) : "(sin efecto)") << "\n";
    }
    std::cout << "Pausa vale " << static_cast<int>(Estado::Pausa) << " por dentro\n\n";

    std::vector<Enemigo> horda = {{"Orco", 55}, {"Slime", 20}, {"Goblin", 35}};
    if (auto objetivo = mas_debil(horda)) {          // declarar y preguntar en el if
        std::cout << "Atacar primero a " << objetivo->nombre << " (" << objetivo->vida << ")\n";
    }
    std::vector<Enemigo> sala_vacia;
    std::cout << std::boolalpha << "¿Hay objetivo en la sala vacía? " << mas_debil(sala_vacia).has_value() << "\n";

    std::vector<std::string> torres = {"Norte", "Reloj", "Faro"};
    std::cout << "Reloj está en " << buscar_indice(torres, "Reloj").value_or(-1) << "\n";
    std::cout << "Vapor está en " << buscar_indice(torres, "Vapor").value_or(-1) << "\n";
    return 0;
}
```

### Salida esperada

```
Estado inicial: Menú
  'j' -> Jugando
  'x' -> (sin efecto)
  'p' -> Pausa
  'p' -> Jugando
  'q' -> Fin
  ' ' -> (sin efecto)
  'r' -> Menú
Pausa vale 2 por dentro

Atacar primero a Slime (20)
¿Hay objetivo en la sala vacía? false
Reloj está en 1
Vapor está en -1
```

### ¿Para qué sirve?

Los estados con nombre están en todo software: el estado de un pedido o un envío, los pasos de un trámite, las fases de un jefe en un juego, los modos de una máquina. Escribirlos como `enum class` y máquinas de estado evita transiciones imposibles (entregar algo que nunca se pagó). `optional` aparece en cualquier búsqueda: un usuario por email, un producto por código, un turno libre.

### Errores habituales

**Esqueleto: el valor sin el nombre del enum.**
```
main.cpp:2:20: error: ‘A’ was not declared in this scope; did you mean ‘E::A’?
```

**Goblin: tratar un `enum class` como entero.**
```
main.cpp:2:34: error: cannot convert ‘Estado’ to ‘int’ in initialization
```

**Ogro: un caso sin manejar.** Agregaste un valor al enum y te olvidaste de un
`switch`; sin `default`, `g++` avisa:
```
main.cpp:2:21: warning: enumeration value ‘Fin’ not handled in switch [-Wswitch]
```

**Goblin: mostrar un `optional` con `cout`.**
```
main.cpp:3:50: error: no match for ‘operator<<’ (operand types are ‘std::ostream’ ... and ‘std::optional<int>’)
```
Hay que abrirlo: `*r` (si hay) o `r.value_or(0)`.

**Ogro: usar `*r` sin preguntar.** Si el `optional` está vacío, `*r` es
comportamiento indefinido. Preguntá con `if (r)`, o usá `value_or`.

### Misión R03-N04-M1 · El faro automático

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La luz del faro tiene cuatro estados: apagada, girando, destellos y averiada.
Eventos: `noche` (apagada → girando), `niebla` (girando → destellos), `despeja`
(destellos → girando), `dia` (girando o destellos → apagada), `rayo` (cualquiera →
averiada) y `reparar` (averiada → apagada). Cualquier otro evento no cambia nada.
Escribí `enum class Luz`, `a_texto` y `siguiente(luz, evento)`, y procesá los
eventos de la entrada mostrando cada cambio (o que sigue igual).

#### Criterio de aprobación

- Usa `enum class` y un `switch` sin `default` en `a_texto`.
- La lógica de transiciones está en `siguiente`.

#### Entrada de ejemplo

```
dia noche niebla niebla despeja rayo noche reparar noche dia
```

#### Salida esperada

```
dia: sigue apagada
noche: apagada -> girando
niebla: girando -> destellos
niebla: sigue destellos
despeja: destellos -> girando
rayo: girando -> averiada
noche: sigue averiada
reparar: averiada -> apagada
noche: apagada -> girando
dia: girando -> apagada
7 cambios; termina apagada
```

#### Solución de referencia

```cpp
// Mision 1 - El automata del faro: una maquina de estados con enum class.
#include <iostream>
#include <string>

enum class Luz { Apagada, Girando, Destellos, Averiada };

std::string a_texto(Luz l)
{
    switch (l) {
    case Luz::Apagada:
        return "apagada";
    case Luz::Girando:
        return "girando";
    case Luz::Destellos:
        return "destellos";
    case Luz::Averiada:
        return "averiada";
    }
    return "?";
}

Luz siguiente(Luz actual, const std::string& evento)
{
    if (evento == "rayo") {
        return Luz::Averiada;
    }
    switch (actual) {
    case Luz::Apagada:
        return evento == "noche" ? Luz::Girando : actual;
    case Luz::Girando:
        if (evento == "niebla") {
            return Luz::Destellos;
        }
        return evento == "dia" ? Luz::Apagada : actual;
    case Luz::Destellos:
        if (evento == "despeja") {
            return Luz::Girando;
        }
        return evento == "dia" ? Luz::Apagada : actual;
    case Luz::Averiada:
        return evento == "reparar" ? Luz::Apagada : actual;
    }
    return actual;
}

int main()
{
    Luz luz = Luz::Apagada;
    std::string evento;
    int cambios = 0;
    while (std::cin >> evento) {
        Luz nueva = siguiente(luz, evento);
        if (nueva != luz) {
            std::cout << evento << ": " << a_texto(luz) << " -> " << a_texto(nueva) << "\n";
            cambios++;
        } else {
            std::cout << evento << ": sigue " << a_texto(luz) << "\n";
        }
        luz = nueva;
    }
    std::cout << cambios << " cambios; termina " << a_texto(luz) << "\n";
    return 0;
}
```

#### Pruebas

##### Rayo de entrada
```entrada
rayo rayo reparar dia
```
```salida
rayo: apagada -> averiada
rayo: sigue averiada
reparar: averiada -> apagada
dia: sigue apagada
2 cambios; termina apagada
```

##### Eventos desconocidos
```entrada
sol lluvia noche
```
```salida
sol: sigue apagada
lluvia: sigue apagada
noche: apagada -> girando
1 cambios; termina girando
```

##### Sin eventos
```entrada
```
```salida
0 cambios; termina apagada
```

### Misión R03-N04-M2 · El catálogo de piezas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con un catálogo fijo de piezas (código, nombre, precio): E24 engranaje de 24 ($350),
R10 resorte de 10 cm ($25), V03 válvula de presión ($1200). Escribí
`std::optional<Pieza> buscar(catalogo, codigo)`. Cada palabra de la entrada es un
código: mostrá la pieza o que no existe, y el total de lo encontrado. Al final,
usá `value_or` para mostrar el precio de X99 (o 0).

#### Criterio de aprobación

- `buscar` devuelve `std::nullopt` si no encuentra.
- Se abre el optional con `if (p)` y `p->`.
- Usa `value_or`.

#### Entrada de ejemplo

```
E24 V03 Z01 R10 E24
```

#### Salida esperada

```
E24: engranaje de 24 $350
V03: válvula de presión $1200
Z01: no existe
R10: resorte de 10 cm $25
E24: engranaje de 24 $350
Total: $1925
Precio de X99 (o 0): 0
```

#### Solución de referencia

```cpp
// Mision 2 - El catalogo de piezas: buscar por codigo devuelve un optional.
#include <iostream>
#include <optional>
#include <string>
#include <vector>

struct Pieza {
    std::string codigo;
    std::string nombre;
    int precio = 0;
};

std::optional<Pieza> buscar(const std::vector<Pieza>& catalogo, const std::string& codigo)
{
    for (const auto& p : catalogo) {
        if (p.codigo == codigo) {
            return p;
        }
    }
    return std::nullopt;
}

int main()
{
    const std::vector<Pieza> catalogo = {
        {"E24", "engranaje de 24", 350},
        {"R10", "resorte de 10 cm", 25},
        {"V03", "válvula de presión", 1200},
    };
    std::string codigo;
    int total = 0;
    while (std::cin >> codigo) {
        std::optional<Pieza> p = buscar(catalogo, codigo);
        if (p) {
            std::cout << codigo << ": " << p->nombre << " $" << p->precio << "\n";
            total += p->precio;
        } else {
            std::cout << codigo << ": no existe\n";
        }
    }
    std::cout << "Total: $" << total << "\n";
    int precio_x = buscar(catalogo, "X99").value_or(Pieza{"", "", 0}).precio;
    std::cout << "Precio de X99 (o 0): " << precio_x << "\n";
    return 0;
}
```

#### Pruebas

##### Ninguna existe
```entrada
A01 B02
```
```salida
A01: no existe
B02: no existe
Total: $0
Precio de X99 (o 0): 0
```

##### Minúsculas
```entrada
e24 E24
```
```salida
e24: no existe
E24: engranaje de 24 $350
Total: $350
Precio de X99 (o 0): 0
```

##### Sin códigos
```entrada
```
```salida
Total: $0
Precio de X99 (o 0): 0
```

### Misión R03-N04-M3 · Números sin romperse

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `std::optional<int> a_entero(const std::string&)`, que convierte **sin
excepciones**: acepta un signo opcional y solo dígitos, y rechaza lo vacío, lo que
tiene otros caracteres y lo que no entra en un `int`. Leé palabras hasta el final,
sumá las que son números y avisá cuáles ignorás.

#### Criterio de aprobación

- No usa `std::stoi` (ni excepciones).
- Rechaza `12abc`, `-`, `+` solo y números demasiado grandes.
- Usa `if (auto n = a_entero(p))`.

#### Entrada de ejemplo

```
10 -3 +5 12abc - 007 99999999999 x 20
```

#### Salida esperada

```
ignoro "12abc"
ignoro "-"
ignoro "99999999999"
ignoro "x"
5 números, suma 39
```

#### Solución de referencia

```cpp
// Mision 3 - Leer numeros sin romperse: a_entero devuelve optional<int>.
#include <iostream>
#include <optional>
#include <string>

std::optional<int> a_entero(const std::string& s)
{
    if (s.empty()) {
        return std::nullopt;
    }
    std::size_t i = 0;
    bool negativo = false;
    if (s[0] == '-' || s[0] == '+') {
        negativo = (s[0] == '-');
        i = 1;
    }
    if (i == s.size()) {
        return std::nullopt;
    }
    long long valor = 0;
    for (; i < s.size(); i++) {
        if (s[i] < '0' || s[i] > '9') {
            return std::nullopt;
        }
        valor = valor * 10 + (s[i] - '0');
        if (valor > 2147483647LL) {
            return std::nullopt;             // no entra en un int
        }
    }
    return static_cast<int>(negativo ? -valor : valor);
}

int main()
{
    std::string palabra;
    int suma = 0, validos = 0;
    while (std::cin >> palabra) {
        if (auto n = a_entero(palabra)) {
            suma += *n;
            validos++;
        } else {
            std::cout << "ignoro \"" << palabra << "\"\n";
        }
    }
    std::cout << validos << " números, suma " << suma << "\n";
    return 0;
}
```

#### Pruebas

##### Límites del int
```entrada
2147483647 -2147483648 2147483648
```
```salida
ignoro "-2147483648"
ignoro "2147483648"
1 números, suma 2147483647
```

##### Signos solos y ceros
```entrada
+ -0 +0 000
```
```salida
ignoro "+"
3 números, suma 0
```

##### Sin números
```entrada
hola chau
```
```salida
ignoro "hola"
ignoro "chau"
0 números, suma 0
```

### Encargo R03-N04-E1 · El estado del pedido

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un pedido de la tienda online puede estar pendiente, pagado, enviado, entregado o
cancelado. Acciones: `pagar` (pendiente → pagado), `enviar` (pagado → enviado),
`entregar` (enviado → entregado) y `cancelar` (solo si está pendiente o pagado).
Escribí `std::optional<Estado> aplicar(estado, accion)`, que devuelve el estado
nuevo o nada si la acción no se puede hacer. Procesá las acciones de la entrada.

#### Criterio de aprobación

- Los estados son un `enum class`.
- Las acciones imposibles devuelven `std::nullopt` y no cambian el pedido.

#### Entrada de ejemplo

```
enviar pagar pagar enviar cancelar entregar
```

#### Salida esperada

```
enviar: no se puede con el pedido pendiente
pagar: pendiente -> pagado
pagar: no se puede con el pedido pagado
enviar: pagado -> enviado
cancelar: no se puede con el pedido enviado
entregar: enviado -> entregado
Estado final: entregado
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El estado de un pedido: transiciones validas con enum class.
#include <iostream>
#include <optional>
#include <string>

enum class Estado { Pendiente, Pagado, Enviado, Entregado, Cancelado };

std::string a_texto(Estado e)
{
    switch (e) {
    case Estado::Pendiente:
        return "pendiente";
    case Estado::Pagado:
        return "pagado";
    case Estado::Enviado:
        return "enviado";
    case Estado::Entregado:
        return "entregado";
    case Estado::Cancelado:
        return "cancelado";
    }
    return "?";
}

// Devuelve el nuevo estado, o nada si la accion no se puede hacer en este estado.
std::optional<Estado> aplicar(Estado e, const std::string& accion)
{
    if (accion == "pagar" && e == Estado::Pendiente) {
        return Estado::Pagado;
    }
    if (accion == "enviar" && e == Estado::Pagado) {
        return Estado::Enviado;
    }
    if (accion == "entregar" && e == Estado::Enviado) {
        return Estado::Entregado;
    }
    if (accion == "cancelar" && (e == Estado::Pendiente || e == Estado::Pagado)) {
        return Estado::Cancelado;
    }
    return std::nullopt;
}

int main()
{
    Estado pedido = Estado::Pendiente;
    std::string accion;
    while (std::cin >> accion) {
        if (auto nuevo = aplicar(pedido, accion)) {
            std::cout << accion << ": " << a_texto(pedido) << " -> " << a_texto(*nuevo) << "\n";
            pedido = *nuevo;
        } else {
            std::cout << accion << ": no se puede con el pedido " << a_texto(pedido) << "\n";
        }
    }
    std::cout << "Estado final: " << a_texto(pedido) << "\n";
    return 0;
}
```

#### Pruebas

##### Cancelar pendiente
```entrada
cancelar pagar enviar
```
```salida
cancelar: pendiente -> cancelado
pagar: no se puede con el pedido cancelado
enviar: no se puede con el pedido cancelado
Estado final: cancelado
```

##### Pagado y cancelado
```entrada
pagar cancelar entregar
```
```salida
pagar: pendiente -> pagado
cancelar: pagado -> cancelado
entregar: no se puede con el pedido cancelado
Estado final: cancelado
```

##### Acción desconocida
```entrada
volar pagar
```
```salida
volar: no se puede con el pedido pendiente
pagar: pendiente -> pagado
Estado final: pagado
```

### Prueba del sello

#### ¿Qué ventajas tiene `enum class` sobre `enum`?

Sus valores no chocan con otros nombres (van con `Tipo::`) y no se convierten solos a entero.

#### ¿Por qué conviene no poner `default` en un `switch` que cubre todo el enum?

Para que el compilador avise si se agrega un valor nuevo y algún `switch` no lo maneja.

#### ¿Qué es `std::nullopt`?

El valor de un `optional` vacío: "no hay".

#### ¿Qué hace `r.value_or(0)`?

Devuelve el valor si hay, o 0 si el optional está vacío.

#### ¿Cuándo usarías `optional` y cuándo no?

Cuando "no hay resultado" es normal (buscar y no encontrar). Si es un error con causa, conviene otra herramienta (excepciones).

### Soluciones (docente)

Material original: `04-C++-Moderno/06-EnumClass` y `07-Optional`. La versión de FullCursos de `a_entero` usaba `try/catch`; acá se valida a mano porque las excepciones llegan en la rama 5.

## R03-N05 · Lambdas

```meta
tipo: tema
padre: R03-N04
precio: 10
criatura: esqueleto
temas: func.lambdas, func.orden-superior
```

### Crónica

El clasificador de la Ciudadela es una máquina enorme que ordena piezas. Pero no sabe **cómo** ordenarlas: por peso, por tamaño, por color. Cada vez que la usás, le das una tarjetita con la regla: "la más pesada primero".

—Escribir una función entera, con nombre, para una regla que uso una sola vez, es un desperdicio —dice {mentor}—. Escribo la regla **ahí mismo**, en la tarjeta. Eso es una lambda.

### Objetivos

Escribir **lambdas** (funciones sin nombre, escritas en el lugar), con sus
capturas (`[]`, `[x]`, `[&x]`), y usarlas con los algoritmos de la biblioteca:
`sort` con criterio propio, `find_if`, `count_if`, `any_of`, `for_each`,
`transform`, `copy_if` y `std::erase_if`.

### Antes de empezar

- Funciones (rama 1) y vectores con `sort` y `find` (rama 1).
- Structs y `auto` (ramas 2 y 3).

### Explicación

#### La forma de una lambda
```cpp
[captura](parámetros) { cuerpo }
```
Por ejemplo, "¿a va antes que b?" para ordenar por vida, de mayor a menor:
```cpp
std::sort(grupo.begin(), grupo.end(),
          [](const Heroe& a, const Heroe& b) { return a.vida > b.vida; });
```
Es una función como cualquier otra, pero sin nombre y escrita justo donde se
necesita. El tipo que devuelve lo deduce el compilador.

#### Guardarla en una variable
```cpp
auto etiqueta = [](const Heroe& h) { return h.vida > 100 ? "tanque" : "ágil"; };
etiqueta(kira);    // se llama como una función
```

#### Capturas: usar variables de afuera
Por defecto, una lambda **no ve** las variables del lugar donde se escribe. Hay que
**capturarlas**:
| Captura | Significa |
|---|---|
| `[]` | nada |
| `[umbral]` | una **copia** de `umbral` (la lambda no puede cambiar la original) |
| `[&total]` | `total` **por referencia** (la lambda puede modificarla) |
| `[umbral, &total]` | varias, cada una a su manera |
| `[=]` / `[&]` | todo lo que use, por copia / por referencia |

Preferí nombrar lo que capturás: se entiende mejor qué usa cada lambda.

#### Los algoritmos que reciben una lambda
| Algoritmo | Qué hace con la lambda |
|---|---|
| `std::sort(b, e, cmp)` | `cmp(a, b)`: ¿`a` va antes que `b`? |
| `std::find_if(b, e, pred)` | el primero donde `pred` da `true` (o `e`) |
| `std::count_if(b, e, pred)` | cuántos cumplen |
| `std::any_of` / `all_of` / `none_of` | ¿alguno / todos / ninguno cumple? |
| `std::for_each(b, e, f)` | llama a `f` con cada elemento |
| `std::transform(b, e, destino, f)` | guarda `f(x)` de cada `x` en `destino` |
| `std::copy_if(b, e, destino, pred)` | copia los que cumplen |
| `std::min_element(b, e, cmp)` | el menor según `cmp` |
| `std::erase_if(v, pred)` (C++20) | **borra** del vector los que cumplen, y dice cuántos |

Para `copy_if` a un vector vacío, el destino es `std::back_inserter(v)` (va
haciendo `push_back`, de `<iterator>`; lo trae `<algorithm>` en la práctica).

#### Ordenar por varios criterios
La lambda compara por el primer criterio; si empatan, por el segundo:
```cpp
[](const Equipo& a, const Equipo& b) {
    if (a.puntos != b.puntos) return a.puntos > b.puntos;
    return a.nombre < b.nombre;
}
```
Siempre con `<` o `>` **estricto**: con `<=` o `>=`, `sort` puede fallar.

#### Borrar los que cumplen algo
Antes de C++20 se usaba el "idioma remove-erase":
```cpp
v.erase(std::remove_if(v.begin(), v.end(), pred), v.end());
```
Lo vas a ver en código ajeno. En C++20, `std::erase_if(v, pred)` hace lo mismo en
una línea.

> **Si venís de C.** Es como pasarle a `qsort` un puntero a función, pero escrita
> ahí mismo, con tipos, y pudiendo usar variables de afuera.

### Código de ejemplo

```cpp
/*
 * Lambdas: funciones chiquitas escritas en el lugar donde se usan.
 */
#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

struct Heroe {
    std::string nombre;
    int vida = 0;
    int nivel = 0;
};

void mostrar(const std::string& titulo, const std::vector<Heroe>& v)
{
    std::cout << titulo << ":";
    for (const auto& h : v) {
        std::cout << " " << h.nombre << "(" << h.vida << ")";
    }
    std::cout << "\n";
}

int main()
{
    std::vector<Heroe> grupo = {{"Kira", 120, 5}, {"Lyn", 70, 8}, {"Bron", 160, 3}, {"Oto", 90, 6}};

    // [captura](parametros) { cuerpo }
    std::sort(grupo.begin(), grupo.end(), [](const Heroe& a, const Heroe& b) { return a.vida > b.vida; });
    mostrar("Por vida, de mayor a menor", grupo);

    std::sort(grupo.begin(), grupo.end(), [](const Heroe& a, const Heroe& b) { return a.nombre < b.nombre; });
    mostrar("Por nombre", grupo);

    // find_if: el primero que cumple
    auto it = std::find_if(grupo.begin(), grupo.end(), [](const Heroe& h) { return h.nivel >= 6; });
    if (it != grupo.end()) {
        std::cout << "Primero con nivel 6 o más: " << it->nombre << "\n";
    }

    // Captura por copia [umbral]: la lambda usa una variable de afuera
    int umbral = 100;
    auto heridos = std::count_if(grupo.begin(), grupo.end(), [umbral](const Heroe& h) { return h.vida < umbral; });
    std::cout << "Heridos (vida < " << umbral << "): " << heridos << "\n";

    // Captura por referencia [&total]: la lambda MODIFICA una variable de afuera
    int total = 0;
    std::for_each(grupo.begin(), grupo.end(), [&total](const Heroe& h) { total += h.vida; });
    std::cout << "Vida total: " << total << "\n";

    // any_of / all_of
    bool alguno_debil = std::any_of(grupo.begin(), grupo.end(), [](const Heroe& h) { return h.vida < 80; });
    std::cout << std::boolalpha << "¿Alguno con menos de 80? " << alguno_debil << "\n";

    // Una lambda guardada en una variable, para reusarla
    auto etiqueta = [](const Heroe& h) { return h.vida > 100 ? "tanque" : "ágil"; };
    for (const auto& h : grupo) {
        std::cout << "  " << h.nombre << ": " << etiqueta(h) << "\n";
    }

    // C++20: std::erase_if borra todos los que cumplen
    std::erase_if(grupo, [](const Heroe& h) { return h.nivel < 5; });
    mostrar("Sin los de nivel bajo", grupo);

    // transform: armar otro vector a partir del primero
    std::vector<int> niveles(grupo.size());
    std::transform(grupo.begin(), grupo.end(), niveles.begin(), [](const Heroe& h) { return h.nivel; });
    std::cout << "Suma de niveles: " << std::accumulate(niveles.begin(), niveles.end(), 0) << "\n";
    return 0;
}
```

### Salida esperada

```
Por vida, de mayor a menor: Bron(160) Kira(120) Oto(90) Lyn(70)
Por nombre: Bron(160) Kira(120) Lyn(70) Oto(90)
Primero con nivel 6 o más: Lyn
Heridos (vida < 100): 2
Vida total: 440
¿Alguno con menos de 80? true
  Bron: tanque
  Kira: tanque
  Lyn: ágil
  Oto: ágil
Sin los de nivel bajo: Kira(120) Lyn(70) Oto(90)
Suma de niveles: 19
```

### ¿Para qué sirve?

Las lambdas son la forma normal de decirle a la biblioteca "cómo": ordenar productos por precio, filtrar los clientes morosos, buscar el primer turno libre, contar las ventas grandes, aplicar un descuento a toda una lista. También se usan para reaccionar a eventos ("cuando toquen este botón, hacé esto"), algo que vas a ver en la rama de Qt (la 6) y en la rama 4 con `std::function`.

### Errores habituales

**Esqueleto: usar una variable sin capturarla.**
```
main.cpp:3:115: error: ‘umbral’ is not captured
main.cpp:3:94: note: the lambda has no capture-default
```
Agregala a los corchetes: `[umbral]`.

**Ogro: capturar por copia algo que querías modificar.** `[total](...) { total +=
...; }` ni siquiera compila (la copia es de solo lectura); y con `mutable` compila
pero modifica la copia. Para acumular afuera: `[&total]`.

**Ogro: el comparador con `<=`.** `sort` con `a.vida <= b.vida` rompe la regla de
"orden estricto": con elementos iguales puede dar resultados raros o incluso leer
fuera del vector.

**Orco: `transform` a un vector vacío.** El destino tiene que tener lugar
(`std::vector<int> r(v.size());`) o usar `std::back_inserter(r)`.

**Troll: capturar por referencia algo que muere.** Una lambda guardada que capturó
`[&x]` de una función que ya terminó apunta a nada. Si la lambda vive más que la
variable, capturá por copia.

### Misión R03-N05-M1 · La tabla del torneo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea trae `equipo puntos goles_a_favor goles_en_contra`. Ordená la tabla con
**una** lambda: más puntos primero; si empatan, mejor diferencia de gol; si
empatan, más goles a favor; y si siguen empatados, por nombre. Mostrá la posición,
el nombre, los puntos y la diferencia (con `+` si es positiva).

#### Criterio de aprobación

- Un solo `std::sort` con una lambda de varios criterios.
- Las comparaciones son estrictas.

#### Entrada de ejemplo

```
Relojeros 10 8 5
Faro 12 9 4
Vapor 10 9 6
Norte 10 8 5
Puente 7 5 9
```

#### Salida esperada

```
1. Faro 12 pts (+5)
2. Vapor 10 pts (+3)
3. Norte 10 pts (+3)
4. Relojeros 10 pts (+3)
5. Puente 7 pts (-4)
```

#### Solución de referencia

```cpp
// Mision 1 - La tabla de clasificacion: ordenar por varios criterios con lambdas.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Equipo {
    std::string nombre;
    int puntos = 0;
    int goles_favor = 0;
    int goles_contra = 0;
    int diferencia() const { return goles_favor - goles_contra; }
};

int main()
{
    std::vector<Equipo> tabla;
    Equipo e;
    while (std::cin >> e.nombre >> e.puntos >> e.goles_favor >> e.goles_contra) {
        tabla.push_back(e);
    }
    // puntos; si empatan, diferencia de gol; si empatan, mas goles a favor; si no, por nombre
    std::sort(tabla.begin(), tabla.end(), [](const Equipo& a, const Equipo& b) {
        if (a.puntos != b.puntos) {
            return a.puntos > b.puntos;
        }
        if (a.diferencia() != b.diferencia()) {
            return a.diferencia() > b.diferencia();
        }
        if (a.goles_favor != b.goles_favor) {
            return a.goles_favor > b.goles_favor;
        }
        return a.nombre < b.nombre;
    });
    for (std::size_t i = 0; i < tabla.size(); i++) {
        const auto& t = tabla[i];
        std::cout << i + 1 << ". " << t.nombre << " " << t.puntos << " pts (" << (t.diferencia() > 0 ? "+" : "")
                  << t.diferencia() << ")\n";
    }
    return 0;
}
```

#### Pruebas

##### Todos empatados
```entrada
B 5 3 3
A 5 3 3
C 5 3 3
```
```salida
1. A 5 pts (0)
2. B 5 pts (0)
3. C 5 pts (0)
```

##### Diferencia negativa en la punta
```entrada
Alfa 9 1 5
Beta 9 2 3
Gama 3 10 0
```
```salida
1. Beta 9 pts (-1)
2. Alfa 9 pts (-4)
3. Gama 3 pts (+10)
```

### Misión R03-N05-M2 · El radar de la muralla

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La primera línea es el alcance del radar; las siguientes, contactos `nombre x y`
(la muralla está en el origen). Con lambdas: contá cuántos están dentro del alcance
(`count_if`), encontrá el primero en alcance (`find_if`), el más cercano
(`min_element` con comparador) y decí si nadie está a menos de 2 (`none_of`).
Guardá la distancia y "está en alcance" en variables lambda y reutilizalas.

#### Criterio de aprobación

- Hay lambdas guardadas en variables y reutilizadas.
- Alguna lambda captura el alcance por copia.

#### Entrada de ejemplo

```
10
cuervo 12 3
goblin 4 5
lobo 1 1.5
orco 9 9
zorro -3 -4
```

#### Salida esperada

```
Dentro del alcance (10): 3 de 5
Primer contacto en alcance: goblin
El más cercano: lobo a 1.80278
¡Hay alguien pegado a la muralla!
```

#### Solución de referencia

```cpp
// Mision 2 - El radar de la muralla: buscar y contar con capturas.
#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Contacto {
    std::string nombre;
    double x = 0;
    double y = 0;
};

int main()
{
    double alcance = 0;
    std::cin >> alcance;
    std::vector<Contacto> radar;
    Contacto c;
    while (std::cin >> c.nombre >> c.x >> c.y) {
        radar.push_back(c);
    }
    auto distancia = [](const Contacto& k) { return std::hypot(k.x, k.y); };
    auto en_alcance = [alcance, distancia](const Contacto& k) { return distancia(k) <= alcance; };

    auto dentro = std::count_if(radar.begin(), radar.end(), en_alcance);
    std::cout << "Dentro del alcance (" << alcance << "): " << dentro << " de " << radar.size() << "\n";

    auto primero = std::find_if(radar.begin(), radar.end(), en_alcance);
    if (primero != radar.end()) {
        std::cout << "Primer contacto en alcance: " << primero->nombre << "\n";
    }
    auto cercano = std::min_element(radar.begin(), radar.end(),
                                    [&distancia](const Contacto& a, const Contacto& b) { return distancia(a) < distancia(b); });
    if (cercano != radar.end()) {
        std::cout << "El más cercano: " << cercano->nombre << " a " << distancia(*cercano) << "\n";
    }
    bool todos_lejos = std::none_of(radar.begin(), radar.end(), [](const Contacto& k) { return std::hypot(k.x, k.y) < 2; });
    std::cout << (todos_lejos ? "Nadie pegado a la muralla." : "¡Hay alguien pegado a la muralla!") << "\n";
    return 0;
}
```

#### Pruebas

##### Nadie en alcance
```entrada
5
lejos 100 100
otro -50 0
```
```salida
Dentro del alcance (5): 0 de 2
El más cercano: otro a 50
Nadie pegado a la muralla.
```

##### Todos pegados
```entrada
3
a 0 0
b 1 1
```
```salida
Dentro del alcance (3): 2 de 2
Primer contacto en alcance: a
El más cercano: a a 0
¡Hay alguien pegado a la muralla!
```

### Misión R03-N05-M3 · La limpieza del campo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea trae un enemigo `nombre vida`. Mostralos; aplicá una explosión de 25 de
daño a todos con `for_each` (capturando el daño); borrá los caídos con
`std::erase_if` y decí cuántos cayeron; y armá con `transform` un vector de "gritos"
(el nombre con `!`).

#### Criterio de aprobación

- El `for_each` recibe cada enemigo por referencia.
- Usa el valor que devuelve `std::erase_if`.
- El vector destino de `transform` tiene el tamaño justo.

#### Entrada de ejemplo

```
slime 20
orco 60
goblin 25
troll 90
rata 5
```

#### Salida esperada

```
Al principio: slime(20) orco(60) goblin(25) troll(90) rata(5)
Tras la explosión: slime(-5) orco(35) goblin(0) troll(65) rata(-20)
Caen 3; quedan: orco(35) troll(65)
Gritos: orco! troll!
```

#### Solución de referencia

```cpp
// Mision 3 - La limpieza del campo: erase_if y transform.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Enemigo {
    std::string nombre;
    int vida = 0;
};

void mostrar(const std::vector<Enemigo>& v)
{
    for (const auto& e : v) {
        std::cout << " " << e.nombre << "(" << e.vida << ")";
    }
    std::cout << "\n";
}

int main()
{
    std::vector<Enemigo> campo;
    Enemigo e;
    while (std::cin >> e.nombre >> e.vida) {
        campo.push_back(e);
    }
    std::cout << "Al principio:";
    mostrar(campo);

    int dano = 25;
    std::for_each(campo.begin(), campo.end(), [dano](Enemigo& x) { x.vida -= dano; });
    std::cout << "Tras la explosión:";
    mostrar(campo);

    auto caidos = std::erase_if(campo, [](const Enemigo& x) { return x.vida <= 0; });
    std::cout << "Caen " << caidos << "; quedan:";
    mostrar(campo);

    std::vector<std::string> nombres(campo.size());
    std::transform(campo.begin(), campo.end(), nombres.begin(), [](const Enemigo& x) { return x.nombre + "!"; });
    std::cout << "Gritos:";
    for (const auto& n : nombres) {
        std::cout << " " << n;
    }
    std::cout << "\n";
    return 0;
}
```

#### Pruebas

##### Nadie cae
```entrada
orco 60
troll 90
```
```salida
Al principio: orco(60) troll(90)
Tras la explosión: orco(35) troll(65)
Caen 0; quedan: orco(35) troll(65)
Gritos: orco! troll!
```

##### Caen todos
```entrada
rata 5
slime 25
```
```salida
Al principio: rata(5) slime(25)
Tras la explosión: rata(-20) slime(0)
Caen 2; quedan:
Gritos:
```

##### Sin enemigos
```entrada
```
```salida
Al principio:
Tras la explosión:
Caen 0; quedan:
Gritos:
```

### Encargo R03-N05-E1 · El buscador de la ferretería

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La primera línea trae un rubro y un precio tope. Las siguientes, productos
`nombre rubro precio stock`. Mostrá los productos de ese rubro, que no pasen del
tope y que tengan stock, ordenados por precio (y por nombre si empatan). Usá
`copy_if` con `std::back_inserter` y una lambda que capture el rubro y el tope.

#### Criterio de aprobación

- El filtro es una lambda con capturas.
- Usa `copy_if` y `back_inserter`.
- Si no hay resultados, lo dice.

#### Entrada de ejemplo

```
herramientas 5000
martillo herramientas 4200 3
tornillo fijaciones 50 900
pinza herramientas 3900 0
llave herramientas 3900 5
sierra herramientas 8700 2
destornillador herramientas 1800 12
```

#### Salida esperada

```
Rubro herramientas hasta $5000:
  destornillador $1800 (12)
  llave $3900 (5)
  martillo $4200 (3)
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El buscador de la ferreteria: filtros y ordenes con lambdas.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Producto {
    std::string nombre;
    std::string rubro;
    int precio = 0;
    int stock = 0;
};

int main()
{
    std::string rubro;
    int tope = 0;
    std::cin >> rubro >> tope;
    std::vector<Producto> todos;
    Producto p;
    while (std::cin >> p.nombre >> p.rubro >> p.precio >> p.stock) {
        todos.push_back(p);
    }
    auto sirve = [&rubro, tope](const Producto& x) { return x.rubro == rubro && x.precio <= tope && x.stock > 0; };
    std::vector<Producto> elegidos;
    std::copy_if(todos.begin(), todos.end(), std::back_inserter(elegidos), sirve);
    std::sort(elegidos.begin(), elegidos.end(), [](const Producto& a, const Producto& b) {
        return a.precio != b.precio ? a.precio < b.precio : a.nombre < b.nombre;
    });
    std::cout << "Rubro " << rubro << " hasta $" << tope << ":\n";
    for (const auto& x : elegidos) {
        std::cout << "  " << x.nombre << " $" << x.precio << " (" << x.stock << ")\n";
    }
    if (elegidos.empty()) {
        std::cout << "  nada\n";
    }
    return 0;
}
```

#### Pruebas

##### Nada del rubro
```entrada
jardin 1000
martillo herramientas 4200 3
```
```salida
Rubro jardin hasta $1000:
  nada
```

##### Empate de precio
```entrada
fijaciones 100
tuerca fijaciones 50 10
arandela fijaciones 50 4
clavo fijaciones 100 0
perno fijaciones 101 9
```
```salida
Rubro fijaciones hasta $100:
  arandela $50 (4)
  tuerca $50 (10)
```

### Prueba del sello

#### ¿Qué partes tiene una lambda?

La captura entre `[]`, los parámetros entre `()` y el cuerpo entre `{}`.

#### ¿Qué diferencia hay entre `[x]` y `[&x]`?

`[x]` captura una copia (no puede modificar la original); `[&x]` captura por referencia (puede modificarla).

#### ¿Qué tiene que devolver la lambda que le pasás a `std::sort`?

`true` si el primer elemento va antes que el segundo, con una comparación estricta.

#### ¿Qué hace `std::erase_if(v, pred)`?

Borra del vector todos los elementos para los que `pred` da `true`, y devuelve cuántos borró.

#### ¿Qué hace `std::back_inserter(v)`?

Un destino que hace `push_back` en `v` con cada elemento que recibe.

### Soluciones (docente)

Material original: `04-C++-Moderno/08-Lambdas`, ampliado con `transform`, `copy_if`, `erase_if` y el idioma remove-erase (que aparecía en `03-C++/11-Vector`).

## R03-N06 · Archivos y carpetas

```meta
tipo: tema
padre: R03-N05
precio: 10
criatura: troll
temas: arch.texto, arch.csv, arch.rutas
```

### Crónica

Cuando cae la noche, la Ciudadela se apaga… pero sus registros no. Todo lo que pasó en el día quedó escrito en los libros del Archivo: el stock, las cuentas, los turnos.

—Un programa que olvida todo al cerrarse no le sirve a nadie —dice {mentor}—. Lo que importa se **guarda en un archivo**. Y lo bueno de C++: los archivos se cierran solos, aunque te olvides.

### Objetivos

Escribir y leer archivos de texto con `std::ofstream` y `std::ifstream`, agregar
al final, leer línea por línea y en formato CSV, y trabajar con rutas y carpetas
con `std::filesystem`: crear, listar, consultar tamaños y borrar.

### Antes de empezar

- `std::getline` e `istringstream` (Textos a fondo).
- `std::map` (Diccionarios y conjuntos).

### Explicación

#### Escribir: `std::ofstream`
```cpp
#include <fstream>
std::ofstream out("piezas.csv");     // abre para escribir (lo crea, o lo VACÍA si existía)
if (!out) { /* no se pudo abrir */ }
out << "engranaje;12;350\n";          // igual que con cout
```
Para **agregar al final** sin borrar lo que había:
```cpp
std::ofstream out("bitacora.txt", std::ios::app);
```

#### Leer: `std::ifstream`
```cpp
std::ifstream in("piezas.csv");
if (!in) { /* no existe o no se puede leer */ }
std::string linea;
while (std::getline(in, linea)) { ... }   // línea por línea
int n; in >> n;                            // o con >>, igual que cin
```
Para leer un CSV, se combina con `std::istringstream` y `std::getline` con
separador (como en Textos a fondo).

#### Se cierran solos
No hace falta `close()`: cuando la variable `out` o `in` deja de existir (al
terminar su bloque), el archivo **se cierra solo** y lo escrito queda guardado.
Esto se llama **RAII** y es una de las ideas centrales de C++: la vas a ver a fondo
en dos nodos. Si necesitás que el archivo se cierre antes (por ejemplo, para
releerlo), encerralo en un bloque `{ }`.

#### Rutas y carpetas: `std::filesystem`
```cpp
#include <filesystem>
namespace fs = std::filesystem;           // alias corto

fs::path ruta = fs::path("deposito") / "piezas.csv";   // / arma rutas (en cualquier sistema)
fs::create_directories("deposito/respaldos");           // crea todo el camino
fs::exists(ruta);   fs::file_size(ruta);   fs::remove(ruta);   fs::remove_all("deposito");
ruta.filename();    ruta.stem();    ruta.extension();    ruta.parent_path();
```
Para recorrer una carpeta:
```cpp
for (const auto& entrada : fs::directory_iterator("deposito")) {
    entrada.path();  entrada.is_directory();  entrada.is_regular_file();  entrada.file_size();
}
```
`fs::recursive_directory_iterator` recorre también las subcarpetas. **El orden en
que aparecen los archivos no está garantizado** (depende del sistema): si lo vas a
mostrar, guardalos en un vector y ordenalos.

#### ¿Dónde se crean los archivos?
Una ruta relativa (`"piezas.csv"`) se busca en la **carpeta desde donde ejecutás**
el programa, no donde está el `.cpp`. Si ejecutás `./build/programa` desde la
carpeta del proyecto, el archivo aparece en la carpeta del proyecto.

> **Si venís de C.** `ofstream`/`ifstream` reemplazan a `fopen`/`fprintf`/`fgets`,
> y se cierran solos (no hay `fclose` que olvidar). `std::filesystem` reemplaza a
> las funciones de cada sistema operativo (`dirent.h`, `stat`, la API de Windows).

### Código de ejemplo

```cpp
/*
 * Archivos: escribir y leer con fstream, y manejar carpetas con filesystem.
 */
#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

namespace fs = std::filesystem;   // un alias corto

struct Pieza {
    std::string nombre;
    int cantidad = 0;
    double precio = 0;
};

bool guardar(const fs::path& ruta, const std::vector<Pieza>& piezas)
{
    std::ofstream out(ruta);                 // abre (y crea o vacia) el archivo
    if (!out) {
        return false;
    }
    out << "nombre;cantidad;precio\n";       // una cabecera
    for (const auto& p : piezas) {
        out << p.nombre << ";" << p.cantidad << ";" << p.precio << "\n";
    }
    return true;
}   // aca out se destruye y el archivo se CIERRA solo

std::vector<Pieza> cargar(const fs::path& ruta)
{
    std::vector<Pieza> piezas;
    std::ifstream in(ruta);
    if (!in) {
        return piezas;
    }
    std::string linea;
    std::getline(in, linea);                 // saltear la cabecera
    while (std::getline(in, linea)) {
        std::istringstream campos(linea);
        Pieza p;
        std::string cantidad, precio;
        if (std::getline(campos, p.nombre, ';') && std::getline(campos, cantidad, ';') && std::getline(campos, precio)) {
            p.cantidad = std::stoi(cantidad);
            p.precio = std::stod(precio);
            piezas.push_back(p);
        }
    }
    return piezas;
}

int main()
{
    fs::path carpeta = "deposito";
    fs::create_directories(carpeta / "respaldos");            // crea todo el camino
    fs::path ruta = carpeta / "piezas.csv";                     // / arma rutas

    guardar(ruta, {{"engranaje", 12, 350}, {"resorte", 40, 25.5}});

    std::ofstream(ruta, std::ios::app) << "valvula;3;1200\n";  // app: agregar al final
    std::ofstream(carpeta / "notas.txt") << "revisar la caldera\n";

    for (const auto& p : cargar(ruta)) {
        std::cout << p.nombre << ": " << p.cantidad << " x $" << p.precio << "\n";
    }

    std::cout << "\n" << ruta << " existe: " << std::boolalpha << fs::exists(ruta)
              << ", ocupa " << fs::file_size(ruta) << " bytes\n";
    std::cout << "nombre " << ruta.filename() << ", sin extensión " << ruta.stem()
              << ", extensión " << ruta.extension() << "\n";

    // Listar una carpeta. El orden del directorio no esta garantizado: se ordena.
    std::vector<std::string> nombres;
    for (const auto& entrada : fs::directory_iterator(carpeta)) {
        nombres.push_back((entrada.is_directory() ? "[carpeta] " : "") + entrada.path().filename().string());
    }
    std::sort(nombres.begin(), nombres.end());
    std::cout << "Contenido de " << carpeta << ":\n";
    for (const auto& n : nombres) {
        std::cout << "  " << n << "\n";
    }

    std::cout << "Borrados: " << fs::remove_all(carpeta) << " elementos\n";
    return 0;
}
```

### Salida esperada

```
engranaje: 12 x $350
resorte: 40 x $25.5
valvula: 3 x $1200

"deposito/piezas.csv" existe: true, ocupa 71 bytes
nombre "piezas.csv", sin extensión "piezas", extensión ".csv"
Contenido de "deposito":
  [carpeta] respaldos
  notas.txt
  piezas.csv
Borrados: 4 elementos
```

### ¿Para qué sirve?

Guardar y cargar es parte de casi cualquier programa: las partidas de un juego, la configuración de una aplicación, los registros (logs) de un servidor, los reportes en CSV que después se abren con Excel, los respaldos de una base de datos. `std::filesystem` sirve para herramientas que ordenan fotos por fecha, buscan archivos duplicados, limpian carpetas temporales o arman el índice de un proyecto.

### Errores habituales

**Ogro: no revisar si abrió.** Si el archivo no existe (o la ruta está mal),
`ifstream` no avisa: las lecturas simplemente fallan y el programa sigue como si el
archivo estuviera vacío. Preguntá `if (!in)`.

**Troll: `ofstream` sin `app` borra todo.** Abrir para escribir **vacía** el
archivo. Para agregar al final, `std::ios::app`.

**Ogro: leer un archivo que todavía está abierto para escribir.** Lo escrito puede
no estar guardado todavía (sigue en el buffer). Cerralo antes: terminá su bloque.

**Esqueleto: el alias `fs` sin declarar.**
```
main.cpp:2:14: error: ‘fs’ has not been declared
```
Falta `namespace fs = std::filesystem;`.

**Ogro: confiar en el orden de `directory_iterator`.** En tu compu sale en un orden
y en otra en otro. Ordená antes de mostrar.

**Ogro: la ruta relativa desde otra carpeta.** "No encuentra el archivo", pero el
archivo está: ejecutaste desde otra carpeta. Mirá `fs::current_path()`.

### Misión R03-N06-M1 · La bitácora

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El programa crea `bitacora.txt` con una primera línea ("Día 1: llegué a la
Ciudadela"). Después, cada línea no vacía de la entrada se **agrega al final** del
archivo (con `std::ios::app`). Al terminar, releé el archivo y mostralo numerado,
con la cantidad de líneas y de bytes de texto.

#### Criterio de aprobación

- Crea el archivo de cero y después agrega con `std::ios::app`.
- Relee el archivo desde el disco (no desde memoria).

#### Entrada de ejemplo

```
Día 2: Tesla me mostró los planos

Día 3: vencí al Autómata
Día 4: la Arena
```

#### Salida esperada

```
Agregadas: 3
1: Día 1: llegué a la Ciudadela
2: Día 2: Tesla me mostró los planos
3: Día 3: vencí al Autómata
4: Día 4: la Arena
4 líneas, 108 bytes de texto
```

#### Solución de referencia

```cpp
// Mision 1 - La bitacora: agregar lineas a un archivo y releerlo numerado.
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    const std::string RUTA = "bitacora.txt";
    {
        std::ofstream out(RUTA);                  // empezar de cero
        out << "Día 1: llegué a la Ciudadela\n";
    }
    std::string linea;
    int agregadas = 0;
    while (std::getline(std::cin, linea)) {
        if (linea.empty()) {
            continue;
        }
        std::ofstream out(RUTA, std::ios::app);   // agregar al final
        out << linea << "\n";
        agregadas++;
    }
    std::cout << "Agregadas: " << agregadas << "\n";

    std::ifstream in(RUTA);
    int numero = 0;
    std::size_t caracteres = 0;
    while (std::getline(in, linea)) {
        numero++;
        caracteres += linea.size();
        std::cout << numero << ": " << linea << "\n";
    }
    std::cout << numero << " líneas, " << caracteres << " bytes de texto\n";
    return 0;
}
```

#### Pruebas

##### Sin líneas nuevas
```entrada
```
```salida
Agregadas: 0
1: Día 1: llegué a la Ciudadela
1 líneas, 30 bytes de texto
```

##### Una línea
```entrada

Día 2: nada nuevo
```
```salida
Agregadas: 1
1: Día 1: llegué a la Ciudadela
2: Día 2: nada nuevo
2 líneas, 48 bytes de texto
```

### Misión R03-N06-M2 · Las notas en CSV

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea de la entrada trae `alumno nota1 nota2 nota3`. Guardalas en
`notas.csv` con una cabecera (`alumno,nota1,nota2,nota3`) y separadas por comas.
Después, **leé el archivo**: salteá la cabecera, partí cada línea por las comas y
mostrá el promedio de cada alumno (con "(recupera)" si es menor que 6) y el del
curso, con 2 decimales.

#### Criterio de aprobación

- Escribe el CSV y lo cierra antes de leerlo.
- Lee con `getline` e `istringstream` con separador `,`.
- Revisa que el archivo se haya abierto.

#### Entrada de ejemplo

```
Ana 8 9 7
Bruno 4 6 5
Celi 10 9 8
Dami 6 5 6
```

#### Salida esperada

```
Ana: 8.00
Bruno: 5.00 (recupera)
Celi: 9.00
Dami: 5.67 (recupera)
Promedio del curso: 6.92
```

#### Solución de referencia

```cpp
// Mision 2 - Las notas en CSV: guardar lo que llega, leerlo y promediar.
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

int main()
{
    const std::string RUTA = "notas.csv";
    {
        std::ofstream out(RUTA);
        out << "alumno,nota1,nota2,nota3\n";
        std::string nombre;
        int a = 0, b = 0, c = 0;
        while (std::cin >> nombre >> a >> b >> c) {
            out << nombre << "," << a << "," << b << "," << c << "\n";
        }
    }

    std::ifstream in(RUTA);
    if (!in) {
        std::cout << "No se pudo abrir " << RUTA << "\n";
        return 1;
    }
    std::string linea;
    std::getline(in, linea);
    std::cout << std::fixed << std::setprecision(2);
    int alumnos = 0;
    double suma_general = 0;
    while (std::getline(in, linea)) {
        std::istringstream campos(linea);
        std::string nombre, nota;
        std::getline(campos, nombre, ',');
        double suma = 0;
        int cuantas = 0;
        while (std::getline(campos, nota, ',')) {
            suma += std::stod(nota);
            cuantas++;
        }
        double promedio = cuantas > 0 ? suma / cuantas : 0;
        std::cout << nombre << ": " << promedio << (promedio >= 6 ? "" : " (recupera)") << "\n";
        suma_general += promedio;
        alumnos++;
    }
    if (alumnos > 0) {
        std::cout << "Promedio del curso: " << suma_general / alumnos << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Un solo alumno aprobado
```entrada
Eva 6 6 6
```
```salida
Eva: 6.00
Promedio del curso: 6.00
```

##### Todos recuperan
```entrada
Fede 1 2 3
Gabi 5 5 5
```
```salida
Fede: 2.00 (recupera)
Gabi: 5.00 (recupera)
Promedio del curso: 3.50
```

### Misión R03-N06-M3 · El orden del archivo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea de la entrada trae `carpeta archivo contenido`. Creá cada archivo dentro
de `archivo_ciudadela/<carpeta>/` con ese contenido (creando las carpetas que
falten). Después, recorré todo con `recursive_directory_iterator`, y mostrá los
archivos ordenados por tamaño (de mayor a menor; si empatan, por ruta), con la
ruta relativa a la carpeta base. Al final, el total, y borrá todo.

#### Criterio de aprobación

- Usa `fs::create_directories` y el operador `/`.
- Ordena antes de mostrar (el orden del directorio no está garantizado).
- Deja todo limpio con `fs::remove_all`.

#### Entrada de ejemplo

```
planos torre.txt la-torre-del-reloj
planos puente.txt puente
notas hoy.txt revisar-caldera-y-valvulas
planos faro.txt faro
```

#### Salida esperada

```
27	notas/hoy.txt
19	planos/torre.txt
7	planos/puente.txt
5	planos/faro.txt
4 archivos, 58 bytes
¿Quedó algo? no
```

#### Solución de referencia

```cpp
// Mision 3 - El orden del archivo: crear carpetas, listar ordenado por tamanio y limpiar.
#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace fs = std::filesystem;

int main()
{
    const fs::path BASE = "archivo_ciudadela";
    std::string carpeta, nombre, contenido;
    while (std::cin >> carpeta >> nombre >> contenido) {
        fs::create_directories(BASE / carpeta);
        std::ofstream(BASE / carpeta / nombre) << contenido << "\n";
    }
    struct Archivo {
        std::string ruta;
        std::uintmax_t bytes;
    };
    std::vector<Archivo> archivos;
    for (const auto& e : fs::recursive_directory_iterator(BASE)) {
        if (e.is_regular_file()) {
            archivos.push_back({fs::relative(e.path(), BASE).string(), e.file_size()});
        }
    }
    std::sort(archivos.begin(), archivos.end(), [](const Archivo& a, const Archivo& b) {
        return a.bytes != b.bytes ? a.bytes > b.bytes : a.ruta < b.ruta;
    });
    std::uintmax_t total = 0;
    for (const auto& a : archivos) {
        std::cout << a.bytes << "\t" << a.ruta << "\n";
        total += a.bytes;
    }
    std::cout << archivos.size() << " archivos, " << total << " bytes\n";
    fs::remove_all(BASE);
    std::cout << "¿Quedó algo? " << (fs::exists(BASE) ? "sí" : "no") << "\n";
    return 0;
}
```

#### Pruebas

##### Una sola carpeta
```entrada
planos a.txt abc
planos b.txt abc
```
```salida
4	planos/a.txt
4	planos/b.txt
2 archivos, 8 bytes
¿Quedó algo? no
```

##### Archivo vacío y grande
```entrada
x vacio.txt -
y grande.txt muchas-letras-para-un-archivo-grande
```
```salida
37	y/grande.txt
2	x/vacio.txt
2 archivos, 39 bytes
¿Quedó algo? no
```

### Encargo R03-N06-E1 · La configuración del programa

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Muchos programas guardan su configuración en un archivo `clave=valor`. El programa
crea `programa.ini` con `idioma=es`, `volumen=7` y `tema=claro` (y un comentario
que empieza con `#`). Después lo **lee** en un `std::map` (ignorando comentarios y
líneas vacías), aplica los cambios de la entrada (líneas `clave=valor`: decí si
cambia una clave existente o agrega una nueva; las líneas sin `=` se ignoran), lo
vuelve a guardar y muestra el archivo final.

Para mostrar un archivo entero de una vez: `std::cout << in.rdbuf();`.

#### Criterio de aprobación

- Lee y escribe con funciones separadas.
- Ignora comentarios y líneas sin `=`.
- El archivo final queda ordenado por clave (por el `map`).

#### Entrada de ejemplo

```
volumen=10
tema=oscuro
sin igual
fuente=grande
```

#### Salida esperada

```
Cambia volumen
Cambia tema
Ignoro: sin igual
Nueva fuente
--- programa.ini ---
# configuración del programa
fuente=grande
idioma=es
tema=oscuro
volumen=10
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La configuracion del programa: clave=valor en un archivo.
#include <fstream>
#include <iostream>
#include <map>
#include <string>

using Config = std::map<std::string, std::string>;

Config leer(const std::string& ruta)
{
    Config c;
    std::ifstream in(ruta);
    std::string linea;
    while (std::getline(in, linea)) {
        if (linea.empty() || linea[0] == '#') {
            continue;
        }
        std::size_t igual = linea.find('=');
        if (igual != std::string::npos) {
            c[linea.substr(0, igual)] = linea.substr(igual + 1);
        }
    }
    return c;
}

void escribir(const std::string& ruta, const Config& c)
{
    std::ofstream out(ruta);
    out << "# configuración del programa\n";
    for (const auto& [clave, valor] : c) {
        out << clave << "=" << valor << "\n";
    }
}

int main()
{
    const std::string RUTA = "programa.ini";
    escribir(RUTA, {{"idioma", "es"}, {"volumen", "7"}, {"tema", "claro"}});

    Config c = leer(RUTA);
    std::string linea;
    while (std::getline(std::cin, linea)) {
        std::size_t igual = linea.find('=');
        if (igual == std::string::npos) {
            std::cout << "Ignoro: " << linea << "\n";
            continue;
        }
        std::string clave = linea.substr(0, igual);
        std::string valor = linea.substr(igual + 1);
        std::cout << (c.contains(clave) ? "Cambia " : "Nueva ") << clave << "\n";
        c[clave] = valor;
    }
    escribir(RUTA, c);

    std::ifstream in(RUTA);
    std::cout << "--- " << RUTA << " ---\n" << in.rdbuf();
    return 0;
}
```

#### Pruebas

##### Sin cambios
```entrada
```
```salida
--- programa.ini ---
# configuración del programa
idioma=es
tema=claro
volumen=7
```

##### Clave con espacios y valor vacío
```entrada
idioma=en
color=
=sin clave
```
```salida
Cambia idioma
Nueva color
Nueva
--- programa.ini ---
# configuración del programa
=sin clave
color=
idioma=en
tema=claro
volumen=7
```

### Prueba del sello

#### ¿Qué pasa si abrís con `std::ofstream` un archivo que ya existía?

Se vacía. Para agregar al final hay que abrirlo con `std::ios::app`.

#### ¿Cuándo se cierra un `ofstream`?

Cuando la variable deja de existir, al terminar su bloque (o antes, con `close()`).

#### ¿Cómo sabés si un `ifstream` pudo abrir el archivo?

Preguntando `if (!in)`.

#### ¿Qué hace `fs::path("a") / "b.txt"`?

Arma la ruta `a/b.txt` con el separador del sistema.

#### ¿Por qué hay que ordenar lo que devuelve `directory_iterator` antes de mostrarlo?

Porque el orden no está garantizado y cambia según el sistema.

### Soluciones (docente)

Nodo nuevo: FullCursos no tenía un ejemplo de archivos de texto en C++ (solo `04/13-Filesystem` y su uso en el Bestiario). Todos los programas crean y borran sus propios archivos, así corren igual en la compu del alumno y en el súper test.

## R03-N07 · Punteros inteligentes

```meta
tipo: tema
padre: R03-N06
precio: 10
criatura: troll
temas: mem.smart-pointers, mem.dinamica
```

### Crónica

En el depósito de autómatas, cada máquina tiene una etiqueta con el nombre de su **dueño**. Cuando el dueño se va, la máquina vuelve a la fundición. Así nunca quedan máquinas abandonadas ocupando lugar… ni dos personas desarmando la misma.

—En el viejo C++, la memoria se pedía con `new` y se devolvía con `delete`, a mano —dice {mentor}—. Y los trolls se hacían un festín: memoria que nadie devolvía, memoria devuelta dos veces. Hoy cada pedazo de memoria tiene un dueño que la devuelve solo.

### Objetivos

Manejar memoria dinámica sin `new` ni `delete` a mano: `std::unique_ptr` (un solo
dueño), transferir la propiedad con `std::move`, `std::shared_ptr` (varios
dueños, con cuenta de referencias) y `std::weak_ptr` (mirar sin ser dueño).
Elegir entre valor, referencia, `unique_ptr` y `shared_ptr`.

### Antes de empezar

- Polimorfismo y el `unique_ptr` como receta (rama 2).
- Punteros: vistazo (rama 1).

### Explicación

#### El problema: `new` y `delete`
Un objeto puede vivir en la **pila** (una variable normal, que muere al terminar su
bloque) o en la memoria **dinámica** (el *heap*), que se pide y se devuelve a mano:
```cpp
Enemigo* e = new Enemigo("Goblin", 30);   // pedir
...
delete e;                                  // devolver (¡acordarse!)
```
Con `new`/`delete` a mano aparecen tres trolls: la **fuga** (nadie hace `delete`),
la **doble liberación** (dos `delete` del mismo objeto) y el **puntero colgante**
(usar el objeto después del `delete`). Y un `return` temprano o un error en el
medio hacen que el `delete` no llegue a ejecutarse.

**En C++ moderno no se escribe `new` ni `delete`**: se usan punteros inteligentes
(de `<memory>`), que devuelven la memoria solos.

#### `std::unique_ptr<T>`: un solo dueño
```cpp
auto goblin = std::make_unique<Enemigo>("Goblin", 30);  // crea el objeto
goblin->vida -= 10;                                      // se usa como un puntero
if (goblin) { ... }                                      // ¿apunta a algo?
```
Cuando el `unique_ptr` muere (fin del bloque, se borra del vector), **borra el
objeto**. No se puede **copiar** (habría dos dueños), pero sí **mover**:
```cpp
std::unique_ptr<Enemigo> b = std::move(a);   // b es el dueño; a queda vacío (nullptr)
```

#### ¿Cuándo hace falta memoria dinámica?
- **Polimorfismo**: guardar objetos de distintos tipos derivados
  (`std::vector<std::unique_ptr<Figura>>`).
- Objetos que tienen que **sobrevivir** a la función que los crea (una fábrica que
  devuelve `std::unique_ptr<Automata>`).
- Objetos muy grandes, o cuya cantidad se decide al ejecutar.

Si no pasa nada de eso, usá una variable normal o un `std::vector`: también
manejan la memoria solos.

#### Pasar punteros inteligentes a funciones
| La función… | Recibe |
|---|---|
| solo **usa** el objeto | `const T&` (o `T&` si lo modifica). ¡No el `unique_ptr`! |
| usa el objeto, que **puede no estar** | `const T*` (y le pasás `p.get()`) |
| se **queda** con el objeto (pasa a ser la dueña) | `std::unique_ptr<T>` por valor, y se llama con `std::move(p)` |

#### `std::shared_ptr<T>`: varios dueños
```cpp
auto atlas = std::make_shared<Textura>("heroes.png");
Sprite a{"kira", atlas}, b{"bron", atlas};   // copiar un shared_ptr está permitido
atlas.use_count();                           // cuántos dueños hay (3)
atlas.reset();                               // este dueño suelta; el objeto sigue si hay otros
```
El objeto se borra cuando se va **el último** dueño. Sirve cuando varios comparten
algo y no se sabe quién termina último (una textura usada por muchos sprites, una
canción en varias listas). Es más caro que `unique_ptr`: **preferí `unique_ptr`**, y
usá `shared_ptr` solo si la propiedad es realmente compartida.

#### `std::weak_ptr<T>`: mirar sin ser dueño
Un `weak_ptr` apunta a algo manejado por `shared_ptr` **sin** contarse como dueño.
Para usarlo, se pide un `shared_ptr` con `lock()`, que viene vacío si el objeto ya
no existe:
```cpp
std::weak_ptr<Libro> prestado = catalogo[1];
if (auto libro = prestado.lock()) { /* todavía existe */ }
```
Sirve para "conozco a alguien, pero no lo mantengo vivo". También rompe los ciclos
(A tiene un `shared_ptr` a B y B a A: ninguno se borraría nunca).

#### Detectar trolls: el sanitizador
Compilando con `-fsanitize=address -g`, el programa avisa fugas, dobles
liberaciones y usos después de liberar, con el archivo y la línea. Usalo cuando
algo "anda raro".

> **Si venís de C.** `unique_ptr` es un `malloc` con su `free` atado: el `free`
> ocurre solo, en todos los caminos de salida. `shared_ptr` es un contador de
> referencias que en C había que programar a mano.

### Código de ejemplo

```cpp
/*
 * Punteros inteligentes: unique_ptr (un duenio) y shared_ptr (varios duenios).
 */
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

struct Enemigo {
    std::string nombre;
    int vida;

    Enemigo(const std::string& n, int v) : nombre(n), vida(v) { std::cout << "  [+] nace " << nombre << "\n"; }
    ~Enemigo() { std::cout << "  [-] se destruye " << nombre << "\n"; }
};

struct Textura {
    std::string archivo;
    explicit Textura(const std::string& a) : archivo(a) { std::cout << "  [carga " << archivo << "]\n"; }
    ~Textura() { std::cout << "  [libera " << archivo << "]\n"; }
};

struct Sprite {
    std::string nombre;
    std::shared_ptr<Textura> textura;     // varios sprites comparten UNA textura
};

int main()
{
    std::cout << "1) unique_ptr: se libera solo al salir del bloque\n";
    {
        std::unique_ptr<Enemigo> goblin = std::make_unique<Enemigo>("Goblin", 30);
        goblin->vida -= 10;                                   // -> como un puntero
        std::cout << "  " << goblin->nombre << " vida " << goblin->vida << "\n";
    }

    std::cout << "\n2) mover la propiedad con std::move\n";
    auto a = std::make_unique<Enemigo>("Orco", 55);
    std::unique_ptr<Enemigo> b = std::move(a);               // a queda vacio
    std::cout << "  ¿a está vacío? " << std::boolalpha << (a == nullptr) << "; b tiene a " << b->nombre << "\n";

    std::cout << "\n3) un vector de unique_ptr: borrar = destruir\n";
    std::vector<std::unique_ptr<Enemigo>> vivos;
    vivos.push_back(std::make_unique<Enemigo>("Slime", 20));
    vivos.push_back(std::make_unique<Enemigo>("Esqueleto", 25));
    vivos.erase(vivos.begin());
    std::cout << "  quedan " << vivos.size() << "\n";

    std::cout << "\n4) shared_ptr: la textura vive mientras alguien la use\n";
    auto atlas = std::make_shared<Textura>("heroes.png");
    std::vector<Sprite> sprites = {{"kira", atlas}, {"bron", atlas}};
    std::cout << "  dueños: " << atlas.use_count() << "\n";
    atlas.reset();                                            // main la suelta...
    std::cout << "  main soltó su puntero; la textura sigue (la usan 2 sprites)\n";
    sprites.clear();                                          // ...y al irse el ultimo, se libera
    std::cout << "  sprites borrados\n";

    std::cout << "\nFin de main\n";
    return 0;
}   // aca se destruyen b (Orco) y el Esqueleto del vector
```

### Salida esperada

```
1) unique_ptr: se libera solo al salir del bloque
  [+] nace Goblin
  Goblin vida 20
  [-] se destruye Goblin

2) mover la propiedad con std::move
  [+] nace Orco
  ¿a está vacío? true; b tiene a Orco

3) un vector de unique_ptr: borrar = destruir
  [+] nace Slime
  [+] nace Esqueleto
  [-] se destruye Slime
  quedan 1

4) shared_ptr: la textura vive mientras alguien la use
  [carga heroes.png]
  dueños: 3
  main soltó su puntero; la textura sigue (la usan 2 sprites)
  [libera heroes.png]
  sprites borrados

Fin de main
  [-] se destruye Esqueleto
  [-] se destruye Orco
```

### ¿Para qué sirve?

Todo programa grande de C++ maneja objetos cuya vida no coincide con un bloque de código: las entidades de un juego que aparecen y desaparecen, las ventanas de una aplicación, las conexiones de un servidor, los nodos de un árbol. Los punteros inteligentes permiten hacerlo sin fugas de memoria, que en un programa que corre días enteros (un servidor, un juego online) terminan agotando la memoria de la máquina.

### Errores habituales

**Troll: copiar un `unique_ptr`.**
```
main.cpp:2:74: error: use of deleted function ‘std::unique_ptr<_Tp, _Dp>::unique_ptr(const std::unique_ptr<_Tp, _Dp>&) [with _Tp = Enemigo; ...]’
```
"Deleted function" = "esa operación está prohibida a propósito". Usá `std::move`.
En un `v.push_back(p)` el mensaje es más largo (empieza con `no matching function
for call to ‘construct_at’`), pero más abajo aparece el mismo "use of deleted
function".

**Troll: usar un `unique_ptr` después de moverlo.** Queda en `nullptr`: `a->vida`
corta el programa (*Segmentation fault*).

**Troll: doble liberación con `new`/`delete`.** El sanitizador la muestra así:
```
==3299423==ERROR: AddressSanitizer: attempting double-free on 0x502000000010 in thread T0:
    #1 0x5bd9915242ab in main main.cpp:2
```

**Troll: fuga de memoria.**
```
==3299431==ERROR: LeakSanitizer: detected memory leaks
Direct leak of 40 byte(s) in 1 object(s) allocated from:
```

**Troll: guardar el `.get()` de un `unique_ptr` que muere.** El puntero crudo queda
colgando cuando el dueño borra el objeto.

**Ogro: `shared_ptr` en todos lados.** Si todo es compartido, nadie sabe quién es
el dueño, y dos objetos que se apuntan con `shared_ptr` no se liberan nunca (un
ciclo). Usá `unique_ptr` por defecto y `weak_ptr` para "conocer sin ser dueño".

### Misión R03-N07-M1 · La fábrica de autómatas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Automata` abstracta (con `carga()` virtual pura, un nombre y un
`bool roto`), que avisa al construirse ("sale de fábrica") y al destruirse ("a la
chatarra"), con dos derivadas: `Grua` (carga 500) y `Carretilla` (80). Escribí la
fábrica `std::unique_ptr<Automata> fabricar(tipo, nombre)`, que devuelve `nullptr`
si no conoce el tipo. Órdenes de la entrada: `fabricar tipo nombre`, `romper
nombre` y `limpiar` (borra los rotos con `std::erase_if`). Al final, cuántos quedan
y la carga total.

#### Criterio de aprobación

- La fábrica devuelve `unique_ptr` y el `main` lo mueve al vector.
- Borrar del vector destruye el autómata (se ve el mensaje).
- No hay `new` ni `delete`.

#### Entrada de ejemplo

```
fabricar grua Titán
fabricar carretilla Pulga
fabricar dron Zumbido
fabricar carretilla Hormiga
romper Pulga
limpiar
fabricar grua Atlas
```

#### Salida esperada

```
  sale de fábrica: Titán
  sale de fábrica: Pulga
  no sé fabricar "dron"
  sale de fábrica: Hormiga
  a la chatarra: Pulga
  sale de fábrica: Atlas
3 autómatas, carga total 1080
  a la chatarra: Titán
  a la chatarra: Hormiga
  a la chatarra: Atlas
```

#### Solución de referencia

```cpp
// Mision 1 - La fabrica de automatas: una funcion que crea y devuelve unique_ptr.
#include <algorithm>
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

class Automata {
public:
    explicit Automata(const std::string& n) : nombre_(n) { std::cout << "  sale de fábrica: " << nombre_ << "\n"; }
    virtual ~Automata() { std::cout << "  a la chatarra: " << nombre_ << "\n"; }
    virtual int carga() const = 0;
    const std::string& nombre() const { return nombre_; }
    bool roto = false;

private:
    std::string nombre_;
};

class Grua : public Automata {
public:
    using Automata::Automata;
    int carga() const override { return 500; }
};

class Carretilla : public Automata {
public:
    using Automata::Automata;
    int carga() const override { return 80; }
};

// La fabrica: devuelve un duenio del automata nuevo, o nullptr si el tipo no existe.
std::unique_ptr<Automata> fabricar(const std::string& tipo, const std::string& nombre)
{
    if (tipo == "grua") {
        return std::make_unique<Grua>(nombre);
    }
    if (tipo == "carretilla") {
        return std::make_unique<Carretilla>(nombre);
    }
    return nullptr;
}

int main()
{
    std::vector<std::unique_ptr<Automata>> taller;
    std::string orden, tipo, nombre;
    while (std::cin >> orden) {
        if (orden == "fabricar" && std::cin >> tipo >> nombre) {
            auto nuevo = fabricar(tipo, nombre);
            if (nuevo) {
                taller.push_back(std::move(nuevo));
            } else {
                std::cout << "  no sé fabricar \"" << tipo << "\"\n";
            }
        } else if (orden == "romper" && std::cin >> nombre) {
            for (auto& a : taller) {
                if (a->nombre() == nombre) {
                    a->roto = true;
                }
            }
        } else if (orden == "limpiar") {
            std::erase_if(taller, [](const std::unique_ptr<Automata>& a) { return a->roto; });
        }
    }
    int total = 0;
    for (const auto& a : taller) {
        total += a->carga();
    }
    std::cout << taller.size() << " autómatas, carga total " << total << "\n";
    return 0;
}
```

#### Pruebas

##### Romper lo que no existe
```entrada
fabricar grua Uno
romper Dos
limpiar
```
```salida
  sale de fábrica: Uno
1 autómatas, carga total 500
  a la chatarra: Uno
```

##### Romper todos
```entrada
fabricar carretilla A
fabricar carretilla B
romper A
romper B
limpiar
```
```salida
  sale de fábrica: A
  sale de fábrica: B
  a la chatarra: A
  a la chatarra: B
0 autómatas, carga total 0
```

##### Solo tipos desconocidos
```entrada
fabricar robot X
fabricar tren Y
```
```salida
  no sé fabricar "robot"
  no sé fabricar "tren"
0 autómatas, carga total 0
```

### Misión R03-N07-M2 · El traspaso

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hay un depósito con tres paquetes (engranajes, resortes, planos), cada uno en un
`unique_ptr` que avisa cuando se destruye. Pasá al carro el primero y el tercero
con `std::move`, y mostrá el depósito (los lugares vacíos como `(vacío)`).
Inspeccioná los paquetes del carro con una función que recibe `const Paquete&`, y
**entregá** el primero con una función que recibe `std::unique_ptr<Paquete>` por
valor. Observá **cuándo** se destruye cada paquete.

#### Criterio de aprobación

- Distingue la función que mira (`const Paquete&`) de la que se queda con el paquete (`unique_ptr` por valor).
- Usa `std::move` para cada traspaso.

#### Salida esperada

```
Depósito: (vacío) resortes (vacío)
  inspecciono: engranajes
  inspecciono: planos
Entrego el primero del carro:
  entregado: engranajes
  (se destruye el paquete de engranajes)
¿carro[0] vacío? sí
Fin de main:
  (se destruye el paquete de planos)
  (se destruye el paquete de resortes)
```

#### Solución de referencia

```cpp
// Mision 2 - El traspaso: quien es duenio de cada paquete.
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

struct Paquete {
    std::string contenido;
    explicit Paquete(const std::string& c) : contenido(c) {}
    ~Paquete() { std::cout << "  (se destruye el paquete de " << contenido << ")\n"; }
};

// Solo MIRA el paquete: no es duenio.
void inspeccionar(const Paquete& p)
{
    std::cout << "  inspecciono: " << p.contenido << "\n";
}

// Se QUEDA con el paquete: recibe el unique_ptr por valor (hay que moverlo).
void entregar(std::unique_ptr<Paquete> p)
{
    std::cout << "  entregado: " << p->contenido << "\n";
}   // aca se destruye

int main()
{
    std::vector<std::unique_ptr<Paquete>> deposito;
    deposito.push_back(std::make_unique<Paquete>("engranajes"));
    deposito.push_back(std::make_unique<Paquete>("resortes"));
    deposito.push_back(std::make_unique<Paquete>("planos"));

    std::vector<std::unique_ptr<Paquete>> carro;
    carro.push_back(std::move(deposito[0]));        // el deposito[0] queda vacio
    carro.push_back(std::move(deposito[2]));
    std::cout << "Depósito:";
    for (const auto& p : deposito) {
        std::cout << " " << (p ? p->contenido : "(vacío)");
    }
    std::cout << "\n";

    for (const auto& p : carro) {
        inspeccionar(*p);
    }
    std::cout << "Entrego el primero del carro:\n";
    entregar(std::move(carro[0]));
    std::cout << "¿carro[0] vacío? " << (carro[0] == nullptr ? "sí" : "no") << "\n";
    std::cout << "Fin de main:\n";
    return 0;
}
```

### Misión R03-N07-M3 · Las canciones compartidas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Tres canciones (Zamba, Chacarera, Vidala) en `shared_ptr`, que avisan cuando se
borran de la memoria. La lista "Viaje" tiene Zamba y Chacarera; "Fiesta" tiene
Chacarera, Vidala y Zamba. `main` suelta sus punteros con `reset()`. Mostrá las
listas con el `use_count()` de cada canción. Después borrá "Fiesta" y volvé a
mostrar "Viaje"; al final, borrá "Viaje". **Antes de ejecutar**, anotá cuándo se va
a borrar cada canción.

#### Criterio de aprobación

- Usa `std::make_shared` y `use_count()`.
- Cada canción se borra cuando se va su último dueño.

#### Salida esperada

```
(main soltó sus punteros; el número es use_count)
Viaje: Zamba(2) Chacarera(2)
Fiesta: Chacarera(2) Vidala(1) Zamba(2)
Borro la lista Fiesta:
  (se borra "Vidala" de la memoria)
Viaje: Zamba(1) Chacarera(1)
Borro la lista Viaje:
  (se borra "Zamba" de la memoria)
  (se borra "Chacarera" de la memoria)
Fin
```

#### Solución de referencia

```cpp
// Mision 3 - Las canciones compartidas: shared_ptr y use_count.
#include <iostream>
#include <memory>
#include <string>
#include <vector>

struct Cancion {
    std::string titulo;
    explicit Cancion(const std::string& t) : titulo(t) {}
    ~Cancion() { std::cout << "  (se borra \"" << titulo << "\" de la memoria)\n"; }
};

using Lista = std::vector<std::shared_ptr<Cancion>>;

void mostrar(const std::string& nombre, const Lista& lista)
{
    std::cout << nombre << ":";
    for (const auto& c : lista) {
        std::cout << " " << c->titulo << "(" << c.use_count() << ")";
    }
    std::cout << "\n";
}

int main()
{
    auto zamba = std::make_shared<Cancion>("Zamba");
    auto chacarera = std::make_shared<Cancion>("Chacarera");
    auto vidala = std::make_shared<Cancion>("Vidala");

    Lista viaje = {zamba, chacarera};
    Lista fiesta = {chacarera, vidala, zamba};
    zamba.reset();
    chacarera.reset();
    vidala.reset();
    std::cout << "(main soltó sus punteros; el número es use_count)\n";
    mostrar("Viaje", viaje);
    mostrar("Fiesta", fiesta);

    std::cout << "Borro la lista Fiesta:\n";
    fiesta.clear();
    mostrar("Viaje", viaje);
    std::cout << "Borro la lista Viaje:\n";
    viaje.clear();
    std::cout << "Fin\n";
    return 0;
}
```

### Encargo R03-N07-E1 · Los préstamos de la biblioteca

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El catálogo de la biblioteca es un vector de `shared_ptr<Libro>` (Rayuela,
Ficciones, Zama). Cada socio guarda el libro que tiene prestado como
`std::weak_ptr<Libro>`: lo conoce, pero no es su dueño. Ana tiene Ficciones y
Bruno tiene Zama. Mostrá los préstamos (con `lock()`); después dá de baja Zama del
catálogo y volvé a mostrarlos: Bruno tiene que "enterarse" de que su libro ya no
existe.

#### Criterio de aprobación

- Los socios usan `weak_ptr`, no `shared_ptr`.
- El informe usa `lock()` y contempla que el libro ya no exista.

#### Salida esperada

```
Préstamos:
  Ana tiene "Ficciones"
  Bruno tiene "Zama"
Se da de baja "Zama" (se mojó):
  Ana tiene "Ficciones"
  Bruno no tiene nada (o el libro ya no existe)
Libros en catálogo: 2
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Los prestamos de la biblioteca: shared_ptr y weak_ptr.
#include <iostream>
#include <memory>
#include <string>
#include <vector>

struct Libro {
    std::string titulo;
    explicit Libro(const std::string& t) : titulo(t) {}
};

struct Socio {
    std::string nombre;
    std::weak_ptr<Libro> prestado;    // lo tiene, pero no es duenio: si el libro se da de baja, se entera
};

int main()
{
    std::vector<std::shared_ptr<Libro>> catalogo = {
        std::make_shared<Libro>("Rayuela"), std::make_shared<Libro>("Ficciones"), std::make_shared<Libro>("Zama")};
    std::vector<Socio> socios = {{"Ana", {}}, {"Bruno", {}}};
    socios[0].prestado = catalogo[1];
    socios[1].prestado = catalogo[2];

    auto informe = [&socios]() {
        for (const auto& s : socios) {
            if (auto libro = s.prestado.lock()) {       // lock: un shared_ptr si todavia existe
                std::cout << "  " << s.nombre << " tiene \"" << libro->titulo << "\"\n";
            } else {
                std::cout << "  " << s.nombre << " no tiene nada (o el libro ya no existe)\n";
            }
        }
    };
    std::cout << "Préstamos:\n";
    informe();

    std::cout << "Se da de baja \"Zama\" (se mojó):\n";
    catalogo.erase(catalogo.begin() + 2);
    informe();
    std::cout << "Libros en catálogo: " << catalogo.size() << "\n";
    return 0;
}
```

### Prueba del sello

#### ¿Qué hace `std::make_unique<T>(args)`?

Crea un objeto `T` en memoria dinámica con esos argumentos y devuelve un `unique_ptr` que es su dueño.

#### ¿Por qué no se puede copiar un `unique_ptr`? ¿Qué se hace en cambio?

Porque habría dos dueños que borrarían el mismo objeto. Se mueve con `std::move`.

#### ¿Cuándo se borra el objeto de un `shared_ptr`?

Cuando se destruye (o suelta) el último `shared_ptr` que lo apunta.

#### ¿Para qué sirve un `weak_ptr`?

Para conocer un objeto manejado por `shared_ptr` sin mantenerlo vivo; con `lock()` se sabe si todavía existe.

#### Una función que solo muestra un enemigo, ¿qué recibe?

`const Enemigo&`, no el `unique_ptr`.

### Soluciones (docente)

Material original: `04-C++-Moderno/10-UniquePtr` y `11-SharedPtr`, ampliado con `weak_ptr`, cómo pasar punteros inteligentes a funciones y el sanitizador (`-fsanitize=address`).

## R03-N08 · RAII, copias y movimientos

```meta
tipo: tema
padre: R03-N07
precio: 10
criatura: troll
temas: mem.raii, mem.movimiento
```

### Crónica

Cuando un artífice entra a la sala de máquinas, la puerta se traba sola detrás de él. Cuando sale (por la puerta, por la ventana o corriendo porque algo explotó), la puerta se destraba. Nadie tiene que acordarse.

—Esa es la regla más importante de la Ciudadela —dice {mentor}—: todo lo que se toma, se toma **al nacer** un objeto, y se devuelve **al morir**. Así nunca queda nada tomado. Y hay objetos que no se pueden duplicar: una llave maestra se **entrega**, no se copia.

### Objetivos

Entender y escribir clases **RAII** (adquirir en el constructor, soltar en el
destructor); controlar la copia de una clase (`= delete`, `= default`); entender
qué es **mover** un objeto (`std::move`, constructor de movimiento); y conocer la
regla de cero, tres y cinco.

### Antes de empezar

- Constructores y destructores (rama 2).
- Punteros inteligentes y archivos (nodos anteriores).

### Explicación

#### RAII: el recurso vive lo que vive el objeto
**RAII** (*Resource Acquisition Is Initialization*): cada recurso (memoria, un
archivo abierto, una sala cerrada, una conexión) se envuelve en un objeto cuyo
**constructor lo toma** y cuyo **destructor lo suelta**. Como el destructor corre
**siempre** al terminar el bloque (por el final, por un `return` temprano o por un
error), el recurso nunca queda tomado.

Ya lo venís usando: `std::vector` y `std::string` liberan su memoria,
`std::ofstream` cierra su archivo y `std::unique_ptr` borra su objeto. Escribir tus
propias clases RAII es igual de fácil: lo que el constructor toma, el destructor lo
suelta.

#### Copiar un objeto
Cuando escribís `Plano copia = torre;` o pasás un objeto por valor, C++ lo
**copia** con el *constructor de copia*. Si no escribís uno, C++ genera uno que
copia cada miembro. Para la mayoría de las clases, eso está perfecto.

Pero hay objetos que **no deben copiarse**: un candado (dos "abrir" serían un error),
una conexión, un archivo abierto. Se prohíbe así:
```cpp
Candado(const Candado&) = delete;              // no se puede construir una copia
Candado& operator=(const Candado&) = delete;   // ni asignar una copia
```

#### Mover un objeto
**Mover** es "pasarle el contenido a otro objeto, dejando al original vacío pero
válido". Es mucho más barato que copiar: mover un vector de un millón de elementos
solo pasa un puntero, en vez de copiar el millón.
```cpp
Plano movido = std::move(torre);   // torre queda vacío (se puede reasignar o destruir)
```
`std::move` no mueve nada por sí mismo: **marca** el objeto como "podés llevarte
su contenido". El trabajo lo hace el **constructor de movimiento**:
```cpp
Plano(Plano&& otro) noexcept : nombre_(std::move(otro.nombre_)) {}
```
`Plano&&` (dos `&`) es una referencia "a algo que se puede vaciar". `noexcept`
promete que no falla (así `std::vector` lo usa al crecer).

C++ mueve **solo** en muchos casos: al devolver un objeto de una función, al
pasar un temporal (`v.push_back(Plano("puente"))`). Después de `std::move(x)`, no
uses `x` salvo para asignarle otro valor o dejarlo morir.

#### La regla de cero, tres y cinco
Hay cinco funciones especiales: destructor, constructor de copia, asignación de
copia, constructor de movimiento y asignación de movimiento.
- **Regla de cero** (la ideal): si tu clase solo tiene miembros que ya se manejan
  solos (`std::string`, `std::vector`, `std::unique_ptr`), **no escribas ninguna**.
  Las generadas hacen lo correcto.
- **Regla de tres / cinco**: si tuviste que escribir **una** (casi siempre, el
  destructor, porque manejás un recurso a mano), probablemente necesites las
  demás: definilas o prohibilas con `= delete`.

En la práctica: usá miembros que se manejen solos y vas a vivir en la regla de
cero. Las clases RAII propias (un candado, una transacción) suelen prohibir la
copia.

#### `= default`
Pide la versión que generaría el compilador, de forma explícita:
`Plano& operator=(const Plano&) = default;`.

> **Si venís de C.** En C, cada `fopen` necesitaba su `fclose` y cada `malloc` su
> `free`, en **cada** camino de salida. RAII hace que eso sea imposible de olvidar.

### Código de ejemplo

```cpp
/*
 * RAII y copias: un objeto que ADQUIERE algo al nacer y lo SUELTA al morir,
 * y que decide si se puede copiar o solo mover.
 */
#include <iostream>
#include <string>
#include <utility>
#include <vector>

// Una clase RAII: marca la entrada y la salida de una seccion, pase lo que pase.
class Seccion {
public:
    explicit Seccion(const std::string& nombre) : nombre_(nombre) { std::cout << ">> entra: " << nombre_ << "\n"; }
    ~Seccion() { std::cout << "<< sale: " << nombre_ << "\n"; }

    Seccion(const Seccion&) = delete;              // no se copia: dos "salidas" serian un error
    Seccion& operator=(const Seccion&) = delete;

private:
    std::string nombre_;
};

bool guardar(bool falla)
{
    Seccion s("guardar");
    if (falla) {
        std::cout << "   error a mitad de camino\n";
        return false;                          // ~Seccion corre igual
    }
    std::cout << "   guardado completo\n";
    return true;
}

// Una clase que se puede copiar y MOVER, y cuenta lo que pasa.
class Plano {
public:
    explicit Plano(const std::string& nombre) : nombre_(nombre) {}
    Plano(const Plano& otro) : nombre_(otro.nombre_) { std::cout << "   (copia de " << nombre_ << ")\n"; }
    Plano(Plano&& otro) noexcept : nombre_(std::move(otro.nombre_)) { std::cout << "   (mueve " << nombre_ << ")\n"; }
    Plano& operator=(const Plano&) = default;
    Plano& operator=(Plano&&) = default;
    const std::string& nombre() const { return nombre_; }

private:
    std::string nombre_;
};

int main()
{
    {
        Seccion nivel("cargar nivel");
        Seccion enemigos("crear enemigos");
        std::cout << "   ... trabajo ...\n";
    }   // se destruyen al reves: enemigos, despues nivel
    guardar(false);
    guardar(true);

    std::cout << "\nCopiar y mover:\n";
    Plano torre("torre");
    Plano copia = torre;                       // copia: las dos tienen el nombre
    Plano movido = std::move(torre);           // mueve: torre queda vacia (pero valida)
    std::cout << "   torre: \"" << torre.nombre() << "\", copia: \"" << copia.nombre()
              << "\", movido: \"" << movido.nombre() << "\"\n";

    std::vector<Plano> archivo;
    archivo.reserve(2);
    archivo.push_back(Plano("puente"));        // un temporal: se mueve, no se copia
    archivo.push_back(copia);                  // una variable: se copia
    return 0;
}
```

### Salida esperada

```
>> entra: cargar nivel
>> entra: crear enemigos
   ... trabajo ...
<< sale: crear enemigos
<< sale: cargar nivel
>> entra: guardar
   guardado completo
<< sale: guardar
>> entra: guardar
   error a mitad de camino
<< sale: guardar

Copiar y mover:
   (copia de torre)
   (mueve torre)
   torre: "", copia: "torre", movido: "torre"
   (mueve puente)
   (copia de torre)
```

### ¿Para qué sirve?

RAII es la idea que hace que el C++ moderno sea seguro: archivos que se cierran solos, conexiones a bases de datos que se devuelven al terminar, candados de concurrencia que se sueltan aunque haya un error, transacciones que se deshacen si no se confirman, temporizadores que miden cuánto tardó un bloque. Mover objetos es lo que permite devolver vectores y textos enormes de una función sin copiarlos.

### Errores habituales

**Troll: copiar algo que no se debe copiar.** Con la copia prohibida:
```
main.cpp:2:25: error: use of deleted function ‘Candado::Candado(const Candado&)’
main.cpp:1:26: note: declared here
```
Si hace falta pasarlo, se mueve (si la clase lo permite) o se pasa por referencia.

**Troll: la clase con un recurso a mano y sin regla de tres.** Una clase que hace
`new` en el constructor y `delete` en el destructor, pero usa la copia generada:
las dos copias apuntan a lo mismo y el segundo destructor libera algo ya liberado
(doble liberación). Usá `std::unique_ptr` o `std::vector` como miembro, o prohibí
la copia.

**Ogro: usar un objeto después de moverlo.** `std::move(a)` deja a `a` vacío: leerlo
da un valor sin sentido (por ejemplo, un texto vacío).

**Ogro: `std::move` de algo `const`.** `std::move` de un `const` no puede vaciarlo,
así que **copia** en silencio.

**Ogro: el destructor que lanza errores o hace cosas largas.** Un destructor tiene
que ser simple y no fallar: corre en momentos (como la salida por un error) donde
no hay forma de manejar un segundo problema.

### Misión R03-N08-M1 · El registro con sangría

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase RAII `Registro` que al nacer muestra `inicio <tarea>` y al morir
`fin <tarea>`, con una sangría de 2 espacios por nivel de anidamiento (un contador
`static` que sube en el constructor y baja en el destructor). Agregá
`static void nota(texto)` que escribe `- texto` con la sangría actual. Prohibí la
copia. En `main`, un `Registro` del turno; por cada número de la entrada, una
función `procesar(n)` con su propio `Registro`: si es par, anota que se descarta y
**devuelve temprano**; si es impar, anota que se pule. Al final, el total de los
impares.

#### Criterio de aprobación

- El `fin` aparece aunque la función salga con un `return` temprano.
- La copia está prohibida con `= delete`.

#### Entrada de ejemplo

```
3 4 7
```

#### Salida esperada

```
inicio turno
  inicio pieza 3
    - impar: se pule
  fin pieza 3
  inicio pieza 4
    - par: se descarta
  fin pieza 4
  inicio pieza 7
    - impar: se pule
  fin pieza 7
  - total 10
fin turno
```

#### Solución de referencia

```cpp
// Mision 1 - El registro con sangria: RAII con un contador static.
#include <iostream>
#include <string>

class Registro {
public:
    explicit Registro(const std::string& tarea) : tarea_(tarea)
    {
        std::cout << std::string(nivel_ * 2, ' ') << "inicio " << tarea_ << "\n";
        nivel_++;
    }

    ~Registro()
    {
        nivel_--;
        std::cout << std::string(nivel_ * 2, ' ') << "fin " << tarea_ << "\n";
    }

    Registro(const Registro&) = delete;
    Registro& operator=(const Registro&) = delete;

    static void nota(const std::string& texto) { std::cout << std::string(nivel_ * 2, ' ') << "- " << texto << "\n"; }

private:
    inline static int nivel_ = 0;
    std::string tarea_;
};

int procesar(int n)
{
    Registro r("pieza " + std::to_string(n));
    if (n % 2 == 0) {
        Registro::nota("par: se descarta");
        return 0;
    }
    Registro::nota("impar: se pule");
    return n;
}

int main()
{
    Registro r("turno");
    int total = 0;
    int n = 0;
    while (std::cin >> n) {
        total += procesar(n);
    }
    Registro::nota("total " + std::to_string(total));
    return 0;
}
```

#### Pruebas

##### Solo pares
```entrada
2 4 6
```
```salida
inicio turno
  inicio pieza 2
    - par: se descarta
  fin pieza 2
  inicio pieza 4
    - par: se descarta
  fin pieza 4
  inicio pieza 6
    - par: se descarta
  fin pieza 6
  - total 0
fin turno
```

##### Sin piezas
```entrada
```
```salida
inicio turno
  - total 0
fin turno
```

##### Un impar grande
```entrada
101
```
```salida
inicio turno
  inicio pieza 101
    - impar: se pule
  fin pieza 101
  - total 101
fin turno
```

### Misión R03-N08-M2 · El candado de la sala de máquinas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Candado`: el constructor cierra una sala (y avisa si ya estaba
cerrada, con un `static bool`), el destructor la abre. No se puede copiar, pero sí
**mover**: el constructor de movimiento pasa la responsabilidad al nuevo objeto y
deja al viejo "inactivo" (su destructor no abre nada). Escribí `Candado entrar()`,
que cierra la sala, revisa y **devuelve** el candado. Probá un turno con un candado
en un bloque y otro turno con `Candado c = entrar();`.

#### Criterio de aprobación

- La copia está prohibida y el movimiento definido.
- La sala se abre una sola vez, al final del bloque donde vive el candado.

#### Salida esperada

```
Turno 1:
  cierro la sala de máquinas
  ocupada: true
  abro la sala de máquinas
  ocupada: false
Turno 2:
  cierro la sala de máquinas
  (reviso las calderas)
  sigo adentro; ocupada: true
  abro la sala de máquinas
  ocupada: false
```

#### Solución de referencia

```cpp
// Mision 2 - El candado de la sala de maquinas: RAII que no se copia pero si se mueve.
#include <iostream>
#include <string>
#include <utility>

class Candado {
public:
    explicit Candado(const std::string& sala) : sala_(sala)
    {
        if (ocupada_) {
            std::cout << "  ¡" << sala_ << " ya estaba cerrada!\n";
        }
        ocupada_ = true;
        std::cout << "  cierro " << sala_ << "\n";
    }

    Candado(Candado&& otro) noexcept : sala_(std::move(otro.sala_)), activo_(otro.activo_) { otro.activo_ = false; }
    Candado& operator=(Candado&&) = delete;
    Candado(const Candado&) = delete;
    Candado& operator=(const Candado&) = delete;

    ~Candado()
    {
        if (activo_) {
            ocupada_ = false;
            std::cout << "  abro " << sala_ << "\n";
        }
    }

    static bool ocupada() { return ocupada_; }

private:
    inline static bool ocupada_ = false;
    std::string sala_;
    bool activo_ = true;
};

Candado entrar()
{
    Candado c("la sala de máquinas");
    std::cout << "  (reviso las calderas)\n";
    return c;                                  // se MUEVE al que llama
}

int main()
{
    std::cout << "Turno 1:\n";
    {
        Candado c("la sala de máquinas");
        std::cout << "  ocupada: " << std::boolalpha << Candado::ocupada() << "\n";
    }
    std::cout << "  ocupada: " << Candado::ocupada() << "\n";

    std::cout << "Turno 2:\n";
    {
        Candado c = entrar();
        std::cout << "  sigo adentro; ocupada: " << Candado::ocupada() << "\n";
    }
    std::cout << "  ocupada: " << Candado::ocupada() << "\n";
    return 0;
}
```

### Misión R03-N08-M3 · Contar copias y movimientos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Pieza` con las cinco funciones especiales (salvo el destructor), que
suman a dos contadores `static`: `copias` y `movidas`. Después de cada paso, mostrá
cuántas hubo y ponelos en cero:
`Pieza b = a;`, `Pieza c = std::move(a);`, `por_valor(b)`, `por_referencia(b)`, tres
`push_back` (de una variable, de un temporal y de un `std::move`, con `reserve(3)`
antes) y `b = v[0];`. **Antes de ejecutar**, anotá qué esperás en cada paso.

#### Criterio de aprobación

- Los constructores y asignaciones de movimiento son `noexcept`.
- Los resultados muestran que `const&` no copia y que los temporales se mueven.

#### Salida esperada

```
Pieza b = a: 1 copias, 0 movidas
Pieza c = std::move(a): 0 copias, 1 movidas
por_valor(b): 1 copias, 0 movidas
por_referencia(b): 0 copias, 0 movidas
tres push_back: 1 copias, 2 movidas
b = v[0]: 1 copias, 0 movidas
```

#### Solución de referencia

```cpp
// Mision 3 - Contar copias y movimientos.
#include <iostream>
#include <string>
#include <utility>
#include <vector>

class Pieza {
public:
    explicit Pieza(const std::string& n) : nombre_(n) {}
    Pieza(const Pieza& o) : nombre_(o.nombre_) { copias++; }
    Pieza(Pieza&& o) noexcept : nombre_(std::move(o.nombre_)) { movidas++; }
    Pieza& operator=(const Pieza& o)
    {
        nombre_ = o.nombre_;
        copias++;
        return *this;
    }
    Pieza& operator=(Pieza&& o) noexcept
    {
        nombre_ = std::move(o.nombre_);
        movidas++;
        return *this;
    }

    inline static int copias = 0;
    inline static int movidas = 0;

private:
    std::string nombre_;
};

void informe(const std::string& paso)
{
    std::cout << paso << ": " << Pieza::copias << " copias, " << Pieza::movidas << " movidas\n";
    Pieza::copias = 0;
    Pieza::movidas = 0;
}

void por_valor(Pieza) {}
void por_referencia(const Pieza&) {}

int main()
{
    Pieza a("engranaje");
    Pieza b = a;
    informe("Pieza b = a");
    Pieza c = std::move(a);
    informe("Pieza c = std::move(a)");
    por_valor(b);
    informe("por_valor(b)");
    por_referencia(b);
    informe("por_referencia(b)");
    std::vector<Pieza> v;
    v.reserve(3);
    v.push_back(b);
    v.push_back(Pieza("resorte"));
    v.push_back(std::move(c));
    informe("tres push_back");
    b = v[0];
    informe("b = v[0]");
    return 0;
}
```

### Encargo R03-N08-E1 · La transferencia segura

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un banco quiere que una transferencia **nunca** quede a medias. Escribí una clase
RAII `Transferencia`: el constructor mueve el dinero entre dos cuentas (que recibe
por referencia) y el destructor **lo devuelve** si nadie llamó a `confirmar()`.
`transferir(de, a, monto)` crea la transferencia, rechaza si el origen queda en
negativo o si supera $50000 (saliendo sin confirmar), y si no, confirma. Ana
empieza con $30000 y Bruno con $5000; cada número de la entrada es una
transferencia de Ana a Bruno.

#### Criterio de aprobación

- El deshacer está en el destructor, no en cada `return`.
- La copia está prohibida.

#### Entrada de ejemplo

```
10000
25000
60000
20000
```

#### Salida esperada

```
Ana -> Bruno $10000:
  hecha
  Ana: $20000, Bruno: $15000
Ana -> Bruno $25000:
  Ana quedaría en negativo
  (transferencia de $25000 deshecha)
  rechazada
  Ana: $20000, Bruno: $15000
Ana -> Bruno $60000:
  supera el límite diario
  (transferencia de $60000 deshecha)
  rechazada
  Ana: $20000, Bruno: $15000
Ana -> Bruno $20000:
  hecha
  Ana: $0, Bruno: $35000
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La transferencia segura: RAII que deshace si no se confirma.
#include <iostream>
#include <string>

struct Cuenta {
    std::string titular;
    int saldo = 0;
};

class Transferencia {
public:
    Transferencia(Cuenta& origen, Cuenta& destino, int monto)
        : origen_(origen), destino_(destino), monto_(monto)
    {
        origen_.saldo -= monto_;
        destino_.saldo += monto_;
    }

    void confirmar() { confirmada_ = true; }

    ~Transferencia()
    {
        if (!confirmada_) {            // si nadie confirmo, se deshace
            origen_.saldo += monto_;
            destino_.saldo -= monto_;
            std::cout << "  (transferencia de $" << monto_ << " deshecha)\n";
        }
    }

    Transferencia(const Transferencia&) = delete;
    Transferencia& operator=(const Transferencia&) = delete;

private:
    Cuenta& origen_;
    Cuenta& destino_;
    int monto_;
    bool confirmada_ = false;
};

void mostrar(const Cuenta& a, const Cuenta& b)
{
    std::cout << "  " << a.titular << ": $" << a.saldo << ", " << b.titular << ": $" << b.saldo << "\n";
}

bool transferir(Cuenta& de, Cuenta& a, int monto)
{
    Transferencia t(de, a, monto);
    if (monto > 50000) {
        std::cout << "  supera el límite diario\n";
        return false;                  // sale sin confirmar: el destructor deshace
    }
    if (de.saldo < 0) {
        std::cout << "  " << de.titular << " quedaría en negativo\n";
        return false;
    }
    t.confirmar();
    return true;
}

int main()
{
    Cuenta ana{"Ana", 30000};
    Cuenta bruno{"Bruno", 5000};
    int monto = 0;
    while (std::cin >> monto) {
        std::cout << "Ana -> Bruno $" << monto << ":\n";
        std::cout << (transferir(ana, bruno, monto) ? "  hecha\n" : "  rechazada\n");
        mostrar(ana, bruno);
    }
    return 0;
}
```

#### Pruebas

##### Justo todo el saldo
```entrada
30000
```
```salida
Ana -> Bruno $30000:
  hecha
  Ana: $0, Bruno: $35000
```

##### Justo el límite
```entrada
50000
```
```salida
Ana -> Bruno $50000:
  Ana quedaría en negativo
  (transferencia de $50000 deshecha)
  rechazada
  Ana: $30000, Bruno: $5000
```

##### Montos chicos
```entrada
1
2
3
```
```salida
Ana -> Bruno $1:
  hecha
  Ana: $29999, Bruno: $5001
Ana -> Bruno $2:
  hecha
  Ana: $29997, Bruno: $5003
Ana -> Bruno $3:
  hecha
  Ana: $29994, Bruno: $5006
```

### Prueba del sello

#### ¿Qué significa RAII?

Que un recurso se toma en el constructor de un objeto y se suelta en su destructor, así se libera siempre que el objeto muere.

#### ¿Cómo prohibís que una clase se copie?

Declarando el constructor de copia y la asignación de copia con `= delete`.

#### ¿Qué hace `std::move(x)`?

Marca a `x` como "se puede vaciar", para que se use el movimiento en vez de la copia. Después `x` queda vacío pero válido.

#### ¿Qué dice la regla de cero?

Que si una clase solo usa miembros que se manejan solos, no hay que escribir ninguna de las funciones especiales.

#### ¿Por qué mover un vector grande es barato?

Porque se pasa el puntero a sus datos en vez de copiar todos los elementos.

### Soluciones (docente)

Material original: `04-C++-Moderno/12-RAII`, ampliado con copia, movimiento y la regla de cero/tres/cinco (que FullCursos no cubría).

## R03-N09 · Jefe: el Mímico del Bestiario

```meta
tipo: jefe
padre: R03-N08
precio: 10
criatura: dragon
insignia: Sello del Mímico
insignia_descripcion: Venciste al Mímico del Bestiario: dominás el C++ moderno, sus contenedores y su memoria.
usa: col.mapas, mem.smart-pointers, err.opcionales, func.lambdas, arch.texto
```

### Crónica

En la biblioteca de los Talleres se guarda el **Bestiario**: el registro de cada criatura que alguna vez pisó la Ciudadela. Anoche, alguien lo revolvió. Hay fichas rotas, criaturas repetidas… y una que no estaba antes: el **Mímico**, una criatura sin forma propia que copia a cualquiera que mire.

—Para atraparlo, primero hay que ordenar el Bestiario —dice {mentor}—. Y después, entender cómo copia: el Mímico no **es** un lobo. **Tiene** una copia de un lobo. Y esa copia es suya.

### Objetivos

Integrar la rama en un proyecto de varios archivos: `map` con `unique_ptr`,
`optional`, `enum class`, lambdas, archivos, y una copia polimórfica con
`clone()`.

### Antes de empezar

- Toda la rama: `auto`, textos, `map`, `enum class`, `optional`, lambdas,
  archivos, punteros inteligentes y RAII.

### Explicación

#### Cómo se enfrenta este jefe
1. **Empezá por los datos**: el `struct Monstruo` y el `enum class Categoria` con sus
   dos conversiones (a texto y desde texto, que devuelve `optional`).
2. **La clase `Bestiario`** en su `.h` (qué sabe hacer) y su `.cpp` (cómo).
3. **Guardar y cargar**: primero guardar, mirar el archivo con un editor, y recién
   después escribir la carga. La carga tiene que **sobrevivir a líneas rotas**.
4. **El `main`** prueba todo en orden.

#### Copiar algo polimórfico: `clonar()`
Si tenés una `Criatura&` que en realidad es un `Lobo`, ¿cómo hacés una copia? Con
`Criatura copia = original;` se rebana (sale una `Criatura`, que además es
abstracta). La solución clásica es un método virtual que cada clase implementa
copiándose a sí misma:
```cpp
virtual std::unique_ptr<Criatura> clonar() const = 0;               // en la base
std::unique_ptr<Criatura> clonar() const override {                 // en Lobo
    return std::make_unique<Lobo>(*this);                           // copia de un Lobo
}
```
Así, `modelo.clonar()` devuelve una copia del tipo real, con su propio dueño.

#### Validar antes de convertir
`std::stoi` de `"??"` corta el programa. Al cargar un archivo que alguien pudo
editar a mano, validá cada campo **antes** de convertir, y contá las líneas que
ignorás.

### ¿Para qué sirve?

Este proyecto es un pequeño sistema de gestión: un catálogo con búsqueda, filtros, orden y persistencia en disco, tolerante a datos rotos. Es la misma forma que tiene el inventario de un comercio, la lista de pacientes de un consultorio o el catálogo de una biblioteca. La copia polimórfica (`clone`) aparece en editores (duplicar una figura), juegos (duplicar un enemigo) y deshacer/rehacer.

### Errores habituales

**Goblin: `std::stoi` de un campo roto.** Una línea como `Mímico;??;30;Demonio`
corta todo el programa si no validás antes.

**Ogro: `[]` en un `map` const.** `buscar` es `const`: usá `find`.

**Troll: rebanar al copiar.** `Criatura c = *sala[0];` no compila (la base es
abstracta) o rebana. Usá `clonar()`.

**Troll: guardar una referencia a la forma del Mímico y después cambiarla.** Si el
Mímico imita otra criatura, el `unique_ptr` viejo se destruye: una referencia
guardada a la forma anterior queda colgando.

**Esqueleto: el `.cpp` del Bestiario fuera del `CMakeLists.txt`.** "undefined
reference" a todos sus métodos.

### Misión R03-N09-M1 · El Bestiario

```meta
entrega: archivo
entorno: local
monedas: 6
xp: 30
extensiones: zip, cpp, h, txt
```

#### Consigna

Armá el proyecto `Bestiario.h` / `Bestiario.cpp` / `main.cpp` con su
`CMakeLists.txt`:
- `enum class Categoria { Bestia, NoMuerto, Demonio, Humanoide }` con `a_texto` y
  `categoria_desde_texto` (que devuelve `optional`).
- `struct Monstruo` (nombre, vida, ataque, categoría).
- `class Bestiario`, con un `std::map<std::string, std::unique_ptr<Monstruo>>`:
  `agregar` (reemplaza si existe), `buscar` y `mas_peligroso` (devuelven
  `optional`), `por_categoria` (ordenado por vida, de mayor a menor, con una
  lambda), `guardar` y `cargar`.
- El archivo tiene una línea por monstruo: `nombre;vida;ataque;categoria`. `cargar`
  **ignora y cuenta** las líneas con campos de menos, números inválidos o una
  categoría desconocida, y devuelve cuántas ignoró (−1 si no pudo abrir).

El `main` guarda 6 monstruos, agrega 3 líneas rotas al archivo, lo carga en un
bestiario nuevo y consulta. Reproducí la salida esperada.

#### Criterio de aprobación

- El proyecto compila con CMake sin advertencias.
- `cargar` valida antes de convertir y cuenta las líneas ignoradas.
- `buscar` y `mas_peligroso` devuelven `optional`.
- La salida coincide con la esperada.

#### Salida esperada

```
6 monstruos guardados
Cargados 6 (ignoradas 3)

Ficha de Lich:
  Lich [NoMuerto] vida 140, ataque 22
No hay ninguna entrada para Mímico.
El más peligroso: Lich

No muertos:
  Lich [NoMuerto] vida 140, ataque 22
  Esqueleto [NoMuerto] vida 25, ataque 8
Bestias:
  Oso [Bestia] vida 90, ataque 16
  Slime [Bestia] vida 20, ataque 5
```

#### Solución de referencia

```cpp
// ===== Bestiario.h =====
#pragma once

#include <map>
#include <memory>
#include <optional>
#include <string>
#include <vector>

enum class Categoria { Bestia, NoMuerto, Demonio, Humanoide };

std::string a_texto(Categoria c);
std::optional<Categoria> categoria_desde_texto(const std::string& s);

struct Monstruo {
    std::string nombre;
    int vida = 0;
    int ataque = 0;
    Categoria categoria = Categoria::Bestia;
};

class Bestiario {
public:
    void agregar(const Monstruo& m);                           // si ya existe, lo reemplaza
    std::optional<Monstruo> buscar(const std::string& nombre) const;
    std::optional<Monstruo> mas_peligroso() const;             // el de mayor ataque
    std::vector<Monstruo> por_categoria(Categoria c) const;    // ordenados por vida, de mayor a menor
    std::size_t cantidad() const { return monstruos_.size(); }

    bool guardar(const std::string& ruta) const;
    int cargar(const std::string& ruta);                       // devuelve las lineas ignoradas, o -1 si no abre

private:
    std::map<std::string, std::unique_ptr<Monstruo>> monstruos_;
};

// ===== Bestiario.cpp =====
#include "Bestiario.h"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <sstream>

std::string a_texto(Categoria c)
{
    switch (c) {
    case Categoria::Bestia:
        return "Bestia";
    case Categoria::NoMuerto:
        return "NoMuerto";
    case Categoria::Demonio:
        return "Demonio";
    case Categoria::Humanoide:
        return "Humanoide";
    }
    return "?";
}

std::optional<Categoria> categoria_desde_texto(const std::string& s)
{
    for (Categoria c : {Categoria::Bestia, Categoria::NoMuerto, Categoria::Demonio, Categoria::Humanoide}) {
        if (a_texto(c) == s) {
            return c;
        }
    }
    return std::nullopt;
}

void Bestiario::agregar(const Monstruo& m)
{
    monstruos_[m.nombre] = std::make_unique<Monstruo>(m);
}

std::optional<Monstruo> Bestiario::buscar(const std::string& nombre) const
{
    auto it = monstruos_.find(nombre);
    if (it == monstruos_.end()) {
        return std::nullopt;
    }
    return *it->second;
}

std::optional<Monstruo> Bestiario::mas_peligroso() const
{
    auto it = std::max_element(monstruos_.begin(), monstruos_.end(),
                               [](const auto& a, const auto& b) { return a.second->ataque < b.second->ataque; });
    if (it == monstruos_.end()) {
        return std::nullopt;
    }
    return *it->second;
}

std::vector<Monstruo> Bestiario::por_categoria(Categoria c) const
{
    std::vector<Monstruo> r;
    for (const auto& [nombre, m] : monstruos_) {
        if (m->categoria == c) {
            r.push_back(*m);
        }
    }
    std::sort(r.begin(), r.end(), [](const Monstruo& a, const Monstruo& b) { return a.vida > b.vida; });
    return r;
}

bool Bestiario::guardar(const std::string& ruta) const
{
    std::ofstream out(ruta);
    if (!out) {
        return false;
    }
    for (const auto& [nombre, m] : monstruos_) {
        out << m->nombre << ';' << m->vida << ';' << m->ataque << ';' << a_texto(m->categoria) << '\n';
    }
    return true;
}

int Bestiario::cargar(const std::string& ruta)
{
    std::ifstream in(ruta);
    if (!in) {
        return -1;
    }
    monstruos_.clear();
    int ignoradas = 0;
    std::string linea;
    while (std::getline(in, linea)) {
        std::istringstream campos(linea);
        std::string nombre, vida, ataque, cat;
        if (!std::getline(campos, nombre, ';') || !std::getline(campos, vida, ';') ||
            !std::getline(campos, ataque, ';') || !std::getline(campos, cat)) {
            ignoradas++;
            continue;
        }
        auto categoria = categoria_desde_texto(cat);
        bool numeros = !vida.empty() && !ataque.empty() &&
                       std::all_of(vida.begin(), vida.end(), ::isdigit) && std::all_of(ataque.begin(), ataque.end(), ::isdigit);
        if (nombre.empty() || !numeros || !categoria) {
            ignoradas++;
            continue;
        }
        agregar({nombre, std::stoi(vida), std::stoi(ataque), *categoria});
    }
    return ignoradas;
}

// ===== main.cpp =====
#include "Bestiario.h"

#include <filesystem>
#include <fstream>
#include <iostream>

namespace fs = std::filesystem;

void mostrar(const Monstruo& m)
{
    std::cout << "  " << m.nombre << " [" << a_texto(m.categoria) << "] vida " << m.vida << ", ataque " << m.ataque << "\n";
}

void consultar(const Bestiario& b, const std::string& nombre)
{
    if (auto m = b.buscar(nombre)) {
        std::cout << "Ficha de " << nombre << ":\n";
        mostrar(*m);
    } else {
        std::cout << "No hay ninguna entrada para " << nombre << ".\n";
    }
}

int main()
{
    const std::string RUTA = "bestiario.txt";
    {
        Bestiario b;
        b.agregar({"Slime", 20, 5, Categoria::Bestia});
        b.agregar({"Goblin", 35, 9, Categoria::Humanoide});
        b.agregar({"Esqueleto", 25, 8, Categoria::NoMuerto});
        b.agregar({"Lich", 140, 22, Categoria::NoMuerto});
        b.agregar({"Imp", 18, 12, Categoria::Demonio});
        b.agregar({"Oso", 90, 16, Categoria::Bestia});
        b.guardar(RUTA);
        std::cout << b.cantidad() << " monstruos guardados\n";
    }
    // Alguien edito el archivo a mano y dejo lineas rotas
    std::ofstream(RUTA, std::ios::app) << "Mímico;??;30;Demonio\nlinea rota\nDragón;300;40;Dragón\n";

    Bestiario juego;
    int ignoradas = juego.cargar(RUTA);
    std::cout << "Cargados " << juego.cantidad() << " (ignoradas " << ignoradas << ")\n\n";

    consultar(juego, "Lich");
    consultar(juego, "Mímico");
    if (auto peligro = juego.mas_peligroso()) {
        std::cout << "El más peligroso: " << peligro->nombre << "\n";
    }
    std::cout << "\nNo muertos:\n";
    for (const auto& m : juego.por_categoria(Categoria::NoMuerto)) {
        mostrar(m);
    }
    std::cout << "Bestias:\n";
    for (const auto& m : juego.por_categoria(Categoria::Bestia)) {
        mostrar(m);
    }
    fs::remove(RUTA);
    return 0;
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(bestiario CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(bestiario main.cpp Bestiario.cpp)
target_compile_options(bestiario PRIVATE -Wall -Wextra)
```

### Misión R03-N09-M2 · Las copias del Mímico

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

En la sala hay tres criaturas (un vector de `unique_ptr<Criatura>`): un lobo
(vida 40, golpe 9), un gólem (120, 15) y un murciélago (15, 4). `Criatura` es
abstracta, con `nombre()`, `golpe()` y `clonar()` virtuales puros, y `herir(n)`.

El `Mimico` **tiene** una forma (`std::unique_ptr<Criatura>`) que es una **copia
propia**, hecha con `clonar()`. Kira tiene 100 de vida. Órdenes:
- `imitar i`: el Mímico copia a la criatura `i` de la sala (con su vida **actual**);
- `herir i n`: se hiere a la criatura original `i` (la copia no cambia);
- `atacar n`: Kira hiere al Mímico; si no cae, responde con el golpe de su forma.

Si el Mímico cae, termina. Si la entrada se acaba, el Mímico escapa.

#### Criterio de aprobación

- Cada criatura implementa `clonar()` con `make_unique` de su propio tipo.
- Herir al original no cambia la copia del Mímico, ni al revés.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
imitar 1
atacar 30
herir 0 25
imitar 0
atacar 10
herir 0 15
atacar 5
```

#### Salida esperada

```
  el Mímico se transforma en gólem (vida 120)
  Kira golpea al Mímico-gólem: vida 90
  responde con 15 (Kira 85)
  el lobo original queda en 15
  el Mímico se transforma en lobo (vida 15)
  Kira golpea al Mímico-lobo: vida 5
  responde con 9 (Kira 76)
  el lobo original queda en 0
  Kira golpea al Mímico-lobo: vida 0
¡El Mímico cae con forma de lobo!
```

#### Solución de referencia

```cpp
// Jefe R03 - El Mimico: copiar objetos polimorficos con clone().
#include <algorithm>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

class Criatura {
public:
    explicit Criatura(int vida) : vida_(vida) {}
    virtual ~Criatura() = default;
    virtual std::string nombre() const = 0;
    virtual int golpe() const = 0;
    // Copia polimorfica: cada tipo sabe copiarse a si mismo.
    virtual std::unique_ptr<Criatura> clonar() const = 0;
    void herir(int n) { vida_ = std::max(0, vida_ - n); }
    int vida() const { return vida_; }

protected:
    int vida_;
};

class Lobo : public Criatura {
public:
    Lobo() : Criatura(40) {}
    std::string nombre() const override { return "lobo"; }
    int golpe() const override { return 9; }
    std::unique_ptr<Criatura> clonar() const override { return std::make_unique<Lobo>(*this); }
};

class Golem : public Criatura {
public:
    Golem() : Criatura(120) {}
    std::string nombre() const override { return "gólem"; }
    int golpe() const override { return 15; }
    std::unique_ptr<Criatura> clonar() const override { return std::make_unique<Golem>(*this); }
};

class Murcielago : public Criatura {
public:
    Murcielago() : Criatura(15) {}
    std::string nombre() const override { return "murciélago"; }
    int golpe() const override { return 4; }
    std::unique_ptr<Criatura> clonar() const override { return std::make_unique<Murcielago>(*this); }
};

// El Mimico no ES ninguna criatura: TIENE la forma que copio.
class Mimico {
public:
    void imitar(const Criatura& modelo)
    {
        forma_ = modelo.clonar();          // una copia PROPIA: si el modelo cambia, la copia no
        std::cout << "  el Mímico se transforma en " << forma_->nombre() << " (vida " << forma_->vida() << ")\n";
    }

    bool tiene_forma() const { return forma_ != nullptr; }
    Criatura& forma() { return *forma_; }

private:
    std::unique_ptr<Criatura> forma_;
};

int main()
{
    std::vector<std::unique_ptr<Criatura>> sala;
    sala.push_back(std::make_unique<Lobo>());
    sala.push_back(std::make_unique<Golem>());
    sala.push_back(std::make_unique<Murcielago>());

    Mimico mimico;
    int kira = 100;
    std::string orden;
    while (kira > 0 && std::cin >> orden) {
        if (orden == "imitar") {
            std::size_t i = 0;
            std::cin >> i;
            if (i < sala.size()) {
                mimico.imitar(*sala[i]);
            }
        } else if (orden == "herir") {
            std::size_t i = 0;
            int n = 0;
            std::cin >> i >> n;
            if (i < sala.size()) {
                sala[i]->herir(n);
                std::cout << "  el " << sala[i]->nombre() << " original queda en " << sala[i]->vida() << "\n";
            }
        } else if (orden == "atacar" && mimico.tiene_forma()) {
            int n = 0;
            std::cin >> n;
            Criatura& f = mimico.forma();
            f.herir(n);
            std::cout << "  Kira golpea al Mímico-" << f.nombre() << ": vida " << f.vida() << "\n";
            if (f.vida() == 0) {
                std::cout << "¡El Mímico cae con forma de " << f.nombre() << "!\n";
                return 0;
            }
            kira -= f.golpe();
            std::cout << "  responde con " << f.golpe() << " (Kira " << kira << ")\n";
        }
    }
    std::cout << (kira <= 0 ? "Kira cae ante el Mímico.\n" : "El Mímico escapa.\n");
    return 0;
}
```

#### Pruebas

##### Atacar sin forma
```entrada
atacar 10
imitar 2
atacar 20
```
```salida
  el Mímico se transforma en murciélago (vida 15)
  Kira golpea al Mímico-murciélago: vida 0
¡El Mímico cae con forma de murciélago!
```

##### Copia de un lobo muerto
```entrada
herir 0 40
imitar 0
atacar 1
```
```salida
  el lobo original queda en 0
  el Mímico se transforma en lobo (vida 0)
  Kira golpea al Mímico-lobo: vida 0
¡El Mímico cae con forma de lobo!
```

##### Escapa
```entrada
imitar 1
atacar 10
```
```salida
  el Mímico se transforma en gólem (vida 120)
  Kira golpea al Mímico-gólem: vida 110
  responde con 15 (Kira 85)
El Mímico escapa.
```

### Encargo R03-N09-E1 · El inventario del almacén

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

El almacén del barrio necesita un inventario. Escribí `class Almacen` con un
`std::map<std::string, Articulo>` (código → stock, stock mínimo y precio),
`consultar` (devuelve `optional`), `mover(codigo, cantidad)` (positivo entra,
negativo sale; rechaza si no existe o quedaría negativo), `a_reponer()` (los que
están bajo su mínimo), `valor_total()` y `guardar(ruta)` en CSV. Cargá YER (40 u.,
mínimo 10, $2500), AZU (12, 15, $1200) y FID (30, 20, $950). Cada línea de la
entrada es `ver COD`, `entra COD n` o `sale COD n`. Al final, lo que hay que
reponer, el valor del stock y el archivo guardado.

#### Criterio de aprobación

- `consultar` devuelve `optional`.
- Usa una lambda en algún recorrido.
- Guarda el CSV y lo muestra leyéndolo del disco.

#### Entrada de ejemplo

```
ver YER
sale AZU 5
sale FID 15
sale YER 50
entra AZU 10
ver ARR
sale FID 1
```

#### Salida esperada

```
YER: 40 unidades
sale 5 AZU: ok
sale 15 FID: ok
sale 50 YER: rechazado
entra 10 AZU: ok
ARR: no existe
sale 1 FID: ok
A reponer: FID
Valor del stock: $133700
--- stock.csv ---
AZU,17,15,1200
FID,14,20,950
YER,40,10,2500
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El inventario del almacen: map, optional, lambdas y archivo.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <optional>
#include <sstream>
#include <string>
#include <vector>

struct Articulo {
    int stock = 0;
    int minimo = 0;
    double precio = 0;
};

class Almacen {
public:
    void cargar(const std::string& codigo, const Articulo& a) { articulos_[codigo] = a; }

    std::optional<Articulo> consultar(const std::string& codigo) const
    {
        auto it = articulos_.find(codigo);
        if (it == articulos_.end()) {
            return std::nullopt;
        }
        return it->second;
    }

    bool mover(const std::string& codigo, int cantidad)
    {
        auto it = articulos_.find(codigo);
        if (it == articulos_.end() || it->second.stock + cantidad < 0) {
            return false;
        }
        it->second.stock += cantidad;
        return true;
    }

    std::vector<std::string> a_reponer() const
    {
        std::vector<std::string> r;
        for (const auto& [codigo, a] : articulos_) {
            if (a.stock < a.minimo) {
                r.push_back(codigo);
            }
        }
        return r;
    }

    double valor_total() const
    {
        double t = 0;
        for (const auto& [codigo, a] : articulos_) {
            t += a.stock * a.precio;
        }
        return t;
    }

    void guardar(const std::string& ruta) const
    {
        std::ofstream out(ruta);
        for (const auto& [codigo, a] : articulos_) {
            out << codigo << "," << a.stock << "," << a.minimo << "," << a.precio << "\n";
        }
    }

private:
    std::map<std::string, Articulo> articulos_;
};

int main()
{
    Almacen almacen;
    almacen.cargar("YER", {40, 10, 2500});
    almacen.cargar("AZU", {12, 15, 1200});
    almacen.cargar("FID", {30, 20, 950});

    std::string linea;
    while (std::getline(std::cin, linea)) {
        std::istringstream in(linea);
        std::string orden, codigo;
        int cantidad = 0;
        in >> orden >> codigo >> cantidad;
        if (orden == "ver") {
            auto a = almacen.consultar(codigo);
            std::cout << codigo << ": " << (a ? std::to_string(a->stock) + " unidades" : std::string("no existe")) << "\n";
        } else if (orden == "entra" || orden == "sale") {
            int delta = orden == "entra" ? cantidad : -cantidad;
            std::cout << orden << " " << cantidad << " " << codigo << (almacen.mover(codigo, delta) ? ": ok" : ": rechazado") << "\n";
        }
    }
    auto faltan = almacen.a_reponer();
    std::cout << "A reponer:";
    std::for_each(faltan.begin(), faltan.end(), [](const std::string& c) { std::cout << " " << c; });
    std::cout << (faltan.empty() ? " nada" : "") << "\n";
    std::cout << "Valor del stock: $" << almacen.valor_total() << "\n";

    almacen.guardar("stock.csv");
    std::ifstream in("stock.csv");
    std::cout << "--- stock.csv ---\n" << in.rdbuf();
    return 0;
}
```

#### Pruebas

##### Movimientos rechazados
```entrada
sale ZZZ 1
entra ZZZ 1
sale AZU 13
```
```salida
sale 1 ZZZ: rechazado
entra 1 ZZZ: rechazado
sale 13 AZU: rechazado
A reponer: AZU
Valor del stock: $142900
--- stock.csv ---
AZU,12,15,1200
FID,30,20,950
YER,40,10,2500
```

##### Nadie a reponer
```entrada
entra AZU 10
ver AZU
```
```salida
entra 10 AZU: ok
AZU: 22 unidades
A reponer: nada
Valor del stock: $154900
--- stock.csv ---
AZU,22,15,1200
FID,30,20,950
YER,40,10,2500
```

##### Sin movimientos
```entrada
```
```salida
A reponer: AZU
Valor del stock: $142900
--- stock.csv ---
AZU,12,15,1200
FID,30,20,950
YER,40,10,2500
```

### Prueba del sello

#### ¿Por qué `buscar` devuelve `optional<Monstruo>`?

Porque puede no encontrar el monstruo, y el `optional` obliga a quien llama a considerar ese caso.

#### ¿Qué hace el Bestiario con una línea como `Mímico;??;30;Demonio`?

La ignora y la cuenta, porque la vida no es un número. Valida antes de convertir.

#### ¿Por qué hace falta `clonar()` para copiar una `Criatura&`?

Porque copiar por la base rebanaría el objeto (o no compilaría, si es abstracta); `clonar()` copia el tipo real.

#### Si herís al lobo original después de que el Mímico lo copió, ¿cambia el Mímico?

No: el Mímico tiene su propia copia.

#### ¿Quién libera la memoria de los monstruos del Bestiario?

Los `unique_ptr` del `map`, al destruirse el Bestiario. No hay `delete`.

### Soluciones (docente)

Jefe de la rama 3. M1 es `04-C++-Moderno/14-ProyectoBestiario` con los ejercicios del README resueltos (`mas_peligroso`, `cargar` tolerante que cuenta las líneas ignoradas). Se entrega como `.zip`.
