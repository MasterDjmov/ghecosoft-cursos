# RAMA R04 · La Gran Biblioteca: la STL a fondo

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · Plantillas

```meta
tipo: tema
padre: R03-N09
precio: 10
criatura: esqueleto
temas: poo.genericos
```

### Crónica

En lo alto de la Ciudadela está la **Gran Biblioteca**: millones de herramientas ya hechas, probadas por generaciones de artífices. Tesla te lleva hasta la puerta y se detiene.

—Adentro no hay un plano para cada tipo de pieza —dice—. Hay **moldes**: un molde de "caja" sirve para cajas de tornillos, de engranajes o de lo que quieras. Así está hecha toda la biblioteca. Si entendés los moldes, entendés la biblioteca.

### Objetivos

Escribir **plantillas** (*templates*) de funciones y de clases que sirven para
cualquier tipo; entender la deducción de tipos, los parámetros numéricos (como el
`N` de `std::array`) y los requisitos que impone una plantilla; y limitar los
tipos aceptados con **conceptos** de C++20.

### Antes de empezar

- Funciones y sobrecarga (rama 1).
- Clases y operadores (rama 2).

### Explicación

#### El problema
Con sobrecarga, para tener `maximo` de `int`, de `double` y de `std::string` hay
que escribir tres funciones idénticas salvo el tipo. Una **plantilla** es un
molde que escribe esas versiones por vos:
```cpp
template <typename T>
T maximo(T a, T b)
{
    return (a > b) ? a : b;
}
maximo(10, 5);                    // el compilador genera maximo<int>
maximo(3.5, 7.2);                 // genera maximo<double>
maximo<double>(10, 7.2);          // T dicho a mano (10 y 7.2 son de tipos distintos)
```
`T` es un **tipo parámetro**. El compilador lo **deduce** de los argumentos y
genera ("instancia") una versión para cada tipo que uses. Esto pasa **al
compilar**: en el programa final no hay ningún costo.

#### Los requisitos implícitos
`maximo` usa `>`: sirve para cualquier `T` que tenga `>`. Si le pasás un tipo sin
`>`, el error aparece **adentro** de la plantilla. Para tus propios tipos, definí
el operador que la plantilla necesita.

#### Plantillas de clase
```cpp
template <typename T>
class Caja {
public:
    explicit Caja(const T& valor) : valor_(valor) {}
    const T& ver() const { return valor_; }
private:
    T valor_;
};
Caja<int> monedas(100);
Caja<std::string> arma("espada");
```
Así están hechos `std::vector<T>`, `std::map<K, V>` y casi toda la biblioteca. En
las clases el tipo se escribe entre `< >` (aunque en C++17 muchas veces también se
deduce: `Caja c(100);`).

#### Parámetros que no son tipos
```cpp
template <typename T, int N>
class Estante { T items_[N]; ... };
Estante<std::string, 3> estante;
```
`N` es un número conocido al compilar. Así funciona `std::array<int, 5>`.

#### Conceptos (C++20): decir qué tipos sirven
```cpp
template <std::integral T>        // T tiene que ser un entero
bool es_par(T n) { return n % 2 == 0; }
```
Si alguien llama `es_par(2.5)`, el error es claro y aparece en la llamada, no
adentro. `<concepts>` trae `std::integral`, `std::floating_point`,
`std::totally_ordered` y otros; también podés definir los tuyos:
```cpp
template <typename T>
concept Numero = std::integral<T> || std::floating_point<T>;
```

#### Dónde van las plantillas
Una plantilla se escribe **entera en el header** (`.h`), no se separa en `.cpp`:
el compilador necesita ver todo el molde en cada lugar donde se usa.

> **Si venís de C.** En C, lo genérico se hacía con `void*` (perdiendo los
> tipos, como `qsort`) o con macros. Las plantillas son genéricas **y** revisan
> los tipos.

### Código de ejemplo

```cpp
/*
 * Plantillas: funciones y clases que sirven para CUALQUIER tipo.
 */
#include <concepts>
#include <iostream>
#include <string>

// Una plantilla de funcion: T es un "tipo parametro".
template <typename T>
T maximo(T a, T b)
{
    return (a > b) ? a : b;
}

// Dos tipos distintos
template <typename A, typename B>
void mostrar_par(const A& a, const B& b)
{
    std::cout << "(" << a << ", " << b << ")\n";
}

// Un concepto (C++20): T tiene que ser un numero entero.
template <std::integral T>
bool es_par(T n)
{
    return n % 2 == 0;
}

// Una plantilla de clase
template <typename T>
class Caja {
public:
    explicit Caja(const T& valor) : valor_(valor) {}
    const T& ver() const { return valor_; }
    void cambiar(const T& nuevo) { valor_ = nuevo; }

private:
    T valor_;
};

// Un parametro que no es un tipo: la capacidad, conocida al compilar (como std::array)
template <typename T, int N>
class Estante {
public:
    bool guardar(const T& x)
    {
        if (cantidad_ == N) {
            return false;
        }
        items_[cantidad_++] = x;
        return true;
    }
    int cantidad() const { return cantidad_; }
    int capacidad() const { return N; }
    const T& operator[](int i) const { return items_[i]; }

private:
    T items_[N]{};
    int cantidad_ = 0;
};

struct Heroe {
    std::string nombre;
    int nivel = 0;
    bool operator>(const Heroe& otro) const { return nivel > otro.nivel; }   // maximo lo necesita
};

int main()
{
    std::cout << "maximo(10, 5) = " << maximo(10, 5) << "\n";                   // T = int
    std::cout << "maximo(3.5, 7.2) = " << maximo(3.5, 7.2) << "\n";             // T = double
    std::cout << "maximo(\"ana\", \"luz\") = " << maximo(std::string("ana"), std::string("luz")) << "\n";
    std::cout << "maximo<double>(10, 7.2) = " << maximo<double>(10, 7.2) << "\n";   // T explicito
    Heroe kira{"Kira", 5}, lyn{"Lyn", 8};
    std::cout << "Héroe de mayor nivel: " << maximo(kira, lyn).nombre << "\n";

    mostrar_par(1, "uno");
    mostrar_par(std::string("vida"), 99.5);
    std::cout << std::boolalpha << "¿14 es par? " << es_par(14) << "\n";

    Caja<int> monedas(100);
    Caja<std::string> arma("espada");
    monedas.cambiar(monedas.ver() + 50);
    std::cout << "Caja<int>: " << monedas.ver() << ", Caja<string>: " << arma.ver() << "\n";

    Estante<std::string, 3> estante;
    for (const char* cosa : {"plano", "compás", "regla", "lupa"}) {
        std::cout << "guardar " << cosa << ": " << (estante.guardar(cosa) ? "sí" : "lleno") << "\n";
    }
    std::cout << estante.cantidad() << "/" << estante.capacidad() << ", el primero: " << estante[0] << "\n";
    return 0;
}
```

### Salida esperada

```
maximo(10, 5) = 10
maximo(3.5, 7.2) = 7.2
maximo("ana", "luz") = luz
maximo<double>(10, 7.2) = 10
Héroe de mayor nivel: Lyn
(1, uno)
(vida, 99.5)
¿14 es par? true
Caja<int>: 150, Caja<string>: espada
guardar plano: sí
guardar compás: sí
guardar regla: sí
guardar lupa: lleno
3/3, el primero: plano
```

### ¿Para qué sirve?

Toda la biblioteca estándar está hecha de plantillas: contenedores, algoritmos, punteros inteligentes. En tus proyectos las vas a usar para escribir una sola vez utilidades que sirven para muchos tipos: un `Vec2<T>` para enteros y decimales, una `Cache<Clave, Valor>`, un `Pool<Objeto>` para los objetos de un juego, funciones de estadística para cualquier número.

### Errores habituales

**Esqueleto: tipos que no coinciden.** `maximo(10, 7.2)`: ¿`T` es `int` o `double`?
```
main.cpp:2:27: error: no matching function for call to ‘maximo(int, double)’
main.cpp:1:25: note:   template argument deduction/substitution failed:
main.cpp:2:27: note:   deduced conflicting types for parameter ‘T’ (‘int’ and ‘double’)
```
Decíselo: `maximo<double>(10, 7.2)`.

**Goblin: el tipo no tiene lo que la plantilla usa.**
```
main.cpp:3:53: error: no match for ‘operator>’ (operand types are ‘Heroe’ and ‘Heroe’)
```
Los errores de plantillas pueden ser **muy** largos. Buscá la primera línea con
`error:` y la línea **de tu archivo** que dice `required from here`.

**Goblin: el concepto no se cumple.** Con conceptos, el mensaje es más claro:
```
main.cpp:3:26: error: no matching function for call to ‘doble(double)’
note: the expression ‘is_integral_v<_Tp> [with _Tp = double]’ evaluated to ‘false’
```

**Esqueleto: la plantilla separada en un `.cpp`.** Declarada en el `.h` y definida
en otro `.cpp`: da "undefined reference" al enlazar. Las plantillas van enteras en
el header.

### Misión R04-N01-M1 · Utilidades genéricas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí tres plantillas de función: `limitar(x, minimo, maximo)` (que use solo `<`),
`intercambiar(a, b)` (por referencia) y `contar(vector, buscado)`. Probalas con
enteros, decimales y textos: `limitar(150, 0, 100)`, `limitar(-3.5, 0.0, 1.0)`,
`limitar("m", "c", "h")` con `std::string`, intercambiar dos textos y dos
enteros, y contar los 6 de `{3, 6, 6, 1, 6, 2}` y los "sí" de una votación.

#### Criterio de aprobación

- Cada función es una sola plantilla que sirve para todos los tipos.
- `limitar` usa solo `<` (así sirve para más tipos).

#### Salida esperada

```
100 0 h
Bron Kira | 2 1
Seises: 3, síes: 3
```

#### Solución de referencia

```cpp
// Mision 1 - Utilidades genericas: limitar, intercambiar y contar en un vector de cualquier tipo.
#include <iostream>
#include <string>
#include <vector>

template <typename T>
T limitar(const T& x, const T& minimo, const T& maximo)
{
    if (x < minimo) {
        return minimo;
    }
    if (maximo < x) {
        return maximo;
    }
    return x;
}

template <typename T>
void intercambiar(T& a, T& b)
{
    T tmp = a;
    a = b;
    b = tmp;
}

template <typename T>
int contar(const std::vector<T>& v, const T& buscado)
{
    int n = 0;
    for (const auto& x : v) {
        if (x == buscado) {
            n++;
        }
    }
    return n;
}

int main()
{
    std::cout << limitar(150, 0, 100) << " " << limitar(-3.5, 0.0, 1.0) << " "
              << limitar(std::string("m"), std::string("c"), std::string("h")) << "\n";
    std::string a = "Kira", b = "Bron";
    intercambiar(a, b);
    int x = 1, y = 2;
    intercambiar(x, y);
    std::cout << a << " " << b << " | " << x << " " << y << "\n";
    std::vector<int> dados = {3, 6, 6, 1, 6, 2};
    std::vector<std::string> votos = {"sí", "no", "sí", "sí"};
    std::cout << "Seises: " << contar(dados, 6) << ", síes: " << contar(votos, std::string("sí")) << "\n";
    return 0;
}
```

### Misión R04-N01-M2 · El par genérico

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la plantilla de clase `Par<A, B>` con `primero()`, `segundo()` e
`invertido()` (que devuelve un `Par<B, A>`), y un `operator<<` también plantilla
que la muestre como `<a, b>`. Probala con `Par<std::string, int>`, `Par<double,
char>` y un par que tiene otro par adentro.

#### Criterio de aprobación

- `invertido` devuelve un par con los tipos cambiados.
- El `operator<<` es una plantilla y funciona con pares anidados.

#### Salida esperada

```
<Reloj, 12> invertido <12, Reloj>
<9.5, A> invertido <A, 9.5>
<<Reloj, 12>, 1>
```

#### Solución de referencia

```cpp
// Mision 2 - El par generico: una plantilla de clase con dos tipos.
#include <iostream>
#include <string>

template <typename A, typename B>
class Par {
public:
    Par(const A& primero, const B& segundo) : primero_(primero), segundo_(segundo) {}
    const A& primero() const { return primero_; }
    const B& segundo() const { return segundo_; }
    Par<B, A> invertido() const { return Par<B, A>(segundo_, primero_); }

private:
    A primero_;
    B segundo_;
};

template <typename A, typename B>
std::ostream& operator<<(std::ostream& os, const Par<A, B>& p)
{
    return os << "<" << p.primero() << ", " << p.segundo() << ">";
}

int main()
{
    Par<std::string, int> torre("Reloj", 12);
    Par<double, char> nota(9.5, 'A');
    std::cout << torre << " invertido " << torre.invertido() << "\n";
    std::cout << nota << " invertido " << nota.invertido() << "\n";
    Par<Par<std::string, int>, bool> anidado(torre, true);
    std::cout << anidado << "\n";
    return 0;
}
```

### Misión R04-N01-M3 · La pila de capacidad fija

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `template <typename T, int N> class Pila` con un array de `N` elementos:
`apilar` (falso si está llena), `desapilar` (falso si está vacía), `tope`,
`vacia` y `tam`. Con una `Pila<std::string, 3>`, procesá la entrada: `+ cosa`
apila, `-` saca y muestra el tope. Al final, cuántas quedan. Probá también una
`Pila<int, 2>`.

#### Criterio de aprobación

- La capacidad es un parámetro de la plantilla.
- No pasa del límite ni desapila de más.

#### Entrada de ejemplo

```
+ plato
+ vaso
+ taza
+ fuente
-
-
-
-
```

#### Salida esperada

```
apilo plato
apilo vaso
apilo taza
no entra fuente
saco taza
saco vaso
saco plato
no hay nada
Quedan 0
Tope de la pila de números: 7
```

#### Solución de referencia

```cpp
// Mision 3 - La pila con capacidad fija: plantilla de clase con parametro numerico.
#include <iostream>
#include <string>

template <typename T, int N>
class Pila {
public:
    bool apilar(const T& x)
    {
        if (tam_ == N) {
            return false;
        }
        datos_[tam_++] = x;
        return true;
    }

    bool desapilar()
    {
        if (tam_ == 0) {
            return false;
        }
        tam_--;
        return true;
    }

    const T& tope() const { return datos_[tam_ - 1]; }
    bool vacia() const { return tam_ == 0; }
    int tam() const { return tam_; }

private:
    T datos_[N]{};
    int tam_ = 0;
};

int main()
{
    Pila<std::string, 3> platos;
    std::string orden, cosa;
    while (std::cin >> orden) {
        if (orden == "+" && std::cin >> cosa) {
            std::cout << (platos.apilar(cosa) ? "apilo " : "no entra ") << cosa << "\n";
        } else if (orden == "-") {
            if (platos.vacia()) {
                std::cout << "no hay nada\n";
            } else {
                std::cout << "saco " << platos.tope() << "\n";
                platos.desapilar();
            }
        }
    }
    std::cout << "Quedan " << platos.tam() << "\n";
    Pila<int, 2> numeros;
    numeros.apilar(7);
    std::cout << "Tope de la pila de números: " << numeros.tope() << "\n";
    return 0;
}
```

#### Pruebas

##### Desapilar vacía
```entrada
-
+ uno
-
-
```
```salida
no hay nada
apilo uno
saco uno
no hay nada
Quedan 0
Tope de la pila de números: 7
```

##### Llena y queda
```entrada
+ a
+ b
+ c
```
```salida
apilo a
apilo b
apilo c
Quedan 3
Tope de la pila de números: 7
```

##### Sin órdenes
```entrada
```
```salida
Quedan 0
Tope de la pila de números: 7
```

### Encargo R04-N01-E1 · Estadísticas para cualquier número

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La cooperativa quiere estadísticas de sus planillas: socios por mes (enteros),
lluvia en mm (decimales) y visitas a la web (números enormes). Definí un concepto
`Numero` (entero o decimal), una plantilla `struct Estadistica<T>` (mínimo,
máximo, promedio) y `estadistica(const std::vector<T>&)`. Un `informe(titulo,
vector)` muestra todo (o "sin datos" si el vector está vacío).

#### Criterio de aprobación

- Usa un concepto propio para limitar los tipos.
- La misma plantilla sirve para `int`, `double` y `long long`.
- Contempla el vector vacío.

#### Salida esperada

```
Socios: mínimo 118, máximo 151, promedio 132.2
Lluvia: mínimo 0, máximo 33.2, promedio 13.45
Visitas: mínimo 1500000000, máximo 2200000000, promedio 1.85e+09
Nada: sin datos
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Estadisticas para cualquier numero: plantilla con concepto.
#include <concepts>
#include <iostream>
#include <vector>

template <typename T>
concept Numero = std::integral<T> || std::floating_point<T>;

template <Numero T>
struct Estadistica {
    T minimo;
    T maximo;
    double promedio;
};

template <Numero T>
Estadistica<T> estadistica(const std::vector<T>& v)
{
    Estadistica<T> e{v[0], v[0], 0};
    double suma = 0;
    for (T x : v) {
        if (x < e.minimo) {
            e.minimo = x;
        }
        if (x > e.maximo) {
            e.maximo = x;
        }
        suma += x;
    }
    e.promedio = suma / v.size();
    return e;
}

template <Numero T>
void informe(const char* titulo, const std::vector<T>& v)
{
    if (v.empty()) {
        std::cout << titulo << ": sin datos\n";
        return;
    }
    auto [minimo, maximo, promedio] = estadistica(v);
    std::cout << titulo << ": mínimo " << minimo << ", máximo " << maximo << ", promedio " << promedio << "\n";
}

int main()
{
    std::vector<int> socios_por_mes = {120, 132, 118, 140, 151};
    std::vector<double> lluvia_mm = {12.5, 0.0, 33.2, 8.1};
    std::vector<long long> visitas = {1500000000LL, 2200000000LL};
    std::vector<int> vacio;
    informe("Socios", socios_por_mes);
    informe("Lluvia", lluvia_mm);
    informe("Visitas", visitas);
    informe("Nada", vacio);
    return 0;
}
```

### Prueba del sello

#### ¿Qué hace `template <typename T>`?

Declara que lo que sigue es un molde con un tipo parámetro `T`; el compilador genera una versión por cada tipo usado.

#### ¿Por qué `maximo(10, 7.2)` no compila si `maximo` es `T maximo(T, T)`?

Porque `T` no puede ser `int` y `double` a la vez; hay que decirlo: `maximo<double>(10, 7.2)`.

#### ¿Qué es el `N` de `std::array<int, N>`?

Un parámetro de plantilla que no es un tipo: un número conocido al compilar.

#### ¿Para qué sirve un concepto como `std::integral`?

Para limitar qué tipos acepta una plantilla y obtener errores claros si no se cumple.

#### ¿Dónde se escriben las plantillas en un proyecto de varios archivos?

Enteras en el header, porque el compilador necesita el molde completo donde se usa.

### Soluciones (docente)

Material original: `11-STL/01-Plantillas`, con conceptos de C++20.

## R04-N02 · Iteradores

```meta
tipo: tema
padre: R04-N01
precio: 10
criatura: orco
temas: func.iteradores
```

### Crónica

Los bibliotecarios de la Gran Biblioteca no leen los estantes: los **recorren** con un dedo de bronce. El dedo sabe apuntar a un libro, pasar al siguiente y avisar cuando se terminó el estante. No importa si el estante es recto, circular o una pila: el dedo funciona igual.

—Ese dedo se llama **iterador** —dice {mentor}—. Es lo que une los contenedores con los algoritmos. Pero cuidado: si movés los libros mientras el dedo apunta, el dedo queda señalando el aire. Ahí esperan los orcos.

### Objetivos

Entender qué es un iterador y cómo se usa (`*`, `++`, `begin`, `end`); recorrer al
revés y en solo lectura; conocer las categorías de iteradores; usar `advance`,
`distance` y `next`; los iteradores de streams y `back_inserter`; y evitar los
iteradores inválidos al modificar un contenedor.

### Antes de empezar

- Vectores, `begin()`, `end()` y algoritmos básicos (rama 1).
- Plantillas (nodo anterior).

### Explicación

#### Un "dedo" que recorre
Un **iterador** apunta a un elemento de un contenedor:
| Operación | Qué hace |
|---|---|
| `c.begin()` | apunta al primer elemento |
| `c.end()` | apunta **después** del último (no es un elemento: es la marca de fin) |
| `*it` | el elemento apuntado |
| `it->campo` | un campo del elemento |
| `++it` | pasa al siguiente |
| `it == c.end()` | ¿llegó al final? |

El recorrido clásico:
```cpp
for (auto it = v.begin(); it != v.end(); ++it) { std::cout << *it; }
```
El `for` de rango (`for (auto x : v)`) es exactamente eso, escrito corto.

Un **rango** es un par `[ini, fin)`: incluye `ini`, no incluye `fin`. Por eso los
algoritmos reciben `v.begin(), v.end()`, y por eso un rango vacío es `ini == fin`.

#### ¿Por qué iteradores y no índices?
Porque no todos los contenedores tienen índices (una `std::list` o un `std::map`
no tienen `[i]`), pero **todos** tienen iteradores. Una función que recibe
iteradores sirve para cualquier contenedor:
```cpp
template <typename It>
void mostrar(It ini, It fin) { for (It it = ini; it != fin; ++it) std::cout << *it; }
```
Así están escritos todos los algoritmos de `<algorithm>`.

#### Variantes
- `c.rbegin()` / `c.rend()`: recorren **al revés**.
- `c.cbegin()` / `c.cend()`: de **solo lectura** (no dejan modificar).

#### Categorías
No todos los iteradores saben lo mismo:
| Categoría | Además de `++` sabe… | Ejemplos |
|---|---|---|
| *forward* (hacia adelante) | — | `std::forward_list`, `unordered_map` |
| *bidirectional* | `--` | `std::list`, `std::map`, `std::set` |
| *random access* | `it + n`, `it - otro`, `it[n]`, `<` | `std::vector`, `std::deque`, `std::array` |

Por eso `std::sort` (que necesita saltar) no sirve para `std::list`, que trae su
propio `l.sort()`. Para moverse en cualquier categoría:
`std::advance(it, n)`, `std::next(it)`, `std::prev(it)` y
`std::distance(a, b)` (cuántos pasos hay de `a` a `b`).

#### Iteradores especiales (`<iterator>`)
- `std::back_inserter(v)`: al "escribir" en él, hace `push_back`.
- `std::ostream_iterator<int>(std::cout, " ")`: escribir en él muestra en pantalla.
- `std::istream_iterator<int>(std::cin)`: lee números de un stream; el iterador
  vacío `std::istream_iterator<int>{}` marca el fin. Leer todos los números de la
  entrada en un vector es una línea.

#### Iteradores inválidos
Si modificás un contenedor, algunos iteradores **dejan de valer**:
- en un `vector`, un `push_back` puede mudar todos los elementos: **todos** los
  iteradores quedan inválidos; un `erase` invalida desde el borrado en adelante;
- en una `list` o un `map`, solo se invalida el del elemento borrado.

Para borrar mientras se recorre, `erase` **devuelve** el iterador al siguiente:
```cpp
for (auto it = v.begin(); it != v.end(); ) {
    if (hay_que_borrar(*it)) it = v.erase(it);
    else ++it;
}
```

> **Si venís de C.** Un iterador de `vector` se usa como un puntero a un array
> (`*p`, `p++`, `p + 3`). La idea generaliza el puntero a cualquier contenedor.

### Código de ejemplo

```cpp
/*
 * Iteradores: el "dedo" que recorre cualquier contenedor.
 */
#include <algorithm>
#include <iostream>
#include <iterator>
#include <list>
#include <numeric>
#include <sstream>
#include <vector>

// Una funcion que recibe un RANGO [ini, fin): sirve para cualquier contenedor.
template <typename It>
void mostrar(It ini, It fin)
{
    for (It it = ini; it != fin; ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";
}

int main()
{
    std::vector<int> v = {5, 2, 8, 1, 9, 3};
    std::list<char> l = {'g', 'e', 'c', 'o'};

    std::cout << "a mano:    ";
    for (auto it = v.begin(); it != v.end(); ++it) {      // begin: el primero; end: DESPUES del ultimo
        std::cout << *it << " ";                           // *it: el elemento
    }
    std::cout << "\n";
    std::cout << "vector:    ";
    mostrar(v.begin(), v.end());
    std::cout << "list:      ";
    mostrar(l.begin(), l.end());
    std::cout << "al revés:  ";
    mostrar(v.rbegin(), v.rend());
    std::cout << "del 2 al 4: ";
    mostrar(v.begin() + 1, v.begin() + 4);                 // random access: se puede sumar

    auto it = l.begin();
    std::advance(it, 2);                                    // en una list se avanza de a uno
    std::cout << "3.º de la list: " << *it << ", distancia total: " << std::distance(l.begin(), l.end()) << "\n";
    std::cout << "siguiente del primero: " << *std::next(v.begin()) << "\n";

    // Los algoritmos reciben iteradores: por eso sirven para cualquier contenedor
    auto mayor = std::max_element(v.begin(), v.end());
    std::cout << "el mayor es " << *mayor << " en la posición " << std::distance(v.begin(), mayor) << "\n";

    // Iteradores "raros": escribir a la salida y leer de un texto
    std::cout << "con ostream_iterator: ";
    std::copy(v.begin(), v.end(), std::ostream_iterator<int>(std::cout, ","));
    std::cout << "\n";
    std::istringstream entrada("10 20 30 40");
    std::vector<int> leidos(std::istream_iterator<int>(entrada), std::istream_iterator<int>{});
    std::cout << "leídos: " << leidos.size() << ", suma " << std::accumulate(leidos.begin(), leidos.end(), 0) << "\n";

    // back_inserter: en vez de pisar, agrega con push_back
    std::vector<int> pares;
    std::copy_if(v.begin(), v.end(), std::back_inserter(pares), [](int x) { return x % 2 == 0; });
    std::cout << "pares: ";
    mostrar(pares.cbegin(), pares.cend());                  // cbegin/cend: solo lectura
    return 0;
}
```

### Salida esperada

```
a mano:    5 2 8 1 9 3 
vector:    5 2 8 1 9 3 
list:      g e c o 
al revés:  3 9 1 8 2 5 
del 2 al 4: 2 8 1 
3.º de la list: c, distancia total: 4
siguiente del primero: 2
el mayor es 9 en la posición 4
con ostream_iterator: 5,2,8,1,9,3,
leídos: 4, suma 100
pares: 2 8 
```

### ¿Para qué sirve?

Los iteradores son la forma en que todo el código genérico de C++ recorre datos: algoritmos, rangos, bibliotecas de terceros. Saber usarlos te deja escribir funciones que sirven para cualquier contenedor, leer y escribir datos de archivos y streams con una línea, y evitar uno de los errores más comunes y difíciles de encontrar: usar un iterador después de modificar el contenedor.

### Errores habituales

**Orco: `*v.end()`.** `end()` no es un elemento: desreferenciarlo es comportamiento
indefinido. Lo mismo `*v.begin()` en un vector vacío.

**Orco: usar un iterador después de modificar el vector.** Un `push_back` dentro
de un recorrido con iteradores del mismo vector. El sanitizador lo muestra así:
```
==3314202==ERROR: AddressSanitizer: heap-use-after-free on address 0x502000000018
READ of size 4 at 0x502000000018 thread T0
```

**Orco: borrar y seguir con `++it`.** Después de `v.erase(it)`, `it` no vale.
Usá `it = v.erase(it);` y **no** avances en esa vuelta.

**Esqueleto: `std::sort` sobre una `list`.** Necesita iteradores de acceso
aleatorio; el error es enorme, pero dice:
```
error: no match for ‘operator-’ (operand types are ‘std::_List_iterator<int>’ and ‘std::_List_iterator<int>’)
```
Usá `lista.sort()`.

**Ogro: mezclar iteradores de dos contenedores.** `std::find(a.begin(), b.end(), x)`
compila y recorre memoria ajena. Los dos extremos del rango, del mismo contenedor.

### Misión R04-N02-M1 · Recorrer a mano

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí dos plantillas que reciben un rango de iteradores: `buscar(ini, fin, x)`
(devuelve el iterador al primero igual a `x`, o `fin`) y `mostrar_al_reves(ini,
fin)` (solo con `--`, sin `rbegin`). Probalas con un `vector<int>` y con una
`list<std::string>`. Con el vector, mostrá la posición calculando `it - begin`.

#### Criterio de aprobación

- Las funciones solo usan `*`, `++`, `--`, `==` y `!=`.
- Funcionan con `vector` y con `list`.

#### Salida esperada

```
16 está en la posición 3
Faro está
7 no está
42 23 16 15 8 4 
Vapor Faro Reloj Norte 
```

#### Solución de referencia

```cpp
// Mision 1 - Recorrer a mano: buscar, contar y dar vuelta un rango con iteradores.
#include <iostream>
#include <list>
#include <string>
#include <vector>

template <typename It, typename T>
It buscar(It ini, It fin, const T& x)
{
    for (It it = ini; it != fin; ++it) {
        if (*it == x) {
            return it;
        }
    }
    return fin;
}

template <typename It>
void mostrar_al_reves(It ini, It fin)
{
    while (fin != ini) {
        --fin;
        std::cout << *fin << " ";
    }
    std::cout << "\n";
}

int main()
{
    std::vector<int> numeros = {4, 8, 15, 16, 23, 42};
    std::list<std::string> torres = {"Norte", "Reloj", "Faro", "Vapor"};

    auto a = buscar(numeros.begin(), numeros.end(), 16);
    if (a != numeros.end()) {
        std::cout << "16 está en la posición " << (a - numeros.begin()) << "\n";
    }
    auto b = buscar(torres.begin(), torres.end(), std::string("Faro"));
    std::cout << (b != torres.end() ? "Faro está" : "Faro no está") << "\n";
    std::cout << (buscar(numeros.begin(), numeros.end(), 7) == numeros.end() ? "7 no está" : "7 está") << "\n";
    mostrar_al_reves(numeros.begin(), numeros.end());
    mostrar_al_reves(torres.begin(), torres.end());
    return 0;
}
```

### Misión R04-N02-M2 · La tubería de números

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé **todos** los números de la entrada en un vector con `std::istream_iterator`
(una sola línea de código). Copiá los positivos a otro vector con `copy_if` y
`back_inserter`, ordenalos y mostralos con `std::ostream_iterator`, primero de
menor a mayor y después de mayor a menor (con `rbegin`/`rend`).

#### Criterio de aprobación

- Lee con `istream_iterator` y escribe con `ostream_iterator`.
- Usa `back_inserter` y los iteradores inversos.

#### Entrada de ejemplo

```
12 -4 7 0 33 -8 5 7
```

#### Salida esperada

```
Leí 8 números
Positivos ordenados: 5 7 7 12 33 
De mayor a menor: 33 12 7 7 5 
```

#### Solución de referencia

```cpp
// Mision 2 - La tubería de numeros: leer con istream_iterator y escribir con ostream_iterator.
#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>

int main()
{
    std::vector<int> datos(std::istream_iterator<int>(std::cin), std::istream_iterator<int>{});
    std::cout << "Leí " << datos.size() << " números\n";

    std::vector<int> positivos;
    std::copy_if(datos.begin(), datos.end(), std::back_inserter(positivos), [](int x) { return x > 0; });
    std::sort(positivos.begin(), positivos.end());

    std::cout << "Positivos ordenados: ";
    std::copy(positivos.begin(), positivos.end(), std::ostream_iterator<int>(std::cout, " "));
    std::cout << "\nDe mayor a menor: ";
    std::copy(positivos.rbegin(), positivos.rend(), std::ostream_iterator<int>(std::cout, " "));
    std::cout << "\n";
    return 0;
}
```

#### Pruebas

##### Sin positivos
```entrada
-1 -2 0
```
```salida
Leí 3 números
Positivos ordenados:
De mayor a menor:
```

##### Uno solo
```entrada
42
```
```salida
Leí 1 números
Positivos ordenados: 42
De mayor a menor: 42
```

##### Vacía
```entrada
```
```salida
Leí 0 números
Positivos ordenados:
De mayor a menor:
```

### Misión R04-N02-M3 · Borrar sin perder el dedo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Con iteradores explícitos (sin `erase_if`):
1. De `{5, 12, 7, 20, 3, 30}` borrá los mayores o iguales a 10.
2. De la `list` `{Kira, Bron, Lyn, Bron, Oto}` borrá los "Bron" y agregale un `!` a
   los demás.
3. En `{1, 2, 3, 4}` insertá un 0 delante de cada par.

Usá lo que devuelven `erase` e `insert` para no quedarte con un iterador inválido.

#### Criterio de aprobación

- Usa `it = c.erase(it)` y no avanza en esa vuelta.
- Usa el iterador que devuelve `insert`.
- No hay iteradores inválidos (probalo con `-fsanitize=address`).

#### Salida esperada

```
5 7 3 
Kira! Lyn! Oto! 
1 0 2 3 0 4 
```

#### Solución de referencia

```cpp
// Mision 3 - Borrar mientras se recorre, bien hecho: erase devuelve el siguiente iterador.
#include <iostream>
#include <list>
#include <string>
#include <vector>

template <typename C>
void mostrar(const C& c)
{
    for (const auto& x : c) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}

int main()
{
    std::vector<int> v = {5, 12, 7, 20, 3, 30};
    for (auto it = v.begin(); it != v.end();) {
        if (*it >= 10) {
            it = v.erase(it);          // erase devuelve el siguiente valido
        } else {
            ++it;                      // solo se avanza si no se borro
        }
    }
    mostrar(v);

    std::list<std::string> cola = {"Kira", "Bron", "Lyn", "Bron", "Oto"};
    for (auto it = cola.begin(); it != cola.end();) {
        if (*it == "Bron") {
            it = cola.erase(it);
        } else {
            *it += "!";
            ++it;
        }
    }
    mostrar(cola);

    // insertar delante de cada numero par, sin perder el iterador
    std::vector<int> w = {1, 2, 3, 4};
    for (auto it = w.begin(); it != w.end(); ++it) {
        if (*it % 2 == 0) {
            it = w.insert(it, 0);      // insert devuelve el iterador al insertado
            ++it;                      // volver al par
        }
    }
    mostrar(w);
    return 0;
}
```

### Encargo R04-N02-E1 · Los turnos de la mañana y la tarde

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La primera línea trae los números de cliente atendidos a la mañana; la segunda,
los de la tarde. Leé cada línea en un vector (con `istringstream` e
`istream_iterator`), ordenalos, unilos en uno solo ordenado con `std::merge`
(usando `back_inserter`), mostralo, y después quitá los repetidos con
`std::unique` + `erase`. Mostrá cuántos clientes distintos hubo.

#### Criterio de aprobación

- Usa `std::merge` sobre rangos ordenados.
- Usa `std::unique` y borra lo que devuelve hasta `end()`.

#### Entrada de ejemplo

```
104 12 57 33 12
57 8 200 104
```

#### Salida esperada

```
Unidos: 8 12 12 33 57 57 104 104 200 
Sin repetir: 8 12 33 57 104 200 
6 clientes distintos
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Fusionar dos listas ordenadas de turnos (merge) sin repetir.
#include <algorithm>
#include <iostream>
#include <iterator>
#include <sstream>
#include <string>
#include <vector>

std::vector<int> leer_linea()
{
    std::string linea;
    std::getline(std::cin, linea);
    std::istringstream in(linea);
    return std::vector<int>(std::istream_iterator<int>(in), std::istream_iterator<int>{});
}

int main()
{
    std::vector<int> manana = leer_linea();
    std::vector<int> tarde = leer_linea();
    std::sort(manana.begin(), manana.end());
    std::sort(tarde.begin(), tarde.end());

    std::vector<int> todos;
    std::merge(manana.begin(), manana.end(), tarde.begin(), tarde.end(), std::back_inserter(todos));
    std::cout << "Unidos: ";
    std::copy(todos.begin(), todos.end(), std::ostream_iterator<int>(std::cout, " "));

    auto fin = std::unique(todos.begin(), todos.end());   // corre los repetidos al final
    todos.erase(fin, todos.end());
    std::cout << "\nSin repetir: ";
    std::copy(todos.begin(), todos.end(), std::ostream_iterator<int>(std::cout, " "));
    std::cout << "\n" << todos.size() << " clientes distintos\n";
    return 0;
}
```

#### Pruebas

##### Sin repetidos
```entrada
1 3 5
2 4 6
```
```salida
Unidos: 1 2 3 4 5 6
Sin repetir: 1 2 3 4 5 6
6 clientes distintos
```

##### Todos iguales
```entrada
7 7 7
7 7
```
```salida
Unidos: 7 7 7 7 7
Sin repetir: 7
1 clientes distintos
```

### Prueba del sello

#### ¿A qué apunta `v.end()`?

A la posición después del último elemento; no es un elemento y no se puede desreferenciar.

#### ¿Por qué los algoritmos reciben iteradores y no el contenedor?

Porque así sirven para cualquier contenedor (y para partes de un contenedor).

#### ¿Por qué `std::sort` no funciona con `std::list`?

Porque necesita iteradores de acceso aleatorio y los de `list` son bidireccionales. `list` trae su propio `sort()`.

#### ¿Qué pasa con los iteradores de un vector después de un `push_back`?

Pueden quedar todos inválidos, porque el vector puede mudarse a otra memoria.

#### ¿Cómo se borra correctamente mientras se recorre?

Con `it = c.erase(it);` y sin avanzar en esa vuelta.

### Soluciones (docente)

Material original: `11-STL/02-Iteradores` y la parte de iteradores invalidados de `11-STL/13-Errores-Buenas-Practicas`.

## R04-N03 · Pilas, colas y otras secuencias

```meta
tipo: tema
padre: R04-N02
precio: 10
criatura: ogro
temas: col.pilas-colas
```

### Crónica

En el depósito de la Biblioteca hay estantes de todas las formas: uno largo y recto, otro donde se agrega y se saca por las dos puntas, una torre de platos donde solo se toca el de arriba, y una fila de carretillas que se atienden en orden de llegada.

—Cada forma de guardar sirve para algo —dice {mentor}—. Si solo necesitás el de arriba, no uses un estante entero: usá una **pila**. Elegir la estructura correcta es la mitad del problema resuelto.

### Objetivos

Conocer los contenedores de secuencia además de `vector` (`deque`, `list`) y
saber cuándo usar cada uno, y usar los **adaptadores**: `std::stack` (pila),
`std::queue` (cola) y `std::priority_queue` (cola con prioridad), con
comparadores propios.

### Antes de empezar

- Vectores e iteradores (nodos anteriores).
- Operadores para tus clases (rama 2).

### Explicación

#### Las secuencias
| Contenedor | Bueno para | Malo para |
|---|---|---|
| `std::vector` | casi todo: acceso por índice, recorrer, agregar al final | insertar o borrar al principio o en el medio |
| `std::deque` | agregar y sacar **por los dos extremos** (`push_front`, `push_back`) | — (un poco más lento que vector para recorrer) |
| `std::list` | insertar y borrar en el medio **si ya tenés el iterador** | acceso por índice (no tiene `[]`), recorrer (es lenta) |
| `std::array` | tamaño fijo | crecer |

**Regla práctica: usá `vector`.** Cambiá solo si tenés un motivo claro (necesitás
el frente: `deque`) o si mediste que otro es más rápido en tu caso. "Uso `list`
porque inserto mucho" casi siempre es un mito: el `vector` gana porque sus datos
están juntos en la memoria, y el procesador los lee mucho más rápido.

#### Los adaptadores: menos operaciones, más claridad
Un adaptador es una interfaz **recortada** sobre otro contenedor: solo deja hacer
lo que tiene sentido para esa estructura. No tienen iteradores (no se recorren con
`for`): se sacan elementos de a uno.

**`std::stack` (pila, LIFO: el último que entra es el primero que sale)**
```cpp
std::stack<std::string> deshacer;
deshacer.push("mover");      // apilar
deshacer.top();              // mirar el de arriba
deshacer.pop();              // sacar el de arriba (¡no lo devuelve!)
```
Sirve para deshacer, para revisar paréntesis, para volver sobre tus pasos.

**`std::queue` (cola, FIFO: el primero que entra es el primero que sale)**
```cpp
std::queue<std::string> fila;
fila.push("Kira");   fila.front();   fila.back();   fila.pop();
```
Sirve para turnos, pedidos, tareas pendientes, recorridos "por niveles".

**`std::priority_queue` (siempre sale el mayor)**
```cpp
std::priority_queue<int> danos;                                        // sale el mayor
std::priority_queue<int, std::vector<int>, std::greater<int>> cerca;   // sale el menor
```
Con un tipo propio, usa su `operator<` (sale el "mayor" según ese orden), o se le
pasa un **comparador** como tercer parámetro: un `struct` con un `operator()` que
recibe dos elementos y dice si el primero tiene **menos** prioridad que el segundo.

Los tres: `empty()`, `size()`, y **`pop()` no devuelve el elemento** (primero se
mira con `top()`/`front()`, después se saca).

> **Si venís de C.** Pilas y colas se programaban a mano con arrays o listas
> enlazadas. Acá vienen hechas, y el `deque` evita escribir un buffer circular.

### Código de ejemplo

```cpp
/*
 * Contenedores de secuencia (vector, deque, list) y adaptadores (stack, queue, priority_queue).
 */
#include <deque>
#include <functional>   // std::greater
#include <iostream>
#include <list>
#include <queue>
#include <stack>
#include <string>
#include <vector>

struct Tarea {
    std::string nombre;
    int prioridad = 0;
    bool operator<(const Tarea& o) const { return prioridad < o.prioridad; }   // la de mayor sale primero
};

int main()
{
    // deque: agregar y sacar rapido por LOS DOS extremos
    std::deque<int> d = {3, 4};
    d.push_front(2);
    d.push_front(1);
    d.push_back(5);
    std::cout << "deque:";
    for (int x : d) {
        std::cout << " " << x;
    }
    std::cout << " (primero " << d.front() << ", d[2] = " << d[2] << ")\n";

    // list: insertar y borrar en el medio sin mover a los demas (pero sin [])
    std::list<std::string> ronda = {"Kira", "Lyn"};
    auto it = ronda.begin();
    ++it;
    ronda.insert(it, "Bron");                 // antes de Lyn
    ronda.push_front("Tesla");
    ronda.sort();                             // la list trae su propio sort
    std::cout << "list:";
    for (const auto& n : ronda) {
        std::cout << " " << n;
    }
    std::cout << "\n";

    // stack: pila, el ultimo que entra es el primero que sale (LIFO)
    std::stack<std::string> deshacer;
    deshacer.push("mover");
    deshacer.push("abrir cofre");
    deshacer.push("beber poción");
    std::cout << "deshaciendo:";
    while (!deshacer.empty()) {
        std::cout << " [" << deshacer.top() << "]";   // top: mirar
        deshacer.pop();                               // pop: sacar (no devuelve nada)
    }
    std::cout << "\n";

    // queue: cola, el primero que entra es el primero que sale (FIFO)
    std::queue<std::string> turnos;
    for (const char* q : {"Kira", "Goblin", "Lyn"}) {
        turnos.push(q);
    }
    std::cout << "turnos:";
    for (int i = 0; i < 5; i++) {
        std::string quien = turnos.front();
        turnos.pop();
        std::cout << " " << quien;
        turnos.push(quien);                            // vuelve al final: una ronda
    }
    std::cout << "\n";

    // priority_queue: siempre sale el MAYOR (o el menor, con std::greater)
    std::priority_queue<int> danos;
    for (int x : {20, 5, 42, 13}) {
        danos.push(x);
    }
    std::cout << "daños de mayor a menor:";
    while (!danos.empty()) {
        std::cout << " " << danos.top();
        danos.pop();
    }
    std::priority_queue<int, std::vector<int>, std::greater<int>> distancias;
    for (int x : {7, 2, 9, 4}) {
        distancias.push(x);
    }
    std::cout << "\nel enemigo más cercano está a " << distancias.top() << "\n";

    std::priority_queue<Tarea> pendientes;
    pendientes.push({"curar a un aliado", 5});
    pendientes.push({"huir", 9});
    pendientes.push({"juntar botín", 1});
    std::cout << "orden de atención:";
    while (!pendientes.empty()) {
        std::cout << " " << pendientes.top().nombre;
        pendientes.pop();
    }
    std::cout << "\n";
    return 0;
}
```

### Salida esperada

```
deque: 1 2 3 4 5 (primero 1, d[2] = 3)
list: Bron Kira Lyn Tesla
deshaciendo: [beber poción] [abrir cofre] [mover]
turnos: Kira Goblin Lyn Kira Goblin
daños de mayor a menor: 42 20 13 5
el enemigo más cercano está a 2
orden de atención: huir curar a un aliado juntar botín
```

### ¿Para qué sirve?

Las pilas están en el "deshacer" de cualquier editor, en el botón "atrás" del navegador y en los compiladores (para revisar paréntesis). Las colas, en cualquier sistema de turnos, en la impresora, en los pedidos de un restaurante y en los mensajes entre programas. La cola con prioridad ordena las urgencias de una guardia médica, los eventos de un simulador o las tareas de un sistema operativo, y está en el corazón de los algoritmos de caminos más cortos (como el GPS).

### Errores habituales

**Goblin: esperar que `pop()` devuelva algo.**
```
main.cpp:2:57: error: void value not ignored as it ought to be
```
Primero `top()` (o `front()`), después `pop()`.

**Orco: `top()` o `front()` de un adaptador vacío.** Comportamiento indefinido.
Preguntá `empty()` antes.

**Esqueleto: recorrer un adaptador con `for`.**
```
main.cpp:2:46: error: no matching function for call to ‘begin(std::stack<int>&)’
```
Los adaptadores no tienen iteradores: se vacían de a uno. Si necesitás recorrer,
quizás querías un `vector` o un `deque`.

**Ogro: el comparador al revés.** En `priority_queue`, el comparador dice si `a`
tiene **menos** prioridad que `b`. `std::greater` hace que salga el **menor**. Si te
sale al revés, invertí la comparación.

**Troll: guardar una referencia a `top()` y después hacer `pop()`.** La referencia
queda colgando: copiá el valor antes de sacarlo si lo vas a seguir usando.

### Misión R04-N03-M1 · Paréntesis balanceados

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea de la entrada es una expresión con `()`, `[]` y `{}`. Con una
`std::stack`, decí si está balanceada. Si no, mostrá debajo una `^` en la posición
del primer error: un cierre que no corresponde, o el último abierto que quedó sin
cerrar. (Guardá en la pila el símbolo y su posición.)

#### Criterio de aprobación

- Usa `std::stack` para los símbolos abiertos.
- Detecta cierres de más, cierres cruzados y aperturas sin cerrar.
- Marca la posición del error.

#### Entrada de ejemplo

```
(a + b) * [c - {d / e}]
(a + b]
{[()()]}(
x) + (y
```

#### Salida esperada

```
ok:    (a + b) * [c - {d / e}]
error: (a + b]
             ^
error: {[()()]}(
               ^
error: x) + (y
        ^
```

#### Solución de referencia

```cpp
// Mision 1 - Parentesis balanceados: una pila de simbolos.
#include <iostream>
#include <stack>
#include <string>
#include <utility>

bool balanceado(const std::string& s, std::size_t& error)
{
    std::stack<std::pair<char, std::size_t>> abiertos;
    for (std::size_t i = 0; i < s.size(); i++) {
        char c = s[i];
        if (c == '(' || c == '[' || c == '{') {
            abiertos.push({c, i});
        } else if (c == ')' || c == ']' || c == '}') {
            char esperado = (c == ')') ? '(' : (c == ']') ? '[' : '{';
            if (abiertos.empty() || abiertos.top().first != esperado) {
                error = i;
                return false;
            }
            abiertos.pop();
        }
    }
    if (!abiertos.empty()) {
        error = abiertos.top().second;
        return false;
    }
    return true;
}

int main()
{
    std::string linea;
    while (std::getline(std::cin, linea)) {
        std::size_t error = 0;
        if (balanceado(linea, error)) {
            std::cout << "ok:    " << linea << "\n";
        } else {
            std::cout << "error: " << linea << "\n       " << std::string(error, ' ') << "^\n";
        }
    }
    return 0;
}
```

#### Pruebas

##### Todo bien
```entrada
()[]{}
sin simbolos
```
```salida
ok:    ()[]{}
ok:    sin simbolos
```

##### Cierre al principio
```entrada
]abc
```
```salida
error: ]abc
       ^
```

##### Solo aperturas
```entrada
(((
```
```salida
error: (((
         ^
```

### Misión R04-N03-M2 · La fila del banco

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Simulá la fila de un banco con una `std::queue`. Órdenes: `llega nombre` y
`atender` (atiende al primero, o avisa que no hay nadie). Al final mostrá cuántos se
atendieron, cuál fue la fila más larga, cuántos quedan esperando y, si queda
alguien, quién es el próximo y quién el último.

#### Criterio de aprobación

- Usa `front`, `back`, `push` y `pop`.
- No atiende una fila vacía.

#### Entrada de ejemplo

```
llega Ana
llega Bruno
atender
llega Celi
llega Dami
llega Eli
atender
atender
atender
atender
atender
llega Fede
llega Gabi
```

#### Salida esperada

```
Atiende a Ana (quedan 1)
Atiende a Bruno (quedan 3)
Atiende a Celi (quedan 2)
Atiende a Dami (quedan 1)
Atiende a Eli (quedan 0)
La caja espera: no hay nadie
Atendidos: 5, fila más larga: 4, esperando: 2
Próximo: Fede, último: Gabi
```

#### Solución de referencia

```cpp
// Mision 2 - La fila del banco: una queue con clientes que llegan y cajas que atienden.
#include <iostream>
#include <queue>
#include <string>

int main()
{
    std::queue<std::string> fila;
    std::string orden;
    int atendidos = 0;
    std::size_t maxima = 0;
    while (std::cin >> orden) {
        if (orden == "llega") {
            std::string nombre;
            std::cin >> nombre;
            fila.push(nombre);
            if (fila.size() > maxima) {
                maxima = fila.size();
            }
        } else if (orden == "atender") {
            if (fila.empty()) {
                std::cout << "La caja espera: no hay nadie\n";
            } else {
                std::cout << "Atiende a " << fila.front() << " (quedan " << fila.size() - 1 << ")\n";
                fila.pop();
                atendidos++;
            }
        }
    }
    std::cout << "Atendidos: " << atendidos << ", fila más larga: " << maxima << ", esperando: " << fila.size() << "\n";
    if (!fila.empty()) {
        std::cout << "Próximo: " << fila.front() << ", último: " << fila.back() << "\n";
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
La caja espera: no hay nadie
La caja espera: no hay nadie
Atendidos: 0, fila más larga: 0, esperando: 0
```

##### Nadie atendido
```entrada
llega Ana
llega Bruno
```
```salida
Atendidos: 0, fila más larga: 2, esperando: 2
Próximo: Ana, último: Bruno
```

##### Sin órdenes
```entrada
```
```salida
Atendidos: 0, fila más larga: 0, esperando: 0
```

### Misión R04-N03-M3 · El historial con límite

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un editor guarda las **últimas 4** acciones en un `std::deque` (si hay más, olvida la
más vieja con `pop_front`). Cada palabra de la entrada es una acción, salvo
`deshacer` (pasa la última acción a una pila de "rehacer", otro `deque`) y
`rehacer` (la vuelve). Una acción nueva vacía el "rehacer". Después de cada orden,
mostrá el historial y cuántas acciones hay para rehacer.

#### Criterio de aprobación

- Usa las dos puntas del `deque`.
- Nunca guarda más de 4 acciones.
- Una acción nueva borra lo que había para rehacer.

#### Entrada de ejemplo

```
escribir negrita pegar deshacer deshacer rehacer copiar cortar mover deshacer rehacer rehacer
```

#### Salida esperada

```
escribir -> escribir | rehacer:0
negrita -> escribir negrita | rehacer:0
pegar -> escribir negrita pegar | rehacer:0
deshacer -> escribir negrita | rehacer:1
deshacer -> escribir | rehacer:2
rehacer -> escribir negrita | rehacer:1
copiar -> escribir negrita copiar | rehacer:0
cortar -> escribir negrita copiar cortar | rehacer:0
mover -> negrita copiar cortar mover | rehacer:0
deshacer -> negrita copiar cortar | rehacer:1
rehacer -> negrita copiar cortar mover | rehacer:0
rehacer -> negrita copiar cortar mover | rehacer:0
```

#### Solución de referencia

```cpp
// Mision 3 - El historial con limite: deque que descarta lo mas viejo.
#include <deque>
#include <iostream>
#include <string>

int main()
{
    const std::size_t LIMITE = 4;
    std::deque<std::string> historial;
    std::deque<std::string> rehacer;
    std::string orden;
    while (std::cin >> orden) {
        if (orden == "deshacer") {
            if (!historial.empty()) {
                rehacer.push_front(historial.back());
                historial.pop_back();
            }
        } else if (orden == "rehacer") {
            if (!rehacer.empty()) {
                historial.push_back(rehacer.front());
                rehacer.pop_front();
            }
        } else {
            historial.push_back(orden);
            rehacer.clear();                     // una accion nueva borra el rehacer
            if (historial.size() > LIMITE) {
                historial.pop_front();           // se olvida lo mas viejo
            }
        }
        std::cout << orden << " ->";
        for (const auto& h : historial) {
            std::cout << " " << h;
        }
        std::cout << " | rehacer:" << rehacer.size() << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Deshacer sin historial
```entrada
deshacer rehacer
```
```salida
deshacer -> | rehacer:0
rehacer -> | rehacer:0
```

##### Seis acciones
```entrada
a b c d e f
```
```salida
a -> a | rehacer:0
b -> a b | rehacer:0
c -> a b c | rehacer:0
d -> a b c d | rehacer:0
e -> b c d e | rehacer:0
f -> c d e f | rehacer:0
```

##### Deshacer y escribir otra cosa
```entrada
a b deshacer c rehacer
```
```salida
a -> a | rehacer:0
b -> a b | rehacer:0
deshacer -> a | rehacer:1
c -> a c | rehacer:0
rehacer -> a c | rehacer:0
```

### Encargo R04-N03-E1 · La guardia del hospital

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

En la guardia se atiende primero al de **mayor urgencia** (1 a 5) y, con la misma
urgencia, al que **llegó antes**. Escribí un comparador (`struct` con `operator()`)
para una `std::priority_queue<Paciente, std::vector<Paciente>, Comparador>`.
Órdenes: `ingresa nombre urgencia` y `medico` (atiende al siguiente). Al final,
cuántos quedan esperando.

#### Criterio de aprobación

- El comparador desempata por orden de llegada.
- No atiende con la sala vacía.

#### Entrada de ejemplo

```
ingresa Ana 2
ingresa Bruno 5
ingresa Celi 2
medico
ingresa Dami 4
medico
medico
ingresa Eli 5
medico
medico
medico
```

#### Salida esperada

```
Pasa Bruno (urgencia 5)
Pasa Dami (urgencia 4)
Pasa Ana (urgencia 2)
Pasa Eli (urgencia 5)
Pasa Celi (urgencia 2)
Sala vacía
Esperando: 0
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La guardia del hospital: triage con priority_queue.
#include <iostream>
#include <queue>
#include <string>
#include <vector>

struct Paciente {
    std::string nombre;
    int urgencia = 0;     // 1 (leve) a 5 (critico)
    int llegada = 0;      // orden de llegada
};

// Primero la mayor urgencia; con la misma urgencia, el que llego antes.
struct MenosUrgente {
    bool operator()(const Paciente& a, const Paciente& b) const
    {
        if (a.urgencia != b.urgencia) {
            return a.urgencia < b.urgencia;
        }
        return a.llegada > b.llegada;
    }
};

int main()
{
    std::priority_queue<Paciente, std::vector<Paciente>, MenosUrgente> guardia;
    std::string orden;
    int llegada = 0;
    while (std::cin >> orden) {
        if (orden == "ingresa") {
            Paciente p;
            std::cin >> p.nombre >> p.urgencia;
            p.llegada = ++llegada;
            guardia.push(p);
        } else if (orden == "medico") {
            if (guardia.empty()) {
                std::cout << "Sala vacía\n";
            } else {
                const Paciente& p = guardia.top();
                std::cout << "Pasa " << p.nombre << " (urgencia " << p.urgencia << ")\n";
                guardia.pop();
            }
        }
    }
    std::cout << "Esperando: " << guardia.size() << "\n";
    return 0;
}
```

#### Pruebas

##### Médico sin pacientes
```entrada
medico
```
```salida
Sala vacía
Esperando: 0
```

##### Misma urgencia en orden de llegada
```entrada
ingresa A 3
ingresa B 3
ingresa C 3
medico
medico
```
```salida
Pasa A (urgencia 3)
Pasa B (urgencia 3)
Esperando: 1
```

##### Quedan esperando
```entrada
ingresa X 1
ingresa Y 5
```
```salida
Esperando: 2
```

### Prueba del sello

#### ¿Qué diferencia hay entre una pila y una cola?

En la pila sale primero el último que entró (LIFO); en la cola, el primero que entró (FIFO).

#### ¿Qué devuelve `pop()` en `stack`, `queue` o `priority_queue`?

Nada. Para leer el elemento hay que usar `top()` o `front()` antes.

#### ¿Cuál sale primero de una `priority_queue<int>`? ¿Y con `std::greater<int>`?

El mayor; con `std::greater`, el menor.

#### ¿Cuándo conviene un `deque` en vez de un `vector`?

Cuando hay que agregar o sacar elementos por el principio además del final.

#### ¿Por qué casi siempre conviene `vector` antes que `list`?

Porque sus datos están juntos en memoria y el procesador los recorre mucho más rápido; `list` solo gana en casos puntuales.

### Soluciones (docente)

Material original: `11-STL/03-Contenedores-Secuencia` (sin las mediciones de tiempo, que dan distinto en cada compu) y `11-STL/05-Adaptadores`.

## R04-N04 · Mapas y conjuntos a fondo

```meta
tipo: tema
padre: R04-N03
precio: 10
criatura: orco
temas: col.mapas, col.conjuntos
```

### Crónica

El índice de la Gran Biblioteca no es un simple fichero. Hay fichas con la misma palabra repetida (un tema en varios libros), búsquedas por rango ("todo lo que esté entre la L y la P") y estantes ordenados con reglas raras.

—Los mapas y conjuntos que ya conocés saben mucho más —dice {mentor}—. Saben guardar repetidos, buscar rangos enteros y ordenar como vos les digas.

### Objetivos

Usar `std::multimap` y `std::multiset` (claves repetidas), consultar rangos con
`lower_bound`, `upper_bound` y `equal_range`, aprovechar lo que devuelve `insert`,
y ordenar mapas y conjuntos con comparadores propios.

### Antes de empezar

- `std::map`, `std::set` y `std::unordered_map` (rama 3).
- Iteradores (Iteradores).

### Explicación

#### Lo que devuelve `insert`
```cpp
auto [it, nuevo] = precios.insert({"engranaje", 350});
```
`insert` devuelve un par: un iterador al elemento y un `bool` que dice si **era
nuevo**. Si la clave ya estaba, `insert` **no** la cambia. Para "insertar o
reemplazar", `insert_or_assign`. Para crear el valor solo si falta, `try_emplace`.

#### Claves repetidas: `multimap` y `multiset`
Un `std::map` tiene una sola entrada por clave. Si necesitás varias (varios enemigos
en la misma casilla, varias actividades el mismo día), se usa `std::multimap`:
```cpp
std::multimap<int, std::string> por_casilla;
por_casilla.insert({3, "slime"});
por_casilla.insert({3, "goblin"});
por_casilla.count(3);                          // 2
auto [desde, hasta] = por_casilla.equal_range(3);   // todas las de la clave 3
```
`multimap` no tiene `[]` (¿a cuál de las repetidas se referiría?). `std::multiset`
es un `set` que guarda repetidos: `erase(valor)` borra **todos** los iguales;
`erase(s.find(valor))`, uno solo.

#### Búsquedas por rango
Como `map` y `set` están **ordenados**, saben buscar rangos:
| Función | Devuelve |
|---|---|
| `m.lower_bound(k)` | el primero con clave **≥ k** |
| `m.upper_bound(k)` | el primero con clave **> k** |
| `m.equal_range(k)` | el par `[lower_bound, upper_bound)`: todos los de clave `k` |

"Todo entre `a` y `b`" es `for (auto it = m.lower_bound(a); it != m.upper_bound(b); ++it)`.
Y "el último tramo que empieza antes de `x`" es `std::prev(m.upper_bound(x))`: el
clásico para tablas de tarifas por tramos.

#### Comparadores propios
El tercer parámetro de `map`/`set` es **cómo ordenar**. Por defecto es `<`; con
`std::greater<T>` queda de mayor a menor, y con un `struct` con `operator()` podés
definir cualquier orden:
```cpp
struct PorLargo {
    bool operator()(const std::string& a, const std::string& b) const {
        return a.size() != b.size() ? a.size() < b.size() : a < b;
    }
};
std::set<std::string, PorLargo> armas;
```
Ojo: el `set` considera **iguales** a dos elementos si ninguno es "menor" que el
otro según el comparador. Si `PorLargo` solo comparara el largo, "arco" y "maza"
serían "iguales" y se guardaría solo uno.

#### Cuánto cuesta
| Contenedor | Buscar, insertar, borrar |
|---|---|
| `map`, `set`, `multimap`, `multiset` | O(log n): unos 20 pasos para un millón |
| `unordered_map`, `unordered_set` | O(1) en promedio: casi directo |
| buscar en un `vector` sin ordenar | O(n): recorre todo |

Los `unordered` no tienen `lower_bound` ni orden: si necesitás rangos, `map`.

> **Si venís de C.** Todo esto (un árbol balanceado con búsquedas por rango) en C
> eran cientos de líneas. Acá es una declaración.

### Código de ejemplo

```cpp
/*
 * Contenedores asociativos a fondo: multimap, multiset, rangos y comparadores.
 */
#include <iostream>
#include <map>
#include <set>
#include <string>

struct PorLargo {                     // un comparador: ordena textos por largo y despues alfabetico
    bool operator()(const std::string& a, const std::string& b) const
    {
        return a.size() != b.size() ? a.size() < b.size() : a < b;
    }
};

int main()
{
    // insert devuelve {iterador, bool}: el bool dice si era nuevo
    std::map<std::string, int> precios;
    auto [it1, nuevo1] = precios.insert({"engranaje", 350});
    auto [it2, nuevo2] = precios.insert({"engranaje", 999});      // ya estaba: NO lo cambia
    std::cout << std::boolalpha << "¿nuevo? " << nuevo1 << ", " << nuevo2 << "; precio: " << it2->second << "\n";
    precios.insert_or_assign("engranaje", 400);                    // este si reemplaza
    std::cout << "tras insert_or_assign: " << precios["engranaje"] << "\n";

    // multimap: una clave puede repetirse (varios enemigos por casilla)
    std::multimap<int, std::string> por_casilla = {{3, "slime"}, {7, "orco"}, {3, "goblin"}, {3, "rata"}};
    std::cout << "en la casilla 3 hay " << por_casilla.count(3) << ":";
    auto [desde, hasta] = por_casilla.equal_range(3);              // el rango de esa clave
    for (auto it = desde; it != hasta; ++it) {
        std::cout << " " << it->second;
    }
    std::cout << "\n";

    // Rangos en un map ordenado: lower_bound y upper_bound
    std::map<int, std::string> eventos = {{800, "abrir"}, {1230, "almuerzo"}, {1500, "entrega"}, {1900, "cierre"}};
    std::cout << "entre las 12:00 y las 16:00:";
    for (auto it = eventos.lower_bound(1200); it != eventos.upper_bound(1600); ++it) {
        std::cout << " " << it->first << "=" << it->second;
    }
    std::cout << "\n";
    auto prox = eventos.lower_bound(1000);                          // el primero >= 1000
    std::cout << "después de las 10:00 viene: " << prox->second << "\n";

    // multiset: ordenado, CON repetidos
    std::multiset<int> tiradas = {4, 6, 2, 6, 6, 1};
    std::cout << "tiradas ordenadas:";
    for (int t : tiradas) {
        std::cout << " " << t;
    }
    std::cout << " (seises: " << tiradas.count(6) << ")\n";
    tiradas.erase(tiradas.find(6));                                 // borra UNO solo
    std::cout << "tras borrar un 6 quedan " << tiradas.count(6) << " seises\n";

    // Un set con comparador propio
    std::set<std::string, PorLargo> armas = {"hacha", "arco", "espada", "maza", "ballesta"};
    std::cout << "armas por largo:";
    for (const auto& a : armas) {
        std::cout << " " << a;
    }
    std::cout << "\n";
    return 0;
}
```

### Salida esperada

```
¿nuevo? true, false; precio: 350
tras insert_or_assign: 400
en la casilla 3 hay 3: slime goblin rata
entre las 12:00 y las 16:00: 1230=almuerzo 1500=entrega
después de las 10:00 viene: almuerzo
tiradas ordenadas: 1 2 4 6 6 6 (seises: 3)
tras borrar un 6 quedan 2 seises
armas por largo: arco maza hacha espada ballesta
```

### ¿Para qué sirve?

Las búsquedas por rango están en cualquier agenda (los turnos entre dos fechas), en las tarifas por tramos (envíos, impuestos, escalas de sueldo), en los rankings y en los índices de un buscador (en qué documentos aparece cada palabra). Los `multimap` modelan relaciones "uno a muchos": un cliente con muchos pedidos, un día con muchas actividades, una casilla con muchos enemigos.

### Errores habituales

**Ogro: creer que `insert` reemplaza.** Si la clave ya estaba, `insert` no hace nada.
Mirá el `bool` que devuelve, o usá `insert_or_assign`.

**Esqueleto: `[]` en un `multimap`.** No existe: usá `insert` y `equal_range`.

**Ogro: `multiset::erase(valor)` borra todos.** Para borrar uno solo:
`s.erase(s.find(valor))` (si `find` no devuelve `end()`).

**Orco: `std::prev(m.upper_bound(x))` cuando no hay tramo.** Si `x` es menor que la
primera clave, `upper_bound` devuelve `begin()` y `prev` de eso es inválido.
Validá el rango antes.

**Ogro: un comparador que "iguala" de más.** Un `set` con un comparador que solo
mira una parte descarta elementos distintos como si fueran iguales. Desempatá con
otro criterio.

### Misión R04-N04-M1 · La agenda del taller

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Guardá una agenda en un `std::multimap<int, std::string>` (día → actividad).
Órdenes: `agendar dia actividad`, `dia N` (todas las actividades de ese día, o
"libre") y `semana desde hasta` (todo lo del rango, con su día). Al final, el total
de actividades.

#### Criterio de aprobación

- Usa `equal_range` para un día y `lower_bound`/`upper_bound` para el rango.
- Permite varias actividades el mismo día.

#### Entrada de ejemplo

```
agendar 3 caldera
agendar 5 planos
agendar 3 aceite
agendar 12 inventario
dia 3
dia 4
semana 1 7
agendar 7 reunion
semana 5 12
```

#### Salida esperada

```
Día 3: caldera aceite
Día 4: libre
Del 1 al 7: 3-caldera 3-aceite 5-planos
Del 5 al 12: 5-planos 7-reunion 12-inventario
Total de actividades: 5
```

#### Solución de referencia

```cpp
// Mision 1 - La agenda de turnos: multimap de dia -> actividad y consultas por rango.
#include <iostream>
#include <map>
#include <string>

int main()
{
    std::multimap<int, std::string> agenda;
    std::string orden;
    while (std::cin >> orden) {
        if (orden == "agendar") {
            int dia = 0;
            std::string actividad;
            std::cin >> dia >> actividad;
            agenda.insert({dia, actividad});
        } else if (orden == "dia") {
            int dia = 0;
            std::cin >> dia;
            auto [ini, fin] = agenda.equal_range(dia);
            std::cout << "Día " << dia << ":";
            if (ini == fin) {
                std::cout << " libre";
            }
            for (auto it = ini; it != fin; ++it) {
                std::cout << " " << it->second;
            }
            std::cout << "\n";
        } else if (orden == "semana") {
            int desde = 0, hasta = 0;
            std::cin >> desde >> hasta;
            std::cout << "Del " << desde << " al " << hasta << ":";
            for (auto it = agenda.lower_bound(desde); it != agenda.upper_bound(hasta); ++it) {
                std::cout << " " << it->first << "-" << it->second;
            }
            std::cout << "\n";
        }
    }
    std::cout << "Total de actividades: " << agenda.size() << "\n";
    return 0;
}
```

#### Pruebas

##### Agenda vacía
```entrada
dia 1
semana 1 30
```
```salida
Día 1: libre
Del 1 al 30:
Total de actividades: 0
```

##### Rango de un día
```entrada
agendar 10 a
agendar 10 b
agendar 11 c
semana 10 10
```
```salida
Del 10 al 10: 10-a 10-b
Total de actividades: 3
```

### Misión R04-N04-M2 · El ranking vivo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea es una partida: `nombre puntos`. Guardalas en un `std::multiset<Marca,
std::greater<Marca>>` (con un `operator>` que ordene por puntos y, si empatan, por
nombre). Mostrá el top 3, cuántas partidas hay y la peor (con `rbegin`).

#### Criterio de aprobación

- El conjunto se mantiene ordenado solo: no hay `sort`.
- Acepta partidas repetidas (es `multiset`).

#### Entrada de ejemplo

```
Kira 340
Bron 120
Lyn 340
Oto 95
Kira 210
Tesla 500
```

#### Salida esperada

```
Top 3:
  1. Tesla 500
  2. Kira 340
  3. Lyn 340
Partidas registradas: 6
Peor partida: Oto 95
```

#### Solución de referencia

```cpp
// Mision 2 - El ranking vivo: multiset ordenado de mayor a menor con std::greater.
#include <functional>
#include <iostream>
#include <set>
#include <string>

struct Marca {
    int puntos = 0;
    std::string nombre;
    bool operator>(const Marca& o) const { return puntos != o.puntos ? puntos > o.puntos : nombre < o.nombre; }
};

int main()
{
    std::multiset<Marca, std::greater<Marca>> ranking;
    Marca m;
    while (std::cin >> m.nombre >> m.puntos) {
        ranking.insert(m);
    }
    std::cout << "Top 3:\n";
    int pos = 1;
    for (auto it = ranking.begin(); it != ranking.end() && pos <= 3; ++it, ++pos) {
        std::cout << "  " << pos << ". " << it->nombre << " " << it->puntos << "\n";
    }
    std::cout << "Partidas registradas: " << ranking.size() << "\n";
    std::cout << "Peor partida: " << ranking.rbegin()->nombre << " " << ranking.rbegin()->puntos << "\n";
    return 0;
}
```

#### Pruebas

##### Menos de tres partidas
```entrada
Kira 10
Bron 20
```
```salida
Top 3:
  1. Bron 20
  2. Kira 10
Partidas registradas: 2
Peor partida: Kira 10
```

##### Empates en todo
```entrada
B 100
A 100
C 100
A 100
```
```salida
Top 3:
  1. A 100
  2. A 100
  3. B 100
Partidas registradas: 4
Peor partida: C 100
```

##### Una sola partida
```entrada
Solo 1
```
```salida
Top 3:
  1. Solo 1
Partidas registradas: 1
Peor partida: Solo 1
```

### Misión R04-N04-M3 · El índice de la biblioteca

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé líneas de texto y armá un índice: `std::map<std::string, std::set<int>>`, de
cada palabra al conjunto de líneas donde aparece (sin repetir una línea). Mostrá
solo las palabras que aparecen en **dos o más** líneas, con sus números.

#### Criterio de aprobación

- Usa un `set` como valor del `map` para no repetir líneas.
- Filtra las que aparecen en una sola línea.

#### Entrada de ejemplo

```
el reloj de la torre
la torre del faro
el faro y el reloj
nada que ver
```

#### Salida esperada

```
el: 1 3
faro: 2 3
la: 1 2
reloj: 1 3
torre: 1 2
```

#### Solución de referencia

```cpp
// Mision 3 - El diccionario inverso: de cada palabra, en que lineas aparece.
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>

int main()
{
    std::map<std::string, std::set<int>> indice;
    std::string linea;
    int numero = 0;
    while (std::getline(std::cin, linea)) {
        numero++;
        std::istringstream palabras(linea);
        std::string p;
        while (palabras >> p) {
            indice[p].insert(numero);        // el set no repite la misma linea
        }
    }
    for (const auto& [palabra, lineas] : indice) {
        if (lineas.size() < 2) {
            continue;
        }
        std::cout << palabra << ":";
        for (int n : lineas) {
            std::cout << " " << n;
        }
        std::cout << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Una sola palabra repetida
```entrada
uno dos
tres uno
cuatro
```
```salida
uno: 1 2
```

##### Misma palabra en la misma línea
```entrada
el el el
el
```
```salida
el: 1 2
```

### Encargo R04-N04-E1 · Las tarifas del correo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El correo cobra por tramos de peso: desde 0 kg, $1500; desde 1 kg, $2300; desde 5
kg, $4100; desde 10 kg, $6800; desde 25 kg, $12500. No se envía nada de 0 kg o
menos, ni de más de 50 kg. Guardá la tarifa en un `const std::map<double, int>` y
encontrá el tramo de cada peso de la entrada con `std::prev(TARIFA.upper_bound(peso))`.

#### Criterio de aprobación

- Usa `upper_bound` y `std::prev`.
- Rechaza los pesos fuera de rango antes de buscar.
- Muestra el tramo usado.

#### Entrada de ejemplo

```
0.5
1
4.5
5
12
25
60
-2
```

#### Salida esperada

```
0.5 kg: $1500 (tramo desde 0.0 kg)
1.0 kg: $2300 (tramo desde 1.0 kg)
4.5 kg: $2300 (tramo desde 1.0 kg)
5.0 kg: $4100 (tramo desde 5.0 kg)
12.0 kg: $6800 (tramo desde 10.0 kg)
25.0 kg: $12500 (tramo desde 25.0 kg)
60.0 kg: no se envía
-2.0 kg: no se envía
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Las tarifas por tramos: buscar en un map con upper_bound.
#include <iomanip>
#include <iostream>
#include <iterator>
#include <map>

int main()
{
    // desde este peso (kg) en adelante, cuesta tanto el envio
    const std::map<double, int> TARIFA = {{0, 1500}, {1, 2300}, {5, 4100}, {10, 6800}, {25, 12500}};
    double peso = 0;
    std::cout << std::fixed << std::setprecision(1);
    while (std::cin >> peso) {
        if (peso <= 0 || peso > 50) {
            std::cout << peso << " kg: no se envía\n";
            continue;
        }
        auto it = std::prev(TARIFA.upper_bound(peso));   // el ultimo tramo que empieza <= peso
        std::cout << peso << " kg: $" << it->second << " (tramo desde " << it->first << " kg)\n";
    }
    return 0;
}
```

#### Pruebas

##### Bordes
```entrada
0
50
50.01
10
24.99
```
```salida
0.0 kg: no se envía
50.0 kg: $12500 (tramo desde 25.0 kg)
50.0 kg: no se envía
10.0 kg: $6800 (tramo desde 10.0 kg)
25.0 kg: $6800 (tramo desde 10.0 kg)
```

##### Peso mínimo
```entrada
0.01
```
```salida
0.0 kg: $1500 (tramo desde 0.0 kg)
```

### Prueba del sello

#### ¿Qué devuelve `insert` en un `map`? ¿Reemplaza el valor si la clave existía?

Un par (iterador, `bool` "era nuevo"). No reemplaza: para eso está `insert_or_assign`.

#### ¿Qué diferencia hay entre `map` y `multimap`?

`multimap` permite varias entradas con la misma clave (y no tiene `[]`).

#### ¿Qué devuelven `lower_bound(k)` y `upper_bound(k)`?

El primero con clave ≥ k y el primero con clave > k.

#### ¿Cómo recorrés todas las entradas de una clave en un `multimap`?

Con `equal_range(k)`, que devuelve el rango de esa clave.

#### ¿Por qué `unordered_map` no tiene `lower_bound`?

Porque no mantiene orden: no hay "el primero mayor o igual".

### Soluciones (docente)

Material original: `11-STL/04-Contenedores-Asociativos`.

## R04-N05 · Los algoritmos de la biblioteca

```meta
tipo: tema
padre: R04-N04
precio: 10
criatura: ogro
temas: alg.ordenamiento, alg.busqueda
```

### Crónica

En el ala de las herramientas hay más de cien instrumentos colgados: para ordenar, buscar, dar vuelta, rotar, mezclar, sumar. Un aprendiz está escribiendo un bucle para sumar una columna.

—Ese bucle ya lo escribió alguien mejor que vos y que yo —dice {mentor}, y le alcanza una herramienta—. Antes de escribir un bucle, preguntate si no hay un algoritmo que lo hace. Casi siempre lo hay.

### Objetivos

Conocer y usar los algoritmos principales de `<algorithm>` y `<numeric>`:
generar (`iota`, `fill`), acumular (`accumulate`, `partial_sum`), reordenar
(`reverse`, `rotate`, `stable_sort`, `partial_sort`, `nth_element`), buscar en
rangos ordenados (`binary_search`, `lower_bound`), limpiar (`unique`) y operar
con conjuntos (`set_intersection`, `set_union`, `set_difference`).

### Antes de empezar

- Lambdas (rama 3).
- Iteradores (Iteradores).

### Explicación

#### Por qué usar algoritmos
- **Dicen qué hacen**: `std::count_if(...)` se entiende de un vistazo; un bucle hay
  que leerlo entero.
- **Están probados**: no tienen el "uno de más" que se escapa en un bucle a mano.
- **Son rápidos**: están optimizados para cada contenedor.

Todos reciben un **rango** de iteradores (`begin`, `end`) y muchos, una **lambda**.

#### Un mapa de la caja de herramientas
| Para… | Algoritmos |
|---|---|
| llenar | `std::fill`, `std::iota` (valores consecutivos), `std::generate` |
| acumular (`<numeric>`) | `std::accumulate`, `std::partial_sum`, `std::reduce` |
| buscar | `std::find`, `std::find_if`, `std::count`, `std::count_if`, `std::min_element`, `std::max_element`, `std::minmax_element` |
| preguntar | `std::all_of`, `std::any_of`, `std::none_of`, `std::equal`, `std::is_sorted` |
| reordenar | `std::reverse`, `std::rotate`, `std::shuffle` |
| ordenar | `std::sort`, `std::stable_sort`, `std::partial_sort`, `std::nth_element` |
| en rangos **ordenados** | `std::binary_search`, `std::lower_bound`, `std::upper_bound`, `std::merge`, `std::unique`, `std::set_intersection`, `std::set_union`, `std::set_difference` |
| copiar y transformar | `std::copy`, `std::copy_if`, `std::transform` |

#### Ordenar: cuál usar
- `std::sort`: el más rápido; entre elementos "iguales" no garantiza el orden.
- `std::stable_sort`: respeta el orden original entre iguales (por ejemplo, ordenar
  por largo sin mezclar los del mismo largo).
- `std::partial_sort(b, b + k, e)`: ordena **solo los k primeros** (el podio): más
  rápido que ordenar todo.
- `std::nth_element(b, b + n, e)`: deja en la posición `n` el elemento que iría ahí
  si estuviera ordenado (la mediana) sin ordenar el resto.

#### Búsqueda binaria: solo en rangos ordenados
Si el rango está ordenado, buscar no hace falta recorrerlo: se parte por la mitad
cada vez (con un millón de elementos, unos 20 pasos).
```cpp
std::binary_search(v.begin(), v.end(), 4);     // ¿está?
auto it = std::lower_bound(v.begin(), v.end(), 4);   // dónde está, o dónde iría
```
`lower_bound` también sirve para **insertar en orden**: `v.insert(it, x)` deja el
vector ordenado. Si el rango **no** está ordenado, el resultado es basura (y no
avisa).

#### Quitar repetidos
`std::unique` **no borra**: corre los repetidos **consecutivos** al final y devuelve
dónde empieza la "basura". Por eso se ordena primero y se borra después:
```cpp
std::sort(v.begin(), v.end());
v.erase(std::unique(v.begin(), v.end()), v.end());
```

#### El tipo de `accumulate`
`std::accumulate(b, e, 0)` suma en `int`; con `0.0`, en `double`. Con un cuarto
parámetro cambia la operación: `std::accumulate(b, e, 1, std::multiplies<int>())`
multiplica.

> **Si venís de C.** C solo traía `qsort` y `bsearch`. En C++ hay más de cien
> algoritmos, con tipos y para cualquier contenedor.

### Código de ejemplo

```cpp
/*
 * Los algoritmos de <algorithm> y <numeric>: no escribas bucles que ya existen.
 */
#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

void mostrar(const std::string& t, const std::vector<int>& v)
{
    std::cout << t << ":";
    for (int x : v) {
        std::cout << " " << x;
    }
    std::cout << "\n";
}

int main()
{
    std::vector<int> v(10);
    std::iota(v.begin(), v.end(), 1);                               // 1, 2, ..., 10
    mostrar("iota", v);

    std::cout << "suma " << std::accumulate(v.begin(), v.end(), 0)
              << ", producto de los 5 primeros " << std::accumulate(v.begin(), v.begin() + 5, 1, std::multiplies<int>()) << "\n";

    std::vector<int> acumulado(v.size());
    std::partial_sum(v.begin(), v.end(), acumulado.begin());       // sumas parciales
    mostrar("partial_sum", acumulado);

    std::reverse(v.begin(), v.end());
    mostrar("reverse", v);
    std::rotate(v.begin(), v.begin() + 3, v.end());                // el 4.o pasa a ser el primero
    mostrar("rotate 3", v);

    std::vector<int> datos = {7, 3, 9, 3, 1, 9, 9, 4};
    auto [menor, mayor] = std::minmax_element(datos.begin(), datos.end());
    std::cout << "menor " << *menor << ", mayor " << *mayor << "\n";

    std::vector<int> top3(3);
    std::partial_sort_copy(datos.begin(), datos.end(), top3.begin(), top3.end(), std::greater<int>());
    mostrar("los 3 mayores", top3);

    std::sort(datos.begin(), datos.end());
    mostrar("sort", datos);
    std::cout << "¿está el 4? " << (std::binary_search(datos.begin(), datos.end(), 4) ? "sí" : "no")
              << " (búsqueda binaria: el rango tiene que estar ORDENADO)\n";
    auto primer9 = std::lower_bound(datos.begin(), datos.end(), 9);
    std::cout << "el primer 9 está en la posición " << (primer9 - datos.begin()) << "\n";

    datos.erase(std::unique(datos.begin(), datos.end()), datos.end());   // quitar repetidos (ordenado)
    mostrar("sin repetidos", datos);

    std::vector<std::string> nombres = {"Lyn", "Kira", "Oto", "Bron", "Ana"};
    std::stable_sort(nombres.begin(), nombres.end(),
                     [](const std::string& a, const std::string& b) { return a.size() < b.size(); });
    std::cout << "por largo (estable, respeta el orden original entre iguales):";
    for (const auto& n : nombres) {
        std::cout << " " << n;
    }
    std::cout << "\n";

    std::vector<int> a = {1, 3, 5, 7}, b = {3, 4, 5, 6};
    std::vector<int> comun;
    std::set_intersection(a.begin(), a.end(), b.begin(), b.end(), std::back_inserter(comun));
    mostrar("en los dos", comun);
    std::fill(comun.begin(), comun.end(), 0);
    mostrar("fill 0", comun);
    return 0;
}
```

### Salida esperada

```
iota: 1 2 3 4 5 6 7 8 9 10
suma 55, producto de los 5 primeros 120
partial_sum: 1 3 6 10 15 21 28 36 45 55
reverse: 10 9 8 7 6 5 4 3 2 1
rotate 3: 7 6 5 4 3 2 1 10 9 8
menor 1, mayor 9
los 3 mayores: 9 9 9
sort: 1 3 3 4 7 9 9 9
¿está el 4? sí (búsqueda binaria: el rango tiene que estar ORDENADO)
el primer 9 está en la posición 5
sin repetidos: 1 3 4 7 9
por largo (estable, respeta el orden original entre iguales): Lyn Oto Ana Kira Bron
en los dos: 3 5
fill 0: 0 0
```

### ¿Para qué sirve?

Cualquier planilla, reporte o estadística es una combinación de algoritmos: ordenar las ventas, quedarse con los 10 mejores clientes, buscar un código en una lista ordenada, unir dos listas de contactos sin repetir, calcular sumas acumuladas mes a mes. En un juego: ordenar los objetos por distancia para dibujarlos, elegir los enemigos más cercanos, mezclar un mazo.

### Errores habituales

**Ogro: `binary_search` o `lower_bound` sobre un rango desordenado.** Compila, corre
y devuelve cualquier cosa. Ordená primero.

**Ogro: `unique` sin ordenar.** Solo quita repetidos **consecutivos**: `{1, 2, 1}`
queda igual.

**Ogro: olvidar el `erase` después de `unique` o `remove_if`.** El vector conserva
su tamaño: los elementos del final son restos sin sentido.

**Goblin: `accumulate` con `0` para decimales.** Trunca cada suma parcial. Usá `0.0`.

**Orco: el destino sin lugar.** `std::copy(a.begin(), a.end(), b.begin())` con `b`
vacío escribe fuera. Usá `std::back_inserter(b)` o dale tamaño antes.

**Orco: `*max_element` de un rango vacío.** Devuelve `end()`: desreferenciarlo es
indefinido.

### Misión R04-N05-M1 · Las notas del examen

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé todas las notas de la entrada con `istream_iterator`. **Sin escribir ningún
bucle**, mostrá: cantidad, promedio (con `accumulate` y `0.0`), mediana (ordenando
una copia; si la cantidad es par, el promedio de las dos del medio), menor y mayor
(`minmax_element`), aprobados (6 o más) y si todos rindieron (ninguna nota 0).
Mostrá las notas ordenadas con `ostream_iterator`.

#### Criterio de aprobación

- No hay bucles escritos a mano.
- La mediana contempla cantidad par e impar.

#### Entrada de ejemplo

```
7 4 10 6 9 2 8 5
```

#### Salida esperada

```
Notas: 8
Promedio: 6.375, mediana: 6.5
Menor: 2, mayor: 10
Aprobados: 5
Todos rindieron
Ordenadas: 2 4 5 6 7 8 9 10 
```

#### Solución de referencia

```cpp
// Mision 1 - Las notas del examen: estadistica con algoritmos, sin bucles escritos a mano.
#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int main()
{
    std::vector<int> notas(std::istream_iterator<int>(std::cin), std::istream_iterator<int>{});
    if (notas.empty()) {
        std::cout << "Sin notas\n";
        return 0;
    }
    double promedio = std::accumulate(notas.begin(), notas.end(), 0.0) / notas.size();
    auto [menor, mayor] = std::minmax_element(notas.begin(), notas.end());
    auto aprobados = std::count_if(notas.begin(), notas.end(), [](int n) { return n >= 6; });
    bool todos_rindieron = std::all_of(notas.begin(), notas.end(), [](int n) { return n >= 1; });

    std::vector<int> ordenadas = notas;
    std::sort(ordenadas.begin(), ordenadas.end());
    double mediana = ordenadas.size() % 2 == 1
                         ? ordenadas[ordenadas.size() / 2]
                         : (ordenadas[ordenadas.size() / 2 - 1] + ordenadas[ordenadas.size() / 2]) / 2.0;

    std::cout << "Notas: " << notas.size() << "\n";
    std::cout << "Promedio: " << promedio << ", mediana: " << mediana << "\n";
    std::cout << "Menor: " << *menor << ", mayor: " << *mayor << "\n";
    std::cout << "Aprobados: " << aprobados << "\n";
    std::cout << (todos_rindieron ? "Todos rindieron" : "Hay ausentes (nota 0)") << "\n";
    std::cout << "Ordenadas: ";
    std::copy(ordenadas.begin(), ordenadas.end(), std::ostream_iterator<int>(std::cout, " "));
    std::cout << "\n";
    return 0;
}
```

#### Pruebas

##### Cantidad impar
```entrada
3 9 6
```
```salida
Notas: 3
Promedio: 6, mediana: 6
Menor: 3, mayor: 9
Aprobados: 2
Todos rindieron
Ordenadas: 3 6 9
```

##### Alguno no rindió
```entrada
0 10 8 6
```
```salida
Notas: 4
Promedio: 6, mediana: 7
Menor: 0, mayor: 10
Aprobados: 3
Hay ausentes (nota 0)
Ordenadas: 0 6 8 10
```

##### Una sola nota
```entrada
10
```
```salida
Notas: 1
Promedio: 10, mediana: 10
Menor: 10, mayor: 10
Aprobados: 1
Todos rindieron
Ordenadas: 10
```

### Misión R04-N05-M2 · El podio de la carrera

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea es un corredor: `nombre segundos`. Mostrá el podio (los 3 más rápidos)
ordenando **solo esos 3** con `std::partial_sort`, el tiempo mediano con
`std::nth_element` (sin ordenar todo) y el último con `max_element`. Usá una única
lambda `mas_rapido` para las tres cosas.

#### Criterio de aprobación

- Usa `partial_sort` y `nth_element`.
- Reutiliza la misma lambda de comparación.
- Funciona con menos de 3 corredores.

#### Entrada de ejemplo

```
Kira 612
Bron 745
Lyn 598
Oto 701
Tesla 588
Ana 650
Fede 830
```

#### Salida esperada

```
1. Tesla (588 s)
2. Lyn (598 s)
3. Kira (612 s)
Tiempo mediano: 650 s (Ana)
Último: Fede
```

#### Solución de referencia

```cpp
// Mision 2 - Los podios: partial_sort y nth_element para no ordenar todo.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Corredor {
    std::string nombre;
    int segundos = 0;
};

int main()
{
    std::vector<Corredor> carrera;
    Corredor c;
    while (std::cin >> c.nombre >> c.segundos) {
        carrera.push_back(c);
    }
    auto mas_rapido = [](const Corredor& a, const Corredor& b) { return a.segundos < b.segundos; };

    std::vector<Corredor> podio = carrera;
    std::size_t k = std::min<std::size_t>(3, podio.size());
    std::partial_sort(podio.begin(), podio.begin() + k, podio.end(), mas_rapido);   // solo los k primeros ordenados
    for (std::size_t i = 0; i < k; i++) {
        std::cout << i + 1 << ". " << podio[i].nombre << " (" << podio[i].segundos << " s)\n";
    }

    std::vector<Corredor> copia = carrera;
    auto medio = copia.begin() + copia.size() / 2;
    std::nth_element(copia.begin(), medio, copia.end(), mas_rapido);   // el del medio, en su lugar
    std::cout << "Tiempo mediano: " << medio->segundos << " s (" << medio->nombre << ")\n";

    auto ultimo = std::max_element(carrera.begin(), carrera.end(), mas_rapido);
    std::cout << "Último: " << ultimo->nombre << "\n";
    return 0;
}
```

#### Pruebas

##### Tres corredores
```entrada
A 300
B 200
C 100
```
```salida
1. C (100 s)
2. B (200 s)
3. A (300 s)
Tiempo mediano: 200 s (B)
Último: A
```

##### Empates de tiempo
```entrada
A 500
B 500
C 400
D 600
```
```salida
1. C (400 s)
2. A (500 s)
3. B (500 s)
Tiempo mediano: 500 s (A)
Último: D
```

### Misión R04-N05-M3 · Los socios en orden

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La lista de socios del club es `{1042, 88, 5310, 713, 2204, 88, 91, 4400}`:
ordenala y quitale los repetidos. Cada número de la entrada es una consulta: con
`std::lower_bound`, decí si es socio y en qué posición; si no lo es, decí cuál es el
siguiente número de socio (si hay) y **agregalo en su lugar**, para que la lista
siga ordenada. Al final, comprobá con `std::is_sorted`.

#### Criterio de aprobación

- Usa `lower_bound` para buscar y para insertar en orden.
- La lista sigue ordenada al final.

#### Entrada de ejemplo

```
713 100 5310 9999 1
```

#### Salida esperada

```
7 socios únicos
713: es socio (posición 2)
100: no es socio; el siguiente número es 713
5310: es socio (posición 7)
9999: no es socio
1: no es socio; el siguiente número es 88
Ahora hay 10, ¿sigue ordenado? sí
```

#### Solución de referencia

```cpp
// Mision 3 - Busqueda binaria en la lista de socios ordenada.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<int> socios = {1042, 88, 5310, 713, 2204, 88, 91, 4400};
    std::sort(socios.begin(), socios.end());
    socios.erase(std::unique(socios.begin(), socios.end()), socios.end());
    std::cout << socios.size() << " socios únicos\n";
    int n = 0;
    while (std::cin >> n) {
        auto it = std::lower_bound(socios.begin(), socios.end(), n);
        if (it != socios.end() && *it == n) {
            std::cout << n << ": es socio (posición " << it - socios.begin() << ")\n";
        } else {
            std::cout << n << ": no es socio";
            if (it != socios.end()) {
                std::cout << "; el siguiente número es " << *it;
            }
            std::cout << "\n";
            socios.insert(it, n);                 // se agrega en su lugar: sigue ordenado
        }
    }
    std::cout << "Ahora hay " << socios.size() << ", ¿sigue ordenado? "
              << (std::is_sorted(socios.begin(), socios.end()) ? "sí" : "no") << "\n";
    return 0;
}
```

#### Pruebas

##### Todos ya socios
```entrada
88 91 5310
```
```salida
7 socios únicos
88: es socio (posición 0)
91: es socio (posición 1)
5310: es socio (posición 6)
Ahora hay 7, ¿sigue ordenado? sí
```

##### Más grande que todos
```entrada
6000 7000
```
```salida
7 socios únicos
6000: no es socio
7000: no es socio
Ahora hay 9, ¿sigue ordenado? sí
```

##### Sin consultas
```entrada
```
```salida
7 socios únicos
Ahora hay 7, ¿sigue ordenado? sí
```

### Encargo R04-N05-E1 · Los invitados del casamiento

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La primera línea es la lista de invitados de la novia; la segunda, la del novio
(pueden tener repetidos). Ordená y quitá los repetidos de cada una, y mostrá con
algoritmos de conjuntos: los invitados por los dos, la lista final (la unión) y los
que invitó solo la novia.

#### Criterio de aprobación

- Usa `set_intersection`, `set_union` y `set_difference` con `back_inserter`.
- Las listas se ordenan y limpian antes.

#### Entrada de ejemplo

```
Ana Beto Caro Dani Ana Eli
Caro Fede Ana Gabi Caro
```

#### Salida esperada

```
Invitados por los dos (2): Ana Caro 
Lista final (7): Ana Beto Caro Dani Eli Fede Gabi 
Solo de la novia (3): Beto Dani Eli 
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Las listas de invitados: interseccion, union y diferencia.
#include <algorithm>
#include <iostream>
#include <iterator>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> leer_lista()
{
    std::string linea;
    std::getline(std::cin, linea);
    std::istringstream in(linea);
    std::vector<std::string> v(std::istream_iterator<std::string>(in), std::istream_iterator<std::string>{});
    std::sort(v.begin(), v.end());
    v.erase(std::unique(v.begin(), v.end()), v.end());
    return v;
}

void mostrar(const std::string& titulo, const std::vector<std::string>& v)
{
    std::cout << titulo << " (" << v.size() << "): ";
    std::copy(v.begin(), v.end(), std::ostream_iterator<std::string>(std::cout, " "));
    std::cout << "\n";
}

int main()
{
    auto novia = leer_lista();
    auto novio = leer_lista();
    std::vector<std::string> ambos, todos, solo_novia;
    std::set_intersection(novia.begin(), novia.end(), novio.begin(), novio.end(), std::back_inserter(ambos));
    std::set_union(novia.begin(), novia.end(), novio.begin(), novio.end(), std::back_inserter(todos));
    std::set_difference(novia.begin(), novia.end(), novio.begin(), novio.end(), std::back_inserter(solo_novia));
    mostrar("Invitados por los dos", ambos);
    mostrar("Lista final", todos);
    mostrar("Solo de la novia", solo_novia);
    return 0;
}
```

#### Pruebas

##### Nadie en común
```entrada
Ana Beto
Caro Dani
```
```salida
Invitados por los dos (0):
Lista final (4): Ana Beto Caro Dani
Solo de la novia (2): Ana Beto
```

##### Listas iguales
```entrada
Ana Beto Ana
Beto Ana
```
```salida
Invitados por los dos (2): Ana Beto
Lista final (2): Ana Beto
Solo de la novia (0):
```

### Prueba del sello

#### ¿Qué hace `std::iota(v.begin(), v.end(), 1)`?

Llena el rango con 1, 2, 3, …

#### ¿Qué diferencia hay entre `sort` y `stable_sort`?

`stable_sort` respeta el orden original entre elementos iguales; `sort` no lo garantiza.

#### ¿Por qué `binary_search` exige un rango ordenado?

Porque parte el rango por la mitad suponiendo el orden; si no está ordenado, el resultado no sirve.

#### ¿Por qué `unique` necesita un `erase` después?

Porque no borra: corre los repetidos al final y devuelve dónde empiezan.

#### ¿Cuándo conviene `partial_sort` en vez de `sort`?

Cuando solo se necesitan los primeros k ordenados (un podio, un top 10).

### Soluciones (docente)

Material original: `11-STL/06-Algoritmos`.

## R04-N06 · Functores y std::function

```meta
tipo: tema
padre: R04-N05
precio: 10
criatura: esqueleto
temas: func.orden-superior
usa: func.lambdas
```

### Crónica

En la sala de control de la Biblioteca hay un tablero de palancas. Cada palanca tiene una tarjeta enganchada: "encender la caldera", "abrir la compuerta", "tocar la campana". Las tarjetas se pueden cambiar sin tocar el tablero.

—Una acción también puede ser un **dato** —dice {mentor}—: se guarda en una caja, se pasa de mano en mano, se cuelga de una palanca. Cuando alguien tira, pasa lo que dice la tarjeta.

### Objetivos

Escribir **functores** (objetos que se llaman como funciones y guardan estado),
entender que una lambda es un functor que escribe el compilador, y guardar
cualquier cosa "llamable" en un `std::function` para armar tablas de comandos,
listas de reglas y un sistema de eventos.

### Antes de empezar

- Lambdas (rama 3) y algoritmos (nodo anterior).
- Operadores para tus clases (rama 2).

### Explicación

#### Functores: objetos que se llaman
Un **functor** es un objeto de una clase que tiene `operator()`:
```cpp
struct MultiplicarPor {
    int factor;
    void operator()(int& n) const { n *= factor; }
};
MultiplicarPor triple{3};
int x = 5;
triple(x);                                            // x vale 15
std::for_each(v.begin(), v.end(), MultiplicarPor{10});
```
La diferencia con una función: **guarda estado** en sus miembros (`factor`). Un
functor puede ir acumulando mientras recorre, y `std::for_each` **devuelve** el
functor al final para que leas lo que juntó.

#### Una lambda es un functor
Cuando escribís `[factor](int& n) { n *= factor; }`, el compilador crea una clase
con un miembro `factor` y un `operator()`. Las capturas son los miembros. Hoy se
usan lambdas para casi todo; los functores con nombre siguen apareciendo como
**comparadores** de contenedores (`std::greater<int>`, el tercer parámetro de un
`set` o una `priority_queue`) y cuando la misma lógica se reutiliza en muchos
lugares.

#### `std::function`: una caja para cualquier cosa llamable
Cada lambda tiene su propio tipo, que no se puede escribir. Para guardar "algo
que se llama con dos `double` y devuelve un `double`", sea lo que sea, está
`std::function` (de `<functional>`):
```cpp
std::function<double(double, double)> op = [](double a, double b) { return a + b; };
op(3, 4);                                   // 7
op = [](double a, double b) { return a * b; };   // otra, con la misma forma
```
Entre `< >` va la **forma** (la firma): lo que devuelve y, entre paréntesis, lo que
recibe. Se puede guardar una función común, una lambda (con o sin capturas) o un
functor. Un `std::function` vacío se puede preguntar con `if (op)`.

#### Acciones como datos
- **Tabla de comandos**: `std::map<std::string, std::function<...>>`: la entrada
  elige qué acción ejecutar, y agregar un comando es agregar una entrada.
- **Listas de reglas**: un vector de structs con una condición y una acción, que se
  aplican en orden.
- **Eventos** (el patrón *observador*): unos se **suscriben** con una función a un
  evento ("golpe"), otro lo **emite**, y se llaman todas las funciones suscriptas.
  Quien emite no conoce a quien escucha: el sonido, la salud y la interfaz de un
  juego no dependen unos de otros.

#### El costo
`std::function` tiene un pequeño costo (como una llamada virtual). En un algoritmo
que recibe una lambda directa (`std::sort(..., [](...){...})`), no lo uses: pasá la
lambda. Usalo cuando tenés que **guardar** la acción.

> **Si venís de C.** Es un puntero a función, pero puede guardar también lambdas
> con capturas y functores con estado.

### Código de ejemplo

```cpp
/*
 * Functores y std::function: acciones que se guardan, se pasan y se eligen.
 */
#include <algorithm>
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>

// Un FUNCTOR: un objeto que se llama como una funcion (tiene operator()) y guarda estado.
struct MultiplicarPor {
    int factor;
    void operator()(int& n) const { n *= factor; }
};

struct ContarPares {
    int pares = 0;
    void operator()(int n)
    {
        if (n % 2 == 0) {
            pares++;
        }
    }
};

// Un bus de eventos: los sistemas se suscriben con una funcion; otro emite.
class Eventos {
public:
    using Oyente = std::function<void(int)>;
    void suscribir(const std::string& evento, Oyente f) { oyentes_[evento].push_back(std::move(f)); }
    void emitir(const std::string& evento, int dato)
    {
        for (auto& f : oyentes_[evento]) {
            f(dato);
        }
    }

private:
    std::map<std::string, std::vector<Oyente>> oyentes_;
};

int main()
{
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::for_each(v.begin(), v.end(), MultiplicarPor{10});
    ContarPares c = std::for_each(v.begin(), v.end(), ContarPares{});    // for_each devuelve el functor
    std::cout << "x10:";
    for (int x : v) {
        std::cout << " " << x;
    }
    std::cout << " (pares: " << c.pares << ")\n";

    // std::function: una "caja" para cualquier cosa que se pueda llamar con esa forma
    std::function<int(int, int)> op = [](int a, int b) { return a + b; };
    std::cout << "op(3, 4) = " << op(3, 4) << "\n";
    int bonus = 100;
    op = [bonus](int a, int b) { return a * b + bonus; };                // otra lambda, misma forma
    std::cout << "op(3, 4) = " << op(3, 4) << "\n";

    // Una tabla de comandos: tecla -> accion
    int oro = 50;
    std::map<char, std::function<void()>> comandos = {
        {'c', [&oro] { oro -= 10; std::cout << "  compra (oro " << oro << ")\n"; }},
        {'v', [&oro] { oro += 20; std::cout << "  vende (oro " << oro << ")\n"; }},
    };
    for (char tecla : std::string("cvvxc")) {
        auto it = comandos.find(tecla);
        if (it != comandos.end()) {
            it->second();
        } else {
            std::cout << "  '" << tecla << "' no hace nada\n";
        }
    }

    // Eventos: salud y sonido no se conocen entre si
    Eventos bus;
    int vida = 100;
    bus.suscribir("golpe", [&vida](int d) { vida -= d; std::cout << "  [salud] vida " << vida << "\n"; });
    bus.suscribir("golpe", [](int) { std::cout << "  [sonido] ¡pum!\n"; });
    bus.emitir("golpe", 30);
    bus.emitir("golpe", 25);
    return 0;
}
```

### Salida esperada

```
x10: 10 20 30 40 50 (pares: 5)
op(3, 4) = 7
op(3, 4) = 112
  compra (oro 40)
  vende (oro 60)
  vende (oro 80)
  'x' no hace nada
  compra (oro 70)
  [salud] vida 70
  [sonido] ¡pum!
  [salud] vida 45
  [sonido] ¡pum!
```

### ¿Para qué sirve?

Guardar acciones es la base de las interfaces gráficas (cada botón guarda qué hacer cuando lo tocan: lo vas a ver en la Senda de Qt), de los sistemas de eventos de los motores de juegos, de los atajos de teclado configurables, de los motores de reglas de negocio (descuentos, validaciones, permisos) y de las tareas programadas ("dentro de 5 minutos, hacé esto").

### Errores habituales

**Ogro: llamar a un `std::function` vacío.** Lanza una excepción
(`std::bad_function_call`) y, si nadie la atrapa, el programa se corta. Preguntá
`if (f)` si puede estar vacío.

**Troll: la lambda guardada que capturó por referencia algo que murió.** Un
`std::function` guardado en un bus de eventos que capturó `[&vida]` de una función
que ya terminó: cuando se emita el evento, `vida` ya no existe. Capturá por copia,
o asegurate de que la variable viva más que la suscripción.

**Goblin: la forma no coincide.** Guardar en `std::function<void(int)>` una lambda
que recibe un `std::string` no compila (el mensaje menciona una conversión
imposible).

**Ogro: el functor sin `const`.** Un comparador de `set` o `priority_queue` tiene
que tener `operator()` `const`; si no, no compila.

**Ogro: `for_each` y el estado perdido.** `std::for_each` trabaja con una **copia**
del functor: el estado queda en la copia que devuelve. Si no guardás el valor de
retorno, perdés lo que contó.

### Misión R04-N06-M1 · Functores con estado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé números de la entrada. Escribí el functor `Estadistica` (con cantidad, suma y
máximo, y un método `promedio()`) y aplicalo con `std::for_each`, guardando lo que
devuelve. Escribí el functor `EnRango{desde, hasta}` y usalo con `count_if` para
contar los que están entre 10 y 30 y entre 0 y 9.

#### Criterio de aprobación

- Usa el functor que devuelve `for_each`.
- `EnRango` se configura en su construcción y su `operator()` es `const`.

#### Entrada de ejemplo

```
12 5 33 18 30 7 25 41 10
```

#### Salida esperada

```
9 datos, suma 181, máximo 41, promedio 20.1111
Entre 10 y 30: 5
Entre 0 y 9: 2
```

#### Solución de referencia

```cpp
// Mision 1 - Functores con estado: contar, sumar y promediar en una pasada.
#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>

struct Estadistica {
    int cantidad = 0;
    long long suma = 0;
    int maximo = 0;
    void operator()(int x)
    {
        if (cantidad == 0 || x > maximo) {
            maximo = x;
        }
        cantidad++;
        suma += x;
    }
    double promedio() const { return cantidad == 0 ? 0 : static_cast<double>(suma) / cantidad; }
};

struct EnRango {
    int desde;
    int hasta;
    bool operator()(int x) const { return desde <= x && x <= hasta; }
};

int main()
{
    std::vector<int> v(std::istream_iterator<int>(std::cin), std::istream_iterator<int>{});
    Estadistica e = std::for_each(v.begin(), v.end(), Estadistica{});
    std::cout << e.cantidad << " datos, suma " << e.suma << ", máximo " << e.maximo << ", promedio " << e.promedio() << "\n";
    EnRango normal{10, 30};
    std::cout << "Entre 10 y 30: " << std::count_if(v.begin(), v.end(), normal) << "\n";
    std::cout << "Entre 0 y 9: " << std::count_if(v.begin(), v.end(), EnRango{0, 9}) << "\n";
    return 0;
}
```

#### Pruebas

##### Bordes del rango
```entrada
0 9 10 30 31
```
```salida
5 datos, suma 80, máximo 31, promedio 16
Entre 10 y 30: 2
Entre 0 y 9: 2
```

##### Un solo dato
```entrada
100
```
```salida
1 datos, suma 100, máximo 100, promedio 100
Entre 10 y 30: 0
Entre 0 y 9: 0
```

### Misión R04-N06-M2 · La calculadora de comandos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá un `std::map<std::string, std::function<double(double, double)>>` con las
operaciones `suma`, `resta`, `por`, `potencia` e `hipotenusa`, y agregá `promedio`
después de crear el map. Cada línea de la entrada es `operacion a b`: ejecutala o
avisá que no existe. Al final, listá las operaciones.

#### Criterio de aprobación

- Las operaciones son lambdas guardadas en el map.
- Agregar una operación no cambia el bucle principal.

#### Entrada de ejemplo

```
suma 3 4
potencia 2 10
hipotenusa 3 4
raiz 9 0
promedio 7 10
```

#### Salida esperada

```
suma(3, 4) = 7
potencia(2, 10) = 1024
hipotenusa(3, 4) = 5
raiz: no existe
promedio(7, 10) = 8.5
Operaciones: hipotenusa por potencia promedio resta suma
```

#### Solución de referencia

```cpp
// Mision 2 - La calculadora de comandos: un map de texto a std::function.
#include <cmath>
#include <functional>
#include <iostream>
#include <map>
#include <string>

int main()
{
    std::map<std::string, std::function<double(double, double)>> ops = {
        {"suma", [](double a, double b) { return a + b; }},
        {"resta", [](double a, double b) { return a - b; }},
        {"por", [](double a, double b) { return a * b; }},
        {"potencia", [](double a, double b) { return std::pow(a, b); }},
        {"hipotenusa", [](double a, double b) { return std::hypot(a, b); }},
    };
    ops["promedio"] = [](double a, double b) { return (a + b) / 2; };     // se agregan en cualquier momento

    std::string nombre;
    double a = 0, b = 0;
    while (std::cin >> nombre >> a >> b) {
        auto it = ops.find(nombre);
        if (it == ops.end()) {
            std::cout << nombre << ": no existe\n";
        } else {
            std::cout << nombre << "(" << a << ", " << b << ") = " << it->second(a, b) << "\n";
        }
    }
    std::cout << "Operaciones:";
    for (const auto& [n, f] : ops) {
        std::cout << " " << n;
    }
    std::cout << "\n";
    return 0;
}
```

#### Pruebas

##### Negativos y decimales
```entrada
resta 2.5 10
por -3 4
```
```salida
resta(2.5, 10) = -7.5
por(-3, 4) = -12
Operaciones: hipotenusa por potencia promedio resta suma
```

##### Ninguna existe
```entrada
dividir 1 2
```
```salida
dividir: no existe
Operaciones: hipotenusa por potencia promedio resta suma
```

##### Sin órdenes
```entrada
```
```salida
Operaciones: hipotenusa por potencia promedio resta suma
```

### Misión R04-N06-M3 · El bus de eventos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Eventos` donde `suscribir(evento, funcion)` devuelve un número de
suscripción y `desuscribir(evento, numero)` la quita. Guardá las funciones en un
`std::map<std::string, std::map<int, std::function<...>>>`. Suscribí: los puntos
(suman la moneda), un festejo (`¡+N!`) y los logros (al vencer un jefe). Cada línea
de la entrada es `evento dato`; el evento especial `silencio` desuscribe el festejo.
Al final, puntos y logros.

#### Criterio de aprobación

- `suscribir` devuelve un identificador y `desuscribir` lo usa.
- Quien emite no sabe quién escucha.

#### Entrada de ejemplo

```
moneda 10
moneda 5
jefe Autómata
silencio x
moneda 20
jefe Quimera
```

#### Salida esperada

```
  ¡+10!
  ¡+5!
  logro: venciste a Autómata
  (sin festejos)
  logro: venciste a Quimera
Puntos: 35, logros: 2
```

#### Solución de referencia

```cpp
// Mision 3 - El bus de eventos del juego: suscribir y desuscribir.
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <utility>

class Eventos {
public:
    using Oyente = std::function<void(const std::string&)>;

    int suscribir(const std::string& evento, Oyente f)
    {
        int id = siguiente_++;
        oyentes_[evento][id] = std::move(f);
        return id;
    }

    void desuscribir(const std::string& evento, int id) { oyentes_[evento].erase(id); }

    void emitir(const std::string& evento, const std::string& dato)
    {
        for (auto& [id, f] : oyentes_[evento]) {
            f(dato);
        }
    }

private:
    int siguiente_ = 1;
    std::map<std::string, std::map<int, Oyente>> oyentes_;
};

int main()
{
    Eventos bus;
    int puntos = 0;
    int logros = 0;
    bus.suscribir("moneda", [&puntos](const std::string& d) { puntos += std::stoi(d); });
    int festejo = bus.suscribir("moneda", [](const std::string& d) { std::cout << "  ¡+" << d << "!\n"; });
    bus.suscribir("jefe", [&logros](const std::string& quien) { logros++; std::cout << "  logro: venciste a " << quien << "\n"; });

    std::string evento, dato;
    while (std::cin >> evento >> dato) {
        if (evento == "silencio") {
            bus.desuscribir("moneda", festejo);
            std::cout << "  (sin festejos)\n";
            continue;
        }
        bus.emitir(evento, dato);
    }
    std::cout << "Puntos: " << puntos << ", logros: " << logros << "\n";
    return 0;
}
```

#### Pruebas

##### Silencio de entrada
```entrada
silencio x
moneda 50
```
```salida
  (sin festejos)
Puntos: 50, logros: 0
```

##### Solo jefes
```entrada
jefe Hidra
jefe Kraken
```
```salida
  logro: venciste a Hidra
  logro: venciste a Kraken
Puntos: 0, logros: 2
```

##### Evento desconocido
```entrada
tesoro 100
moneda 1
```
```salida
  ¡+1!
Puntos: 1, logros: 0
```

### Encargo R04-N06-E1 · Las reglas de descuento

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un comercio aplica, en orden, las reglas de descuento que correspondan: "socio 10%"
(si es socio), "miércoles 2x" (15% si es miércoles y lleva 2 o más artículos) y
"compra grande −$500" (si el total original es de $10000 o más). Cada regla es un
struct con un nombre y dos `std::function`: una condición y el descuento. Cada línea
de la entrada es `total articulos si|no dia`; mostrá las reglas aplicadas y el
total final.

#### Criterio de aprobación

- Las reglas están en un vector y se aplican en orden.
- Agregar una regla no cambia el bucle.

#### Entrada de ejemplo

```
8000 1 si lunes
12000 3 no miercoles
15000 2 si miercoles
500 1 no sabado
```

#### Salida esperada

```
$8000.00: [socio 10%] -> $7200.00
$12000.00: [miércoles 2x] [compra grande -$500] -> $9700.00
$15000.00: [socio 10%] [miércoles 2x] [compra grande -$500] -> $10975.00
$500.00: -> $500.00
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Las reglas de descuento: una lista de std::function que se aplican en orden.
#include <functional>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Compra {
    double total = 0;
    int articulos = 0;
    bool socio = false;
    std::string dia;
};

struct Regla {
    std::string nombre;
    std::function<bool(const Compra&)> aplica;
    std::function<double(double)> descuento;
};

int main()
{
    const std::vector<Regla> reglas = {
        {"socio 10%", [](const Compra& c) { return c.socio; }, [](double t) { return t * 0.9; }},
        {"miércoles 2x", [](const Compra& c) { return c.dia == "miercoles" && c.articulos >= 2; }, [](double t) { return t * 0.85; }},
        {"compra grande -$500", [](const Compra& c) { return c.total >= 10000; }, [](double t) { return t - 500; }},
    };
    std::cout << std::fixed << std::setprecision(2);
    Compra c;
    std::string socio;
    while (std::cin >> c.total >> c.articulos >> socio >> c.dia) {
        c.socio = (socio == "si");
        double final = c.total;
        std::cout << "$" << c.total << ":";
        for (const auto& r : reglas) {
            if (r.aplica(c)) {
                final = r.descuento(final);
                std::cout << " [" << r.nombre << "]";
            }
        }
        std::cout << " -> $" << final << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Socio con compra grande sin miércoles
```entrada
20000 1 si martes
```
```salida
$20000.00: [socio 10%] [compra grande -$500] -> $17500.00
```

##### Miércoles con un solo artículo
```entrada
5000 1 no miercoles
```
```salida
$5000.00: -> $5000.00
```

##### Justo 10000
```entrada
10000 1 no lunes
```
```salida
$10000.00: [compra grande -$500] -> $9500.00
```

### Prueba del sello

#### ¿Qué es un functor?

Un objeto de una clase con `operator()`: se llama como una función y puede guardar estado.

#### ¿Qué relación hay entre una lambda y un functor?

Una lambda es un functor que el compilador escribe por vos; sus capturas son los miembros.

#### ¿Qué puede guardar un `std::function<int(int)>`?

Cualquier cosa que se llame con un `int` y devuelva un `int`: una función, una lambda o un functor.

#### ¿Qué pasa si llamás a un `std::function` vacío?

Lanza `std::bad_function_call`.

#### ¿Para qué sirve un bus de eventos?

Para que distintas partes del programa reaccionen a un evento sin conocerse entre sí.

### Soluciones (docente)

Material original: `11-STL/07-Functores-Lambdas` y `09-Functional`, con el ejercicio de desuscribir resuelto.

## R04-N07 · Vistas y ranges

```meta
tipo: tema
padre: R04-N06
precio: 10
criatura: troll
temas: func.streams
```

### Crónica

En la sala de lectura de la Biblioteca nadie se lleva los libros: se usa un **lente**. Apuntás el lente a una página y leés sin copiarla. Y los lentes se pueden encadenar: uno que solo muestra los capítulos de mapas, otro que solo muestra los títulos, otro que solo deja ver los tres primeros.

—Un lente no es dueño de nada —advierte {mentor}—. Si alguien se lleva el libro mientras mirás, el lente muestra el vacío. Pero bien usados, te ahorran copiar bibliotecas enteras.

### Objetivos

Usar **vistas** que miran datos sin copiarlos: `std::string_view` para textos y
`std::span` para secuencias; usar los algoritmos de `std::ranges` con proyecciones;
y encadenar **views** perezosas (`filter`, `transform`, `take`, `drop`, `reverse`,
`iota`, `keys`) con `|`.

### Antes de empezar

- Textos, lambdas y algoritmos (ramas 3 y 4).
- Iteradores (Iteradores).

### Explicación

#### `std::string_view`: mirar un texto sin copiarlo
Un `std::string_view` (de `<string_view>`) es un par "dónde empieza, cuánto mide"
que **mira** un texto de otro. Como parámetro acepta `std::string`, literales
`"..."` y pedazos de texto, **sin copiar**:
```cpp
int contar_vocales(std::string_view s);
contar_vocales(nombre);          // un std::string
contar_vocales("murciélago");    // un literal: sin crear un std::string
```
Tiene casi todo lo de `std::string` para leer (`size`, `find`, `substr`, `[]`,
`starts_with`), y su `substr` **no copia**. Además, `remove_prefix(n)` y
`remove_suffix(n)` achican la vista (no el texto).

#### `std::span<T>`: lo mismo para secuencias
Un `std::span` (de `<span>`) mira una secuencia **contigua** de elementos: un
`vector`, un `array` o un pedazo de ellos.
```cpp
int suma(std::span<const int> datos);    // lee (const)
void normalizar(std::span<double> datos); // puede modificar lo que mira
suma(v);   suma(arr);   suma(std::span(v).subspan(2, 3));   std::span(v).first(3);
```

#### La regla de oro de las vistas
Una vista **no es dueña**: si el dato original muere, la vista queda colgando.
- Usalas **como parámetros** (ahí son perfectas: el dato vive mientras dura la
  llamada).
- **No** las guardes más allá de la vida del dato.
- **Nunca** devuelvas una vista a una variable local ni la hagas a partir de un
  `std::string` temporal.

#### `std::ranges`: algoritmos que reciben el contenedor
Desde C++20, casi todos los algoritmos tienen una versión en `std::ranges` que
recibe el contenedor entero y acepta una **proyección** (qué campo comparar):
```cpp
std::ranges::sort(horda);                                  // en vez de sort(begin, end)
std::ranges::sort(horda, {}, &Enemigo::vida);              // ordenar por el campo vida
std::ranges::sort(gremio, std::ranges::greater{}, &Artifice::nivel);   // de mayor a menor
std::ranges::find(gremio, "vapor", &Artifice::taller);     // buscar por un campo
std::ranges::count_if(v, pred);
```

#### Views: transformaciones perezosas y encadenables
Una **view** (de `<ranges>`) es una "receta" que se aplica **recién al recorrer**,
sin crear contenedores intermedios. Se encadenan con `|` y se leen de izquierda a
derecha:
```cpp
auto nombres = horda
    | std::views::filter([](const Enemigo& e) { return e.vivo(); })
    | std::views::transform([](const Enemigo& e) { return e.nombre; });
for (const auto& n : nombres) { ... }       // recién acá se filtra y transforma
```
| View | Qué hace |
|---|---|
| `std::views::filter(pred)` | deja pasar los que cumplen |
| `std::views::transform(f)` | cambia cada uno por `f(x)` |
| `std::views::take(n)` / `drop(n)` | los primeros `n` / saltea los primeros `n` |
| `std::views::reverse` | al revés |
| `std::views::iota(a, b)` | los números de `a` a `b - 1` (sin guardarlos) |
| `std::views::keys` / `values` | las claves / los valores de un `map` |

Las views también **miran**: el contenedor tiene que seguir vivo mientras las
usás. Para guardar el resultado, recorrelo y cargá un vector.

> **Si venís de C.** `string_view` y `span` son lo que en C era "puntero + largo",
> pero con tipos y con todos los métodos. Las views no tienen equivalente: en C
> cada paso era un bucle y un array intermedio.

### Código de ejemplo

```cpp
/*
 * Vistas: string_view y span miran datos sin copiarlos; ranges los encadenan.
 */
#include <algorithm>
#include <iostream>
#include <map>
#include <ranges>
#include <span>
#include <string>
#include <string_view>
#include <vector>

// Acepta std::string, literales y pedazos de texto, sin copiar nada.
int contar_vocales(std::string_view s)
{
    int n = 0;
    for (char c : s) {
        if (std::string_view("aeiouAEIOU").find(c) != std::string_view::npos) {
            n++;
        }
    }
    return n;
}

// Acepta vector, array o un pedazo de ellos.
int suma(std::span<const int> datos)
{
    int total = 0;
    for (int x : datos) {
        total += x;
    }
    return total;
}

struct Enemigo {
    std::string nombre;
    int vida;
    bool vivo() const { return vida > 0; }
};

int main()
{
    std::string nombre = "Kira de la Ciudadela";
    std::cout << "vocales: " << contar_vocales(nombre) << " y " << contar_vocales("murciélago") << "\n";
    std::string_view sv = nombre;
    std::cout << "el apellido, sin copiar: " << sv.substr(8) << "\n";

    std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8};
    std::cout << "suma de todo: " << suma(v) << ", del medio: " << suma(std::span(v).subspan(2, 3)) << "\n";

    // ranges: algoritmos que reciben el contenedor entero
    std::vector<Enemigo> horda = {{"orco", 55}, {"slime", 0}, {"goblin", 35}, {"rata", 8}, {"troll", 90}};
    std::ranges::sort(horda, {}, &Enemigo::vida);        // ordenar POR un campo (proyeccion)
    std::cout << "por vida:";
    for (const auto& e : horda) {
        std::cout << " " << e.nombre;
    }
    std::cout << "\n";

    // views: transformaciones PEREZOSAS y encadenables con |
    auto vivos_fuertes = horda
        | std::views::filter([](const Enemigo& e) { return e.vivo(); })
        | std::views::filter([](const Enemigo& e) { return e.vida >= 30; })
        | std::views::transform([](const Enemigo& e) { return e.nombre; });
    std::cout << "vivos con 30 o más:";
    for (const auto& n : vivos_fuertes) {                // recien aca se hace el trabajo
        std::cout << " " << n;
    }
    std::cout << "\n";

    std::cout << "cuadrados de los pares del 1 al 20, los 4 primeros:";
    for (int x : std::views::iota(1, 21)
                     | std::views::filter([](int n) { return n % 2 == 0; })
                     | std::views::transform([](int n) { return n * n; })
                     | std::views::take(4)) {
        std::cout << " " << x;
    }
    std::cout << "\n";

    std::map<std::string, int> oro = {{"Bron", 12}, {"Kira", 50}, {"Lyn", 30}};
    std::cout << "héroes:";
    for (const auto& n : std::views::keys(oro)) {
        std::cout << " " << n;
    }
    std::cout << " | al revés:";
    for (int x : v | std::views::reverse | std::views::drop(5)) {
        std::cout << " " << x;
    }
    std::cout << "\n";
    return 0;
}
```

### Salida esperada

```
vocales: 9 y 4
el apellido, sin copiar: la Ciudadela
suma de todo: 36, del medio: 12
por vida: slime rata goblin orco troll
vivos con 30 o más: goblin orco troll
cuadrados de los pares del 1 al 20, los 4 primeros: 4 16 36 64
héroes: Bron Kira Lyn | al revés: 3 2 1
```

### ¿Para qué sirve?

Las vistas se usan en todo código que procesa muchos datos sin querer copiarlos: analizadores de archivos de texto y logs, lectores de protocolos de red, motores de juegos que pasan pedazos de arrays de vértices, procesamiento de audio. Los ranges hacen que las consultas sobre colecciones ("los 5 clientes con más compras que viven en La Rioja") se escriban como se piensan, en una línea que se lee de izquierda a derecha.

### Errores habituales

**Troll: devolver una vista de algo local.** No hay aviso con `-Wall`: el programa
compila y lee memoria liberada. El sanitizador lo encuentra:
```
==3314202==ERROR: AddressSanitizer: heap-use-after-free on address 0x502000000018
```

**Troll: una vista de un temporal.**
`std::string_view sv = std::string("hola") + "!";` mira un texto que muere al final
de esa misma línea.

**Troll: la vista de un vector que después crece.** Un `span` a un vector que hace
`push_back` puede quedar mirando la memoria vieja.

**Ogro: pensar que la view ya hizo el trabajo.** Una view no calcula nada hasta que
se recorre; si la recorrés dos veces, calcula dos veces.

**Goblin: `string_view` no termina en `'\0'`.** Si una función vieja de C necesita
un texto terminado en cero, `sv.data()` no sirve: pasale un `std::string(sv)`.

### Misión R04-N07-M1 · Partir sin copiar

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `partir(std::string_view texto, char sep)`, que devuelve un
`std::vector<std::string_view>` con los pedazos (incluidos los vacíos entre dos
separadores seguidos), y `recortar(std::string_view)`, que quita los espacios de
las puntas con `remove_prefix`/`remove_suffix`. Cada línea de la entrada es un
registro separado por comas: mostrá cuántos campos tiene y cada uno recortado
entre corchetes.

#### Criterio de aprobación

- Ninguna función copia texto: todo son vistas.
- El `std::string` de la línea sigue vivo mientras se usan las vistas.
- Contempla campos vacíos.

#### Entrada de ejemplo

```
Kira, artífice , 27
Bron,,guerrero
  solo  
```

#### Salida esperada

```
3 campos: [Kira] [artífice] [27]
3 campos: [Bron] [] [guerrero]
1 campos: [solo]
```

#### Solución de referencia

```cpp
// Mision 1 - Partir sin copiar: split con string_view.
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

std::vector<std::string_view> partir(std::string_view texto, char sep)
{
    std::vector<std::string_view> partes;
    std::size_t inicio = 0;
    while (true) {
        std::size_t pos = texto.find(sep, inicio);
        partes.push_back(texto.substr(inicio, pos - inicio));
        if (pos == std::string_view::npos) {
            break;
        }
        inicio = pos + 1;
    }
    return partes;
}

std::string_view recortar(std::string_view s)
{
    while (!s.empty() && s.front() == ' ') {
        s.remove_prefix(1);
    }
    while (!s.empty() && s.back() == ' ') {
        s.remove_suffix(1);
    }
    return s;
}

int main()
{
    std::string linea;                                  // el texto VIVE aca: las vistas lo miran
    while (std::getline(std::cin, linea)) {
        auto campos = partir(linea, ',');
        std::cout << campos.size() << " campos:";
        for (auto c : campos) {
            std::cout << " [" << recortar(c) << "]";
        }
        std::cout << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Campos vacíos
```entrada
,,
```
```salida
3 campos: [] [] []
```

##### Sin comas y con espacios
```entrada
   a b c
```
```salida
1 campos: [a b c]
```

##### Coma al final
```entrada
uno,dos,
```
```salida
3 campos: [uno] [dos] []
```

### Misión R04-N07-M2 · Normalizar con span

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `normalizar(std::span<double>)`, que divide cada valor por el mayor
(si el mayor es 0, no hace nada), y `mostrar(std::span<const double>)`.
Normalizá un `vector` de lecturas de un sensor, un `std::array` de viento y solo los
**3 primeros** de otro vector (con `std::span(v).first(3)`). Todo con 2 decimales.

#### Criterio de aprobación

- Las mismas funciones sirven para `vector` y `array`.
- La versión que modifica recibe `span<double>` y la que lee `span<const double>`.

#### Salida esperada

```
sensor: 0.40 1.00 0.80 0.20 0.50
viento: 0.08 0.25 0.50 1.00
temps (3 primeros): 0.25 0.50 1.00 5.00 8.00
```

#### Solución de referencia

```cpp
// Mision 2 - Normalizar lecturas con span: la funcion no sabe si es vector o array.
#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <span>
#include <vector>

void normalizar(std::span<double> datos)
{
    if (datos.empty()) {
        return;
    }
    double mayor = *std::max_element(datos.begin(), datos.end());
    if (mayor == 0) {
        return;
    }
    for (double& x : datos) {
        x /= mayor;
    }
}

void mostrar(std::span<const double> datos)
{
    for (double x : datos) {
        std::cout << " " << x;
    }
    std::cout << "\n";
}

int main()
{
    std::cout << std::fixed << std::setprecision(2);
    std::vector<double> sensor = {12, 30, 24, 6, 15};
    std::array<double, 4> viento = {3, 9, 18, 36};
    normalizar(sensor);
    normalizar(viento);
    std::cout << "sensor:";
    mostrar(sensor);
    std::cout << "viento:";
    mostrar(viento);
    std::vector<double> temps = {10, 20, 40, 5, 8};
    normalizar(std::span(temps).first(3));              // solo los 3 primeros
    std::cout << "temps (3 primeros):";
    mostrar(temps);
    return 0;
}
```

### Misión R04-N07-M3 · Consultas al Gremio

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea trae un artífice: `nombre taller nivel`. Ordenalos de mayor a menor
nivel con `std::ranges::sort` y una proyección. Con views, mostrá: los 3 de mayor
nivel (`take`), los nombres del taller de "relojes" (`filter` + `transform`),
cuántos aprendices hay (nivel menor que 3, con `std::ranges::count_if`) y el primero
del taller de "vapor" (con `std::ranges::find` y una proyección).

#### Criterio de aprobación

- Usa proyecciones (`&Artifice::nivel`, `&Artifice::taller`).
- Encadena views con `|`.

#### Entrada de ejemplo

```
Kira relojes 5
Bron vapor 7
Lyn relojes 2
Oto vapor 3
Tesla faros 10
Ana relojes 1
```

#### Salida esperada

```
Los 3 de mayor nivel: Tesla(10) Bron(7) Kira(5)
Del taller de relojes: Kira Lyn Ana
Aprendices: 2
El de más nivel en vapor: Bron
```

#### Solución de referencia

```cpp
// Mision 3 - Consultas con ranges sobre la tabla de artifices.
#include <algorithm>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

struct Artifice {
    std::string nombre;
    std::string taller;
    int nivel = 0;
};

int main()
{
    std::vector<Artifice> gremio;
    Artifice a;
    while (std::cin >> a.nombre >> a.taller >> a.nivel) {
        gremio.push_back(a);
    }
    std::ranges::sort(gremio, std::ranges::greater{}, &Artifice::nivel);

    std::cout << "Los 3 de mayor nivel:";
    for (const auto& x : gremio | std::views::take(3)) {
        std::cout << " " << x.nombre << "(" << x.nivel << ")";
    }
    std::cout << "\n";

    std::cout << "Del taller de relojes:";
    for (const auto& n : gremio
                             | std::views::filter([](const Artifice& x) { return x.taller == "relojes"; })
                             | std::views::transform([](const Artifice& x) { return x.nombre; })) {
        std::cout << " " << n;
    }
    std::cout << "\n";

    auto aprendices = std::ranges::count_if(gremio, [](const Artifice& x) { return x.nivel < 3; });
    auto primero_vapor = std::ranges::find(gremio, "vapor", &Artifice::taller);
    std::cout << "Aprendices: " << aprendices << "\n";
    if (primero_vapor != gremio.end()) {
        std::cout << "El de más nivel en vapor: " << primero_vapor->nombre << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Nadie de relojes ni de vapor
```entrada
Tesla faros 10
Edison faros 9
```
```salida
Los 3 de mayor nivel: Tesla(10) Edison(9)
Del taller de relojes:
Aprendices: 0
```

##### Todos aprendices
```entrada
A relojes 1
B vapor 2
```
```salida
Los 3 de mayor nivel: B(2) A(1)
Del taller de relojes: A
Aprendices: 2
El de más nivel en vapor: B
```

### Encargo R04-N07-E1 · El log del servidor

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Cada línea de un log tiene la forma `[NIVEL] mensaje` (o está rota). Escribí
`analizar(std::string_view)`, que separa el nivel y el mensaje (las líneas sin
corchetes van con nivel `?`). Mostrá cuántas líneas hay de cada nivel y, con views,
los mensajes de los `ERROR`.

#### Criterio de aprobación

- El análisis usa `string_view` y solo copia al guardar el resultado.
- Los errores se listan con `filter` + `transform`.

#### Entrada de ejemplo

```
[INFO] servidor iniciado
[ERROR] no se pudo abrir la base
[WARN] memoria al 80%
línea rota sin nivel
[INFO] 12 usuarios conectados
[ERROR] tiempo agotado en /pedidos
```

#### Salida esperada

```
?: 1
ERROR: 2
INFO: 2
WARN: 1
Errores:
  no se pudo abrir la base
  tiempo agotado en /pedidos
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El log del servidor: analizar lineas con string_view y ranges.
#include <algorithm>
#include <iostream>
#include <map>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>

struct Entrada {
    std::string nivel;
    std::string mensaje;
};

Entrada analizar(std::string_view linea)
{
    std::size_t abre = linea.find('[');
    std::size_t cierra = linea.find(']');
    if (abre == std::string_view::npos || cierra == std::string_view::npos || cierra < abre) {
        return {"?", std::string(linea)};
    }
    std::string_view resto = linea.substr(cierra + 1);
    while (!resto.empty() && resto.front() == ' ') {
        resto.remove_prefix(1);
    }
    return {std::string(linea.substr(abre + 1, cierra - abre - 1)), std::string(resto)};
}

int main()
{
    std::vector<Entrada> log;
    std::string linea;
    while (std::getline(std::cin, linea)) {
        log.push_back(analizar(linea));
    }
    std::map<std::string, int> por_nivel;
    for (const auto& e : log) {
        por_nivel[e.nivel]++;
    }
    for (const auto& [nivel, n] : por_nivel) {
        std::cout << nivel << ": " << n << "\n";
    }
    std::cout << "Errores:\n";
    for (const auto& m : log
                             | std::views::filter([](const Entrada& e) { return e.nivel == "ERROR"; })
                             | std::views::transform([](const Entrada& e) { return e.mensaje; })) {
        std::cout << "  " << m << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Sin errores
```entrada
[INFO] todo bien
[WARN] cuidado
```
```salida
INFO: 1
WARN: 1
Errores:
```

##### Corchetes raros
```entrada
[] vacío
[ERROR]sin espacio
ERROR sin corchetes
```
```salida
: 1
?: 1
ERROR: 1
Errores:
  sin espacio
```

### Prueba del sello

#### ¿Qué ventaja tiene recibir `std::string_view` en vez de `const std::string&`?

Acepta también literales y pedazos de texto sin crear un `std::string` (sin copiar).

#### ¿Cuál es la regla de oro de las vistas?

Que no son dueñas: el dato que miran tiene que seguir vivo mientras se usan.

#### ¿Qué hace `std::ranges::sort(v, {}, &Enemigo::vida)`?

Ordena el vector comparando el campo `vida` de cada enemigo.

#### ¿Cuándo se ejecuta el trabajo de `v | std::views::filter(f)`?

Recién al recorrer el resultado: las views son perezosas.

#### ¿Qué da `std::views::iota(1, 5)`?

Los números 1, 2, 3 y 4, sin guardarlos en ningún contenedor.

### Soluciones (docente)

Material original: `11-STL/08-StringView-Span` y `11-Ranges`. `std::ranges::to` (C++23) no está en g++ 13, por eso los resultados se recorren con `for`.

## R04-N08 · Un contenedor propio

```meta
tipo: tema
padre: R04-N07
precio: 10
criatura: orco
temas: poo.genericos
usa: func.iteradores
```

### Crónica

En el taller de la Biblioteca, un artífice fabricó un estante raro: circular, donde el libro nuevo empuja al más viejo fuera del estante. Nadie sabía cómo catalogarlo… hasta que le puso un **dedo de bronce** que sabía recorrerlo.

—No hace falta que la Biblioteca conozca tu estante —dice {mentor}—. Si le das un dedo que sepa avanzar y mostrar, todas las herramientas de la Biblioteca funcionan con él. Gratis.

### Objetivos

Escribir un contenedor propio (una plantilla de clase) con un **iterador**
mínimo, para que funcionen con él el `for` de rango y todos los algoritmos de la
biblioteca; y reutilizar los iteradores de un contenedor interno cuando alcanza.

### Antes de empezar

- Plantillas e iteradores (nodos anteriores).
- Operadores para tus clases (rama 2).

### Explicación

#### La idea que atraviesa la biblioteca
Los **contenedores** guardan, los **iteradores** recorren y los **algoritmos**
operan sobre rangos de iteradores. Un algoritmo como `std::accumulate` no sabe si
le pasás un `vector` o tu propio contenedor: solo usa `*`, `++` y `!=`. Así que
**si tu contenedor da iteradores válidos, toda la biblioteca funciona con él**.

#### Qué necesita un contenedor
Dos métodos: `begin()` y `end()`, que devuelven iteradores. Con eso ya funcionan
el `for` de rango y los algoritmos.

#### Qué necesita un iterador (el mínimo, *forward*)
```cpp
class iterator {
public:
    // "etiquetas" que leen los algoritmos para saber qué pueden hacer
    using iterator_category = std::forward_iterator_tag;
    using value_type = T;
    using difference_type = std::ptrdiff_t;
    using pointer = const T*;
    using reference = const T&;

    iterator() = default;
    reference operator*() const { ... }           // el elemento actual
    iterator& operator++() { ...; return *this; } // ++it: avanzar
    iterator operator++(int) { auto c = *this; ++*this; return c; }   // it++
    bool operator==(const iterator& o) const { ... }   // != sale solo (C++20)
};
```
Lo que el iterador guarda por dentro depende del contenedor: en el `RingBuffer`,
un puntero al buffer y una posición lógica (0, 1, 2… desde el más viejo), que se
convierte en posición real con `(ini + pos) % N`.

#### Cuando alcanza con prestar iteradores
Si tu contenedor guarda los datos en un `std::vector` (como una `Matriz` que
guarda sus filas una detrás de otra), no hace falta escribir un iterador: devolvé
los del vector.
```cpp
auto begin() { return datos_.begin(); }
auto end() { return datos_.end(); }
auto begin() const { return datos_.begin(); }   // y las versiones const
auto end() const { return datos_.end(); }
```

#### Categorías, otra vez
Con `++`, tu iterador es *forward*: alcanza para `accumulate`, `find`, `count_if`,
`max_element`, `for_each` y el `for` de rango. Para `std::sort` haría falta *random
access* (`+`, `-`, `<`, `[]`). Agregar `--` lo hace *bidirectional* (y permite
recorrer al revés).

#### Contenedores que no guardan nada
Un "contenedor" puede **generar** sus elementos al recorrerlo: un `Rango(1, 10, 2)`
cuyo iterador solo guarda el número actual y el paso. No ocupa memoria por
elemento, y los algoritmos funcionan igual (así funciona `std::views::iota`).

> **Si venís de C.** En C, cada estructura necesitaba sus propias funciones de
> recorrido y su propio "sumar", "buscar", "máximo". Acá escribís el iterador una
> vez y reutilizás cien algoritmos.

### Código de ejemplo

```cpp
/*
 * Un contenedor propio que la STL entiende: RingBuffer (buffer circular).
 * Guarda los ultimos N valores: lo nuevo pisa lo mas viejo.
 */
#include <algorithm>
#include <array>
#include <cstddef>
#include <iostream>
#include <iterator>
#include <numeric>

template <typename T, std::size_t N>
class RingBuffer {
public:
    void push(const T& valor)
    {
        datos_[fin_] = valor;
        fin_ = (fin_ + 1) % N;
        if (tam_ < N) {
            tam_++;
        } else {
            ini_ = (ini_ + 1) % N;          // ya estaba lleno: se pisa el mas viejo
        }
    }

    std::size_t size() const { return tam_; }
    bool empty() const { return tam_ == 0; }

    // Un iterador minimo: *, ++, == y los "tipos" que piden los algoritmos.
    class iterator {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = const T*;
        using reference = const T&;

        iterator() = default;
        iterator(const RingBuffer* rb, std::size_t pos) : rb_(rb), pos_(pos) {}
        reference operator*() const { return rb_->datos_[(rb_->ini_ + pos_) % N]; }
        iterator& operator++()
        {
            ++pos_;
            return *this;
        }
        iterator operator++(int)
        {
            iterator copia = *this;
            ++pos_;
            return copia;
        }
        bool operator==(const iterator& o) const { return pos_ == o.pos_; }

    private:
        const RingBuffer* rb_ = nullptr;
        std::size_t pos_ = 0;
    };

    iterator begin() const { return iterator(this, 0); }
    iterator end() const { return iterator(this, tam_); }

private:
    std::array<T, N> datos_{};
    std::size_t ini_ = 0;
    std::size_t fin_ = 0;
    std::size_t tam_ = 0;
};

int main()
{
    RingBuffer<int, 5> ultimos;
    for (int i = 1; i <= 8; i++) {
        ultimos.push(i);
        std::cout << "push " << i << ":";
        for (int x : ultimos) {                // el for de rango usa begin() y end()
            std::cout << " " << x;
        }
        std::cout << "\n";
    }
    // Los algoritmos de la STL funcionan sin escribir nada mas
    std::cout << "suma " << std::accumulate(ultimos.begin(), ultimos.end(), 0)
              << ", máximo " << *std::max_element(ultimos.begin(), ultimos.end())
              << ", pares " << std::count_if(ultimos.begin(), ultimos.end(), [](int x) { return x % 2 == 0; }) << "\n";

    RingBuffer<double, 4> fps;
    for (double f : {58.0, 61.0, 60.0, 59.0, 62.0, 60.0}) {
        fps.push(f);
    }
    std::cout << "FPS promedio de las últimas 4 mediciones: "
              << std::accumulate(fps.begin(), fps.end(), 0.0) / fps.size() << "\n";
    return 0;
}
```

### Salida esperada

```
push 1: 1
push 2: 1 2
push 3: 1 2 3
push 4: 1 2 3 4
push 5: 1 2 3 4 5
push 6: 2 3 4 5 6
push 7: 3 4 5 6 7
push 8: 4 5 6 7 8
suma 30, máximo 8, pares 3
FPS promedio de las últimas 4 mediciones: 60.25
```

### ¿Para qué sirve?

Los contenedores propios aparecen cuando los de la biblioteca no alcanzan: buffers circulares para los últimos N eventos (historial de daño, promedios de FPS, logs rotativos), matrices para imágenes y mapas de juegos, grafos, árboles especiales, estructuras que leen un archivo enorme sin cargarlo entero. Dándoles iteradores, se integran con todo el resto del código sin adaptadores.

### Errores habituales

**Orco: `end()` mal calculado.** Si `end()` no coincide con el iterador al que llega
el recorrido (por ejemplo, un `Rango` de a 3 que salta por encima de `hasta`), el
`for` no termina nunca. `end()` tiene que ser **exactamente** el primer iterador
"después del último".

**Esqueleto: faltan los `using` del iterador.** Algunos algoritmos (o
`std::iterator_traits`) no compilan: el mensaje menciona `iterator_category` o
`value_type`.

**Goblin: falta la versión `const`.** Una función que recibe `const Matriz&` y hace
`for (int x : m)` no compila si solo hay `begin()` no `const`.

**Esqueleto: `std::sort` con un iterador *forward*.** Hace falta *random access*.
Si lo necesitás, devolvé iteradores de un `vector` interno o implementá los
operadores que faltan.

**Troll: un iterador que sobrevive a su contenedor.** Guarda un puntero al
contenedor: si el contenedor muere, el iterador apunta a nada.

### Misión R04-N08-M1 · El rango que no guarda nada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Rango(desde, hasta, paso = 1)` que representa los números `desde,
desde + paso, …` menores que `hasta`, **sin guardarlos**: su iterador solo guarda el
número actual y el paso. Calculá bien `end()` (el primer valor que "ya no entra",
alineado con el paso) para que el recorrido termine siempre. Cada línea de la
entrada es `desde hasta paso`: mostrá los números, su suma (`accumulate`) y cuántos
son múltiplos de 3 (`count_if`).

#### Criterio de aprobación

- El iterador tiene los `using` y los operadores mínimos.
- Funcionan el `for` de rango, `accumulate` y `count_if`.
- El recorrido termina aunque `hasta - desde` no sea múltiplo del paso, y con rangos vacíos.

#### Entrada de ejemplo

```
1 10 1
0 20 3
5 5 1
2 11 4
```

#### Salida esperada

```
[1, 10) de a 1: 1 2 3 4 5 6 7 8 9 | suma 45, múltiplos de 3: 3
[0, 20) de a 3: 0 3 6 9 12 15 18 | suma 63, múltiplos de 3: 7
[5, 5) de a 1: | suma 0, múltiplos de 3: 0
[2, 11) de a 4: 2 6 10 | suma 18, múltiplos de 3: 1
```

#### Solución de referencia

```cpp
// Mision 1 - El rango de numeros: un "contenedor" que no guarda nada (genera al recorrer).
#include <algorithm>
#include <cstddef>
#include <iostream>
#include <iterator>
#include <numeric>

class Rango {
public:
    Rango(int desde, int hasta, int paso = 1) : desde_(desde), hasta_(hasta), paso_(paso > 0 ? paso : 1) {}

    class iterator {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = int;
        using difference_type = std::ptrdiff_t;
        using pointer = const int*;
        using reference = int;

        iterator() = default;
        iterator(int actual, int paso) : actual_(actual), paso_(paso) {}
        int operator*() const { return actual_; }
        iterator& operator++()
        {
            actual_ += paso_;
            return *this;
        }
        iterator operator++(int)
        {
            iterator c = *this;
            actual_ += paso_;
            return c;
        }
        bool operator==(const iterator& o) const { return actual_ == o.actual_; }

    private:
        int actual_ = 0;
        int paso_ = 1;
    };

    iterator begin() const { return iterator(desde_, paso_); }
    iterator end() const
    {
        int pasos = (hasta_ > desde_) ? (hasta_ - desde_ + paso_ - 1) / paso_ : 0;
        return iterator(desde_ + pasos * paso_, paso_);   // el primero que ya no entra
    }

private:
    int desde_;
    int hasta_;
    int paso_;
};

int main()
{
    int desde = 0, hasta = 0, paso = 0;
    while (std::cin >> desde >> hasta >> paso) {
        Rango r(desde, hasta, paso);
        std::cout << "[" << desde << ", " << hasta << ") de a " << paso << ":";
        for (int x : r) {
            std::cout << " " << x;
        }
        std::cout << " | suma " << std::accumulate(r.begin(), r.end(), 0)
                  << ", múltiplos de 3: " << std::count_if(r.begin(), r.end(), [](int x) { return x % 3 == 0; }) << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Paso que no cae justo
```entrada
0 10 3
1 2 5
```
```salida
[0, 10) de a 3: 0 3 6 9 | suma 18, múltiplos de 3: 4
[1, 2) de a 5: 1 | suma 1, múltiplos de 3: 0
```

##### Rango al revés
```entrada
10 1 1
```
```salida
[10, 1) de a 1: | suma 0, múltiplos de 3: 0
```

### Misión R04-N08-M2 · El anillo que rechaza

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Agregale al `RingBuffer` un tercer parámetro de plantilla: un `enum class
AlLlenarse { Pisar, Rechazar }` (por defecto `Pisar`). Con `Rechazar`, `push`
devuelve `false` si está lleno; agregá `pop()` (saca el más viejo). Usá un anillo
de 3 que pisa como historial de los últimos en llegar, y otro de 3 que rechaza como
**sala** de espera. Órdenes: `entra nombre` (a los dos) y `sale` (de la sala). Al
final, mostrá los dos con una plantilla `mostrar` que use `std::for_each`.

#### Criterio de aprobación

- La política es un parámetro de la plantilla.
- Los dos anillos funcionan con `for_each`.

#### Entrada de ejemplo

```
entra Ana
entra Beto
entra Caro
entra Dani
sale
entra Eli
entra Fede
```

#### Salida esperada

```
La sala está llena: Dani espera
La sala está llena: Fede espera
Últimos 3 en llegar: Dani Eli Fede
En la sala: Beto Caro Eli
```

#### Solución de referencia

```cpp
// Mision 2 - El RingBuffer que rechaza: una politica al llenarse, como parametro de la plantilla.
#include <algorithm>
#include <array>
#include <cstddef>
#include <iostream>
#include <iterator>
#include <numeric>
#include <string>

enum class AlLlenarse { Pisar, Rechazar };

template <typename T, std::size_t N, AlLlenarse politica = AlLlenarse::Pisar>
class Anillo {
public:
    bool push(const T& v)
    {
        if (tam_ == N && politica == AlLlenarse::Rechazar) {
            return false;
        }
        datos_[fin_] = v;
        fin_ = (fin_ + 1) % N;
        if (tam_ < N) {
            tam_++;
        } else {
            ini_ = (ini_ + 1) % N;
        }
        return true;
    }

    bool pop()                              // saca el mas viejo
    {
        if (tam_ == 0) {
            return false;
        }
        ini_ = (ini_ + 1) % N;
        tam_--;
        return true;
    }

    std::size_t size() const { return tam_; }

    class iterator {
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = const T*;
        using reference = const T&;
        iterator() = default;
        iterator(const Anillo* a, std::size_t p) : a_(a), p_(p) {}
        reference operator*() const { return a_->datos_[(a_->ini_ + p_) % N]; }
        iterator& operator++()
        {
            ++p_;
            return *this;
        }
        iterator operator++(int)
        {
            iterator c = *this;
            ++p_;
            return c;
        }
        bool operator==(const iterator& o) const { return p_ == o.p_; }

    private:
        const Anillo* a_ = nullptr;
        std::size_t p_ = 0;
    };

    iterator begin() const { return iterator(this, 0); }
    iterator end() const { return iterator(this, tam_); }

private:
    std::array<T, N> datos_{};
    std::size_t ini_ = 0;
    std::size_t fin_ = 0;
    std::size_t tam_ = 0;
};

template <typename C>
void mostrar(const std::string& titulo, const C& c)
{
    std::cout << titulo << ":";
    std::for_each(c.begin(), c.end(), [](const auto& x) { std::cout << " " << x; });
    std::cout << "\n";
}

int main()
{
    Anillo<std::string, 3> historial;                         // pisa
    Anillo<std::string, 3, AlLlenarse::Rechazar> sala;         // rechaza
    std::string orden, quien;
    while (std::cin >> orden) {
        if (orden == "entra" && std::cin >> quien) {
            historial.push(quien);
            if (!sala.push(quien)) {
                std::cout << "La sala está llena: " << quien << " espera\n";
            }
        } else if (orden == "sale") {
            sala.pop();
        }
    }
    mostrar("Últimos 3 en llegar", historial);
    mostrar("En la sala", sala);
    return 0;
}
```

#### Pruebas

##### Sale de una sala vacía
```entrada
sale
entra Ana
sale
sale
```
```salida
Últimos 3 en llegar: Ana
En la sala:
```

##### Sin órdenes
```entrada
```
```salida
Últimos 3 en llegar:
En la sala:
```

##### Muchos llegan
```entrada
entra A
entra B
entra C
entra D
entra E
```
```salida
La sala está llena: D espera
La sala está llena: E espera
Últimos 3 en llegar: C D E
En la sala: A B C
```

### Misión R04-N08-M3 · La matriz de alturas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `template <typename T> class Matriz` que guarda sus datos en un
`std::vector<T>` (fila por fila), se accede con `m(fila, columna)` (con versión
`const`) y **presta** los iteradores del vector (`begin`/`end`, también `const`).
Leé filas, columnas y las alturas de un terreno **con el `for` de rango**. Mostrala,
su suma, la cima, y reemplazá los pozos (negativos) por 0 con `std::replace_if`.

#### Criterio de aprobación

- No escribe un iterador: reutiliza los del vector.
- El `operator()` tiene versión `const` y no `const`.
- Funciona con algoritmos que modifican (`replace_if`).

#### Entrada de ejemplo

```
3 4
2 5 -1 3
7 -3 4 1
0 6 2 -2
```

#### Salida esperada

```
2 5 -1 3
7 -3 4 1
0 6 2 -2
Suma: 24
Cima: 7
Sin pozos:
2 5 0 3
7 0 4 1
0 6 2 0
```

#### Solución de referencia

```cpp
// Mision 3 - La matriz: un contenedor 2D con operator() y begin/end que la recorren entera.
#include <algorithm>
#include <cstddef>
#include <iostream>
#include <numeric>
#include <vector>

template <typename T>
class Matriz {
public:
    Matriz(std::size_t filas, std::size_t columnas, const T& inicial = T{})
        : filas_(filas), columnas_(columnas), datos_(filas * columnas, inicial)
    {
    }

    T& operator()(std::size_t f, std::size_t c) { return datos_[f * columnas_ + c]; }
    const T& operator()(std::size_t f, std::size_t c) const { return datos_[f * columnas_ + c]; }
    std::size_t filas() const { return filas_; }
    std::size_t columnas() const { return columnas_; }

    // Se reutilizan los iteradores del vector: la matriz se recorre fila por fila.
    auto begin() { return datos_.begin(); }
    auto end() { return datos_.end(); }
    auto begin() const { return datos_.begin(); }
    auto end() const { return datos_.end(); }

private:
    std::size_t filas_;
    std::size_t columnas_;
    std::vector<T> datos_;
};

template <typename T>
void mostrar(const Matriz<T>& m)
{
    for (std::size_t f = 0; f < m.filas(); f++) {
        for (std::size_t c = 0; c < m.columnas(); c++) {
            std::cout << m(f, c) << (c + 1 < m.columnas() ? " " : "\n");
        }
    }
}

int main()
{
    std::size_t filas = 0, columnas = 0;
    std::cin >> filas >> columnas;
    Matriz<int> alturas(filas, columnas);
    for (int& x : alturas) {                          // cargar con el for de rango
        std::cin >> x;
    }
    mostrar(alturas);
    std::cout << "Suma: " << std::accumulate(alturas.begin(), alturas.end(), 0) << "\n";
    std::cout << "Cima: " << *std::max_element(alturas.begin(), alturas.end()) << "\n";
    std::replace_if(alturas.begin(), alturas.end(), [](int x) { return x < 0; }, 0);   // sin pozos
    std::cout << "Sin pozos:\n";
    mostrar(alturas);
    return 0;
}
```

#### Pruebas

##### Una sola fila
```entrada
1 3
-5 0 5
```
```salida
-5 0 5
Suma: 0
Cima: 5
Sin pozos:
0 0 5
```

##### Todo pozos
```entrada
2 2
-1 -2
-3 -4
```
```salida
-1 -2
-3 -4
Suma: -10
Cima: -1
Sin pozos:
0 0
0 0
```

### Encargo R04-N08-E1 · El promedio móvil de ventas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una tienda quiere el promedio de ventas de los **últimos 7 días**. Escribí una
plantilla `Ultimos<T, N>` que guarda los últimos N valores (pisando el más viejo) y
tiene `begin`/`end` (acá el orden no importa: se promedia). Cada número de la
entrada es la venta de un día: mostrá el promedio de los días guardados, y marcá un
"pico" si con la semana completa la venta supera 1.5 veces el promedio.

#### Criterio de aprobación

- El promedio se calcula con `std::accumulate` sobre el contenedor propio.
- Nunca guarda más de 7 valores.

#### Entrada de ejemplo

```
100 120 90 110 105 95 100 240 98 102
```

#### Salida esperada

```
Día 1: 100.0 | promedio de 1 días: 100.0
Día 2: 120.0 | promedio de 2 días: 110.0
Día 3: 90.0 | promedio de 3 días: 103.3
Día 4: 110.0 | promedio de 4 días: 105.0
Día 5: 105.0 | promedio de 5 días: 105.0
Día 6: 95.0 | promedio de 6 días: 103.3
Día 7: 100.0 | promedio de 7 días: 102.9
Día 8: 240.0 | promedio de 7 días: 122.9  <- ¡pico de ventas!
Día 9: 98.0 | promedio de 7 días: 119.7
Día 10: 102.0 | promedio de 7 días: 121.4
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Promedio movil de ventas: los ultimos 7 dias con un buffer circular.
#include <array>
#include <cstddef>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <numeric>

template <typename T, std::size_t N>
class Ultimos {
public:
    void push(const T& v)
    {
        datos_[fin_] = v;
        fin_ = (fin_ + 1) % N;
        if (tam_ < N) {
            tam_++;
        }
    }
    std::size_t size() const { return tam_; }
    bool lleno() const { return tam_ == N; }
    // Aca el orden no importa (se promedia): se recorren los tam_ datos guardados.
    auto begin() const { return datos_.begin(); }
    auto end() const { return datos_.begin() + tam_; }

private:
    std::array<T, N> datos_{};
    std::size_t fin_ = 0;
    std::size_t tam_ = 0;
};

int main()
{
    Ultimos<double, 7> semana;
    double venta = 0;
    int dia = 0;
    std::cout << std::fixed << std::setprecision(1);
    while (std::cin >> venta) {
        dia++;
        semana.push(venta);
        double promedio = std::accumulate(semana.begin(), semana.end(), 0.0) / semana.size();
        std::cout << "Día " << dia << ": " << venta << " | promedio de " << semana.size() << " días: " << promedio;
        if (semana.lleno() && venta > promedio * 1.5) {
            std::cout << "  <- ¡pico de ventas!";
        }
        std::cout << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Menos de una semana
```entrada
50 60
```
```salida
Día 1: 50.0 | promedio de 1 días: 50.0
Día 2: 60.0 | promedio de 2 días: 55.0
```

##### Ventas iguales sin picos
```entrada
100 100 100 100 100 100 100 100
```
```salida
Día 1: 100.0 | promedio de 1 días: 100.0
Día 2: 100.0 | promedio de 2 días: 100.0
Día 3: 100.0 | promedio de 3 días: 100.0
Día 4: 100.0 | promedio de 4 días: 100.0
Día 5: 100.0 | promedio de 5 días: 100.0
Día 6: 100.0 | promedio de 6 días: 100.0
Día 7: 100.0 | promedio de 7 días: 100.0
Día 8: 100.0 | promedio de 7 días: 100.0
```

##### Pico justo en el límite
```entrada
100 100 100 100 100 100 100 150 151
```
```salida
Día 1: 100.0 | promedio de 1 días: 100.0
Día 2: 100.0 | promedio de 2 días: 100.0
Día 3: 100.0 | promedio de 3 días: 100.0
Día 4: 100.0 | promedio de 4 días: 100.0
Día 5: 100.0 | promedio de 5 días: 100.0
Día 6: 100.0 | promedio de 6 días: 100.0
Día 7: 100.0 | promedio de 7 días: 100.0
Día 8: 150.0 | promedio de 7 días: 107.1
Día 9: 151.0 | promedio de 7 días: 114.4
```

### Prueba del sello

#### ¿Qué necesita un contenedor para funcionar en un `for` de rango?

Los métodos `begin()` y `end()` que devuelvan iteradores.

#### ¿Qué operaciones necesita como mínimo un iterador *forward*?

`*` (el elemento), `++` (avanzar) y `==` (comparar), más los `using` de sus tipos.

#### ¿Por qué `std::accumulate` funciona con tu `RingBuffer` sin cambiar nada?

Porque solo usa iteradores, y el `RingBuffer` los provee.

#### ¿Cuándo no hace falta escribir un iterador propio?

Cuando los datos están en un contenedor interno (como un `vector`) y alcanza con devolver sus iteradores.

#### ¿Por qué `std::sort` no funcionaría con el iterador del `RingBuffer`?

Porque es *forward* y `sort` necesita *random access*.

### Soluciones (docente)

Material original: `11-STL/12-Contenedor-Propio`, con los ejercicios del README (política al llenarse) resueltos.

## R04-N09 · Jefe: el Kraken de los Contenedores

```meta
tipo: jefe
padre: R04-N08
precio: 10
criatura: dragon
insignia: Sello del Kraken
insignia_descripcion: Venciste al Kraken de los Contenedores: dominás la biblioteca estándar de C++.
usa: col.pilas-colas, func.streams, err.opcionales
```

### Crónica

En los sótanos inundados de la Gran Biblioteca vive el **Kraken de los Contenedores**: un monstruo que se esconde entre las estanterías y saca un tentáculo por cada pasillo. Hace siglos que desordena todo lo que toca.

—No lo vas a encontrar recorriendo pasillo por pasillo —dice {mentor}—. Usá lo que aprendiste: el contenedor justo para cada cosa, algoritmos en vez de bucles, eventos que avisen solos. Ordená la Biblioteca y el Kraken no tendrá dónde esconderse.

### Objetivos

Integrar la rama en programas completos: contenedores bien elegidos,
algoritmos, lambdas, `optional`, `std::function`, ranges y entrada robusta.

### Antes de empezar

- Toda la rama: plantillas, iteradores, contenedores, adaptadores, algoritmos,
  functores, `std::function`, vistas y ranges.

### Explicación

#### Cómo se enfrenta este jefe
1. **Elegí los contenedores primero.** Por cada dato, preguntate: ¿lo busco por
   clave? (`map` o `unordered_map`), ¿lo recorro en orden? (`vector`), ¿saco
   siempre el más urgente? (`priority_queue`), ¿puede faltar? (`optional`).
2. **Escribí las operaciones como algoritmos**: cada vez que empieces un bucle,
   buscá si hay uno que lo haga (`any_of`, `count_if`, `erase_if`, `find`).
3. **Separá la entrada del resto**: una función que lee una opción de forma robusta,
   y el resto del programa no se preocupa por el teclado.

#### Un menú a prueba de todo
Si el usuario escribe una letra donde va un número, `std::cin` queda en estado de
error y hay que **limpiarlo** antes de seguir:
```cpp
int leer_opcion()
{
    int op = 0;
    while (!(std::cin >> op)) {
        if (std::cin.eof()) return 0;               // se terminó la entrada
        std::cin.clear();                           // quitar el estado de error
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');   // tirar la línea
        std::cout << "Opción inválida: ";
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');   // el Enter
    return op;
}
```
`std::numeric_limits` viene de `<limits>`: el `max()` dice "todo lo que haya".

#### Un "sistema de entidades"
Los motores de juegos modernos no hacen una clase por tipo de cosa: cada
**entidad** es un conjunto de datos opcionales (tiene vida, o no; ataca, o no;
persigue, o no), y los **sistemas** recorren las entidades que tienen lo que les
interesa. Con `optional` para los datos, algoritmos y views para los sistemas, y
`std::function` para los eventos, queda todo desacoplado.

### ¿Para qué sirve?

El menú robusto es la base de cualquier herramienta de consola; la lista de tareas es, en chico, un gestor de pedidos o de tickets. El sistema de entidades es exactamente cómo se organizan los motores de juegos modernos (Unity DOTS, Bevy, EnTT), y el despacho por prioridad es cómo trabaja la logística de un correo o de una aplicación de delivery.

### Errores habituales

**Goblin: el menú que enloquece con una letra.** Sin `clear()` e `ignore()`, `cin`
queda en error y el menú se repite para siempre.

**Ogro: el bucle a mano donde había un algoritmo.** No es un error, pero es donde
se esconden los "uno de más". Si existe `count_if`, usalo.

**Orco: modificar el vector mientras lo recorrés.** En el sistema de entidades,
borrar entidades dentro del recorrido rompe los iteradores. Marcá y después
`erase_if`.

**Troll: guardar un puntero a un elemento de un vector que después cambia.** Un
`Entidad*` que devolvió `buscar` deja de valer después de un `erase_if` o un
`push_back`. Volvé a buscar.

**Ogro: `*optional` sin preguntar.** En el sistema de entidades, una poción no tiene
vida: `*e.vida` sin preguntar es comportamiento indefinido.

### Misión R04-N09-M1 · La lista de tareas del Gremio

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Programá una lista de tareas con un menú: **1** agregar (no vacías ni repetidas),
**2** ver (numeradas, con `[x]` las hechas), **3** marcar como hecha (por número),
**4** limpiar las hechas (y decir cuántas), **5** ordenar (las urgentes, que
empiezan con `!`, primero; después alfabético; con un orden estable) y mostrar,
**6** resumen (total, hechas y urgentes pendientes), **0** salir. El menú no se
rompe si se escribe una letra, y termina bien si se acaba la entrada. Usá
algoritmos (`any_of`, `for_each`, `erase_if`, `stable_sort`, `count_if`), no bucles
a mano.

#### Criterio de aprobación

- `leer_opcion` limpia el error con `clear` e `ignore`.
- Usa algoritmos con lambdas en cada operación.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
1
comprar aceite
1
!revisar caldera
1
comprar aceite
x
1
barrer
1

2
3
1
3
9
6
5
4
2
0
```

#### Salida esperada

```
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
Tarea: 
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
Tarea: 
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
Tarea: 
Esa tarea ya existe.
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: Opción inválida, escribí un número: 
Tarea: 
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
Tarea: 
La tarea no puede estar vacía.
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
1. [ ] comprar aceite
2. [ ] !revisar caldera
3. [ ] barrer
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
Número: 
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
Número: 
No existe la tarea 9.
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
3 tareas, 1 hechas, 1 urgentes pendientes
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
1. [ ] !revisar caldera
2. [ ] barrer
3. [x] comprar aceite
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
Borradas: 1
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
1. [ ] !revisar caldera
2. [ ] barrer
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: 
¡Hasta luego!
```

#### Solución de referencia

```cpp
// Jefe R04 - La lista de tareas del Gremio: menu robusto y algoritmos de la STL.
#include <algorithm>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

struct Tarea {
    std::string texto;
    bool hecha = false;
    bool urgente() const { return !texto.empty() && texto[0] == '!'; }
};

int leer_opcion()
{
    int op = 0;
    while (!(std::cin >> op)) {
        if (std::cin.eof()) {
            return 0;
        }
        std::cin.clear();                                                     // limpiar el error
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');   // tirar la linea
        std::cout << "Opción inválida, escribí un número: ";
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    return op;
}

void mostrar(const std::vector<Tarea>& tareas)
{
    if (tareas.empty()) {
        std::cout << "(no hay tareas)\n";
        return;
    }
    int n = 1;
    std::for_each(tareas.begin(), tareas.end(), [&n](const Tarea& t) {
        std::cout << n++ << ". [" << (t.hecha ? "x" : " ") << "] " << t.texto << "\n";
    });
}

int main()
{
    std::vector<Tarea> tareas;
    int op = -1;
    while (op != 0) {
        std::cout << "1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir: ";
        op = leer_opcion();
        std::cout << "\n";
        if (op == 1) {
            std::string texto;
            std::cout << "Tarea: ";
            std::getline(std::cin, texto);
            std::cout << "\n";
            auto igual = [&texto](const Tarea& t) { return t.texto == texto; };
            if (texto.empty()) {
                std::cout << "La tarea no puede estar vacía.\n";
            } else if (std::any_of(tareas.begin(), tareas.end(), igual)) {
                std::cout << "Esa tarea ya existe.\n";
            } else {
                tareas.push_back({texto});
            }
        } else if (op == 2) {
            mostrar(tareas);
        } else if (op == 3) {
            std::cout << "Número: ";
            int n = leer_opcion();
            std::cout << "\n";
            if (n >= 1 && n <= static_cast<int>(tareas.size())) {
                tareas[n - 1].hecha = true;
            } else {
                std::cout << "No existe la tarea " << n << ".\n";
            }
        } else if (op == 4) {
            auto borradas = std::erase_if(tareas, [](const Tarea& t) { return t.hecha; });
            std::cout << "Borradas: " << borradas << "\n";
        } else if (op == 5) {
            std::stable_sort(tareas.begin(), tareas.end(), [](const Tarea& a, const Tarea& b) {
                if (a.urgente() != b.urgente()) {
                    return a.urgente();                  // las urgentes primero
                }
                return a.texto < b.texto;
            });
            mostrar(tareas);
        } else if (op == 6) {
            auto urgentes = std::count_if(tareas.begin(), tareas.end(), [](const Tarea& t) { return t.urgente() && !t.hecha; });
            auto hechas = std::count_if(tareas.begin(), tareas.end(), [](const Tarea& t) { return t.hecha; });
            std::cout << tareas.size() << " tareas, " << hechas << " hechas, " << urgentes << " urgentes pendientes\n";
        } else if (op != 0) {
            std::cout << "No existe la opción " << op << ".\n";
        }
    }
    std::cout << "¡Hasta luego!\n";
    return 0;
}
```

#### Pruebas

##### Sale enseguida
```entrada
0
```
```salida
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
¡Hasta luego!
```

##### Se termina la entrada
```entrada
1
lavar
2
```
```salida
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
Tarea:
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
1. [ ] lavar
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
¡Hasta luego!
```

##### Marcar fuera de rango y limpiar sin hechas
```entrada
1
!urgente
3
5
4
6
0
```
```salida
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
Tarea:
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
Número:
No existe la tarea 5.
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
Borradas: 0
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
1 tareas, 0 hechas, 1 urgentes pendientes
1 agregar, 2 ver, 3 hecha, 4 limpiar hechas, 5 ordenar, 6 resumen, 0 salir:
¡Hasta luego!
```

### Misión R04-N09-M2 · Los tentáculos del Kraken

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Armá un pequeño **sistema de entidades** en una grilla de 10 × 5. Cada `Entidad`
tiene id, nombre, símbolo, posición, `optional<int>` vida, `optional<int>` ataque y si
persigue. Un `Mundo` guarda un vector de entidades y ofrece:
- `crear` (asigna el id), `buscar(id)` (con `std::ranges::find` y proyección);
- `mover_perseguidores(objetivo)`: los que persiguen dan un paso hacia el
  objetivo (primero en x, después en y), recorriendo con `views::filter`;
- `combatir(id)`: arma un **índice espacial** (`unordered_map` de casilla → ids) y
  hace que la heroína intercambie golpes con cada enemigo de su casilla;
- `recoger(pos)`: quita (con `erase_if`) y devuelve lo que no tiene vida y está en
  esa casilla;
- `limpiar_muertos()`: avisa a los suscriptos (`std::function`) de cada muerte y
  los borra;
- `dibujar`: cada entidad con su símbolo (`@` Kira, `t` tentáculo, `K` el Kraken,
  `+` la poción); si dos comparten casilla, se ve la última creada.

Kira (40 de vida, 12 de ataque) empieza en (0, 2); hay dos tentáculos que persiguen,
el Kraken quieto en (8, 2) y una poción (+20 de vida) en (3, 2). La entrada es una
palabra con los pasos de Kira (`d` derecha, `i` izquierda, `a` arriba, `b` abajo).
En cada turno: mover a Kira, recoger, mover perseguidores, combatir y limpiar.

#### Criterio de aprobación

- Usa `optional` para los datos que pueden faltar y pregunta antes de usarlos.
- Usa un índice espacial con `unordered_map`.
- Las muertes se avisan por un evento (`std::function`).
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
dddddddbd
```

#### Salida esperada

```
..........
.....t....
@..+....K.
......t...
..........
Turno 1: Kira va a (1, 2)
Turno 2: Kira va a (2, 2)
Turno 3: Kira va a (3, 2)
  Kira junta poción (vida 60)
  Kira y tentáculo chocan: tentáculo queda en 3, Kira en 54
Turno 4: Kira va a (4, 2)
  Kira y tentáculo chocan: tentáculo queda en -9, Kira en 48
  [evento] cae tentáculo
Turno 5: Kira va a (5, 2)
Turno 6: Kira va a (6, 2)
Turno 7: Kira va a (7, 2)
Turno 8: Kira va a (7, 3)
  Kira y tentáculo chocan: tentáculo queda en 3, Kira en 42
Turno 9: Kira va a (8, 3)
  Kira y tentáculo chocan: tentáculo queda en -9, Kira en 36
  [evento] cae tentáculo
..........
..........
........K.
........@.
..........
Kira sigue en pie; enemigos caídos: 2, entidades: 2
```

#### Solución de referencia

```cpp
// Jefe R04 - El sistema de entidades: el Kraken y sus tentaculos en una grilla.
#include <algorithm>
#include <functional>
#include <iostream>
#include <map>
#include <optional>
#include <ranges>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

struct Posicion {
    int x = 0;
    int y = 0;
    bool operator==(const Posicion&) const = default;
};

struct Entidad {
    int id = 0;
    std::string nombre;
    char simbolo = '?';
    Posicion pos;
    std::optional<int> vida;          // no todas tienen vida (una pocion no)
    std::optional<int> ataque;        // no todas atacan
    bool persigue = false;            // IA: avanza hacia la heroina
};

class Mundo {
public:
    using Oyente = std::function<void(const Entidad&)>;

    int crear(Entidad e)
    {
        e.id = siguiente_++;
        entidades_.push_back(e);
        return e.id;
    }

    void al_morir(Oyente f) { muertes_.push_back(std::move(f)); }

    Entidad* buscar(int id)
    {
        auto it = std::ranges::find(entidades_, id, &Entidad::id);
        return it == entidades_.end() ? nullptr : &*it;
    }

    // IA: los que persiguen dan un paso hacia el objetivo (primero en x, despues en y).
    void mover_perseguidores(const Posicion& objetivo)
    {
        for (auto& e : entidades_ | std::views::filter([](const Entidad& x) { return x.persigue; })) {
            if (e.pos.x != objetivo.x) {
                e.pos.x += (objetivo.x > e.pos.x) ? 1 : -1;
            } else if (e.pos.y != objetivo.y) {
                e.pos.y += (objetivo.y > e.pos.y) ? 1 : -1;
            }
        }
    }

    // Combate: todos los que comparten casilla con la heroina y tienen ataque intercambian golpes.
    void combatir(int id_heroina)
    {
        Entidad* h = buscar(id_heroina);
        std::unordered_map<int, std::vector<int>> por_casilla;          // indice espacial: casilla -> ids
        for (const auto& e : entidades_) {
            por_casilla[e.pos.y * 100 + e.pos.x].push_back(e.id);
        }
        for (int id : por_casilla[h->pos.y * 100 + h->pos.x]) {
            Entidad* e = buscar(id);
            if (id == id_heroina || !e->vida || !e->ataque || *e->vida <= 0) {
                continue;
            }
            *e->vida -= *h->ataque;
            *h->vida -= *e->ataque;
            std::cout << "  " << h->nombre << " y " << e->nombre << " chocan: " << e->nombre << " queda en " << *e->vida
                      << ", " << h->nombre << " en " << *h->vida << "\n";
        }
    }

    // Juntar: lo que no tiene vida y esta en la misma casilla, se recoge.
    std::vector<std::string> recoger(const Posicion& p)
    {
        std::vector<std::string> juntado;
        std::erase_if(entidades_, [&](const Entidad& e) {
            bool es_objeto = !e.vida && e.pos == p;
            if (es_objeto) {
                juntado.push_back(e.nombre);
            }
            return es_objeto;
        });
        return juntado;
    }

    void limpiar_muertos()
    {
        for (const auto& e : entidades_) {
            if (e.vida && *e.vida <= 0) {
                for (auto& f : muertes_) {
                    f(e);
                }
            }
        }
        std::erase_if(entidades_, [](const Entidad& e) { return e.vida && *e.vida <= 0; });
    }

    void dibujar(int ancho, int alto) const
    {
        std::map<std::pair<int, int>, char> marcas;
        for (const auto& e : entidades_) {
            marcas[{e.pos.y, e.pos.x}] = e.simbolo;
        }
        for (int y = 0; y < alto; y++) {
            for (int x = 0; x < ancho; x++) {
                auto it = marcas.find({y, x});
                std::cout << (it == marcas.end() ? '.' : it->second);
            }
            std::cout << "\n";
        }
    }

    std::size_t cantidad() const { return entidades_.size(); }

private:
    int siguiente_ = 1;
    std::vector<Entidad> entidades_;
    std::vector<Oyente> muertes_;
};

int main()
{
    Mundo mundo;
    int kira = mundo.crear({0, "Kira", '@', {0, 2}, 40, 12, false});
    mundo.crear({0, "tentáculo", 't', {5, 1}, 15, 6, true});
    mundo.crear({0, "tentáculo", 't', {6, 3}, 15, 6, true});
    mundo.crear({0, "Kraken", 'K', {8, 2}, 60, 9, false});
    mundo.crear({0, "poción", '+', {3, 2}, std::nullopt, std::nullopt, false});

    int caidos = 0;
    mundo.al_morir([&caidos](const Entidad& e) {
        caidos++;
        std::cout << "  [evento] cae " << e.nombre << "\n";
    });

    std::string pasos;
    std::cin >> pasos;                            // d = derecha, i = izquierda, a = arriba, b = abajo
    mundo.dibujar(10, 5);
    int turno = 1;
    for (char p : pasos) {
        Entidad* h = mundo.buscar(kira);
        if (h == nullptr) {
            break;
        }
        h->pos.x += (p == 'd') - (p == 'i');
        h->pos.y += (p == 'b') - (p == 'a');
        std::cout << "Turno " << turno++ << ": Kira va a (" << h->pos.x << ", " << h->pos.y << ")\n";
        for (const auto& cosa : mundo.recoger(h->pos)) {
            h->vida = *h->vida + 20;
            std::cout << "  Kira junta " << cosa << " (vida " << *h->vida << ")\n";
        }
        mundo.mover_perseguidores(h->pos);
        mundo.combatir(kira);
        mundo.limpiar_muertos();
    }
    mundo.dibujar(10, 5);
    Entidad* h = mundo.buscar(kira);
    std::cout << (h ? "Kira sigue en pie" : "Kira cayó") << "; enemigos caídos: " << caidos
              << ", entidades: " << mundo.cantidad() << "\n";
    return 0;
}
```

#### Pruebas

##### Kira no se mueve
```entrada
x
```
```salida
..........
.....t....
@..+....K.
......t...
..........
Turno 1: Kira va a (0, 2)
..........
....t.....
@..+....K.
.....t....
..........
Kira sigue en pie; enemigos caídos: 0, entidades: 5
```

##### Kira va hacia arriba
```entrada
aaaa
```
```salida
..........
.....t....
@..+....K.
......t...
..........
Turno 1: Kira va a (0, 1)
Turno 2: Kira va a (0, 0)
Turno 3: Kira va a (0, -1)
Turno 4: Kira va a (0, -2)
..........
.t........
...+....K.
..t.......
..........
Kira sigue en pie; enemigos caídos: 0, entidades: 5
```

##### Camino largo
```entrada
ddddddddddddd
```
```salida
..........
.....t....
@..+....K.
......t...
..........
Turno 1: Kira va a (1, 2)
Turno 2: Kira va a (2, 2)
Turno 3: Kira va a (3, 2)
  Kira junta poción (vida 60)
  Kira y tentáculo chocan: tentáculo queda en 3, Kira en 54
Turno 4: Kira va a (4, 2)
  Kira y tentáculo chocan: tentáculo queda en -9, Kira en 48
  [evento] cae tentáculo
Turno 5: Kira va a (5, 2)
Turno 6: Kira va a (6, 2)
Turno 7: Kira va a (7, 2)
Turno 8: Kira va a (8, 2)
  Kira y Kraken chocan: Kraken queda en 48, Kira en 39
Turno 9: Kira va a (9, 2)
Turno 10: Kira va a (10, 2)
Turno 11: Kira va a (11, 2)
Turno 12: Kira va a (12, 2)
Turno 13: Kira va a (13, 2)
..........
..........
........K.
..........
..........
Kira sigue en pie; enemigos caídos: 1, entidades: 3
```

### Encargo R04-N09-E1 · El despacho de pedidos

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

Un depósito despacha pedidos por orden de **vencimiento** (el que vence antes sale
primero; si empatan, el de menor número). Órdenes: `pedido numero zona vence
bultos` y `camion capacidad`: cada camión sale 30 minutos después del anterior y
carga pedidos en orden mientras entren (se detiene en el primero que no entra). Un
pedido cargado después de su vencimiento queda **atrasado**. Al final, mostrá los
bultos por zona, los atrasados (con `views::transform` sobre un vector) y cuántos
quedan.

#### Criterio de aprobación

- Usa `priority_queue` con un comparador que desempata.
- Acumula por zona en un `map`.
- Lista los atrasados con una view.

#### Entrada de ejemplo

```
pedido 1 norte 50 4
pedido 2 sur 20 3
pedido 3 norte 90 6
pedido 4 centro 40 2
camion 6
pedido 5 sur 70 5
camion 10
camion 4
```

#### Salida esperada

```
Camión (min 30): #2 #4
Camión (min 60): #1 #5
Camión (min 90):
Bultos por zona: centro=2 norte=4 sur=8
Atrasados: #2 #1
Quedan: 1
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El despacho de pedidos: prioridad por vencimiento y reporte por zona.
#include <iostream>
#include <map>
#include <queue>
#include <ranges>
#include <string>
#include <vector>

struct Pedido {
    int numero = 0;
    std::string zona;
    int vence = 0;          // hora limite, en minutos desde la apertura
    int bultos = 0;
};

struct VenceDespues {
    bool operator()(const Pedido& a, const Pedido& b) const
    {
        return a.vence != b.vence ? a.vence > b.vence : a.numero > b.numero;
    }
};

int main()
{
    std::priority_queue<Pedido, std::vector<Pedido>, VenceDespues> pendientes;
    std::map<std::string, int> bultos_por_zona;
    std::vector<Pedido> atrasados;
    int reloj = 0;
    std::string orden;
    while (std::cin >> orden) {
        if (orden == "pedido") {
            Pedido p;
            std::cin >> p.numero >> p.zona >> p.vence >> p.bultos;
            pendientes.push(p);
        } else if (orden == "camion") {
            int capacidad = 0;
            std::cin >> capacidad;
            reloj += 30;
            std::cout << "Camión (min " << reloj << "):";
            while (!pendientes.empty() && pendientes.top().bultos <= capacidad) {
                Pedido p = pendientes.top();
                pendientes.pop();
                capacidad -= p.bultos;
                bultos_por_zona[p.zona] += p.bultos;
                if (p.vence < reloj) {
                    atrasados.push_back(p);
                }
                std::cout << " #" << p.numero;
            }
            std::cout << "\n";
        }
    }
    std::cout << "Bultos por zona:";
    for (const auto& [zona, b] : bultos_por_zona) {
        std::cout << " " << zona << "=" << b;
    }
    std::cout << "\nAtrasados:";
    for (int n : atrasados | std::views::transform(&Pedido::numero)) {
        std::cout << " #" << n;
    }
    std::cout << (atrasados.empty() ? " ninguno" : "") << "\nQuedan: " << pendientes.size() << "\n";
    return 0;
}
```

#### Pruebas

##### Camión sin pedidos
```entrada
camion 10
```
```salida
Camión (min 30):
Bultos por zona:
Atrasados: ninguno
Quedan: 0
```

##### Pedido que no entra en ningún camión
```entrada
pedido 1 norte 100 50
camion 10
camion 20
```
```salida
Camión (min 30):
Camión (min 60):
Bultos por zona:
Atrasados: ninguno
Quedan: 1
```

##### Empate de vencimiento
```entrada
pedido 7 sur 60 1
pedido 3 norte 60 1
camion 5
```
```salida
Camión (min 30): #3 #7
Bultos por zona: norte=1 sur=1
Atrasados: ninguno
Quedan: 0
```

### Prueba del sello

#### ¿Por qué hay que llamar a `std::cin.clear()` después de una lectura fallida?

Porque `cin` queda en estado de error y todas las lecturas siguientes fallan hasta limpiarlo.

#### ¿Qué contenedor usarías para sacar siempre el pedido que vence antes?

Una `priority_queue` con un comparador por vencimiento.

#### ¿Por qué la poción tiene `std::nullopt` como vida?

Porque no es un ser vivo: con `optional`, "no tiene vida" es distinto de "tiene 0 de vida".

#### ¿Qué gana el sistema de entidades con el índice espacial?

Encontrar quién está en una casilla sin recorrer todas las entidades.

#### ¿Por qué conviene avisar las muertes con eventos?

Porque quien cuenta, anima o suma puntos no necesita estar dentro del `Mundo`: se suscribe.

### Soluciones (docente)

Jefe de la rama 4. M1 es `11-STL/14-ToDo-List` ampliada (hechas, urgentes, orden estable). M2 reescribe en chico `11-STL/15-Proyecto` (sistema de entidades). El texto del menú se muestra entero en la salida esperada porque la entrada viene de un archivo.
