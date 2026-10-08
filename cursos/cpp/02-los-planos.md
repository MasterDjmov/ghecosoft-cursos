# RAMA R02 · Los Planos: clases y objetos

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Structs y clases

```meta
tipo: tema
padre: R01-N09
precio: 10
criatura: esqueleto
temas: col.registros, poo.clases
```

### Crónica

Después de vencer al Autómata, Tesla te lleva a la **Sala de los Planos**: miles de hojas colgadas, cada una con el dibujo de una pieza. Una torre, un reloj, un puente.

—Hasta ahora escribiste instrucciones sueltas —te dice—. Acá se dibujan **planos**: un plano dice qué datos tiene una cosa y qué sabe hacer. Con un plano, construís una torre o cien. En C++, el plano se llama **clase**, y cada torre construida es un **objeto**.

### Objetivos

Agrupar datos relacionados en un `struct`, crear vectores de structs, escribir
**métodos** (funciones dentro de la clase), usar `class` con datos privados y
métodos públicos, y marcar con `const` los métodos que no modifican el objeto.

### Antes de empezar

- Funciones, referencias y `const&` (rama 1).
- Vectores (Vectores: listas que crecen).

### Explicación

#### El problema: datos que van juntos
Una pieza del depósito tiene nombre, cantidad y precio. Con variables sueltas,
para 50 piezas harían falta 150 variables, o tres vectores "paralelos" que hay que
mantener sincronizados a mano. Un **`struct`** junta esos datos en un tipo nuevo:
```cpp
struct Pieza {
    std::string nombre;
    int cantidad = 0;        // valor por defecto
    double precio = 0.0;
};                           // ¡el ; del final!

Pieza engranaje{"engranaje", 12, 350.0};   // campo por campo, en orden
engranaje.cantidad += 3;                   // cada campo, con el punto
std::vector<Pieza> deposito;               // un vector de piezas
```
`Pieza` ahora es un tipo como `int`: podés declarar variables, pasarlas a funciones
(por `const Pieza&` si solo se leen) y guardarlas en vectores.

#### Métodos: funciones que viven en el tipo
Una función que trabaja con una pieza puede ir **dentro** del `struct`:
```cpp
struct Rectangulo {
    double ancho = 1.0;
    double alto = 1.0;

    double area() const { return ancho * alto; }
    void escalar(double f) { ancho *= f; alto *= f; }
};

Rectangulo puerta{2.0, 3.5};
puerta.area();        // se llama con el punto, sobre un objeto
puerta.escalar(2);
```
Dentro de un método, `ancho` y `alto` son **los del objeto sobre el que se llamó**:
`puerta.escalar(2)` cambia el ancho de `puerta`, no el de otro rectángulo.

#### Métodos `const`
Un `const` después de los paréntesis promete que el método **no modifica** el
objeto. El compilador lo hace cumplir, y además permite llamarlo sobre objetos
recibidos como `const&`. Regla: **todo método que solo consulta, lleva `const`**.

#### `class`: datos privados, métodos públicos
Con un `struct`, cualquiera puede escribir `torre.pisos = -5`. Una **clase** decide
qué se ve desde afuera:
```cpp
class Torre {
public:                       // lo que se usa desde afuera: la interfaz
    void construir_pisos(int n) { if (n > 0) pisos_ += n; }
    int pisos() const { return pisos_; }
private:                      // solo lo tocan los métodos de Torre
    int pisos_ = 1;
};
```
Así, la única forma de cambiar los pisos es `construir_pisos`, que no acepta
negativos. El guion bajo final (`pisos_`) es una convención para distinguir los
datos de la clase de los parámetros y variables locales.

#### `struct` o `class`
En C++ son casi lo mismo: la única diferencia es que en un `struct` todo es
público por defecto y en una `class`, privado. La costumbre:
- **`struct`** para datos simples sin reglas (una pieza, un punto, una fila de
  tabla);
- **`class`** cuando hay reglas que proteger (una cuenta con saldo, una torre con
  pisos válidos).

#### Clase y objeto
La **clase** es el plano; cada **objeto** es una cosa construida con ese plano, con
**sus propios** datos. `Torre norte; Torre reloj;` son dos torres independientes:
construir pisos en una no cambia la otra.

> **Si venís de C.** Un `struct` de C es solo datos y las funciones van afuera
> (`torre_construir(&t, 4)`). En C++ los métodos van adentro (`t.construir(4)`),
> no hace falta `typedef` para usar el nombre, y `private` impide romper las reglas.

### Código de ejemplo

```cpp
/*
 * Structs y clases: juntar datos, y despues juntar datos con sus funciones.
 */
#include <iostream>
#include <string>
#include <vector>

// 1) Un struct AGRUPA datos que van juntos.
struct Pieza {
    std::string nombre;
    int cantidad = 0;       // valor por defecto si no se da otro
    double precio = 0.0;
};

// Una funcion suelta que trabaja con una Pieza (por const&: no la copia).
double valor(const Pieza& p)
{
    return p.cantidad * p.precio;
}

// 2) Una clase junta los DATOS y las FUNCIONES que los usan (metodos).
class Torre {
public:
    // Metodos: funciones que viven dentro de la clase.
    void construir_pisos(int n)
    {
        if (n > 0) {
            pisos_ += n;
        }
    }

    int pisos() const          // const: promete no modificar la torre
    {
        return pisos_;
    }

    double altura() const
    {
        return pisos_ * 3.5;
    }

private:
    int pisos_ = 1;            // privado: solo lo tocan los metodos de Torre
};

int main()
{
    Pieza engranaje{"engranaje", 12, 350.0};   // inicializar campo por campo, en orden
    Pieza resorte;                              // usa los valores por defecto
    resorte.nombre = "resorte";
    resorte.cantidad = 40;
    resorte.precio = 25.5;

    std::cout << engranaje.nombre << ": $" << valor(engranaje) << "\n";
    std::cout << resorte.nombre << ": $" << valor(resorte) << "\n";

    // Un vector de structs
    std::vector<Pieza> deposito = {engranaje, resorte, {"remache", 200, 3.0}};
    double total = 0;
    for (const Pieza& p : deposito) {
        total += valor(p);
    }
    std::cout << "Valor del depósito: $" << total << "\n";

    // Objetos de una clase: cada uno con sus propios datos
    Torre norte;
    Torre reloj;
    norte.construir_pisos(4);
    reloj.construir_pisos(9);
    reloj.construir_pisos(-3);                  // el metodo lo ignora
    std::cout << "Norte: " << norte.pisos() << " pisos, " << norte.altura() << " m\n";
    std::cout << "Reloj: " << reloj.pisos() << " pisos, " << reloj.altura() << " m\n";
    // reloj.pisos_ = 100;   // ERROR: pisos_ es privado
    return 0;
}
```

### Salida esperada

```
engranaje: $4200
resorte: $1020
Valor del depósito: $5820
Norte: 5 pisos, 17.5 m
Reloj: 10 pisos, 35 m
```

### ¿Para qué sirve?

Todo sistema modela cosas del mundo: un `Producto`, un `Cliente`, una `Factura`, un `Jugador`, un `Enemigo`, un `Turno`. Los structs representan los registros de una planilla o de una base de datos; las clases, las cosas que tienen reglas (una cuenta que no puede quedar en negativo, un turno que no puede tener fecha pasada). Es la base de la programación orientada a objetos, que usan casi todos los programas grandes.

### Errores habituales

**Slime: el `;` después de la llave de cierre.**
```
main.cpp:1:31: error: expected ‘;’ after class definition
```

**Esqueleto: tocar algo privado desde afuera.**
```
main.cpp:2:21: error: ‘int Torre::pisos_’ is private within this context
main.cpp:2:21: note: field ‘int Torre::pisos_’ can be accessed via ‘int Torre::pisos() const’
```
`g++` hasta sugiere el método que lo lee.

**Goblin: un método `const` que modifica.**
```
main.cpp:1:61: error: increment of member ‘Torre::pisos_’ in read-only object
```

**Goblin: llamar a un método no `const` sobre un objeto `const`.**
```
main.cpp:2:32: error: passing ‘const Torre’ as ‘this’ argument discards qualifiers [-fpermissive]
```
Pasa cuando una función recibe `const Torre&` y llama a un método al que le falta
el `const`. Si el método solo consulta, agregale `const`.

**Ogro: modificar una copia.** `for (Pieza p : deposito) p.cantidad = 0;` pone en
cero **copias**. Para modificar, `for (Pieza& p : deposito)`.

### Misión R02-N01-M1 · El inventario de piezas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé piezas hasta que se termine la entrada, cada una como `nombre cantidad
precio`, y guardalas en un `std::vector<Pieza>`. Mostrá cada pieza con su valor
(`cantidad * precio`, calculado por una función `valor(const Pieza&)`), el total,
la pieza más cara (por precio unitario) y las que tienen menos de 10 unidades.

#### Criterio de aprobación

- Define `struct Pieza` con valores por defecto.
- Guarda las piezas en un vector y las recorre.
- `valor` recibe la pieza por `const&`.

#### Entrada de ejemplo

```
engranaje 12 350
resorte 40 25.5
valvula 6 1200
remache 200 3
manometro 2 8400
```

#### Salida esperada

```
engranaje: 12 x $350 = $4200
resorte: 40 x $25.5 = $1020
valvula: 6 x $1200 = $7200
remache: 200 x $3 = $600
manometro: 2 x $8400 = $16800
Total: $29820
La pieza más cara: manometro
Con poco stock (menos de 10): valvula manometro
```

#### Solución de referencia

```cpp
// Mision 1 - El inventario de piezas: un vector de structs.
#include <iostream>
#include <string>
#include <vector>

struct Pieza {
    std::string nombre;
    int cantidad = 0;
    double precio = 0.0;
};

double valor(const Pieza& p)
{
    return p.cantidad * p.precio;
}

int main()
{
    std::vector<Pieza> piezas;
    Pieza p;
    while (std::cin >> p.nombre >> p.cantidad >> p.precio) {
        piezas.push_back(p);
    }
    if (piezas.empty()) {
        std::cout << "Depósito vacío.\n";
        return 0;
    }
    double total = 0;
    std::size_t cara = 0;
    for (std::size_t i = 0; i < piezas.size(); i++) {
        std::cout << piezas[i].nombre << ": " << piezas[i].cantidad << " x $" << piezas[i].precio
                  << " = $" << valor(piezas[i]) << "\n";
        total += valor(piezas[i]);
        if (piezas[i].precio > piezas[cara].precio) {
            cara = i;
        }
    }
    std::cout << "Total: $" << total << "\n";
    std::cout << "La pieza más cara: " << piezas[cara].nombre << "\n";
    std::cout << "Con poco stock (menos de 10):";
    for (const Pieza& x : piezas) {
        if (x.cantidad < 10) {
            std::cout << " " << x.nombre;
        }
    }
    std::cout << "\n";
    return 0;
}
```

#### Pruebas

##### Una sola pieza
```entrada
tornillo 500 1.5
```
```salida
tornillo: 500 x $1.5 = $750
Total: $750
La pieza más cara: tornillo
Con poco stock (menos de 10):
```

##### Nada con poco stock
```entrada
perno 10 100
arandela 50 2
```
```salida
perno: 10 x $100 = $1000
arandela: 50 x $2 = $100
Total: $1100
La pieza más cara: perno
Con poco stock (menos de 10):
```

### Misión R02-N01-M2 · El rectángulo del plano

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `struct Rectangulo` con `ancho` y `alto` (por defecto 1) y los métodos
`area()`, `perimetro()`, `es_cuadrado()` (todos `const`) y `escalar(factor)`.
Escribí `informe(const Rectangulo&)`. Probá con una puerta de 2 × 3.5 y una baldosa
por defecto; escalá la puerta ×2 y la baldosa ×0.5.

#### Criterio de aprobación

- Los métodos que consultan son `const`.
- `informe` recibe `const Rectangulo&` (por eso necesita los `const`).

#### Salida esperada

```
2 x 3.5: área 7, perímetro 11
1 x 1: área 1, perímetro 4 (cuadrado)
4 x 7: área 28, perímetro 22
0.5 x 0.5: área 0.25, perímetro 2 (cuadrado)
```

#### Solución de referencia

```cpp
// Mision 2 - El rectangulo del plano: metodos dentro de un struct.
#include <iostream>

struct Rectangulo {
    double ancho = 1.0;
    double alto = 1.0;

    double area() const
    {
        return ancho * alto;
    }

    double perimetro() const
    {
        return 2 * (ancho + alto);
    }

    bool es_cuadrado() const
    {
        return ancho == alto;
    }

    void escalar(double factor)
    {
        ancho *= factor;
        alto *= factor;
    }
};

void informe(const Rectangulo& r)
{
    std::cout << r.ancho << " x " << r.alto << ": área " << r.area() << ", perímetro " << r.perimetro()
              << (r.es_cuadrado() ? " (cuadrado)" : "") << "\n";
}

int main()
{
    Rectangulo puerta{2.0, 3.5};
    Rectangulo baldosa;
    informe(puerta);
    informe(baldosa);
    puerta.escalar(2);
    informe(puerta);
    baldosa.escalar(0.5);
    informe(baldosa);
    return 0;
}
```

### Misión R02-N01-M3 · El contador de la puerta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Contador` con dos datos **privados**: cuántas personas hay adentro y
cuántas entraron en total. Métodos: `entrar()`, `salir()` (si no hay nadie, no hace
nada), `dentro()` y `total()`. La entrada es una secuencia de `e` (entra) y `s`
(sale); al final mostrá los dos números.

#### Criterio de aprobación

- Los datos son `private` y terminan en `_`.
- `salir` nunca deja el contador en negativo.
- Los getters son `const`.

#### Entrada de ejemplo

```
e e s e s s s e e
```

#### Salida esperada

```
Adentro: 2
Entraron en total: 5
```

#### Solución de referencia

```cpp
// Mision 3 - El contador de visitantes: una clase con datos privados.
#include <iostream>

class Contador {
public:
    void entrar()
    {
        dentro_++;
        total_++;
    }

    void salir()
    {
        if (dentro_ > 0) {
            dentro_--;
        }
    }

    int dentro() const
    {
        return dentro_;
    }

    int total() const
    {
        return total_;
    }

private:
    int dentro_ = 0;
    int total_ = 0;
};

int main()
{
    Contador puerta;
    char c = ' ';
    while (std::cin >> c) {
        if (c == 'e') {
            puerta.entrar();
        } else if (c == 's') {
            puerta.salir();
        }
    }
    std::cout << "Adentro: " << puerta.dentro() << "\n";
    std::cout << "Entraron en total: " << puerta.total() << "\n";
    return 0;
}
```

#### Pruebas

##### Sale con nadie adentro
```entrada
s s e s s
```
```salida
Adentro: 0
Entraron en total: 1
```

##### Solo entradas
```entrada
e e e e
```
```salida
Adentro: 4
Entraron en total: 4
```

##### Sin movimientos
```entrada
```
```salida
Adentro: 0
Entraron en total: 0
```

### Encargo R02-N01-E1 · Las notas de la escuela

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Cada línea de la entrada trae un alumno: `nombre cantidad nota1 nota2 …`. Escribí
`struct Alumno` con el nombre, un `std::vector<int>` de notas y un método
`promedio() const` (0 si no tiene notas). Mostrá cada alumno con su promedio y si
está aprobado (6 o más) o a recuperar, y quién tiene el mejor promedio.

#### Criterio de aprobación

- El struct tiene un vector adentro y un método `const`.
- Lee una cantidad variable de notas por alumno.

#### Entrada de ejemplo

```
Ana 3 8 9 7
Bruno 2 4 6
Celi 4 10 9 8 10
Dami 1 5
```

#### Salida esperada

```
Ana: 8 aprobado
Bruno: 5 a recuperar
Celi: 9.25 aprobado
Dami: 5 a recuperar
Mejor promedio: Celi
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Las notas de la escuela: struct con un vector adentro.
#include <iostream>
#include <string>
#include <vector>

struct Alumno {
    std::string nombre;
    std::vector<int> notas;

    double promedio() const
    {
        if (notas.empty()) {
            return 0;
        }
        int suma = 0;
        for (int n : notas) {
            suma += n;
        }
        return static_cast<double>(suma) / notas.size();
    }
};

int main()
{
    std::vector<Alumno> curso;
    std::string nombre;
    int cantidad = 0;
    while (std::cin >> nombre >> cantidad) {
        Alumno a;
        a.nombre = nombre;
        for (int i = 0; i < cantidad; i++) {
            int nota = 0;
            std::cin >> nota;
            a.notas.push_back(nota);
        }
        curso.push_back(a);
    }
    std::size_t mejor = 0;
    for (std::size_t i = 0; i < curso.size(); i++) {
        std::cout << curso[i].nombre << ": " << curso[i].promedio()
                  << (curso[i].promedio() >= 6 ? " aprobado" : " a recuperar") << "\n";
        if (curso[i].promedio() > curso[mejor].promedio()) {
            mejor = i;
        }
    }
    if (!curso.empty()) {
        std::cout << "Mejor promedio: " << curso[mejor].nombre << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Alumno sin notas
```entrada
Eva 0
Fede 2 6 6
```
```salida
Eva: 0 a recuperar
Fede: 6 aprobado
Mejor promedio: Fede
```

##### Uno solo
```entrada
Gabi 3 10 10 9
```
```salida
Gabi: 9.66667 aprobado
Mejor promedio: Gabi
```

### Prueba del sello

#### ¿Qué diferencia hay entre `struct` y `class` en C++?

Solo el acceso por defecto: público en `struct`, privado en `class`. Por costumbre, `struct` para datos simples y `class` cuando hay reglas.

#### ¿Qué es un método? ¿Cómo se llama?

Una función que pertenece a la clase; se llama sobre un objeto con el punto: `torre.pisos()`.

#### ¿Qué significa el `const` en `int pisos() const`?

Que el método no modifica el objeto. Permite llamarlo sobre objetos `const`.

#### Si `Torre a, b;` y hacés `a.construir_pisos(3)`, ¿cambia `b`?

No: cada objeto tiene sus propios datos.

#### ¿Para qué sirve hacer `private` un dato?

Para que solo lo modifiquen los métodos de la clase, que respetan las reglas.

### Soluciones (docente)

Material original: `03-C++/05-StructVsClass`, rehecho desde cero: primero `struct` como agrupador de datos, después métodos y recién ahí `class`.

## R02-N02 · Constructores y destructores

```meta
tipo: tema
padre: R02-N01
precio: 10
criatura: troll
temas: poo.constructores
```

### Crónica

En la línea de ensamblaje, cada autómata sale de la máquina ya armado, con la batería cargada y su nombre grabado. Nunca sale uno a medias.

—Un objeto a medio construir es un peligro —dice {mentor}—. Por eso cada plano trae un **ritual de nacimiento**, el constructor, que lo deja listo para trabajar. Y un **ritual de despedida**, el destructor, que ordena todo cuando se apaga.

### Objetivos

Escribir **constructores** que dejan cada objeto en un estado válido desde que
nace, con lista de inicialización, sobrecarga y delegación; entender `explicit`;
escribir **destructores** y predecir cuándo corren; crear y borrar objetos con
`new` y `delete`; usar el puntero `this`; y conocer los miembros `static`,
compartidos por todos los objetos de una clase.

### Antes de empezar

- Clases, datos privados y métodos (Structs y clases).

### Explicación

#### El constructor
Es un método especial que **se llama igual que la clase**, no devuelve nada (ni
`void`) y corre **automáticamente** al crear el objeto:
```cpp
class Automata {
public:
    Automata(const std::string& nombre, int energia)
        : nombre_(nombre), energia_(energia), energia_max_(energia)   // lista de inicialización
    {
        // cuerpo: lo que haga falta después de inicializar
    }
private:
    std::string nombre_;
    int energia_;
    int energia_max_;
};

Automata guardian("Guardián", 80);    // corre el constructor
Automata otro{"Otro", 50};            // lo mismo, con llaves
```
Si una clase tiene constructor con parámetros, **no se puede** crear un objeto sin
pasarlos: el compilador te obliga a darle lo que necesita para nacer bien.

#### La lista de inicialización
Lo que va después de los `:` inicializa cada miembro **antes** de entrar al cuerpo.
Es la forma correcta:
- inicializa directamente (asignar en el cuerpo sería "crear vacío y después
  cambiar");
- es **obligatoria** para miembros `const` y referencias;
- los miembros se inicializan en el **orden en que están declarados** en la clase,
  no en el de la lista. Escribilos en el mismo orden (`-Wall` avisa si no).

#### Valores por defecto en los miembros
```cpp
class Contador {
    int dentro_ = 0;     // si el constructor no dice otra cosa, vale 0
};
```

#### Varios constructores
Como cualquier función, el constructor se puede **sobrecargar**. Y uno puede
**delegar** en otro para no repetir código:
```cpp
Color() : Color(128, 128, 128) {}             // sin parámetros: gris medio
explicit Color(int gris) : Color(gris, gris, gris) {}
Color(int r, int g, int b) : r_(r), g_(g), b_(b) {}
```
El constructor **sin parámetros** (el "por defecto") es el que corre en
`Color c;`. Si no escribís ninguno, C++ genera uno que no hace nada especial; si
escribís otro, deja de generarlo (y podés pedirlo con `Color() = default;`).

#### `explicit`
Un constructor de **un** parámetro sirve, sin querer, para convertir: con
`Color(int gris)`, la línea `Color c = 40;` compila y crea un gris. Casi nunca se
quiere eso. `explicit` lo prohíbe y obliga a escribir `Color c(40);`. Regla:
**los constructores de un parámetro llevan `explicit`**.

#### El destructor
Se llama `~` + el nombre de la clase, no recibe nada y corre **solo** cuando el
objeto deja de existir:
```cpp
~Automata() { std::cout << "se apaga " << nombre_ << "\n"; }
```
¿Cuándo deja de existir un objeto? Cuando termina **el bloque `{ }` donde se
declaró**: al final de la función, del `if`, de cada vuelta de un bucle. Y los
objetos de un mismo bloque se destruyen **al revés** de como se crearon (el último
en nacer es el primero en irse).

Casi nunca vas a escribir un destructor para imprimir: su uso real es **liberar
recursos** (cerrar un archivo, devolver memoria, soltar una conexión). Esa idea,
"lo que se adquiere en el constructor se libera en el destructor", se llama
**RAII** y la vas a ver a fondo en la rama 3.

#### `new` y `delete`: objetos que viven hasta que los borrás
Hasta ahora cada objeto vive en su bloque (en la **pila**). Con `new` se crea un objeto en el **montón** (*heap*): no muere al terminar el bloque, sino cuando alguien hace `delete`:
```cpp
Automata* a = new Automata("Cucu", 3);   // corre el constructor; a apunta al objeto
a->trabajar();                           // con un puntero se usa -> en vez de .
delete a;                                // corre el destructor y devuelve la memoria
a = nullptr;                             // que no quede apuntando a algo que ya no existe

int* numeros = new int[10];              // un arreglo en el montón
delete[] numeros;                        // los arreglos, con delete[]
```
Es lo que en C eran `malloc` y `free`, con una diferencia importante: `new` **llama al constructor** y `delete` **al destructor**.

Las trampas son las mismas de C:
- Olvidar el `delete`: la memoria queda ocupada hasta que termina el programa (una **fuga**).
- Hacer `delete` dos veces, o usar el objeto después del `delete`: comportamiento indefinido.
- Mezclar: `new[]` va con `delete[]`, y `new` con `delete`.

Por eso el C++ de hoy casi no escribe `delete` a mano: en la rama 3 vas a ver los **punteros inteligentes** (`std::unique_ptr`), que hacen el `delete` solos en su destructor. Pero tenés que saber qué hacen por dentro, y en los parciales y el código viejo vas a ver mucho `new` y `delete`.

#### El puntero `this`
Adentro de un método, `this` es un **puntero al objeto sobre el que se llamó**: en `a.trabajar()`, `this` apunta a `a`. Casi nunca hace falta escribirlo (`nombre_` ya es `this->nombre_`), salvo:
- cuando un parámetro se llama igual que un dato: `this->vida = vida;`;
- para devolver el objeto mismo y encadenar: `return *this;` (lo vas a ver en los operadores).

#### Miembros `static`: uno para todos
Un dato `static` no pertenece a cada objeto sino **a la clase**: hay uno solo,
compartido. Sirve, por ejemplo, para numerar objetos:
```cpp
class Turno {
    inline static int siguiente_ = 1;   // uno solo para todos los turnos
    int numero_;
public:
    Turno() : numero_(siguiente_++) {}
    static int entregados() { return siguiente_ - 1; }   // se llama Turno::entregados()
};
```
Un método `static` no trabaja sobre un objeto (no tiene `this`) y solo ve los
datos `static`.

> **Si venís de C.** En C, uno creaba el struct y después llamaba a
> `automata_init(&a, ...)` si se acordaba, y a `automata_liberar(&a)` al final.
> En C++ las dos cosas pasan solas.

### Código de ejemplo

```cpp
/*
 * Constructores y destructores: nacer en un estado valido y limpiar al morir.
 */
#include <iostream>
#include <string>

class Automata {
public:
    // Constructor con LISTA DE INICIALIZACION: los miembros se inicializan antes del cuerpo.
    Automata(const std::string& nombre, int energia)
        : nombre_(nombre), energia_(energia), energia_max_(energia)
    {
        std::cout << "  [se enciende " << nombre_ << " con " << energia_ << " de energía]\n";
    }

    // Otro constructor (sobrecarga): solo el nombre, energia 100.
    explicit Automata(const std::string& nombre)
        : Automata(nombre, 100)          // delega en el otro constructor
    {
    }

    // Destructor: corre solo cuando el objeto deja de existir.
    ~Automata()
    {
        std::cout << "  [se apaga " << nombre_ << "]\n";
    }

    void trabajar(int costo)
    {
        energia_ -= costo;
        if (energia_ < 0) {
            energia_ = 0;
        }
    }

    void estado() const
    {
        std::cout << "  " << nombre_ << ": " << energia_ << "/" << energia_max_ << "\n";
    }

private:
    std::string nombre_;
    int energia_;
    int energia_max_;
};

int main()
{
    std::cout << "Entrando a main\n";
    Automata guardian("Guardián", 80);      // aca corre el constructor
    guardian.trabajar(30);
    guardian.estado();

    {
        std::cout << "Entrando al taller\n";
        Automata ayudante("Ayudante");      // el constructor de un argumento
        Automata limpiador("Limpiador", 20);
        ayudante.estado();
        std::cout << "Saliendo del taller\n";
    }   // aca se destruyen limpiador y ayudante: al reves de como nacieron

    std::cout << "De vuelta en main\n";
    return 0;
}   // aca se destruye guardian
```

### Salida esperada

```
Entrando a main
  [se enciende Guardián con 80 de energía]
  Guardián: 50/80
Entrando al taller
  [se enciende Ayudante con 100 de energía]
  [se enciende Limpiador con 20 de energía]
  Ayudante: 100/100
Saliendo del taller
  [se apaga Limpiador]
  [se apaga Ayudante]
De vuelta en main
  [se apaga Guardián]
```

### ¿Para qué sirve?

Los constructores garantizan que no exista un `Pedido` sin cliente ni una `Fecha` con el mes 13: si el objeto existe, es válido. Los destructores están detrás de todo lo que se "cierra solo" en C++: archivos que se cierran al terminar la función, conexiones a bases de datos que se liberan, candados de concurrencia que se sueltan. Los contadores `static` numeran facturas, turnos o identificadores únicos.

### Errores habituales

**Esqueleto: crear un objeto sin darle lo que necesita.**
```
main.cpp:3:16: error: no matching function for call to ‘Automata::Automata()’
main.cpp:2:19: note: candidate: ‘Automata::Automata(const std::string&, int)’
main.cpp:2:19: note:   candidate expects 2 arguments, 0 provided
```

**Ogro: el orden de la lista de inicialización.** Si `vida_` se declaró antes que
`vida_max_`, esto usa `vida_max_` **antes** de inicializarlo:
```cpp
P(int v) : vida_max_(v), vida_(vida_max_) {}
```
```
main.cpp:2:79: warning: ‘P::vida_max_’ will be initialized after [-Wreorder]
main.cpp:2:68: warning:   ‘int P::vida_’ [-Wreorder]
```

**Goblin: conversión implícita por falta de `explicit`.** Sin `explicit`,
`mostrar(40)` puede construir un `Color` sin que lo notes. Con `explicit`:
```
main.cpp:4:49: error: conversion from ‘int’ to non-scalar type ‘Color’ requested
```

**Ogro: "la función más molesta".** `Automata a();` **no** crea un objeto: declara
una función que devuelve un `Automata`. Para el constructor sin parámetros:
`Automata a;` o `Automata a{};`.

**Troll: guardar una referencia a algo que se destruye.** Un objeto que guarda
`const std::string&` a un texto temporal se queda con una referencia colgante
cuando el temporal muere. Guardá una copia (`std::string`).

### Misión R02-N02-M1 · El reloj de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Reloj` que guarda solo los **minutos desde la medianoche** (0 a
1439). El constructor recibe horas y minutos cualesquiera (incluso `23, 150` o
`0, -15`) y los normaliza. `avanzar(minutos)` acepta negativos. `mostrar()`
imprime `HH:MM` con ceros adelante.

Pista: `((x % 1440) + 1440) % 1440` deja cualquier entero entre 0 y 1439.

#### Criterio de aprobación

- El constructor deja el reloj siempre en un estado válido.
- Guarda un solo dato privado.
- Maneja minutos negativos.

#### Salida esperada

```
09:45
10:15
01:30
23:45
23:45
```

#### Solución de referencia

```cpp
// Mision 1 - El reloj de la torre: un constructor que normaliza.
#include <iostream>

class Reloj {
public:
    Reloj(int horas, int minutos)
        : minutos_totales_(0)
    {
        avanzar(horas * 60 + minutos);
    }

    void avanzar(int minutos)
    {
        minutos_totales_ = ((minutos_totales_ + minutos) % 1440 + 1440) % 1440;
    }

    void mostrar() const
    {
        int h = minutos_totales_ / 60;
        int m = minutos_totales_ % 60;
        std::cout << (h < 10 ? "0" : "") << h << ":" << (m < 10 ? "0" : "") << m << "\n";
    }

private:
    int minutos_totales_;
};

int main()
{
    Reloj a(9, 45);
    a.mostrar();
    a.avanzar(30);
    a.mostrar();
    Reloj b(23, 150);          // 23 h + 150 min = 01:30 del dia siguiente
    b.mostrar();
    Reloj c(0, -15);           // 15 minutos antes de la medianoche
    c.mostrar();
    c.avanzar(-1440 * 3);      // tres dias para atras: la misma hora
    c.mostrar();
    return 0;
}
```

### Misión R02-N02-M2 · Los colores del vitral

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Color` con tres constructores: sin parámetros (gris 128), con un
nivel de gris (`explicit`) y con `r, g, b`. Los dos primeros **delegan** en el
tercero, que recorta cada valor a 0..255 con `std::clamp`. Agregá `mostrar()` y
`mezclar(const Color&)`, que devuelve un color nuevo con el promedio de cada canal.

#### Criterio de aprobación

- Hay tres constructores y dos delegan en el tercero.
- El de un parámetro es `explicit`.
- Los valores fuera de rango se recortan en la lista de inicialización.

#### Salida esperada

```
rgb(128, 128, 128)
rgb(40, 40, 40)
rgb(184, 115, 51)
rgb(255, 0, 90)
rgb(112, 77, 45)
```

#### Solución de referencia

```cpp
// Mision 2 - Los colores del vitral: varios constructores.
#include <algorithm>
#include <iostream>

class Color {
public:
    Color() : Color(128, 128, 128) {}                    // gris medio
    explicit Color(int gris) : Color(gris, gris, gris) {}
    Color(int r, int g, int b)
        : r_(std::clamp(r, 0, 255)), g_(std::clamp(g, 0, 255)), b_(std::clamp(b, 0, 255))
    {
    }

    void mostrar() const
    {
        std::cout << "rgb(" << r_ << ", " << g_ << ", " << b_ << ")\n";
    }

    Color mezclar(const Color& otro) const
    {
        return Color((r_ + otro.r_) / 2, (g_ + otro.g_) / 2, (b_ + otro.b_) / 2);
    }

private:
    int r_;
    int g_;
    int b_;
};

int main()
{
    Color gris;
    Color oscuro(40);
    Color cobre(184, 115, 51);
    Color fuera(300, -20, 90);
    gris.mostrar();
    oscuro.mostrar();
    cobre.mostrar();
    fuera.mostrar();
    cobre.mezclar(oscuro).mostrar();
    return 0;
}
```

### Misión R02-N02-M3 · La guardia de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Guardia` cuyo constructor muestra `entra <nombre>` y cuyo destructor
muestra `sale <nombre>`. Armá este `main` (y la función `ronda`), **predecí en un
papel** qué va a mostrar y después comprobalo:
```cpp
void ronda() { Guardia g("Ronda"); std::cout << "(ronda por las murallas)\n"; }

int main()
{
    Guardia a("Capitana");
    {
        Guardia b("Vigía");
        Guardia c("Aprendiz");
        ronda();
    }
    for (int i = 1; i <= 2; i++) {
        Guardia t("Turno " + std::to_string(i));
    }
    std::cout << "fin de main\n";
}
```

#### Criterio de aprobación

- El constructor es `explicit` y usa lista de inicialización.
- La salida coincide con la esperada (y la predijiste antes).

#### Salida esperada

```
entra Capitana
entra Vigía
entra Aprendiz
entra Ronda
(ronda por las murallas)
sale Ronda
sale Aprendiz
sale Vigía
entra Turno 1
sale Turno 1
entra Turno 2
sale Turno 2
fin de main
sale Capitana
```

#### Solución de referencia

```cpp
// Mision 3 - La guardia de la torre: el orden de constructores y destructores.
#include <iostream>
#include <string>

class Guardia {
public:
    explicit Guardia(const std::string& nombre) : nombre_(nombre)
    {
        std::cout << "entra " << nombre_ << "\n";
    }

    ~Guardia()
    {
        std::cout << "sale " << nombre_ << "\n";
    }

private:
    std::string nombre_;
};

void ronda()
{
    Guardia g("Ronda");
    std::cout << "(ronda por las murallas)\n";
}

int main()
{
    Guardia a("Capitana");
    {
        Guardia b("Vigía");
        Guardia c("Aprendiz");
        ronda();
    }
    for (int i = 1; i <= 2; i++) {
        Guardia t("Turno " + std::to_string(i));
    }
    std::cout << "fin de main\n";
    return 0;
}
```

### Encargo R02-N02-E1 · El turnero de la carnicería

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Escribí `class Turno` que se numera sola: el primer turno creado es el 1, el
segundo el 2… usando un contador `static`. Cada línea de la entrada es el nombre de
un cliente: creá su turno y anuncialo. Al final, mostrá cuántos turnos se
entregaron con un método `static`.

#### Criterio de aprobación

- El número sale de un miembro `inline static`.
- `entregados()` es un método `static` que se llama con `Turno::`.

#### Entrada de ejemplo

```
Ana
Bruno
Celi
Dami
```

#### Salida esperada

```
Turno 1: Ana
Turno 2: Bruno
Turno 3: Celi
Turno 4: Dami
Turnos entregados: 4
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El turnero de la carniceria: un contador compartido (static).
#include <iostream>
#include <string>

class Turno {
public:
    explicit Turno(const std::string& cliente)
        : numero_(siguiente_++), cliente_(cliente)
    {
    }

    void anunciar() const
    {
        std::cout << "Turno " << numero_ << ": " << cliente_ << "\n";
    }

    static int entregados()
    {
        return siguiente_ - 1;
    }

private:
    inline static int siguiente_ = 1;   // uno solo, compartido por todos los turnos
    int numero_;
    std::string cliente_;
};

int main()
{
    std::string nombre;
    while (std::cin >> nombre) {
        Turno t(nombre);
        t.anunciar();
    }
    std::cout << "Turnos entregados: " << Turno::entregados() << "\n";
    return 0;
}
```

#### Pruebas

##### Un cliente
```entrada
Ana
```
```salida
Turno 1: Ana
Turnos entregados: 1
```

##### Nadie
```entrada
```
```salida
Turnos entregados: 0
```

### Prueba del sello

#### ¿Qué diferencia hay entre `Automata a("Cucu", 3);` y `new Automata("Cucu", 3)`?

El primero vive hasta que termina su bloque; el segundo vive en el montón hasta que alguien hace `delete`.

#### ¿Con qué se libera `new int[10]`?

Con `delete[]`.

#### ¿Qué es `this`?

Un puntero al objeto sobre el que se llamó el método.

#### ¿Cuándo corre el constructor? ¿Y el destructor?

El constructor, al crear el objeto; el destructor, cuando el objeto deja de existir (al terminar su bloque).

#### En un mismo bloque se crean `a`, `b` y `c`. ¿En qué orden se destruyen?

Al revés: `c`, `b`, `a`.

#### ¿Por qué conviene la lista de inicialización en vez de asignar en el cuerpo?

Porque inicializa directamente, es obligatoria para `const` y referencias, y deja el objeto listo antes de ejecutar el cuerpo.

#### ¿Para qué sirve `explicit` en un constructor de un parámetro?

Para prohibir que se use como conversión automática (`Color c = 40;`).

#### ¿Qué tiene de especial un dato `static`?

Hay uno solo, compartido por todos los objetos de la clase.

### Soluciones (docente)

Material original: `03-C++/06-Constructores`, ampliado con delegación, `explicit` y `static`.

## R02-N03 · Encapsulamiento

```meta
tipo: tema
padre: R02-N02
precio: 10
criatura: ogro
temas: poo.encapsulamiento
```

### Crónica

Un aprendiz entra corriendo: alguien cambió a mano la presión de la caldera principal y el manómetro marca un número imposible. Tesla ni se inmuta.

—Por eso la presión no se toca a mano —dice, y te muestra un panel con solo tres palancas—. Se sube, se baja o se purga. Nada más. Si la única forma de cambiar algo respeta las reglas, **nunca** se rompen. Eso es encapsular.

### Objetivos

Diseñar clases que protegen sus **invariantes** (reglas que siempre se cumplen):
datos privados, métodos con nombre de acción que validan, getters de solo lectura,
métodos que avisan si una acción no se pudo hacer, y helpers privados.

### Antes de empezar

- Clases y constructores (nodos anteriores).

### Explicación

#### Invariantes
Una **invariante** es una regla que tiene que cumplirse **siempre**, desde que el
objeto nace hasta que muere:
- una cuenta nunca tiene saldo negativo;
- una fracción nunca tiene denominador 0;
- la vida está entre 0 y el máximo.

Si los datos fueran públicos, cualquier línea del programa (de las miles que tiene)
podría romper la regla. Si son privados, **solo los métodos de la clase** los
tocan, y basta con que esos pocos métodos la respeten. Encapsular no es "esconder
por esconder": es **reducir los lugares donde algo puede salir mal**.

#### El constructor establece la invariante…
…y cada método público la **mantiene**. Si el constructor puede recibir datos
inválidos, los corrige o los rechaza (`den == 0 ? 1 : den`).

#### Métodos con nombre de acción, no setters crudos
```cpp
void set_vida(int v);            // cualquiera pone cualquier cosa
void curar(int n);               // una acción del mundo, con sus reglas
void recibir_dano(int n);
```
No todo dato necesita un *setter*. La mayoría cambia por **acciones**: se deposita,
se extrae, se cura, se reserva. Cada acción valida lo suyo.

#### Getters: leer sin dar permiso de escribir
```cpp
int vida() const { return vida_; }
```
Un getter `const` devuelve una copia del valor: quien lo llama puede leerlo, pero no
cambiarlo. Para datos grandes (un texto, un vector), se devuelve
`const std::string&` para no copiarlo.

#### Cuando una acción no se puede hacer
Un método puede devolver `bool` para avisar si hizo lo pedido:
```cpp
bool gastar_mana(int n)
{
    if (n > mana_) return false;   // no alcanza: no pasa nada
    mana_ -= n;
    return true;
}
```
Quien lo llama decide qué hacer (`if (!maga.gastar_mana(30)) ...`). En la rama 5
vas a ver otra forma de avisar errores: las **excepciones**.

#### Helpers privados
Las funciones auxiliares que solo usa la clase (normalizar, recortar, validar) van
en `private`. Si mañana cambian, nadie de afuera se entera.

#### ¿Cómo sé si mi clase está bien encapsulada?
Probá escribir, desde `main`, una línea que rompa la regla. Si **no compila**, está
bien encapsulada.

> **Si venís de C.** En C la regla dependía de que todos llamaran a la función
> correcta; nada impedía escribir `cuenta.saldo = -500`. En C++ el compilador lo
> impide.

### Código de ejemplo

```cpp
/*
 * Encapsulamiento: la clase protege sus reglas (invariantes).
 *   Invariantes de Vitalidad:  0 <= vida <= vida_max   y   0 <= mana <= mana_max
 */
#include <algorithm>
#include <iostream>

class Vitalidad {
public:
    Vitalidad(int vida_max, int mana_max)
        : vida_(vida_max), vida_max_(vida_max), mana_(mana_max), mana_max_(mana_max)
    {
    }

    // Acciones con nombre del dominio: mejor que setters crudos.
    void curar(int n)
    {
        vida_ = ajustar(vida_ + n, vida_max_);
    }

    void recibir_dano(int n)
    {
        vida_ = ajustar(vida_ - n, vida_max_);
    }

    // Si no alcanza, la accion NO ocurre y el que llama se entera.
    bool gastar_mana(int n)
    {
        if (n < 0 || n > mana_) {
            return false;
        }
        mana_ -= n;
        return true;
    }

    // Getters: lectura sin permiso de escritura.
    int vida() const { return vida_; }
    int mana() const { return mana_; }
    bool vivo() const { return vida_ > 0; }

private:
    // Helper privado: detalle interno, nadie de afuera lo usa.
    static int ajustar(int valor, int maximo)
    {
        return std::clamp(valor, 0, maximo);
    }

    int vida_;
    int vida_max_;
    int mana_;
    int mana_max_;
};

int main()
{
    Vitalidad maga(80, 50);
    std::cout << "Inicio: vida " << maga.vida() << ", maná " << maga.mana() << "\n";

    maga.recibir_dano(100);
    std::cout << "Tras 100 de daño: vida " << maga.vida() << " (no baja de 0)\n";

    maga.curar(1000);
    std::cout << "Tras curar 1000: vida " << maga.vida() << " (tope en el máximo)\n";

    if (maga.gastar_mana(30)) {
        std::cout << "Lanza un hechizo. Maná restante: " << maga.mana() << "\n";
    }
    if (!maga.gastar_mana(30)) {
        std::cout << "No puede lanzar otro: maná insuficiente (" << maga.mana() << ")\n";
    }
    // maga.vida_ = 999;   // ERROR: vida_ es privada. La regla no se puede saltear.
    return 0;
}
```

### Salida esperada

```
Inicio: vida 80, maná 50
Tras 100 de daño: vida 0 (no baja de 0)
Tras curar 1000: vida 80 (tope en el máximo)
Lanza un hechizo. Maná restante: 20
No puede lanzar otro: maná insuficiente (20)
```

### ¿Para qué sirve?

Una clase bien encapsulada se puede usar sin miedo: una `Cuenta` que no acepta extracciones sin saldo, un `Carrito` que no deja cantidades negativas, un `Calendario` que no permite turnos superpuestos, un `Stock` que no sobrevende. En equipos grandes es fundamental: quien usa tu clase no puede romperla aunque quiera, y vos podés cambiar cómo está hecha por dentro sin romper el código de los demás.

### Errores habituales

**Ogro: el setter que deja pasar todo.** `void set_saldo(double s) { saldo_ = s; }`
hace privado el dato… y lo vuelve a abrir. Si hace falta, que valide; mejor, que
sea una acción con nombre.

**Ogro: devolver una referencia **no** `const` a un dato privado.**
`std::vector<double>& historial() { return historial_; }` permite
`cuenta.historial().clear()` desde afuera: la puerta queda abierta. Devolvé
`const std::vector<double>&`.

**Ogro: ignorar el `bool` de una acción.** `cuenta.extraer(5000);` sin mirar si se
pudo: el programa sigue como si hubiera sacado la plata.

**Ogro: el constructor que no valida.** Si `Fraccion(1, 0)` crea una fracción con
denominador 0, la invariante está rota desde el primer segundo.

**Esqueleto: acceder a lo privado desde una función suelta.**
```
main.cpp:12:12: error: ‘int Fraccion::den_’ is private within this context
```
Si una función de afuera lo necesita, quizás esa función debería ser un método.

### Misión R02-N03-M1 · La cuenta del Gremio

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Cuenta` con titular, saldo e historial (un vector de montos:
positivos los depósitos, negativos las extracciones), todo privado. `depositar` y
`extraer` devuelven `bool`: rechazan montos no positivos y extracciones mayores al
saldo. La entrada trae operaciones `d monto` o `e monto`; mostrá cada una con su
resultado y el saldo, y al final un resumen. Todo con 2 decimales.

#### Criterio de aprobación

- El saldo nunca queda negativo.
- Las acciones devuelven `bool` y `main` muestra si se aceptaron.
- No hay setters: solo acciones y getters `const`.

#### Entrada de ejemplo

```
d 5000
e 1200
e 9000
d -50
e 3800
d 250.5
```

#### Salida esperada

```
d 5000.00 ok -> $5000.00
e 1200.00 ok -> $3800.00
e 9000.00 rechazado -> $3800.00
d -50.00 rechazado -> $3800.00
e 3800.00 ok -> $0.00
d 250.50 ok -> $250.50
Kira: 4 movimientos, saldo $250.50
```

#### Solución de referencia

```cpp
// Mision 1 - La cuenta del Gremio: el saldo nunca es negativo.
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

class Cuenta {
public:
    explicit Cuenta(const std::string& titular) : titular_(titular) {}

    bool depositar(double monto)
    {
        if (monto <= 0) {
            return false;
        }
        saldo_ += monto;
        historial_.push_back(monto);
        return true;
    }

    bool extraer(double monto)
    {
        if (monto <= 0 || monto > saldo_) {
            return false;
        }
        saldo_ -= monto;
        historial_.push_back(-monto);
        return true;
    }

    double saldo() const { return saldo_; }

    void resumen() const
    {
        std::cout << titular_ << ": " << historial_.size() << " movimientos, saldo $" << saldo_ << "\n";
    }

private:
    std::string titular_;
    double saldo_ = 0;
    std::vector<double> historial_;
};

int main()
{
    std::cout << std::fixed << std::setprecision(2);
    Cuenta cuenta("Kira");
    char op = ' ';
    double monto = 0;
    while (std::cin >> op >> monto) {
        bool ok = (op == 'd') ? cuenta.depositar(monto) : cuenta.extraer(monto);
        std::cout << op << " " << monto << (ok ? " ok" : " rechazado") << " -> $" << cuenta.saldo() << "\n";
    }
    cuenta.resumen();
    return 0;
}
```

#### Pruebas

##### Solo rechazos
```entrada
e 100
d 0
d -5
```
```salida
e 100.00 rechazado -> $0.00
d 0.00 rechazado -> $0.00
d -5.00 rechazado -> $0.00
Kira: 0 movimientos, saldo $0.00
```

##### Extrae todo justo
```entrada
d 1000
e 1000
e 0.01
```
```salida
d 1000.00 ok -> $1000.00
e 1000.00 ok -> $0.00
e 0.01 rechazado -> $0.00
Kira: 2 movimientos, saldo $0.00
```

### Misión R02-N03-M2 · La fracción siempre simplificada

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Fraccion` cuya invariante es: **siempre simplificada** y con
**denominador positivo** (un denominador 0 se reemplaza por 1). El constructor la
establece con un helper privado `normalizar()` (usá `std::gcd` de `<numeric>`).
Agregá `sumar`, `multiplicar` (devuelven una fracción nueva), `valor()` y
`mostrar()` (sin `/1` si el denominador es 1). Probá: 6/8, 3/−9, 1/2 + 1/3,
2/3 × 9/4 y 5/0.

#### Criterio de aprobación

- La normalización es un método privado que llama el constructor.
- Las operaciones devuelven fracciones nuevas, que también quedan normalizadas.

#### Salida esperada

```
3/4 = 0.75
-1/3 = -0.333333
5/6 = 0.833333
3/2 = 1.5
5 = 5
```

#### Solución de referencia

```cpp
// Mision 2 - La fraccion siempre simplificada y con denominador positivo.
#include <iostream>
#include <numeric>   // std::gcd

class Fraccion {
public:
    Fraccion(int num, int den) : num_(num), den_(den == 0 ? 1 : den)
    {
        normalizar();
    }

    Fraccion sumar(const Fraccion& o) const
    {
        return Fraccion(num_ * o.den_ + o.num_ * den_, den_ * o.den_);
    }

    Fraccion multiplicar(const Fraccion& o) const
    {
        return Fraccion(num_ * o.num_, den_ * o.den_);
    }

    double valor() const
    {
        return static_cast<double>(num_) / den_;
    }

    void mostrar() const
    {
        std::cout << num_;
        if (den_ != 1) {
            std::cout << "/" << den_;
        }
    }

private:
    void normalizar()
    {
        if (den_ < 0) {
            num_ = -num_;
            den_ = -den_;
        }
        int d = std::gcd(num_, den_);
        if (d > 1) {
            num_ /= d;
            den_ /= d;
        }
    }

    int num_;
    int den_;
};

void linea(const Fraccion& f)
{
    f.mostrar();
    std::cout << " = " << f.valor() << "\n";
}

int main()
{
    linea(Fraccion(6, 8));
    linea(Fraccion(3, -9));
    linea(Fraccion(1, 2).sumar(Fraccion(1, 3)));
    linea(Fraccion(2, 3).multiplicar(Fraccion(9, 4)));
    linea(Fraccion(5, 0));
    return 0;
}
```

### Misión R02-N03-M3 · La mochila con capacidad

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Mochila` con una capacidad máxima de peso. `agregar(objeto, peso)`
solo guarda si entra (y el peso es positivo); `quitar(objeto)` saca el primero con
ese nombre. Ambos devuelven `bool`. La entrada trae `+ objeto peso` o `- objeto`.
Mostrá el resultado de cada acción, la mochila al final y el lugar libre.

#### Criterio de aprobación

- La invariante es: el peso nunca supera la capacidad.
- Los datos (objetos, pesos) son privados.

#### Entrada de ejemplo

```
+ cuerda 5
+ farol 3
+ yunque 15
+ mapa 1
- farol
+ brujula 2
- espada
+ carpa 9
```

#### Salida esperada

```
Guardado: cuerda
Guardado: farol
No entra: yunque
Guardado: mapa
Sacado: farol
Guardado: brujula
No está: espada
Guardado: carpa
Mochila (17/20): cuerda mapa brujula carpa
Lugar libre: 3
```

#### Solución de referencia

```cpp
// Mision 3 - La mochila con capacidad: agregar solo si entra.
#include <iostream>
#include <string>
#include <vector>

class Mochila {
public:
    explicit Mochila(int capacidad) : capacidad_(capacidad) {}

    bool agregar(const std::string& objeto, int peso)
    {
        if (peso <= 0 || peso_ + peso > capacidad_) {
            return false;
        }
        objetos_.push_back(objeto);
        pesos_.push_back(peso);
        peso_ += peso;
        return true;
    }

    bool quitar(const std::string& objeto)
    {
        for (std::size_t i = 0; i < objetos_.size(); i++) {
            if (objetos_[i] == objeto) {
                peso_ -= pesos_[i];
                objetos_.erase(objetos_.begin() + i);
                pesos_.erase(pesos_.begin() + i);
                return true;
            }
        }
        return false;
    }

    int libre() const { return capacidad_ - peso_; }

    void mostrar() const
    {
        std::cout << "Mochila (" << peso_ << "/" << capacidad_ << "):";
        for (const std::string& o : objetos_) {
            std::cout << " " << o;
        }
        std::cout << "\n";
    }

private:
    int capacidad_;
    int peso_ = 0;
    std::vector<std::string> objetos_;
    std::vector<int> pesos_;
};

int main()
{
    Mochila m(20);
    std::string accion, objeto;
    while (std::cin >> accion >> objeto) {
        if (accion == "+") {
            int peso = 0;
            std::cin >> peso;
            std::cout << (m.agregar(objeto, peso) ? "Guardado: " : "No entra: ") << objeto << "\n";
        } else if (accion == "-") {
            std::cout << (m.quitar(objeto) ? "Sacado: " : "No está: ") << objeto << "\n";
        }
    }
    m.mostrar();
    std::cout << "Lugar libre: " << m.libre() << "\n";
    return 0;
}
```

#### Pruebas

##### Quita de una mochila vacía
```entrada
- farol
+ pluma 0
+ ancla 21
```
```salida
No está: farol
No entra: pluma
No entra: ancla
Mochila (0/20):
Lugar libre: 20
```

##### Llena justo
```entrada
+ carpa 20
+ hilo 1
- carpa
+ hilo 1
```
```salida
Guardado: carpa
No entra: hilo
Sacado: carpa
Guardado: hilo
Mochila (1/20): hilo
Lugar libre: 19
```

### Encargo R02-N03-E1 · Las entradas del recital

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un recital tiene 100 entradas. Escribí `class Stock` que permite `reservar(n)`,
`confirmar(n)` (pasa reservadas a vendidas) y `cancelar(n)` (libera reservadas),
**sin sobrevender nunca**: disponibles + reservadas + vendidas = total, y ninguna
cuenta negativa. La entrada trae operaciones como `reservar 30`. Mostrá cada una y
el estado.

#### Criterio de aprobación

- Las tres acciones validan y devuelven `bool`.
- Disponibles se calcula, no se guarda aparte (así no se desincroniza).

#### Entrada de ejemplo

```
reservar 30
reservar 80
confirmar 20
cancelar 15
reservar 70
confirmar 5
cancelar 10
```

#### Salida esperada

```
reservar 30: ok -> disponibles 70, reservadas 30, vendidas 0
reservar 80: rechazado -> disponibles 70, reservadas 30, vendidas 0
confirmar 20: ok -> disponibles 70, reservadas 10, vendidas 20
cancelar 15: rechazado -> disponibles 70, reservadas 10, vendidas 20
reservar 70: ok -> disponibles 0, reservadas 80, vendidas 20
confirmar 5: ok -> disponibles 0, reservadas 75, vendidas 25
cancelar 10: ok -> disponibles 10, reservadas 65, vendidas 25
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El stock de entradas: reservar, confirmar y cancelar sin sobrevender.
#include <iostream>
#include <string>

class Stock {
public:
    explicit Stock(int total) : total_(total) {}

    bool reservar(int n)
    {
        if (n <= 0 || n > disponibles()) {
            return false;
        }
        reservadas_ += n;
        return true;
    }

    bool confirmar(int n)
    {
        if (n <= 0 || n > reservadas_) {
            return false;
        }
        reservadas_ -= n;
        vendidas_ += n;
        return true;
    }

    bool cancelar(int n)
    {
        if (n <= 0 || n > reservadas_) {
            return false;
        }
        reservadas_ -= n;
        return true;
    }

    int disponibles() const { return total_ - reservadas_ - vendidas_; }

    void mostrar() const
    {
        std::cout << "disponibles " << disponibles() << ", reservadas " << reservadas_
                  << ", vendidas " << vendidas_ << "\n";
    }

private:
    int total_;
    int reservadas_ = 0;
    int vendidas_ = 0;
};

int main()
{
    Stock recital(100);
    std::string op;
    int n = 0;
    while (std::cin >> op >> n) {
        bool ok = false;
        if (op == "reservar") {
            ok = recital.reservar(n);
        } else if (op == "confirmar") {
            ok = recital.confirmar(n);
        } else if (op == "cancelar") {
            ok = recital.cancelar(n);
        }
        std::cout << op << " " << n << (ok ? ": ok -> " : ": rechazado -> ");
        recital.mostrar();
    }
    return 0;
}
```

#### Pruebas

##### Confirma más de lo reservado
```entrada
reservar 10
confirmar 11
cancelar 11
confirmar 10
```
```salida
reservar 10: ok -> disponibles 90, reservadas 10, vendidas 0
confirmar 11: rechazado -> disponibles 90, reservadas 10, vendidas 0
cancelar 11: rechazado -> disponibles 90, reservadas 10, vendidas 0
confirmar 10: ok -> disponibles 90, reservadas 0, vendidas 10
```

##### Vende todo
```entrada
reservar 100
confirmar 100
reservar 1
```
```salida
reservar 100: ok -> disponibles 0, reservadas 100, vendidas 0
confirmar 100: ok -> disponibles 0, reservadas 0, vendidas 100
reservar 1: rechazado -> disponibles 0, reservadas 0, vendidas 100
```

##### Cantidades no positivas
```entrada
reservar 0
reservar -5
cancelar -1
```
```salida
reservar 0: rechazado -> disponibles 100, reservadas 0, vendidas 0
reservar -5: rechazado -> disponibles 100, reservadas 0, vendidas 0
cancelar -1: rechazado -> disponibles 100, reservadas 0, vendidas 0
```

### Prueba del sello

#### ¿Qué es una invariante? Dá un ejemplo.

Una regla que siempre se cumple en un objeto; por ejemplo, que el saldo de una cuenta nunca sea negativo.

#### ¿Por qué los datos privados ayudan a mantener las invariantes?

Porque solo los métodos de la clase pueden modificarlos; basta con que esos métodos respeten la regla.

#### ¿Por qué `curar(n)` es mejor que `set_vida(v)`?

Porque modela una acción con sus reglas en vez de dejar poner cualquier valor.

#### ¿Qué ventaja tiene que `extraer` devuelva `bool`?

Que quien llama se entera si la acción se hizo o no.

#### ¿Por qué en `Stock` conviene calcular las disponibles en vez de guardarlas?

Porque un dato calculado no puede quedar desincronizado con los demás.

### Soluciones (docente)

Material original: `03-C++/07-Encapsulamiento`, ampliado con invariantes explícitas y ejemplos fuera de los juegos.

## R02-N04 · Operadores para tus clases

```meta
tipo: tema
padre: R02-N03
precio: 10
criatura: goblin
temas: poo.operadores
```

### Crónica

En la mesa del cartógrafo de la Ciudadela, los mapas se suman: un tramo más otro tramo, una flecha más otra flecha. El cartógrafo escribe `tramo1 + tramo2` en sus planos, y el Taller lo entiende.

—Si tus piezas son números, que se sumen como números —dice {mentor}—. C++ te deja enseñarle a tus clases qué significa `+`, `==` o `<<`.

### Objetivos

Definir operadores para tus propios tipos: aritméticos (`+`, `-`, `*`, `+=`),
de comparación (`==`, `<`, y los generados con `= default`) y el de salida (`<<`)
para mostrarlos con `std::cout`, como métodos o como **funciones amigas**
(`friend`). Ordenar vectores de tus tipos con `std::sort`.

### Antes de empezar

- Structs, clases, constructores y encapsulamiento (nodos anteriores).

### Explicación

#### La idea
`a + b` es, para C++, una llamada a una función que se llama `operator+`. Si
escribís esa función para tu tipo, podés sumar tus objetos con `+`:
```cpp
Vec2 operator+(const Vec2& a, const Vec2& b)
{
    return {a.x + b.x, a.y + b.y};
}
Vec2 c = a + b;     // llama a operator+(a, b)
```

#### ¿Método o función libre?
- Los que **modifican** el objeto de la izquierda (`+=`, `-=`) van como **método**:
  ```cpp
  Vec2& operator+=(const Vec2& otro) { x += otro.x; y += otro.y; return *this; }
  ```
  `*this` es "el objeto sobre el que se llamó". Se devuelve por referencia para
  poder encadenar (`a += b += c`).
- Los que **crean uno nuevo** (`+`, `-`, `*`) conviene escribirlos como **funciones
  libres**, reutilizando el compuesto:
  ```cpp
  Vec2 operator+(Vec2 a, const Vec2& b) { a += b; return a; }   // a es una copia
  ```
  Como función libre, funcionan los dos órdenes (`2 * v` y `v * 2`, si escribís
  las dos versiones).

#### Comparar: `==`, `<` y `= default`
Desde C++20, el compilador puede generar `==` (y `!=`) comparando campo por campo:
```cpp
bool operator==(const Vec2&) const = default;
```
Y el operador "nave espacial" `<=>` genera **todas** las comparaciones (`<`, `<=`,
`>`, `>=`, `==`, `!=`), comparando los campos en el orden en que están declarados:
```cpp
auto operator<=>(const Dinero&) const = default;
```
Si querés un orden propio (por ejemplo, "más puntos primero"), escribí `operator<`:
```cpp
bool operator<(const Marca& otra) const { return puntos > otra.puntos; }
```
`std::sort` usa `<` para ordenar: con él definido, `std::sort(v.begin(), v.end())`
funciona con tu tipo.

#### Mostrar con `<<`
`std::cout << v` llama a `operator<<(std::cout, v)`. Se escribe como función libre
que recibe el stream (`std::ostream&`), escribe en él y **lo devuelve** (para poder
seguir encadenando `<< "\n"`):
```cpp
std::ostream& operator<<(std::ostream& os, const Vec2& v)
{
    return os << "(" << v.x << ", " << v.y << ")";
}
```
Si necesita datos privados, tiene dos caminos: usar los getters de la clase o ser su **amiga** (lo que sigue).

#### `friend`: funciones amigas
Una función **amiga** no es un método de la clase, pero la clase le da permiso para leer lo privado. Se declara **adentro** de la clase con `friend`:
```cpp
class Complejo {
public:
    Complejo(int re = 0, int im = 0) : re_(re), im_(im) {}
    friend Complejo operator+(const Complejo& a, const Complejo& b);      // amiga: puede leer re_ e im_
    friend std::ostream& operator<<(std::ostream& os, const Complejo& c);
private:
    int re_, im_;
};

Complejo operator+(const Complejo& a, const Complejo& b)   // sin "Complejo::": no es un método
{
    return {a.re_ + b.re_, a.im_ + b.im_};
}
```
- No tiene `this`: recibe los dos objetos como parámetros.
- Se puede escribir entera adentro de la clase (`friend ... { ... }`), como en la misión 4.
- La amistad **la da la clase**, no la pide la función: nadie de afuera puede hacerse amigo solo.
- **Cuándo usarla**: para operadores con dos objetos del mismo tipo (`+`, `==`) y para `<<` y `>>`, donde a la izquierda va el stream y no puede ser un método. Para lo demás, mejor métodos y getters: cada amiga es una función más que puede romper la invariante.

> **El apunte de la cátedra** define así la clase `complejo`, con `+`, `-`, `*` y `==` amigos: es el ejemplo clásico de sobrecarga de operadores en los parciales.

#### Con mesura
Un operador tiene que hacer **lo que todos esperan**: `+` suma, `==` compara. Usar
`+` para "agregar a la lista" o `*` para algo raro confunde. Si no es obvio, mejor
un método con nombre.

> **Si venís de C.** En C no se podía: había que escribir `vec2_sumar(a, b)`. En
> C++ los tipos propios se usan como los del lenguaje.

### Código de ejemplo

```cpp
/*
 * Operadores para tus clases: que un Vec2 se sume con + y se muestre con <<.
 */
#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Vec2 {
    double x = 0;
    double y = 0;

    double largo() const { return std::hypot(x, y); }

    // Operador como METODO: el objeto de la izquierda es "this".
    Vec2& operator+=(const Vec2& otro)
    {
        x += otro.x;
        y += otro.y;
        return *this;                        // devuelve el mismo objeto, ya modificado
    }

    // == y != generados por el compilador: comparan campo por campo (C++20).
    bool operator==(const Vec2&) const = default;
};

// Operadores como FUNCIONES LIBRES: reciben los dos lados.
Vec2 operator+(Vec2 a, const Vec2& b)
{
    a += b;                                  // reutiliza +=
    return a;
}

Vec2 operator-(const Vec2& a, const Vec2& b)
{
    return {a.x - b.x, a.y - b.y};
}

Vec2 operator*(const Vec2& v, double k)
{
    return {v.x * k, v.y * k};
}

// Mostrar con cout: recibe el stream, escribe en el, y lo devuelve para encadenar.
std::ostream& operator<<(std::ostream& os, const Vec2& v)
{
    return os << "(" << v.x << ", " << v.y << ")";
}

// Una clase con operator< se puede ordenar con std::sort sin decirle nada mas.
struct Marca {
    int puntos = 0;
    std::string nombre;
    bool operator<(const Marca& otra) const { return puntos > otra.puntos; }   // mas puntos va primero
};

int main()
{
    Vec2 pos{3, 4};
    Vec2 vel{1, -2};
    std::cout << "pos = " << pos << ", vel = " << vel << "\n";
    std::cout << "pos + vel = " << pos + vel << "\n";
    std::cout << "pos - vel = " << pos - vel << "\n";
    std::cout << "vel * 3 = " << vel * 3 << "\n";
    std::cout << "largo de pos: " << pos.largo() << "\n";

    pos += vel;
    std::cout << "tras pos += vel: " << pos << "\n";
    std::cout << std::boolalpha << "pos == (4, 2)? " << (pos == Vec2{4, 2}) << "\n";
    std::cout << "pos != vel? " << (pos != vel) << "\n";

    std::vector<Marca> tabla = {{120, "Bron"}, {340, "Kira"}, {95, "Lyn"}};
    std::sort(tabla.begin(), tabla.end());          // usa operator<
    for (const Marca& m : tabla) {
        std::cout << m.nombre << " " << m.puntos << "\n";
    }
    return 0;
}
```

### Salida esperada

```
pos = (3, 4), vel = (1, -2)
pos + vel = (4, 2)
pos - vel = (2, 6)
vel * 3 = (3, -6)
largo de pos: 5
tras pos += vel: (4, 2)
pos == (4, 2)? true
pos != vel? true
Kira 340
Bron 120
Lyn 95
```

### ¿Para qué sirve?

Los operadores hacen que el código de matemática, física y finanzas se lea como en el papel: vectores y matrices en motores de juegos (`pos += vel * dt`), números complejos, fracciones, fechas (`fecha + dias`), dinero exacto. `operator<<` se usa en todo proyecto para mostrar y registrar objetos, y `operator<` para ordenarlos sin escribir comparaciones a mano.

### Errores habituales

**Esqueleto: operador que no existe para tu tipo.**
```
main.cpp:3:40: error: no match for ‘operator+’ (operand types are ‘V’ and ‘V’)
```
```
main.cpp:3:34: error: no match for ‘operator<<’ (operand types are ‘std::ostream’ {aka ‘std::basic_ostream<char>’} and ‘V’)
```
Falta escribir el operador (o incluir el archivo donde está).

**Ogro: `operator<<` que no devuelve el stream.** Si devuelve `void`,
`std::cout << v << "\n"` no compila: la segunda parte no tiene a quién mandarle.

**Ogro: `operator+=` que devuelve una copia.** `Vec2 operator+=(...)` compila, pero
`(a += b) += c` modifica una copia. Devolvé `Vec2&` y `*this`.

**Ogro: `operator<` inconsistente.** Si `a < b` y `b < a` pueden ser verdaderas a la
vez (por ejemplo, usando `<=`), `std::sort` puede comportarse de forma indefinida.
Usá `<` estricto.

**Goblin: comparar `double` con `==`.** `0.1 + 0.2 == 0.3` es **falso** por el
redondeo. Para dinero, guardá centavos en enteros (ver el Encargo).

### Misión R02-N04-M1 · El vector del cartógrafo

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Completá `struct Vec2` con `+=`, `-=` (métodos), `+`, `-`, `*` por un número en los
**dos órdenes** (funciones libres), `==` generado con `= default`, `largo()` y
`<<`. Partiendo de (2, 3), sumá 4 veces el paso (1.5, −0.5) mostrando cada posición;
después mostrá el recorrido, su largo, `2 * paso` y `paso * 2`, y comprobá con `==`
que la posición menos 4 pasos es el inicio.

#### Criterio de aprobación

- `+` y `-` reutilizan `+=` y `-=`.
- `*` funciona con el número a la izquierda y a la derecha.
- `<<` devuelve el stream.

#### Salida esperada

```
Paso 1: (3.5, 2.5)
Paso 2: (5, 2)
Paso 3: (6.5, 1.5)
Paso 4: (8, 1)
Recorrido: (6, -2), largo 6.32456
Doble paso: (3, -1) = (3, -1)
¿Volvió al inicio? true
```

#### Solución de referencia

```cpp
// Mision 1 - El Vec2 del cartografo: suma, resta, escala, igualdad y <<.
#include <cmath>
#include <iostream>

struct Vec2 {
    double x = 0;
    double y = 0;

    Vec2& operator+=(const Vec2& o)
    {
        x += o.x;
        y += o.y;
        return *this;
    }

    Vec2& operator-=(const Vec2& o)
    {
        x -= o.x;
        y -= o.y;
        return *this;
    }

    double largo() const { return std::hypot(x, y); }

    bool operator==(const Vec2&) const = default;
};

Vec2 operator+(Vec2 a, const Vec2& b) { return a += b; }
Vec2 operator-(Vec2 a, const Vec2& b) { return a -= b; }
Vec2 operator*(const Vec2& v, double k) { return {v.x * k, v.y * k}; }
Vec2 operator*(double k, const Vec2& v) { return v * k; }

std::ostream& operator<<(std::ostream& os, const Vec2& v)
{
    return os << "(" << v.x << ", " << v.y << ")";
}

int main()
{
    Vec2 inicio{2, 3};
    Vec2 paso{1.5, -0.5};
    Vec2 pos = inicio;
    for (int i = 1; i <= 4; i++) {
        pos += paso;
        std::cout << "Paso " << i << ": " << pos << "\n";
    }
    Vec2 recorrido = pos - inicio;
    std::cout << "Recorrido: " << recorrido << ", largo " << recorrido.largo() << "\n";
    std::cout << "Doble paso: " << 2 * paso << " = " << paso * 2 << "\n";
    std::cout << std::boolalpha << "¿Volvió al inicio? " << (pos - 4 * paso == inicio) << "\n";
    return 0;
}
```

### Misión R02-N04-M2 · Fracciones con operadores

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Tomá la fracción siempre simplificada del nodo anterior y dale operadores: `+=`,
`*=`, `+`, `*`, `==` y `<<` (sin `/1` si el denominador es 1). Con un constructor
con valores por defecto (`Fraccion(int num = 0, int den = 1)`), un entero se
convierte en fracción. Mostrá: 1/2 + 1/3, 1/2 × 1/3, si 1/2 == 2/4, la suma
1/(1·2) + 1/(2·3) + 1/(3·4) + 1/(4·5) con un bucle, y 3 + 1/4.

#### Criterio de aprobación

- La fracción sigue normalizada después de cada operación.
- `==` funciona porque las fracciones están normalizadas.

#### Salida esperada

```
1/2 + 1/3 = 5/6
1/2 * 1/3 = 1/6
1/2 == 1/2? true
1/2 + 1/6 + 1/12 + 1/20 = 4/5
3 + 1/4 = 13/4
```

#### Solución de referencia

```cpp
// Mision 2 - Fracciones con operadores: +, *, == y <<.
#include <iostream>
#include <numeric>

class Fraccion {
public:
    Fraccion(int num = 0, int den = 1) : num_(num), den_(den == 0 ? 1 : den) { normalizar(); }

    Fraccion& operator+=(const Fraccion& o)
    {
        num_ = num_ * o.den_ + o.num_ * den_;
        den_ = den_ * o.den_;
        normalizar();
        return *this;
    }

    Fraccion& operator*=(const Fraccion& o)
    {
        num_ *= o.num_;
        den_ *= o.den_;
        normalizar();
        return *this;
    }

    bool operator==(const Fraccion&) const = default;
    int num() const { return num_; }
    int den() const { return den_; }

private:
    void normalizar()
    {
        if (den_ < 0) {
            num_ = -num_;
            den_ = -den_;
        }
        int d = std::gcd(num_, den_);
        if (d > 1) {
            num_ /= d;
            den_ /= d;
        }
    }

    int num_;
    int den_;
};

Fraccion operator+(Fraccion a, const Fraccion& b) { return a += b; }
Fraccion operator*(Fraccion a, const Fraccion& b) { return a *= b; }

std::ostream& operator<<(std::ostream& os, const Fraccion& f)
{
    os << f.num();
    if (f.den() != 1) {
        os << "/" << f.den();
    }
    return os;
}

int main()
{
    Fraccion a(1, 2), b(1, 3), c(2, 4);
    std::cout << a << " + " << b << " = " << a + b << "\n";
    std::cout << a << " * " << b << " = " << a * b << "\n";
    std::cout << std::boolalpha << a << " == " << c << "? " << (a == c) << "\n";
    Fraccion suma;
    for (int n = 1; n <= 4; n++) {
        suma += Fraccion(1, n * (n + 1));
    }
    std::cout << "1/2 + 1/6 + 1/12 + 1/20 = " << suma << "\n";
    std::cout << "3 + 1/4 = " << Fraccion(3) + Fraccion(1, 4) << "\n";
    return 0;
}
```

### Misión R02-N04-M3 · El tablero de la estación

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Cada línea de la entrada es una salida de tren: `HH:MM destino`. Escribí
`struct Hora` con `operator<` y `<<` (con ceros adelante), y `struct Salida` con su
propio `operator<` (por hora). Ordená con `std::sort` y mostrá el tablero. Al final,
mostrá cuánto tiempo hay entre la primera y la última salida.

#### Criterio de aprobación

- `std::sort` se usa sin comparador: usa el `operator<` de `Salida`.
- `Hora` se muestra con `<<` como `07:05`.

#### Entrada de ejemplo

```
14:30 Norte
07:05 Faro
21:10 Reloj
09:45 Vapor
07:40 Norte
```

#### Salida esperada

```
07:05  Faro
07:40  Norte
09:45  Vapor
14:30  Norte
21:10  Reloj
Entre el primero y el último: 14:05
```

#### Solución de referencia

```cpp
// Mision 3 - Los horarios de los trenes: operator< para ordenar y << para mostrar.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Hora {
    int h = 0;
    int m = 0;

    int minutos() const { return h * 60 + m; }
    bool operator<(const Hora& o) const { return minutos() < o.minutos(); }
    bool operator==(const Hora&) const = default;
};

std::ostream& operator<<(std::ostream& os, const Hora& t)
{
    return os << (t.h < 10 ? "0" : "") << t.h << ":" << (t.m < 10 ? "0" : "") << t.m;
}

struct Salida {
    Hora hora;
    std::string destino;
    bool operator<(const Salida& o) const { return hora < o.hora; }
};

int main()
{
    std::vector<Salida> tablero;
    Salida s;
    char dos_puntos = ':';
    while (std::cin >> s.hora.h >> dos_puntos >> s.hora.m >> s.destino) {
        tablero.push_back(s);
    }
    std::sort(tablero.begin(), tablero.end());
    for (const Salida& x : tablero) {
        std::cout << x.hora << "  " << x.destino << "\n";
    }
    if (!tablero.empty()) {
        int total = tablero.back().hora.minutos() - tablero.front().hora.minutos();
        Hora espera{total / 60, total % 60};
        std::cout << "Entre el primero y el último: " << espera << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Una sola salida
```entrada
12:00 Norte
```
```salida
12:00  Norte
Entre el primero y el último: 00:00
```

##### Medianoche y última
```entrada
23:59 Reloj
00:00 Faro
00:01 Vapor
```
```salida
00:00  Faro
00:01  Vapor
23:59  Reloj
Entre el primero y el último: 23:59
```

### Misión R02-N04-M4 · Los complejos del apunte

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí la clase `Complejo` (parte real e imaginaria, enteras y **privadas**) con los operadores `+`, `-`, `*` y `==` como funciones **amigas**, y también `<<` (que muestre `3 + 2i` o `1 - 4i`) y `>>` (que lea dos enteros).

El programa lee pares de complejos (cuatro enteros: real e imaginaria de `a`, real e imaginaria de `b`) hasta que se terminen, y por cada par muestra la suma, la resta, el producto y si son iguales.

Recordá: `(a + bi) * (c + di) = (ac - bd) + (ad + bc)i`.

#### Criterio de aprobación

- Los datos son privados y no hay getters: los operadores son amigos.
- `<<` y `>>` devuelven el stream para poder encadenar.
- El signo de la parte imaginaria se muestra bien (`1 - 4i`, no `1 + -4i`).

#### Entrada de ejemplo

```
3 2 1 -4
```

#### Salida esperada

```
(3 + 2i) + (1 - 4i) = 4 - 2i
(3 + 2i) - (1 - 4i) = 2 + 6i
(3 + 2i) * (1 - 4i) = 11 - 10i
Son distintos
```

#### Solución de referencia

```cpp
// Mision 4 - Los complejos del apunte: una clase con datos privados y operadores amigos.
#include <iostream>

class Complejo {
public:
    Complejo(int re = 0, int im = 0) : re_(re), im_(im) {}

    // Amigas: no son metodos (no tienen this), pero pueden leer re_ e im_.
    friend Complejo operator+(const Complejo& a, const Complejo& b) { return {a.re_ + b.re_, a.im_ + b.im_}; }
    friend Complejo operator-(const Complejo& a, const Complejo& b) { return {a.re_ - b.re_, a.im_ - b.im_}; }
    friend Complejo operator*(const Complejo& a, const Complejo& b)
    {
        return {a.re_ * b.re_ - a.im_ * b.im_, a.re_ * b.im_ + a.im_ * b.re_};
    }
    friend bool operator==(const Complejo& a, const Complejo& b) { return a.re_ == b.re_ && a.im_ == b.im_; }

    friend std::ostream& operator<<(std::ostream& os, const Complejo& c)
    {
        os << c.re_;
        if (c.im_ < 0) {
            return os << " - " << -c.im_ << "i";
        }
        return os << " + " << c.im_ << "i";
    }

    friend std::istream& operator>>(std::istream& is, Complejo& c) { return is >> c.re_ >> c.im_; }

private:
    int re_;
    int im_;
};

int main()
{
    Complejo a, b;
    while (std::cin >> a >> b) {
        std::cout << "(" << a << ") + (" << b << ") = " << a + b << "\n";
        std::cout << "(" << a << ") - (" << b << ") = " << a - b << "\n";
        std::cout << "(" << a << ") * (" << b << ") = " << a * b << "\n";
        std::cout << (a == b ? "Son iguales" : "Son distintos") << "\n";
    }
    return 0;
}
```

#### Pruebas

##### i por i da -1
```entrada
0 1 0 1
```
```salida
(0 + 1i) + (0 + 1i) = 0 + 2i
(0 + 1i) - (0 + 1i) = 0 + 0i
(0 + 1i) * (0 + 1i) = -1 + 0i
Son iguales
```

##### Dos pares: reales y conjugados
```entrada
5 0 -2 0
2 3 2 -3
```
```salida
(5 + 0i) + (-2 + 0i) = 3 + 0i
(5 + 0i) - (-2 + 0i) = 7 + 0i
(5 + 0i) * (-2 + 0i) = -10 + 0i
Son distintos
(2 + 3i) + (2 - 3i) = 4 + 0i
(2 + 3i) - (2 - 3i) = 0 + 6i
(2 + 3i) * (2 - 3i) = 13 + 0i
Son distintos
```

### Encargo R02-N04-E1 · Dinero sin errores

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Para no perder centavos, el almacén guarda el dinero **en centavos** (enteros).
Escribí `class Dinero` con un constructor `explicit` en centavos, una función
`static Dinero pesos(pesos, centavos)`, `+`, `-`, `*` por un entero,
`porcentaje(int)`, todas las comparaciones con `<=>` generado y `<<` que muestre
`$7501,50`. Calculá: 3 yerbas de $2500,50 y 2 paquetes de galletitas de $899,99,
un 15% de descuento, el total a pagar y el vuelto de $10000. Al final, mostrá que
con `double`, sumar 10 veces 0.1 **no** da exactamente 1.

#### Criterio de aprobación

- Guarda un `long long` de centavos.
- Usa `<=>` con `= default` para comparar.
- `<<` muestra siempre dos dígitos de centavos.

#### Salida esperada

```
Subtotal: $9301,48
Descuento 15%: $1395,22
A pagar: $7906,26
Paga con $10000,00, vuelto $2093,74
Alcanza.
Con double, 10 veces 0.1 == 1? no
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Dinero en centavos: sin errores de redondeo.
#include <iostream>

class Dinero {
public:
    explicit Dinero(long long centavos = 0) : centavos_(centavos) {}

    static Dinero pesos(long long p, int c = 0) { return Dinero(p * 100 + c); }

    Dinero& operator+=(const Dinero& o)
    {
        centavos_ += o.centavos_;
        return *this;
    }

    Dinero& operator-=(const Dinero& o)
    {
        centavos_ -= o.centavos_;
        return *this;
    }

    Dinero porcentaje(int pct) const { return Dinero(centavos_ * pct / 100); }
    long long centavos() const { return centavos_; }
    auto operator<=>(const Dinero&) const = default;

private:
    long long centavos_;
};

Dinero operator+(Dinero a, const Dinero& b) { return a += b; }
Dinero operator-(Dinero a, const Dinero& b) { return a -= b; }
Dinero operator*(const Dinero& d, int n) { return Dinero(d.centavos() * n); }

std::ostream& operator<<(std::ostream& os, const Dinero& d)
{
    long long c = d.centavos();
    if (c < 0) {
        os << "-";
        c = -c;
    }
    return os << "$" << c / 100 << "," << (c % 100 < 10 ? "0" : "") << c % 100;
}

int main()
{
    Dinero yerba = Dinero::pesos(2500, 50);
    Dinero galletitas = Dinero::pesos(899, 99);
    Dinero total = yerba * 3 + galletitas * 2;
    Dinero descuento = total.porcentaje(15);
    std::cout << "Subtotal: " << total << "\n";
    std::cout << "Descuento 15%: " << descuento << "\n";
    Dinero a_pagar = total - descuento;
    std::cout << "A pagar: " << a_pagar << "\n";
    Dinero pago = Dinero::pesos(10000);
    std::cout << "Paga con " << pago << ", vuelto " << pago - a_pagar << "\n";
    std::cout << (pago >= a_pagar ? "Alcanza." : "No alcanza.") << "\n";

    double suma = 0;
    for (int i = 0; i < 10; i++) {
        suma += 0.1;
    }
    std::cout << "Con double, 10 veces 0.1 == 1? " << (suma == 1.0 ? "si" : "no") << "\n";
    return 0;
}
```

### Prueba del sello

#### ¿Qué función llama C++ cuando escribís `a + b` con tus objetos?

`operator+(a, b)` (o `a.operator+(b)` si es un método).

#### ¿Por qué `operator+=` devuelve `Vec2&` y `*this`?

Porque modifica el objeto de la izquierda y lo devuelve para poder encadenar.

#### ¿Por qué `operator<<` recibe y devuelve `std::ostream&`?

Para escribir en ese stream y devolverlo, así se puede seguir encadenando `<<`.

#### ¿Qué genera `auto operator<=>(const T&) const = default;`?

Todas las comparaciones (`<`, `<=`, `>`, `>=`, `==`, `!=`), comparando campo por campo en orden.

#### ¿Qué es una función `friend`? ¿Tiene `this`?

Una función que no es método de la clase, pero puede leer lo privado porque la clase la declaró amiga. No tiene `this`: recibe los objetos como parámetros.

#### ¿Por qué `operator<<` no puede ser un método de tu clase?

Porque a la izquierda de `<<` va el `ostream` (`cout << c`), y un método tiene siempre su objeto a la izquierda.

#### ¿Qué necesita tu tipo para poder usar `std::sort(v.begin(), v.end())` sin comparador?

Un `operator<`.

### Soluciones (docente)

Nodo nuevo (no estaba en FullCursos): sobrecarga de operadores, necesaria para `Vec2` en las Sendas y para ordenar con la STL. Usa `= default` y `<=>` de C++20.

## R02-N05 · Composición

```meta
tipo: tema
padre: R02-N04
precio: 10
criatura: esqueleto
temas: poo.composicion
```

### Crónica

Tesla despliega el plano del Gran Reloj de la plaza. No es un dibujo enorme: es una lista. "Una caja. Un péndulo. Tres agujas. Un mecanismo de campanas." Y cada cosa de la lista tiene su propio plano.

—Nadie diseña un reloj de una sola pieza —dice—. Se diseña con **piezas que ya existen**. Un reloj **tiene** un péndulo. Eso se llama composición, y es la forma más sana de construir cosas grandes.

### Objetivos

Construir clases que **contienen** objetos de otras clases (composición, relación
"tiene un"), delegar el trabajo en esas partes, entender el orden en que se
construyen y destruyen, y distinguir composición de herencia.

### Antes de empezar

- Clases, constructores y operadores (nodos anteriores).

### Explicación

#### "Tiene un"
Una clase puede tener como miembros **objetos de otras clases**:
```cpp
class Jugador {
    std::string nombre_;
    Vec2 pos_;            // un Jugador TIENE UNA posición
    Mochila mochila_;     // TIENE UNA mochila
};
```
Y una `Mochila` tiene un `std::vector<Item>`: la composición se arma en capas,
cada una con su responsabilidad.

#### Delegar
La clase de afuera no hace todo: le **pide** a sus partes.
```cpp
void Jugador::recoger(const Item& it) { mochila_.agregar(it); }
```
`Jugador` no sabe cómo guarda la mochila sus cosas; solo sabe pedirle que guarde
una. Si mañana la mochila cambia por dentro, `Jugador` no se entera. Cada clase
chica se prueba sola, y la grande es fácil de leer.

#### Construcción y destrucción
Al crear un objeto compuesto, **primero** se construyen sus miembros, en el
**orden en que están declarados**, y después corre el cuerpo del constructor. Para
pasarles parámetros, se usa la lista de inicialización:
```cpp
Reloj() : caja_("caja"), pendulo_("péndulo") { /* acá las partes ya existen */ }
```
Al destruirlo, al revés: primero el cuerpo del destructor, después los miembros en
orden inverso.

#### Composición o herencia
El nodo siguiente presenta la **herencia** ("es un"). Para elegir:
| Pregunta | Relación | Herramienta |
|---|---|---|
| ¿Un Jugador **es una** Mochila? No. ¿**Tiene** una? Sí. | tiene un | composición |
| ¿Un Guerrero **es una** Entidad del juego? Sí. | es un | herencia |

Regla práctica: **preferí composición**. Es más flexible (se cambian las partes sin
tocar todo) y más fácil de razonar. Herencia solo cuando hay un "es un" real.

#### Partes que se prestan
A veces un objeto necesita **usar** otro sin ser su dueño (un Jugador que conoce el
Mapa, pero no lo contiene). Eso se hace guardando una referencia o un puntero, y
tiene sus peligros (¿qué pasa si el mapa muere antes?). Lo vas a ver con los
punteros inteligentes en la rama 3; por ahora, cada objeto **contiene** sus partes.

> **Si venís de C.** Es como un struct con otros structs adentro, pero cada parte
> trae sus métodos y se construye y destruye sola.

### Código de ejemplo

```cpp
/*
 * Composicion: un objeto que TIENE otros objetos adentro.
 *   un Jugador TIENE UNA posicion y TIENE UNA mochila; una Mochila TIENE muchos Item.
 */
#include <iostream>
#include <string>
#include <vector>

struct Vec2 {
    double x = 0;
    double y = 0;
};

struct Item {
    std::string nombre;
    int valor = 0;
};

class Mochila {
public:
    void agregar(const Item& it) { items_.push_back(it); }

    int valor_total() const
    {
        int total = 0;
        for (const Item& it : items_) {
            total += it.valor;
        }
        return total;
    }

    void listar() const
    {
        if (items_.empty()) {
            std::cout << "    (vacía)\n";
        }
        for (const Item& it : items_) {
            std::cout << "    - " << it.nombre << " (" << it.valor << ")\n";
        }
    }

private:
    std::vector<Item> items_;
};

class Jugador {
public:
    explicit Jugador(const std::string& nombre) : nombre_(nombre) {}

    // Jugador DELEGA en sus partes: mover toca la posicion, recoger la mochila.
    void mover(double dx, double dy)
    {
        pos_.x += dx;
        pos_.y += dy;
    }

    void recoger(const Item& it) { mochila_.agregar(it); }

    void ficha() const
    {
        std::cout << nombre_ << " en (" << pos_.x << ", " << pos_.y << ")\n";
        std::cout << "  mochila (valor " << mochila_.valor_total() << "):\n";
        mochila_.listar();
    }

private:
    std::string nombre_;
    Vec2 pos_;            // TIENE UNA posicion
    Mochila mochila_;     // TIENE UNA mochila
};

int main()
{
    Jugador kira("Kira");
    kira.ficha();
    kira.mover(3, 0);
    kira.mover(0, 2.5);
    kira.recoger({"Poción", 15});
    kira.recoger({"Llave de bronce", 0});
    kira.recoger({"Rubí", 120});
    kira.ficha();
    return 0;
}
```

### Salida esperada

```
Kira en (0, 0)
  mochila (valor 0):
    (vacía)
Kira en (3, 2.5)
  mochila (valor 135):
    - Poción (15)
    - Llave de bronce (0)
    - Rubí (120)
```

### ¿Para qué sirve?

Casi todo software se arma por composición: una `Factura` tiene un `Cliente` y muchas `Lineas`; un `Auto` de un simulador tiene `Motor`, `Ruedas` y `Tanque`; un personaje de un juego tiene `Salud`, `Inventario` y `Animacion`. Los motores de juegos modernos (Unity, Godot, Unreal) se basan en esta idea: una entidad es una colección de componentes.

### Errores habituales

**Esqueleto: una parte sin constructor por defecto.** Si `Pieza` necesita un
nombre, el constructor del `Reloj` tiene que dárselo en la lista de inicialización:
```
main.cpp:12:5: error: no matching function for call to ‘Pieza::Pieza()’
```

**Ogro: la clase "Dios".** Un `Juego` que guarda 40 datos sueltos y tiene 60
métodos. Partilo: `Mapa`, `Jugador`, `Marcador`, cada uno con lo suyo.

**Ogro: herencia donde iba composición.** `class Jugador : public Mochila` compila,
pero dice que un jugador **es** una mochila: de golpe, `jugador.agregar(item)` y
todo lo de la mochila queda a la vista. Si la relación es "tiene", es un miembro.

**Troll: modificar la copia de una parte.** Un getter que devuelve la mochila **por
valor** (`Mochila mochila() const`) entrega una copia: agregarle cosas no cambia la
del jugador. Delegá con un método (`recoger`) en vez de exponer la parte.

### Misión R02-N05-M1 · La tienda del taller

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí tres clases: `Deposito` (un vector de productos con nombre, stock y precio;
`sacar(nombre, cantidad)` devuelve el precio total o −1 si no puede), `Caja`
(acumula ventas y total) y `Tienda`, que **tiene** un depósito y una caja y
**delega** en ellos. Cargá engranaje (10 u., $350), resorte (50, $25) y válvula
(3, $1200). Cada línea de la entrada es una venta `producto cantidad`. Al final,
el cierre: ventas, total y stock.

#### Criterio de aprobación

- `Tienda` no guarda productos ni dinero: delega en `Deposito` y `Caja`.
- Las ventas imposibles no cambian nada.

#### Entrada de ejemplo

```
engranaje 4
valvula 5
resorte 20
valvula 3
tuerca 1
engranaje 6
```

#### Salida esperada

```
Vendido: 4 engranaje por $1400
No se puede vender 5 valvula
Vendido: 20 resorte por $500
Vendido: 3 valvula por $3600
No se puede vender 1 tuerca
Vendido: 6 engranaje por $2100
Cierre: 4 ventas, $7600
  engranaje: 0
  resorte: 30
  valvula: 0
```

#### Solución de referencia

```cpp
// Mision 1 - La tienda del taller: Tienda TIENE un Deposito y una Caja.
#include <iostream>
#include <string>
#include <vector>

struct Producto {
    std::string nombre;
    int stock = 0;
    int precio = 0;
};

class Deposito {
public:
    void cargar(const Producto& p) { productos_.push_back(p); }

    // Devuelve el precio total si pudo sacar la cantidad, o -1 si no.
    int sacar(const std::string& nombre, int cantidad)
    {
        for (Producto& p : productos_) {
            if (p.nombre == nombre) {
                if (cantidad <= 0 || cantidad > p.stock) {
                    return -1;
                }
                p.stock -= cantidad;
                return p.precio * cantidad;
            }
        }
        return -1;
    }

    void listar() const
    {
        for (const Producto& p : productos_) {
            std::cout << "  " << p.nombre << ": " << p.stock << "\n";
        }
    }

private:
    std::vector<Producto> productos_;
};

class Caja {
public:
    void cobrar(int monto)
    {
        total_ += monto;
        ventas_++;
    }

    int total() const { return total_; }
    int ventas() const { return ventas_; }

private:
    int total_ = 0;
    int ventas_ = 0;
};

class Tienda {
public:
    void cargar(const Producto& p) { deposito_.cargar(p); }

    void vender(const std::string& nombre, int cantidad)
    {
        int monto = deposito_.sacar(nombre, cantidad);
        if (monto < 0) {
            std::cout << "No se puede vender " << cantidad << " " << nombre << "\n";
            return;
        }
        caja_.cobrar(monto);
        std::cout << "Vendido: " << cantidad << " " << nombre << " por $" << monto << "\n";
    }

    void cierre() const
    {
        std::cout << "Cierre: " << caja_.ventas() << " ventas, $" << caja_.total() << "\n";
        deposito_.listar();
    }

private:
    Deposito deposito_;
    Caja caja_;
};

int main()
{
    Tienda tienda;
    tienda.cargar({"engranaje", 10, 350});
    tienda.cargar({"resorte", 50, 25});
    tienda.cargar({"valvula", 3, 1200});
    std::string nombre;
    int cantidad = 0;
    while (std::cin >> nombre >> cantidad) {
        tienda.vender(nombre, cantidad);
    }
    tienda.cierre();
    return 0;
}
```

#### Pruebas

##### Vende todo el resorte
```entrada
resorte 50
resorte 1
```
```salida
Vendido: 50 resorte por $1250
No se puede vender 1 resorte
Cierre: 1 ventas, $1250
  engranaje: 10
  resorte: 0
  valvula: 3
```

##### Sin ventas
```entrada
```
```salida
Cierre: 0 ventas, $0
  engranaje: 10
  resorte: 50
  valvula: 3
```

### Misión R02-N05-M2 · El tren de carga

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Vagon` (tipo, capacidad y carga; `cargar(t)` carga lo que entra y
devuelve lo que sobró) y `class Tren`, que tiene un vector de vagones.
`Tren::cargar(tipo, t)` reparte la carga entre los vagones de ese tipo, en orden, y
devuelve lo que no entró. El tren tiene vagones de carbón (30), agua (20), carbón
(30) y hierro (40). Cada línea de la entrada es una carga `tipo toneladas`.
Mostrá cada carga (y lo que no entró) y el informe final.

#### Criterio de aprobación

- `Tren` recorre sus vagones por referencia para cargarlos.
- La carga que no entra en un vagón pasa al siguiente del mismo tipo.

#### Entrada de ejemplo

```
carbon 45
agua 25
hierro 10
carbon 20
madera 5
```

#### Salida esperada

```
Carga de 45 t de carbon
Carga de 25 t de agua: no entraron 5 t
Carga de 10 t de hierro
Carga de 20 t de carbon: no entraron 5 t
Carga de 5 t de madera: no entraron 5 t
El Carbonero:
  vagón 1 (carbon): 30/30
  vagón 2 (agua): 20/20
  vagón 3 (carbon): 30/30
  vagón 4 (hierro): 10/40
  total: 90 t
```

#### Solución de referencia

```cpp
// Mision 2 - El tren de carga: un Tren TIENE Vagones, cada uno con su capacidad.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

class Vagon {
public:
    Vagon(const std::string& tipo, int capacidad) : tipo_(tipo), capacidad_(capacidad) {}

    // Carga lo que entra y devuelve lo que sobro.
    int cargar(int toneladas)
    {
        int entra = std::min(toneladas, capacidad_ - carga_);
        carga_ += entra;
        return toneladas - entra;
    }

    const std::string& tipo() const { return tipo_; }
    int carga() const { return carga_; }
    int capacidad() const { return capacidad_; }

private:
    std::string tipo_;
    int capacidad_;
    int carga_ = 0;
};

class Tren {
public:
    explicit Tren(const std::string& nombre) : nombre_(nombre) {}

    void enganchar(const Vagon& v) { vagones_.push_back(v); }

    // Reparte la carga en los vagones del tipo pedido, en orden. Devuelve lo que no entro.
    int cargar(const std::string& tipo, int toneladas)
    {
        for (Vagon& v : vagones_) {
            if (v.tipo() == tipo && toneladas > 0) {
                toneladas = v.cargar(toneladas);
            }
        }
        return toneladas;
    }

    void informe() const
    {
        int total = 0;
        std::cout << nombre_ << ":\n";
        for (std::size_t i = 0; i < vagones_.size(); i++) {
            const Vagon& v = vagones_[i];
            std::cout << "  vagón " << i + 1 << " (" << v.tipo() << "): " << v.carga() << "/" << v.capacidad() << "\n";
            total += v.carga();
        }
        std::cout << "  total: " << total << " t\n";
    }

private:
    std::string nombre_;
    std::vector<Vagon> vagones_;
};

int main()
{
    Tren tren("El Carbonero");
    tren.enganchar(Vagon("carbon", 30));
    tren.enganchar(Vagon("agua", 20));
    tren.enganchar(Vagon("carbon", 30));
    tren.enganchar(Vagon("hierro", 40));
    std::string tipo;
    int toneladas = 0;
    while (std::cin >> tipo >> toneladas) {
        int sobra = tren.cargar(tipo, toneladas);
        std::cout << "Carga de " << toneladas << " t de " << tipo;
        if (sobra > 0) {
            std::cout << ": no entraron " << sobra << " t";
        }
        std::cout << "\n";
    }
    tren.informe();
    return 0;
}
```

#### Pruebas

##### Llena todo el carbón de una
```entrada
carbon 60
carbon 1
```
```salida
Carga de 60 t de carbon
Carga de 1 t de carbon: no entraron 1 t
El Carbonero:
  vagón 1 (carbon): 30/30
  vagón 2 (agua): 0/20
  vagón 3 (carbon): 30/30
  vagón 4 (hierro): 0/40
  total: 60 t
```

##### Sin cargas
```entrada
```
```salida
El Carbonero:
  vagón 1 (carbon): 0/30
  vagón 2 (agua): 0/20
  vagón 3 (carbon): 0/30
  vagón 4 (hierro): 0/40
  total: 0 t
```

##### Hierro justo
```entrada
hierro 40
agua 0
```
```salida
Carga de 40 t de hierro
Carga de 0 t de agua
El Carbonero:
  vagón 1 (carbon): 0/30
  vagón 2 (agua): 0/20
  vagón 3 (carbon): 0/30
  vagón 4 (hierro): 40/40
  total: 40 t
```

### Misión R02-N05-M3 · El orden del reloj

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Pieza`, que avisa cuando se arma y cuando se desarma, y
`class Reloj`, que tiene tres piezas (caja, péndulo y agujas, declaradas en ese
orden) y avisa cuando está listo y cuando se apaga. Creá un reloj dentro de un
bloque y observá el orden. **Antes de ejecutar**, escribí el orden que esperás.

Después, probá cambiar el orden de la lista de inicialización (sin cambiar el de
las declaraciones): ¿cambia algo? ¿Qué dice `-Wall`?

#### Criterio de aprobación

- Las piezas se pasan por la lista de inicialización.
- La salida muestra el orden de construcción y destrucción.

#### Salida esperada

```
Construir:
  arma caja
  arma péndulo
  arma agujas
  el reloj está listo
Destruir:
  se apaga el reloj
  desarma agujas
  desarma péndulo
  desarma caja
```

#### Solución de referencia

```cpp
// Mision 3 - El orden de construccion en la composicion.
#include <iostream>
#include <string>

class Pieza {
public:
    explicit Pieza(const std::string& nombre) : nombre_(nombre) { std::cout << "  arma " << nombre_ << "\n"; }
    ~Pieza() { std::cout << "  desarma " << nombre_ << "\n"; }

private:
    std::string nombre_;
};

class Reloj {
public:
    Reloj() : caja_("caja"), pendulo_("péndulo"), agujas_("agujas")
    {
        std::cout << "  el reloj está listo\n";
    }

    ~Reloj() { std::cout << "  se apaga el reloj\n"; }

private:
    Pieza caja_;          // se construyen en ESTE orden (el de la declaracion)
    Pieza pendulo_;
    Pieza agujas_;
};

int main()
{
    std::cout << "Construir:\n";
    {
        Reloj r;
        std::cout << "Destruir:\n";
    }
    return 0;
}
```

### Encargo R02-N05-E1 · La factura del mayorista

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un `Pedido` **tiene** un `Cliente` (nombre y si es mayorista) y un vector de
`Linea` (producto, cantidad, precio; con `subtotal()`). Los mayoristas tienen 10%
de descuento sobre el total. La primera línea de la entrada es el cliente
(`nombre minorista|mayorista`) y las siguientes, las líneas del pedido. Imprimí la
factura en columnas con 2 decimales.

#### Criterio de aprobación

- El pedido se construye con su cliente.
- El total se calcula a partir de las líneas.
- El descuento depende del cliente.

#### Entrada de ejemplo

```
Ferreteria mayorista
tornillos 200 12.5
tuercas 150 8
llaves 3 4500
```

#### Salida esperada

```
Cliente: Ferreteria (mayorista)
tornillos    200   2500.00
tuercas      150   1200.00
llaves         3  13500.00
TOTAL             15480.00
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La factura: un Pedido TIENE un Cliente y muchas lineas.
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Cliente {
    std::string nombre;
    bool mayorista = false;
};

struct Linea {
    std::string producto;
    int cantidad = 0;
    double precio = 0;
    double subtotal() const { return cantidad * precio; }
};

class Pedido {
public:
    explicit Pedido(const Cliente& c) : cliente_(c) {}

    void agregar(const Linea& l) { lineas_.push_back(l); }

    double total() const
    {
        double t = 0;
        for (const Linea& l : lineas_) {
            t += l.subtotal();
        }
        return cliente_.mayorista ? t * 0.9 : t;
    }

    void imprimir() const
    {
        std::cout << "Cliente: " << cliente_.nombre << (cliente_.mayorista ? " (mayorista)" : "") << "\n";
        for (const Linea& l : lineas_) {
            std::cout << std::left << std::setw(12) << l.producto << std::right << std::setw(4) << l.cantidad
                      << std::setw(10) << l.subtotal() << "\n";
        }
        std::cout << std::left << std::setw(16) << "TOTAL" << std::right << std::setw(10) << total() << "\n";
    }

private:
    Cliente cliente_;
    std::vector<Linea> lineas_;
};

int main()
{
    std::cout << std::fixed << std::setprecision(2);
    std::string nombre, tipo;
    std::cin >> nombre >> tipo;
    Pedido pedido({nombre, tipo == "mayorista"});
    Linea l;
    while (std::cin >> l.producto >> l.cantidad >> l.precio) {
        pedido.agregar(l);
    }
    pedido.imprimir();
    return 0;
}
```

#### Pruebas

##### Minorista
```entrada
Kiosco minorista
alfajores 24 950
gaseosa 6 1800.5
```
```salida
Cliente: Kiosco
alfajores     24  22800.00
gaseosa        6  10803.00
TOTAL             33603.00
```

##### Mayorista con una sola línea
```entrada
Mayorista mayorista
cable 1000 0.75
```
```salida
Cliente: Mayorista (mayorista)
cable       1000    750.00
TOTAL               675.00
```

### Prueba del sello

#### ¿Qué relación modela la composición? ¿Y la herencia?

La composición, "tiene un"; la herencia, "es un".

#### ¿En qué orden se construyen los miembros de una clase?

En el orden en que están declarados, antes del cuerpo del constructor.

#### ¿Qué significa que `Jugador` "delegue" en su mochila?

Que para guardar un objeto le pide a su mochila que lo haga, en vez de hacerlo él.

#### ¿Por qué conviene preferir composición?

Porque es más flexible: las partes se cambian y se prueban por separado, sin exponer todo.

### Soluciones (docente)

Material original: `03-C++/10-Composicion`, con prácticas nuevas fuera del juego (tienda, tren, factura).

## R02-N06 · Herencia

```meta
tipo: tema
padre: R02-N05
precio: 10
criatura: esqueleto
temas: poo.herencia
```

### Crónica

En el archivo de planos hay una carpeta que dice "Autómata" y, adentro, otras más finas: "Autómata de carga", "Autómata guardián", "Autómata jardinero". Todos comparten el mismo esqueleto; cada uno agrega lo suyo.

—No voy a redibujar el esqueleto cada vez —dice {mentor}—. El autómata de carga **es un** autómata, con brazos más fuertes. Heredo el plano base y le agrego lo que le falta.

### Objetivos

Crear clases **derivadas** que reutilizan una clase **base** (relación "es un"):
llamar al constructor de la base, usar `protected`, agregar datos y métodos,
redefinir un método y llamar a la versión de la base, entender el orden de
construcción y destrucción, la tabla de accesos de la herencia `public`,
`protected` y `private`, y la herencia múltiple.

### Antes de empezar

- Clases, constructores, encapsulamiento y composición (nodos anteriores).

### Explicación

#### "Es un"
```cpp
class Entidad { ... };                  // la base: lo común
class Heroe : public Entidad { ... };   // Heroe ES UNA Entidad
class Enemigo : public Entidad { ... }; // Enemigo ES UNA Entidad
```
`Heroe` **hereda** todo lo público de `Entidad`: puede llamar a `recibir_dano()`,
`vivo()`, `estado()` sin escribirlos de nuevo. Y agrega lo suyo (maná,
experiencia). El `public` de `: public Entidad` dice que lo público de la base
sigue siendo público en la derivada: es el que se usa casi siempre.

#### El constructor de la base
La parte de `Entidad` que hay dentro de un `Heroe` se construye con el constructor
de `Entidad`, y se lo llama **en la lista de inicialización**:
```cpp
Heroe(const std::string& nombre)
    : Entidad(nombre, 120, 18),   // primero, la base
      mana_(50)                   // después, lo propio
{}
```
Orden: **primero la base**, después los miembros propios, después el cuerpo. Al
destruir, al revés: primero la derivada, al final la base.

#### `protected`
| Acceso | Desde la propia clase | Desde una derivada | Desde afuera |
|---|---|---|---|
| `public` | sí | sí | sí |
| `protected` | sí | **sí** | no |
| `private` | sí | **no** | no |

Si `Heroe` necesita tocar `ataque_` para subir de nivel, `ataque_` tiene que ser
`protected` en `Entidad`. Usalo con cuidado: lo `protected` es parte de lo que las
derivadas pueden romper. Si alcanza con métodos, mejor.

#### Redefinir un método y usar el de la base
Una derivada puede escribir un método con el mismo nombre que uno de la base. Para
reutilizar la versión de la base, se la nombra con `Base::`:
```cpp
void Enemigo::estado() const
{
    Entidad::estado();                 // lo que ya hacía la base
    std::cout << ", oro " << oro_;     // y lo propio
}
```

#### Varios niveles
Una derivada puede ser base de otra: `Jefe : Enemigo : Entidad`. Un `Jefe` es un
`Enemigo` y también es una `Entidad`.

#### Herencia `public`, `protected` y `private`
El `public` de `class Heroe : public Entidad` también se puede cambiar. Dice **cómo quedan en la derivada** los miembros que vienen de la base. Es la tabla del apunte de la cátedra:

| En la base es… | con `: public Base` queda | con `: protected Base` queda | con `: private Base` queda |
|---|---|---|---|
| `public` | `public` | `protected` | `private` |
| `protected` | `protected` | `protected` | `private` |
| `private` | inaccesible | inaccesible | inaccesible |

Se lee así: el tipo de herencia es un **techo**. Nada queda más abierto que eso, y lo privado de la base nunca se ve desde la derivada (está adentro del objeto, pero solo lo tocan los métodos de la base).

```cpp
class Motor { public: void arrancar(); };
class Auto : private Motor {             // Auto USA un Motor, pero no ES un Motor para los de afuera
public:
    void andar() { arrancar(); }         // adentro de Auto, arrancar() se puede usar
};
Auto a;
a.andar();        // bien
a.arrancar();     // error: 'arrancar' es private dentro de Auto
```
- Si no escribís nada, `class` hereda **`private`** y `struct` hereda **`public`**. Por eso conviene escribirlo siempre.
- Casi siempre se usa `public` (la relación "es un"). Con `private` lo de afuera no puede tratar a un `Auto` como un `Motor`: para "usa un" casi siempre es más claro un **miembro** (composición, el nodo anterior).

#### Herencia múltiple
Una clase puede tener **varias** bases, separadas con comas:
```cpp
class Volador { public: void volar() const; };
class Nadador { public: void nadar() const; };
class Pato : public Volador, public Nadador { };    // un Pato vuela y nada
```
Las bases se construyen en el orden en que están escritas (`Volador`, después `Nadador`). Si dos bases tienen un método con el mismo nombre, hay que decir cuál: `p.Volador::mover()`. Se usa poco (y con cuidado): lo más común es una base con datos y otras que solo piden métodos, como las interfaces de Java.

#### Una limitación (que resuelve el nodo siguiente)
Sin nada más, cuando una función recibe una `Entidad&` y llama a `estado()`, se
ejecuta **siempre** la versión de `Entidad`, aunque el objeto sea un `Enemigo`. Para
que se elija la versión **del tipo real** hace falta `virtual`: eso es el
**polimorfismo**, el próximo nodo.

> **Si venís de C.** En C se imitaba poniendo el struct base como primer campo y
> casteando punteros a mano. En C++ es parte del lenguaje, y el compilador controla
> los tipos.

### Código de ejemplo

```cpp
/*
 * Herencia: una clase derivada REUTILIZA una base y agrega lo suyo.
 *   Entidad            <- lo comun a todo lo que vive y pelea
 *     |-- Heroe        <- agrega: mana y experiencia
 *     |-- Enemigo      <- agrega: oro que suelta
 */
#include <algorithm>
#include <iostream>
#include <string>

class Entidad {
public:
    Entidad(const std::string& nombre, int vida, int ataque)
        : nombre_(nombre), vida_(vida), vida_max_(vida), ataque_(ataque)
    {
    }

    void recibir_dano(int n)
    {
        vida_ = std::max(0, vida_ - n);
    }

    bool vivo() const { return vida_ > 0; }
    const std::string& nombre() const { return nombre_; }
    int ataque() const { return ataque_; }

    void estado() const
    {
        std::cout << "  " << nombre_ << ": vida " << vida_ << "/" << vida_max_ << ", ataque " << ataque_ << "\n";
    }

protected:            // como private, pero las derivadas SI lo ven
    std::string nombre_;
    int vida_;
    int vida_max_;
    int ataque_;
};

// Heroe ES UNA Entidad, con mana y experiencia.
class Heroe : public Entidad {
public:
    explicit Heroe(const std::string& nombre)
        : Entidad(nombre, 120, 18),       // primero se construye la parte de Entidad
          mana_(50)
    {
    }

    void ganar_exp(int n)
    {
        exp_ += n;
        while (exp_ >= 100) {
            exp_ -= 100;
            subir_nivel();
        }
    }

    int exp() const { return exp_; }

private:
    void subir_nivel()
    {
        ataque_ += 3;                     // protected: la derivada lo puede tocar
        vida_max_ += 20;
        vida_ = vida_max_;
        std::cout << "  ¡" << nombre_ << " sube de nivel! ataque " << ataque_ << "\n";
    }

    int mana_;
    int exp_ = 0;
};

// Enemigo ES UNA Entidad, que suelta oro.
class Enemigo : public Entidad {
public:
    Enemigo(const std::string& nombre, int vida, int ataque, int oro)
        : Entidad(nombre, vida, ataque), oro_(oro)
    {
    }

    int oro() const { return oro_; }

private:
    int oro_;
};

int main()
{
    Heroe kira("Kira");
    Enemigo goblin("Goblin", 30, 9, 12);
    kira.estado();             // metodo heredado de Entidad
    goblin.estado();

    std::cout << "\nKira golpea al Goblin por " << kira.ataque() << ", dos veces:\n";
    goblin.recibir_dano(kira.ataque());
    goblin.recibir_dano(kira.ataque());
    goblin.estado();

    if (!goblin.vivo()) {
        std::cout << "\nGoblin derrotado: suelta " << goblin.oro() << " de oro.\n";
        kira.ganar_exp(80);
        kira.ganar_exp(50);
    }
    std::cout << "\nKira (exp " << kira.exp() << "):\n";
    kira.estado();
    return 0;
}
```

### Salida esperada

```
  Kira: vida 120/120, ataque 18
  Goblin: vida 30/30, ataque 9

Kira golpea al Goblin por 18, dos veces:
  Goblin: vida 0/30, ataque 9

Goblin derrotado: suelta 12 de oro.
  ¡Kira sube de nivel! ataque 21

Kira (exp 30):
  Kira: vida 140/140, ataque 21
```

### ¿Para qué sirve?

La herencia organiza familias de cosas que comparten comportamiento: tipos de cuentas bancarias (caja de ahorro, cuenta corriente), empleados con distintas formas de cobrar, vehículos, figuras geométricas, enemigos de un juego. Los frameworks la usan muchísimo: en Qt, cada ventana hereda de `QWidget`; en un motor de juegos, cada objeto hereda de una clase base de la escena.

### Errores habituales

**Esqueleto: la base no tiene constructor sin parámetros.** Si la derivada no
llama al constructor de la base, C++ busca uno vacío:
```
main.cpp:3:34: error: no matching function for call to ‘Entidad::Entidad()’
main.cpp:2:19: note: candidate: ‘Entidad::Entidad(const std::string&)’
```
Llamalo en la lista de inicialización.

**Esqueleto: tocar algo `private` de la base.**
```
main.cpp:2:55: error: ‘int Entidad::vida_’ is private within this context
```
Si la derivada lo necesita, `protected` (o, mejor, un método de la base).

**Esqueleto: tocar algo `protected` desde afuera.**
```
main.cpp:3:28: error: ‘int Entidad::vida_’ is protected within this context
```

**Ogro: herencia donde iba composición.** `class Auto : public Motor` dice que un
auto **es** un motor. Si la frase "X es un Y" suena rara, es composición.

**Ogro: redefinir y olvidar la base.** Una `Jefe::recibir_dano` que no llama a
`Entidad::recibir_dano` y resta la vida a mano puede saltearse las reglas de la base
(como no bajar de 0).

### Misión R02-N06-M1 · Los vehículos de la Ciudadela

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Vehiculo` (patente, ruedas, consumo cada 100 km; `ficha()` y
`combustible_para(km)`), y dos derivadas: `Auto` (4 ruedas, 7.5 l/100 km, con
cantidad de asientos y `costo_por_persona(km, precio_litro)`) y `Moto` (2 ruedas y
3 l, o 3 ruedas y 4.5 l si tiene sidecar; con `hacer_willy()`). Probá con un auto de
5 asientos y dos motos, una con sidecar.

#### Criterio de aprobación

- Las derivadas llaman al constructor de la base con los valores que corresponden.
- Usan los métodos heredados sin reescribirlos.

#### Salida esperada

```
AB123CD: 4 ruedas, 7.5 l/100 km
A012BCD: 2 ruedas, 3 l/100 km
A999ZZZ: 3 ruedas, 4.5 l/100 km
Para 300 km: auto 22.5 l, moto 9 l
Costo por persona en auto (300 km, $1200 el litro): $5400
A012BCD levanta la rueda de adelante
```

#### Solución de referencia

```cpp
// Mision 1 - Los vehiculos de la Ciudadela: una base y dos derivadas.
#include <iostream>
#include <string>

class Vehiculo {
public:
    Vehiculo(const std::string& patente, int ruedas, double consumo_cada_100)
        : patente_(patente), ruedas_(ruedas), consumo_(consumo_cada_100)
    {
    }

    double combustible_para(double km) const { return km * consumo_ / 100; }

    void ficha() const
    {
        std::cout << patente_ << ": " << ruedas_ << " ruedas, " << consumo_ << " l/100 km\n";
    }

protected:
    std::string patente_;
    int ruedas_;
    double consumo_;
};

class Auto : public Vehiculo {
public:
    Auto(const std::string& patente, int asientos) : Vehiculo(patente, 4, 7.5), asientos_(asientos) {}

    double costo_por_persona(double km, double precio_litro) const
    {
        return combustible_para(km) * precio_litro / asientos_;
    }

private:
    int asientos_;
};

class Moto : public Vehiculo {
public:
    Moto(const std::string& patente, bool con_sidecar)
        : Vehiculo(patente, con_sidecar ? 3 : 2, con_sidecar ? 4.5 : 3.0)
    {
    }

    void hacer_willy() const { std::cout << patente_ << " levanta la rueda de adelante\n"; }
};

int main()
{
    Auto familiar("AB123CD", 5);
    Moto rapida("A012BCD", false);
    Moto carga("A999ZZZ", true);
    familiar.ficha();
    rapida.ficha();
    carga.ficha();
    std::cout << "Para 300 km: auto " << familiar.combustible_para(300) << " l, moto "
              << rapida.combustible_para(300) << " l\n";
    std::cout << "Costo por persona en auto (300 km, $1200 el litro): $"
              << familiar.costo_por_persona(300, 1200) << "\n";
    rapida.hacer_willy();
    return 0;
}
```

### Misión R02-N06-M2 · El Jefe que se enfurece

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Armá tres niveles: `Entidad` → `Enemigo` (con oro) → `Jefe` (con fase). `Enemigo`
y `Jefe` redefinen `estado()` llamando a la versión de su base y agregando lo suyo.
`Jefe::recibir_dano` usa la de `Entidad` y, la **primera vez** que la vida queda en
la mitad o menos (y sigue viva), pasa a fase 2: duplica el ataque y triplica el oro.
Creá una Quimera (100 de vida, 12 de ataque, 100 de oro); cada número de la entrada
es un golpe, mientras siga viva.

#### Criterio de aprobación

- Cada `estado()` reutiliza el de su base con `Base::estado()`.
- El enfurecimiento pasa una sola vez.
- `Jefe` no resta la vida a mano: usa la de `Entidad`.

#### Entrada de ejemplo

```
20 25 10 30 40
```

#### Salida esperada

```
Quimera: vida 80/100, ataque 12, oro 100, fase 1
Quimera: vida 55/100, ataque 12, oro 100, fase 1
¡Quimera se enfurece!
Quimera: vida 45/100, ataque 24, oro 300, fase 2
Quimera: vida 15/100, ataque 24, oro 300, fase 2
Quimera: vida 0/100, ataque 24, oro 300, fase 2
La Quimera cae.
```

#### Solución de referencia

```cpp
// Mision 2 - El Jefe: una derivada de una derivada, que usa la version de la base.
#include <algorithm>
#include <iostream>
#include <string>

class Entidad {
public:
    Entidad(const std::string& nombre, int vida, int ataque)
        : nombre_(nombre), vida_(vida), vida_max_(vida), ataque_(ataque)
    {
    }

    void recibir_dano(int n) { vida_ = std::max(0, vida_ - n); }
    bool vivo() const { return vida_ > 0; }

    void estado() const
    {
        std::cout << nombre_ << ": vida " << vida_ << "/" << vida_max_ << ", ataque " << ataque_;
    }

protected:
    std::string nombre_;
    int vida_;
    int vida_max_;
    int ataque_;
};

class Enemigo : public Entidad {
public:
    Enemigo(const std::string& nombre, int vida, int ataque, int oro) : Entidad(nombre, vida, ataque), oro_(oro) {}
    int oro() const { return oro_; }

    void estado() const
    {
        Entidad::estado();                     // la version de la base, y despues lo propio
        std::cout << ", oro " << oro_;
    }

protected:
    int oro_;
};

class Jefe : public Enemigo {
public:
    Jefe(const std::string& nombre, int vida, int ataque) : Enemigo(nombre, vida, ataque, 100) {}

    void recibir_dano(int n)
    {
        Entidad::recibir_dano(n);
        if (fase_ == 1 && vida_ <= vida_max_ / 2 && vivo()) {
            fase_ = 2;
            ataque_ *= 2;
            oro_ *= 3;
            std::cout << "¡" << nombre_ << " se enfurece!\n";
        }
    }

    void estado() const
    {
        Enemigo::estado();
        std::cout << ", fase " << fase_;
    }

private:
    int fase_ = 1;
};

int main()
{
    Jefe quimera("Quimera", 100, 12);
    int golpe = 0;
    while (std::cin >> golpe && quimera.vivo()) {
        quimera.recibir_dano(golpe);
        quimera.estado();
        std::cout << "\n";
    }
    std::cout << (quimera.vivo() ? "La Quimera resiste." : "La Quimera cae.") << "\n";
    return 0;
}
```

#### Pruebas

##### Muere de un golpe
```entrada
150
```
```salida
Quimera: vida 0/100, ataque 12, oro 100, fase 1
La Quimera cae.
```

##### Justo la mitad
```entrada
50 10 10
```
```salida
¡Quimera se enfurece!
Quimera: vida 50/100, ataque 24, oro 300, fase 2
Quimera: vida 40/100, ataque 24, oro 300, fase 2
Quimera: vida 30/100, ataque 24, oro 300, fase 2
La Quimera resiste.
```

##### Golpes que no la matan
```entrada
5 5 5
```
```salida
Quimera: vida 95/100, ataque 12, oro 100, fase 1
Quimera: vida 90/100, ataque 12, oro 100, fase 1
Quimera: vida 85/100, ataque 12, oro 100, fase 1
La Quimera resiste.
```

### Misión R02-N06-M3 · Tres generaciones

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `Base`, `Derivada : Base` y `Nieta : Derivada`, cada una con un constructor
y un destructor que muestran un mensaje (`Base` recibe un texto en su
constructor). Creá una `Nieta` dentro de un bloque. **Antes de ejecutar**, escribí
el orden que esperás. ¿Por qué `Nieta` no llama explícitamente a `Base`?

#### Criterio de aprobación

- `Derivada` llama al constructor de `Base` con un texto.
- La salida muestra la construcción de la base hacia la nieta y la destrucción al revés.

#### Salida esperada

```
Nace una nieta:
  base de derivada
  cuerpo de derivada
  cuerpo de nieta
Muere la nieta:
  ~nieta
  ~derivada
  ~base
```

#### Solución de referencia

```cpp
// Mision 3 - El orden de construccion y destruccion con herencia.
#include <iostream>
#include <string>

class Base {
public:
    explicit Base(const std::string& quien) { std::cout << "  base de " << quien << "\n"; }
    ~Base() { std::cout << "  ~base\n"; }
};

class Derivada : public Base {
public:
    Derivada() : Base("derivada") { std::cout << "  cuerpo de derivada\n"; }
    ~Derivada() { std::cout << "  ~derivada\n"; }
};

class Nieta : public Derivada {
public:
    Nieta() { std::cout << "  cuerpo de nieta\n"; }
    ~Nieta() { std::cout << "  ~nieta\n"; }
};

int main()
{
    std::cout << "Nace una nieta:\n";
    {
        Nieta n;
        std::cout << "Muere la nieta:\n";
    }
    return 0;
}
```

### Encargo R02-N06-E1 · Los sueldos de la empresa

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Escribí `class Empleado` (nombre, básico; `aportes()` es el 17% del básico y
`sueldo()` el básico menos los aportes) y dos derivadas: `Vendedor` (suma 5% de sus
ventas) y `Encargado` (suma $15000 por persona a cargo). Cada una redefine
`sueldo()` usando `Empleado::sueldo()`. Mostrá los sueldos de Ana (empleada,
$800000), Bruno (vendedor, $700000, ventas $3000000) y Celi (encargada, $1000000,
6 personas), y los aportes de Celi.

#### Criterio de aprobación

- Las derivadas reutilizan `Empleado::sueldo()`.
- Los aportes se heredan sin cambios.

#### Salida esperada

```
Ana: $664000.00
Bruno: $731000.00
Celi: $920000.00
Aportes de Celi: $170000.00
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Empleados: la base calcula el sueldo basico; cada derivada suma lo suyo.
#include <iomanip>
#include <iostream>
#include <string>

class Empleado {
public:
    Empleado(const std::string& nombre, double basico) : nombre_(nombre), basico_(basico) {}

    double sueldo() const { return basico_ - aportes(); }
    double aportes() const { return basico_ * 0.17; }
    const std::string& nombre() const { return nombre_; }

protected:
    std::string nombre_;
    double basico_;
};

class Vendedor : public Empleado {
public:
    Vendedor(const std::string& nombre, double basico, double ventas)
        : Empleado(nombre, basico), ventas_(ventas)
    {
    }

    double sueldo() const { return Empleado::sueldo() + ventas_ * 0.05; }

private:
    double ventas_;
};

class Encargado : public Empleado {
public:
    Encargado(const std::string& nombre, double basico, int personas)
        : Empleado(nombre, basico), personas_(personas)
    {
    }

    double sueldo() const { return Empleado::sueldo() + personas_ * 15000; }

private:
    int personas_;
};

int main()
{
    std::cout << std::fixed << std::setprecision(2);
    Empleado ana("Ana", 800000);
    Vendedor bruno("Bruno", 700000, 3000000);
    Encargado celi("Celi", 1000000, 6);
    std::cout << ana.nombre() << ": $" << ana.sueldo() << "\n";
    std::cout << bruno.nombre() << ": $" << bruno.sueldo() << "\n";
    std::cout << celi.nombre() << ": $" << celi.sueldo() << "\n";
    std::cout << "Aportes de Celi: $" << celi.aportes() << "\n";
    return 0;
}
```

### Prueba del sello

#### En `class B : protected A`, ¿cómo queda en `B` un método `public` de `A`?

`protected`: lo pueden usar `B` y sus derivadas, pero no los de afuera.

#### Si `A` tiene un dato `private`, ¿puede usarlo un método de una clase derivada?

No, con ningún tipo de herencia: está dentro del objeto, pero solo lo tocan los métodos de `A` (o se lo hace `protected`).

#### ¿Qué herencia usa `class B : A` si no se escribe nada?

`private` (con `struct`, sería `public`).

#### ¿Qué hereda `class Heroe : public Entidad`?

Todos los miembros de `Entidad`; puede usar directamente los públicos y los protegidos.

#### ¿Dónde se llama al constructor de la base?

En la lista de inicialización del constructor de la derivada.

#### ¿En qué orden se construyen la base y la derivada? ¿Y se destruyen?

Se construye primero la base y después la derivada; se destruyen al revés.

#### ¿Qué diferencia hay entre `protected` y `private`?

Las derivadas pueden acceder a lo `protected`, pero no a lo `private`.

#### ¿Cómo llama una derivada a la versión de la base de un método que redefinió?

Con el nombre de la base: `Entidad::estado()`.

### Soluciones (docente)

Material original: `03-C++/08-Herencia`, con prácticas nuevas. A propósito todavía no hay `virtual`: la limitación se menciona y se resuelve en Polimorfismo.

## R02-N07 · Polimorfismo

```meta
tipo: tema
padre: R02-N06
precio: 10
criatura: ogro
temas: poo.polimorfismo, poo.abstractas
```

### Crónica

En el patio, Tesla le da la misma orden a tres autómatas distintos: "¡Trabajá!". El de carga levanta cajas. El soldador enciende una chispa. El jardinero riega las macetas.

—Una orden, tres respuestas —sonríe—. Yo no necesito saber qué autómata tengo adelante: le digo "trabajá" y cada uno sabe cómo. Esa es la magia más poderosa de la Ciudadela: **polimorfismo**, "muchas formas".

### Objetivos

Hacer que un mismo llamado ejecute la versión del **tipo real** del objeto:
métodos `virtual`, `override`, métodos virtuales puros y clases abstractas,
destructor virtual, y colecciones de objetos de distintos tipos con
`std::vector<std::unique_ptr<Base>>`. Reconocer el "rebanado" de objetos.

### Antes de empezar

- Herencia (Herencia).
- Referencias y un vistazo a los punteros (Referencias).

### Explicación

#### El problema
Con herencia sola, si una función recibe `const Entidad& e` y llama a
`e.grito()`, se ejecuta **siempre** el `grito()` de `Entidad`, aunque le hayas
pasado un `Guerrero`. El compilador solo mira el tipo **declarado**.

#### `virtual`: elegir según el tipo real
```cpp
class Entidad {
public:
    virtual ~Entidad() = default;
    virtual std::string grito() const { return "..."; }
};
class Guerrero : public Entidad {
public:
    std::string grito() const override { return "¡Por la Ciudadela!"; }
};

void presentar(const Entidad& e) { std::cout << e.grito(); }
presentar(Guerrero{...});   // "¡Por la Ciudadela!"
```
Con `virtual`, cuando se llama por **referencia o puntero a la base**, se ejecuta
la versión del tipo **real** del objeto. Eso es **polimorfismo**: el mismo código
(`e.grito()`) hace cosas distintas según el objeto.

#### `override`: que el compilador controle
En la derivada, `override` dice "estoy redefiniendo un virtual de la base". Si te
equivocás en la firma (un `const` de menos, otro tipo de parámetro), **no compila**.
Sin `override`, habrías creado un método nuevo sin darte cuenta. **Ponelo siempre.**

#### Virtual puro y clases abstractas
```cpp
virtual int ataque() const = 0;
```
El `= 0` dice "la base **no** tiene versión: cada derivada tiene que dar la suya".
Una clase con al menos un virtual puro es **abstracta**: no se pueden crear objetos
de ella (`Entidad e;` no compila), solo de sus derivadas que definan todo. Sirve
para describir **qué** tiene que saber hacer cualquier cosa de esa familia.

#### El destructor virtual
Si vas a destruir derivadas **a través de un puntero a la base** (y lo vas a hacer
con `unique_ptr<Base>`), la base **tiene** que tener destructor virtual:
```cpp
virtual ~Entidad() = default;
```
Sin él, solo se destruye la parte de la base: comportamiento indefinido. Regla: **si
una clase tiene algún método virtual, su destructor es virtual.**

#### Colecciones de objetos de distintos tipos
Un `std::vector<Entidad>` no sirve: cada lugar tiene el tamaño de una `Entidad`, y
un `Guerrero` no entra (se rebana, ver abajo). Se guardan **punteros a la base**:
```cpp
std::vector<std::unique_ptr<Entidad>> grupo;
grupo.push_back(std::make_unique<Guerrero>("Bron"));
grupo.push_back(std::make_unique<Arquera>("Lyn"));
for (const std::unique_ptr<Entidad>& e : grupo) {
    e->atacar(blanco);        // -> para llamar a un método a través de un puntero
}
```
`std::unique_ptr<T>` (de `<memory>`) es un puntero **dueño** de su objeto: cuando el
puntero se destruye (por ejemplo, al destruirse el vector), borra el objeto. No hay
que hacer nada más. `std::make_unique<Guerrero>(args)` crea el objeto con esos
argumentos. En la rama 3 lo vas a ver a fondo; por ahora usalo como receta.

#### El rebanado (*slicing*)
Si pasás una derivada **por valor** a algo que espera la base, se copia **solo la
parte de la base**: el objeto se "rebana" y pierde su tipo real.
```cpp
void por_valor(Pieza p);          // recibe una copia de la parte Pieza
por_valor(engranaje);             // llama a Pieza::describir, no a la de Engranaje
```
Por eso el polimorfismo siempre va **por referencia o por puntero**.

> **Si venís de C.** En C se imitaba con punteros a función dentro de los structs
> (una "tabla" de funciones armada a mano). `virtual` hace exactamente eso, pero lo
> arma y lo controla el compilador.

### Código de ejemplo

```cpp
/*
 * Polimorfismo: el mismo llamado, y cada objeto responde a su manera.
 */
#include <iostream>
#include <memory>    // std::unique_ptr, std::make_unique
#include <string>
#include <vector>

class Entidad {
public:
    explicit Entidad(const std::string& nombre, int vida) : nombre_(nombre), vida_(vida) {}
    virtual ~Entidad() = default;          // destructor virtual: OBLIGATORIO en una base polimorfica

    // virtual puro (= 0): cada derivada TIENE que definirlo. Entidad pasa a ser abstracta.
    virtual int ataque() const = 0;

    // virtual con una version por defecto: la derivada PUEDE redefinirlo.
    virtual std::string grito() const { return "..."; }

    // No virtual: igual para todos. Pero llama a metodos virtuales.
    void atacar(Entidad& objetivo) const
    {
        std::cout << "  " << nombre_ << " (\"" << grito() << "\") ataca a " << objetivo.nombre_
                  << " por " << ataque() << "\n";
        objetivo.vida_ -= ataque();
    }

    bool vivo() const { return vida_ > 0; }
    const std::string& nombre() const { return nombre_; }

protected:
    std::string nombre_;
    int vida_;
};

class Guerrero : public Entidad {
public:
    explicit Guerrero(const std::string& nombre) : Entidad(nombre, 140) {}
    int ataque() const override { return 20; }                  // override: "redefino un virtual"
    std::string grito() const override { return "¡Por la Ciudadela!"; }
};

class Arquera : public Entidad {
public:
    explicit Arquera(const std::string& nombre) : Entidad(nombre, 90) {}
    int ataque() const override { return 14; }
    std::string grito() const override { return "*silba una flecha*"; }
};

class Slime : public Entidad {
public:
    Slime() : Entidad("Slime", 60) {}
    int ataque() const override { return 5; }
    // no redefine grito(): usa el "..." de la base
};

// Recibe CUALQUIER Entidad por referencia: se ejecuta la version del tipo REAL.
void presentar(const Entidad& e)
{
    std::cout << e.nombre() << " grita: " << e.grito() << "\n";
}

int main()
{
    Guerrero bron("Bron");
    Arquera lyn("Lyn");
    Slime blanco;
    presentar(bron);
    presentar(lyn);
    presentar(blanco);

    // Un vector de objetos de TIPOS DISTINTOS: se guardan punteros a la base.
    // std::unique_ptr es un puntero que borra solo su objeto (lo ves a fondo en la rama 3).
    std::vector<std::unique_ptr<Entidad>> grupo;
    grupo.push_back(std::make_unique<Guerrero>("Bron"));
    grupo.push_back(std::make_unique<Arquera>("Lyn"));
    grupo.push_back(std::make_unique<Slime>());

    std::cout << "\nCada uno ataca al Slime de prueba:\n";
    for (const std::unique_ptr<Entidad>& e : grupo) {
        e->atacar(blanco);             // -> : un metodo del objeto apuntado
    }
    std::cout << "El Slime de prueba " << (blanco.vivo() ? "sigue vivo" : "cae") << ".\n";
    // Entidad e("x", 1);   // ERROR: Entidad es abstracta
    return 0;
}
```

### Salida esperada

```
Bron grita: ¡Por la Ciudadela!
Lyn grita: *silba una flecha*
Slime grita: ...

Cada uno ataca al Slime de prueba:
  Bron ("¡Por la Ciudadela!") ataca a Slime por 20
  Lyn ("*silba una flecha*") ataca a Slime por 14
  Slime ("...") ataca a Slime por 5
El Slime de prueba sigue vivo.
```

### ¿Para qué sirve?

El polimorfismo permite escribir código que funciona con tipos que todavía no existen: una función `dibujar_todo(const std::vector<std::unique_ptr<Figura>>&)` sirve para cualquier figura futura. Así funcionan los sistemas de plugins, los medios de pago de una tienda (efectivo, tarjeta, transferencia), los formatos de exportación (PDF, Excel, CSV), los distintos enemigos de un juego y los widgets de una interfaz gráfica.

### Errores habituales

**Esqueleto: crear un objeto de una clase abstracta.**
```
main.cpp:2:16: error: cannot declare variable ‘f’ to be of abstract type ‘Figura’
main.cpp:1:8: note:   because the following virtual functions are pure within ‘Figura’:
main.cpp:1:51: note:     ‘virtual double Figura::area() const’
```
También pasa si una derivada **se olvidó** de definir algún virtual puro: la nota
dice cuál falta.

**Goblin: `override` que no redefine nada.** Te faltó el `const`:
```
main.cpp:2:23: error: ‘double Circulo::area()’ marked ‘override’, but does not override
```
Gracias a `override` te enterás; sin él, compilaría y el polimorfismo no andaría.

**Troll: base polimórfica sin destructor virtual.**
```
main.cpp:4:28: warning: deleting object of polymorphic class type ‘Figura’ which has non-virtual destructor might cause undefined behavior [-Wdelete-non-virtual-dtor]
```

**Ogro: el rebanado.** `std::vector<Entidad>` o un parámetro `Entidad e` por valor:
todos terminan comportándose como la base. Referencias o punteros.

**Ogro: olvidar `virtual` en la base.** Compila sin avisos y cada llamado por la
base ejecuta la versión de la base. Con `override` en las derivadas, el compilador
te lo marca.

### Misión R02-N07-M1 · Las figuras del vitral

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Figura` **abstracta** con `area()`, `perimetro()` y `nombre()`
virtuales puros, y tres derivadas: `Circulo(r)`, `Rectangulo(a, b)` (que se llama
"cuadrado" si los lados son iguales) y `Triangulo(a, b, c)` (área con la fórmula de
Herón: `s = perímetro / 2`, `área = √(s(s−a)(s−b)(s−c))`). La entrada trae figuras
como `c 2`, `r 3 4`, `t 3 4 5`. Guardalas en un
`std::vector<std::unique_ptr<Figura>>` y mostrá cada una, el área total y la más
grande. Todo con 2 decimales.

#### Criterio de aprobación

- `Figura` es abstracta y tiene destructor virtual.
- Las derivadas usan `override`.
- El recorrido no pregunta el tipo: llama a los métodos virtuales.

#### Entrada de ejemplo

```
c 2
r 3 4
t 3 4 5
r 5 5
c 0.5
```

#### Salida esperada

```
círculo: área 12.57, perímetro 12.57
rectángulo: área 12.00, perímetro 14.00
triángulo: área 6.00, perímetro 12.00
cuadrado: área 25.00, perímetro 20.00
círculo: área 0.79, perímetro 3.14
Vidrio total: 56.35
La pieza más grande: cuadrado
```

#### Solución de referencia

```cpp
// Mision 1 - Las figuras del vitral: una base abstracta y tres derivadas.
#include <cmath>
#include <iomanip>
#include <iostream>
#include <memory>
#include <numbers>
#include <string>
#include <vector>

class Figura {
public:
    virtual ~Figura() = default;
    virtual double area() const = 0;
    virtual double perimetro() const = 0;
    virtual std::string nombre() const = 0;
};

class Circulo : public Figura {
public:
    explicit Circulo(double r) : r_(r) {}
    double area() const override { return std::numbers::pi * r_ * r_; }
    double perimetro() const override { return 2 * std::numbers::pi * r_; }
    std::string nombre() const override { return "círculo"; }

private:
    double r_;
};

class Rectangulo : public Figura {
public:
    Rectangulo(double a, double b) : a_(a), b_(b) {}
    double area() const override { return a_ * b_; }
    double perimetro() const override { return 2 * (a_ + b_); }
    std::string nombre() const override { return a_ == b_ ? "cuadrado" : "rectángulo"; }

private:
    double a_;
    double b_;
};

class Triangulo : public Figura {
public:
    Triangulo(double a, double b, double c) : a_(a), b_(b), c_(c) {}
    double perimetro() const override { return a_ + b_ + c_; }
    double area() const override
    {
        double s = perimetro() / 2;                        // formula de Heron
        return std::sqrt(s * (s - a_) * (s - b_) * (s - c_));
    }
    std::string nombre() const override { return "triángulo"; }

private:
    double a_;
    double b_;
    double c_;
};

int main()
{
    std::vector<std::unique_ptr<Figura>> vitral;
    std::string tipo;
    while (std::cin >> tipo) {
        if (tipo == "c") {
            double r = 0;
            std::cin >> r;
            vitral.push_back(std::make_unique<Circulo>(r));
        } else if (tipo == "r") {
            double a = 0, b = 0;
            std::cin >> a >> b;
            vitral.push_back(std::make_unique<Rectangulo>(a, b));
        } else if (tipo == "t") {
            double a = 0, b = 0, c = 0;
            std::cin >> a >> b >> c;
            vitral.push_back(std::make_unique<Triangulo>(a, b, c));
        }
    }
    std::cout << std::fixed << std::setprecision(2);
    double total = 0;
    const Figura* mayor = nullptr;
    for (const std::unique_ptr<Figura>& f : vitral) {
        std::cout << f->nombre() << ": área " << f->area() << ", perímetro " << f->perimetro() << "\n";
        total += f->area();
        if (mayor == nullptr || f->area() > mayor->area()) {
            mayor = f.get();
        }
    }
    std::cout << "Vidrio total: " << total << "\n";
    if (mayor != nullptr) {
        std::cout << "La pieza más grande: " << mayor->nombre() << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Una sola figura
```entrada
t 5 5 5
```
```salida
triángulo: área 10.83, perímetro 15.00
Vidrio total: 10.83
La pieza más grande: triángulo
```

##### Empate en la más grande
```entrada
r 2 8
r 4 4
c 1
```
```salida
rectángulo: área 16.00, perímetro 20.00
cuadrado: área 16.00, perímetro 16.00
círculo: área 3.14, perímetro 6.28
Vidrio total: 35.14
La pieza más grande: rectángulo
```

### Misión R02-N07-M2 · La cuadrilla de autómatas

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Automata` abstracta con `trabajar()` (produce algo en una hora y lo
devuelve) y `costo_por_hora()`. Tres tipos:
- **Cargador**: produce 30 por hora, cuesta 12.
- **Soldador**: produce 45, pero cada tercera hora se enfría y produce 0; cuesta 20.
- **Aprendiz**: la primera hora produce 5 y cada hora produce 5 más; cuesta 4.

Leé la cantidad de horas y, para cada autómata de la cuadrilla, mostrá cuánto
produjo, cuánto costó y cuánto rinde (producción − costo). Probá heredar el
constructor con `using Automata::Automata;`.

#### Criterio de aprobación

- `trabajar()` no es `const`: algunos autómatas guardan estado.
- La cuadrilla es un vector de `unique_ptr<Automata>`.

#### Entrada de ejemplo

```
6
```

#### Salida esperada

```
Cargo-1: produjo 180, costó 72, rinde 108
Chispa: produjo 180, costó 120, rinde 60
Tuerca: produjo 105, costó 24, rinde 81
```

#### Solución de referencia

```cpp
// Mision 2 - La cuadrilla de automatas: cada tipo trabaja distinto.
#include <iostream>
#include <memory>
#include <string>
#include <vector>

class Automata {
public:
    explicit Automata(const std::string& nombre) : nombre_(nombre) {}
    virtual ~Automata() = default;

    // Hace su trabajo de una hora y devuelve cuanto produjo.
    virtual int trabajar() = 0;
    virtual int costo_por_hora() const = 0;

    const std::string& nombre() const { return nombre_; }

private:
    std::string nombre_;
};

class Cargador : public Automata {
public:
    using Automata::Automata;              // hereda el constructor de la base
    int trabajar() override { return 30; }
    int costo_por_hora() const override { return 12; }
};

class Soldador : public Automata {
public:
    using Automata::Automata;
    int trabajar() override
    {
        horas_++;
        return horas_ % 3 == 0 ? 0 : 45;   // cada tres horas se enfria y no produce
    }
    int costo_por_hora() const override { return 20; }

private:
    int horas_ = 0;
};

class Aprendiz : public Automata {
public:
    using Automata::Automata;
    int trabajar() override
    {
        ritmo_ += 5;                       // aprende: cada hora produce mas
        return ritmo_;
    }
    int costo_por_hora() const override { return 4; }

private:
    int ritmo_ = 0;
};

int main()
{
    std::vector<std::unique_ptr<Automata>> cuadrilla;
    cuadrilla.push_back(std::make_unique<Cargador>("Cargo-1"));
    cuadrilla.push_back(std::make_unique<Soldador>("Chispa"));
    cuadrilla.push_back(std::make_unique<Aprendiz>("Tuerca"));

    int horas = 0;
    std::cin >> horas;
    for (const std::unique_ptr<Automata>& a : cuadrilla) {
        int produccion = 0;
        for (int h = 0; h < horas; h++) {
            produccion += a->trabajar();
        }
        int costo = a->costo_por_hora() * horas;
        std::cout << a->nombre() << ": produjo " << produccion << ", costó " << costo
                  << ", rinde " << produccion - costo << "\n";
    }
    return 0;
}
```

#### Pruebas

##### Una hora
```entrada
1
```
```salida
Cargo-1: produjo 30, costó 12, rinde 18
Chispa: produjo 45, costó 20, rinde 25
Tuerca: produjo 5, costó 4, rinde 1
```

##### Tres horas (el soldador se enfría)
```entrada
3
```
```salida
Cargo-1: produjo 90, costó 36, rinde 54
Chispa: produjo 90, costó 60, rinde 30
Tuerca: produjo 30, costó 12, rinde 18
```

##### Diez horas
```entrada
10
```
```salida
Cargo-1: produjo 300, costó 120, rinde 180
Chispa: produjo 315, costó 200, rinde 115
Tuerca: produjo 275, costó 40, rinde 235
```

### Misión R02-N07-M3 · El rebanado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `class Pieza` con `virtual describir()` y `class Engranaje` que lo
redefine. Pasale un engranaje a tres funciones: una que recibe `Pieza` **por
valor**, otra por `const Pieza&` y otra por `const Pieza*`. Después, copiá el
engranaje en una variable `Pieza`. **Antes de ejecutar**, anotá qué va a mostrar
cada una. Explicá en un comentario por qué la primera y la última "se equivocan".

#### Criterio de aprobación

- Muestra las cuatro formas.
- El comentario explica el rebanado.

#### Salida esperada

```
por valor:      una pieza cualquiera
por referencia: un engranaje de 24 dientes
por puntero:    un engranaje de 24 dientes
copia:          una pieza cualquiera
```

#### Solución de referencia

```cpp
// Mision 3 - El rebanado: por valor se pierde el tipo real; por referencia, no.
#include <iostream>
#include <string>

class Pieza {
public:
    virtual ~Pieza() = default;
    virtual std::string describir() const { return "una pieza cualquiera"; }
};

class Engranaje : public Pieza {
public:
    std::string describir() const override { return "un engranaje de 24 dientes"; }
};

void por_valor(Pieza p)          // se COPIA solo la parte Pieza: se "rebana"
{
    std::cout << "por valor:      " << p.describir() << "\n";
}

void por_referencia(const Pieza& p)
{
    std::cout << "por referencia: " << p.describir() << "\n";
}

void por_puntero(const Pieza* p)
{
    std::cout << "por puntero:    " << p->describir() << "\n";
}

int main()
{
    Engranaje e;
    por_valor(e);
    por_referencia(e);
    por_puntero(&e);
    Pieza copia = e;             // otra vez: la copia es solo una Pieza
    std::cout << "copia:          " << copia.describir() << "\n";
    return 0;
}
```

### Encargo R02-N07-E1 · Los medios de pago

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Una tienda acepta tres medios de pago, cada uno con su recargo:
- **efectivo**: 10% de descuento (recargo negativo);
- **tarjeta**: 4% por cuota si son 2 o más cuotas (en 1 cuota, sin recargo);
- **transferencia**: $150 fijos si el monto es de $100000 o menos.

Escribí una base abstracta `Pago` con `recargo()` y `medio()` virtuales puros y un
`total()` común. La entrada trae pagos como `efectivo 5000`, `tarjeta 60000 3` o
`transferencia 80000`. Mostrá cada pago con su total y lo cobrado en el día.

#### Criterio de aprobación

- `total()` no es virtual: usa `recargo()`, que sí lo es.
- Agregar un medio nuevo solo requiere una clase nueva.

#### Entrada de ejemplo

```
efectivo 5000
tarjeta 60000 3
transferencia 80000
tarjeta 12000 1
transferencia 250000
```

#### Salida esperada

```
efectivo: $5000.00 -> $4500.00
tarjeta en 3 cuota(s): $60000.00 -> $67200.00
transferencia: $80000.00 -> $80150.00
tarjeta en 1 cuota(s): $12000.00 -> $12000.00
transferencia: $250000.00 -> $250000.00
Total cobrado: $413850.00
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Medios de pago: cada uno calcula su recargo.
#include <iomanip>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

class Pago {
public:
    explicit Pago(double monto) : monto_(monto) {}
    virtual ~Pago() = default;
    virtual double recargo() const = 0;
    virtual std::string medio() const = 0;
    double total() const { return monto_ + recargo(); }
    double monto() const { return monto_; }

protected:
    double monto_;
};

class Efectivo : public Pago {
public:
    using Pago::Pago;
    double recargo() const override { return -monto_ * 0.10; }     // 10% de descuento
    std::string medio() const override { return "efectivo"; }
};

class Tarjeta : public Pago {
public:
    Tarjeta(double monto, int cuotas) : Pago(monto), cuotas_(cuotas) {}
    double recargo() const override { return cuotas_ <= 1 ? 0 : monto_ * 0.04 * cuotas_; }
    std::string medio() const override { return "tarjeta en " + std::to_string(cuotas_) + " cuota(s)"; }

private:
    int cuotas_;
};

class Transferencia : public Pago {
public:
    using Pago::Pago;
    double recargo() const override { return monto_ > 100000 ? 0 : 150; }   // costo fijo si es chica
    std::string medio() const override { return "transferencia"; }
};

int main()
{
    std::vector<std::unique_ptr<Pago>> pagos;
    std::string tipo;
    double monto = 0;
    while (std::cin >> tipo >> monto) {
        if (tipo == "efectivo") {
            pagos.push_back(std::make_unique<Efectivo>(monto));
        } else if (tipo == "tarjeta") {
            int cuotas = 1;
            std::cin >> cuotas;
            pagos.push_back(std::make_unique<Tarjeta>(monto, cuotas));
        } else if (tipo == "transferencia") {
            pagos.push_back(std::make_unique<Transferencia>(monto));
        }
    }
    std::cout << std::fixed << std::setprecision(2);
    double cobrado = 0;
    for (const std::unique_ptr<Pago>& p : pagos) {
        std::cout << p->medio() << ": $" << p->monto() << " -> $" << p->total() << "\n";
        cobrado += p->total();
    }
    std::cout << "Total cobrado: $" << cobrado << "\n";
    return 0;
}
```

#### Pruebas

##### Transferencia justo en el tope
```entrada
transferencia 100000
transferencia 100000.01
```
```salida
transferencia: $100000.00 -> $100150.00
transferencia: $100000.01 -> $100000.01
Total cobrado: $200150.01
```

##### Tarjeta en 12 cuotas
```entrada
tarjeta 10000 12
efectivo 0.5
```
```salida
tarjeta en 12 cuota(s): $10000.00 -> $14800.00
efectivo: $0.50 -> $0.45
Total cobrado: $14800.45
```

##### Sin pagos
```entrada
```
```salida
Total cobrado: $0.00
```

### Prueba del sello

#### ¿Qué hace `virtual`?

Que al llamar al método por referencia o puntero a la base, se ejecute la versión del tipo real del objeto.

#### ¿Para qué sirve `override`?

Para que el compilador verifique que el método realmente redefine un virtual de la base.

#### ¿Qué es una clase abstracta? ¿Se pueden crear objetos de ella?

Una clase con al menos un método virtual puro (`= 0`). No se pueden crear objetos de ella, solo de derivadas que definan todo.

#### ¿Por qué la base necesita destructor virtual?

Para que, al destruir una derivada a través de un puntero a la base, se ejecute el destructor correcto.

#### ¿Por qué no sirve `std::vector<Entidad>` para guardar guerreros y arqueras?

Porque cada lugar guarda una `Entidad`: las derivadas se rebanan. Hay que guardar punteros (`unique_ptr<Entidad>`).

### Soluciones (docente)

Material original: `03-C++/09-Polimorfismo`. `std::unique_ptr` se usa como receta; se explica a fondo en la rama 3 (Punteros inteligentes).

## R02-N08 · Programas en varios archivos

```meta
tipo: tema
padre: R02-N07
precio: 10
criatura: esqueleto
temas: prog.modulos, cal.build
```

### Crónica

La Sala de los Planos tiene un orden estricto: en un cajón, la **ficha** de cada máquina (qué hace, qué palancas tiene); en otro, los **planos de detalle** (cómo está hecha por dentro). El que quiere usar una máquina lee la ficha. Solo el que la construye abre el detalle.

—Un programa de cinco mil líneas en un solo archivo es un plano ilegible —dice {mentor}—. Cada clase va en su propio par de archivos: la ficha y el detalle. Y un capataz, **CMake**, sabe cómo juntarlos.

### Objetivos

Separar un programa en varios archivos: **headers** (`.h`) con las declaraciones
y **fuentes** (`.cpp`) con las definiciones; evitar las inclusiones dobles;
compilar y enlazar varios `.cpp`; reconocer los errores del enlazador; y armar
un proyecto con **CMake**.

### Antes de empezar

- Clases, herencia y polimorfismo (nodos anteriores).
- Los tres pasos del compilador (Clase 0).

### Explicación

#### Declaración y definición
- Una **declaración** dice que algo existe y cómo se usa: `double altura() const;`
  o `class Torre { ... };` con los prototipos de sus métodos.
- Una **definición** dice cómo está hecho: el cuerpo del método.

Para usar una clase, alcanza con su declaración. Por eso se separan:

| Archivo | Tiene | Lo lee |
|---|---|---|
| `Torre.h` (*header*) | la declaración de la clase | quien **usa** la torre |
| `Torre.cpp` | la definición de cada método | solo el compilador |
| `main.cpp` | el programa que usa las torres | |

#### El header
```cpp
#pragma once
#include <string>

class Torre {
public:
    Torre(const std::string& nombre, int pisos);
    double altura() const;
private:
    std::string nombre_;
    int pisos_;
};
```
- `#pragma once` evita que el header se incluya **dos veces** en el mismo `.cpp`
  (pasaría si `main.cpp` incluye `Torre.h` y también `Arena.h`, que a su vez incluye
  `Torre.h`). La forma clásica equivalente son los *include guards*:
  `#ifndef TORRE_H` / `#define TORRE_H` / … / `#endif`.
- El header incluye **lo que él mismo usa** (`<string>`, porque declara un
  `std::string`).
- Los métodos cortísimos (un getter de una línea) pueden quedar definidos en el
  header.

#### El `.cpp`
```cpp
#include "Torre.h"          // comillas: un archivo del proyecto

double Torre::altura() const
{
    return pisos_ * 3.5;
}
```
Cada método se define con `Clase::` adelante, para decir de qué clase es. `#include
"..."` busca en la carpeta del proyecto; `#include <...>`, en la biblioteca.

#### Compilar varios archivos
```bash
g++ -std=c++20 -Wall -Wextra -o ciudadela main.cpp Torre.cpp
```
Por dentro, cada `.cpp` se compila **por separado** en un archivo objeto (`.o`), y
al final el **enlazador** los une. Se puede hacer en pasos:
```bash
g++ -std=c++20 -Wall -Wextra -c Torre.cpp     # -> Torre.o
g++ -std=c++20 -Wall -Wextra -c main.cpp      # -> main.o
g++ -o ciudadela main.o Torre.o               # enlazar
```
La ventaja: si solo cambiás `main.cpp`, solo se recompila ese.

Los errores del **enlazador** se ven distintos: no mencionan una línea, sino un
nombre que "no está definido" o "está definido dos veces".

#### CMake: el capataz
En un proyecto de muchos archivos, nadie escribe el comando de `g++` a mano. Se
usa **CMake**, que lee un archivo `CMakeLists.txt`:
```cmake
cmake_minimum_required(VERSION 3.16)
project(ciudadela CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(ciudadela main.cpp Torre.cpp)
target_compile_options(ciudadela PRIVATE -Wall -Wextra)
```
Y se compila con:
```bash
cmake -B build              # prepara la carpeta build (una sola vez)
cmake --build build         # compila solo lo que cambió
./build/ciudadela
```
Para agregar un archivo nuevo al proyecto, se suma a la lista de
`add_executable`. CMake funciona igual en Linux, Windows y macOS, y lo entienden
todos los editores (VS Code, CLion, Qt Creator). Instalalo con
`sudo apt install cmake`.

#### Cómo entregar un proyecto de varios archivos
Comprimí la carpeta (sin la carpeta `build`) en un `.zip` y subila.

> **Si venís de C.** Es la misma idea que `.h` y `.c`, con clases en vez de
> funciones sueltas, y CMake en lugar de un Makefile escrito a mano.

### Código de ejemplo

`Torre.h`

```cpp
#pragma once   // que este archivo se incluya una sola vez por .cpp

#include <string>

// La DECLARACION de la clase: que tiene y que sabe hacer (la "interfaz").
class Torre {
public:
    Torre(const std::string& nombre, int pisos);

    void construir(int pisos);
    double altura() const;
    const std::string& nombre() const { return nombre_; }   // los metodos cortisimos pueden quedar aca
    int pisos() const { return pisos_; }

private:
    std::string nombre_;
    int pisos_;
};

// Una funcion libre del mismo modulo: aca solo el prototipo.
void mostrar(const Torre& t);
```

`Torre.cpp`

```cpp
#include "Torre.h"   // comillas: un archivo del proyecto; <...>: de la biblioteca

#include <iostream>

// La DEFINICION de cada metodo: Clase::metodo
Torre::Torre(const std::string& nombre, int pisos) : nombre_(nombre), pisos_(pisos > 0 ? pisos : 1) {}

void Torre::construir(int pisos)
{
    if (pisos > 0) {
        pisos_ += pisos;
    }
}

double Torre::altura() const
{
    return pisos_ * 3.5;
}

void mostrar(const Torre& t)
{
    std::cout << t.nombre() << ": " << t.pisos() << " pisos, " << t.altura() << " m\n";
}
```

`main.cpp`

```cpp
#include "Torre.h"

#include <vector>

int main()
{
    std::vector<Torre> ciudadela = {Torre("Norte", 4), Torre("Reloj", 9), Torre("Faro", -2)};
    ciudadela[0].construir(3);
    for (const Torre& t : ciudadela) {
        mostrar(t);
    }
    return 0;
}
```

`CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.16)
project(ciudadela CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Un ejecutable hecho de varios .cpp (los .h no se listan: los trae el #include)
add_executable(ciudadela main.cpp Torre.cpp)
target_compile_options(ciudadela PRIVATE -Wall -Wextra)
```

### Salida esperada

```
Norte: 7 pisos, 24.5 m
Reloj: 9 pisos, 31.5 m
Faro: 1 pisos, 3.5 m
```

### ¿Para qué sirve?

Todo proyecto real de C++ está partido en decenas o miles de archivos: un motor de juegos, un navegador, una aplicación de escritorio. Separar declaración y definición permite trabajar en equipo (cada uno en su módulo), recompilar solo lo que cambió y reutilizar módulos en otros proyectos. CMake es el sistema de construcción más usado en C++: lo vas a encontrar en casi cualquier repositorio.

### Errores habituales

**Esqueleto: un método declarado y nunca definido.** Compila, pero el enlazador no
lo encuentra:
```
/usr/bin/ld: main.o: in function `main':
main.cpp:(.text+0x32): undefined reference to `Torre::altura() const'
collect2: error: ld returned 1 exit status
```
(Con la terminal en español: "referencia a `Torre::altura() const' sin definir".)
O falta definirlo en el `.cpp`, o el `.cpp` no está en el comando de compilación (o
en `add_executable`).

**Esqueleto: definido dos veces.**
```
Torre.cpp:(.text+0x0): multiple definition of `Torre::altura() const'; Torre2.cpp: first defined here
```
Dos `.cpp` definen lo mismo, o una función **no** `inline` está definida en un
header que incluyen dos `.cpp`.

**Slime: el header sin `#pragma once`.** Incluido dos veces:
```
nog.h:1:8: error: redefinition of ‘struct P’
```

**Esqueleto: definir un método sin incluir su header.**
```
Torre.cpp:1:5: error: ‘Torre’ has not been declared
```

**Ogro: olvidar el `Torre::`.** `double altura() const { ... }` en el `.cpp` define
una función suelta llamada `altura`, no el método. El resultado es otro
"undefined reference".

**Ogro: compilar solo `main.cpp`.** `g++ main.cpp` sin `Torre.cpp` da "undefined
reference" para **todos** los métodos de `Torre`.

### Misión R02-N08-M1 · Separar la cuenta

```meta
entrega: archivo
entorno: local
monedas: 4
xp: 10
extensiones: zip, cpp, h, txt
```

#### Consigna

Tomá la `Cuenta` del Gremio (Encapsulamiento) y separala en `Cuenta.h`,
`Cuenta.cpp` y `main.cpp`, con un `CMakeLists.txt`. Compilá con CMake y probá con
la entrada de ejemplo. Entregá un `.zip` con los cuatro archivos.

#### Criterio de aprobación

- `Cuenta.h` tiene `#pragma once` y solo declaraciones (salvo getters de una línea).
- `Cuenta.cpp` define cada método con `Cuenta::`.
- El `CMakeLists.txt` lista los dos `.cpp` y compila sin advertencias.

#### Entrada de ejemplo

```
d 5000
e 1200
e 9000
d -50
e 3800
d 250.5
```

#### Salida esperada

```
d 5000.00 ok -> $5000.00
e 1200.00 ok -> $3800.00
e 9000.00 rechazado -> $3800.00
d -50.00 rechazado -> $3800.00
e 3800.00 ok -> $0.00
d 250.50 ok -> $250.50
Kira: 4 movimientos, saldo $250.50
```

#### Solución de referencia

```cpp
// ===== Cuenta.h =====
#pragma once

#include <string>
#include <vector>

class Cuenta {
public:
    explicit Cuenta(const std::string& titular);

    bool depositar(double monto);
    bool extraer(double monto);
    double saldo() const { return saldo_; }
    void resumen() const;

private:
    std::string titular_;
    double saldo_ = 0;
    std::vector<double> historial_;
};

// ===== Cuenta.cpp =====
#include "Cuenta.h"

#include <iostream>

Cuenta::Cuenta(const std::string& titular) : titular_(titular) {}

bool Cuenta::depositar(double monto)
{
    if (monto <= 0) {
        return false;
    }
    saldo_ += monto;
    historial_.push_back(monto);
    return true;
}

bool Cuenta::extraer(double monto)
{
    if (monto <= 0 || monto > saldo_) {
        return false;
    }
    saldo_ -= monto;
    historial_.push_back(-monto);
    return true;
}

void Cuenta::resumen() const
{
    std::cout << titular_ << ": " << historial_.size() << " movimientos, saldo $" << saldo_ << "\n";
}

// ===== main.cpp =====
#include "Cuenta.h"

#include <iomanip>
#include <iostream>

int main()
{
    std::cout << std::fixed << std::setprecision(2);
    Cuenta cuenta("Kira");
    char op = ' ';
    double monto = 0;
    while (std::cin >> op >> monto) {
        bool ok = (op == 'd') ? cuenta.depositar(monto) : cuenta.extraer(monto);
        std::cout << op << " " << monto << (ok ? " ok" : " rechazado") << " -> $" << cuenta.saldo() << "\n";
    }
    cuenta.resumen();
    return 0;
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(cuenta CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(cuenta main.cpp Cuenta.cpp)
target_compile_options(cuenta PRIVATE -Wall -Wextra)
```

### Misión R02-N08-M2 · El módulo de textos

```meta
entrega: archivo
entorno: local
monedas: 4
xp: 10
extensiones: zip, cpp, h, txt
```

#### Consigna

Armá un módulo `texto.h` / `texto.cpp` con cuatro funciones libres:
`mayusculas(s)`, `recortar(s)` (sin espacios al principio ni al final),
`palabras(s)` (un vector con las palabras separadas por espacios) y
`es_palindromo(s)` (ignora espacios y mayúsculas). En `main.cpp`, leé líneas hasta
el final y, para cada una, mostrá el texto recortado entre corchetes, cuántas
palabras tiene, el texto recortado en mayúsculas y si es palíndromo.

Para `recortar` te sirven `s.find_first_not_of(' ')`, `s.find_last_not_of(' ')` y
`s.substr(desde, cantidad)`. Si no encuentran nada, devuelven `std::string::npos`.

#### Criterio de aprobación

- Las funciones se declaran en `texto.h` y se definen en `texto.cpp`.
- El proyecto compila con CMake.
- Usa `static_cast<unsigned char>` antes de `std::toupper`.

#### Entrada de ejemplo

```
  hola mundo  
anita lava la tina
   
C++ en la Ciudadela
```

#### Salida esperada

```
[hola mundo] 2 palabra(s), HOLA MUNDO
[anita lava la tina] 4 palabra(s), ANITA LAVA LA TINA (palíndromo)
[] 0 palabra(s),  (palíndromo)
[C++ en la Ciudadela] 4 palabra(s), C++ EN LA CIUDADELA
```

#### Solución de referencia

```cpp
// ===== texto.h =====
#pragma once

#include <string>
#include <vector>

// Utilidades de texto del Gremio: funciones libres en un modulo propio.
std::string mayusculas(const std::string& s);
std::string recortar(const std::string& s);                  // sin espacios al principio ni al final
std::vector<std::string> palabras(const std::string& s);     // separadas por espacios
bool es_palindromo(const std::string& s);                    // ignora espacios y mayusculas

// ===== texto.cpp =====
#include "texto.h"

#include <cctype>

std::string mayusculas(const std::string& s)
{
    std::string r = s;
    for (char& c : r) {
        c = static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
    }
    return r;
}

std::string recortar(const std::string& s)
{
    std::size_t ini = s.find_first_not_of(' ');
    if (ini == std::string::npos) {
        return "";
    }
    std::size_t fin = s.find_last_not_of(' ');
    return s.substr(ini, fin - ini + 1);
}

std::vector<std::string> palabras(const std::string& s)
{
    std::vector<std::string> r;
    std::string actual;
    for (char c : s) {
        if (c == ' ') {
            if (!actual.empty()) {
                r.push_back(actual);
                actual.clear();
            }
        } else {
            actual += c;
        }
    }
    if (!actual.empty()) {
        r.push_back(actual);
    }
    return r;
}

bool es_palindromo(const std::string& s)
{
    std::string limpio;
    for (char c : mayusculas(s)) {
        if (c != ' ') {
            limpio += c;
        }
    }
    for (std::size_t i = 0; i < limpio.size() / 2; i++) {
        if (limpio[i] != limpio[limpio.size() - 1 - i]) {
            return false;
        }
    }
    return true;
}

// ===== main.cpp =====
#include "texto.h"

#include <iostream>
#include <string>

int main()
{
    std::string linea;
    while (std::getline(std::cin, linea)) {
        std::cout << "[" << recortar(linea) << "] ";
        std::cout << palabras(linea).size() << " palabra(s), " << mayusculas(recortar(linea));
        std::cout << (es_palindromo(linea) ? " (palíndromo)" : "") << "\n";
    }
    return 0;
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(texto CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(texto main.cpp texto.cpp)
target_compile_options(texto PRIVATE -Wall -Wextra)
```

### Misión R02-N08-M3 · Cazar esqueletos del enlazador

```meta
entrega: archivo
entorno: local
monedas: 4
xp: 10
extensiones: txt, md, pdf
```

#### Consigna

Con el proyecto de la torre del ejemplo, provocá a propósito estos cuatro errores,
de a uno, y copiá la **primera línea importante** de cada mensaje:
1. Borrá la definición de `Torre::altura` del `.cpp`.
2. Compilá con `g++ main.cpp` (sin `Torre.cpp`).
3. En `Torre.cpp`, escribí `double altura() const` sin `Torre::`.
4. Sacá el `#pragma once` e incluí `Torre.h` dos veces en `main.cpp`.

Para cada uno, respondé: ¿lo detectó el **compilador** o el **enlazador**? ¿Cómo te
diste cuenta? Entregá las respuestas en un archivo de texto (`.txt` o `.md`).

#### Criterio de aprobación

- Reproduce los cuatro errores y copia el mensaje.
- Distingue bien los de compilador (tienen archivo:línea) y los de enlazador (`undefined reference`, `ld`).

### Encargo R02-N08-E1 · La biblioteca de fechas

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 15
extensiones: zip, cpp, h, txt
```

#### Consigna

La administración del club necesita fechas. Armá `Fecha.h` / `Fecha.cpp` con una
clase `Fecha(dia, mes, anio)` que sabe si es válida (si no, queda en 1/1 de ese
año y `valida()` da `false`), el día del año (1 a 366), `sumar_dias(n)` y funciones
`static` `bisiesto(anio)` y `dias_del_mes(mes, anio)`. Agregá `operator<<` para
mostrarla como `dd/mm/aaaa`. Cada línea de la entrada trae `dia mes anio n`:
mostrá la fecha, su día del año y la fecha `n` días después.

Pista: en el header alcanza con `#include <iosfwd>` para declarar
`std::ostream&`; el `.cpp` incluye `<ostream>`.

#### Criterio de aprobación

- Separa declaración y definición.
- Valida meses y días, con años bisiestos.
- Cruza bien de mes y de año al sumar días.

#### Entrada de ejemplo

```
28 2 2024 2
31 12 2025 1
29 2 2023 0
15 7 2026 200
```

#### Salida esperada

```
28/02/2024 (día 59 del año) + 2 días = 01/03/2024
31/12/2025 (día 365 del año) + 1 días = 01/01/2026
29/2/2023: fecha inválida
15/07/2026 (día 196 del año) + 200 días = 31/01/2027
```

#### Solución de referencia

```cpp
// ===== Fecha.h =====
#pragma once

#include <iosfwd>

class Fecha {
public:
    Fecha(int dia, int mes, int anio);    // si es invalida, queda en 1/1/anio

    bool valida() const { return valida_; }
    int dia_del_anio() const;
    void sumar_dias(int n);               // n >= 0
    int dia() const { return dia_; }
    int mes() const { return mes_; }
    int anio() const { return anio_; }

    static bool bisiesto(int anio);
    static int dias_del_mes(int mes, int anio);

private:
    int dia_;
    int mes_;
    int anio_;
    bool valida_;
};

std::ostream& operator<<(std::ostream& os, const Fecha& f);

// ===== Fecha.cpp =====
#include "Fecha.h"

#include <ostream>

Fecha::Fecha(int dia, int mes, int anio)
    : dia_(dia), mes_(mes), anio_(anio),
      valida_(mes >= 1 && mes <= 12 && dia >= 1 && dia <= dias_del_mes(mes, anio))
{
    if (!valida_) {
        dia_ = 1;
        mes_ = 1;
    }
}

bool Fecha::bisiesto(int anio)
{
    return (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
}

int Fecha::dias_del_mes(int mes, int anio)
{
    const int DIAS[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (mes < 1 || mes > 12) {
        return 0;
    }
    return (mes == 2 && bisiesto(anio)) ? 29 : DIAS[mes - 1];
}

int Fecha::dia_del_anio() const
{
    int total = dia_;
    for (int m = 1; m < mes_; m++) {
        total += dias_del_mes(m, anio_);
    }
    return total;
}

void Fecha::sumar_dias(int n)
{
    for (int i = 0; i < n; i++) {
        dia_++;
        if (dia_ > dias_del_mes(mes_, anio_)) {
            dia_ = 1;
            mes_++;
            if (mes_ > 12) {
                mes_ = 1;
                anio_++;
            }
        }
    }
}

std::ostream& operator<<(std::ostream& os, const Fecha& f)
{
    return os << (f.dia() < 10 ? "0" : "") << f.dia() << "/" << (f.mes() < 10 ? "0" : "") << f.mes() << "/" << f.anio();
}

// ===== main.cpp =====
#include "Fecha.h"

#include <iostream>

int main()
{
    int d = 0, m = 0, a = 0, n = 0;
    while (std::cin >> d >> m >> a >> n) {
        Fecha f(d, m, a);
        if (!f.valida()) {
            std::cout << d << "/" << m << "/" << a << ": fecha inválida\n";
            continue;
        }
        std::cout << f << " (día " << f.dia_del_anio() << " del año)";
        f.sumar_dias(n);
        std::cout << " + " << n << " días = " << f << "\n";
    }
    return 0;
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(fechas CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(fechas main.cpp Fecha.cpp)
target_compile_options(fechas PRIVATE -Wall -Wextra)
```

### Prueba del sello

#### ¿Qué va en el `.h` y qué en el `.cpp`?

En el `.h`, las declaraciones (la clase con los prototipos de sus métodos); en el `.cpp`, las definiciones (los cuerpos).

#### ¿Para qué sirve `#pragma once`?

Para que un header se incluya una sola vez por archivo `.cpp`, aunque aparezca en varios `#include`.

#### ¿Qué significa "undefined reference"? ¿Quién lo dice?

Que algo se declaró y se usó, pero nadie lo definió (o su `.cpp` no se enlazó). Lo dice el enlazador.

#### ¿Qué diferencia hay entre `#include "Torre.h"` y `#include <string>`?

Con comillas se busca primero en la carpeta del proyecto; con `< >`, en las bibliotecas del sistema.

#### ¿Qué hacen `cmake -B build` y `cmake --build build`?

El primero prepara la carpeta de compilación a partir del `CMakeLists.txt`; el segundo compila lo que cambió.

### Soluciones (docente)

Nodo nuevo como tal (FullCursos lo mencionaba de pasada en `03/12` y `04/14`). Las entregas de varios archivos se suben como `.zip`. En M3 el alumno responde por escrito: se corrige leyendo.

## R02-N09 · Jefe: la Quimera de la Arena

```meta
tipo: jefe
padre: R02-N08
precio: 10
criatura: dragon
insignia: Sello de la Quimera
insignia_descripcion: Venciste a la Quimera de la Arena: dominás clases, herencia y polimorfismo en C++.
usa: poo.polimorfismo, poo.composicion, mem.smart-pointers
```

### Crónica

Bajo la Ciudadela hay una **Arena** donde los artífices prueban sus planos. Esta semana hay algo nuevo en la jaula del fondo: la **Quimera**, una criatura con cabeza de león, cuerpo de cabra y cola de serpiente, que cambia de forma en cada turno.

—No la vas a vencer con un solo tipo de golpe —advierte {mentor}—. Cada forma resiste algo distinto. Pero vos ya sabés escribir un código que pregunta "¿qué sos?" sin preguntarlo: que cada forma responda por sí misma.

### Objetivos

Integrar la rama en un proyecto de varios archivos: clases con encapsulamiento,
herencia, polimorfismo con `unique_ptr`, composición y CMake.

### Antes de empezar

- Toda la rama: clases, constructores, encapsulamiento, operadores, composición,
  herencia, polimorfismo y varios archivos.

### Explicación

#### Cómo se enfrenta a un jefe de clases
1. **Leé la consigna y dibujá las clases**: un rectángulo por clase, con sus datos y
   sus métodos. Flechas de "es un" (herencia) y de "tiene un" (composición).
2. **Empezá por la base.** Compilala sola, probala con un `main` chiquito.
3. **Sumá las derivadas de a una.** Con `override` en cada método redefinido.
4. **Recién después, la clase que las usa** (la Arena, la central): recibe y guarda
   `unique_ptr<Base>`, y no pregunta nunca qué tipo tiene cada uno.
5. **El `main` es corto**: arma los objetos y llama a un método.

#### Una pregunta que te salva
Cada vez que escribas `if (tipo == "goblin")` fuera de la fábrica que crea los
objetos, preguntate: ¿no debería ser un método virtual? Si el comportamiento
depende del tipo, el tipo tiene que resolverlo.

#### Pasar dueños: `std::move`
Para darle a otra clase un `unique_ptr` (que sea su nuevo dueño), se usa
`std::move`:
```cpp
void Arena::agregar(std::unique_ptr<Entidad> rival)
{
    oleada_.push_back(std::move(rival));   // la Arena pasa a ser la dueña
}
arena.agregar(std::make_unique<Goblin>());
```
Un `unique_ptr` no se copia (solo puede haber un dueño): se **mueve**. En la rama 3
vas a ver por qué.

#### Guardar una referencia a algo que vive afuera
`Arena` guarda `Heroina& heroina_`: la heroína vive en `main` y la Arena solo la
**usa**. Es seguro porque la heroína vive más que la Arena. Si pudiera morir antes,
sería una referencia colgante.

### ¿Para qué sirve?

Este es el esqueleto de muchísimos programas: una colección de objetos de distintos tipos, todos con la misma interfaz, manejados por una clase que no conoce los detalles. Un editor de dibujo con figuras, un sistema de notificaciones (mail, SMS, WhatsApp), una central de sensores, un juego con enemigos: agregar un tipo nuevo es escribir una clase, sin tocar el resto.

### Errores habituales

**Esqueleto: un `.cpp` que no está en `add_executable`.** "undefined reference" a
todos sus métodos.

**Ogro: el `if` por tipo.** `if (rival.nombre() == "Quimera")` dentro de la Arena:
cada criatura nueva obliga a tocar la Arena. Que lo resuelva un virtual.

**Troll: copiar un `unique_ptr`.** `oleada_.push_back(rival);` no compila (el mensaje
menciona una "use of deleted function"). Hay que moverlo: `std::move(rival)`.

**Troll: usar un `unique_ptr` después de moverlo.** Después de `std::move(rival)`,
`rival` queda vacío: usarlo es desreferenciar `nullptr`.

**Ogro: el combate infinito.** Si nadie puede dañar a nadie, el bucle no termina:
poné un límite de rondas.

### Misión R02-N09-M1 · La Arena

```meta
entrega: archivo
entorno: local
monedas: 6
xp: 30
extensiones: zip, cpp, h, txt
```

#### Consigna

Armá el proyecto de la Arena en cuatro módulos: `Entidad` (base con `turno` y
`descripcion` virtuales), `Criaturas` (las derivadas), `Arena` y `main`, con su
`CMakeLists.txt`.

- **Entidad**: nombre, vida, vida máxima y ataque. `turno(rival)` golpea con el
  ataque y lo devuelve; `descripcion()` da `Nombre (vida/máx)`; `recibir_dano` y
  `curar` respetan 0 y el máximo.
- **Heroína** (120 de vida, 14 de ataque): cada tercer golpe es crítico (doble, y
  lo anuncia); `descripcion` antepone "Heroína"; `descansar()` cura 30.
- **Slime** (30, 4): en su turno primero se cura 3 y después golpea.
- **Goblin** (40, 8): golpea y se cura la mitad del daño que hizo.
- **Quimera** (110): cambia de forma cada turno, en orden león → cabra → serpiente.
  León: 18 de daño. Cabra: se cura 12 y hace 6. Serpiente: suma 4 al veneno y no
  hace daño propio. **Todas** las formas agregan el veneno acumulado al daño.
  `descripcion` agrega la forma actual.
- **Arena**: guarda una referencia a la heroína y un vector de `unique_ptr<Entidad>`
  (la oleada). Cada combate: la heroína golpea y, si el rival sigue vivo, responde;
  máximo 20 rondas. Entre combates la heroína descansa.

Reproducí exactamente la salida esperada.

#### Criterio de aprobación

- El proyecto está en cuatro módulos y compila con CMake sin advertencias.
- `Arena` no pregunta el tipo de ningún rival.
- Las derivadas usan `override` y reutilizan los métodos de la base.
- La salida coincide con la esperada.

#### Salida esperada

```
Heroína Kira (120/120) entra a la Arena.

-- Entra Slime (30/30) --
  1: Kira golpea por 14
  1: Slime responde por 4  | 116 vs 19
  2: Kira golpea por 14
  2: Slime responde por 4  | 112 vs 8
    ¡golpe crítico!
  3: Kira golpea por 28  | 112 vs 0
>> Slime cae. Heroína Kira (120/120)

-- Entra Goblin (40/40) --
  1: Kira golpea por 14
  1: Goblin responde por 8  | 112 vs 30
  2: Kira golpea por 14
  2: Goblin responde por 8  | 104 vs 20
    ¡golpe crítico!
  3: Kira golpea por 28  | 104 vs 0
>> Goblin cae. Heroína Kira (120/120)

-- Entra Quimera (110/110) [forma: león] --
  1: Kira golpea por 14
    la Quimera ruge como león
  1: Quimera responde por 18  | 102 vs 96
  2: Kira golpea por 14
    la Quimera se cura como cabra
  2: Quimera responde por 6  | 96 vs 94
    ¡golpe crítico!
  3: Kira golpea por 28
    la Quimera muerde como serpiente (veneno 4)
  3: Quimera responde por 4  | 92 vs 66
  4: Kira golpea por 14
    la Quimera ruge como león
  4: Quimera responde por 22  | 70 vs 52
  5: Kira golpea por 14
    la Quimera se cura como cabra
  5: Quimera responde por 10  | 60 vs 50
    ¡golpe crítico!
  6: Kira golpea por 28
    la Quimera muerde como serpiente (veneno 8)
  6: Quimera responde por 8  | 52 vs 22
  7: Kira golpea por 14
    la Quimera ruge como león
  7: Quimera responde por 26  | 26 vs 8
  8: Kira golpea por 14  | 26 vs 0
>> Quimera cae. Heroína Kira (56/120)

=== ¡Kira vence a la Quimera de la Arena! ===
```

#### Solución de referencia

```cpp
// ===== Entidad.h =====
#pragma once

#include <string>

class Entidad {
public:
    Entidad(const std::string& nombre, int vida, int ataque);
    virtual ~Entidad() = default;

    // Lo que hace en su turno contra el rival. Devuelve el danio infligido.
    virtual int turno(Entidad& rival);
    // Cada tipo se describe a su manera.
    virtual std::string descripcion() const;

    void recibir_dano(int n);
    void curar(int n);
    bool vivo() const { return vida_ > 0; }
    const std::string& nombre() const { return nombre_; }
    int vida() const { return vida_; }

protected:
    std::string nombre_;
    int vida_;
    int vida_max_;
    int ataque_;
};

// ===== Entidad.cpp =====
#include "Entidad.h"

#include <algorithm>

Entidad::Entidad(const std::string& nombre, int vida, int ataque)
    : nombre_(nombre), vida_(vida), vida_max_(vida), ataque_(ataque)
{
}

int Entidad::turno(Entidad& rival)
{
    rival.recibir_dano(ataque_);
    return ataque_;
}

std::string Entidad::descripcion() const
{
    return nombre_ + " (" + std::to_string(vida_) + "/" + std::to_string(vida_max_) + ")";
}

void Entidad::recibir_dano(int n)
{
    vida_ = std::max(0, vida_ - n);
}

void Entidad::curar(int n)
{
    vida_ = std::min(vida_max_, vida_ + n);
}

// ===== Criaturas.h =====
#pragma once

#include "Entidad.h"

class Heroina : public Entidad {
public:
    explicit Heroina(const std::string& nombre);
    int turno(Entidad& rival) override;     // cada tercer golpe es critico
    std::string descripcion() const override;
    void descansar();                       // entre rondas recupera 30

private:
    int golpes_ = 0;
};

class Slime : public Entidad {
public:
    Slime();
    int turno(Entidad& rival) override;     // se divide: cada turno recupera 3
};

class Goblin : public Entidad {
public:
    Goblin();
    int turno(Entidad& rival) override;     // roba: golpea y se cura la mitad
};

class Quimera : public Entidad {
public:
    Quimera();
    int turno(Entidad& rival) override;     // cambia de forma cada turno
    std::string descripcion() const override;

private:
    int forma_ = 0;                          // 0 leon, 1 cabra, 2 serpiente
    int veneno_ = 0;
};

// ===== Criaturas.cpp =====
#include "Criaturas.h"

#include <iostream>

// ---------- Heroina ----------
Heroina::Heroina(const std::string& nombre) : Entidad(nombre, 120, 14) {}

int Heroina::turno(Entidad& rival)
{
    golpes_++;
    int dano = (golpes_ % 3 == 0) ? ataque_ * 2 : ataque_;
    if (golpes_ % 3 == 0) {
        std::cout << "    ¡golpe crítico!\n";
    }
    rival.recibir_dano(dano);
    return dano;
}

std::string Heroina::descripcion() const
{
    return "Heroína " + Entidad::descripcion();
}

void Heroina::descansar()
{
    curar(30);
}

// ---------- Slime ----------
Slime::Slime() : Entidad("Slime", 30, 4) {}

int Slime::turno(Entidad& rival)
{
    curar(3);
    return Entidad::turno(rival);
}

// ---------- Goblin ----------
Goblin::Goblin() : Entidad("Goblin", 40, 8) {}

int Goblin::turno(Entidad& rival)
{
    int dano = Entidad::turno(rival);
    curar(dano / 2);
    return dano;
}

// ---------- Quimera ----------
Quimera::Quimera() : Entidad("Quimera", 110, 0) {}

int Quimera::turno(Entidad& rival)
{
    int dano = 0;
    if (forma_ == 0) {                        // leon: golpe fuerte
        dano = 18;
        std::cout << "    la Quimera ruge como león\n";
    } else if (forma_ == 1) {                 // cabra: se cura y cornea suave
        curar(12);
        dano = 6;
        std::cout << "    la Quimera se cura como cabra\n";
    } else {                                  // serpiente: acumula veneno
        veneno_ += 4;
        std::cout << "    la Quimera muerde como serpiente (veneno " << veneno_ << ")\n";
    }
    dano += veneno_;
    rival.recibir_dano(dano);
    forma_ = (forma_ + 1) % 3;
    return dano;
}

std::string Quimera::descripcion() const
{
    const char* formas[] = {"león", "cabra", "serpiente"};
    return Entidad::descripcion() + " [forma: " + formas[forma_] + "]";
}

// ===== Arena.h =====
#pragma once

#include <memory>
#include <vector>

#include "Criaturas.h"

class Arena {
public:
    explicit Arena(Heroina& heroina);
    void agregar(std::unique_ptr<Entidad> rival);
    bool jugar();                    // true si la heroina vence a todos

private:
    bool combate(Entidad& rival);

    Heroina& heroina_;
    std::vector<std::unique_ptr<Entidad>> oleada_;
};

// ===== Arena.cpp =====
#include "Arena.h"

#include <iostream>
#include <utility>

Arena::Arena(Heroina& heroina) : heroina_(heroina) {}

void Arena::agregar(std::unique_ptr<Entidad> rival)
{
    oleada_.push_back(std::move(rival));
}

bool Arena::combate(Entidad& rival)
{
    std::cout << "\n-- Entra " << rival.descripcion() << " --\n";
    int ronda = 1;
    while (heroina_.vivo() && rival.vivo() && ronda <= 20) {
        int d1 = heroina_.turno(rival);
        std::cout << "  " << ronda << ": " << heroina_.nombre() << " golpea por " << d1;
        if (rival.vivo()) {
            std::cout << "\n";
            int d2 = rival.turno(heroina_);
            std::cout << "  " << ronda << ": " << rival.nombre() << " responde por " << d2;
        }
        std::cout << "  | " << heroina_.vida() << " vs " << rival.vida() << "\n";
        ronda++;
    }
    return heroina_.vivo() && !rival.vivo();
}

bool Arena::jugar()
{
    for (const std::unique_ptr<Entidad>& rival : oleada_) {
        if (!combate(*rival)) {
            return false;
        }
        heroina_.descansar();
        std::cout << ">> " << rival->nombre() << " cae. " << heroina_.descripcion() << "\n";
    }
    return true;
}

// ===== main.cpp =====
#include "Arena.h"

#include <iostream>
#include <memory>

int main()
{
    Heroina kira("Kira");
    Arena arena(kira);
    arena.agregar(std::make_unique<Slime>());
    arena.agregar(std::make_unique<Goblin>());
    arena.agregar(std::make_unique<Quimera>());

    std::cout << kira.descripcion() << " entra a la Arena.\n";
    if (arena.jugar()) {
        std::cout << "\n=== ¡Kira vence a la Quimera de la Arena! ===\n";
    } else {
        std::cout << "\n=== Kira cae en la Arena. ===\n";
    }
    return 0;
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(arena CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(arena main.cpp Entidad.cpp Criaturas.cpp Arena.cpp)
target_compile_options(arena PRIVATE -Wall -Wextra)
```

### Misión R02-N09-M2 · Las tres formas de la Quimera

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Ahora la Quimera es una clase que **tiene** sus formas: un vector de
`unique_ptr<Forma>`, donde `Forma` es abstracta con `nombre()`, `dano()` y
`defensa(arma)` (el porcentaje del golpe que absorbe).

| Forma | Daño | Absorbe |
|---|---|---|
| león | 16 | 50%, salvo la **lanza** (0%) |
| cabra | 8 | 30%, salvo el **martillo** (0%) |
| serpiente | 12 | 60%, salvo la **espada** (0%) |

La Quimera tiene 100 de vida; Kira, 80. Cada línea de la entrada es el arma que
usa Kira (fuerza 30). Si el arma no existe, pierde el golpe. Después, si la Quimera
sigue viva, golpea con el daño de su forma y cambia a la siguiente. El duelo
termina cuando alguien cae o se acaba la entrada.

#### Criterio de aprobación

- `Quimera` compone formas polimórficas y no usa `if` por forma.
- El daño efectivo se calcula con la defensa de la forma actual.
- La salida coincide con la esperada.

#### Entrada de ejemplo

```
lanza
arco
espada
martillo
martillo
espada
```

#### Salida esperada

```
Turno 1: la Quimera es león
  Kira usa lanza: 30 de daño (Quimera 70)
  La Quimera golpea por 16 (Kira 64)
Turno 2: la Quimera es cabra
  Kira duda con "arco" y pierde el golpe.
  La Quimera golpea por 8 (Kira 56)
Turno 3: la Quimera es serpiente
  Kira usa espada: 30 de daño (Quimera 40)
  La Quimera golpea por 12 (Kira 44)
Turno 4: la Quimera es león
  Kira usa martillo: 15 de daño (Quimera 25)
  La Quimera golpea por 16 (Kira 28)
Turno 5: la Quimera es cabra
  Kira usa martillo: 30 de daño (Quimera 0)
¡La Quimera cae! Kira leyó cada forma.
```

#### Solución de referencia

```cpp
// Jefe R02 - La Quimera: una clase que TIENE formas polimorficas y cambia entre ellas.
#include <algorithm>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

class Forma {
public:
    virtual ~Forma() = default;
    virtual std::string nombre() const = 0;
    virtual int dano() const = 0;
    // Cuanto del golpe de Kira absorbe esta forma (0 a 100 %).
    virtual int defensa(const std::string& arma) const = 0;
};

class Leon : public Forma {
public:
    std::string nombre() const override { return "león"; }
    int dano() const override { return 16; }
    int defensa(const std::string& arma) const override { return arma == "lanza" ? 0 : 50; }
};

class Cabra : public Forma {
public:
    std::string nombre() const override { return "cabra"; }
    int dano() const override { return 8; }
    int defensa(const std::string& arma) const override { return arma == "martillo" ? 0 : 30; }
};

class Serpiente : public Forma {
public:
    std::string nombre() const override { return "serpiente"; }
    int dano() const override { return 12; }
    int defensa(const std::string& arma) const override { return arma == "espada" ? 0 : 60; }
};

class Quimera {
public:
    Quimera()
    {
        formas_.push_back(std::make_unique<Leon>());
        formas_.push_back(std::make_unique<Cabra>());
        formas_.push_back(std::make_unique<Serpiente>());
    }

    const Forma& forma() const { return *formas_[actual_]; }

    int recibir(const std::string& arma, int fuerza)
    {
        int efectivo = fuerza * (100 - forma().defensa(arma)) / 100;
        vida_ = std::max(0, vida_ - efectivo);
        return efectivo;
    }

    void cambiar() { actual_ = (actual_ + 1) % formas_.size(); }
    int vida() const { return vida_; }

private:
    std::vector<std::unique_ptr<Forma>> formas_;
    std::size_t actual_ = 0;
    int vida_ = 100;
};

int main()
{
    Quimera q;
    int kira = 80;
    int turno = 1;
    std::string arma;
    while (kira > 0 && q.vida() > 0 && std::cin >> arma) {
        std::cout << "Turno " << turno << ": la Quimera es " << q.forma().nombre() << "\n";
        if (arma != "espada" && arma != "lanza" && arma != "martillo") {
            std::cout << "  Kira duda con \"" << arma << "\" y pierde el golpe.\n";
        } else {
            int hecho = q.recibir(arma, 30);
            std::cout << "  Kira usa " << arma << ": " << hecho << " de daño (Quimera " << q.vida() << ")\n";
        }
        if (q.vida() > 0) {
            kira = std::max(0, kira - q.forma().dano());
            std::cout << "  La Quimera golpea por " << q.forma().dano() << " (Kira " << kira << ")\n";
            q.cambiar();
        }
        turno++;
    }
    if (q.vida() == 0) {
        std::cout << "¡La Quimera cae! Kira leyó cada forma.\n";
    } else if (kira == 0) {
        std::cout << "Kira cae. La Quimera cambia de forma y se ríe.\n";
    } else {
        std::cout << "El duelo queda sin terminar.\n";
    }
    return 0;
}
```

#### Pruebas

##### Kira vence a la Quimera
```entrada
lanza
martillo
espada
lanza
```
```salida
Turno 1: la Quimera es león
  Kira usa lanza: 30 de daño (Quimera 70)
  La Quimera golpea por 16 (Kira 64)
Turno 2: la Quimera es cabra
  Kira usa martillo: 30 de daño (Quimera 40)
  La Quimera golpea por 8 (Kira 56)
Turno 3: la Quimera es serpiente
  Kira usa espada: 30 de daño (Quimera 10)
  La Quimera golpea por 12 (Kira 44)
Turno 4: la Quimera es león
  Kira usa lanza: 30 de daño (Quimera 0)
¡La Quimera cae! Kira leyó cada forma.
```

##### Armas que no sirven
```entrada
espada
lanza
martillo
arco
arco
arco
arco
arco
arco
```
```salida
Turno 1: la Quimera es león
  Kira usa espada: 15 de daño (Quimera 85)
  La Quimera golpea por 16 (Kira 64)
Turno 2: la Quimera es cabra
  Kira usa lanza: 21 de daño (Quimera 64)
  La Quimera golpea por 8 (Kira 56)
Turno 3: la Quimera es serpiente
  Kira usa martillo: 12 de daño (Quimera 52)
  La Quimera golpea por 12 (Kira 44)
Turno 4: la Quimera es león
  Kira duda con "arco" y pierde el golpe.
  La Quimera golpea por 16 (Kira 28)
Turno 5: la Quimera es cabra
  Kira duda con "arco" y pierde el golpe.
  La Quimera golpea por 8 (Kira 20)
Turno 6: la Quimera es serpiente
  Kira duda con "arco" y pierde el golpe.
  La Quimera golpea por 12 (Kira 8)
Turno 7: la Quimera es león
  Kira duda con "arco" y pierde el golpe.
  La Quimera golpea por 16 (Kira 0)
Kira cae. La Quimera cambia de forma y se ríe.
```

##### Sin armas
```entrada
```
```salida
El duelo queda sin terminar.
```

### Encargo R02-N09-E1 · La central de alarmas

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

Una empresa de seguridad tiene una central con cuatro sensores, en este orden: humo
en la cocina (alarma si pasa de 300 ppm), temperatura en la cámara de frío (alarma
fuera de −20 a −15), puerta del depósito (alarma si la lectura no es 0) y
temperatura en la sala de servidores (alarma fuera de 15 a 27).

Escribí una base abstracta `Sensor` (con el lugar, `alarma(lectura)` y `tipo()`) y
sus derivadas. La entrada trae lecturas en rondas: la primera lectura es del primer
sensor, la segunda del segundo… y después de la cuarta se vuelve a empezar. Mostrá
cada alarma con la ronda, y el total.

#### Criterio de aprobación

- La central es un vector de `unique_ptr<Sensor>`.
- Los dos sensores de temperatura son la misma clase con distintos límites.
- Ninguna parte del `main` pregunta el tipo de sensor.

#### Entrada de ejemplo

```
120 -18 0 22
350 -12 0 24
90 -17 1 31
400 -21 0 26
```

#### Salida esperada

```
Ronda 2: ¡ALARMA! humo en cocina (350)
Ronda 2: ¡ALARMA! temperatura en cámara de frío (-12)
Ronda 3: ¡ALARMA! puerta en depósito (1)
Ronda 3: ¡ALARMA! temperatura en sala de servidores (31)
Ronda 4: ¡ALARMA! humo en cocina (400)
Ronda 4: ¡ALARMA! temperatura en cámara de frío (-21)
Alarmas: 6
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La central de alarmas: sensores polimorficos.
#include <iostream>
#include <memory>
#include <string>
#include <vector>

class Sensor {
public:
    explicit Sensor(const std::string& lugar) : lugar_(lugar) {}
    virtual ~Sensor() = default;
    // Recibe una lectura y dice si hay que dar la alarma.
    virtual bool alarma(double lectura) const = 0;
    virtual std::string tipo() const = 0;
    const std::string& lugar() const { return lugar_; }

private:
    std::string lugar_;
};

class Humo : public Sensor {
public:
    using Sensor::Sensor;
    bool alarma(double ppm) const override { return ppm > 300; }
    std::string tipo() const override { return "humo"; }
};

class Temperatura : public Sensor {
public:
    Temperatura(const std::string& lugar, double minima, double maxima)
        : Sensor(lugar), minima_(minima), maxima_(maxima)
    {
    }
    bool alarma(double grados) const override { return grados < minima_ || grados > maxima_; }
    std::string tipo() const override { return "temperatura"; }

private:
    double minima_;
    double maxima_;
};

class Puerta : public Sensor {
public:
    using Sensor::Sensor;
    bool alarma(double abierta) const override { return abierta != 0; }
    std::string tipo() const override { return "puerta"; }
};

int main()
{
    std::vector<std::unique_ptr<Sensor>> central;
    central.push_back(std::make_unique<Humo>("cocina"));
    central.push_back(std::make_unique<Temperatura>("cámara de frío", -20, -15));
    central.push_back(std::make_unique<Puerta>("depósito"));
    central.push_back(std::make_unique<Temperatura>("sala de servidores", 15, 27));

    std::size_t i = 0;
    double lectura = 0;
    int alarmas = 0;
    int ronda = 1;
    while (std::cin >> lectura) {
        const Sensor& s = *central[i];
        if (s.alarma(lectura)) {
            std::cout << "Ronda " << ronda << ": ¡ALARMA! " << s.tipo() << " en " << s.lugar() << " (" << lectura << ")\n";
            alarmas++;
        }
        i++;
        if (i == central.size()) {
            i = 0;
            ronda++;
        }
    }
    std::cout << "Alarmas: " << alarmas << "\n";
    return 0;
}
```

#### Pruebas

##### Sin alarmas
```entrada
100 -18 0 20
```
```salida
Alarmas: 0
```

##### Ronda incompleta
```entrada
500 -30
```
```salida
Ronda 1: ¡ALARMA! humo en cocina (500)
Ronda 1: ¡ALARMA! temperatura en cámara de frío (-30)
Alarmas: 2
```

##### Bordes exactos
```entrada
300 -20 0 15
301 -15 0 27
0 -14 2 28
```
```salida
Ronda 2: ¡ALARMA! humo en cocina (301)
Ronda 3: ¡ALARMA! temperatura en cámara de frío (-14)
Ronda 3: ¡ALARMA! puerta en depósito (2)
Ronda 3: ¡ALARMA! temperatura en sala de servidores (28)
Alarmas: 4
```

### Prueba del sello

#### ¿Por qué la Arena guarda `unique_ptr<Entidad>` y no `Entidad`?

Para poder guardar criaturas de distintos tipos sin rebanarlas, y que cada una ejecute su propio `turno`.

#### ¿Por qué para agregar un `unique_ptr` a un vector hace falta `std::move`?

Porque un `unique_ptr` no se copia (tiene un solo dueño): se transfiere.

#### ¿Qué tendrías que cambiar para agregar un Troll a la Arena?

Solo escribir la clase `Troll` (con su `turno`) y agregarla a la oleada; la Arena no cambia.

#### ¿Por qué es seguro que la Arena guarde una referencia a la heroína?

Porque la heroína se crea en `main` antes que la Arena y vive más que ella.

#### En la Quimera del duelo, ¿dónde está la decisión de "cuánto absorbe"?

En cada forma (`defensa`, un método virtual), no en la Quimera.

### Soluciones (docente)

Jefe de la rama 2. M1 reescribe `03-C++/12-ProyectoArena` con polimorfismo real (cada criatura tiene su `turno`) y cuatro módulos. Se entrega como `.zip`.
