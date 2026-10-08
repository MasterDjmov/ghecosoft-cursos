# RAMA R05 · El Taller del Juego: calidad y un juego completo

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · Excepciones

```meta
tipo: tema
padre: R04-N09
precio: 10
criatura: ogro
temas: err.excepciones
```

### Crónica

Pasando la Biblioteca está el **Taller del Juego**, la parte más ruidosa de la Ciudadela: acá se construyen máquinas grandes, de esas que no pueden fallar en silencio. Bron se sube a un andamio para ver mejor, el andamio se rompe, y Bron cae.

Lo ataja una **red**, tendida justo abajo. El que la tendió sabía que el andamio podía romperse, aunque no sabía cuándo. Tesla le da a Bron un amuleto con forma de red: **el Amuleto del Catch**. —Para la próxima —dice—. Siempre hay una próxima.

—Cuando algo sale mal en lo profundo de una máquina —dice {mentor}—, el que lo descubre muchas veces no sabe qué hacer. Pero puede **tocar la alarma**, y alguien más arriba, que sí sabe, la atrapa. Eso es una excepción.

### Objetivos

Avisar errores con `throw` y manejarlos con `try`/`catch`; usar las excepciones
de la biblioteca (`std::invalid_argument`, `std::out_of_range`, `std::runtime_error`)
y escribir las propias; entender qué pasa con los objetos cuando una excepción
atraviesa funciones (RAII); y elegir entre excepción, `optional` y `bool`.

### Antes de empezar

- Herencia (rama 2).
- `optional`, RAII y destructores (rama 3).

### Explicación

#### Lanzar y atrapar
```cpp
void subir_presion(int& presion, int cuanto)
{
    if (cuanto < 0) {
        throw std::invalid_argument("no se sube una cantidad negativa");
    }
    ...
}

try {
    subir_presion(p, -5);
    std::cout << "esto no se ejecuta si hubo error";
} catch (const std::invalid_argument& e) {
    std::cout << "error: " << e.what();
}
```
- `throw` **lanza** una excepción: la función se corta **en ese punto** y la
  excepción "sube" por las funciones que la llamaron, hasta encontrar un `catch`
  que la atrape.
- `try { ... }` marca el código que puede fallar; cada `catch` atrapa un tipo.
- `e.what()` da el mensaje.
- Si **nadie** la atrapa, el programa se corta con `terminate`.

Se atrapa **por referencia constante** (`const tipo&`): así no se copia y no se
rebana.

#### Las excepciones de la biblioteca (`<stdexcept>`)
Todas heredan de `std::exception`:
| Excepción | Significa | La lanzan |
|---|---|---|
| `std::invalid_argument` | un argumento sin sentido | `std::stoi("hola")` |
| `std::out_of_range` | fuera del rango válido | `v.at(10)`, `m.at(clave)`, `std::stoi("99999999999")` |
| `std::runtime_error` | algo falló al ejecutar | para tus errores generales |
| `std::logic_error` | un error de programación | |
| `std::bad_alloc` | no hay memoria | `new` |

Como es una jerarquía, los `catch` van **del más específico al más general**: un
`catch (const std::exception&)` al final atrapa todo lo demás.

#### Tus propias excepciones
Heredá de `std::runtime_error` y agregá los datos del error:
```cpp
class SinStock : public std::runtime_error {
public:
    SinStock(const std::string& producto, int pedido)
        : std::runtime_error("no alcanza el stock de " + producto), pedido_(pedido) {}
    int pedido() const { return pedido_; }
private:
    int pedido_;
};
```
Así, quien atrapa puede preguntar `e.pedido()` para decidir qué hacer.

#### Excepciones y RAII
Cuando una excepción sale de una función, los objetos locales se **destruyen** en
el camino (se llama *stack unwinding*). Por eso RAII es tan importante: los
archivos se cierran y la memoria se libera aunque haya un error. Con `new`/`delete`
a mano, el `delete` no llegaría a ejecutarse.

#### ¿Excepción, `optional` o `bool`?
| Situación | Herramienta |
|---|---|
| "no hay resultado" es normal (buscar y no encontrar) | `std::optional` |
| la acción puede no hacerse y el que llama lo espera (extraer sin saldo) | `bool` |
| algo **falló** y el que lo detecta no puede resolverlo (archivo roto, dato imposible en un constructor) | excepción |

Un constructor no puede devolver `false`: si no puede construir un objeto válido,
**lanza**. Las excepciones son para lo **excepcional**: no se usan para el flujo
normal del programa (por ejemplo, para salir de un bucle).

#### `noexcept`
Marca una función que promete no lanzar. Si lanza igual, el programa termina. Se
usa en los movimientos (rama 3) y en funciones simples que no pueden fallar.

> **Si venís de C.** En C, cada función devolvía un código de error que había que
> revisar en cada llamada (y era fácil olvidarlo). Una excepción no se puede
> ignorar: o alguien la atrapa, o el programa se detiene.

### Código de ejemplo

```cpp
/*
 * Excepciones: avisar un error y manejarlo lejos de donde paso.
 */
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

// Una excepcion propia: hereda de std::runtime_error.
class CalderaRota : public std::runtime_error {
public:
    CalderaRota(const std::string& que, int presion)
        : std::runtime_error(que), presion_(presion) {}
    int presion() const { return presion_; }

private:
    int presion_;
};

void subir_presion(int& presion, int cuanto)
{
    if (cuanto < 0) {
        throw std::invalid_argument("no se sube una cantidad negativa");
    }
    presion += cuanto;
    if (presion > 100) {
        throw CalderaRota("la caldera explotó", presion);    // lanzar: la funcion se corta aca
    }
}

class Seccion {                                                // RAII: se ve que se limpia igual
public:
    explicit Seccion(const std::string& n) : n_(n) { std::cout << "  [abro " << n_ << "]\n"; }
    ~Seccion() { std::cout << "  [cierro " << n_ << "]\n"; }

private:
    std::string n_;
};

void turno(int& presion, int cuanto)
{
    Seccion s("sala de calderas");
    subir_presion(presion, cuanto);
    std::cout << "  presión: " << presion << "\n";
}

int main()
{
    int presion = 60;
    for (int cuanto : {20, -5, 30, 10}) {
        std::cout << "Subir " << cuanto << ":\n";
        try {                                                  // intentar...
            turno(presion, cuanto);
        } catch (const CalderaRota& e) {                       // ...y atrapar, del mas especifico
            std::cout << "  ¡" << e.what() << "! (presión " << e.presion() << ")\n";
            presion = 50;
        } catch (const std::exception& e) {                    // al mas general
            std::cout << "  error: " << e.what() << "\n";
        }
    }

    // La biblioteca tambien lanza: stoi, at, ...
    for (const std::string texto : {"42", "cuarenta", "99999999999"}) {
        try {
            int n = std::stoi(texto);                          // si lanza, no se muestra nada de esta linea
            std::cout << texto << " -> " << n << "\n";
        } catch (const std::invalid_argument&) {
            std::cout << texto << " -> no es un número\n";
        } catch (const std::out_of_range&) {
            std::cout << texto << " -> no entra en un int\n";
        }
    }
    std::vector<int> v = {1, 2, 3};
    try {
        std::cout << v.at(10) << "\n";
    } catch (const std::out_of_range& e) {
        std::cout << "at(10): fuera de rango\n";
    }
    return 0;
}
```

### Salida esperada

```
Subir 20:
  [abro sala de calderas]
  presión: 80
  [cierro sala de calderas]
Subir -5:
  [abro sala de calderas]
  [cierro sala de calderas]
  error: no se sube una cantidad negativa
Subir 30:
  [abro sala de calderas]
  [cierro sala de calderas]
  ¡la caldera explotó! (presión 110)
Subir 10:
  [abro sala de calderas]
  presión: 60
  [cierro sala de calderas]
42 -> 42
cuarenta -> no es un número
99999999999 -> no entra en un int
at(10): fuera de rango
```

### ¿Para qué sirve?

Toda la biblioteca estándar y casi todas las bibliotecas de C++ avisan sus errores con excepciones: no se pudo abrir un archivo, no hay conexión, un dato vino mal de la red, un JSON está roto. Un importador de datos, un servidor o una aplicación de escritorio las usa para que un error en un registro, un pedido o una ventana no tire abajo todo el programa: se atrapa, se informa y se sigue.

### Errores habituales

**Ogro: la excepción que nadie atrapa.**
```
terminate called after throwing an instance of 'std::runtime_error'
  what():  no se pudo abrir la caldera
```

**Ogro: el `catch` general primero.** Si `catch (const std::exception&)` va antes
que `catch (const SinStock&)`, el general atrapa todo y el específico nunca se
ejecuta (`g++` avisa: "exception of type ‘SinStock’ will be caught by earlier
handler").

**Troll: atrapar por valor.** `catch (std::exception e)` copia y **rebana**: se
pierde el tipo real y sus datos. Siempre `catch (const T& e)`.

**Ogro: tragarse el error.** `catch (...) {}` vacío esconde los problemas: el
programa sigue como si nada. Si atrapás, hacé algo (informar, reintentar, deshacer).

**Ogro: lanzar desde un `noexcept` o un destructor.**
```
main.cpp:1:21: warning: ‘throw’ will always call ‘terminate’ [-Wterminate]
```

**Goblin: `std::stoi` y los sobrantes.** `std::stoi("12abc")` **no** lanza: da 12.
Para exigir que todo sea número, usá su segundo parámetro (cuántos caracteres
usó).

### Misión R05-N01-M1 · Leer números de verdad

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `int a_entero(const std::string&)` con `std::stoi` y su segundo parámetro
(la cantidad de caracteres usados): si sobran caracteres, lanzá
`std::invalid_argument` con el sobrante. Leé palabras hasta el final y sumá los
números; para cada error, mostrá si "no es un número", "no entra en un int" o qué
sobra.

#### Criterio de aprobación

- Atrapa `out_of_range` e `invalid_argument` por separado.
- Detecta los sobrantes y lanza con un mensaje claro.
- Un error no corta la suma.

#### Entrada de ejemplo

```
10 -3 12abc hola 99999999999 7
```

#### Salida esperada

```
12abc: sobran caracteres: "abc"
hola: no es un número
99999999999: no entra en un int
Suma: 14 (3 errores)
```

#### Solución de referencia

```cpp
// Mision 1 - Leer numeros de verdad: stoi con try/catch y el texto sobrante.
#include <iostream>
#include <stdexcept>
#include <string>

int a_entero(const std::string& s)
{
    std::size_t usados = 0;
    int n = std::stoi(s, &usados);            // puede lanzar invalid_argument u out_of_range
    if (usados != s.size()) {
        throw std::invalid_argument("sobran caracteres: \"" + s.substr(usados) + "\"");
    }
    return n;
}

int main()
{
    std::string palabra;
    int suma = 0, errores = 0;
    while (std::cin >> palabra) {
        try {
            suma += a_entero(palabra);
        } catch (const std::out_of_range&) {
            std::cout << palabra << ": no entra en un int\n";
            errores++;
        } catch (const std::invalid_argument& e) {
            std::cout << palabra << ": " << (std::string(e.what()) == "stoi" ? "no es un número" : e.what()) << "\n";
            errores++;
        }
    }
    std::cout << "Suma: " << suma << " (" << errores << " errores)\n";
    return 0;
}
```

#### Pruebas

##### Sin errores
```entrada
1 2 3
```
```salida
Suma: 6 (0 errores)
```

##### Todo errores
```entrada
abc 12.5 +
```
```salida
abc: no es un número
12.5: sobran caracteres: ".5"
+: no es un número
Suma: 0 (3 errores)
```

##### Límite del int
```entrada
2147483647 -2147483648
```
```salida
Suma: -1 (0 errores)
```

### Misión R05-N01-M2 · El depósito que valida

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class SinStock` (hereda de `std::runtime_error` y guarda lo pedido y lo que
hay) y `class Deposito` cuyo `sacar(producto, n)` lanza `std::invalid_argument` si
`n` no es positivo, `std::out_of_range` si el producto no existe, y `SinStock` si no
alcanza. Cargá 10 engranajes y 4 resortes; cada línea de la entrada es `producto
cantidad`. Atrapá `SinStock` (mostrando sus datos) y después `std::exception`.

#### Criterio de aprobación

- Los `catch` van del más específico al más general.
- La excepción propia lleva los datos del error.

#### Entrada de ejemplo

```
engranaje 3
resorte 6
valvula 1
engranaje -2
resorte 4
engranaje 7
```

#### Salida esperada

```
Salen 3 engranaje (quedan 7)
no alcanza el stock de resorte: pidieron 6, hay 4
Error: no existe el producto valvula
Error: la cantidad tiene que ser positiva
Salen 4 resorte (quedan 0)
Salen 7 engranaje (quedan 0)
```

#### Solución de referencia

```cpp
// Mision 2 - El deposito que valida: excepciones propias con datos del error.
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>

class SinStock : public std::runtime_error {
public:
    SinStock(const std::string& producto, int pedido, int hay)
        : std::runtime_error("no alcanza el stock de " + producto), pedido_(pedido), hay_(hay) {}
    int pedido() const { return pedido_; }
    int hay() const { return hay_; }

private:
    int pedido_;
    int hay_;
};

class Deposito {
public:
    void cargar(const std::string& p, int n) { stock_[p] += n; }

    void sacar(const std::string& p, int n)
    {
        if (n <= 0) {
            throw std::invalid_argument("la cantidad tiene que ser positiva");
        }
        auto it = stock_.find(p);
        if (it == stock_.end()) {
            throw std::out_of_range("no existe el producto " + p);
        }
        if (it->second < n) {
            throw SinStock(p, n, it->second);
        }
        it->second -= n;
    }

    int cuanto(const std::string& p) const
    {
        auto it = stock_.find(p);
        return it == stock_.end() ? 0 : it->second;
    }

private:
    std::map<std::string, int> stock_;
};

int main()
{
    Deposito d;
    d.cargar("engranaje", 10);
    d.cargar("resorte", 4);
    std::string producto;
    int n = 0;
    while (std::cin >> producto >> n) {
        try {
            d.sacar(producto, n);
            std::cout << "Salen " << n << " " << producto << " (quedan " << d.cuanto(producto) << ")\n";
        } catch (const SinStock& e) {
            std::cout << e.what() << ": pidieron " << e.pedido() << ", hay " << e.hay() << "\n";
        } catch (const std::exception& e) {
            std::cout << "Error: " << e.what() << "\n";
        }
    }
    return 0;
}
```

#### Pruebas

##### Pedir justo lo que hay
```entrada
resorte 4
resorte 1
```
```salida
Salen 4 resorte (quedan 0)
no alcanza el stock de resorte: pidieron 1, hay 0
```

##### Cero
```entrada
engranaje 0
```
```salida
Error: la cantidad tiene que ser positiva
```

### Misión R05-N01-M3 · ¿Dónde se atrapa?

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá una cadena de tres funciones: `informe` llama a `promedio`, que llama a
`dividir`, que lanza `std::domain_error` si divide por cero. Cada función crea un
objeto `Registro` que avisa al entrar y al salir. `main` llama a `informe` con
`{4, 8, 6}` y con un vector vacío, y atrapa el error. **Antes de ejecutar**,
anotá qué líneas esperás ver en el segundo caso y en qué orden.

#### Criterio de aprobación

- Solo `main` tiene `try`/`catch`.
- La salida muestra que los objetos se destruyen aunque haya excepción.

#### Salida esperada

```
Con 3 datos:
  entra a informe
  entra a promedio
  entra a dividir
  sale de dividir
  sale de promedio
  promedio: 6
  (esta línea no se ve si hubo error)
  sale de informe
Con 0 datos:
  entra a informe
  entra a promedio
  entra a dividir
  sale de dividir
  sale de promedio
  sale de informe
  main atrapa: división por cero
```

#### Solución de referencia

```cpp
// Mision 3 - Donde se atrapa: una excepcion que atraviesa varias funciones.
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Registro {
    std::string nombre;
    Registro(const std::string& n) : nombre(n) { std::cout << "  entra a " << nombre << "\n"; }
    ~Registro() { std::cout << "  sale de " << nombre << "\n"; }
};

int dividir(int a, int b)
{
    Registro r("dividir");
    if (b == 0) {
        throw std::domain_error("división por cero");
    }
    return a / b;
}

int promedio(const std::vector<int>& v)
{
    Registro r("promedio");
    int suma = 0;
    for (int x : v) {
        suma += x;
    }
    return dividir(suma, static_cast<int>(v.size()));
}

void informe(const std::vector<int>& v)
{
    Registro r("informe");
    int p = promedio(v);
    std::cout << "  promedio: " << p << "\n";
    std::cout << "  (esta línea no se ve si hubo error)\n";
}

int main()
{
    for (const auto& datos : {std::vector<int>{4, 8, 6}, std::vector<int>{}}) {
        std::cout << "Con " << datos.size() << " datos:\n";
        try {
            informe(datos);
        } catch (const std::domain_error& e) {
            std::cout << "  main atrapa: " << e.what() << "\n";
        }
    }
    return 0;
}
```

### Encargo R05-N01-E1 · Importar socios

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Cada línea de la entrada es un socio: `nombre,edad,cuota`. Escribí
`Socio leer_socio(const std::string& linea)`, que lanza una excepción propia
`LineaInvalida` si faltan campos, el nombre está vacío, un número no se puede
convertir (atrapá la de `stoi`/`stod` y **traducila** a `LineaInvalida`) o la edad
es imposible. El programa importa todo lo válido, informa cada línea inválida con
su número y muestra cuántos se importaron y la recaudación mensual.

#### Criterio de aprobación

- Un error en una línea no corta la importación.
- Los errores de la biblioteca se traducen a uno propio.
- Informa el número de línea.

#### Entrada de ejemplo

```
Ana,34,4500
Bruno,x,4500
,20,3000
Celi,150,4500
Dami,27
Eli,19,2500.5
```

#### Salida esperada

```
Línea 2: número inválido
Línea 3: nombre vacío
Línea 4: edad imposible: 150
Línea 5: faltan campos
Importados 2 de 6; recaudación mensual $7000.5
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Importar un CSV de socios: errores por linea sin cortar la importacion.
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

struct Socio {
    std::string nombre;
    int edad = 0;
    double cuota = 0;
};

class LineaInvalida : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

Socio leer_socio(const std::string& linea)
{
    std::istringstream in(linea);
    std::string nombre, edad, cuota;
    if (!std::getline(in, nombre, ',') || !std::getline(in, edad, ',') || !std::getline(in, cuota)) {
        throw LineaInvalida("faltan campos");
    }
    if (nombre.empty()) {
        throw LineaInvalida("nombre vacío");
    }
    Socio s;
    s.nombre = nombre;
    try {
        s.edad = std::stoi(edad);
        s.cuota = std::stod(cuota);
    } catch (const std::exception&) {
        throw LineaInvalida("número inválido");          // traducir el error a uno propio
    }
    if (s.edad < 0 || s.edad > 120) {
        throw LineaInvalida("edad imposible: " + std::to_string(s.edad));
    }
    return s;
}

int main()
{
    std::vector<Socio> socios;
    std::string linea;
    int numero = 0;
    while (std::getline(std::cin, linea)) {
        numero++;
        try {
            socios.push_back(leer_socio(linea));
        } catch (const LineaInvalida& e) {
            std::cout << "Línea " << numero << ": " << e.what() << "\n";
        }
    }
    double total = 0;
    for (const auto& s : socios) {
        total += s.cuota;
    }
    std::cout << "Importados " << socios.size() << " de " << numero << "; recaudación mensual $" << total << "\n";
    return 0;
}
```

#### Pruebas

##### Todo válido
```entrada
Ana,34,4500
Bruno,40,1000.25
```
```salida
Importados 2 de 2; recaudación mensual $5500.25
```

##### Edades en el borde
```entrada
A,0,100
B,-1,100
C,120,100
```
```salida
Línea 2: edad imposible: -1
Importados 2 de 3; recaudación mensual $200
```

##### Sin socios
```entrada
```
```salida
Importados 0 de 0; recaudación mensual $0
```

### Prueba del sello

#### ¿Qué pasa con el resto de una función cuando se ejecuta un `throw`?

No se ejecuta: la función se corta y la excepción sube hasta un `catch` que la atrape.

#### ¿Por qué se atrapa con `const std::exception& e` y no con `std::exception e`?

Para no copiar y no rebanar: así se conserva el tipo real y su mensaje.

#### ¿En qué orden van los `catch`?

Del tipo más específico al más general.

#### ¿Qué pasa con los objetos locales cuando una excepción atraviesa una función?

Se destruyen (corre su destructor), por eso RAII libera los recursos aunque haya error.

#### ¿Cuándo usarías `optional` en vez de una excepción?

Cuando "no hay resultado" es un caso normal, como buscar y no encontrar.

### Soluciones (docente)

Nodo nuevo: FullCursos solo usaba `try/catch` de pasada (`04/07-Optional`). Las excepciones se presentan acá, después de RAII, para explicar el *stack unwinding*.

## R05-N02 · Depuración y buenas prácticas

```meta
tipo: tema
padre: R05-N01
precio: 10
criatura: ogro
temas: cal.depuracion
```

### Crónica

Un autómata del Taller camina en círculos. No da error, no se detiene: solo hace algo que nadie le pidió. Los aprendices discuten teorías; Bron quiere abrirlo con la llave.

—Adivinar es lo más lento que hay —dice {mentor}, y saca una lupa y un cuaderno—. Se **observa**: qué hace, paso a paso, y dónde deja de hacer lo que debería. Y se le pide ayuda a las herramientas: el Taller tiene instrumentos que ven lo que tus ojos no ven.

Resulta que el autómata caminaba en círculos porque alguien le había atado un cordón entre las dos patas. Lyn jura que no fue ella. Lyn tiene un cordón de menos en la bota.

### Objetivos

Encontrar errores con método: leer las advertencias, usar `assert` para las
suposiciones, los **sanitizadores** (`-fsanitize=address,undefined`) y el
depurador `gdb`; y conocer las trampas más comunes de C++ y cómo evitarlas.

### Antes de empezar

- Excepciones (nodo anterior).
- Toda la rama 4.

### Explicación

#### El método
1. **Reproducí** el error con una entrada fija (un archivo de entrada).
2. **Achicá** el caso: la entrada más chica que todavía falla.
3. **Observá**: mostrá valores intermedios (con `std::cerr`, así no se mezclan
   con la salida normal) o usá el depurador.
4. **Formulá una hipótesis**, cambiá **una** cosa y volvé a probar.
5. Cuando lo arregles, **agregá una prueba** para que no vuelva (nodo siguiente).

#### Las advertencias son tu primera línea
Compilá siempre con `-Wall -Wextra`, y sumá `-Wshadow` (una variable que tapa a
otra con el mismo nombre) y `-Wconversion` (conversiones que pierden datos) cuando
busques un bug. Casi todos los bugs de esta lista los señala una advertencia.

#### `assert`: suposiciones que deben cumplirse
```cpp
#include <cassert>
assert(n > 0 && "n tiene que ser positivo");
```
Si la condición es falsa, el programa se detiene y dice **dónde**:
```
programa: main.cpp:3: int main(): Assertion `doble(3) == 7' failed.
```
`assert` es para **errores de programación** (una función llamada mal, un estado
imposible), no para validar lo que escribe el usuario: eso se valida siempre, con
`if`. Compilando con `-DNDEBUG` (versión final), los `assert` desaparecen.

#### Los sanitizadores
```bash
g++ -std=c++20 -Wall -Wextra -g -fsanitize=address,undefined -o programa main.cpp
```
El programa corre un poco más lento, pero **detiene y explica** los errores de
memoria y el comportamiento indefinido, con el archivo y la línea:
- *AddressSanitizer*: leer fuera de un array o vector, usar memoria liberada, dobles
  liberaciones, fugas.
- *UndefinedBehaviorSanitizer*: desbordes de enteros con signo, índices fuera de
  un array de C, divisiones por cero.

Es la herramienta que más tiempo te va a ahorrar: usala cada vez que algo "anda
raro".

#### El depurador: `gdb`
Compilá con `-g` (información para depurar) y:
```bash
gdb ./programa
(gdb) break promedio_ultimos     # detenerse al entrar a esa función
(gdb) run < entrada.txt          # ejecutar (con la entrada de un archivo)
(gdb) next                       # ejecutar la línea siguiente
(gdb) step                       # entrar en la función de la línea
(gdb) print suma                 # ver una variable
(gdb) backtrace                  # quién llamó a quién, hasta acá
(gdb) continue                   # seguir hasta el próximo break
```
Si el programa se corta (*Segmentation fault*), `run` y después `backtrace`
muestran **exactamente** dónde. VS Code, CLion y Qt Creator tienen el mismo
depurador con botones.

#### Trampas comunes de C++ (y cómo evitarlas)
| Trampa | Cómo se evita |
|---|---|
| índice fuera de rango | `.at()` al depurar, `for` de rango, sanitizador |
| iterador inválido tras modificar | `it = v.erase(it)`, `std::erase_if` |
| variable sin inicializar | inicializar siempre (`int x = 0;`, `T x{};`) |
| copia sin querer | `const T&` en parámetros y en el `for` |
| `int` que se desborda | `long long`, o revisar los límites |
| referencia o vista colgante | no devolver referencias a locales; vistas solo como parámetros |
| `new`/`delete` a mano | `std::vector`, `std::unique_ptr`, RAII |
| `while (!cin.eof())` | leer **en la condición**: `while (std::cin >> x)` |
| una variable que tapa a otra | `-Wshadow`, nombres claros |

> **Si venís de C.** Las mismas herramientas (`gdb`, sanitizadores) sirven para C.
> C++ agrega trampas propias (iteradores, copias, vistas), pero también muchas
> defensas (`at()`, RAII, punteros inteligentes).

### Código de ejemplo

```cpp
/*
 * Depuracion: un programa con dos bugs clasicos, y como encontrarlos.
 * Compilalo de dos maneras y compara:
 *   g++ -std=c++20 -Wall -Wextra -o programa main.cpp
 *   g++ -std=c++20 -Wall -Wextra -g -fsanitize=address,undefined -o programa main.cpp
 * Esta version ya esta CORREGIDA: los comentarios dicen donde estaban los bugs.
 */
#include <cassert>
#include <iomanip>
#include <iostream>
#include <vector>

// Promedio de los ultimos n valores. BUG 1 (ya corregido): el bucle empezaba en
// v.size() - n sin revisar que n <= v.size(), y leia fuera del vector.
double promedio_ultimos(const std::vector<int>& v, std::size_t n)
{
    assert(n > 0 && "n tiene que ser positivo");      // una suposicion que DEBE cumplirse
    if (n > v.size()) {
        n = v.size();
    }
    if (n == 0) {
        return 0;
    }
    long long suma = 0;                               // BUG 2 (ya corregido): era int y se desbordaba
    for (std::size_t i = v.size() - n; i < v.size(); i++) {
        suma += v[i];
    }
    return static_cast<double>(suma) / n;
}

int main()
{
    std::vector<int> ventas = {1200, 800, 1500, 2000000000, 2000000000};
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Últimos 2: " << promedio_ultimos(ventas, 2) << "\n";
    std::cout << "Últimos 10 (hay 5): " << promedio_ultimos(ventas, 10) << "\n";
    std::cout << "Últimos 3 de uno vacío: " << promedio_ultimos({}, 3) << "\n";
    return 0;
}
```

### Salida esperada

```
Últimos 2: 2000000000.0
Últimos 10 (hay 5): 800000700.0
Últimos 3 de uno vacío: 0.0
```

### ¿Para qué sirve?

En el trabajo real, se pasa más tiempo leyendo y arreglando código que escribiéndolo. Saber depurar con método (reproducir, achicar, observar) y usar herramientas (sanitizadores, depurador) es lo que distingue a quien tarda cinco minutos en encontrar un bug de quien tarda un día. En videojuegos, sistemas embebidos o servidores, donde un error de memoria puede aparecer una vez cada mil ejecuciones, los sanitizadores son imprescindibles.

### Errores habituales

**Ogro: el `assert` que falla.**
```
programa: main.cpp:3: int main(): Assertion `doble(3) == 7' failed.
Abortado (`core' generado)
```

**Ogro: desborde, visto por el sanitizador.**
```
main.cpp:3:49: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

**Orco: índice fuera de un array, visto por el sanitizador.**
```
main.cpp:3:125: runtime error: index 3 out of bounds for type 'int [3]'
```

**Orco: `at()` fuera de rango.**
```
terminate called after throwing an instance of 'std::out_of_range'
  what():  vector::_M_range_check: __n (which is 3) >= this->size() (which is 0)
```

**Ogro: una variable que tapa a otra.**
```
main.cpp:1:68: warning: declaration of ‘int vida’ shadows a parameter [-Wshadow]
```

**Ogro: `assert` con efectos.** `assert(guardar(archivo));` desaparece al compilar
con `-DNDEBUG`, ¡y el archivo no se guarda! Dentro de un `assert`, solo
comprobaciones sin efectos.

### Misión R05-N02-M1 · La lista de compras rota

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este programa tiene **tres** bugs. Encontralos con las advertencias, el sanitizador
o el depurador, arreglalos y dejá un comentario sobre cada uno:
```cpp
double total(const std::vector<Item>& items)
{
    double t;
    for (const auto& it : items) t += it.cantidad * it.precio;
    return t;
}
const Item* mas_caro(const std::vector<Item>& items)
{
    const Item* mejor = nullptr;
    for (std::size_t i = 0; i <= items.size(); i++)
        if (mejor == nullptr || items[i].precio > mejor->precio) mejor = &items[i];
    return mejor;
}
void quitar_sin_stock(std::vector<Item> items)
{
    std::erase_if(items, [](const Item& it) { return it.cantidad == 0; });
}
```
El `main` lee ítems (`nombre cantidad precio`), quita los que no tienen stock y
muestra cuántos quedan, el total y el más caro.

#### Criterio de aprobación

- Corrige los tres bugs (sin inicializar, uno de más, parámetro por valor).
- Deja un comentario explicando cada uno.
- Compila sin advertencias y sin errores del sanitizador.

#### Entrada de ejemplo

```
yerba 2 2500
azucar 0 1200
fideos 3 950
aceite 1 3100
```

#### Salida esperada

```
Ítems: 3
Total: $10950
El más caro: aceite
```

#### Solución de referencia

```cpp
// Mision 1 - La lista de compras arreglada (tenia tres bugs).
#include <iostream>
#include <string>
#include <vector>

struct Item {
    std::string nombre;
    int cantidad = 0;
    double precio = 0;
};

// BUG 1: el total arrancaba sin inicializar (double total;).
double total(const std::vector<Item>& items)
{
    double t = 0;
    for (const auto& it : items) {
        t += it.cantidad * it.precio;
    }
    return t;
}

// BUG 2: el for iba hasta <= size() y leia uno de mas.
const Item* mas_caro(const std::vector<Item>& items)
{
    const Item* mejor = nullptr;
    for (std::size_t i = 0; i < items.size(); i++) {
        if (mejor == nullptr || items[i].precio > mejor->precio) {
            mejor = &items[i];
        }
    }
    return mejor;
}

// BUG 3: recibia el vector por valor y "quitaba" de una copia.
void quitar_sin_stock(std::vector<Item>& items)
{
    std::erase_if(items, [](const Item& it) { return it.cantidad == 0; });
}

int main()
{
    std::vector<Item> lista;
    Item it;
    while (std::cin >> it.nombre >> it.cantidad >> it.precio) {
        lista.push_back(it);
    }
    quitar_sin_stock(lista);
    std::cout << "Ítems: " << lista.size() << "\n";
    std::cout << "Total: $" << total(lista) << "\n";
    if (const Item* caro = mas_caro(lista)) {
        std::cout << "El más caro: " << caro->nombre << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Todo sin stock
```entrada
a 0 100
b 0 200
```
```salida
Ítems: 0
Total: $0
```

##### Un solo ítem
```entrada
cafe 1 4000
```
```salida
Ítems: 1
Total: $4000
El más caro: cafe
```

### Misión R05-N02-M2 · Funciones que se defienden

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `en_letras(nota)` (de "uno" a "diez") con un `assert` de su precondición
(1 a 10), y `repartir(total, partes)`, que divide un total en partes casi iguales
(las primeras reciben uno más) con un `assert` de que las partes **suman el
total**. En `main`, leé notas: la entrada del usuario se valida con `if` (**no**
con `assert`). Al final, mostrá el reparto de 17 en 5.

Probá qué pasa si llamás a `en_letras(0)` directamente: el `assert` tiene que
detener el programa.

#### Criterio de aprobación

- Los `assert` verifican suposiciones del programador, no la entrada.
- La entrada inválida se informa sin cortar el programa.

#### Entrada de ejemplo

```
7 11 1 0 10
```

#### Salida esperada

```
7: siete
11: nota inválida
1: uno
0: nota inválida
10: diez
Reparto de 17 en 5: 4 4 3 3 3
```

#### Solución de referencia

```cpp
// Mision 2 - Suposiciones con assert: funciones que se defienden.
#include <cassert>
#include <iostream>
#include <string>
#include <vector>

// Devuelve la nota en letras. Precondicion: 1 <= nota <= 10.
std::string en_letras(int nota)
{
    assert(nota >= 1 && nota <= 10 && "la nota tiene que estar entre 1 y 10");
    const std::vector<std::string> NOMBRES = {"uno", "dos", "tres", "cuatro", "cinco",
                                              "seis", "siete", "ocho", "nueve", "diez"};
    return NOMBRES[nota - 1];
}

// Divide el total en partes casi iguales. Postcondicion: las partes suman el total.
std::vector<int> repartir(int total, int partes)
{
    assert(partes > 0);
    std::vector<int> r(partes, total / partes);
    for (int i = 0; i < total % partes; i++) {
        r[i]++;
    }
    int suma = 0;
    for (int x : r) {
        suma += x;
    }
    assert(suma == total && "el reparto tiene que sumar el total");
    return r;
}

int main()
{
    int nota = 0;
    while (std::cin >> nota) {
        if (nota < 1 || nota > 10) {             // la entrada del usuario se valida SIEMPRE, no con assert
            std::cout << nota << ": nota inválida\n";
            continue;
        }
        std::cout << nota << ": " << en_letras(nota) << "\n";
    }
    std::cout << "Reparto de 17 en 5:";
    for (int x : repartir(17, 5)) {
        std::cout << " " << x;
    }
    std::cout << "\n";
    return 0;
}
```

#### Pruebas

##### Sin notas
```entrada
```
```salida
Reparto de 17 en 5: 4 4 3 3 3
```

##### Todas válidas
```entrada
1 2 3 4 5 6 7 8 9 10
```
```salida
1: uno
2: dos
3: tres
4: cuatro
5: cinco
6: seis
7: siete
8: ocho
9: nueve
10: diez
Reparto de 17 en 5: 4 4 3 3 3
```

##### Todas inválidas
```entrada
-1 100 0
```
```salida
-1: nota inválida
100: nota inválida
0: nota inválida
Reparto de 17 en 5: 4 4 3 3 3
```

### Misión R05-N02-M3 · Limpiar la función tramposa

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Esta función compila con varias advertencias y tiene un comportamiento indefinido.
Reescribila limpia:
```cpp
std::vector<std::string> ganadores(std::vector<Jugador> jugadores, int minimo)
{
    std::vector<std::string> nombres;
    for (int i = 0; i < jugadores.size(); i++) {
        int puntos = jugadores[i].puntos;
        for (auto it = jugadores.begin(); it != jugadores.end(); ++it)
            if (it->puntos < minimo) jugadores.erase(it);
        ...
    }
}
```
Tiene que devolver los nombres de los que tienen `minimo` puntos o más, ordenados
de más a menos puntos (y por nombre si empatan). Usá `const&`, `std::erase_if` y
`std::ranges::sort`. La primera línea de la entrada es el mínimo; las siguientes,
`nombre puntos`.

#### Criterio de aprobación

- Compila sin advertencias con `-Wall -Wextra -Wshadow`.
- No borra mientras recorre con un iterador.
- Recibe el vector por `const&`.

#### Entrada de ejemplo

```
100
Lima 340
Bron 80
Lyn 120
Oto 100
Tesla 340
```

#### Salida esperada

```
4 con 100 o más: Lima Tesla Lyn Oto
```

#### Solución de referencia

```cpp
// Mision 3 - Buenas practicas: la version limpia de una funcion llena de trampas.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Jugador {
    std::string nombre;
    int puntos = 0;
};

// Antes: recibia el vector por valor, usaba int para el indice (-Wsign-compare),
// una variable 'puntos' tapaba al campo (-Wshadow) y borraba dentro del for (iterador invalido).
std::vector<std::string> ganadores(const std::vector<Jugador>& jugadores, int minimo)
{
    std::vector<Jugador> copia = jugadores;
    std::erase_if(copia, [minimo](const Jugador& j) { return j.puntos < minimo; });
    std::ranges::sort(copia, [](const Jugador& a, const Jugador& b) {
        return a.puntos != b.puntos ? a.puntos > b.puntos : a.nombre < b.nombre;
    });
    std::vector<std::string> nombres;
    for (const auto& j : copia) {
        nombres.push_back(j.nombre);
    }
    return nombres;
}

int main()
{
    int minimo = 0;
    std::cin >> minimo;
    std::vector<Jugador> jugadores;
    Jugador j;
    while (std::cin >> j.nombre >> j.puntos) {
        jugadores.push_back(j);
    }
    const auto lista = ganadores(jugadores, minimo);
    std::cout << lista.size() << " con " << minimo << " o más:";
    for (const auto& n : lista) {
        std::cout << " " << n;
    }
    std::cout << "\n";
    return 0;
}
```

#### Pruebas

##### Nadie llega
```entrada
500
Lima 340
Bron 80
```
```salida
0 con 500 o más:
```

##### Todos empatados
```entrada
0
C 5
A 5
B 5
```
```salida
3 con 0 o más: A B C
```

### Encargo R05-N02-E1 · La planilla de horas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un comercio registra las horas trabajadas: cada línea es `empleado horas`. El
programa que usaban tenía tres errores: leía con `while (!std::cin.eof())` (y
repetía el último registro), no validaba las horas (aceptaba −3 o 30) y calculaba
el promedio dividiendo por la cantidad de **empleados** en vez de los días de cada
uno. Escribí la versión correcta: total y días por empleado, el promedio diario y
las horas extra (más de 40 en total), con 1 decimal. Comentá cada arreglo.

#### Criterio de aprobación

- Lee en la condición del `while`.
- Ignora e informa los registros imposibles.
- El promedio es por empleado.

#### Entrada de ejemplo

```
ana 8
beto 9
ana 9.5
beto -3
ana 30
caro 7
beto 10
ana 8
beto 12
beto 11
```

#### Salida esperada

```
Registro ignorado: beto -3
Registro ignorado: ana 30
ana: 25.5 h en 3 días (promedio 8.5)
beto: 42.0 h en 4 días (promedio 10.5) +2.0 h extra
caro: 7.0 h en 1 días (promedio 7.0)
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La planilla de horas: un informe con los errores corregidos y comentados.
#include <iomanip>
#include <iostream>
#include <map>
#include <string>

int main()
{
    std::map<std::string, double> horas;
    std::map<std::string, int> dias;
    std::string empleado;
    double h = 0;
    // Antes: while (!std::cin.eof()) repetia el ultimo registro. Se lee en la condicion.
    while (std::cin >> empleado >> h) {
        if (h < 0 || h > 24) {                     // antes no se validaba
            std::cout << "Registro ignorado: " << empleado << " " << h << "\n";
            continue;
        }
        horas[empleado] += h;
        dias[empleado]++;
    }
    std::cout << std::fixed << std::setprecision(1);
    for (const auto& [nombre, total] : horas) {
        double promedio = total / dias[nombre];    // antes: total / dias.size() (el promedio de todos)
        std::cout << nombre << ": " << total << " h en " << dias[nombre] << " días (promedio " << promedio << ")";
        if (total > 40) {
            std::cout << " +" << total - 40 << " h extra";
        }
        std::cout << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Horas en el borde
```entrada
ana 0
ana 24
ana 24.5
```
```salida
Registro ignorado: ana 24.5
ana: 24.0 h en 2 días (promedio 12.0)
```

##### Un solo empleado con extra
```entrada
zoe 10
zoe 10
zoe 10
zoe 10
zoe 10
```
```salida
zoe: 50.0 h en 5 días (promedio 10.0) +10.0 h extra
```

### Prueba del sello

#### ¿Cuáles son los pasos para depurar con método?

Reproducir con una entrada fija, achicar el caso, observar, probar una hipótesis cambiando una cosa, y agregar una prueba.

#### ¿Para qué sirve `assert`? ¿Sirve para validar lo que escribe el usuario?

Para detener el programa si una suposición del programador no se cumple. No: la entrada del usuario se valida con `if`.

#### ¿Qué detecta `-fsanitize=address,undefined`?

Errores de memoria (fuera de rango, uso después de liberar, fugas) y comportamiento indefinido (desbordes, índices inválidos).

#### En `gdb`, ¿qué hacen `break`, `next`, `print` y `backtrace`?

Detenerse en un lugar, avanzar una línea, mostrar una variable y ver la cadena de llamadas.

#### ¿Por qué `while (!std::cin.eof())` es una trampa?

Porque el fin de archivo se detecta recién después de una lectura fallida: la última vuelta procesa datos viejos. Hay que leer en la condición.

### Soluciones (docente)

Material original: `11-STL/13-Errores-Buenas-Practicas`, con depuración (`gdb`, sanitizadores, `assert`) agregada. En M1 y M3 el alumno entrega el código corregido y comentado.

## R05-N03 · Pruebas y medición

```meta
tipo: tema
padre: R05-N02
precio: 10
criatura: ogro
temas: cal.pruebas, cal.rendimiento
```

### Crónica

Antes de que una máquina salga del Taller, pasa por el **Banco de Pruebas** de la Maestra Artífice: una mesa larga con palancas que la hacen trabajar en todos los casos raros que a alguien se le ocurrieron. Si una prueba falla, la máquina no sale.

Bron dice que su máquina «ya anda». La Maestra no levanta la vista: —¿Y la prueba? —Esta vez Bron tiene las pruebas: doce, escritas, y las corre delante de ella. Pasan todas en verde. La Maestra sonríe **medio segundo**. Lima jura que fue un tic.

—Probar a mano una vez no alcanza —dice {mentor}—. Las pruebas se **escriben**, y se corren cada vez que cambiás algo. Y cuando alguien dice «esto es más rápido», se **mide**. No se opina.

### Objetivos

Escribir **pruebas automáticas**: funciones que comprueban casos normales y casos
borde y cuentan cuáles pasan; probar clases y sus invariantes; y **medir el
tiempo** con `<chrono>` (`steady_clock`, `duration_cast`) y un cronómetro RAII.

### Antes de empezar

- Depuración (nodo anterior).
- RAII (rama 3) y lambdas.

### Explicación

#### ¿Por qué pruebas automáticas?
Una prueba es código que **usa** tu código y comprueba el resultado. La escribís
una vez y la corrés siempre: si mañana cambiás algo y rompés lo que andaba, te
enterás en un segundo.
```cpp
void comprobar(bool condicion, const std::string& descripcion)
{
    if (condicion) pasaron++;
    else { fallaron++; std::cout << "FALLA: " << descripcion << "\n"; }
}
comprobar(es_bisiesto(2024), "2024 es bisiesto");
comprobar(!es_bisiesto(1900), "1900 no es bisiesto");
```
El programa de pruebas termina con `return fallaron == 0 ? 0 : 1;`: así otras
herramientas (un script, la integración continua) saben si todo anduvo.

#### Qué probar
- **Casos normales**: lo que se usa todos los días.
- **Casos borde**: los límites. Si la regla es "8 o más caracteres", probá 7 y 8.
  Si es "hasta 160 horas", probá 160 y 161. Ahí viven la mayoría de los bugs.
- **Casos vacíos y raros**: el texto vacío, el vector vacío, el cero, los
  negativos.
- **Invariantes** de las clases: después de cualquier operación, ¿se sigue
  cumpliendo la regla?

Agrupá las pruebas en funciones (`probar_construccion`, `probar_operaciones`).

#### Comparar decimales
`0.1 + 0.2 == 0.3` es falso. Los `double` se comparan con **tolerancia**:
`std::abs(obtenido - esperado) < 0.001`.

#### Frameworks de pruebas
En proyectos reales se usan bibliotecas como **GoogleTest** o **Catch2**, que
hacen lo mismo que `comprobar` con más comodidades (mensajes, grupos, correr solo
algunas). La idea es idéntica: si sabés escribir las tuyas, sabés usar cualquiera.

#### Medir el tiempo: `<chrono>`
```cpp
auto t0 = std::chrono::steady_clock::now();
hacer_algo();
auto t1 = std::chrono::steady_clock::now();
auto us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
```
- `steady_clock` es el reloj para **medir duraciones** (nunca retrocede).
  `system_clock` es la hora del día (para fechas).
- `t1 - t0` es una duración; `duration_cast<milliseconds>` o `<microseconds>` la
  convierte y `.count()` da el número.

Un **cronómetro RAII** mide lo que vive su bloque: toma la hora en el constructor
y muestra la diferencia en el destructor.

#### Medir bien
- Compilá con optimizaciones (`-O2`) para medir en serio.
- Repetí la operación muchas veces y medí el total.
- Los tiempos **cambian en cada compu y en cada ejecución**: en los programas del
  curso salen por `std::cerr`, y por `std::cout` solo lo que no cambia.
- "Esto es más rápido" se dice **después** de medir.

> **Si venís de C.** `<chrono>` reemplaza a `clock()` y `time()`, con unidades que
> el compilador revisa (no se mezclan milisegundos con segundos por accidente).

### Código de ejemplo

```cpp
/*
 * Pruebas automaticas y medicion de tiempo.
 * Los tiempos salen por std::cerr (cambian en cada compu); el resultado de las pruebas, por std::cout.
 */
#include <chrono>
#include <iostream>
#include <string>
#include <vector>

// --- un mini "framework" de pruebas ---
int pasaron = 0;
int fallaron = 0;

void comprobar(bool condicion, const std::string& descripcion)
{
    if (condicion) {
        pasaron++;
    } else {
        fallaron++;
        std::cout << "  FALLA: " << descripcion << "\n";
    }
}

// --- un cronometro RAII: mide lo que vive su bloque ---
class Cronometro {
public:
    explicit Cronometro(const std::string& que) : que_(que), inicio_(std::chrono::steady_clock::now()) {}
    ~Cronometro()
    {
        auto fin = std::chrono::steady_clock::now();
        auto us = std::chrono::duration_cast<std::chrono::microseconds>(fin - inicio_).count();
        std::cerr << "[tiempo] " << que_ << ": " << us << " µs\n";
    }

private:
    std::string que_;
    std::chrono::steady_clock::time_point inicio_;
};

// --- lo que se prueba ---
bool es_bisiesto(int anio)
{
    return (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
}

std::string invertir(const std::string& s)
{
    return std::string(s.rbegin(), s.rend());
}

long long suma_hasta(int n)
{
    long long s = 0;
    for (int i = 1; i <= n; i++) {
        s += i;
    }
    return s;
}

int main()
{
    std::cout << "Probando es_bisiesto...\n";
    comprobar(es_bisiesto(2024), "2024 es bisiesto");
    comprobar(!es_bisiesto(2023), "2023 no es bisiesto");
    comprobar(!es_bisiesto(1900), "1900 no es bisiesto (divisible por 100)");
    comprobar(es_bisiesto(2000), "2000 es bisiesto (divisible por 400)");

    std::cout << "Probando invertir...\n";
    comprobar(invertir("abc") == "cba", "abc -> cba");
    comprobar(invertir("") == "", "el texto vacío queda vacío");
    comprobar(invertir("a") == "a", "una letra queda igual");

    std::cout << "Probando suma_hasta...\n";
    comprobar(suma_hasta(0) == 0, "hasta 0 da 0");
    comprobar(suma_hasta(10) == 55, "hasta 10 da 55");
    {
        Cronometro c("suma_hasta(1000000)");
        comprobar(suma_hasta(1000000) == 500000500000LL, "hasta un millón (no se desborda)");
    }
    std::cout << pasaron << " pasaron, " << fallaron << " fallaron\n";
    return fallaron == 0 ? 0 : 1;          // un programa de pruebas devuelve error si algo fallo
}
```

### Salida esperada

```
Probando es_bisiesto...
Probando invertir...
Probando suma_hasta...
10 pasaron, 0 fallaron
```

### ¿Para qué sirve?

Ningún equipo profesional entrega código sin pruebas: cada cambio corre miles de pruebas automáticas antes de llegar a los usuarios. Medir es lo que permite optimizar donde importa: el cuadro de un juego que tarda más de 16 ms, la consulta que hace lenta una página, el algoritmo que no escala con un millón de datos. Los cronómetros RAII son la base de los *profilers* que usan los motores de juegos.

### Errores habituales

**Ogro: probar solo el caso feliz.** Si solo probás "2024 es bisiesto", el bug de
1900 pasa. Los bordes y los casos raros son la parte importante.

**Ogro: comparar `double` con `==`.** Una prueba que "falla a veces" o que falla
con valores que parecen iguales.

**Ogro: una prueba que depende de otra.** Si la segunda prueba usa lo que dejó la
primera, al cambiar el orden todo se rompe. Cada prueba arma sus propios datos.

**Ogro: medir sin optimizar o una sola vez.** Los números no significan nada.
Medí con `-O2` y repitiendo.

**Goblin: mezclar unidades.** `duration_cast<milliseconds>` de algo que tarda 300
microsegundos da **0**. Elegí la unidad según lo que medís.

**Ogro: poner los tiempos en la salida que se compara.** Cambian en cada
ejecución: la prueba nunca coincide. Los tiempos, por `std::cerr`.

### Misión R05-N03-M1 · Las contraseñas seguras

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una contraseña es segura si tiene **8 o más** caracteres, al menos una mayúscula,
una minúscula y un dígito, y ningún espacio. Escribí `contrasenia_segura` y las
pruebas: una buena, 6 y 7 caracteres (no), **8** justos (sí), sin mayúscula, sin
minúscula, sin dígito, con espacio y vacía. Tip: probá primero con el límite mal
puesto (`< 7`) y mirá qué prueba lo detecta.

#### Criterio de aprobación

- Prueba los dos lados del borde (7 y 8 caracteres).
- Prueba cada regla por separado.
- El programa devuelve 1 si alguna prueba falla.

#### Salida esperada

```
9 pasaron, 0 fallaron
```

#### Solución de referencia

```cpp
// Mision 1 - Pruebas para la validacion de contrasenias (con un bug que las pruebas encuentran).
#include <cctype>
#include <iostream>
#include <string>

int pasaron = 0, fallaron = 0;

void comprobar(bool condicion, const std::string& descripcion)
{
    if (condicion) {
        pasaron++;
    } else {
        fallaron++;
        std::cout << "FALLA: " << descripcion << "\n";
    }
}

// Valida: 8 o mas caracteres, al menos una mayuscula, una minuscula y un digito, sin espacios.
bool contrasenia_segura(const std::string& c)
{
    if (c.size() < 8) {                 // el bug era "< 7": aceptaba 7 caracteres
        return false;
    }
    bool mayus = false, minus = false, digito = false;
    for (char ch : c) {
        unsigned char u = static_cast<unsigned char>(ch);
        if (std::isspace(u)) {
            return false;
        }
        mayus = mayus || std::isupper(u);
        minus = minus || std::islower(u);
        digito = digito || std::isdigit(u);
    }
    return mayus && minus && digito;
}

int main()
{
    comprobar(contrasenia_segura("Ciudad3la"), "una buena es segura");
    comprobar(!contrasenia_segura("Ciud4d"), "6 caracteres es poco");
    comprobar(!contrasenia_segura("Ciuda4d"), "7 caracteres es poco (borde)");
    comprobar(contrasenia_segura("Ciudad4d"), "8 caracteres alcanza (borde)");
    comprobar(!contrasenia_segura("ciudad3la"), "sin mayúscula no");
    comprobar(!contrasenia_segura("CIUDAD3LA"), "sin minúscula no");
    comprobar(!contrasenia_segura("Ciudadela"), "sin dígito no");
    comprobar(!contrasenia_segura("Ciudad 3la"), "con espacio no");
    comprobar(!contrasenia_segura(""), "vacía no");
    std::cout << pasaron << " pasaron, " << fallaron << " fallaron\n";
    return fallaron == 0 ? 0 : 1;
}
```

### Misión R05-N03-M2 · Probar la fracción

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Tomá la `Fraccion` (siempre simplificada, denominador positivo, con `+`, `*` y `==`)
y escribí dos grupos de pruebas: **construcción** (2/4 = 1/2, el signo pasa al
numerador, denominador 0 → 1, cero es 0/1) y **operaciones** (1/2 + 1/3, 2/3 × 3/2,
a + (−a) = 0, un entero más una fracción). Mostrá el resultado de cada grupo y el
total.

#### Criterio de aprobación

- Las pruebas están agrupadas en funciones.
- Se prueban las invariantes, no solo las cuentas.

#### Salida esperada

```
Construcción:
Operaciones:
8 pasaron, 0 fallaron
```

#### Solución de referencia

```cpp
// Mision 2 - Probar una clase: la Fraccion y sus invariantes.
#include <iostream>
#include <numeric>
#include <string>

class Fraccion {
public:
    Fraccion(int n = 0, int d = 1) : n_(n), d_(d == 0 ? 1 : d) { normalizar(); }
    Fraccion operator+(const Fraccion& o) const { return Fraccion(n_ * o.d_ + o.n_ * d_, d_ * o.d_); }
    Fraccion operator*(const Fraccion& o) const { return Fraccion(n_ * o.n_, d_ * o.d_); }
    bool operator==(const Fraccion&) const = default;
    int num() const { return n_; }
    int den() const { return d_; }

private:
    void normalizar()
    {
        if (d_ < 0) {
            n_ = -n_;
            d_ = -d_;
        }
        int g = std::gcd(n_, d_);
        if (g > 1) {
            n_ /= g;
            d_ /= g;
        }
    }
    int n_;
    int d_;
};

int pasaron = 0, fallaron = 0;

void comprobar(bool c, const std::string& d)
{
    if (c) {
        pasaron++;
    } else {
        fallaron++;
        std::cout << "FALLA: " << d << "\n";
    }
}

void probar_construccion()
{
    comprobar(Fraccion(2, 4) == Fraccion(1, 2), "2/4 se simplifica a 1/2");
    comprobar(Fraccion(3, -6).num() == -1 && Fraccion(3, -6).den() == 2, "el signo pasa al numerador");
    comprobar(Fraccion(5, 0).den() == 1, "denominador 0 se reemplaza por 1");
    comprobar(Fraccion(0, 7) == Fraccion(0, 1), "cero es 0/1");
}

void probar_operaciones()
{
    comprobar(Fraccion(1, 2) + Fraccion(1, 3) == Fraccion(5, 6), "1/2 + 1/3 = 5/6");
    comprobar(Fraccion(2, 3) * Fraccion(3, 2) == Fraccion(1), "2/3 * 3/2 = 1");
    comprobar(Fraccion(1, 2) + Fraccion(-1, 2) == Fraccion(0), "a + (-a) = 0");
    comprobar(Fraccion(3) + Fraccion(1, 4) == Fraccion(13, 4), "un entero se convierte en fracción");
}

int main()
{
    std::cout << "Construcción:\n";
    probar_construccion();
    std::cout << "Operaciones:\n";
    probar_operaciones();
    std::cout << pasaron << " pasaron, " << fallaron << " fallaron\n";
    return fallaron == 0 ? 0 : 1;
}
```

### Misión R05-N03-M3 · Medir antes de opinar

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá un vector con los números de 0 a 199999 desordenados, un `std::set` con los
mismos y una copia ordenada del vector. Medí con `<chrono>` cuánto tardan 2000
búsquedas en cada uno: `std::find` en el vector, `contains` en el set y
`std::binary_search` en el vector ordenado. Por `std::cout` mostrá solo lo que no
cambia (cuántas búsquedas, cuántos encontró cada uno, si ganó la búsqueda lineal);
los tiempos, por `std::cerr`. Escribí una función plantilla `medir_us(lambda)`.

#### Criterio de aprobación

- Mide con `steady_clock` y `duration_cast`.
- Los tiempos van por `std::cerr` y la salida estándar es siempre la misma.
- Encuentra los mismos números con los tres métodos.

#### Salida esperada

```
Búsquedas: 2000
Encontrados: 2000 / 2000 / 2000
¿Ganó la búsqueda lineal? no
```

#### Solución de referencia

```cpp
// Mision 3 - Medir antes de opinar: buscar en vector, en set y en vector ordenado.
#include <algorithm>
#include <chrono>
#include <iostream>
#include <set>
#include <string>
#include <vector>

template <typename F>
long long medir_us(F&& f)
{
    auto t0 = std::chrono::steady_clock::now();
    f();
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
}

int main()
{
    const int N = 200000;
    std::vector<int> v;
    for (int i = 0; i < N; i++) {
        v.push_back((i * 7919) % N);          // todos los numeros de 0 a N-1, desordenados
    }
    std::set<int> s(v.begin(), v.end());
    std::vector<int> ordenado = v;
    std::sort(ordenado.begin(), ordenado.end());

    int encontrados_v = 0, encontrados_s = 0, encontrados_b = 0;
    auto t_vector = medir_us([&] {
        for (int x = 0; x < N; x += 100) {
            encontrados_v += std::find(v.begin(), v.end(), x) != v.end();
        }
    });
    auto t_set = medir_us([&] {
        for (int x = 0; x < N; x += 100) {
            encontrados_s += s.contains(x);
        }
    });
    auto t_binaria = medir_us([&] {
        for (int x = 0; x < N; x += 100) {
            encontrados_b += std::binary_search(ordenado.begin(), ordenado.end(), x);
        }
    });
    // Lo que no depende de la compu, por cout; los tiempos, por cerr.
    std::cout << "Búsquedas: " << N / 100 << "\n";
    std::cout << "Encontrados: " << encontrados_v << " / " << encontrados_s << " / " << encontrados_b << "\n";
    std::cout << "¿Ganó la búsqueda lineal? " << (t_vector < t_set && t_vector < t_binaria ? "sí" : "no") << "\n";
    std::cerr << "vector (find): " << t_vector << " µs\n";
    std::cerr << "set (contains): " << t_set << " µs\n";
    std::cerr << "vector ordenado (binary_search): " << t_binaria << " µs\n";
    return 0;
}
```

### Encargo R05-N03-E1 · Las pruebas de la liquidación

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una empresa liquida horas así: las primeras 160 del mes al valor normal; de 160 a
200, con 50% más; las que pasan de 200, al doble. Con horas o valor no positivos,
paga 0. Escribí `liquidar(horas, valor_hora)` y sus pruebas con **tolerancia**
para `double`, incluyendo los bordes (160, 161, 200, 210), los casos inválidos y
media hora extra.

#### Criterio de aprobación

- Compara los `double` con tolerancia.
- Prueba los dos lados de cada borde.

#### Salida esperada

```
9 pasaron, 0 fallaron
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Las pruebas del calculo de sueldos: casos borde de la liquidacion.
#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

// Liquida horas: las primeras 160 del mes al valor normal; las siguientes, al 50% mas.
// Si hay mas de 200 horas, las que pasan de 200 se pagan al doble.
double liquidar(double horas, double valor_hora)
{
    if (horas <= 0 || valor_hora <= 0) {
        return 0;
    }
    double normales = std::min(horas, 160.0);
    double extras50 = std::max(0.0, std::min(horas, 200.0) - 160);
    double extras100 = std::max(0.0, horas - 200);
    return normales * valor_hora + extras50 * valor_hora * 1.5 + extras100 * valor_hora * 2;
}

int pasaron = 0, fallaron = 0;

void comprobar(double obtenido, double esperado, const std::string& d)
{
    if (std::abs(obtenido - esperado) < 0.001) {       // los double se comparan con tolerancia
        pasaron++;
    } else {
        fallaron++;
        std::cout << "FALLA: " << d << " (dio " << obtenido << ", esperaba " << esperado << ")\n";
    }
}

int main()
{
    comprobar(liquidar(100, 1000), 100000, "menos de 160 horas");
    comprobar(liquidar(160, 1000), 160000, "justo 160 (borde)");
    comprobar(liquidar(161, 1000), 161500, "una hora extra");
    comprobar(liquidar(200, 1000), 220000, "justo 200 (borde)");
    comprobar(liquidar(210, 1000), 240000, "10 horas al doble");
    comprobar(liquidar(0, 1000), 0, "cero horas");
    comprobar(liquidar(-5, 1000), 0, "horas negativas");
    comprobar(liquidar(100, 0), 0, "valor cero");
    comprobar(liquidar(160.5, 1000), 160750, "media hora extra");
    std::cout << pasaron << " pasaron, " << fallaron << " fallaron\n";
    return fallaron == 0 ? 0 : 1;
}
```

### Prueba del sello

#### ¿Qué es un caso borde? Dá un ejemplo.

Un valor en el límite de una regla; por ejemplo, 7 y 8 caracteres si la regla es "8 o más".

#### ¿Por qué un programa de pruebas devuelve 1 si algo falla?

Para que otras herramientas sepan, sin leer la salida, que las pruebas no pasaron.

#### ¿Cómo se comparan dos `double` en una prueba?

Con tolerancia: `std::abs(a - b) < 0.001`.

#### ¿Qué reloj se usa para medir cuánto tarda algo?

`std::chrono::steady_clock`.

#### ¿Por qué los tiempos van por `std::cerr` en las misiones?

Porque cambian en cada ejecución y no pueden formar parte de la salida que se compara.

### Soluciones (docente)

Material original: `11-STL/10-Chrono` (el cronómetro RAII) más pruebas automáticas, que FullCursos no tenía en C++. En M3 la salida estándar es determinista; los tiempos, no.

## R05-N04 · Las piezas de un juego

```meta
tipo: tema
padre: R05-N03
precio: 10
criatura: orco
temas: juegos.ia, diseno.maquina-estados
usa: poo.encapsulamiento, err.opcionales
```

### Crónica

En el fondo del Taller hay una mesa con las piezas de un juego desarmado: una heroína de madera, enemigos de lata, una mochila de cuero, un dado. Bron arma la heroína con la cara de Lima, «porque es la que más pelea». Lima no sabe si ofenderse.

—Un juego no es una máquina misteriosa —dice {mentor}—. Es un montón de piezas chicas que ya sabés hacer: clases con reglas, un inventario, una IA que decide, un combate con azar. Juntalas bien y tenés un juego.

Oto pide que haya un enemigo que sea un guiso violeta. Se lo agregan.

### Objetivos

Diseñar las piezas de un juego con lo aprendido: personajes con reglas
(encapsulamiento), una **IA** simple que decide según la situación (máquina de
estados), un **inventario** que apila y equipa (con `optional`), y un **combate**
con azar reproducible.

### Antes de empezar

- Clases, `enum class`, `optional`, azar con semilla y algoritmos (ramas anteriores).

### Explicación

#### Pensar en piezas
Antes de escribir código, se listan las **responsabilidades**:
- **Personaje/combatiente**: vida (con sus límites), ataque, defensa; sabe recibir
  un golpe y curarse.
- **Inventario**: guarda objetos, apila los que se apilan, saca uno cuando se usa.
- **IA**: mira la situación y **decide** una acción; no la ejecuta.
- **Combate**: aplica las reglas (quién pega, cuánto, cuándo termina).

Cada pieza es una clase o una función chica, que se puede probar sola.

#### Separar decidir de hacer
La IA devuelve una **acción** (un `enum class Accion { Esperar, Acercarse, Atacar
}`), y otra parte del programa la aplica. Así, la IA se prueba sin combate ("a
distancia 1, ¿ataca?"), y el combate sin IA. Es la misma idea de las máquinas de
estado: según el estado y lo que ve, el enemigo pasa de "patrulla" a "persigue" a
"ataca".

#### El inventario con `optional`
Usar un objeto puede fallar (no lo tenés). `usar(nombre)` devuelve
`std::optional<Item>`: si hay, la copia del objeto usado; si no, vacío. Quien llama
decide qué hacer con cada tipo de objeto (beberlo, equiparlo).

#### Azar reproducible
El combate usa un **único** `std::mt19937` con semilla, pasado por referencia a
todos los que tiran dados. Con la misma semilla, el mismo combate: se puede
reproducir un error, probar un balance o grabar una partida.

#### Balancear
Los números (vida, ataque, defensa, cuánto cura una poción) se ponen en **un
lugar** (constantes o los constructores), así se ajustan sin buscar por todo el
código. Una regla habitual: el daño nunca es menor que 1 (`std::max(1, ...)`),
para que ninguna defensa haga invencible a nadie.

> **Si venís de C.** Es lo mismo que harías con structs y funciones, pero cada
> pieza protege sus reglas y el compilador te impide saltearlas.

### Código de ejemplo

```cpp
/*
 * Las piezas de un juego: un heroe con inventario, enemigos con una IA simple y combate.
 */
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <random>
#include <string>
#include <vector>

// --- Inventario: pociones que se apilan, armas que se equipan ---
enum class TipoItem { Pocion, Arma };

struct Item {
    std::string nombre;
    TipoItem tipo = TipoItem::Pocion;
    int valor = 0;          // pocion: cuanto cura; arma: cuanto ataque suma
    int cantidad = 1;
};

class Inventario {
public:
    void agregar(const Item& nuevo)
    {
        auto it = std::ranges::find(items_, nuevo.nombre, &Item::nombre);
        if (it != items_.end() && nuevo.tipo == TipoItem::Pocion) {
            it->cantidad += nuevo.cantidad;          // las pociones se apilan
        } else {
            items_.push_back(nuevo);
        }
    }

    // Saca UNA unidad y la devuelve; nada si no hay.
    std::optional<Item> usar(const std::string& nombre)
    {
        auto it = std::ranges::find(items_, nombre, &Item::nombre);
        if (it == items_.end()) {
            return std::nullopt;
        }
        Item usado = *it;
        if (--it->cantidad == 0) {
            items_.erase(it);
        }
        return usado;
    }

    void mostrar() const
    {
        std::cout << "  mochila:";
        for (const auto& i : items_) {
            std::cout << " " << i.nombre << (i.cantidad > 1 ? " x" + std::to_string(i.cantidad) : "");
        }
        std::cout << "\n";
    }

private:
    std::vector<Item> items_;
};

// --- Combatientes ---
class Combatiente {
public:
    Combatiente(const std::string& nombre, int vida, int ataque, int defensa)
        : nombre_(nombre), vida_(vida), vida_max_(vida), ataque_(ataque), defensa_(defensa) {}

    // El danio real: ataque del otro +- 2 al azar, menos la defensa, y al menos 1.
    int recibir_golpe(int ataque, std::mt19937& gen)
    {
        std::uniform_int_distribution<int> variacion(-2, 2);
        int dano = std::max(1, ataque + variacion(gen) - defensa_);
        vida_ = std::max(0, vida_ - dano);
        return dano;
    }

    void curar(int n) { vida_ = std::min(vida_max_, vida_ + n); }
    void sumar_ataque(int n) { ataque_ += n; }
    bool vivo() const { return vida_ > 0; }
    int ataque() const { return ataque_; }
    int vida() const { return vida_; }
    const std::string& nombre() const { return nombre_; }

private:
    std::string nombre_;
    int vida_;
    int vida_max_;
    int ataque_;
    int defensa_;
};

// --- Una IA minima: decide segun la distancia ---
enum class Accion { Esperar, Acercarse, Atacar };

Accion decidir(int distancia)
{
    if (distancia <= 1) {
        return Accion::Atacar;
    }
    return distancia <= 5 ? Accion::Acercarse : Accion::Esperar;
}

int main()
{
    std::mt19937 gen(12345);
    Combatiente lima("Lima", 60, 9, 2);
    Inventario mochila;
    mochila.agregar({"poción", TipoItem::Pocion, 20});
    mochila.agregar({"poción", TipoItem::Pocion, 20});
    mochila.agregar({"martillo", TipoItem::Arma, 4});
    mochila.mostrar();
    if (auto arma = mochila.usar("martillo")) {
        lima.sumar_ataque(arma->valor);
        std::cout << "  Lima equipa el " << arma->nombre << ": ataque " << lima.ataque() << "\n";
    }

    Combatiente orco("Orco", 40, 11, 1);
    int distancia = 7;
    for (int turno = 1; lima.vivo() && orco.vivo(); turno++) {
        std::cout << "Turno " << turno << " (distancia " << distancia << "): ";
        switch (decidir(distancia)) {
        case Accion::Esperar:
            std::cout << "el orco vigila";
            break;
        case Accion::Acercarse:
            distancia--;
            std::cout << "el orco se acerca";
            break;
        case Accion::Atacar:
            std::cout << "Lima pega " << orco.recibir_golpe(lima.ataque(), gen);
            if (orco.vivo()) {
                std::cout << ", el orco pega " << lima.recibir_golpe(orco.ataque(), gen);
            }
            break;
        }
        if (distancia > 1) {
            distancia--;                                     // Lima avanza hacia el orco
        }
        if (lima.vida() < 25 && mochila.usar("poción")) {
            lima.curar(20);
            std::cout << " | Lima bebe una poción";
        }
        std::cout << " | Lima " << lima.vida() << ", orco " << orco.vida() << "\n";
    }
    std::cout << (lima.vivo() ? "Gana Lima" : "Gana el orco") << "\n";
    mochila.mostrar();
    return 0;
}
```

### Salida esperada

```
  mochila: poción x2 martillo
  Lima equipa el martillo: ataque 13
Turno 1 (distancia 7): el orco vigila | Lima 60, orco 40
Turno 2 (distancia 6): el orco vigila | Lima 60, orco 40
Turno 3 (distancia 5): el orco se acerca | Lima 60, orco 40
Turno 4 (distancia 3): el orco se acerca | Lima 60, orco 40
Turno 5 (distancia 1): Lima pega 14, el orco pega 11 | Lima 49, orco 26
Turno 6 (distancia 1): Lima pega 11, el orco pega 7 | Lima 42, orco 15
Turno 7 (distancia 1): Lima pega 10, el orco pega 7 | Lima 35, orco 5
Turno 8 (distancia 1): Lima pega 11 | Lima 35, orco 0
Gana Lima
  mochila: poción x2
```

### ¿Para qué sirve?

Estas piezas están en todos los juegos: el inventario de un RPG, la IA de los guardias de un juego de sigilo, el combate por turnos de un juego de estrategia. Y la misma forma de pensar (piezas chicas con reglas propias, decidir separado de hacer) sirve fuera de los juegos: el carrito de una tienda es un inventario, un sistema de alertas es una IA que decide, un simulador de colas usa azar reproducible.

### Errores habituales

**Ogro: la IA que también mueve.** Si `decidir` además cambia la posición, ya no se
puede probar sola, y es fácil que el enemigo se mueva dos veces por turno.

**Ogro: el daño negativo.** Si la defensa supera al ataque, `ataque − defensa` da
negativo: el golpe **cura**. `std::max(1, ...)`.

**Ogro: el generador en cada golpe.** Crear `std::mt19937 gen(12345)` dentro de
`recibir_golpe` da siempre la misma variación. Uno solo, por referencia.

**Troll: guardar un puntero a un ítem del inventario.** Si el inventario hace
`erase` o `push_back`, el puntero queda inválido. Trabajá con copias (`optional<Item>`)
o volvé a buscar.

**Ogro: los números mágicos desparramados.** Un `20` en cinco lugares distintos:
cuando quieras cambiar cuánto cura una poción, vas a olvidarte de alguno.

### Misión R05-N04-M1 · Los guardias del puente

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

En un puente de 0 a 20 hay dos guardias: G1 en la posición 5 (ve a 3 casilleros) y
G2 en la 18 (ve a 5). Lima empieza en 0; cada letra de la entrada la mueve (`d`
derecha, `i` izquierda, otra cosa: se queda). Después de cada paso, cada guardia
actúa según la distancia a Lima: a 1 o menos **ataca**; dentro de su visión
**persigue** (un paso hacia ella); hasta 2 más allá de su visión queda en **alerta**
(no se mueve); más lejos, **patrulla** (va y viene de a un paso entre 0 y 20).
Mostrá cada turno con la posición y el estado de cada guardia.

#### Criterio de aprobación

- Los estados son un `enum class`.
- Cada guardia decide solo con su distancia a Lima.
- La patrulla cambia de sentido en los bordes.

#### Entrada de ejemplo

```
ddd.dddddddddd
```

#### Salida esperada

```
T1 Lima@1: G1@5 alerta G2@19 patrulla
T2 Lima@2: G1@4 persigue G2@20 patrulla
T3 Lima@3: G1@4 ataca G2@19 patrulla
T4 Lima@3: G1@4 ataca G2@18 patrulla
T5 Lima@4: G1@4 ataca G2@17 patrulla
T6 Lima@5: G1@4 ataca G2@16 patrulla
T7 Lima@6: G1@5 persigue G2@15 patrulla
T8 Lima@7: G1@6 persigue G2@14 patrulla
T9 Lima@8: G1@7 persigue G2@14 alerta
T10 Lima@9: G1@8 persigue G2@13 persigue
T11 Lima@10: G1@9 persigue G2@12 persigue
T12 Lima@11: G1@10 persigue G2@12 ataca
T13 Lima@12: G1@11 persigue G2@12 ataca
T14 Lima@13: G1@12 persigue G2@12 ataca
```

#### Solución de referencia

```cpp
// Mision 1 - Los guardias del puente: IA por distancia en una linea.
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

enum class Estado { Patrulla, Alerta, Persigue, Ataca };

std::string a_texto(Estado e)
{
    switch (e) {
    case Estado::Patrulla:
        return "patrulla";
    case Estado::Alerta:
        return "alerta";
    case Estado::Persigue:
        return "persigue";
    case Estado::Ataca:
        return "ataca";
    }
    return "?";
}

class Guardia {
public:
    Guardia(const std::string& nombre, int pos, int vision) : nombre_(nombre), pos_(pos), vision_(vision) {}

    void actuar(int lima)
    {
        int d = std::abs(lima - pos_);
        if (d <= 1) {
            estado_ = Estado::Ataca;
        } else if (d <= vision_) {
            estado_ = Estado::Persigue;
            pos_ += (lima > pos_) ? 1 : -1;
        } else if (d <= vision_ + 2) {
            estado_ = Estado::Alerta;             // la ve de lejos: no se mueve, pero avisa
        } else {
            estado_ = Estado::Patrulla;
            pos_ += paso_;                        // va y viene entre 0 y 20
            if (pos_ <= 0 || pos_ >= 20) {
                paso_ = -paso_;
            }
        }
    }

    std::string informe() const { return nombre_ + "@" + std::to_string(pos_) + " " + a_texto(estado_); }

private:
    std::string nombre_;
    int pos_;
    int vision_;
    int paso_ = 1;
    Estado estado_ = Estado::Patrulla;
};

int main()
{
    std::vector<Guardia> guardias = {{"G1", 5, 3}, {"G2", 18, 5}};
    int lima = 0;
    int turno = 1;
    char tecla = ' ';
    while (std::cin >> tecla) {
        lima += (tecla == 'd') - (tecla == 'i');
        std::cout << "T" << turno++ << " Lima@" << lima << ":";
        for (auto& g : guardias) {
            g.actuar(lima);
            std::cout << " " << g.informe();
        }
        std::cout << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Lima quieta
```entrada
.....
```
```salida
T1 Lima@0: G1@5 alerta G2@19 patrulla
T2 Lima@0: G1@5 alerta G2@20 patrulla
T3 Lima@0: G1@5 alerta G2@19 patrulla
T4 Lima@0: G1@5 alerta G2@18 patrulla
T5 Lima@0: G1@5 alerta G2@17 patrulla
```

##### Lima va y vuelve
```entrada
ddddiiii
```
```salida
T1 Lima@1: G1@5 alerta G2@19 patrulla
T2 Lima@2: G1@4 persigue G2@20 patrulla
T3 Lima@3: G1@4 ataca G2@19 patrulla
T4 Lima@4: G1@4 ataca G2@18 patrulla
T5 Lima@3: G1@4 ataca G2@17 patrulla
T6 Lima@2: G1@3 persigue G2@16 patrulla
T7 Lima@1: G1@2 persigue G2@15 patrulla
T8 Lima@0: G1@1 persigue G2@14 patrulla
```

##### Corre hasta el final
```entrada
dddddddddddddddddddd
```
```salida
T1 Lima@1: G1@5 alerta G2@19 patrulla
T2 Lima@2: G1@4 persigue G2@20 patrulla
T3 Lima@3: G1@4 ataca G2@19 patrulla
T4 Lima@4: G1@4 ataca G2@18 patrulla
T5 Lima@5: G1@4 ataca G2@17 patrulla
T6 Lima@6: G1@5 persigue G2@16 patrulla
T7 Lima@7: G1@6 persigue G2@15 patrulla
T8 Lima@8: G1@7 persigue G2@15 alerta
T9 Lima@9: G1@8 persigue G2@15 alerta
T10 Lima@10: G1@9 persigue G2@14 persigue
T11 Lima@11: G1@10 persigue G2@13 persigue
T12 Lima@12: G1@11 persigue G2@13 ataca
T13 Lima@13: G1@12 persigue G2@13 ataca
T14 Lima@14: G1@13 persigue G2@13 ataca
T15 Lima@15: G1@14 persigue G2@14 persigue
T16 Lima@16: G1@15 persigue G2@15 persigue
T17 Lima@17: G1@16 persigue G2@16 persigue
T18 Lima@18: G1@17 persigue G2@17 persigue
T19 Lima@19: G1@18 persigue G2@18 persigue
T20 Lima@20: G1@19 persigue G2@19 persigue
```

### Misión R05-N04-M2 · La mochila del explorador

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Una mochila de **4 lugares** (las pociones del mismo nombre se apilan en un lugar).
Órdenes: `juntar nombre` (si empieza con "pocion" es una poción que cura 15; si
empieza con "llave", una llave; si no, un arma cuyo bonus es el largo del nombre) y
`usar nombre`: la poción cura (máximo 60), el arma se **equipa** (la que estaba
equipada vuelve a la mochila) y la llave "se usa en una puerta". `sacar` devuelve
`std::optional<Item>`. Después de cada orden, mostrá la mochila; al final, vida y
ataque (base 5 + bonus del arma equipada).

#### Criterio de aprobación

- `sacar` devuelve `optional` y quien llama decide según el tipo.
- Las pociones se apilan y la mochila respeta sus 4 lugares.
- El arma anterior vuelve a la mochila al equipar otra.

#### Entrada de ejemplo

```
juntar pocion
juntar daga
juntar pocion
juntar llave
juntar hacha
usar daga
usar pocion
juntar mandoble
usar mandoble
usar escudo
usar llave
```

#### Salida esperada

```
Junta pocion
  [pocion x1]
Junta daga
  [pocion x1, daga x1]
Junta pocion
  [pocion x2, daga x1]
Junta llave
  [pocion x2, daga x1, llave x1]
Junta hacha
  [pocion x2, daga x1, llave x1, hacha x1]
Equipa daga: ataque 9
  [pocion x2, llave x1, hacha x1]
Bebe pocion: vida 60
  [pocion x1, llave x1, hacha x1]
Junta mandoble
  [pocion x1, llave x1, hacha x1, mandoble x1]
Equipa mandoble: ataque 13
  [pocion x1, llave x1, hacha x1, daga x1]
No tiene escudo
  [pocion x1, llave x1, hacha x1, daga x1]
Usa llave en una puerta
  [pocion x1, hacha x1, daga x1]
Final: vida 60, ataque 13
```

#### Solución de referencia

```cpp
// Mision 2 - La mochila del explorador: apilar, usar y equipar con optional.
#include <algorithm>
#include <iostream>
#include <optional>
#include <string>
#include <vector>

enum class Tipo { Pocion, Arma, Llave };

struct Item {
    std::string nombre;
    Tipo tipo;
    int valor = 0;
    int cantidad = 1;
};

class Mochila {
public:
    bool agregar(const Item& nuevo)
    {
        auto it = std::ranges::find(items_, nuevo.nombre, &Item::nombre);
        if (it != items_.end() && nuevo.tipo == Tipo::Pocion) {
            it->cantidad += nuevo.cantidad;
            return true;
        }
        if (items_.size() >= 4) {
            return false;                          // 4 lugares como mucho
        }
        items_.push_back(nuevo);
        return true;
    }

    std::optional<Item> sacar(const std::string& nombre)
    {
        auto it = std::ranges::find(items_, nombre, &Item::nombre);
        if (it == items_.end()) {
            return std::nullopt;
        }
        Item copia = *it;
        copia.cantidad = 1;
        if (--it->cantidad == 0) {
            items_.erase(it);
        }
        return copia;
    }

    void mostrar() const
    {
        std::cout << "  [";
        for (std::size_t i = 0; i < items_.size(); i++) {
            std::cout << (i ? ", " : "") << items_[i].nombre << " x" << items_[i].cantidad;
        }
        std::cout << "]\n";
    }

private:
    std::vector<Item> items_;
};

int main()
{
    Mochila m;
    int vida = 50, ataque = 5;
    std::optional<Item> arma;
    std::string orden, nombre;
    while (std::cin >> orden >> nombre) {
        if (orden == "juntar") {
            Tipo t = nombre.starts_with("pocion") ? Tipo::Pocion : nombre.starts_with("llave") ? Tipo::Llave : Tipo::Arma;
            int valor = t == Tipo::Pocion ? 15 : (t == Tipo::Arma ? static_cast<int>(nombre.size()) : 0);
            std::cout << (m.agregar({nombre, t, valor}) ? "Junta " : "No entra ") << nombre << "\n";
        } else if (orden == "usar") {
            auto it = m.sacar(nombre);
            if (!it) {
                std::cout << "No tiene " << nombre << "\n";
            } else if (it->tipo == Tipo::Pocion) {
                vida = std::min(60, vida + it->valor);
                std::cout << "Bebe " << nombre << ": vida " << vida << "\n";
            } else if (it->tipo == Tipo::Arma) {
                if (arma) {
                    m.agregar(*arma);                  // el arma anterior vuelve a la mochila
                }
                arma = it;
                std::cout << "Equipa " << nombre << ": ataque " << ataque + arma->valor << "\n";
            } else {
                std::cout << "Usa " << nombre << " en una puerta\n";
            }
        }
        m.mostrar();
    }
    std::cout << "Final: vida " << vida << ", ataque " << ataque + (arma ? arma->valor : 0) << "\n";
    return 0;
}
```

#### Pruebas

##### Mochila llena
```entrada
juntar a
juntar b
juntar c
juntar d
juntar e
```
```salida
Junta a
  [a x1]
Junta b
  [a x1, b x1]
Junta c
  [a x1, b x1, c x1]
Junta d
  [a x1, b x1, c x1, d x1]
No entra e
  [a x1, b x1, c x1, d x1]
Final: vida 50, ataque 5
```

##### Usar lo que no hay
```entrada
usar pocion
usar llave
```
```salida
No tiene pocion
  []
No tiene llave
  []
Final: vida 50, ataque 5
```

##### Muchas pociones
```entrada
juntar pocion
juntar pocion
juntar pocion
usar pocion
usar pocion
usar pocion
usar pocion
```
```salida
Junta pocion
  [pocion x1]
Junta pocion
  [pocion x2]
Junta pocion
  [pocion x3]
Bebe pocion: vida 60
  [pocion x2]
Bebe pocion: vida 60
  [pocion x1]
Bebe pocion: vida 60
  []
No tiene pocion
  []
Final: vida 60, ataque 5
```

### Misión R05-N04-M3 · El torneo de la Arena

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cuatro luchadores (Lima 60/12/3, Bron 80/9/5, Lyn 50/14/2 y Oto 70/10/4: vida,
ataque, defensa) juegan un torneo por eliminación: 1 contra 2 y 3 contra 4, y los
ganadores la final. Cada golpe hace `ataque ± 2` (al azar) menos la defensa del
otro, y al menos 1. Entre rondas, el ganador recupera su vida original. Leé la
semilla de la entrada y mostrá cada pelea (rondas y vida que le queda al ganador) y
el campeón.

#### Criterio de aprobación

- Un único generador con la semilla leída, pasado por referencia.
- El daño nunca es menor que 1.

#### Entrada de ejemplo

```
2026
```

#### Salida esperada

```
Ronda 1:
  Lima vs Bron: gana Bron en 10 rondas (le queda 8)
  Lyn vs Oto: gana Oto en 6 rondas (le queda 13)
Ronda 2:
  Bron vs Oto: gana Bron en 15 rondas (le queda 15)
Campeón: Bron
```

#### Solución de referencia

```cpp
// Mision 3 - El torneo de la Arena: combates con semilla, defensa y variacion.
#include <algorithm>
#include <iostream>
#include <random>
#include <string>
#include <vector>

struct Luchador {
    std::string nombre;
    int vida;
    int ataque;
    int defensa;
};

int golpe(const Luchador& atacante, Luchador& defensor, std::mt19937& gen)
{
    std::uniform_int_distribution<int> variacion(-2, 2);
    int dano = std::max(1, atacante.ataque + variacion(gen) - defensor.defensa);
    defensor.vida = std::max(0, defensor.vida - dano);
    return dano;
}

// Pelea hasta que uno cae; devuelve el ganador (una copia con la vida que le quedo).
Luchador pelear(Luchador a, Luchador b, std::mt19937& gen)
{
    int rondas = 0;
    while (a.vida > 0 && b.vida > 0) {
        golpe(a, b, gen);
        if (b.vida > 0) {
            golpe(b, a, gen);
        }
        rondas++;
    }
    Luchador ganador = a.vida > 0 ? a : b;
    std::cout << "  " << a.nombre << " vs " << b.nombre << ": gana " << ganador.nombre << " en " << rondas
              << " rondas (le queda " << ganador.vida << ")\n";
    return ganador;
}

int main()
{
    unsigned semilla = 0;
    std::cin >> semilla;
    std::mt19937 gen(semilla);
    std::vector<Luchador> base = {{"Lima", 60, 12, 3}, {"Bron", 80, 9, 5}, {"Lyn", 50, 14, 2}, {"Oto", 70, 10, 4}};
    std::vector<Luchador> ronda = base;
    int numero = 1;
    while (ronda.size() > 1) {
        std::cout << "Ronda " << numero++ << ":\n";
        std::vector<Luchador> siguiente;
        for (std::size_t i = 0; i + 1 < ronda.size(); i += 2) {
            Luchador g = pelear(ronda[i], ronda[i + 1], gen);
            auto original = std::ranges::find(base, g.nombre, &Luchador::nombre);
            g.vida = original->vida;                     // entre rondas se recupera
            siguiente.push_back(g);
        }
        ronda = siguiente;
    }
    std::cout << "Campeón: " << ronda[0].nombre << "\n";
    return 0;
}
```

#### Pruebas

##### Semilla 1
```entrada
1
```
```salida
Ronda 1:
  Lima vs Bron: gana Bron en 10 rondas (le queda 20)
  Lyn vs Oto: gana Lyn en 7 rondas (le queda 2)
Ronda 2:
  Bron vs Lyn: gana Bron en 7 rondas (le queda 27)
Campeón: Bron
```

##### Semilla 777
```entrada
777
```
```salida
Ronda 1:
  Lima vs Bron: gana Bron en 10 rondas (le queda 9)
  Lyn vs Oto: gana Oto en 7 rondas (le queda 1)
Ronda 2:
  Bron vs Oto: gana Bron en 16 rondas (le queda 7)
Campeón: Bron
```

### Encargo R05-N04-E1 · La máquina expendedora

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una expendedora tiene agua (A1, $800, 2 unidades), gaseosa (A2, $1200, 1) y alfajor
(B1, $900, 3). Estados: esperando, con crédito y sin stock (fuera de servicio).
Órdenes: `moneda valor`, `elegir codigo` y `cancelar` (devuelve el crédito). Al
vender, da el vuelto y vuelve a "esperando" (o a "sin stock" si no queda nada). En
"sin stock" devuelve las monedas. Mostrá la respuesta a cada orden.

#### Criterio de aprobación

- Los estados son un `enum class` y cada orden se maneja según el estado.
- Da el vuelto y controla el stock.

#### Entrada de ejemplo

```
elegir A1
moneda 500
elegir A1
moneda 500
elegir A1
moneda 2000
elegir A2
elegir A2
moneda 100
cancelar
```

#### Salida esperada

```
Primero poné plata
Crédito: $500
Faltan $300
Crédito: $1000
Sale agua, vuelto $200
Crédito: $2000
Sale gaseosa, vuelto $800
Primero poné plata
Crédito: $100
Devuelve $100
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La maquina expendedora: estados, stock y vuelto.
#include <iostream>
#include <map>
#include <string>

enum class Estado { Esperando, ConCredito, SinStock };

struct Producto {
    std::string nombre;
    int precio;
    int stock;
};

class Expendedora {
public:
    Expendedora()
    {
        productos_["A1"] = {"agua", 800, 2};
        productos_["A2"] = {"gaseosa", 1200, 1};
        productos_["B1"] = {"alfajor", 900, 3};
    }

    void moneda(int valor)
    {
        if (estado_ == Estado::SinStock) {
            std::cout << "Fuera de servicio: devuelve $" << valor << "\n";
            return;
        }
        credito_ += valor;
        estado_ = Estado::ConCredito;
        std::cout << "Crédito: $" << credito_ << "\n";
    }

    void elegir(const std::string& codigo)
    {
        auto it = productos_.find(codigo);
        if (estado_ != Estado::ConCredito) {
            std::cout << "Primero poné plata\n";
        } else if (it == productos_.end()) {
            std::cout << "No existe " << codigo << "\n";
        } else if (it->second.stock == 0) {
            std::cout << it->second.nombre << " agotado\n";
        } else if (credito_ < it->second.precio) {
            std::cout << "Faltan $" << it->second.precio - credito_ << "\n";
        } else {
            it->second.stock--;
            credito_ -= it->second.precio;
            std::cout << "Sale " << it->second.nombre << (credito_ > 0 ? ", vuelto $" + std::to_string(credito_) : "") << "\n";
            credito_ = 0;
            estado_ = hay_stock() ? Estado::Esperando : Estado::SinStock;
        }
    }

    void cancelar()
    {
        if (credito_ > 0) {
            std::cout << "Devuelve $" << credito_ << "\n";
        }
        credito_ = 0;
        if (estado_ == Estado::ConCredito) {
            estado_ = Estado::Esperando;
        }
    }

private:
    bool hay_stock() const
    {
        for (const auto& [codigo, p] : productos_) {
            if (p.stock > 0) {
                return true;
            }
        }
        return false;
    }

    std::map<std::string, Producto> productos_;
    Estado estado_ = Estado::Esperando;
    int credito_ = 0;
};

int main()
{
    Expendedora m;
    std::string orden;
    while (std::cin >> orden) {
        if (orden == "moneda") {
            int v = 0;
            std::cin >> v;
            m.moneda(v);
        } else if (orden == "elegir") {
            std::string c;
            std::cin >> c;
            m.elegir(c);
        } else if (orden == "cancelar") {
            m.cancelar();
        }
    }
    return 0;
}
```

#### Pruebas

##### Agota el stock
```entrada
moneda 5000
elegir A2
moneda 5000
elegir A2
cancelar
```
```salida
Crédito: $5000
Sale gaseosa, vuelto $3800
Crédito: $5000
gaseosa agotado
Devuelve $5000
```

##### Código que no existe
```entrada
moneda 1000
elegir Z9
cancelar
cancelar
```
```salida
Crédito: $1000
No existe Z9
Devuelve $1000
```

##### Vende todo y queda fuera de servicio
```entrada
moneda 800
elegir A1
moneda 800
elegir A1
moneda 1200
elegir A2
moneda 900
elegir B1
moneda 900
elegir B1
moneda 900
elegir B1
moneda 100
```
```salida
Crédito: $800
Sale agua
Crédito: $800
Sale agua
Crédito: $1200
Sale gaseosa
Crédito: $900
Sale alfajor
Crédito: $900
Sale alfajor
Crédito: $900
Sale alfajor
Fuera de servicio: devuelve $100
```

### Prueba del sello

#### ¿Por qué conviene que la IA devuelva una acción en vez de ejecutarla?

Porque así la decisión se prueba sola y el que ejecuta controla el orden de los turnos.

#### ¿Qué ventaja tiene que `usar` devuelva `optional<Item>`?

Que quien llama sabe si había el objeto y recibe una copia para decidir qué hacer según su tipo.

#### ¿Por qué el daño se calcula con `std::max(1, ...)`?

Para que nunca sea cero o negativo (un golpe no puede curar).

#### ¿Qué pasa si cada combatiente crea su propio generador con la misma semilla?

Todos tiran los mismos números: el azar deja de parecer azar.

### Soluciones (docente)

Material original: `05-C++-Videojuegos/01-Player` a `04-Inventory`, integrados en un nodo. La expendedora (Encargo) lleva la misma idea fuera del juego.

## R05-N05 · Estados y el bucle de juego

```meta
tipo: tema
padre: R05-N04
precio: 10
criatura: ogro
temas: juegos.bucle, juegos.estados
usa: diseno.maquina-estados
```

### Crónica

En el centro del Taller gira el **Gran Péndulo**. Con cada vaivén, todos los autómatas de la sala hacen tres cosas: miran si alguien les dio una orden, se mueven un poquito, y encienden sus luces. Vaivén tras vaivén.

Bron frena el péndulo para ver qué pasa: todos los autómatas se quedan congelados con un pie en el aire. Uno, el de Oto, con la batidora encendida.

—Eso es un juego por dentro —dice {mentor}—. Un **bucle** que se repite muchas veces por segundo: escuchar, actualizar, dibujar. Y según el momento (menú, jugando, pausa), la misma tecla hace cosas distintas.

### Objetivos

Organizar un programa interactivo como un **bucle de juego** (entrada →
actualizar → dibujar), manejar sus **estados** (menú, jugando, pausa, fin) con una
máquina de estados, y mover las cosas con **delta time** (`dt`) para que la
velocidad no dependa de la compu.

### Antes de empezar

- `enum class` y máquinas de estado (rama 3).
- Las piezas de un juego (nodo anterior).

### Explicación

#### El bucle de juego
Todo juego (y muchos programas interactivos) tiene esta forma:
```cpp
while (corriendo) {
    procesar_entrada();   // ¿qué pidió el jugador?
    actualizar(dt);       // mover todo, IA, colisiones, reglas
    dibujar();            // mostrar el estado actual
}
```
Cada vuelta es un **cuadro** (*frame*). Las tres partes están **separadas**: la
entrada solo registra qué se quiere, `actualizar` cambia el mundo y `dibujar` solo
muestra (no cambia nada). Gracias a eso, pasar de la consola a una ventana (la
Senda de SDL3) es cambiar la entrada y el dibujo: la lógica queda igual.

#### Los estados del juego
La misma tecla significa cosas distintas según el momento: `p` pausa mientras se
juega y reanuda en la pausa; en el menú no hace nada. Se modela con un
`enum class Estado { Menu, Jugando, Pausa, Fin }` y un `switch` en la entrada (y a
veces en el dibujo). En pausa, `actualizar` no hace nada: el mundo se congela.

#### Delta time: moverse por segundo, no por cuadro
```cpp
x += velocidad;          // MAL: 1 por cuadro. A 144 cuadros por segundo va más rápido que a 30
x += velocidad * dt;     // BIEN: velocidad por SEGUNDO, dt = segundos desde el cuadro anterior
```
`dt` (*delta time*) es cuánto tiempo pasó desde el cuadro anterior. Multiplicando
por `dt`, el movimiento es igual en cualquier compu. Con gravedad, la velocidad
también cambia con el tiempo: `vy += gravedad * dt; y += vy * dt;`.

En un juego de verdad, `dt` se mide con `std::chrono::steady_clock`. En este curso
usamos un **dt fijo** (por ejemplo, 0.1 s) para que el resultado sea siempre el
mismo y se pueda comparar. Los motores de física también usan un paso fijo, por el
mismo motivo.

#### Turnos o tiempo real
- **Por turnos** (un roguelike, un juego de mesa): cada tecla es un "tick", y el
  mundo avanza un turno. No hace falta `dt`.
- **En tiempo real** (un plataformas, un shooter): el mundo avanza aunque no
  toques nada; se usa `dt`.

El jefe final es por turnos; la Senda de SDL3, en tiempo real.

> **Si venís de C.** El bucle y el `dt` son iguales en C. Lo que cambia es que
> las partes se organizan en clases y los estados son `enum class`.

### Código de ejemplo

```cpp
/*
 * Estados del juego y el bucle: entrada -> actualizar(dt) -> dibujar.
 * Aca el dt es FIJO (0.1 s) para que el resultado sea siempre el mismo.
 */
#include <cmath>
#include <iostream>
#include <string>

enum class Estado { Menu, Jugando, Pausa, Fin };

struct Mundo {
    Estado estado = Estado::Menu;
    double x = 0;           // posicion de Lima (en casilleros)
    double velocidad = 0;   // casilleros por SEGUNDO
    double meta = 12;
    int cuadro = 0;
};

// 1) Entrada: solo decide que quiere el jugador.
void procesar_entrada(Mundo& m, char tecla)
{
    switch (m.estado) {
    case Estado::Menu:
        if (tecla == 'j') {
            m.estado = Estado::Jugando;
        }
        break;
    case Estado::Jugando:
        if (tecla == 'p') {
            m.estado = Estado::Pausa;
        } else if (tecla == 'd') {
            m.velocidad = 8;           // corre
        } else if (tecla == '.') {
            m.velocidad = 0;           // se detiene
        }
        break;
    case Estado::Pausa:
        if (tecla == 'p') {
            m.estado = Estado::Jugando;
        }
        break;
    case Estado::Fin:
        break;
    }
}

// 2) Actualizar: mueve el mundo segun el tiempo que paso (dt).
void actualizar(Mundo& m, double dt)
{
    if (m.estado != Estado::Jugando) {
        return;                                    // en pausa, el mundo no avanza
    }
    m.x += m.velocidad * dt;                       // velocidad * tiempo: igual en cualquier compu
    if (m.x >= m.meta) {
        m.x = m.meta;
        m.estado = Estado::Fin;
    }
}

// 3) Dibujar: solo muestra, no cambia nada.
void dibujar(const Mundo& m)
{
    const char* nombres[] = {"MENÚ", "JUGANDO", "PAUSA", "FIN"};
    std::string pista(13, '.');
    pista[static_cast<std::size_t>(m.meta)] = 'X';
    pista[static_cast<std::size_t>(std::floor(m.x))] = '@';
    std::cout << "cuadro " << m.cuadro << " " << pista << " " << nombres[static_cast<int>(m.estado)] << "\n";
}

int main()
{
    Mundo m;
    const double DT = 0.1;                           // 10 cuadros por segundo
    std::string entradas = "-j-d--p---p------";      // una tecla por cuadro ('-' = nada)
    for (char tecla : entradas) {
        procesar_entrada(m, tecla);
        actualizar(m, DT);
        dibujar(m);
        m.cuadro++;
        if (m.estado == Estado::Fin) {
            break;
        }
    }
    std::cout << "Llegó en " << m.cuadro * DT << " segundos de juego\n";
    return 0;
}
```

### Salida esperada

```
cuadro 0 @...........X MENÚ
cuadro 1 @...........X JUGANDO
cuadro 2 @...........X JUGANDO
cuadro 3 @...........X JUGANDO
cuadro 4 .@..........X JUGANDO
cuadro 5 ..@.........X JUGANDO
cuadro 6 ..@.........X PAUSA
cuadro 7 ..@.........X PAUSA
cuadro 8 ..@.........X PAUSA
cuadro 9 ..@.........X PAUSA
cuadro 10 ...@........X JUGANDO
cuadro 11 ....@.......X JUGANDO
cuadro 12 ....@.......X JUGANDO
cuadro 13 .....@......X JUGANDO
cuadro 14 ......@.....X JUGANDO
cuadro 15 .......@....X JUGANDO
cuadro 16 .......@....X JUGANDO
Llegó en 1.7 segundos de juego
```

### ¿Para qué sirve?

El bucle "entrada, actualizar, dibujar" es el corazón de todos los motores de juegos, pero también de las simulaciones (tráfico, física, epidemias), de los programas de control de máquinas y robots (leer sensores, decidir, actuar) y de las interfaces gráficas por dentro. Las máquinas de estados con tiempo controlan semáforos, ascensores, lavarropas y cualquier aparato con modos.

### Errores habituales

**Ogro: mover por cuadro.** `x += 5;` sin `dt`: el juego va el doble de rápido en
una compu el doble de rápida.

**Ogro: dibujar que cambia cosas.** Si `dibujar` mueve algo, al pausar el dibujo
el mundo "se acelera" o se congela mal. `dibujar` recibe `const Mundo&`.

**Ogro: actualizar en pausa.** Si `actualizar` no revisa el estado, los enemigos
siguen moviéndose con el juego pausado.

**Ogro: la tecla que hace dos cosas.** Sin máquina de estados, `p` pausa y reanuda
en el mismo cuadro, y parece que no hace nada.

**Goblin: comparar `double` con `==` para llegar a una meta.** `if (x == meta)`
casi nunca se cumple con decimales: `x` salta de 11.9 a 12.7. Usá `>=`.

**Ogro: un `dt` enorme.** Si la compu se traba un segundo, `dt` vale 1 y los
objetos atraviesan paredes. Los juegos limitan `dt` (por ejemplo, a 0.1).

### Misión R05-N05-M1 · Las pantallas del juego

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Modelá las pantallas de un juego: **Título** (cualquier evento pasa al Menú),
**Menú** (`jugar` empieza una partida con 0 puntos y 3 vidas), **Jugando**
(`moneda` suma 10, `golpe` resta una vida y con 0 vidas pasa a Game Over guardando
el récord, `pausa` pausa), **Pausa** (`pausa` vuelve, `salir` va al menú) y **Game
Over** (`ok` vuelve al menú). Cada palabra de la entrada es un evento: mostrá la
pantalla antes, la nueva (si cambió) y, jugando, los puntos y las vidas. Al final,
el récord.

#### Criterio de aprobación

- Un `enum class` para las pantallas y un `switch` por estado.
- Los eventos que no corresponden a la pantalla actual no hacen nada.

#### Entrada de ejemplo

```
empezar jugar moneda moneda pausa moneda pausa golpe moneda golpe golpe jugar ok jugar moneda salir
```

#### Salida esperada

```
empezar: Título -> Menú
jugar: Menú -> Jugando (0 pts, 3 vidas)
moneda: Jugando (10 pts, 3 vidas)
moneda: Jugando (20 pts, 3 vidas)
pausa: Jugando -> Pausa
moneda: Pausa
pausa: Pausa -> Jugando (20 pts, 3 vidas)
golpe: Jugando (20 pts, 2 vidas)
moneda: Jugando (30 pts, 2 vidas)
golpe: Jugando (30 pts, 1 vidas)
golpe: Jugando -> Game Over
jugar: Game Over
ok: Game Over -> Menú
jugar: Menú -> Jugando (0 pts, 3 vidas)
moneda: Jugando (10 pts, 3 vidas)
salir: Jugando (10 pts, 3 vidas)
Récord: 30
```

#### Solución de referencia

```cpp
// Mision 1 - Las pantallas del juego: una maquina de estados completa.
#include <algorithm>
#include <iostream>
#include <string>

enum class Pantalla { Titulo, Menu, Jugando, Pausa, GameOver };

std::string nombre(Pantalla p)
{
    switch (p) {
    case Pantalla::Titulo:
        return "Título";
    case Pantalla::Menu:
        return "Menú";
    case Pantalla::Jugando:
        return "Jugando";
    case Pantalla::Pausa:
        return "Pausa";
    case Pantalla::GameOver:
        return "Game Over";
    }
    return "?";
}

struct Partida {
    Pantalla pantalla = Pantalla::Titulo;
    int puntos = 0;
    int vidas = 3;
    int record = 0;
};

void evento(Partida& p, const std::string& e)
{
    switch (p.pantalla) {
    case Pantalla::Titulo:
        p.pantalla = Pantalla::Menu;             // cualquier tecla
        break;
    case Pantalla::Menu:
        if (e == "jugar") {
            p.pantalla = Pantalla::Jugando;
            p.puntos = 0;
            p.vidas = 3;
        }
        break;
    case Pantalla::Jugando:
        if (e == "moneda") {
            p.puntos += 10;
        } else if (e == "golpe" && --p.vidas == 0) {
            p.record = std::max(p.record, p.puntos);
            p.pantalla = Pantalla::GameOver;
        } else if (e == "pausa") {
            p.pantalla = Pantalla::Pausa;
        }
        break;
    case Pantalla::Pausa:
        if (e == "pausa") {
            p.pantalla = Pantalla::Jugando;
        } else if (e == "salir") {
            p.pantalla = Pantalla::Menu;
        }
        break;
    case Pantalla::GameOver:
        if (e == "ok") {
            p.pantalla = Pantalla::Menu;
        }
        break;
    }
}

int main()
{
    Partida p;
    std::string e;
    while (std::cin >> e) {
        Pantalla antes = p.pantalla;
        evento(p, e);
        std::cout << e << ": " << nombre(antes);
        if (p.pantalla != antes) {
            std::cout << " -> " << nombre(p.pantalla);
        }
        if (p.pantalla == Pantalla::Jugando) {
            std::cout << " (" << p.puntos << " pts, " << p.vidas << " vidas)";
        }
        std::cout << "\n";
    }
    std::cout << "Récord: " << p.record << "\n";
    return 0;
}
```

#### Pruebas

##### Pierde enseguida
```entrada
empezar jugar golpe golpe golpe ok
```
```salida
empezar: Título -> Menú
jugar: Menú -> Jugando (0 pts, 3 vidas)
golpe: Jugando (0 pts, 2 vidas)
golpe: Jugando (0 pts, 1 vidas)
golpe: Jugando -> Game Over
ok: Game Over -> Menú
Récord: 0
```

##### Récord que mejora
```entrada
x jugar moneda golpe golpe golpe ok jugar moneda moneda moneda golpe golpe golpe
```
```salida
x: Título -> Menú
jugar: Menú -> Jugando (0 pts, 3 vidas)
moneda: Jugando (10 pts, 3 vidas)
golpe: Jugando (10 pts, 2 vidas)
golpe: Jugando (10 pts, 1 vidas)
golpe: Jugando -> Game Over
ok: Game Over -> Menú
jugar: Menú -> Jugando (0 pts, 3 vidas)
moneda: Jugando (10 pts, 3 vidas)
moneda: Jugando (20 pts, 3 vidas)
moneda: Jugando (30 pts, 3 vidas)
golpe: Jugando (30 pts, 2 vidas)
golpe: Jugando (30 pts, 1 vidas)
golpe: Jugando -> Game Over
Récord: 30
```

##### Sin eventos
```entrada
```
```salida
Récord: 0
```

### Misión R05-N05-M2 · El salto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Lima salta con una velocidad inicial de 6 m/s hacia arriba, y la gravedad es de
−20 m/s². En cada cuadro: `vy += gravedad * dt`, `y += vy * dt`, y si `y` llega a 0,
aterriza. Leé el `dt` de la entrada y simulá el salto cuadro a cuadro. Mostrá el
tiempo y la altura cada 5 cuadros (y al aterrizar), la altura máxima y cuántos
cuadros duró. Probá después con `dt = 0.01` y `dt = 0.1`: ¿cambia mucho?

#### Criterio de aprobación

- La posición y la velocidad se actualizan con `dt`.
- El aterrizaje deja la altura en 0 exacto.
- Con distintos `dt` el salto dura casi lo mismo en segundos.

#### Entrada de ejemplo

```
0.02
```

#### Salida esperada

```
t=0.10s altura 0.48
t=0.20s altura 0.76
t=0.30s altura 0.84
t=0.40s altura 0.72
t=0.50s altura 0.40
t=0.58s altura 0.00
Altura máxima: 0.84 m, 29 cuadros
```

#### Solución de referencia

```cpp
// Mision 2 - El salto: gravedad con dt fijo, cuadro por cuadro.
#include <algorithm>
#include <iomanip>
#include <iostream>

struct Cuerpo {
    double y = 0;            // altura (metros)
    double vy = 0;           // velocidad vertical (m/s)
    bool en_el_piso = true;
};

void saltar(Cuerpo& c)
{
    if (c.en_el_piso) {
        c.vy = 6;
        c.en_el_piso = false;
    }
}

void actualizar(Cuerpo& c, double dt)
{
    const double GRAVEDAD = -20;         // m/s por segundo
    if (c.en_el_piso) {
        return;
    }
    c.vy += GRAVEDAD * dt;               // la gravedad cambia la velocidad
    c.y += c.vy * dt;                    // la velocidad cambia la posicion
    if (c.y <= 0) {
        c.y = 0;
        c.vy = 0;
        c.en_el_piso = true;
    }
}

int main()
{
    double dt = 0;
    std::cin >> dt;
    Cuerpo lima;
    double maxima = 0;
    int cuadros = 0;
    std::cout << std::fixed << std::setprecision(2);
    saltar(lima);
    while (!lima.en_el_piso || cuadros == 0) {
        actualizar(lima, dt);
        cuadros++;
        maxima = std::max(maxima, lima.y);
        if (cuadros % 5 == 0 || lima.en_el_piso) {
            std::cout << "t=" << cuadros * dt << "s altura " << lima.y << "\n";
        }
    }
    std::cout << "Altura máxima: " << maxima << " m, " << cuadros << " cuadros\n";
    return 0;
}
```

#### Pruebas

##### Paso fino
```entrada
0.01
```
```salida
t=0.05s altura 0.27
t=0.10s altura 0.49
t=0.15s altura 0.66
t=0.20s altura 0.78
t=0.25s altura 0.85
t=0.30s altura 0.87
t=0.35s altura 0.84
t=0.40s altura 0.76
t=0.45s altura 0.63
t=0.50s altura 0.45
t=0.55s altura 0.22
t=0.59s altura 0.00
Altura máxima: 0.87 m, 59 cuadros
```

##### Paso grueso
```entrada
0.1
```
```salida
t=0.50s altura 0.00
t=0.60s altura 0.00
Altura máxima: 0.60 m, 6 cuadros
```

### Misión R05-N05-M3 · Esquivar rocas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

En una pantalla de 7 × 6, Lima está en la fila de abajo y caen rocas. Escribí
`struct Mundo` y tres funciones: `entrada(m, tecla)` (`i`/`d` mueve a Lima),
`actualizar(m, cuadro)` (las rocas bajan una fila; si una llega a la fila de Lima
en su columna, pierde; las que salen de la pantalla cuentan como esquivadas; cada 2
cuadros aparece una roca arriba en la columna `(cuadro * 5 + 1) % 7`) y
`dibujar(m, cuadro)` (con `const Mundo&`). Dibujá cada 3 cuadros o cuando Lima
pierde. La entrada es una palabra con una tecla por cuadro.

#### Criterio de aprobación

- Las tres funciones están separadas y `dibujar` no cambia el mundo.
- Las rocas que salen se borran con `erase_if`.

#### Entrada de ejemplo

```
d.i..dd..ii.d...
```

#### Salida esperada

```
cuadro 0:
  .o.....
  .......
  .......
  .......
  .......
  ....@..
cuadro 3:
  .......
  ....o..
  .......
  .o.....
  .......
  ...@...
cuadro 6:
  ...o...
  .......
  o......
  .......
  ....o..
  .....@.
cuadro 9:
  .......
  ......o
  .......
  ...o...
  .......
  o...@..
cuadro 11:
  .......
  ..o....
  .......
  ......o
  .......
  ...X...
¡Una roca alcanzó a Lima!; rocas esquivadas: 3
```

#### Solución de referencia

```cpp
// Mision 3 - Esquivar rocas: entrada, actualizar y dibujar sobre un Mundo.
#include <iostream>
#include <string>
#include <vector>

struct Roca {
    int x;
    int y;
};

struct Mundo {
    int ancho = 7;
    int alto = 6;
    int lima = 3;                  // columna de Lima (en la fila de abajo)
    std::vector<Roca> rocas;
    int esquivadas = 0;
    bool viva = true;
};

void entrada(Mundo& m, char tecla)
{
    if (tecla == 'i' && m.lima > 0) {
        m.lima--;
    } else if (tecla == 'd' && m.lima < m.ancho - 1) {
        m.lima++;
    }
}

void actualizar(Mundo& m, int cuadro)
{
    for (auto& r : m.rocas) {
        r.y++;
    }
    for (const auto& r : m.rocas) {
        if (r.y == m.alto - 1 && r.x == m.lima) {
            m.viva = false;
        }
    }
    auto antes = m.rocas.size();
    std::erase_if(m.rocas, [&m](const Roca& r) { return r.y >= m.alto; });
    m.esquivadas += static_cast<int>(antes - m.rocas.size());
    if (cuadro % 2 == 0) {
        m.rocas.push_back({(cuadro * 5 + 1) % m.ancho, 0});     // aparece una roca "al azar" pero predecible
    }
}

void dibujar(const Mundo& m, int cuadro)
{
    std::vector<std::string> pantalla(m.alto, std::string(m.ancho, '.'));
    for (const auto& r : m.rocas) {
        pantalla[r.y][r.x] = 'o';
    }
    pantalla[m.alto - 1][m.lima] = m.viva ? '@' : 'X';
    std::cout << "cuadro " << cuadro << ":\n";
    for (const auto& fila : pantalla) {
        std::cout << "  " << fila << "\n";
    }
}

int main()
{
    Mundo m;
    std::string teclas;
    std::cin >> teclas;
    int cuadro = 0;
    for (char t : teclas) {
        entrada(m, t);
        actualizar(m, cuadro);
        if (cuadro % 3 == 0 || !m.viva) {
            dibujar(m, cuadro);
        }
        cuadro++;
        if (!m.viva) {
            break;
        }
    }
    std::cout << (m.viva ? "Lima sigue en pie" : "¡Una roca alcanzó a Lima!") << "; rocas esquivadas: " << m.esquivadas << "\n";
    return 0;
}
```

#### Pruebas

##### Lima quieta
```entrada
................
```
```salida
cuadro 0:
  .o.....
  .......
  .......
  .......
  .......
  ...@...
cuadro 3:
  .......
  ....o..
  .......
  .o.....
  .......
  ...@...
cuadro 6:
  ...o...
  .......
  o......
  .......
  ....o..
  ...@...
cuadro 9:
  .......
  ......o
  .......
  ...o...
  .......
  o..@...
cuadro 11:
  .......
  ..o....
  .......
  ......o
  .......
  ...X...
¡Una roca alcanzó a Lima!; rocas esquivadas: 3
```

##### Siempre a la izquierda
```entrada
iiiiiiiiiiiiiiii
```
```salida
cuadro 0:
  .o.....
  .......
  .......
  .......
  .......
  ..@....
cuadro 3:
  .......
  ....o..
  .......
  .o.....
  .......
  @......
cuadro 6:
  ...o...
  .......
  o......
  .......
  ....o..
  @......
cuadro 9:
  .......
  ......o
  .......
  ...o...
  .......
  X......
¡Una roca alcanzó a Lima!; rocas esquivadas: 2
```

##### Pocos cuadros
```entrada
d
```
```salida
cuadro 0:
  .o.....
  .......
  .......
  .......
  .......
  ....@..
Lima sigue en pie; rocas esquivadas: 0
```

### Encargo R05-N05-E1 · El semáforo de la esquina

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un semáforo dura 20 s en verde, 3 en amarillo y 15 en rojo. Si un peatón aprieta el
botón, el verde se acorta a 5 s (contando desde que empezó el verde); cuando se pone
rojo, el pedido se borra. Simulá 60 segundos con `dt = 0.5`: la entrada es el
segundo en que el peatón aprieta el botón. Mostrá cuándo aprieta y cada cambio de
luz con su tiempo.

#### Criterio de aprobación

- El semáforo es una máquina de estados que avanza con `dt`.
- El pedido del peatón acorta solo el verde y se borra en rojo.

#### Entrada de ejemplo

```
30
```

#### Salida esperada

```
20.0 s: amarilla
23.0 s: roja
30.0 s: un peatón aprieta el botón
38.0 s: verde
43.0 s: amarilla
46.0 s: roja
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El semaforo de la esquina: estados con tiempo (dt) y un boton peatonal.
#include <iomanip>
#include <iostream>
#include <string>

enum class Luz { Verde, Amarilla, Roja };

struct Semaforo {
    Luz luz = Luz::Verde;
    double tiempo = 0;          // segundos en la luz actual
    bool pedido = false;        // un peaton apreto el boton

    double duracion() const
    {
        switch (luz) {
        case Luz::Verde:
            return pedido ? 5 : 20;          // con pedido, el verde se acorta
        case Luz::Amarilla:
            return 3;
        case Luz::Roja:
            return 15;
        }
        return 0;
    }

    // Devuelve true si cambio de luz.
    bool actualizar(double dt)
    {
        tiempo += dt;
        if (tiempo < duracion()) {
            return false;
        }
        tiempo = 0;
        luz = luz == Luz::Verde ? Luz::Amarilla : luz == Luz::Amarilla ? Luz::Roja : Luz::Verde;
        if (luz == Luz::Roja) {
            pedido = false;                  // el peaton cruza
        }
        return true;
    }
};

std::string nombre(Luz l)
{
    switch (l) {
    case Luz::Verde:
        return "verde";
    case Luz::Amarilla:
        return "amarilla";
    case Luz::Roja:
        return "roja";
    }
    return "?";
}

int main()
{
    Semaforo s;
    const double DT = 0.5;
    double reloj = 0;
    double boton = -1;
    std::cin >> boton;                        // en que segundo aprieta el boton el peaton
    std::cout << std::fixed << std::setprecision(1);
    while (reloj < 60) {
        if (!s.pedido && boton >= 0 && reloj >= boton) {
            s.pedido = true;
            boton = -1;
            std::cout << reloj << " s: un peatón aprieta el botón\n";
        }
        reloj += DT;
        if (s.actualizar(DT)) {
            std::cout << reloj << " s: " << nombre(s.luz) << "\n";
        }
    }
    return 0;
}
```

#### Pruebas

##### Aprieta temprano
```entrada
2
```
```salida
2.0 s: un peatón aprieta el botón
5.0 s: amarilla
8.0 s: roja
23.0 s: verde
43.0 s: amarilla
46.0 s: roja
```

##### Aprieta en rojo
```entrada
21
```
```salida
20.0 s: amarilla
21.0 s: un peatón aprieta el botón
23.0 s: roja
38.0 s: verde
58.0 s: amarilla
```

##### Aprieta justo al final
```entrada
59.5
```
```salida
20.0 s: amarilla
23.0 s: roja
38.0 s: verde
58.0 s: amarilla
59.5 s: un peatón aprieta el botón
```

### Prueba del sello

#### ¿Cuáles son las tres partes del bucle de juego?

Procesar la entrada, actualizar el mundo y dibujar.

#### ¿Por qué se multiplica la velocidad por `dt`?

Para que el movimiento dependa de los segundos que pasaron y no de cuántos cuadros por segundo dibuja la compu.

#### ¿Por qué `dibujar` recibe el mundo por `const&`?

Para garantizar que dibujar no cambie el estado del juego.

#### ¿Qué tiene que hacer `actualizar` en pausa?

Nada: el mundo se congela.

#### ¿Por qué en el curso se usa un `dt` fijo?

Para que la simulación dé siempre el mismo resultado y se pueda comparar con la salida esperada.

### Soluciones (docente)

Material original: `05-C++-Videojuegos/05-GameState` y `06-GameLoop` (con dt fijo para que la salida sea comparable).

## R05-N06 · Jefe: el Minotauro del Laberinto

```meta
tipo: jefe
padre: R05-N05
precio: 10
criatura: dragon
insignia: Sello del Minotauro
insignia_descripcion: Venciste al Minotauro del Laberinto: dominás C++, de la primera línea a un juego completo.
usa: arch.texto, err.excepciones, prog.modulos
```

### Crónica

Debajo del Taller del Juego, detrás de una puerta que ningún aprendiz abrió, está el **Laberinto**. Adentro vive el **Minotauro**, un toro de hierro y bronce que camina en dos patas: no persigue, **embiste**. Si te ve en línea recta, cruza el pasillo de dos zancadas. Del cuello le cuelga un **engranaje** enorme.

—Todo lo que aprendiste está en este plano —dice {mentor}, y le da a Bron una hoja con un laberinto dibujado—. Clases, contenedores, `optional`, excepciones, estados, el bucle. Armalo pieza por pieza.

Bron no entra a los golpes: entra con el plano. Cuando el Minotauro se queda trabado en un pasillo en diagonal, el engranaje se le suelta del cuello. Es **el Engranaje del Portal**: tiene los mismos dientes que las bisagras del Vidriero. Tesla lo mira y, por primera vez, no termina la frase de nadie.

### Objetivos

Integrar todo el curso en un juego completo de varios archivos, y en programas que
guardan y cargan datos con manejo de errores.

### Antes de empezar

- Todo el camino principal.

### Explicación

#### El proyecto: un juego de laberinto por turnos
| Archivo | Responsabilidad |
|---|---|
| `Vec2.h` | una coordenada de la grilla, con `==`, `+` y la distancia en pasos |
| `Mapa.h` / `.cpp` | la grilla: validar el nivel (lanza si está mal), decir qué es transitable, vaciar casillas, dibujar con entidades encima |
| `Entidades.h` / `.cpp` | la clase `Entidad` (jugadora y enemigos) y las funciones de dirección (`optional<Vec2>`) y de "un paso hacia" |
| `Juego.h` / `.cpp` | junta todo: un turno = mover a Lima, mover a los enemigos, revisar el fin |
| `main.cpp` | el nivel, el bucle de teclas y el `try`/`catch` |

#### Cómo encararlo
1. `Vec2` y `Mapa` primero: con un `main` de prueba que cargue el nivel y lo dibuje.
   Probá un nivel roto (una fila más corta) y verificá que lanza.
2. `Entidad` y `direccion`/`paso_hacia`, probadas solas.
3. `Juego` con solo la jugadora moviéndose; después la llave, la puerta y la poción;
   al final los enemigos, **uno por uno**.
4. El bucle de `main`.

Compilá con `-fsanitize=address,undefined` mientras lo armás: un índice fuera de
la grilla aparece enseguida.

#### Las reglas de los enemigos
Son tres "IA" distintas, elegidas por un `enum class Tipo` dentro de
`mover_enemigo`. (Otra forma sería una jerarquía con un `virtual mover()`: pensá qué
ventajas tendría cada una.)

### ¿Para qué sirve?

Un roguelike por turnos es un proyecto completo en miniatura: mapa, entidades, IA, reglas, estados, entrada y salida. La arquitectura (mapa, entidades, juego, bucle) es la misma que la de un juego gráfico: en la Senda de SDL3 solo cambian la entrada y el dibujo. Guardar y cargar con errores claros es lo que hace cualquier programa serio con sus archivos.

### Errores habituales

**Orco: mirar fuera de la grilla.** `filas_[p.y][p.x]` con `p` fuera del mapa. Por
eso `en()` revisa `dentro()` y devuelve pared.

**Ogro: el enemigo que atraviesa a otro.** Antes de mover, revisar que el destino
esté libre (sin pared, sin puerta, sin otra entidad).

**Troll: guardar un `Entidad*` y después agregar enemigos.** Si el vector crece,
los punteros dejan de valer. Buscá cuando lo necesitás.

**Ogro: la IA que se mueve dos veces.** El Minotauro embiste dos pasos, pero si en
el primero llega a Lima, ataca y **termina**.

**Ogro: seguir jugando después del final.** Cuando el estado ya no es "jugando",
`turno` no hace nada.

### Misión R05-N06-M1 · El Laberinto del Minotauro

```meta
entrega: archivo
entorno: local
monedas: 8
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

Armá el juego en los cinco módulos de la tabla, con su `CMakeLists.txt`. El nivel:
```
###############
#S...#......!.#
#.##.#.##.###.#
#..#.+..g.....#
#k.#.#.###.M..#
#..r.#......#>#
###############
```
**Mapa**: `#` pared, `.` piso, `+` puerta cerrada, `k` llave, `!` poción, `>`
salida, `S` inicio. El constructor valida (filas del mismo largo, hay `S` y `>`) y
lanza `std::invalid_argument` si no.

**Lima** (30 de vida, ataque 6) se mueve con `w a s d`; cualquier otra tecla es
esperar. Moverse hacia un enemigo lo **golpea**. Pisar la llave la junta; la poción
cura 15; empujar la puerta con la llave la abre (sin moverse); llegar a `>` es la
victoria.

**Enemigos** (letras del nivel): la **rata** (6 de vida, ataque 2) persigue si está a
3 pasos o menos; el **goblin** (12, 3) persigue a 8 o menos; el **Minotauro** (30, 7)
solo se mueve si Lima está en su misma fila o columna, a 6 o menos, sin paredes en
el medio: entonces avanza **dos** pasos. Todos se mueven un paso hacia Lima (primero
en x, después en y) si el destino está libre, y si el destino es Lima, la atacan.

La entrada es una palabra con las teclas. Mostrá el mapa al principio y al final, y
una línea por turno con la tecla, la posición de Lima y lo que pasó.

#### Criterio de aprobación

- El proyecto está en cinco módulos y compila con CMake sin advertencias.
- El mapa lanza una excepción con un nivel inválido y `main` la atrapa.
- Los enemigos siguen sus reglas y el juego termina en victoria o derrota.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
sssssddddwwddddddddddddss
```

#### Salida esperada

```
###############
#@...#......!.#
#.##.#.##.###.#
#..#.+..g.....#
#k.#.#.###.M..#
#..r.#......#>#
###############
Vida 30/30
Turno 1 [s] (1,2):
Turno 2 [s] (1,3):
Turno 3 [s] (1,4): Lima junta la llave.
Turno 4 [s] (1,5): La rata ataca a Lima (28).
Turno 5 [s] (1,5): Lima choca contra la pared. La rata ataca a Lima (26).
Turno 6 [d] (1,5): Lima golpea: la rata cae.
Turno 7 [d] (2,5):
Turno 8 [d] (3,5):
Turno 9 [d] (4,5):
Turno 10 [w] (4,4):
Turno 11 [w] (4,3):
Turno 12 [d] (4,3): Lima abre la puerta con la llave.
Turno 13 [d] (4,3): Lima golpea: el goblin queda en 6. El goblin ataca a Lima (23).
Turno 14 [d] (4,3): Lima golpea: el goblin cae.
Turno 15 [d] (5,3):
Turno 16 [d] (6,3):
Turno 17 [d] (7,3):
Turno 18 [d] (8,3):
Turno 19 [d] (9,3):
Turno 20 [d] (10,3):
Turno 21 [d] (11,3): El Minotauro ataca a Lima (16).
Turno 22 [d] (12,3):
Turno 23 [d] (13,3):
Turno 24 [s] (13,4): El Minotauro embiste. El Minotauro ataca a Lima (9).
Turno 25 [s] (13,5): ¡Lima sale del laberinto!
###############
#....#......!.#
#.##.#.##.###.#
#..#..........#
#..#.#.###..M.#
#....#......#@#
###############
Vida 9/30  [llave]
=== ¡VICTORIA! Lima escapa del Minotauro ===
```

#### Solución de referencia

```cpp
// ===== Vec2.h =====
#pragma once

#include <cstdlib>

struct Vec2 {
    int x = 0;
    int y = 0;
    bool operator==(const Vec2&) const = default;
};

inline Vec2 operator+(Vec2 a, Vec2 b) { return {a.x + b.x, a.y + b.y}; }

inline int distancia(Vec2 a, Vec2 b) { return std::abs(a.x - b.x) + std::abs(a.y - b.y); }   // en pasos

// ===== Mapa.h =====
#pragma once

#include <string>
#include <utility>
#include <vector>

#include "Vec2.h"

// La grilla del laberinto: '#' pared, '.' piso, '+' puerta cerrada, 'k' llave,
// '!' pocion, '>' salida, 'S' inicio. Lanza std::invalid_argument si el mapa es invalido.
class Mapa {
public:
    explicit Mapa(const std::vector<std::string>& filas);

    bool dentro(Vec2 p) const;
    char en(Vec2 p) const;
    bool transitable(Vec2 p) const;           // dentro, sin pared ni puerta cerrada
    void vaciar(Vec2 p);                      // lo que habia (llave, pocion, puerta) pasa a ser piso
    Vec2 inicio() const { return inicio_; }
    std::string dibujar(const std::vector<std::pair<Vec2, char>>& encima) const;

private:
    std::vector<std::string> filas_;
    Vec2 inicio_;
};

// ===== Mapa.cpp =====
#include "Mapa.h"

#include <stdexcept>

Mapa::Mapa(const std::vector<std::string>& filas) : filas_(filas)
{
    if (filas_.empty()) {
        throw std::invalid_argument("el mapa está vacío");
    }
    bool hay_inicio = false, hay_salida = false;
    for (std::size_t y = 0; y < filas_.size(); y++) {
        if (filas_[y].size() != filas_[0].size()) {
            throw std::invalid_argument("la fila " + std::to_string(y) + " tiene otro largo");
        }
        for (std::size_t x = 0; x < filas_[y].size(); x++) {
            if (filas_[y][x] == 'S') {
                inicio_ = {static_cast<int>(x), static_cast<int>(y)};
                filas_[y][x] = '.';
                hay_inicio = true;
            } else if (filas_[y][x] == '>') {
                hay_salida = true;
            }
        }
    }
    if (!hay_inicio || !hay_salida) {
        throw std::invalid_argument("al mapa le falta el inicio (S) o la salida (>)");
    }
}

bool Mapa::dentro(Vec2 p) const
{
    return p.y >= 0 && p.y < static_cast<int>(filas_.size()) && p.x >= 0 && p.x < static_cast<int>(filas_[0].size());
}

char Mapa::en(Vec2 p) const
{
    return dentro(p) ? filas_[p.y][p.x] : '#';
}

bool Mapa::transitable(Vec2 p) const
{
    char c = en(p);
    return c != '#' && c != '+';
}

void Mapa::vaciar(Vec2 p)
{
    if (dentro(p)) {
        filas_[p.y][p.x] = '.';
    }
}

std::string Mapa::dibujar(const std::vector<std::pair<Vec2, char>>& encima) const
{
    std::vector<std::string> lienzo = filas_;
    for (const auto& [p, c] : encima) {
        if (dentro(p)) {
            lienzo[p.y][p.x] = c;
        }
    }
    std::string r;
    for (const auto& fila : lienzo) {
        r += fila + "\n";
    }
    return r;
}

// ===== Entidades.h =====
#pragma once

#include <optional>
#include <string>

#include "Vec2.h"

enum class Tipo { Jugador, Rata, Goblin, Minotauro };

class Entidad {
public:
    Entidad(Tipo tipo, const std::string& nombre, char glifo, Vec2 pos, int vida, int ataque);

    Tipo tipo() const { return tipo_; }
    const std::string& nombre() const { return nombre_; }
    char glifo() const { return glifo_; }
    Vec2 pos() const { return pos_; }
    int vida() const { return vida_; }
    int vida_max() const { return vida_max_; }
    int ataque() const { return ataque_; }
    bool viva() const { return vida_ > 0; }

    void mover_a(Vec2 p) { pos_ = p; }
    void recibir_dano(int n);
    void curar(int n);

private:
    Tipo tipo_;
    std::string nombre_;
    char glifo_;
    Vec2 pos_;
    int vida_;
    int vida_max_;
    int ataque_;
};

std::optional<Vec2> direccion(char tecla);        // w a s d; otra tecla: nada
Vec2 paso_hacia(Vec2 desde, Vec2 hacia);          // un paso: primero en x, despues en y

// ===== Entidades.cpp =====
#include "Entidades.h"

#include <algorithm>

Entidad::Entidad(Tipo tipo, const std::string& nombre, char glifo, Vec2 pos, int vida, int ataque)
    : tipo_(tipo), nombre_(nombre), glifo_(glifo), pos_(pos), vida_(vida), vida_max_(vida), ataque_(ataque)
{
}

void Entidad::recibir_dano(int n)
{
    vida_ = std::max(0, vida_ - n);
}

void Entidad::curar(int n)
{
    vida_ = std::min(vida_max_, vida_ + n);
}

std::optional<Vec2> direccion(char tecla)
{
    switch (tecla) {
    case 'w':
        return Vec2{0, -1};
    case 's':
        return Vec2{0, 1};
    case 'a':
        return Vec2{-1, 0};
    case 'd':
        return Vec2{1, 0};
    default:
        return std::nullopt;
    }
}

Vec2 paso_hacia(Vec2 desde, Vec2 hacia)
{
    if (desde.x != hacia.x) {
        return {hacia.x > desde.x ? 1 : -1, 0};
    }
    if (desde.y != hacia.y) {
        return {0, hacia.y > desde.y ? 1 : -1};
    }
    return {0, 0};
}

// ===== Juego.h =====
#pragma once

#include <string>
#include <vector>

#include "Entidades.h"
#include "Mapa.h"

enum class Estado { Jugando, Victoria, Derrota };

class Juego {
public:
    explicit Juego(const std::vector<std::string>& nivel);   // puede lanzar si el nivel es invalido

    void turno(char tecla);
    std::string dibujar() const;
    const std::vector<std::string>& registro() const { return registro_; }
    Estado estado() const { return estado_; }
    int numero_turno() const { return turno_; }
    const Entidad& jugadora() const { return jugadora_; }

private:
    void mover_jugadora(char tecla);
    void mover_enemigos();
    void mover_enemigo(Entidad& e);
    Entidad* enemigo_en(Vec2 p);
    bool libre(Vec2 p);
    bool linea_libre(Vec2 a, Vec2 b) const;

    Mapa mapa_;
    Entidad jugadora_;
    std::vector<Entidad> enemigos_;
    bool llave_ = false;
    Estado estado_ = Estado::Jugando;
    int turno_ = 0;
    std::vector<std::string> registro_;
};

// ===== Juego.cpp =====
#include "Juego.h"

#include <algorithm>
#include <cctype>

namespace {

std::string mayuscula(std::string s)          // "el goblin" -> "El goblin", para empezar una frase
{
    if (!s.empty()) {
        s[0] = static_cast<char>(std::toupper(static_cast<unsigned char>(s[0])));
    }
    return s;
}

}  // namespace

Juego::Juego(const std::vector<std::string>& nivel)
    : mapa_(nivel), jugadora_(Tipo::Jugador, "Lima", '@', mapa_.inicio(), 30, 6)
{
    // los enemigos se marcan en el nivel con su letra; se sacan del mapa y se crean
    for (std::size_t y = 0; y < nivel.size(); y++) {
        for (std::size_t x = 0; x < nivel[y].size(); x++) {
            Vec2 p{static_cast<int>(x), static_cast<int>(y)};
            switch (nivel[y][x]) {
            case 'r':
                enemigos_.emplace_back(Tipo::Rata, "la rata", 'r', p, 6, 2);
                break;
            case 'g':
                enemigos_.emplace_back(Tipo::Goblin, "el goblin", 'g', p, 12, 3);
                break;
            case 'M':
                enemigos_.emplace_back(Tipo::Minotauro, "el Minotauro", 'M', p, 30, 7);
                break;
            default:
                continue;
            }
            mapa_.vaciar(p);
        }
    }
}

Entidad* Juego::enemigo_en(Vec2 p)
{
    auto it = std::ranges::find_if(enemigos_, [p](const Entidad& e) { return e.viva() && e.pos() == p; });
    return it == enemigos_.end() ? nullptr : &*it;
}

bool Juego::libre(Vec2 p)
{
    return mapa_.transitable(p) && enemigo_en(p) == nullptr && !(jugadora_.pos() == p);
}

void Juego::turno(char tecla)
{
    if (estado_ != Estado::Jugando) {
        return;
    }
    registro_.clear();
    turno_++;
    mover_jugadora(tecla);
    if (estado_ == Estado::Jugando) {
        mover_enemigos();
    }
    if (!jugadora_.viva()) {
        estado_ = Estado::Derrota;
        registro_.push_back("Lima cae en el laberinto.");
    }
}

void Juego::mover_jugadora(char tecla)
{
    auto dir = direccion(tecla);
    if (!dir) {
        registro_.push_back("Lima espera.");
        return;
    }
    Vec2 destino = jugadora_.pos() + *dir;
    if (Entidad* e = enemigo_en(destino)) {
        e->recibir_dano(jugadora_.ataque());
        registro_.push_back("Lima golpea: " + e->nombre() + (e->viva() ? " queda en " + std::to_string(e->vida()) + "." : " cae."));
        return;
    }
    char c = mapa_.en(destino);
    if (c == '+') {
        if (llave_) {
            mapa_.vaciar(destino);
            registro_.push_back("Lima abre la puerta con la llave.");
        } else {
            registro_.push_back("La puerta está cerrada.");
        }
        return;
    }
    if (!mapa_.transitable(destino)) {
        registro_.push_back("Lima choca contra la pared.");
        return;
    }
    jugadora_.mover_a(destino);
    if (c == 'k') {
        llave_ = true;
        mapa_.vaciar(destino);
        registro_.push_back("Lima junta la llave.");
    } else if (c == '!') {
        jugadora_.curar(15);
        mapa_.vaciar(destino);
        registro_.push_back("Lima bebe una poción (" + std::to_string(jugadora_.vida()) + ").");
    } else if (c == '>') {
        estado_ = Estado::Victoria;
        registro_.push_back("¡Lima sale del laberinto!");
    }
}

bool Juego::linea_libre(Vec2 a, Vec2 b) const
{
    Vec2 paso = paso_hacia(a, b);
    for (Vec2 p = a + paso; !(p == b); p = p + paso) {
        if (!mapa_.transitable(p)) {
            return false;
        }
    }
    return true;
}

void Juego::mover_enemigo(Entidad& e)
{
    Vec2 k = jugadora_.pos();
    int d = distancia(e.pos(), k);
    int pasos = 0;
    switch (e.tipo()) {
    case Tipo::Rata:
        pasos = d <= 3 ? 1 : 0;                  // solo persigue de cerca
        break;
    case Tipo::Goblin:
        pasos = d <= 8 ? 1 : 0;                  // persigue de lejos
        break;
    case Tipo::Minotauro:                        // embiste en linea recta
        pasos = ((e.pos().x == k.x || e.pos().y == k.y) && d <= 6 && linea_libre(e.pos(), k)) ? 2 : 0;
        break;
    case Tipo::Jugador:
        break;
    }
    for (int i = 0; i < pasos; i++) {
        Vec2 destino = e.pos() + paso_hacia(e.pos(), k);
        if (destino == k) {
            jugadora_.recibir_dano(e.ataque());
            registro_.push_back(mayuscula(e.nombre()) + " ataca a Lima (" + std::to_string(jugadora_.vida()) + ").");
            return;
        }
        if (!libre(destino)) {
            return;
        }
        e.mover_a(destino);
        if (e.tipo() == Tipo::Minotauro && i == 0) {
            registro_.push_back("El Minotauro embiste.");
        }
    }
}

void Juego::mover_enemigos()
{
    for (auto& e : enemigos_) {
        if (e.viva() && jugadora_.viva()) {
            mover_enemigo(e);
        }
    }
}

std::string Juego::dibujar() const
{
    std::vector<std::pair<Vec2, char>> encima;
    for (const auto& e : enemigos_) {
        if (e.viva()) {
            encima.push_back({e.pos(), e.glifo()});
        }
    }
    encima.push_back({jugadora_.pos(), jugadora_.glifo()});
    return mapa_.dibujar(encima) + "Vida " + std::to_string(jugadora_.vida()) + "/" + std::to_string(jugadora_.vida_max()) +
           (llave_ ? "  [llave]" : "") + "\n";
}

// ===== main.cpp =====
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "Juego.h"

const std::vector<std::string> NIVEL = {
    "###############",
    "#S...#......!.#",
    "#.##.#.##.###.#",
    "#..#.+..g.....#",
    "#k.#.#.###.M..#",
    "#..r.#......#>#",
    "###############",
};

int main()
{
    try {
        Juego juego(NIVEL);
        std::cout << juego.dibujar();
        std::string teclas;
        std::cin >> teclas;
        for (char t : teclas) {
            if (juego.estado() != Estado::Jugando) {
                break;
            }
            juego.turno(t);
            Vec2 p = juego.jugadora().pos();
            std::cout << "Turno " << juego.numero_turno() << " [" << t << "] (" << p.x << "," << p.y << "):";
            for (const auto& linea : juego.registro()) {
                std::cout << " " << linea;
            }
            std::cout << "\n";
        }
        std::cout << juego.dibujar();
        switch (juego.estado()) {
        case Estado::Victoria:
            std::cout << "=== ¡VICTORIA! Lima escapa del Minotauro ===\n";
            break;
        case Estado::Derrota:
            std::cout << "=== DERROTA ===\n";
            break;
        case Estado::Jugando:
            std::cout << "=== Lima sigue en el laberinto ===\n";
            break;
        }
    } catch (const std::invalid_argument& e) {
        std::cerr << "Nivel inválido: " << e.what() << "\n";
        return 1;
    }
    return 0;
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(laberinto CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(laberinto main.cpp Mapa.cpp Entidades.cpp Juego.cpp)
target_compile_options(laberinto PRIVATE -Wall -Wextra)
```

### Misión R05-N06-M2 · La partida guardada

```meta
entrega: codigo
entorno: local
monedas: 8
xp: 40
```

#### Consigna

Guardá una partida (heroína, posición, vida, llave y enemigos vencidos) en
`partida.sav`, en líneas `clave valor` con una primera línea `LABERINTO 1`. Escribí
`cargar(ruta)`, que **lanza** una excepción propia `ArchivoRoto(linea, motivo)` si
la primera línea no es la esperada, si una posición o una vida es inválida (vida de
1 a 30), si hay una clave desconocida o si faltan datos; y `std::runtime_error` si
el archivo no existe.

El programa guarda, carga y muestra. Después, cada línea de la entrada es una
"rotura": `N texto` reemplaza la línea N del archivo por `texto`; se intenta cargar
(mostrando la partida o el error) y se restaura el archivo.

#### Criterio de aprobación

- Los errores de formato lanzan `ArchivoRoto` con el número de línea.
- Una carga fallida no corta el programa.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
4 vida 99
1 PARTIDA VIEJA
3 posicion -1 2
6 enemigos rata
2 heroina Bron
```

#### Salida esperada

```
Guardada.
  Lima en (4, 3), vida 23, con llave, venció a 2
Rompo la línea 4 -> "vida 99"
  Partida dañada, línea 4: vida fuera de rango
Rompo la línea 1 -> "PARTIDA VIEJA"
  Partida dañada, línea 1: no es una partida guardada
Rompo la línea 3 -> "posicion -1 2"
  Partida dañada, línea 3: posición inválida
Rompo la línea 6 -> "enemigos rata"
  Partida dañada, línea 6: clave desconocida "enemigos"
Rompo la línea 2 -> "heroina Bron"
  Bron en (4, 3), vida 23, con llave, venció a 2
```

#### Solución de referencia

```cpp
// Jefe final - La partida guardada: guardar y cargar, con errores claros si el archivo esta roto.
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

class ArchivoRoto : public std::runtime_error {
public:
    ArchivoRoto(int linea, const std::string& motivo)
        : std::runtime_error("línea " + std::to_string(linea) + ": " + motivo) {}
};

struct Partida {
    std::string heroina;
    int x = 0;
    int y = 0;
    int vida = 0;
    bool llave = false;
    std::vector<std::string> enemigos_vencidos;
};

void guardar(const Partida& p, const std::string& ruta)
{
    std::ofstream out(ruta);
    if (!out) {
        throw std::runtime_error("no se puede escribir " + ruta);
    }
    out << "LABERINTO 1\n";
    out << "heroina " << p.heroina << "\n";
    out << "posicion " << p.x << " " << p.y << "\n";
    out << "vida " << p.vida << "\n";
    out << "llave " << (p.llave ? 1 : 0) << "\n";
    out << "vencidos";
    for (const auto& e : p.enemigos_vencidos) {
        out << " " << e;
    }
    out << "\n";
}

Partida cargar(const std::string& ruta)
{
    std::ifstream in(ruta);
    if (!in) {
        throw std::runtime_error("no existe " + ruta);
    }
    std::string linea;
    if (!std::getline(in, linea) || linea != "LABERINTO 1") {
        throw ArchivoRoto(1, "no es una partida guardada");
    }
    Partida p;
    int numero = 1;
    int campos = 0;
    while (std::getline(in, linea)) {
        numero++;
        std::istringstream ss(linea);
        std::string clave;
        ss >> clave;
        if (clave == "heroina") {
            ss >> p.heroina;
        } else if (clave == "posicion") {
            if (!(ss >> p.x >> p.y) || p.x < 0 || p.y < 0) {
                throw ArchivoRoto(numero, "posición inválida");
            }
        } else if (clave == "vida") {
            if (!(ss >> p.vida) || p.vida <= 0 || p.vida > 30) {
                throw ArchivoRoto(numero, "vida fuera de rango");
            }
        } else if (clave == "llave") {
            int l = 0;
            ss >> l;
            p.llave = (l == 1);
        } else if (clave == "vencidos") {
            std::string e;
            while (ss >> e) {
                p.enemigos_vencidos.push_back(e);
            }
        } else {
            throw ArchivoRoto(numero, "clave desconocida \"" + clave + "\"");
        }
        campos++;
    }
    if (campos < 5) {
        throw ArchivoRoto(numero, "faltan datos");
    }
    return p;
}

void mostrar(const Partida& p)
{
    std::cout << "  " << p.heroina << " en (" << p.x << ", " << p.y << "), vida " << p.vida << (p.llave ? ", con llave" : "")
              << ", venció a " << p.enemigos_vencidos.size() << "\n";
}

int main()
{
    const std::string RUTA = "partida.sav";
    guardar({"Lima", 4, 3, 23, true, {"rata", "goblin"}}, RUTA);
    std::cout << "Guardada.\n";

    // Cada linea de la entrada es una "rotura" que alguien le hace al archivo: la linea N se reemplaza.
    std::string cambio;
    int prueba = 0;
    do {
        if (prueba > 0) {
            std::istringstream c(cambio);
            int n = 0;
            c >> n;
            std::string nuevo;
            std::getline(c >> std::ws, nuevo);
            std::ifstream in(RUTA);
            std::vector<std::string> lineas;
            for (std::string l; std::getline(in, l);) {
                lineas.push_back(l);
            }
            in.close();
            if (n >= 1 && n <= static_cast<int>(lineas.size())) {
                lineas[n - 1] = nuevo;
            }
            std::ofstream out(RUTA);
            for (const auto& l : lineas) {
                out << l << "\n";
            }
            std::cout << "Rompo la línea " << n << " -> \"" << nuevo << "\"\n";
        }
        try {
            mostrar(cargar(RUTA));
        } catch (const ArchivoRoto& e) {
            std::cout << "  Partida dañada, " << e.what() << "\n";
        } catch (const std::exception& e) {
            std::cout << "  Error: " << e.what() << "\n";
        }
        guardar({"Lima", 4, 3, 23, true, {"rata", "goblin"}}, RUTA);   // se restaura para la proxima prueba
        prueba++;
    } while (std::getline(std::cin, cambio));
    return 0;
}
```

#### Pruebas

##### Sin roturas
```entrada
```
```salida
Guardada.
  Lima en (4, 3), vida 23, con llave, venció a 2
```

##### Línea vacía
```entrada
5
```
```salida
Guardada.
  Lima en (4, 3), vida 23, con llave, venció a 2
Rompo la línea 5 -> ""
  Partida dañada, línea 5: clave desconocida ""
```

##### Llave y vida en el borde
```entrada
4 vida 30
4 vida 0
```
```salida
Guardada.
  Lima en (4, 3), vida 23, con llave, venció a 2
Rompo la línea 4 -> "vida 30"
  Lima en (4, 3), vida 30, con llave, venció a 2
Rompo la línea 4 -> "vida 0"
  Partida dañada, línea 4: vida fuera de rango
```

### Encargo R05-N06-E1 · Las reservas de la cancha

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 40
```

#### Consigna

El club necesita un sistema de reservas para su cancha. Cada línea de la entrada es
`reservar dia hora nombre` o `cancelar dia hora`. `class Cancha` guarda un
`std::map<dia, std::map<hora, nombre>>` y lanza una excepción propia
`ReservaInvalida` si el día no existe, la hora está fuera de 9 a 22, el turno ya está
tomado o se cancela algo que no estaba. Mostrá la respuesta a cada pedido, las
reservas por día y guardalas en `reservas.txt` (mostrá el archivo).

#### Criterio de aprobación

- Las validaciones están en la clase y lanzan una excepción propia.
- Un pedido rechazado no corta el programa.
- Guarda el archivo y lo muestra leyéndolo del disco.

#### Entrada de ejemplo

```
reservar lunes 18 Ana
reservar lunes 18 Bruno
reservar martes 23 Celi
reservar juevs 10 Dami
reservar lunes 20 Bruno
cancelar martes 10
reservar sabado 9 Eli
cancelar lunes 18
reservar lunes 18 Fede
pagar lunes 18
```

#### Salida esperada

```
Reservado: lunes 18h (Ana)
No se pudo: el lunes a las 18 ya está reservado
No se pudo: la cancha abre de 9 a 22
No se pudo: día desconocido: juevs
Reservado: lunes 20h (Bruno)
No se pudo: no había reserva el martes a las 10
Reservado: sabado 9h (Eli)
Cancelado: lunes 18h
Reservado: lunes 18h (Fede)
No se pudo: orden desconocida: pagar
Reservas (5 pedidos rechazados):
  lunes: 18h Fede 20h Bruno
  sabado: 9h Eli
--- reservas.txt ---
lunes 18 Fede
lunes 20 Bruno
sabado 9 Eli
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Las reservas de la cancha: menu, excepciones, map y archivo.
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>

class ReservaInvalida : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

class Cancha {
public:
    void reservar(const std::string& dia, int hora, const std::string& quien)
    {
        validar(dia, hora);
        auto& del_dia = turnos_[dia];
        if (del_dia.contains(hora)) {
            throw ReservaInvalida("el " + dia + " a las " + std::to_string(hora) + " ya está reservado");
        }
        del_dia[hora] = quien;
    }

    void cancelar(const std::string& dia, int hora)
    {
        validar(dia, hora);
        if (turnos_[dia].erase(hora) == 0) {
            throw ReservaInvalida("no había reserva el " + dia + " a las " + std::to_string(hora));
        }
    }

    void guardar(const std::string& ruta) const
    {
        std::ofstream out(ruta);
        for (const auto& [dia, horas] : turnos_) {
            for (const auto& [hora, quien] : horas) {
                out << dia << " " << hora << " " << quien << "\n";
            }
        }
    }

    void mostrar() const
    {
        for (const auto& [dia, horas] : turnos_) {
            if (horas.empty()) {
                continue;
            }
            std::cout << "  " << dia << ":";
            for (const auto& [hora, quien] : horas) {
                std::cout << " " << hora << "h " << quien;
            }
            std::cout << "\n";
        }
    }

private:
    static void validar(const std::string& dia, int hora)
    {
        static const std::set<std::string> DIAS = {"lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"};
        if (!DIAS.contains(dia)) {
            throw ReservaInvalida("día desconocido: " + dia);
        }
        if (hora < 9 || hora > 22) {
            throw ReservaInvalida("la cancha abre de 9 a 22");
        }
    }

    std::map<std::string, std::map<int, std::string>> turnos_;
};

int main()
{
    Cancha cancha;
    std::string linea;
    int errores = 0;
    while (std::getline(std::cin, linea)) {
        std::istringstream in(linea);
        std::string orden, dia, quien;
        int hora = 0;
        in >> orden >> dia >> hora >> quien;
        try {
            if (orden == "reservar") {
                cancha.reservar(dia, hora, quien);
                std::cout << "Reservado: " << dia << " " << hora << "h (" << quien << ")\n";
            } else if (orden == "cancelar") {
                cancha.cancelar(dia, hora);
                std::cout << "Cancelado: " << dia << " " << hora << "h\n";
            } else {
                throw ReservaInvalida("orden desconocida: " + orden);
            }
        } catch (const ReservaInvalida& e) {
            std::cout << "No se pudo: " << e.what() << "\n";
            errores++;
        }
    }
    std::cout << "Reservas (" << errores << " pedidos rechazados):\n";
    cancha.mostrar();
    cancha.guardar("reservas.txt");
    std::ifstream in("reservas.txt");
    std::cout << "--- reservas.txt ---\n" << in.rdbuf();
    return 0;
}
```

#### Pruebas

##### Sin pedidos
```entrada
```
```salida
Reservas (0 pedidos rechazados):
--- reservas.txt ---
```

##### Bordes del horario
```entrada
reservar domingo 9 Ana
reservar domingo 22 Bruno
reservar domingo 8 Celi
reservar domingo 23 Dami
```
```salida
Reservado: domingo 9h (Ana)
Reservado: domingo 22h (Bruno)
No se pudo: la cancha abre de 9 a 22
No se pudo: la cancha abre de 9 a 22
Reservas (2 pedidos rechazados):
  domingo: 9h Ana 22h Bruno
--- reservas.txt ---
domingo 9 Ana
domingo 22 Bruno
```

##### Cancelar dos veces
```entrada
reservar viernes 10 Ana
cancelar viernes 10
cancelar viernes 10
```
```salida
Reservado: viernes 10h (Ana)
Cancelado: viernes 10h
No se pudo: no había reserva el viernes a las 10
Reservas (1 pedidos rechazados):
--- reservas.txt ---
```

### Prueba del sello

#### ¿Qué hace el constructor de `Mapa` si el nivel está mal? ¿Quién lo maneja?

Lanza `std::invalid_argument`; `main` la atrapa y termina con un mensaje.

#### ¿Por qué `direccion` devuelve `optional<Vec2>`?

Porque una tecla puede no ser una dirección (esperar), y eso es un resultado normal.

#### ¿Cómo sabe el Minotauro que puede embestir?

Si Lima está en su misma fila o columna, a 6 pasos o menos, y no hay paredes en el medio.

#### ¿Qué cambiaría para llevar este juego a una ventana con SDL3?

Solo la entrada (teclas de SDL) y el dibujo (dibujar en la ventana); el `Juego` quedaría igual.

#### ¿Por qué la carga de la partida valida cada campo?

Porque el archivo pudo editarse a mano o romperse; mejor un error claro que una partida imposible.

### Soluciones (docente)

Jefe final del camino principal. M1 reescribe `05-C++-Videojuegos/07-ProyectoMazmorra` con llave, puerta, poción, tres IA y validación con excepciones; se entrega como `.zip`. La secuencia de la entrada de ejemplo gana en 25 turnos.
