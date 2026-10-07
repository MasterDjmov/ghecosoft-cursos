# RAMA R02 · Objetos y errores: la Gran Biblioteca

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · Clases y objetos

```meta
tipo: tema
padre: R01-N11
precio: 10
criatura: esqueleto
temas: poo.clases, poo.encapsulamiento, poo.operadores, poo.records
```

### Crónica

Con la Hidra vencida, el Paso lleva al **Bastión de las Escamas**, que guarda **la Gran Biblioteca**. Ahí trabaja **Sila**, la Archivera. Sus guardianes no escriben cada criatura por separado: tienen **moldes**. Un molde de «orco» dice qué datos tiene todo orco (vida, fuerza) y qué sabe hacer (atacar, gritar). De un molde salen mil orcos, cada uno con su propia vida.

—A ese molde lo llamamos **clase** —dice Sila—, y a cada pieza que sale de él, **objeto**.

Cuando Mia crea el suyo, por primera vez aparecen **cubos de datos** flotando sobre sus manos.

### Objetivos

- Definir una clase con `__init__`, atributos y métodos.
- Entender qué es `self` y distinguir atributos de instancia y de clase.
- Usar `@property` y los métodos especiales (`__str__`, `__eq__`, `__add__`…).
- Ahorrar código con `@dataclass`.

### Antes de empezar

Funciones (R01-N08), diccionarios (R01-N06) y referencias (R01-N07): un objeto se comporta como una estructura mutable.

### Explicación

#### Por qué hacen falta las clases

Hasta ahora, un personaje era un diccionario (`{"nombre": "Mia", "vida": 100}`) y las acciones eran funciones sueltas (`curar(personaje, 20)`). Funciona, pero nada impide escribir `personaje["vdia"]` o pasarle a `curar` un diccionario de otra cosa. Una **clase** junta en un solo lugar los **datos** (atributos) y las **acciones** (métodos) de un tipo de cosa.

#### Definir una clase

```python
class Personaje:
    def __init__(self, nombre, vida=100):
        self.nombre = nombre
        self.vida = vida

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)


mia = Personaje("Mia")        # crear un OBJETO (una instancia)
mia.recibir(30)                # llamar a un MÉTODO
print(mia.vida)                # leer un ATRIBUTO → 70
```

- `class Personaje:` define el molde. Por convención, los nombres de clase van en **MayúsculaInicial**.
- `__init__` se ejecuta **solo** cada vez que creás un objeto: arma sus atributos iniciales.
- `self` es "este objeto". Python lo pasa solo: `mia.recibir(30)` es en realidad `Personaje.recibir(mia, 30)`. Por eso todo método tiene `self` como primer parámetro, pero al llamarlo no se escribe.
- `self.vida = vida` crea un atributo **del objeto**: cada personaje tiene su propia vida.

#### Atributos de instancia y de clase

Un atributo escrito dentro de la clase, fuera de los métodos, es **de la clase**: lo comparten todos los objetos (`especie = "humana"`). Los de `self.` son de cada objeto. Regla práctica: lo que cambia de un objeto a otro va en `self`; las constantes comunes, en la clase.

#### `@property`: un cálculo que se usa como atributo

```python
@property
def porcentaje(self):
    return self.vida / self.vida_max

print(tilo.porcentaje)   # sin paréntesis
```

Sirve para valores que se **calculan** a partir de otros, o para proteger un atributo: por convención, un nombre que empieza con `_` (como `_saldo`) avisa "no lo toques desde afuera"; la `@property saldo` deja leerlo sin poder asignarlo.

#### Métodos especiales

Los métodos con doble guion bajo (*dunder*) le enseñan a tu clase a funcionar con lo que ya trae Python:

| Método | Hace funcionar |
|---|---|
| `__str__` | `print(objeto)` y `str(objeto)` |
| `__repr__` | cómo se ve en la consola o dentro de una lista |
| `__eq__` | `a == b` (si no está, compara si son **el mismo** objeto) |
| `__lt__` | `a < b`, y con eso `sorted()`, `min()` y `max()` |
| `__add__`, `__sub__`, `__mul__` | `a + b`, `a - b`, `a * 2` |
| `__len__` | `len(objeto)` |

#### `@dataclass`: menos código repetido

Muchas clases solo guardan datos. `@dataclass` escribe `__init__`, `__repr__` y `__eq__` por vos a partir de los campos anotados:

```python
from dataclasses import dataclass, field

@dataclass
class Item:
    nombre: str
    valor: int = 0
    etiquetas: list = field(default_factory=list)   # ¡no [] a secas!
```

- Los campos se declaran con `nombre: tipo` (la anotación de tipo es obligatoria acá, aunque Python no la verifica).
- Un valor por defecto **mutable** (lista, dict) va con `field(default_factory=list)`: por la misma trampa del default mutable de las funciones (R01-N08), cada objeto necesita su propia lista.
- `@dataclass(frozen=True)` hace objetos que no se pueden modificar y que sirven como clave de diccionario o elemento de un set.

### Código de ejemplo

```python
"""Clases y objetos: el molde y las piezas."""

from dataclasses import dataclass, field
import math


# =========================================================
# Una clase es un MOLDE; cada objeto hecho con ella es una PIEZA
# =========================================================
class Personaje:
    """Un personaje con nombre y vida."""

    especie = "humana"            # atributo de CLASE: lo comparten todos

    def __init__(self, nombre, vida=100):
        # __init__ arma cada objeto nuevo. self es "este objeto".
        self.nombre = nombre      # atributos de INSTANCIA: cada uno tiene los suyos
        self.vida = vida
        self.vida_max = vida

    def recibir(self, danio):
        """Un método: una función que trabaja sobre self."""
        self.vida = max(0, self.vida - danio)

    @property
    def porcentaje(self):
        """Se usa como un atributo (sin paréntesis), pero se calcula."""
        return self.vida / self.vida_max

    def __str__(self):
        """Cómo se ve con print()."""
        return f"{self.nombre} ({self.vida}/{self.vida_max})"


mia = Personaje("Mia")
tilo = Personaje("Tilo", vida=150)
tilo.recibir(40)
print(mia)
print(tilo)
print(f"Tilo está al {tilo.porcentaje:.0%}")
print("especie:", mia.especie, "y", tilo.especie)


# =========================================================
# Métodos especiales: que tus objetos funcionen con + == print…
# =========================================================
class Vec2:
    """Una posición o un desplazamiento en el mapa."""

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, otro):          # a + b
        return Vec2(self.x + otro.x, self.y + otro.y)

    def __mul__(self, k):             # a * 2
        return Vec2(self.x * k, self.y * k)

    def __eq__(self, otro):           # a == b
        return isinstance(otro, Vec2) and (self.x, self.y) == (otro.x, otro.y)

    def __repr__(self):               # cómo se ve en una lista o en la consola
        return f"Vec2({self.x}, {self.y})"

    def largo(self):
        return math.hypot(self.x, self.y)


a = Vec2(3, 4)
print(a + Vec2(1, 1))
print(a * 2)
print(a == Vec2(3, 4))
print("largo de a:", a.largo())


# =========================================================
# @dataclass: Python escribe __init__, __repr__ y __eq__ por vos
# =========================================================
@dataclass
class Item:
    nombre: str
    valor: int = 0

    def vender(self):
        return self.valor // 2


@dataclass
class Jugador:
    nombre: str
    vida: int = 100
    inventario: list = field(default_factory=list)   # una lista NUEVA para cada jugador

    def recoger(self, item):
        self.inventario.append(item)


pocion = Item("Poción", valor=25)
print(pocion)
print(pocion == Item("Poción", 25))
j = Jugador("Mia")
j.recoger(pocion)
print(j)


# frozen=True: no se puede modificar y sirve como clave de dict o elemento de set
@dataclass(frozen=True)
class Celda:
    fila: int
    col: int


visitadas = {Celda(0, 0), Celda(1, 2), Celda(0, 0)}
print("celdas distintas:", len(visitadas))
```

### Salida esperada

```
Mia (100/100)
Tilo (110/150)
Tilo está al 73%
especie: humana y humana
Vec2(4, 5)
Vec2(6, 8)
True
largo de a: 5.0
Item(nombre='Poción', valor=25)
True
Jugador(nombre='Mia', vida=100, inventario=[Item(nombre='Poción', valor=25)])
celdas distintas: 2
```

### ¿Para qué sirve?

Las clases son la forma de modelar "cosas" en casi cualquier programa: un `Usuario` con su correo y su clave, un `Producto` con precio y stock, una `Factura` con sus ítems y su total, un `Sensor` que sabe leer su valor. Las bibliotecas que vas a usar (para web, juegos o datos) te dan clases listas: un `DataFrame` de pandas o un `Sprite` de pygame son objetos con sus atributos y métodos.

### Errores habituales

**Esqueleto: el atributo que no existe** (`AttributeError`):

```
AttributeError: 'Personaje' object has no attribute 'vdia'. Did you mean: 'vida'?
```

Un error de tipeo al leer o escribir un atributo. Ojo: **asignar** con un nombre mal escrito (`mia.vdia = 50`) no da error: crea un atributo nuevo y el verdadero queda igual (un ogro).

**Goblin: olvidar `self`**:

```
TypeError: Personaje.recibir() takes 1 positional argument but 2 were given
```

Pasa cuando escribís `def recibir(danio):` sin `self`: Python igual le pasa el objeto como primer argumento.

**Esqueleto: `vida = vida` en lugar de `self.vida = vida`**: adentro de `__init__`, sin `self.`, la variable es local y desaparece al terminar. Después aparece el `AttributeError`.

**Troll: el default mutable** en una clase normal: `def __init__(self, items=[])` comparte **la misma lista** entre todos los objetos. Usá `None` y creala adentro, o `field(default_factory=list)` en una dataclass.

### Misión R02-N01-M1 · El vector que apunta

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

La clase `Vec2` representa posiciones y desplazamientos en el mapa. Agregale:

1. `__truediv__`, para que `v / 2` divida las dos coordenadas.
2. `normalizado()`, que devuelva un `Vec2` **nuevo** con el mismo sentido y largo 1 (dividí por el largo). El vector `(0, 0)` no tiene sentido: devolvé `Vec2(0, 0)` para no dividir por cero.

Probalo con `Vec2(3, 4)` y con `Vec2(0, 0)`.

#### Criterio de aprobación

- `v / 2` funciona gracias a `__truediv__`.
- `normalizado()` devuelve un objeto nuevo de largo 1 y no modifica el original.
- El vector `(0, 0)` no provoca `ZeroDivisionError`.

#### Código inicial

```python
import math


class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, otro):
        return Vec2(self.x + otro.x, self.y + otro.y)

    def __sub__(self, otro):
        return Vec2(self.x - otro.x, self.y - otro.y)

    def __mul__(self, k):
        return Vec2(self.x * k, self.y * k)

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def largo(self):
        return math.hypot(self.x, self.y)
```

#### Salida esperada

```
Vec2(1.5, 2.0)
Vec2(0.6, 0.8) largo: 1.0
Vec2(0, 0)
```

#### Solución de referencia

```python
import math


class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, otro):
        return Vec2(self.x + otro.x, self.y + otro.y)

    def __sub__(self, otro):
        return Vec2(self.x - otro.x, self.y - otro.y)

    def __mul__(self, k):
        return Vec2(self.x * k, self.y * k)

    def __truediv__(self, k):
        return Vec2(self.x / k, self.y / k)

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def largo(self):
        return math.hypot(self.x, self.y)

    def normalizado(self):
        """Mismo sentido, largo 1. El vector (0, 0) no tiene sentido: se devuelve igual."""
        largo = self.largo()
        if largo == 0:
            return Vec2(0, 0)
        return self / largo


flecha = Vec2(3, 4)
print(flecha / 2)
unidad = flecha.normalizado()
print(unidad, "largo:", unidad.largo())
print(Vec2(0, 0).normalizado())
```

### Misión R02-N01-M2 · El enemigo que acecha

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con `@dataclass`, definí `Vec2` (con `x`, `y` y un método `distancia(otro)`) y `Enemigo` con `nombre`, `vida` y `pos: Vec2`. Agregale a `Enemigo` el método `esta_cerca(objetivo, radio)`, que diga si el enemigo está a `radio` o menos de la posición `objetivo`.

Con Mia en `(2, 3)`, revisá una horda de tres enemigos: Slime en `(3, 3)`, Orco en `(10, 1)` y Goblin en `(2, 7)`, con radio 4.

#### Criterio de aprobación

- Usa `@dataclass` para las dos clases (sin escribir `__init__`).
- `esta_cerca` usa la distancia y devuelve `True` o `False`.
- Muestra que Slime y Goblin están cerca y Orco lejos.

#### Salida esperada

```
Slime: ¡cerca!
Orco: lejos
Goblin: ¡cerca!
```

#### Solución de referencia

```python
from dataclasses import dataclass
import math


@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0

    def distancia(self, otro):
        return math.hypot(self.x - otro.x, self.y - otro.y)


@dataclass
class Enemigo:
    nombre: str
    vida: int
    pos: Vec2

    def esta_cerca(self, objetivo, radio):
        return self.pos.distancia(objetivo) <= radio


mia = Vec2(2, 3)
horda = [Enemigo("Slime", 20, Vec2(3, 3)), Enemigo("Orco", 40, Vec2(10, 1)), Enemigo("Goblin", 30, Vec2(2, 7))]
for enemigo in horda:
    alerta = "¡cerca!" if enemigo.esta_cerca(mia, radio=4) else "lejos"
    print(f"{enemigo.nombre}: {alerta}")
```

### Misión R02-N01-M3 · El tasador ordena

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí una clase `Item` (sin dataclass) con `nombre` y `valor`, un `__repr__` que la muestre como `Espada ($120)` y un `__lt__` que compare por valor.

Con un botín de cuatro ítems, mostrá la lista ordenada con `sorted()`, los dos más caros y el más barato con `min()`.

#### Criterio de aprobación

- `__lt__` compara por valor y con eso funcionan `sorted()` y `min()` sin `key=`.
- `__repr__` muestra nombre y valor.
- Muestra el botín ordenado, los dos más caros y el más barato.

#### Salida esperada

```
[Pan ($3), Poción ($25), Llave ($100), Espada ($120)]
[Espada ($120), Llave ($100)]
el más barato: Pan ($3)
```

#### Solución de referencia

```python
class Item:
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def __lt__(self, otro):
        """a < b compara por valor: con esto, sorted() sabe ordenar Items."""
        return self.valor < otro.valor

    def __repr__(self):
        return f"{self.nombre} (${self.valor})"


botin = [Item("Espada", 120), Item("Poción", 25), Item("Llave", 100), Item("Pan", 3)]
print(sorted(botin))
print(sorted(botin, reverse=True)[:2])
print("el más barato:", min(botin))
```

### Encargo R02-N01-E1 · La cuenta del Gremio

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El Gremio abre cuentas a sus socios. Escribí `CuentaGremio` con titular, saldo inicial e historial de movimientos:

- `depositar(monto)`: solo montos positivos.
- `extraer(monto)`: solo si alcanza el saldo.
- El saldo se guarda en `_saldo` y se lee con una `@property saldo` (desde afuera no se puede asignar).
- `__str__` muestra `Titular: $saldo`.

#### Criterio de aprobación

- El saldo solo cambia con `depositar` y `extraer`, que validan el monto.
- Tiene una `@property saldo` de solo lectura.
- Guarda el historial de movimientos.

#### Salida esperada

```
Saldo insuficiente: tenés 750.
El depósito tiene que ser positivo.
Tilo: $450
movimientos: ['+250', '-300']
```

#### Solución de referencia

```python
class CuentaGremio:
    """Cuenta de un socio del Gremio: el saldo solo cambia con depósitos y extracciones."""

    def __init__(self, titular, saldo=0):
        self.titular = titular
        self._saldo = saldo           # el _ avisa: "no lo toques desde afuera"
        self.historial = []

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, monto):
        if monto <= 0:
            print("El depósito tiene que ser positivo.")
            return
        self._saldo += monto
        self.historial.append(f"+{monto}")

    def extraer(self, monto):
        if monto > self._saldo:
            print(f"Saldo insuficiente: tenés {self._saldo}.")
            return
        self._saldo -= monto
        self.historial.append(f"-{monto}")

    def __str__(self):
        return f"{self.titular}: ${self._saldo}"


cuenta = CuentaGremio("Tilo", 500)
cuenta.depositar(250)
cuenta.extraer(1000)
cuenta.extraer(300)
cuenta.depositar(-5)
print(cuenta)
print("movimientos:", cuenta.historial)
```

### Prueba del sello

#### ¿Qué diferencia hay entre una clase y un objeto?

La clase es el **molde** (define qué datos y métodos hay); el objeto es una **pieza** hecha con ese molde, con sus propios valores.

#### ¿Qué es `self` y por qué no se escribe al llamar a un método?

Es el objeto sobre el que se llama el método. Python lo pasa solo: `mia.recibir(5)` equivale a `Personaje.recibir(mia, 5)`.

#### ¿Cuándo se ejecuta `__init__`?

Cada vez que se crea un objeto nuevo, por ejemplo `Personaje("Mia")`.

#### ¿Qué hace `@dataclass` por vos?

Escribe `__init__`, `__repr__` y `__eq__` a partir de los campos declarados.

#### ¿Por qué en una dataclass no se escribe `items: list = []`?

Porque todos los objetos compartirían la misma lista. Se usa `field(default_factory=list)`, que crea una lista nueva para cada uno.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/12-Clases` (que estaba pensado como diferencia con C++). Clave: que entiendan `self` con la equivalencia `mia.recibir(5)` = `Personaje.recibir(mia, 5)`.

## R02-N02 · Herencia y polimorfismo

```meta
tipo: tema
padre: R02-N01
precio: 10
criatura: goblin
temas: poo.herencia, poo.polimorfismo, poo.abstractas
```

### Crónica

Sila le cuenta que alguien está mezclando los registros de la Biblioteca. Para entender qué pasa, la lleva al **Ala de Estrategia**: un mapa de batalla con héroes, enemigos y torres de defensa. Todos tienen vida, todos reciben daño, todos juegan su turno… pero cada uno **a su manera**.

—No escribas cada uno desde cero, Mia —dice Sila—. Escribí lo **común** una vez y dejá que cada uno **herede** y cambie solo lo que lo hace distinto.

### Objetivos

- Crear subclases que heredan de otra y usar `super()`.
- Aprovechar el polimorfismo: la misma llamada, distinto comportamiento.
- Definir clases abstractas con `abc` y entender el *duck typing*.

### Antes de empezar

Clases y objetos (R02-N01).

### Explicación

#### Herencia: "es un"

Si un `Heroe` **es una** `Entidad` (tiene nombre y vida, recibe daño), no hace falta repetir todo:

```python
class Entidad:
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)


class Heroe(Entidad):                 # Heroe hereda de Entidad
    def __init__(self, nombre):
        super().__init__(nombre, 100)  # que Entidad arme lo suyo
        self.pociones = 2              # y después, lo propio
```

- `class Heroe(Entidad):` dice que `Heroe` **hereda** todos los atributos y métodos de `Entidad` (la clase **base** o **padre**).
- `super().__init__(...)` llama al `__init__` de la base. Si lo olvidás, el héroe no tiene `nombre` ni `vida`.
- Una subclase puede **redefinir** (*override*) un método: si `Heroe` tiene su propio `recibir`, se usa ese. Dentro, `super().recibir(danio)` sigue llamando al de la base.

#### Polimorfismo: la misma llamada, distintas respuestas

```python
for e in [Heroe("Mia"), Enemigo("Orco", 40, 6), TorreDefensiva()]:
    e.turno(objetivo)
```

El bucle no pregunta de qué clase es cada uno: cada objeto sabe cómo jugar **su** turno. Agregar un tipo nuevo de enemigo no obliga a tocar el bucle. Esa es la gran ventaja: el código que **usa** los objetos no se llena de `if tipo == ...`.

#### Clases abstractas: "todos tienen que saber hacer esto"

```python
from abc import ABC, abstractmethod

class Entidad(ABC):
    @abstractmethod
    def turno(self, objetivo):
        ...
```

Una clase con métodos abstractos **no se puede crear** directamente, y toda subclase **tiene** que implementarlos. Si falta alguno, al crear el objeto aparece un `TypeError`. Es una forma de dejar escrito el contrato.

#### Duck typing: "si camina como pato…"

Python no exige herencia para el polimorfismo. `TorreDefensiva` no hereda de `Entidad`, pero tiene `vivo()`, `recibir()` y `turno()`, y el bucle la acepta igual. Lo que importa es **qué métodos tiene**, no de qué clase viene.

#### `isinstance`

`isinstance(mia, Entidad)` da `True` si `mia` es de esa clase **o de una subclase**. Usalo poco: si te encontrás preguntando el tipo para decidir qué hacer, probablemente ese comportamiento tendría que ser un método.

#### Herencia o no

Usá herencia cuando la relación es "**es un**" (un héroe es una entidad). Si es "**tiene un**" (un héroe tiene un inventario), no heredes: guardá el otro objeto como atributo (composición).

### Código de ejemplo

```python
"""Herencia, polimorfismo y duck typing: una compañía, muchos comportamientos."""

from abc import ABC, abstractmethod
import random


# =========================================================
# Clase base ABSTRACTA: define lo común y exige lo que falta
# =========================================================
class Entidad(ABC):
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    def vivo(self):
        return self.vida > 0

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)
        print(f"  {self.nombre} recibe {danio} (vida {self.vida})")

    @abstractmethod
    def turno(self, objetivo):
        """Cada subclase decide qué hace en su turno."""


# =========================================================
# Subclases: HEREDAN todo de Entidad y agregan o cambian lo suyo
# =========================================================
class Heroe(Entidad):
    def __init__(self, nombre, vida=100):
        super().__init__(nombre, vida)      # primero, lo que arma Entidad
        self.pociones = 2                   # después, lo propio del héroe

    def turno(self, objetivo):
        if self.vida < 30 and self.pociones > 0:
            self.pociones -= 1
            self.vida += 40
            print(f"  {self.nombre} toma una poción (vida {self.vida})")
        else:
            objetivo.recibir(random.randint(8, 14))


class Enemigo(Entidad):
    def __init__(self, nombre, vida, danio):
        super().__init__(nombre, vida)
        self.danio = danio

    def turno(self, objetivo):
        objetivo.recibir(self.danio + random.randint(0, 3))


# =========================================================
# Polimorfismo: la misma llamada, cada objeto responde a su manera
# =========================================================
def ronda(entidades, objetivo):
    for e in entidades:
        if e.vivo():
            e.turno(objetivo)       # no pregunta de qué clase es cada uno


# =========================================================
# Duck typing: NO hereda de Entidad, pero tiene los mismos métodos,
# así que ronda() la acepta igual. "Si camina como pato y hace cuac…"
# =========================================================
class TorreDefensiva:
    def __init__(self):
        self.nombre = "Torreta"
        self.vida = 1

    def vivo(self):
        return self.vida > 0

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)
        print(f"  {self.nombre} recibe {danio} (vida {self.vida})")

    def turno(self, objetivo):
        objetivo.recibir(5)


random.seed(3)
heroe = Heroe("Mia")
horda = [Enemigo("Orco", 40, 6), Enemigo("Slime", 20, 3), TorreDefensiva()]

numero = 1
while heroe.vivo() and any(e.vivo() for e in horda):
    print(f"--- turno {numero} ---")
    heroe.turno(next(e for e in horda if e.vivo()))
    ronda(horda, heroe)
    numero += 1

print("gana el héroe" if heroe.vivo() else "cae el héroe")
print("¿Mia es una Entidad?", isinstance(heroe, Entidad))
print("¿la torreta es una Entidad?", isinstance(horda[2], Entidad))
```

### Salida esperada

```
--- turno 1 ---
  Orco recibe 9 (vida 31)
  Mia recibe 7 (vida 93)
  Mia recibe 5 (vida 88)
  Mia recibe 5 (vida 83)
--- turno 2 ---
  Orco recibe 12 (vida 19)
  Mia recibe 9 (vida 74)
  Mia recibe 3 (vida 71)
  Mia recibe 5 (vida 66)
--- turno 3 ---
  Orco recibe 12 (vida 7)
  Mia recibe 6 (vida 60)
  Mia recibe 6 (vida 54)
  Mia recibe 5 (vida 49)
--- turno 4 ---
  Orco recibe 10 (vida 0)
  Mia recibe 4 (vida 45)
  Mia recibe 5 (vida 40)
--- turno 5 ---
  Slime recibe 9 (vida 11)
  Mia recibe 6 (vida 34)
  Mia recibe 5 (vida 29)
--- turno 6 ---
  Mia toma una poción (vida 69)
  Mia recibe 6 (vida 63)
  Mia recibe 5 (vida 58)
--- turno 7 ---
  Slime recibe 11 (vida 0)
  Mia recibe 5 (vida 53)
--- turno 8 ---
  Torreta recibe 13 (vida 0)
gana el héroe
¿Mia es una Entidad? True
¿la torreta es una Entidad? False
```

### ¿Para qué sirve?

El polimorfismo está en todo sistema que maneja "variantes" de algo: medios de pago (efectivo, débito, crédito) que calculan distinto el total; notificaciones que se envían por correo, SMS o WhatsApp con la misma llamada `enviar()`; figuras de un programa de dibujo que saben dibujarse cada una. Los frameworks web y de juegos se basan en heredar de sus clases (un `Sprite`, una vista) y redefinir un par de métodos.

### Errores habituales

**Goblin: crear una clase abstracta o una subclase incompleta** (`TypeError`):

```
TypeError: Can't instantiate abstract class Guerrero without an implementation for abstract method 'turno'
```

Te falta implementar ese método en la subclase (revisá también que el nombre esté bien escrito).

**Esqueleto: olvidar `super().__init__`** en la subclase:

```
AttributeError: 'Heroe' object has no attribute 'nombre'
```

Si la subclase tiene su propio `__init__`, el de la base **no** se ejecuta solo.

**Ogro: redefinir un método con otro nombre**: si la base llama a `turno()` y la subclase define `Turno()` o `turn()`, no hay error, pero se sigue usando el de la base.

**Ogro: heredar para reutilizar código cuando no hay relación "es un"**: la herencia se vuelve un laberinto. Preferí la composición.

### Misión R02-N02-M1 · El jefe furioso

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Creá `Jefe(Enemigo)`: un enemigo que cuenta sus turnos y **cada 3 turnos entra en furia** y pega el doble de su daño (mostrando un aviso). En los demás turnos juega igual que un `Enemigo`: usá `super().turno(objetivo)`.

Probalo con `random.seed(1)`: un Rey Slime (200 de vida, 5 de daño) juega 6 turnos contra un muñeco de práctica de 100 de vida (una subclase mínima de `Entidad` cuyo `turno` no hace nada).

#### Criterio de aprobación

- `Jefe` hereda de `Enemigo` y llama a `super().__init__`.
- Cuenta los turnos y en los múltiplos de 3 pega el doble.
- En los otros turnos reutiliza `super().turno(objetivo)`.

#### Código inicial

```python
from abc import ABC, abstractmethod
import random


class Entidad(ABC):
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    def vivo(self):
        return self.vida > 0

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)
        print(f"  {self.nombre} recibe {danio} (vida {self.vida})")

    @abstractmethod
    def turno(self, objetivo):
        """Cada subclase decide qué hace en su turno."""


class Enemigo(Entidad):
    def __init__(self, nombre, vida, danio):
        super().__init__(nombre, vida)
        self.danio = danio

    def turno(self, objetivo):
        objetivo.recibir(self.danio + random.randint(0, 3))


# Escribí la clase Jefe(Enemigo)
```

#### Salida esperada

```
  Muñeco de práctica recibe 6 (vida 94)
  Muñeco de práctica recibe 5 (vida 89)
  ¡Rey Slime entra en furia!
  Muñeco de práctica recibe 10 (vida 79)
  Muñeco de práctica recibe 7 (vida 72)
  Muñeco de práctica recibe 5 (vida 67)
  ¡Rey Slime entra en furia!
  Muñeco de práctica recibe 10 (vida 57)
```

#### Solución de referencia

```python
from abc import ABC, abstractmethod
import random


class Entidad(ABC):
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    def vivo(self):
        return self.vida > 0

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)
        print(f"  {self.nombre} recibe {danio} (vida {self.vida})")

    @abstractmethod
    def turno(self, objetivo):
        """Cada subclase decide qué hace en su turno."""


class Enemigo(Entidad):
    def __init__(self, nombre, vida, danio):
        super().__init__(nombre, vida)
        self.danio = danio

    def turno(self, objetivo):
        objetivo.recibir(self.danio + random.randint(0, 3))


class Jefe(Enemigo):
    """Un enemigo que cada 3 turnos entra en furia y pega el doble."""

    def __init__(self, nombre, vida, danio):
        super().__init__(nombre, vida, danio)
        self.turnos = 0

    def turno(self, objetivo):
        self.turnos += 1
        if self.turnos % 3 == 0:
            print(f"  ¡{self.nombre} entra en furia!")
            objetivo.recibir(self.danio * 2)
        else:
            super().turno(objetivo)       # el turno normal de Enemigo


class Muñeco(Entidad):
    def turno(self, objetivo):
        pass


random.seed(1)
jefe = Jefe("Rey Slime", 200, 5)
muñeco = Muñeco("Muñeco de práctica", 100)
for _ in range(6):
    jefe.turno(muñeco)
```

### Misión R02-N02-M2 · La curandera

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Creá `Curandero` **sin heredar** de `Entidad` (duck typing): tiene `nombre`, `vida`, una lista de `aliados` y los métodos `vivo()`, `recibir()` y `turno(objetivo)`. En su turno, en lugar de atacar, cura 15 al aliado vivo con **menos vida**.

Armá una ronda con Mia (40), Tilo (25) y la curandera Sila contra un orco: dos rondas en las que los héroes atacan, Sila cura y el orco le pega a Tilo. Usá `random.seed(4)`.

#### Criterio de aprobación

- `Curandero` no hereda de `Entidad`, pero la función `ronda` lo acepta igual.
- Cura al aliado vivo con menos vida (`min(..., key=...)`).
- La ronda llama a `turno()` sin preguntar la clase de cada uno.

#### Código inicial

```python
from abc import ABC, abstractmethod
import random


class Entidad(ABC):
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    def vivo(self):
        return self.vida > 0

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)
        print(f"  {self.nombre} recibe {danio} (vida {self.vida})")

    @abstractmethod
    def turno(self, objetivo):
        """Cada subclase decide qué hace en su turno."""


class Enemigo(Entidad):
    def __init__(self, nombre, vida, danio):
        super().__init__(nombre, vida)
        self.danio = danio

    def turno(self, objetivo):
        objetivo.recibir(self.danio + random.randint(0, 3))


# Escribí Heroe, Curandero y la función ronda
```

#### Salida esperada

```
--- ronda 1 ---
  Orco recibe 10 (vida 50)
  Orco recibe 10 (vida 40)
  Sila cura a Tilo (vida 40)
  Tilo recibe 6 (vida 34)
--- ronda 2 ---
  Orco recibe 10 (vida 30)
  Orco recibe 10 (vida 20)
  Sila cura a Tilo (vida 49)
  Tilo recibe 7 (vida 42)
```

#### Solución de referencia

```python
from abc import ABC, abstractmethod
import random


class Entidad(ABC):
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    def vivo(self):
        return self.vida > 0

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)
        print(f"  {self.nombre} recibe {danio} (vida {self.vida})")

    @abstractmethod
    def turno(self, objetivo):
        """Cada subclase decide qué hace en su turno."""


class Enemigo(Entidad):
    def __init__(self, nombre, vida, danio):
        super().__init__(nombre, vida)
        self.danio = danio

    def turno(self, objetivo):
        objetivo.recibir(self.danio + random.randint(0, 3))


class Heroe(Entidad):
    def turno(self, objetivo):
        objetivo.recibir(10)


class Curandero:
    """No hereda de Entidad: alcanza con que tenga vivo(), recibir() y turno()."""

    def __init__(self, nombre, aliados):
        self.nombre = nombre
        self.vida = 60
        self.aliados = aliados

    def vivo(self):
        return self.vida > 0

    def recibir(self, danio):
        self.vida = max(0, self.vida - danio)

    def turno(self, objetivo):
        vivos = [a for a in self.aliados if a.vivo()]
        herido = min(vivos, key=lambda a: a.vida)
        herido.vida += 15
        print(f"  {self.nombre} cura a {herido.nombre} (vida {herido.vida})")


def ronda(entidades, objetivo):
    for e in entidades:
        if e.vivo():
            e.turno(objetivo)


mia = Heroe("Mia", 40)
tilo = Heroe("Tilo", 25)
sila = Curandero("Sila", [mia, tilo])
orco = Enemigo("Orco", 60, 5)

random.seed(4)
for numero in range(1, 3):
    print(f"--- ronda {numero} ---")
    ronda([mia, tilo, sila], orco)
    orco.turno(tilo)
```

### Misión R02-N02-M3 · Las fichas de la compañía

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Agregale a `Entidad` un segundo método abstracto: `descripcion()`, que devuelva una línea que presente al personaje. Creá `Guerrero`, `Maga` y `Picaro`, cada una con su `descripcion()`.

Antes de terminar, **probá** crear un `Picaro` sin `descripcion()` y leé el error. Después implementalo y mostrá la ficha de toda la compañía con un solo bucle.

#### Criterio de aprobación

- `descripcion` es abstracto en `Entidad` y cada subclase lo implementa.
- Hay un comentario con el `TypeError` que apareció al faltar el método.
- Un solo bucle muestra la ficha de toda la compañía.

#### Salida esperada

```
La compañía:
 - Tilo, guerrero de primera línea (150 de vida)
 - Sila, maga del fuego (80 de vida)
 - Baldo, pícaro sigiloso (90 de vida)
```

#### Solución de referencia

```python
from abc import ABC, abstractmethod


class Entidad(ABC):
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    @abstractmethod
    def turno(self, objetivo):
        ...

    @abstractmethod
    def descripcion(self):
        """Una línea que presenta al personaje."""


class Guerrero(Entidad):
    def turno(self, objetivo):
        pass

    def descripcion(self):
        return f"{self.nombre}, guerrero de primera línea ({self.vida} de vida)"


class Maga(Entidad):
    def turno(self, objetivo):
        pass

    def descripcion(self):
        return f"{self.nombre}, maga del fuego ({self.vida} de vida)"


class Picaro(Entidad):
    def turno(self, objetivo):
        pass

    def descripcion(self):
        return f"{self.nombre}, pícaro sigiloso ({self.vida} de vida)"


# Si Picaro no tuviera descripcion(), crearlo daría:
# TypeError: Can't instantiate abstract class Picaro without an implementation
# for abstract method 'descripcion'

compania = [Guerrero("Tilo", 150), Maga("Sila", 80), Picaro("Baldo", 90)]
print("La compañía:")
for integrante in compania:
    print(" -", integrante.descripcion())
```

### Encargo R02-N02-E1 · Los medios de pago del mercado

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El mercado acepta varios medios de pago. Escribí una clase abstracta `MedioDePago` con `total(monto)` abstracto y un método común `ticket(monto)` que muestre el nombre de la clase y el total alineados.

- `Efectivo`: 10 % de descuento.
- `Debito`: sin cambios.
- `Credito(cuotas)`: en 1 cuota, sin recargo; si no, 5 % por cuota.

Mostrá el ticket de una compra de $20.000 con cada medio (crédito en 1 y en 6 cuotas).

#### Criterio de aprobación

- `MedioDePago` es abstracta y `ticket` está escrito una sola vez, en la base.
- Cada subclase implementa su propio `total`.
- Un bucle muestra los cuatro tickets.

#### Salida esperada

```
Efectivo      $ 18,000.00
Debito        $ 20,000.00
Credito       $ 20,000.00
Credito       $ 26,000.00
```

#### Solución de referencia

```python
from abc import ABC, abstractmethod


class MedioDePago(ABC):
    @abstractmethod
    def total(self, monto):
        """Lo que termina pagando el cliente."""

    def ticket(self, monto):
        return f"{type(self).__name__:<14}${self.total(monto):>10,.2f}"


class Efectivo(MedioDePago):
    def total(self, monto):
        return monto * 0.90            # 10 % de descuento


class Debito(MedioDePago):
    def total(self, monto):
        return monto


class Credito(MedioDePago):
    def __init__(self, cuotas):
        self.cuotas = cuotas

    def total(self, monto):
        recargo = 0.0 if self.cuotas == 1 else 0.05 * self.cuotas
        return monto * (1 + recargo)


compra = 20000
for medio in [Efectivo(), Debito(), Credito(1), Credito(6)]:
    print(medio.ticket(compra))
```

### Prueba del sello

#### ¿Qué hereda una subclase?

Todos los atributos y métodos de la clase base. Puede agregar los suyos y redefinir los que quiera.

#### ¿Para qué sirve `super().__init__(...)`?

Para que la clase base arme su parte del objeto. Si la subclase tiene su propio `__init__`, el de la base no se ejecuta solo.

#### ¿Qué es el polimorfismo?

Que la misma llamada (`e.turno(x)`) haga cosas distintas según la clase de cada objeto, sin preguntar el tipo.

#### ¿Qué pasa si una subclase no implementa un método abstracto?

No se puede crear: aparece un `TypeError` al instanciarla.

#### ¿Qué es el duck typing?

Aceptar cualquier objeto que tenga los métodos necesarios, herede o no de una clase en particular.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/14-Herencia-Polimorfismo`. El ejemplo del combate usa `random.seed(3)`: la salida es siempre la misma y se puede comparar con la esperada.

## R02-N03 · Excepciones y archivos

```meta
tipo: tema
padre: R02-N02
precio: 10
criatura: goblin
temas: err.excepciones, arch.texto, arch.rutas
```

### Crónica

Los registros dañados vienen del **Sótano**. Ahí los pergaminos están húmedos, rotos o directamente no están. Un aprendiz intentó leer uno que no existía y el hechizo le explotó en la cara.

—Un buen mago no espera que todo salga bien —dice {mentor}—. **Intenta**, y tiene preparado qué hacer si sale mal. Y cuando abre un pergamino, **siempre** lo vuelve a cerrar.

Entre la humedad, Mia encuentra **notas del viajero del vitral, a medio borrar**. Por primera vez, el error no le da miedo: lo espera.

### Objetivos

- Capturar errores con `try` / `except` / `else` / `finally`.
- Lanzar errores con `raise` y crear excepciones propias.
- Leer y escribir archivos de texto con `with` y `pathlib`.

### Antes de empezar

Clases y herencia (R02-N01 y R02-N02): las excepciones son clases. Ya viste muchos tracebacks desde la Clase 0.

### Explicación

#### Qué es una excepción

Cuando algo sale mal en plena ejecución (convertir `"abc"` a número, dividir por cero, abrir un archivo que no existe), Python **lanza una excepción**: corta lo que estaba haciendo y, si nadie la atrapa, termina el programa con el traceback. Cada tipo de problema es una clase: `ValueError`, `ZeroDivisionError`, `FileNotFoundError`, `KeyError`…

#### `try` / `except`

```python
try:
    nivel = int(texto)          # lo que puede fallar
except ValueError:
    nivel = 1                   # qué hacer si falla
```

- Si el bloque `try` funciona, el `except` se saltea.
- Si lanza un `ValueError`, Python salta al `except` y el programa **sigue**.
- Si lanza **otro** tipo de error, no se atrapa: sigue de largo como siempre.
- `except ValueError as error:` guarda el error para mostrar su mensaje.
- Se pueden poner varios `except`, uno por tipo. Como las excepciones son clases, `except Exception` atrapa casi todo… y justamente por eso **no conviene**: esconde errores que no esperabas. Atrapá lo que sabés manejar.

#### `else` y `finally`

```python
try:
    n = int(texto)
except ValueError:
    print("no es un número")
else:
    print("ok")            # solo si NO hubo error
finally:
    print("fin")           # SIEMPRE, con error o sin él
```

#### Lanzar errores: `raise`

Tus funciones también pueden avisar que algo está mal: `raise ValueError("la vida tiene que ser positiva")`. Es mejor que devolver un valor raro (`-1`, `None`) que quien llama puede olvidarse de revisar.

#### Excepciones propias

```python
class VidaInvalida(Exception):
    pass

raise VidaInvalida("vino -10")
```

Una excepción propia es una clase que hereda de `Exception`. Le da nombre al problema de **tu** programa y permite atraparlo aparte. Si armás varias relacionadas, hacé que hereden de una base común (`ErrorDeTienda` → `OroInsuficiente`, `SinStock`) para poder atraparlas juntas.

#### Pedir perdón en vez de permiso (EAFP)

En Python es común **intentar** y atrapar el error, en lugar de revisar todo antes:

```python
try:
    precio = precios[objeto]
except KeyError:
    precio = 0
```

#### Archivos: `open` y `with`

```python
with open("puntajes.txt", "w", encoding="utf-8") as f:
    f.write("Mia,1200\n")

with open("puntajes.txt", encoding="utf-8") as f:
    for linea in f:
        print(linea.strip())
```

- El modo: `"r"` leer (por defecto), `"w"` escribir (**borra** lo que había), `"a"` agregar al final.
- `with` **cierra el archivo solo** al salir del bloque, aunque haya un error en el medio.
- Declará siempre `encoding="utf-8"` para que los acentos y la ñ se lean bien en cualquier compu.
- Recorrer el archivo con `for` lee **línea por línea**; cada línea trae su `\n` al final (`strip()` lo saca).

#### `pathlib`: rutas como objetos

`Path("partidas") / "slot1.txt"` arma rutas que funcionan en Windows, Linux y Mac. Tiene atajos: `.exists()`, `.read_text()`, `.write_text()`, `.unlink()` (borrar).

En la plataforma, los archivos que crea tu programa viven en una memoria temporal del navegador: podés escribirlos y leerlos mientras se ejecuta, pero no quedan en tu compu.

### Código de ejemplo

```python
"""Excepciones y archivos: intentá, y si sale mal, que no se caiga todo."""

from pathlib import Path


# =========================================================
# try / except / else / finally
# =========================================================
def leer_nivel(texto):
    try:
        nivel = int(texto)              # lo que puede fallar
    except ValueError:
        print(f"  '{texto}' no es un número: uso nivel 1")
        return 1
    else:
        print(f"  nivel {nivel} ok")    # solo si NO hubo error
        return nivel
    finally:
        print("  (fin de la lectura)")  # SIEMPRE, haya error o no


leer_nivel("5")
leer_nivel("difícil")


# =========================================================
# Capturar varios tipos, y ver el mensaje del error
# =========================================================
mochila = ["antorcha", "cuerda"]
for pedido in [0, 5, "dos"]:
    try:
        print("sacás:", mochila[pedido])
    except IndexError:
        print(f"no hay nada en la posición {pedido}")
    except TypeError as error:
        print("pedido raro:", error)


# =========================================================
# raise y excepciones propias
# =========================================================
class VidaInvalida(Exception):
    """Una vida que no tiene sentido (cero o negativa)."""


def crear_heroe(nombre, vida):
    if vida <= 0:
        raise VidaInvalida(f"la vida de {nombre} tiene que ser mayor que 0 (vino {vida})")
    return {"nombre": nombre, "vida": vida}


try:
    crear_heroe("Baldo", -10)
except VidaInvalida as error:
    print("error controlado:", error)


# =========================================================
# Archivos: with los cierra solo, pase lo que pase
# =========================================================
archivo = Path("puntajes.txt")

with archivo.open("w", encoding="utf-8") as f:
    for nombre, puntos in [("Mia", 1200), ("Tilo", 950), ("Sila", 1500)]:
        f.write(f"{nombre},{puntos}\n")

filas = []
with archivo.open(encoding="utf-8") as f:
    for linea in f:
        nombre, puntos = linea.strip().split(",")
        filas.append((nombre, int(puntos)))

print("ranking:")
for nombre, puntos in sorted(filas, key=lambda fila: fila[1], reverse=True):
    print(f"  {nombre:6}{puntos:>6}")

# Leer un archivo que no existe: FileNotFoundError
try:
    Path("no_existe.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    print("el pergamino no existe")

archivo.unlink()
print("¿quedó el archivo?", archivo.exists())
```

### Salida esperada

```
nivel 5 ok
  (fin de la lectura)
  'difícil' no es un número: uso nivel 1
  (fin de la lectura)
sacás: antorcha
no hay nada en la posición 5
pedido raro: list indices must be integers or slices, not str
error controlado: la vida de Baldo tiene que ser mayor que 0 (vino -10)
ranking:
  Sila    1500
  Mia     1200
  Tilo     950
el pergamino no existe
¿quedó el archivo? False
```

### ¿Para qué sirve?

Ningún programa real puede suponer que todo sale bien: el usuario escribe cualquier cosa, el archivo no está, internet se corta, la base de datos no responde. Las excepciones permiten que una app muestre "no pudimos conectarnos, probá de nuevo" en lugar de cerrarse. Y leer y escribir archivos es la base de guardar configuraciones, registros (logs), exportar reportes y procesar datos.

### Errores habituales

**Goblin: atrapar todo con `except:` a secas o `except Exception`**: el programa "no falla", pero tampoco te enterás cuando algo se rompe de verdad (un error de tipeo, un nombre mal escrito). Atrapá solo lo que sabés resolver.

**Ogro: el `try` gigante**: si envolvés 30 líneas en un `try`, no sabés cuál falló. Poné en el `try` solo la línea que puede fallar.

**Esqueleto: `FileNotFoundError`**:

```
FileNotFoundError: [Errno 2] No such file or directory: 'config.txt'
```

La ruta es relativa a la carpeta **desde donde ejecutás** el programa, no a donde está el archivo `.py`.

**Troll: abrir con `"w"` un archivo que querías conservar**: lo borra al instante, aunque no escribas nada. Para agregar, `"a"`.

**Goblin: leer un número de un archivo y olvidarse de que es texto**: `"950" > "1200"` es `True` (compara letras). Convertí con `int()`.

### Misión R02-N03-M1 · El dato rebelde

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí `pedir_entero(mensaje, minimo, maximo)`: pide un número con `input` hasta que el usuario escriba un **entero** dentro del rango, y lo devuelve. Si escribe algo que no es un número, avisa y vuelve a pedir (sin cortar el programa); si está fuera de rango, también.

Usala para pedir un nivel (1 a 10) y una cantidad de pociones (0 a 5).

#### Criterio de aprobación

- Usa `try` / `except ValueError` alrededor de la conversión.
- Vuelve a pedir si no es número o si está fuera de rango.
- Con la entrada de ejemplo muestra `Nivel 7 con 2 pociones.`

#### Entrada de ejemplo

```
cinco
15
7
-1
2
```

#### Salida esperada

```
Nivel (1-10): 'cinco' no es un número entero.
Nivel (1-10): Tiene que estar entre 1 y 10.
Nivel (1-10): Pociones (0-5): Tiene que estar entre 0 y 5.
Pociones (0-5): Nivel 7 con 2 pociones.
```

#### Solución de referencia

```python
def pedir_entero(mensaje, minimo, maximo):
    """Pide un número hasta que sea un entero entre minimo y maximo."""
    while True:
        texto = input(mensaje)
        try:
            numero = int(texto)
        except ValueError:
            print(f"'{texto}' no es un número entero.")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"Tiene que estar entre {minimo} y {maximo}.")


nivel = pedir_entero("Nivel (1-10): ", 1, 10)
pociones = pedir_entero("Pociones (0-5): ", 0, 5)
print(f"Nivel {nivel} con {pociones} pociones.")
```

#### Pruebas

##### Bordes
```entrada
1
0
```
```salida
Nivel (1-10): Pociones (0-5): Nivel 1 con 0 pociones.
```

##### Más bordes
```entrada
10
5
```
```salida
Nivel (1-10): Pociones (0-5): Nivel 10 con 5 pociones.
```

##### Decimales
```entrada
7.5
3
2
```
```salida
Nivel (1-10): '7.5' no es un número entero.
Nivel (1-10): Pociones (0-5): Nivel 3 con 2 pociones.
```

### Misión R02-N03-M2 · La configuración perdida

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí `cargar_config(ruta)`, que lea un archivo de líneas `clave=valor` y devuelva un diccionario. Si el archivo **no existe**, avisa y devuelve la configuración por defecto: `{"dificultad": "normal", "volumen": "7", "idioma": "es"}`. Lo que esté en el archivo pisa a lo por defecto.

Probala primero sin archivo; después creá `config.txt` con `dificultad=difícil` y `volumen=3` y volvé a cargarla. Al final, borrá el archivo.

#### Criterio de aprobación

- Atrapa `FileNotFoundError` y devuelve la config por defecto.
- Abre el archivo con `with` y `encoding="utf-8"`.
- Lo leído del archivo pisa los valores por defecto (el idioma sigue en `es`).

#### Salida esperada

```
No encontré config.txt: uso la configuración por defecto.
{'dificultad': 'normal', 'volumen': '7', 'idioma': 'es'}
{'dificultad': 'difícil', 'volumen': '3', 'idioma': 'es'}
```

#### Solución de referencia

```python
from pathlib import Path

POR_DEFECTO = {"dificultad": "normal", "volumen": "7", "idioma": "es"}


def cargar_config(ruta):
    """Lee líneas 'clave=valor'. Si el archivo no existe, usa la config por defecto."""
    config = dict(POR_DEFECTO)
    try:
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                if "=" in linea:
                    clave, valor = linea.strip().split("=", 1)
                    config[clave] = valor
    except FileNotFoundError:
        print(f"No encontré {ruta}: uso la configuración por defecto.")
    return config


print(cargar_config("config.txt"))

Path("config.txt").write_text("dificultad=difícil\nvolumen=3\n", encoding="utf-8")
print(cargar_config("config.txt"))

Path("config.txt").unlink()   # limpiar: la próxima ejecución arranca igual
```

### Misión R02-N03-M3 · Los errores de la tienda

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Creá una excepción base `ErrorDeTienda` y dos hijas: `OroInsuficiente` (que guarde cuánto falta en un atributo `faltan`) y `SinStock`. Escribí `comprar(objeto, oro)`, que **lance** la que corresponda o devuelva el oro que queda.

Con 30 de oro, intentá comprar poción, espada (sin stock), poción y poción. Atrapá `OroInsuficiente` mostrando cuánto falta, y cualquier otro problema de la tienda con `except ErrorDeTienda`.

#### Criterio de aprobación

- Las dos excepciones heredan de `ErrorDeTienda`.
- `comprar` usa `raise` y no imprime nada: avisa con la excepción.
- El bucle atrapa primero `OroInsuficiente` y después `ErrorDeTienda`.

#### Salida esperada

```
Compraste poción. Te quedan 18.
No se pudo: no quedan espada.
Compraste poción. Te quedan 6.
No alcanza: cuesta 12 y tenés 6 (faltan 6).
```

#### Solución de referencia

```python
class ErrorDeTienda(Exception):
    """Algo salió mal en una compra."""


class OroInsuficiente(ErrorDeTienda):
    def __init__(self, precio, oro):
        super().__init__(f"cuesta {precio} y tenés {oro}")
        self.faltan = precio - oro


class SinStock(ErrorDeTienda):
    pass


PRECIOS = {"poción": 12, "espada": 60}
STOCK = {"poción": 3, "espada": 0}


def comprar(objeto, oro):
    if STOCK.get(objeto, 0) == 0:
        raise SinStock(f"no quedan {objeto}")
    if PRECIOS[objeto] > oro:
        raise OroInsuficiente(PRECIOS[objeto], oro)
    STOCK[objeto] -= 1
    return oro - PRECIOS[objeto]


oro = 30
for objeto in ["poción", "espada", "poción", "poción"]:
    try:
        oro = comprar(objeto, oro)
        print(f"Compraste {objeto}. Te quedan {oro}.")
    except OroInsuficiente as error:
        print(f"No alcanza: {error} (faltan {error.faltan}).")
    except ErrorDeTienda as error:
        print(f"No se pudo: {error}.")
```

### Encargo R02-N03-E1 · El cronómetro del Gremio

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

Hacé tu propio **gestor de contexto** (lo que se usa con `with`) con `contextlib.contextmanager`: `cronometro(tarea)` muestra `entrando: …` al empezar y `saliendo: … (X s)` al terminar, con el tiempo que tardó el bloque. Tiene que mostrar el "saliendo" **aunque el bloque falle** (usá `try` / `finally` alrededor del `yield`).

Probalo con una suma larga y con un bloque que divide por cero.

#### Criterio de aprobación

- Usa `@contextmanager` y `yield`.
- Mide el tiempo con `time.perf_counter()`.
- El mensaje de salida aparece aunque el bloque lance un error.

#### Solución de referencia

```python
from contextlib import contextmanager
import time


@contextmanager
def cronometro(tarea):
    print(f"entrando: {tarea}")
    inicio = time.perf_counter()
    try:
        yield
    finally:
        duracion = time.perf_counter() - inicio
        print(f"saliendo: {tarea} ({duracion:.3f} s)")


with cronometro("contar hasta un millón"):
    total = sum(range(1_000_000))
print("total:", total)

try:
    with cronometro("tarea que falla"):
        1 / 0
except ZeroDivisionError:
    print("el error llegó igual, pero el cronómetro cerró")
```

### Prueba del sello

#### ¿Qué pasa con el programa si una excepción no se atrapa?

Se corta en esa línea y muestra el traceback.

#### ¿Cuándo se ejecuta el `else` de un `try`? ¿Y el `finally`?

El `else`, solo si no hubo ninguna excepción. El `finally`, siempre.

#### ¿Por qué no conviene `except:` a secas?

Porque atrapa todo, incluso errores que no esperabas (de tipeo, de lógica), y los esconde.

#### ¿Qué ventaja tiene `with` al abrir un archivo?

Lo cierra solo al terminar el bloque, aunque haya un error en el medio.

#### ¿Qué hace el modo `"w"` si el archivo ya existe?

Lo vacía antes de escribir. Para agregar al final se usa `"a"`.

#### ¿Cómo se crea una excepción propia?

Con una clase que hereda de `Exception` (o de otra excepción): `class MiError(Exception): pass`.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/16-Excepciones`. El encargo no tiene salida esperada fija porque el tiempo cambia en cada ejecución.

## R02-N04 · JSON y CSV: guardar la partida

```meta
tipo: tema
padre: R02-N03
precio: 10
criatura: orco
temas: arch.json, arch.csv
usa: poo.records
```

### Crónica

En **el Archivo**, Sila guarda las crónicas de cada aventurero en dos formatos. Uno, prolijo y anidado, que cualquier mago del reino sabe leer: el **JSON**. El otro, en columnas, como las planillas de Baldo: el **CSV**.

Mia copia las notas del viajero en los dos, para que no se pierdan.

—Si tu partida no se puede guardar, se pierde al apagar la vela —dice Sila—. Aprendé a escribirla en papel.

### Objetivos

- Convertir datos de Python a JSON y de vuelta (`dump`, `load`, `dumps`, `loads`).
- Guardar y reconstruir dataclasses con `asdict` y `Clase(**datos)`.
- Leer y escribir planillas CSV con `csv.reader`, `csv.writer` y `DictReader`.

### Antes de empezar

Diccionarios y listas (R01), dataclasses (R02-N01) y archivos con `with` (R02-N03).

### Explicación

#### Qué es JSON

JSON es un formato de **texto** para guardar datos con estructura. Se parece muchísimo a los diccionarios y listas de Python:

```json
{"heroe": "Mia", "nivel": 3, "inventario": ["poción", "llave"], "maldito": false}
```

Lo entiende cualquier lenguaje, por eso es el idioma de las APIs, las configuraciones y los guardados. JSON solo conoce: objetos (`dict`), listas (`list`), textos (`str`), números (`int`, `float`), `true`/`false` (`bool`) y `null` (`None`).

#### El módulo `json`

| Función | Convierte | Con |
|---|---|---|
| `json.dump(datos, archivo)` | Python → JSON | un archivo abierto |
| `json.load(archivo)` | JSON → Python | un archivo abierto |
| `json.dumps(datos)` | Python → JSON | un **texto** (la `s` es de *string*) |
| `json.loads(texto)` | JSON → Python | un texto |

- `indent=2` lo escribe legible, con sangría.
- `ensure_ascii=False` deja los acentos y la ñ tal cual (si no, escribe `\u00f3`).

#### Guardar objetos

Una dataclass **no** se puede pasar directo a `json.dump`. Hay que convertirla en diccionario con `asdict(objeto)` (también convierte las dataclasses anidadas). Al cargar, `json.load` devuelve diccionarios, y la dataclass se reconstruye con `Heroe(**datos)`: el `**` reparte el diccionario como argumentos por nombre.

#### Versionar lo que se guarda

Los guardados viven más que tu código: si mañana agregás un campo, los archivos viejos no lo tienen. Guardá un `"version"` y, al cargar, **migrá** los viejos.

#### CSV: planillas de texto

Un CSV es una tabla en texto: una fila por línea, columnas separadas por comas. Lo abren Excel y LibreOffice.

```python
import csv

with open("ventas.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    escritor.writerow(["producto", "cantidad"])
    escritor.writerow(["poción", 3])

with open("ventas.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):       # {"producto": "poción", "cantidad": "3"}
        print(fila["producto"], int(fila["cantidad"]))
```

- Abrí siempre con `newline=""`: el módulo `csv` se encarga de los fines de línea.
- `csv.writer` usa `\r\n` (el de Windows) por defecto; con `lineterminator="\n"` escribe el de Linux y Mac.
- **Todo lo que se lee de un CSV es texto**: convertí los números con `int()` o `float()`.
- No partas las líneas a mano con `split(",")`: un nombre como `"Pérez, Ana"` tiene una coma adentro y `csv` lo maneja bien.

### Código de ejemplo

```python
"""JSON y CSV: guardar la partida y leer planillas."""

import csv
import json
from dataclasses import dataclass, asdict, field
from pathlib import Path


@dataclass
class Heroe:
    nombre: str
    vida: int = 100
    nivel: int = 1
    inventario: list = field(default_factory=list)


@dataclass
class Partida:
    heroe: Heroe
    mapa: str = "cripta-01"
    gemas: int = 0


SAVE = Path("partida.json")


def guardar(partida, ruta=SAVE):
    datos = asdict(partida)             # dataclass → dict (también las anidadas)
    with ruta.open("w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def cargar(ruta=SAVE):
    with ruta.open(encoding="utf-8") as f:
        d = json.load(f)                # JSON → dict
    return Partida(heroe=Heroe(**d["heroe"]), mapa=d["mapa"], gemas=d["gemas"])


# =========================================================
# JSON: guardar y cargar
# =========================================================
partida = Partida(Heroe("Mia", vida=80, nivel=3, inventario=["poción", "llave"]), gemas=7)
guardar(partida)
print("--- partida.json ---")
print(SAVE.read_text(encoding="utf-8"))

recuperada = cargar()
print("cargada:", recuperada)
print("¿mismo estado?", partida == recuperada)

# dumps / loads: con textos, sin archivo (lo que viaja por internet)
evento = json.dumps({"tipo": "gema", "total": recuperada.gemas})
print("para la web:", evento)
print("de vuelta:", json.loads(evento))

# =========================================================
# CSV: la planilla del Gremio
# =========================================================
PLANILLA = Path("ventas.csv")
with PLANILLA.open("w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    escritor.writerow(["producto", "cantidad", "precio"])
    escritor.writerows([["poción", 3, 12], ["espada", 1, 60], ["poción", 2, 12]])

total = 0
with PLANILLA.open(newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):     # cada fila es un dict: {"producto": ..., ...}
        subtotal = int(fila["cantidad"]) * int(fila["precio"])
        total += subtotal
        print(f"{fila['producto']:<8}{subtotal:>5}")
print(f"{'TOTAL':<8}{total:>5}")

SAVE.unlink()
PLANILLA.unlink()
```

### Salida esperada

```
--- partida.json ---
{
  "heroe": {
    "nombre": "Mia",
    "vida": 80,
    "nivel": 3,
    "inventario": [
      "poción",
      "llave"
    ]
  },
  "mapa": "cripta-01",
  "gemas": 7
}
cargada: Partida(heroe=Heroe(nombre='Mia', vida=80, nivel=3, inventario=['poción', 'llave']), mapa='cripta-01', gemas=7)
¿mismo estado? True
para la web: {"tipo": "gema", "total": 7}
de vuelta: {'tipo': 'gema', 'total': 7}
poción     36
espada     60
poción     24
TOTAL     120
```

### ¿Para qué sirve?

JSON es el formato con el que hablan casi todas las aplicaciones: cuando una app del celular pide el clima o tu saldo, el servidor responde en JSON. También se usa para configuraciones y guardados de juegos. CSV es la puerta de entrada y salida de las planillas: exportar las ventas del mes, importar una lista de alumnos, cargar datos para analizarlos (lo vas a ver en la Senda de los datos).

### Errores habituales

**Goblin: pasar un objeto que JSON no conoce**:

```
TypeError: Object of type Heroe is not JSON serializable
```

Convertilo antes con `asdict()` o usá el parámetro `default=` de `json.dump`.

**Orco: la clave que no está** al cargar un guardado viejo (`KeyError: 'mapa'`): usá `datos.get("mapa", "cripta-01")` o migrá por versión.

**Slime: JSON mal escrito** (`json.JSONDecodeError`): en JSON las claves y los textos van **entre comillas dobles**, no hay comas al final y es `true`/`false`/`null`, no `True`/`False`/`None`.

**Goblin: sumar lo que viene de un CSV sin convertir**: `"3" + "2"` da `"32"`.

**Ogro: filas vacías de más** al escribir un CSV en Windows: pasa si abrís el archivo sin `newline=""`.

### Misión R02-N04-M1 · Guardados de otra época

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Los guardados viejos (versión 1) no tenían `"version"` ni `"mapa"`. Escribí:

- `cargar(texto)`: lee el JSON con `json.loads` y lo **migra** con una función `migrar(datos)`: si no tiene versión o es menor que 2, agrega `"mapa": "cripta-01"` y `"version": 2`.
- `guardar(datos)`: devuelve el JSON con `"version": 2`.

Probá con un guardado viejo (`{"heroe": "Mia", "gemas": 3}`) y uno nuevo.

#### Criterio de aprobación

- `migrar` agrega lo que falta solo a los guardados viejos.
- Un guardado nuevo no cambia al cargarlo.
- Al guardar, siempre queda la versión actual.

#### Salida esperada

```
{'heroe': 'Mia', 'gemas': 3, 'mapa': 'cripta-01', 'version': 2}
{'heroe': 'Tilo', 'gemas': 5, 'mapa': 'torre-02', 'version': 2}
{"heroe": "Mia", "gemas": 3, "mapa": "cripta-01", "version": 2}
```

#### Solución de referencia

```python
import json

VERSION = 2


def migrar(datos):
    """Los saves viejos (sin "version") no tenían mapa: se agrega el inicial."""
    if datos.get("version", 1) < 2:
        datos["mapa"] = "cripta-01"
        datos["version"] = 2
    return datos


def cargar(texto):
    return migrar(json.loads(texto))


def guardar(datos):
    return json.dumps({**datos, "version": VERSION}, ensure_ascii=False)


viejo = '{"heroe": "Mia", "gemas": 3}'
nuevo = '{"heroe": "Tilo", "gemas": 5, "mapa": "torre-02", "version": 2}'
print(cargar(viejo))
print(cargar(nuevo))
print(guardar(cargar(viejo)))
```

### Misión R02-N04-M2 · Los tres espacios de guardado

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Guardá **tres** partidas (una dataclass `Partida` con `heroe`, `mapa` y `gemas`) en un solo archivo `slots.json`, como una lista. Después cargalas, reconstruí las dataclasses y mostralas numeradas. Comprobá que lo cargado es igual a lo guardado y borrá el archivo al final.

#### Criterio de aprobación

- Guarda una lista de diccionarios con `asdict` y `json.dump`.
- Al cargar reconstruye cada `Partida` con `Partida(**d)`.
- Compara lo cargado con lo original y da `True`.

#### Salida esperada

```
Slot 1: Mia en cripta-01 (7 gemas)
Slot 2: Tilo en torre-02 (12 gemas)
Slot 3: Sila en valle (0 gemas)
¿se recuperó todo? True
```

#### Solución de referencia

```python
import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Partida:
    heroe: str
    mapa: str
    gemas: int


RUTA = Path("slots.json")


def guardar_slots(slots):
    with RUTA.open("w", encoding="utf-8") as f:
        json.dump([asdict(p) for p in slots], f, indent=2, ensure_ascii=False)


def cargar_slots():
    with RUTA.open(encoding="utf-8") as f:
        return [Partida(**d) for d in json.load(f)]


slots = [Partida("Mia", "cripta-01", 7), Partida("Tilo", "torre-02", 12), Partida("Sila", "valle", 0)]
guardar_slots(slots)
for numero, partida in enumerate(cargar_slots(), start=1):
    print(f"Slot {numero}: {partida.heroe} en {partida.mapa} ({partida.gemas} gemas)")
print("¿se recuperó todo?", cargar_slots() == slots)
RUTA.unlink()
```

### Misión R02-N04-M3 · La planilla de los vendedores

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con esta planilla de ventas (escribila en `ventas.csv` desde el programa):

```
fecha,vendedor,producto,monto
2026-09-01,Tilo,espada,60
2026-09-01,Sila,poción,24
2026-09-02,Tilo,escudo,45
2026-09-02,Baldo,poción,12
2026-09-03,Sila,espada,60
```

Calculá el total de cada vendedor con `csv.DictReader` y escribí un `resumen.csv` con `vendedor,total`, ordenado de mayor a menor. Mostrá el resumen y borrá los dos archivos.

#### Criterio de aprobación

- Lee con `csv.DictReader` y convierte los montos a número.
- Acumula en un diccionario por vendedor.
- Escribe el resumen con `csv.writer`, ordenado de mayor a menor.

#### Salida esperada

```
vendedor,total
Tilo,105
Sila,84
Baldo,12
```

#### Solución de referencia

```python
import csv
from pathlib import Path

DATOS = """fecha,vendedor,producto,monto
2026-09-01,Tilo,espada,60
2026-09-01,Sila,poción,24
2026-09-02,Tilo,escudo,45
2026-09-02,Baldo,poción,12
2026-09-03,Sila,espada,60
"""
RUTA = Path("ventas.csv")
RUTA.write_text(DATOS, encoding="utf-8")

por_vendedor = {}
with RUTA.open(newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        por_vendedor[fila["vendedor"]] = por_vendedor.get(fila["vendedor"], 0) + int(fila["monto"])

with Path("resumen.csv").open("w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f, lineterminator="\n")   # fin de línea de Linux/Mac
    escritor.writerow(["vendedor", "total"])
    for vendedor, total in sorted(por_vendedor.items(), key=lambda par: par[1], reverse=True):
        escritor.writerow([vendedor, total])

print(Path("resumen.csv").read_text(encoding="utf-8"), end="")
RUTA.unlink()
Path("resumen.csv").unlink()
```

### Encargo R02-N04-E1 · El traductor universal

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

Escribí una función `a_json(objeto)` para usar como `json.dumps(..., default=a_json)`: si el objeto es una dataclass, lo convierte con `asdict`; si es un `set`, lo devuelve como lista ordenada; si es otra cosa, lanza `TypeError`.

Probala con un héroe que tiene una lista de ítems (dataclasses) y un set de habilidades.

#### Criterio de aprobación

- Usa `is_dataclass` para reconocer dataclasses.
- Los sets salen como listas ordenadas.
- Lo desconocido lanza `TypeError`, como hace `json` normalmente.

#### Salida esperada

```
{"nombre": "Mia", "items": [{"nombre": "espada", "valor": 60}], "habilidades": ["fuego", "sigilo"]}
```

#### Solución de referencia

```python
import json
from dataclasses import dataclass, asdict, is_dataclass, field


def a_json(objeto):
    """Para json.dump(default=...): se llama con lo que JSON no sabe guardar."""
    if is_dataclass(objeto):
        return asdict(objeto)
    if isinstance(objeto, set):
        return sorted(objeto)
    raise TypeError(f"no sé guardar {type(objeto).__name__}")


@dataclass
class Item:
    nombre: str
    valor: int


@dataclass
class Heroe:
    nombre: str
    items: list = field(default_factory=list)
    habilidades: set = field(default_factory=set)


mia = Heroe("Mia", [Item("espada", 60)], {"sigilo", "fuego"})
print(json.dumps(mia, default=a_json, ensure_ascii=False))
```

### Prueba del sello

#### ¿Qué diferencia hay entre `json.dump` y `json.dumps`?

`dump` escribe en un archivo abierto; `dumps` devuelve un texto.

#### ¿Cómo guardás una dataclass en JSON y cómo la recuperás?

Se guarda `asdict(objeto)` y se recupera con `Clase(**datos)`.

#### ¿Qué tipos de Python entiende JSON directamente?

`dict`, `list`, `str`, `int`, `float`, `bool` y `None`.

#### ¿Por qué conviene guardar una versión en los archivos?

Para poder reconocer los guardados viejos y migrarlos cuando cambie la estructura.

#### Al leer un CSV, ¿de qué tipo son los valores?

Siempre texto: los números hay que convertirlos.

### Soluciones (docente)

Reescrito desde cero a partir de `17-Python/18-JSON-CSV` (el original solo tenía JSON; se sumó CSV, que la auditoría marcaba como faltante).

## R02-N05 · Jefe: el Archivista Corrupto

```meta
tipo: jefe
padre: R02-N04
precio: 10
criatura: dragon
insignia: Sello del Archivista
insignia_descripcion: Venciste al Archivista Corrupto: tus datos sobreviven a cualquier maldición.
usa: poo.clases, err.excepciones, arch.json
```

### Crónica

Las copias empiezan a cambiar solas. En **la Bóveda**, el **Archivista Corrupto** mezcla los registros: borra campos, rompe los pergaminos a la mitad, cambia números por palabras. Quiere borrar las notas del viajero, porque la corrupción se come la claridad.

—Para vencerlo no alcanza con guardar —dice {mentor}—. Hay que **validar** lo que entra, **modelar** bien lo que se guarda y **sobrevivir** a lo que viene roto.

### Objetivos

- Combinar clases, excepciones propias y JSON en un mismo programa.
- Validar datos al crear objetos y al cargarlos.
- Encadenar excepciones con `raise ... from`.

### Antes de empezar

Toda la rama Objetos y errores. Proyecto integrador: no hay teoría nueva salvo dos detalles.

### Explicación

#### `__post_init__`: validar una dataclass

Una dataclass escribe su `__init__`, pero podés agregar un `__post_init__` que se ejecuta justo después: es el lugar para revisar los datos y lanzar una excepción si no tienen sentido.

```python
@dataclass
class Heroe:
    nombre: str
    nivel: int = 1

    def __post_init__(self):
        if not 1 <= self.nivel <= 50:
            raise ErrorDeCompania(f"nivel {self.nivel} fuera de rango")
```

#### `@classmethod`: otra forma de crear objetos

Un método con `@classmethod` recibe la **clase** (`cls`) en lugar del objeto. Se usa para "constructores alternativos": `Compania.desde_json(texto)` arma una compañía a partir de un JSON.

#### `raise ... from`: traducir un error

Cuando atrapás un error de bajo nivel (`json.JSONDecodeError`) y querés avisar con uno **tuyo** (`PergaminoCorrupto`), usá `raise PergaminoCorrupto("…") from error`: el traceback muestra los dos, y quien llama solo necesita conocer tu excepción.

### ¿Para qué sirve?

Toda aplicación que recibe datos de afuera (un formulario, un archivo subido, la respuesta de otra API) hace esto: valida, rechaza lo que está roto con un mensaje claro y guarda solo lo que está bien. Es lo que separa un programa que "funciona en mi compu" de uno que aguanta usuarios reales.

### Errores habituales

El Archivista combina a todas las criaturas de la rama:

- **Goblin**: un campo con el tipo equivocado (`"vida": "mucha"`). Revisá con `isinstance`.
- **Orco**: el campo que falta (`KeyError`). Revisá antes de usarlo.
- **Slime**: el JSON cortado a la mitad (`json.JSONDecodeError`).
- **Ogro**: atrapar el error y seguir como si nada, sin avisar qué se perdió.

### Misión R02-N05-M1 · El registro de la compañía

```meta
entrega: codigo
monedas: 6
xp: 30
```

#### Consigna

Modelá una compañía de aventureros:

- `ErrorDeCompania(Exception)`.
- `@dataclass Heroe` con `nombre`, `clase` y `nivel` (1 por defecto). En `__post_init__`, lanzá `ErrorDeCompania` si el nombre está vacío o el nivel no está entre 1 y 50.
- `Compania` con `nombre` y una lista de héroes. `sumar(heroe)` lanza `ErrorDeCompania` si ya hay 4 integrantes o si el nombre está repetido. `nivel_promedio()`.
- `a_json()` devuelve la compañía como texto JSON y `@classmethod desde_json(texto)` la reconstruye.

Procesá esta lista de pedidos mostrando `+ nombre` o `x motivo` en cada uno:

```python
pedidos = [("Mia", "maga", 6), ("Tilo", "guerrero", 8), ("", "maga", 3),
           ("Sila", "maga", 5), ("Tilo", "guerrero", 8), ("Baldo", "pícaro", 70),
           ("Baldo", "pícaro", 4), ("Ana", "arquera", 2)]
```

Al final guardá la compañía en JSON, reconstruila y mostrá sus integrantes y el nivel promedio.

#### Criterio de aprobación

- Las validaciones lanzan `ErrorDeCompania`; el bucle las atrapa y sigue.
- `Heroe` valida en `__post_init__`.
- `desde_json` es un `@classmethod` y reconstruye la compañía con sus héroes.
- Resultado: Mia, Tilo, Sila y Baldo, con nivel promedio 5.8.

#### Salida esperada

```
+ Mia
+ Tilo
x el héroe necesita un nombre
+ Sila
x Tilo ya está en la compañía
x nivel 70 fuera de rango (1-50)
+ Baldo
x la compañía ya tiene 4 integrantes
Los del Valle: ['Mia', 'Tilo', 'Sila', 'Baldo'], nivel promedio 5.8
```

#### Solución de referencia

```python
import json
from dataclasses import dataclass, asdict


class ErrorDeCompania(Exception):
    """Algo no se puede hacer con la compañía."""


@dataclass
class Heroe:
    nombre: str
    clase: str
    nivel: int = 1

    def __post_init__(self):
        if not self.nombre.strip():
            raise ErrorDeCompania("el héroe necesita un nombre")
        if not 1 <= self.nivel <= 50:
            raise ErrorDeCompania(f"nivel {self.nivel} fuera de rango (1-50)")


class Compania:
    MAXIMO = 4

    def __init__(self, nombre):
        self.nombre = nombre
        self.heroes = []

    def sumar(self, heroe):
        if len(self.heroes) >= self.MAXIMO:
            raise ErrorDeCompania(f"la compañía ya tiene {self.MAXIMO} integrantes")
        if any(h.nombre == heroe.nombre for h in self.heroes):
            raise ErrorDeCompania(f"{heroe.nombre} ya está en la compañía")
        self.heroes.append(heroe)

    def nivel_promedio(self):
        return sum(h.nivel for h in self.heroes) / len(self.heroes)

    def a_json(self):
        return json.dumps({"nombre": self.nombre, "heroes": [asdict(h) for h in self.heroes]}, ensure_ascii=False)

    @classmethod
    def desde_json(cls, texto):
        datos = json.loads(texto)
        compania = cls(datos["nombre"])
        for d in datos["heroes"]:
            compania.sumar(Heroe(**d))
        return compania


compania = Compania("Los del Valle")
pedidos = [("Mia", "maga", 6), ("Tilo", "guerrero", 8), ("", "maga", 3),
           ("Sila", "maga", 5), ("Tilo", "guerrero", 8), ("Baldo", "pícaro", 70),
           ("Baldo", "pícaro", 4), ("Ana", "arquera", 2)]
for nombre, clase, nivel in pedidos:
    try:
        compania.sumar(Heroe(nombre, clase, nivel))
        print(f"+ {nombre or '(sin nombre)'}")
    except ErrorDeCompania as error:
        print(f"x {error}")

guardada = compania.a_json()
copia = Compania.desde_json(guardada)
print(f"{copia.nombre}: {[h.nombre for h in copia.heroes]}, nivel promedio {copia.nivel_promedio():.1f}")
```

### Misión R02-N05-M2 · Los pergaminos corruptos

```meta
entrega: codigo
monedas: 6
xp: 30
```

#### Consigna

Escribí `leer_pergamino(texto)`, que convierta un guardado JSON en diccionario o lance `PergaminoCorrupto` explicando el motivo:

- si no es JSON válido (traducí el `json.JSONDecodeError` con `raise ... from`);
- si no es un objeto (por ejemplo, una lista);
- si falta alguno de los campos `heroe` (texto), `vida` y `gemas` (números enteros), o si tiene otro tipo.

Procesá esta lista y mostrá qué pergaminos se salvaron y cuántas gemas se recuperaron:

```python
pergaminos = [
    '{"heroe": "Mia", "vida": 80, "gemas": 7}',
    '{"heroe": "Tilo", "vida": 95',
    '{"heroe": "Sila", "gemas": 3}',
    '{"heroe": "Baldo", "vida": "mucha", "gemas": 1}',
    '["no", "es", "un", "save"]',
    '{"heroe": "Ana", "vida": 60, "gemas": 12}',
]
```

#### Criterio de aprobación

- Usa una excepción propia y `raise ... from` para el JSON inválido.
- Revisa que existan los campos y su tipo con `isinstance`.
- Se salvan 2 de 6 pergaminos, con 19 gemas.

#### Salida esperada

```
pergamino 1: ok
pergamino 2: corrupto, no es JSON válido (Expecting ',' delimiter)
pergamino 3: corrupto, falta el campo 'vida'
pergamino 4: corrupto, 'vida' tendría que ser int
pergamino 5: corrupto, no es un objeto JSON
pergamino 6: ok
Se salvaron 2 de 6. Gemas recuperadas: 19
```

#### Solución de referencia

```python
import json


class PergaminoCorrupto(Exception):
    """El archivo de guardado no se puede usar."""


CAMPOS = {"heroe": str, "vida": int, "gemas": int}


def leer_pergamino(texto):
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as error:
        raise PergaminoCorrupto(f"no es JSON válido ({error.msg})") from error
    if not isinstance(datos, dict):
        raise PergaminoCorrupto("no es un objeto JSON")
    for campo, tipo in CAMPOS.items():
        if campo not in datos:
            raise PergaminoCorrupto(f"falta el campo '{campo}'")
        if not isinstance(datos[campo], tipo):
            raise PergaminoCorrupto(f"'{campo}' tendría que ser {tipo.__name__}")
    return datos


pergaminos = [
    '{"heroe": "Mia", "vida": 80, "gemas": 7}',
    '{"heroe": "Tilo", "vida": 95',
    '{"heroe": "Sila", "gemas": 3}',
    '{"heroe": "Baldo", "vida": "mucha", "gemas": 1}',
    '["no", "es", "un", "save"]',
    '{"heroe": "Ana", "vida": 60, "gemas": 12}',
]

sanos = []
for numero, texto in enumerate(pergaminos, start=1):
    try:
        sanos.append(leer_pergamino(texto))
        print(f"pergamino {numero}: ok")
    except PergaminoCorrupto as error:
        print(f"pergamino {numero}: corrupto, {error}")

print(f"Se salvaron {len(sanos)} de {len(pergaminos)}. Gemas recuperadas: {sum(d['gemas'] for d in sanos)}")
```

### Encargo R02-N05-E1 · La planilla de inscriptos

```meta
entrega: codigo
monedas: 2
xp: 20
```

#### Consigna

La escuela del pueblo quiere la lista de inscriptos en una planilla. Con una lista de diccionarios (`nombre`, `curso`, `nota`), escribí `inscriptos.csv` con `csv.DictWriter` (encabezado incluido) y mostralo.

#### Criterio de aprobación

- Usa `csv.DictWriter` con `fieldnames` y `writeheader()`.
- El archivo tiene una fila por inscripto.

#### Salida esperada

```
nombre,curso,nota
Mia,Python,9
Tilo,Python,6
Sila,Python,10
```

#### Solución de referencia

```python
import csv
from pathlib import Path

inscriptos = [
    {"nombre": "Mia", "curso": "Python", "nota": 9},
    {"nombre": "Tilo", "curso": "Python", "nota": 6},
    {"nombre": "Sila", "curso": "Python", "nota": 10},
]

ruta = Path("inscriptos.csv")
with ruta.open("w", newline="", encoding="utf-8") as f:
    escritor = csv.DictWriter(f, fieldnames=["nombre", "curso", "nota"], lineterminator="\n")
    escritor.writeheader()
    escritor.writerows(inscriptos)

print(ruta.read_text(encoding="utf-8"), end="")
ruta.unlink()
```

### Prueba del sello

#### ¿Para qué sirve `__post_init__` en una dataclass?

Para ejecutar código justo después del `__init__` automático, por ejemplo validar los campos.

#### ¿Qué recibe un método con `@classmethod`?

La clase (`cls`) en lugar del objeto: sirve para crear objetos de otra forma, como `desde_json`.

#### ¿Qué ventaja tiene `raise MiError(...) from error`?

Quien llama maneja un solo tipo de error (el tuyo) y el traceback conserva la causa original.

#### ¿Por qué conviene validar al crear el objeto y no después?

Porque así nunca existe un objeto inválido: el error aparece en el lugar exacto donde entró el dato malo.

### Soluciones (docente)

Proyecto integrador nuevo. El mensaje de `JSONDecodeError` ("Expecting ',' delimiter") es el de CPython; Pyodide usa el mismo intérprete, así que la salida coincide.
