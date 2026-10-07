# RAMA R01 · Fundamentos: el despertar en el Valle

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Tipos de datos y conversiones

```meta
tipo: tema
padre: R00-N01
precio: 10
criatura: goblin
temas: prog.variables
```

### Crónica

En el mercado del Valle, un mercader te vende tres cosas y te anota los precios en un papel: "12", "3.5", "7". Los sumás y le decís "123.57". El mercader se ríe:

—Sumaste **letras**, no números.

{mentor} interviene: —En este mundo, cada valor tiene un **tipo**, {heroe}. Aprendé a reconocerlos y a convertirlos, o los goblins te van a robar hasta la última escama.

### Objetivos

Reconocer los tipos básicos de Python, saber de qué tipo es un valor, convertir
entre tipos y mostrar números con formato.

### Antes de empezar

- Variables, `print`, f-strings e `input` (01).

### Explicación

#### Los cinco tipos básicos
| Tipo | Qué guarda | Ejemplos |
|---|---|---|
| `int` | números enteros | `100`, `-3`, `1_250_000` |
| `float` | números con decimales | `3.5`, `-0.25`, `1.5e3` (= 1500.0) |
| `str` | texto | `"Kira"`, `'hola'`, `""` (texto vacío) |
| `bool` | verdadero o falso | `True`, `False` (con mayúscula) |
| `NoneType` | "no hay valor" | `None` |

- `type(valor)` dice el tipo: `type(3.5)` → `<class 'float'>`.
- `isinstance(valor, tipo)` pregunta si es de ese tipo: `isinstance(3, int)` → `True`.

#### Tipado dinámico
En Python **la variable no tiene tipo; el valor sí**. La misma variable puede
apuntar a un `int` y después a un `str`. Eso da flexibilidad, pero también
significa que Python **no te avisa de antemano** si mezclás tipos: el error
aparece recién cuando se ejecuta esa línea.

#### `int`: enteros sin límite
Un `int` puede ser tan grande como quieras (`2 ** 100` funciona). Los `_` dentro
de un número son solo para leerlo mejor: `1_000_000`.

#### `float`: decimales con una trampa
Se escriben con **punto**, nunca con coma. La computadora guarda los decimales
en binario, así que algunos no son exactos:
`0.1 + 0.2` da `0.30000000000000004`. Para mostrar, redondeá con
`round(x, 2)` o con formato (`f"{x:.2f}"`). Para dinero exacto existe el módulo
`decimal` (se ve en 11).

#### `None`
Representa "todavía no hay valor" (un objetivo que no se eligió, un resultado
que no existe). Para preguntar si algo es `None` se usa `is None` (lo vas a
entender en 03 y 08).

#### Conversiones
| Función | Convierte a | Ejemplo | Resultado |
|---|---|---|---|
| `int(x)` | entero | `int("7")`, `int(3.99)` | `7`, `3` (**corta**, no redondea) |
| `float(x)` | decimal | `float("12.50")` | `12.5` |
| `str(x)` | texto | `str(7)` | `"7"` |
| `bool(x)` | verdadero/falso | `bool("")` | `False` |
| `round(x, n)` | redondea | `round(3.99)`, `round(2.567, 1)` | `4`, `2.6` |

#### Verdadero y falso ("truthy" y "falsy")
Cualquier valor se puede convertir a `bool`. Son **falsos**: `0`, `0.0`, `""`,
`None` y las colecciones vacías (se ven en 06–07). **Todo lo demás es
verdadero**. Esto se vuelve muy útil en los `if` (05).

#### Formato de números en f-strings
`f"{valor:formato}"`:
| Formato | Significa | `f"{1234.5:...}"` |
|---|---|---|
| `.2f` | 2 decimales | `1234.50` |
| `,.2f` | separador de miles + 2 decimales | `1,234.50` |
| `.0%` | porcentaje (multiplica por 100) | con `0.75` → `75%` |
| `5` | ancho mínimo 5 | `[    7]` |
| `05` | ancho 5 rellenado con ceros | `[00007]` |

### Código de ejemplo

```python
"""02 - Tipos de datos y conversiones.

Cada VALOR tiene un tipo: numero entero, numero con decimales, texto,
verdadero/falso o "nada". La variable no tiene tipo: solo apunta a un valor.
"""

# =========================================================
# Los cinco tipos basicos
# =========================================================
vida = 100              # int   -> numero entero
velocidad = 3.5         # float -> numero con decimales (punto, no coma)
nombre = "Kira"         # str   -> texto (string)
viva = True             # bool  -> True o False (con mayuscula)
objetivo = None         # None  -> "no hay valor todavia"

# type() dice de que tipo es un valor
print(type(vida), type(velocidad), type(nombre), type(viva), type(objetivo))

# isinstance() pregunta "¿es de este tipo?" y responde True o False
print("¿vida es int?", isinstance(vida, int))
print("¿nombre es int?", isinstance(nombre, int))

# =========================================================
# int: enteros sin limite de tamaño
# =========================================================
oro_del_reino = 2 ** 100          # ** es "elevado a"
print("oro del reino:", oro_del_reino)
poblacion = 1_250_000             # los _ solo ayudan a leer; Python los ignora
print("poblacion:", poblacion)

# =========================================================
# float: decimales (con una trampa)
# =========================================================
print("0.1 + 0.2 =", 0.1 + 0.2)            # 0.30000000000000004 !
print("redondeado:", round(0.1 + 0.2, 2))  # round(valor, decimales)
distancia = 1.5e3                          # notacion cientifica: 1.5 x 10^3
print("distancia:", distancia)

# =========================================================
# Tipado dinamico: el nombre puede apuntar a otro tipo
# =========================================================
recompensa = 50
print("recompensa:", recompensa, type(recompensa))
recompensa = "una espada"
print("recompensa:", recompensa, type(recompensa))

# =========================================================
# Conversiones explicitas
# =========================================================
texto_nivel = "7"                   # lo que devolveria input()
nivel = int(texto_nivel)            # str -> int
print("nivel + 1 =", nivel + 1)

precio = float("12.50")             # str -> float
print("precio x 2 =", precio * 2)

print("int(3.99) =", int(3.99))     # int() CORTA los decimales, no redondea
print("round(3.99) =", round(3.99)) # round() si redondea

mensaje = "Nivel " + str(nivel)     # int -> str para poder unir textos
print(mensaje)

# =========================================================
# bool(): que se considera "verdadero" y que "falso"
# =========================================================
# Son FALSOS: 0, 0.0, "" (texto vacio), None, y las colecciones vacias.
# Todo lo demas es VERDADERO.
print("bool(0) =", bool(0), "| bool(15) =", bool(15))
print('bool("") =', bool(""), '| bool("Kira") =', bool("Kira"))
print("bool(None) =", bool(None))

# =========================================================
# Formato de numeros en f-strings:  {valor:formato}
# =========================================================
oro = 1234567.891
print(f"oro: {oro:.2f}")          # 2 decimales
print(f"oro: {oro:,.2f}")         # separador de miles
porcentaje_vida = 0.75
print(f"vida: {porcentaje_vida:.0%}")   # como porcentaje (multiplica por 100)
print(f"[{nivel:5}]")             # ancho 5 (los numeros se alinean a la derecha)
print(f"[{nivel:05}]")            # ancho 5, rellenado con ceros
```

### Salida esperada

```
<class 'int'> <class 'float'> <class 'str'> <class 'bool'> <class 'NoneType'>
¿vida es int? True
¿nombre es int? False
oro del reino: 1267650600228229401496703205376
poblacion: 1250000
0.1 + 0.2 = 0.30000000000000004
redondeado: 0.3
distancia: 1500.0
recompensa: 50 <class 'int'>
recompensa: una espada <class 'str'>
nivel + 1 = 8
precio x 2 = 25.0
int(3.99) = 3
round(3.99) = 4
Nivel 7
bool(0) = False | bool(15) = True
bool("") = False | bool("Kira") = True
bool(None) = False
oro: 1234567.89
oro: 1,234,567.89
vida: 75%
[    7]
[00007]
```

### ¿Para qué sirve?

Todo formulario de internet recibe **texto**: el precio, la edad, la cantidad. Antes de hacer cuentas hay que convertirlo, y antes de mostrar un resultado hay que darle formato: el total de una compra con dos decimales, el porcentaje de batería de un celular, la temperatura de una estación meteorológica. Confundir tipos es uno de los errores más caros de la programación real: sistemas de cobro que "suman" `"100" + "50"` y cobran 10050.

### Errores habituales

**Goblin: sumar texto y número** (`TypeError`):
```python
print("Nivel " + 7)
```
```
TypeError: can only concatenate str (not "int") to str
```
Solución: `"Nivel " + str(7)` o, mejor, `f"Nivel {7}"`.

**Goblin: convertir algo que no es un entero** (`ValueError`):
```
>>> int("7.5")
ValueError: invalid literal for int() with base 10: '7.5'
>>> int("")
ValueError: invalid literal for int() with base 10: ''
```
`int()` solo acepta texto con un entero. Para `"7.5"` usá `float()`. El texto
vacío aparece cuando el usuario aprieta Enter sin escribir nada.

**Ogro: el programa corre, pero calcula mal:**
- Sumar lo que devuelve `input()` sin convertirlo: `"12" + "3"` da `"123"`.
- Esperar que `int(3.99)` dé `4`: da `3`. Para redondear, `round()`.
- Comparar floats con `==`: `0.1 + 0.2 == 0.3` es `False`. Compará con
  `round(...)` o con `math.isclose` (11).
- Escribir decimales con coma: `precio = 12,5` no da error, pero crea **otra
  cosa** (una tupla, se ve en 06). Siempre punto: `12.5`.

### Micro-misión R01-N01-P1 · El papel del mercader

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Los 5 tipos | int 12 · float 3.5 · str "7" · bool True · None · type(valor)
recompensa: xp 10
```

#### Escena
El Mercado de la Aldea es un enredo de toldos verdes, faroles y serpientes de piedra que hacen de columnas. Detrás de un puesto lleno de cajitas brillantes, un hombrecito de orejas puntiagudas y antiparras en la frente se frota las manos.
—¡Una cara nueva! **Baldo**, para servirte. Para el camino vas a necesitar una bolsa, una cantimplora y una capa. Te anoto los precios.
Te da un papelito: `"12"`, `"3.5"`, `"7"`.

Gheco entrecierra los ojos.
—Antes de sumar nada… ¿de qué **tipo** es cada cosa?

#### Gheco sugiere
Cada valor tiene un **tipo**:
- `int`: enteros;
- `float`: con decimales;
- `str`: texto, entre comillas;
- `bool`: `True` o `False`;
- `None`: nada.

`type(valor)` te dice cuál es.

#### Desafío
Mostrá el tipo de cada uno de estos cinco valores, uno por línea.

#### Código inicial
```python
print(type(12))
print(type(3.5))
print(type(___))
print(type(True))
print(type(___))
```

#### Salida esperada
```
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

#### Solución
`type("7")` y `type(None)`.

#### Al superarla
Ves que los números del papel tienen **comillas**: no son números, son texto. Baldo se rasca la oreja, incómodo.

#### Imagen
- El Mercado de la Aldea de noche: toldos verdes, faroles, columnas con forma de serpiente.
- Baldo detrás de su puesto, con una caja de gemas.
- Mia sostiene un papelito con tres números entre comillas, que brillan en rojo.
- Gheco, con una lupa holográfica sobre el papel.

### Micro-misión R01-N01-P2 · Sumar números, no letras

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo, un goblin
criatura: goblin
carta: Conversiones | int("12") → 12 · float("3.5") → 3.5 · str(7) → "7"
recompensa: xp 15, oro 15
item: Bolsa de cuero
se abre: el oro del jugador (la bolsa de cuero en el inventario)
```

#### Escena
Sumás los tres precios como vienen y el pergamino dice `123.57`. Baldo abre grande los ojos, demasiado contento.
—¡Ciento veintitrés con cincuenta y siete! Justo, justo.
Y debajo del puesto, algo se ríe: un **goblin** verde y flaco, con los bolsillos llenos de escamas ajenas.
—¡Te estaban cobrando de más! —grita Gheco—. Los goblins nacen de **mezclar tipos**: sumaste **letras**, no números.

#### Gheco sugiere
Para usar un texto como número, **convertilo**: `int("12")` da `12` y `float("3.5")` da `3.5`. Con `+`, dos textos se **pegan** (`"12" + "7"` da `"127"`), y dos números se **suman**.

#### Desafío
Convertí los precios antes de sumar.

#### Código inicial
```python
a = "12"
b = "3.5"
c = "7"
print(a + b + c)          # lo que te quería cobrar
total = ___
print(f"Total: {total}")
```

#### Salida esperada
```
123.57
Total: 22.5
```

#### Solución
```python
total = int(a) + float(b) + int(c)
```

#### Al superarla
El goblin suelta las escamas y sale corriendo entre los toldos. Baldo, colorado, te cobra lo justo y te regala una **bolsa de cuero** «por las molestias».
—Para que guardes tu oro, que en este mercado no falta quien se lo quiera llevar.

**Se abre:** el **oro** del jugador (la bolsa de cuero en el inventario).

#### Imagen
- Un goblin flaco y verde huye entre los toldos, con escamas que se le caen de los bolsillos.
- En el pergamino de Mia, `int("12") + float("3.5")` brilla en verde.
- Baldo, avergonzado, le entrega una bolsa de cuero.
- Gheco, triunfante, con los brazos en alto.

### Micro-misión R01-N01-P3 · El vuelto que no da justo

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Decimales | 0.1 + 0.2 → 0.30000000000000004 · round(x, 2)
recompensa: xp 10, oro 10
```

#### Escena
Baldo te da el vuelto en dos monedas: una de 0.1 y otra de 0.2. Le pedís al pergamino que confirme que son 0.3, y el pergamino, muy serio, dice que **no**.
—¿Me estás estafando otra vez? —le preguntás.
—¡Esta vez no, lo juro por mis orejas!

#### Gheco sugiere
Los `float` no son exactos: `0.1 + 0.2` da `0.30000000000000004`. No es un error de Python: así se guardan los decimales en la máquina. Para comparar o mostrar, **redondeá**: `round(x, 2)`.

#### Desafío
Mostrá el vuelto tal cual y después compará el vuelto **redondeado** con 0.3.

#### Código inicial
```python
vuelto = 0.1 + 0.2
print(vuelto)
print(___ == 0.3)
```

#### Salida esperada
```
0.30000000000000004
True
```

#### Solución
```python
print(round(vuelto, 2) == 0.3)
```

#### Al superarla
Baldo respira aliviado.
—Ves que soy honesto… a veces. —Y te agrega 10 de oro de propina, por la paciencia.

#### Imagen
- Primer plano de dos monedas brillantes sobre el mostrador de Baldo.
- Sobre ellas flota el número `0.30000000000000004`, partido en dos por una grieta de luz.
- Mia lo mira con el ceño fruncido; Baldo, con las manos en alto, inocente.

### Micro-misión R01-N01-P4 · ¿Hay algo en la bolsa?

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Verdadero y falso | bool("") → False · bool("0") → True · 0, None y "" son falsos
recompensa: xp 10, oro 10
```

#### Escena
Baldo vacía sobre el mostrador cuatro bolsitas que le dejaron otros viajeros: una con una nota en blanco, otra con un papel que dice «0», una con cero monedas y otra que nadie sabe qué tiene.
—¿Cuáles tienen **algo**? —te pregunta—. Las vacías las tiro.

#### Gheco sugiere
`bool(valor)` dice si Python lo considera verdadero o falso. Son **falsos**: `0`, `0.0`, el texto vacío `""` y `None` (y las colecciones vacías, que vas a ver más adelante). **Todo lo demás es verdadero**, ¡aunque sea el texto `"0"`!

#### Desafío
Mostrá en una línea qué bolsas tienen algo.

#### Código inicial
```python
print(bool(""), bool("0"), bool(___), bool(None))
```

#### Salida esperada
```
False True False False
```

#### Solución
```python
bool(0)
```

#### Al superarla
Baldo está por tirar la del papel «0», y lo frenás: **tiene algo**. Adentro, doblado, hay un dibujito: **un vitral pequeño, en tinta**. Baldo se encoge de hombros.
—Lo dejó un viajero hace muchísimo. Nunca volvió a buscarlo.
Lo guardás en el pergamino.

#### Imagen
- Cuatro bolsitas de tela sobre el mostrador, cada una con una etiqueta de luz: `False`, `True`, `False`, `False`.
- Mia sostiene la bolsa marcada `True` y saca un papel con un vitral dibujado en tinta.
- Gheco, intrigado, se asoma por encima.

### Micro-misión R01-N01-P5 · El cartel del puesto

```meta
lugar: El Mercado de la Aldea del Script
personajes: Mia, Gheco, Baldo
carta: Formato de números | f"{x:,.2f}" → 15,230.50 · f"{n:03}" → 007 · f"{p:.0%}" → 15%
recompensa: xp 15, oro 15
```

#### Escena
—Ya que sabés tanto —dice Baldo—, haceme un cartel nuevo. Que se lea lo que hay en la caja, el número de mi puesto y el descuento de hoy. **Prolijo**, que los clientes desconfían de los números feos.

#### Gheco sugiere
En un f-string, después de `:` va el **formato**:
- `{x:,.2f}`: separador de miles y 2 decimales;
- `{n:03}`: rellena con ceros hasta 3 cifras;
- `{p:.0%}`: lo muestra como porcentaje.

#### Desafío


#### Código inicial
```python
caja = 15230.5
puesto = 7
descuento = 0.15
print(f"Escamas en la caja: {caja:___}")
print(f"Puesto N.º {puesto:___}")
print(f"Descuento: {descuento:___}")
```

#### Salida esperada
```
Escamas en la caja: 15,230.50
Puesto N.º 007
Descuento: 15%
```

#### Solución
`,.2f`, `03` y `.0%`.

#### Al superarla
El cartel nuevo se ilumina sobre el puesto y se forma una fila de clientes. Baldo, feliz, te señala el camino.
—Para salir de la Aldea hay que cruzar **el Puente del Juicio**. El guardián no deja pasar a cualquiera: hay que saber **calcular**. Suerte, maguita.

#### Imagen
- El puesto de Baldo con un cartel holográfico nuevo, prolijo, en verde y dorado.
- Una fila de aldeanos curiosos.
- Al fondo, entre la niebla, se ve un puente de piedra con una gran serpiente tallada: el Puente del Juicio.
- Mia, de espaldas, mirando hacia el puente, con su bolsa de cuero al cinturón.

### Misión R01-N01-M1 · El tasador

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

El mercader te pasa tres precios como texto: `"12"`, `"3.5"` y
`"7"`. Mostrá qué pasa si los "sumás" sin convertir y después el total real,
con 2 decimales.

#### Criterio de aprobación

- Muestra qué pasa al unir los tres textos sin convertir.
- Convierte con `int()`/`float()` antes de sumar.
- Muestra el total real con 2 decimales (22.50).

#### Salida esperada

```
Sin convertir: 123.57
Total real: 22.5
Total con formato: 22.50 monedas
```

#### Solución de referencia

```python
"""Mision 1 - El tasador.

El mercader anota los precios como TEXTO. Hay que convertirlos a numero
antes de sumarlos: si no, "12" + "3.5" pegaria los textos ("123.5").
"""

espada = "12"
escudo = "3.5"
pocion = "7"

total = int(espada) + float(escudo) + int(pocion)
print("Sin convertir:", espada + escudo + pocion)   # une textos: '123.57'
print("Total real:", total)
print(f"Total con formato: {total:.2f} monedas")
```

### Misión R01-N01-M2 · La ficha con formato

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con `oro = 15230.5`, `vida = 63` y `vida_max = 90`,
mostrá el oro con separador de miles y 2 decimales, la vida como `63/90 (70%)`
y el nivel 3 como `003`.

#### Criterio de aprobación

- El oro se ve con separador de miles y 2 decimales (15,230.50).
- La vida se ve como `63/90 (70%)`, calculando el porcentaje.
- El nivel 3 se ve como `003`.

#### Salida esperada

```
Heroína: Kira
Oro:     15,230.50
Vida:    63/90 (70%)
Nivel:   003
```

#### Solución de referencia

```python
"""Mision 2 - La ficha con formato."""

nombre = "Kira"
oro = 15230.5
vida = 63
vida_max = 90

print(f"Heroína: {nombre}")
print(f"Oro:     {oro:,.2f}")
print(f"Vida:    {vida}/{vida_max} ({vida / vida_max:.0%})")
print(f"Nivel:   {3:03}")
```

### Misión R01-N01-M3 · ¿Qué tipo es?

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Antes de ejecutar, anotá qué tipo y qué valor da cada
expresión: `10 / 2`, `"7" + "2"`, `True + True`, `int("08")`, `3 * 1.0`. Después
verificalo con `type()`.

#### Criterio de aprobación

- Muestra con `type()` el tipo y el valor de cada una de las cinco expresiones.
- Deja anotada (en comentarios) la predicción de cada línea antes de ejecutar.

#### Salida esperada

```
<class 'float'> 5.0
<class 'str'> 72
<class 'int'> 2
<class 'int'> 8
<class 'float'> 3.0
<class 'NoneType'> None
```

#### Solución de referencia

```python
"""Mision 3 - ¿Que tipo es? Primero predecilo, despues correlo."""

print(type(10 / 2), 10 / 2)            # float: la division / SIEMPRE da float
print(type("7" + "2"), "7" + "2")      # str: une textos -> '72'
print(type(True + True), True + True)  # int: True vale 1 -> 2
print(type(int("08")), int("08"))      # int: los ceros a la izquierda se ignoran -> 8
print(type(3 * 1.0), 3 * 1.0)          # float: int mezclado con float da float
print(type(None), None)                # NoneType
```

### Encargo R01-N01-E1 · El termómetro del herrero

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El herrero mide la forja en Celsius, pero su manual está en Fahrenheit. Hacé un
programa que pida los grados Celsius (`input`) y muestre el equivalente con un
decimal: `F = C * 9 / 5 + 32`.

#### Criterio de aprobación

- Lee los grados con `input()` y los convierte con `float()`.
- Aplica `F = C * 9 / 5 + 32`.
- Muestra el resultado con un decimal.

#### Entrada de ejemplo

```
1250
```

#### Salida esperada

```
Temperatura en °C: 1250.0 °C son 2282.0 °F
```

#### Solución de referencia

```python
"""Encargo del Gremio - El termometro del herrero.

La forja necesita pasar grados Celsius a Fahrenheit:  F = C * 9 / 5 + 32
"""

celsius = float(input("Temperatura en °C: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius:.1f} °C son {fahrenheit:.1f} °F")
```

#### Pruebas

##### Cero
```entrada
0
```
```salida
Temperatura en °C: 0.0 °C son 32.0 °F
```

##### Bajo cero
```entrada
-40
```
```salida
Temperatura en °C: -40.0 °C son -40.0 °F
```

##### Con decimales
```entrada
36.6
```
```salida
Temperatura en °C: 36.6 °C son 97.9 °F
```

### Prueba del sello

#### ¿Qué tipo tiene el valor que devuelve `input()`? ¿Cómo lo pasás a número?

Siempre `str` (texto). Se pasa a número con `int(...)` o `float(...)`.

#### ¿Qué diferencia hay entre `int(2.7)` y `round(2.7)`?

`int(2.7)` **corta** los decimales y da `2`; `round(2.7)` redondea y da `3`.

#### Nombrá cuatro valores que sean "falsos" al convertirlos con `bool()`.

Por ejemplo `0`, `0.0`, `""` (texto vacío) y `None`. También las colecciones vacías.

#### ¿Por qué `0.1 + 0.2` no da exactamente `0.3`?

Porque la computadora guarda los decimales en binario y algunos, como 0.1, no tienen una representación exacta: queda un error mínimo.

#### ¿Qué muestra `f"{0.456:.1%}"`?

`45.6%`: multiplica por 100 y deja un decimal.

### Soluciones (docente)

Material original: `17-Python/02-Tipos` (soluciones completas en `soluciones/`).

Clave pedagógica: la diferencia entre el tipo del **valor** y la variable. Si alguien pregunta por `Decimal`, se ve en Módulos (R01-N10).

## R01-N02 · Operadores

```meta
tipo: tema
padre: R01-N01
precio: 10
criatura: ogro
temas: prog.operadores
```

### Crónica

La primera prueba de {mentor} es en el Puente del Juicio. El puente solo deja pasar a quien sabe **calcular** su daño, **comparar** su fuerza con la del guardián y **combinar** condiciones sin equivocarse: "nivel 5 o más, con llave o con magia, y sin maldición".

—Un error en el orden de las palabras, {heroe}, y el puente se derrumba.

### Objetivos

Usar todos los operadores de Python: aritméticos, de asignación, de comparación,
lógicos, de pertenencia y de identidad, y saber en qué orden se evalúan.

### Antes de empezar

- Variables y f-strings (01).
- Tipos `int`, `float`, `str`, `bool`, `None` (02).

### Explicación

#### Aritméticos
| Operador | Nombre | `17 ? 5` |
|---|---|---|
| `+` `-` `*` | suma, resta, producto | `22`, `12`, `85` |
| `/` | división | `3.4` (**siempre** da `float`, incluso `10 / 2` → `5.0`) |
| `//` | división entera | `3` (redondea **hacia abajo**: `-7 // 2` → `-4`) |
| `%` | resto (módulo) | `2` |
| `**` | potencia | `2 ** 10` → `1024` |

Usos típicos: `n % 2 == 0` (¿es par?), `seg // 60` y `seg % 60` (minutos y
segundos), `turno % 3 == 0` (cada 3 turnos).

Con textos: `"ab" + "cd"` → `"abcd"` y `"ja" * 3` → `"jajaja"` (se ve en 04).

#### Asignación aumentada
`oro += 25` es lo mismo que `oro = oro + 25`. Existen `+=`, `-=`, `*=`, `/=`,
`//=`, `%=` y `**=`. (Python **no** tiene `++` ni `--`.)

#### Comparación
`==` (igual), `!=` (distinto), `<`, `<=`, `>`, `>=`. Siempre devuelven `True` o `False`.
- **`=` asigna y `==` compara.** Confundirlos es el error más común.
- Se pueden **encadenar**: `30 <= vida < 70` equivale a `30 <= vida and vida < 70`.
- Los textos se comparan en orden alfabético, letra por letra, según el código
  de cada carácter: las **mayúsculas van antes que las minúsculas** (`"Zed" < "ana"`).

#### Lógicos: `and`, `or`, `not`
| Expresión | Es verdadera cuando… |
|---|---|
| `a and b` | las dos son verdaderas |
| `a or b` | al menos una es verdadera |
| `not a` | `a` es falsa |

- **Cortocircuito:** en `a and b`, si `a` es falsa, `b` **ni se evalúa**. En
  `a or b`, si `a` es verdadera, tampoco. Sirve para proteger operaciones
  peligrosas: `oro > 0 and 100 / oro > 10` nunca divide por cero.
- **Devuelven uno de los operandos**, no necesariamente `True`/`False`.
  `apodo or "Anónimo"` da `apodo` si no está vacío y `"Anónimo"` si lo está: es
  la forma corta de poner un **valor por defecto**.

#### Pertenencia: `in` y `not in`
`"r" in "orco"` → `True`. Pregunta si algo está **dentro** de otra cosa. Funciona
con textos y con todas las colecciones (06–07).

#### Identidad: `is` y `is not`
`==` pregunta si dos cosas **valen lo mismo**; `is` pregunta si son **el mismo
objeto**. Por ahora, la regla es simple:
- Para `None` usá **siempre** `is`: `if objetivo is None`.
- Para números, textos y todo lo demás usá **siempre** `==`.

La diferencia de fondo se entiende en 08 (referencias).

#### Precedencia (de mayor a menor)
| Prioridad | Operadores |
|---|---|
| 1 | `( )` |
| 2 | `**` (se agrupa de derecha a izquierda: `2 ** 3 ** 2` = `2 ** 9`) |
| 3 | `-x` (signo) |
| 4 | `*` `/` `//` `%` |
| 5 | `+` `-` |
| 6 | comparaciones: `<` `<=` `>` `>=` `==` `!=` `in` `not in` `is` `is not` |
| 7 | `not` |
| 8 | `and` |
| 9 | `or` |

Trampas: `-2 ** 2` da `-4` (la potencia va antes que el signo), y `and` va antes
que `or`. **Ante la duda, usá paréntesis**: no cuestan nada y hacen el código más
claro.

### Código de ejemplo

```python
"""03 - Operadores.

Los operadores combinan valores: hacen cuentas (+ - * /), comparan (< == !=),
combinan condiciones (and or not) y preguntan pertenencia (in) o identidad (is).
"""

# =========================================================
# Aritmeticos
# =========================================================
ataque = 17
defensa = 5
print("suma       ", ataque + defensa)    # 22
print("resta      ", ataque - defensa)    # 12
print("producto   ", ataque * defensa)    # 85
print("division   ", ataque / defensa)    # 3.4  -> SIEMPRE da float
print("div entera ", ataque // defensa)   # 3    -> descarta los decimales (redondea hacia abajo)
print("resto      ", ataque % defensa)    # 2    -> lo que sobra de la division entera
print("potencia   ", 2 ** 10)             # 1024

# // redondea hacia ABAJO (hacia menos infinito), tambien con negativos
print("-7 // 2 =", -7 // 2)               # -4, no -3

# Usos tipicos de // y %
segundos = 135
print(f"{segundos} s = {segundos // 60} min {segundos % 60} s")
turno = 7
print("¿turno par?", turno % 2 == 0)

# =========================================================
# Asignacion aumentada: modificar una variable usando su propio valor
# =========================================================
oro = 100
oro += 25       # igual que oro = oro + 25
oro -= 10       # oro = oro - 10
oro *= 2        # oro = oro * 2
oro //= 3       # oro = oro // 3
print("oro final:", oro)

# =========================================================
# Comparacion: siempre devuelven True o False
# =========================================================
vida = 35
print("vida == 35 ->", vida == 35)    # igual (dos signos =)
print("vida != 0  ->", vida != 0)     # distinto
print("vida < 30  ->", vida < 30)
print("vida >= 30 ->", vida >= 30)

# Comparaciones encadenadas: se leen como en matematica
print("¿vida entre 30 y 70?", 30 <= vida < 70)

# Los textos se comparan en orden alfabetico (por codigo de cada letra)
print('"ana" < "bron" ->', "ana" < "bron")
print('"Zed" < "ana"  ->', "Zed" < "ana")    # las MAYUSCULAS van antes que las minusculas

# =========================================================
# Logicos: and, or, not
# =========================================================
tiene_llave = True
es_de_noche = False
print("abre la puerta:", tiene_llave and not es_de_noche)
print("hay luz:", es_de_noche or tiene_llave)

# Cortocircuito: Python deja de evaluar en cuanto sabe el resultado.
# Aca, como oro_en_bolsa es 0, la division NUNCA se hace (no hay error).
oro_en_bolsa = 0
print("¿puede repartir?", oro_en_bolsa > 0 and 100 / oro_en_bolsa > 10)

# and / or devuelven UNO DE LOS VALORES, no necesariamente True/False.
# 'or' devuelve el primero que sea verdadero: sirve para dar un valor por defecto.
apodo = ""
print("se presenta como:", apodo or "Viajero anónimo")

# =========================================================
# Pertenencia: in / not in
# =========================================================
print("¿'r' está en 'orco'?", "r" in "orco")
print("¿'dragon' está en 'jefe dragon rojo'?", "dragon" in "jefe dragon rojo")
print("¿'z' NO está en 'slime'?", "z" not in "slime")

# =========================================================
# Identidad: is  (¿es EL MISMO objeto?)  vs  ==  (¿vale lo mismo?)
# =========================================================
objetivo = None
print("objetivo is None:", objetivo is None)   # para None se usa SIEMPRE 'is'
# Para comparar valores (numeros, textos) se usa SIEMPRE '=='.
# La diferencia entre 'is' y '==' se ve a fondo en 08.

# =========================================================
# Precedencia: que se calcula primero
# =========================================================
print("2 + 3 * 4   =", 2 + 3 * 4)        # 14: * antes que +
print("(2 + 3) * 4 =", (2 + 3) * 4)      # 20: los parentesis mandan
print("-2 ** 2     =", -2 ** 2)          # -4: ** antes que el signo menos
print("2 ** 3 ** 2 =", 2 ** 3 ** 2)      # 512: ** se agrupa de derecha a izquierda

# Formula de daño del Valle: se lee mejor con parentesis aunque no hagan falta
multiplicador_critico = 2
danio = (ataque - defensa) * multiplicador_critico
print("daño:", danio)
```

### Salida esperada

```
suma        22
resta       12
producto    85
division    3.4
div entera  3
resto       2
potencia    1024
-7 // 2 = -4
135 s = 2 min 15 s
¿turno par? False
oro final: 76
vida == 35 -> True
vida != 0  -> True
vida < 30  -> False
vida >= 30 -> True
¿vida entre 30 y 70? True
"ana" < "bron" -> True
"Zed" < "ana"  -> True
abre la puerta: True
hay luz: True
¿puede repartir? False
se presenta como: Viajero anónimo
¿'r' está en 'orco'? True
¿'dragon' está en 'jefe dragon rojo'? True
¿'z' NO está en 'slime'? True
objetivo is None: True
2 + 3 * 4   = 14
(2 + 3) * 4 = 20
-2 ** 2     = -4
2 ** 3 ** 2 = 512
daño: 24
```

### ¿Para qué sirve?

Los operadores están en cada regla de negocio: "envío gratis si la compra supera $30.000 **o** es cliente premium", "descuento si es jubilado **y** paga en efectivo". El `%` sirve para saber si un número es par, repartir turnos o armar relojes (`segundos // 60`, `segundos % 60`), y el cortocircuito evita divisiones por cero en planillas y reportes.

### Errores habituales

**Slime: `=` en lugar de `==`.** Python lo detecta y hasta sugiere el arreglo:
```
    if x = 5:
       ^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

**Goblin: dividir por cero** (`ZeroDivisionError: division by zero`). Protegé la
división con cortocircuito (`n != 0 and total / n`) o con un `if` (05).

**Ogros (corre, pero calcula mal):**
- Esperar un entero de `/`: `10 / 2` es `5.0`. Si necesitás entero, `//`.
- Olvidar que `and` va antes que `or`: `a and b or c` es `(a and b) or c`.
- `x == 1 or 2` **siempre** es verdadero (`2` es verdadero). Lo correcto es
  `x == 1 or x == 2` (o `x in (1, 2)`, en 06).
- Comparar números que vienen de `input()` sin convertir: `"10" < "9"` es
  `True` (compara letras, no números).
- `-7 // 2` da `-4`, no `-3`: `//` redondea hacia abajo, no "corta".

### Micro-misión R01-N02-P1 · Los golpes que hacen falta

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Aritméticos | + - * / · // división entera · % resto · ** potencia
recompensa: xp 10, oro 10
```

#### Escena
El cartel de Baldo tenía razón: el puente es de piedra negra, y en el arco se enrosca una **serpiente tallada** tan grande como el río. Cuando ponés un pie encima, sus ojos de musgo se encienden.
—Nadie cruza sin saber **calcular** —retumba—. Primera pregunta, aprendiz: si cada golpe tuyo quita 7 de vida, ¿cuántos golpes **enteros** necesitás para un enemigo de 50? ¿Y cuánta vida le queda después?

#### Gheco sugiere
`/` divide con decimales (`50 / 7` da `7.142…`). `//` da la **división entera** (cuántas veces entra) y `%` da **el resto** (lo que sobra). Son la pareja que más se usa para repartir y contar.

#### Desafío
Completá con los operadores que faltan.

#### Código inicial
```python
vida = 50
golpe = 7
print(f"Golpes enteros: {vida ___ golpe}")
print(f"Le queda: {vida ___ golpe}")
print(f"Golpes exactos: {vida / golpe:.2f}")
```

#### Salida esperada
```
Golpes enteros: 7
Le queda: 1
Golpes exactos: 7.14
```

#### Solución
```python
vida = 50
golpe = 7
print(f"Golpes enteros: {vida // golpe}")
print(f"Le queda: {vida % golpe}")
print(f"Golpes exactos: {vida / golpe:.2f}")
```

#### Al superarla
Se enciende la primera de las cinco runas talladas en la baranda del puente. El Guardián gruñe, que en piedra es lo más parecido a estar conforme.

#### Imagen
- El Puente del Juicio de noche: piedra negra sobre un río que brilla verde, con una serpiente gigante tallada en el arco y ojos de musgo encendidos.
- Mia, chiquita frente a la escultura, con el pergamino abierto donde brillan `//` y `%`.
- Gheco flota a su lado contando con los dedos.
- En la baranda, cinco runas: la primera encendida.

### Micro-misión R01-N02-P2 · La cuenta de la energía

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Asignación aumentada | x += 3 · x -= 5 · x *= 2 · x //= 2 (es x = x + 3, etc.)
recompensa: xp 10, oro 10
```

#### Escena
—Segunda pregunta. —El Guardián entrecierra los ojos—. Tenés 20 de energía. Cruzar el primer tramo te cuesta 5. En el medio hay una fuente que te devuelve 3. Y si llegás al final, el puente **duplica** lo que te quede. ¿Con cuánto llegás?

#### Gheco sugiere
Para cambiar una variable usando su propio valor hay atajos: `energia -= 5` es lo mismo que `energia = energia - 5`. También existen `+=`, `*=`, `//=` y `%=`.

#### Desafío
Escribí cada paso con un atajo y mostrá la energía después de cada uno.

#### Código inicial
```python
energia = 20
energia ___ 5
print(f"Primer tramo: {energia}")
energia ___ 3
print(f"La fuente: {energia}")
energia ___ 2
print(f"Al final: {energia}")
```

#### Salida esperada
```
Primer tramo: 15
La fuente: 18
Al final: 36
```

#### Solución
```python
energia = 20
energia -= 5
print(f"Primer tramo: {energia}")
energia += 3
print(f"La fuente: {energia}")
energia *= 2
print(f"Al final: {energia}")
```

#### Al superarla
Se enciende la segunda runa. Del medio del puente brota, de verdad, una fuente chiquita de agua verde. Gheco mete la cola y se ríe porque le hace cosquillas.

#### Imagen
- El medio del Puente del Juicio: una fuente pequeña de agua verde luminosa brota de la piedra.
- Gheco moja la cola en la fuente y se ríe.
- Mia anota en el pergamino `energia += 3`.
- Dos runas encendidas en la baranda.

### Micro-misión R01-N02-P3 · ¿Quién es más fuerte?

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Comparación | == != < > <= >= · encadenadas: 10 <= x < 20 · dan True o False
recompensa: xp 10, oro 10
```

#### Escena
—Tercera. —La voz del Guardián hace temblar el agua—. Tu fuerza es 12; la mía, 15. Decime sin miedo si sos más fuerte que yo. Decime si tu fuerza está entre 10 y 20, que es lo que pide el puente. Y decime si «Mia» y «mia» son el mismo nombre.

#### Gheco sugiere
Las comparaciones **siempre** dan `True` o `False`. Se pueden encadenar como en matemática: `10 <= fuerza < 20`. Y ojo: `=` guarda un valor; `==` **pregunta** si son iguales. Las mayúsculas cuentan: `"Mia" == "mia"` es `False`.

#### Desafío
Escribí las tres comparaciones.

#### Código inicial
```python
fuerza_mia = 12
fuerza_guardian = 15
print(fuerza_mia ___ fuerza_guardian)
print(10 <= fuerza_mia ___ 20)
print("Mia" ___ "mia")
```

#### Salida esperada
```
False
True
False
```

#### Solución
```python
fuerza_mia = 12
fuerza_guardian = 15
print(fuerza_mia > fuerza_guardian)
print(10 <= fuerza_mia < 20)
print("Mia" == "mia")
```

#### Al superarla
—No sos más fuerte que yo —dice el Guardián, y por primera vez suena divertido—. Pero no mentiste. Eso vale más.
Se enciende la tercera runa.

#### Imagen
- Primer plano de la cabeza de piedra del Guardián, a centímetros de Mia.
- Entre los dos flotan tres resultados de luz: `False`, `True`, `False`.
- Mia sostiene la mirada, con las manos apretando el pergamino; Gheco se esconde detrás de su coleta.

### Micro-misión R01-N02-P4 · La regla del puente

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Lógicos | and · or · not · cortocircuito · valor por defecto: nombre or "Anónimo"
recompensa: xp 15, oro 15
```

#### Escena
En la piedra del arco aparece grabada la regla del puente:
*«Pasa quien tenga nivel 5 o más y una llave, **o** quien sea maga y no esté maldita.»*
Tenés nivel 3, no tenés llave, sos aprendiz de maga y, que sepas, no estás maldita.
—¿Y cómo te llamo? —agrega el Guardián—. No me dijiste tu título. Si no tenés, te llamo «Aprendiz».

#### Gheco sugiere
`and` pide que se cumplan **las dos**; `or`, **alguna**; `not` da vuelta el valor. `and` se evalúa antes que `or`, pero los paréntesis lo hacen más claro. Y un truco: `titulo or "Aprendiz"` da `titulo` si tiene algo y, si está vacío, `"Aprendiz"`.

#### Desafío
Escribí la regla del puente con `and`, `or` y `not`, y el título con `or`.

#### Código inicial
```python
nivel = 3
tiene_llave = False
es_maga = True
maldita = False
titulo = ""
pasa = ___
print(f"¿Pasa? {pasa}")
print(f"Te llaman: {___}")
```

#### Salida esperada
```
¿Pasa? True
Te llaman: Aprendiz
```

#### Solución
```python
nivel = 3
tiene_llave = False
es_maga = True
maldita = False
titulo = ""
pasa = (nivel >= 5 and tiene_llave) or (es_maga and not maldita)
print(f"¿Pasa? {pasa}")
print(f"Te llaman: {titulo or 'Aprendiz'}")
```

#### Al superarla
La cuarta runa se enciende con un brillo violeta, del mismo color que tu túnica. Por un segundo, **una de las runas apagadas de tu túnica parpadea**, como si te reconociera. Después se apaga.

#### Imagen
- La regla del puente grabada en la piedra del arco, con `and`, `or` y `not` brillando.
- Mia mira sorprendida el borde de su túnica: una runa bordada parpadea en violeta.
- Cuatro runas encendidas en la baranda.

### Micro-misión R01-N02-P5 · La llave del puente

```meta
lugar: El Puente del Juicio
personajes: Mia, Gheco, el Guardián del Puente
carta: Pertenencia e identidad | "x" in texto · x is None · precedencia: * antes que +
recompensa: xp 15, oro 20
item: Llave del Puente
```

#### Escena
—Última —dice el Guardián, y abre la boca de piedra. Adentro, sobre la lengua, hay una **llave verde**—. Es tuya si me decís tres cosas: si la palabra «serpiente» está en mi nombre, si de verdad **no** tenías llave (si tu llave era `None`) y cuánto da `2 + 3 * 4`, que los apurados siempre contestan mal.

#### Gheco sugiere
`"serpiente" in texto` pregunta si un texto está **adentro** de otro. Para preguntar si algo es `None` se usa `is`: `llave is None`. Y la precedencia es la de la escuela: `*` antes que `+`. Si dudás, paréntesis.

#### Desafío
Completá las tres preguntas del Guardián.

#### Código inicial
```python
nombre = "Guardián del puente, la serpiente de piedra"
llave = None
print("serpiente" ___ nombre)
print(llave ___ None)
print(2 + 3 * 4, ___)
```

#### Salida esperada
```
True
True
14 20
```

#### Solución
```python
nombre = "Guardián del puente, la serpiente de piedra"
llave = None
print("serpiente" in nombre)
print(llave is None)
print(2 + 3 * 4, (2 + 3) * 4)
```

#### Al superarla
Las cinco runas brillan a la vez. El Guardián deja caer la **Llave del Puente** en tu mano y se vuelve a quedar quieto, piedra otra vez.
Del otro lado del río, entre los faroles de la Aldea, hay una casa con la puerta abierta y montañas de carteles afuera: **la Casa de los Copistas**. Alguien adentro está gritando que nadie entiende lo que escribe.

#### Imagen
- El Guardián de piedra con la boca abierta; sobre su lengua, una llave verde brillante.
- Mia estira la mano para tomarla.
- Las cinco runas de la baranda encendidas.
- Al fondo, cruzando el río, una casa con carteles amontonados en la puerta.

### Misión R01-N02-M1 · El reloj de arena

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Pasá 4000 segundos a horas, minutos y segundos usando
solo `//` y `%`, y mostralo también como `01:06:40`.

#### Criterio de aprobación

- Usa solo `//` y `%` para calcular horas, minutos y segundos.
- Muestra `4000 segundos = 1 h 6 min 40 s`.
- Muestra el formato reloj `01:06:40`.

#### Salida esperada

```
4000 segundos = 1 h 6 min 40 s
Formato reloj: 01:06:40
```

#### Solución de referencia

```python
"""Mision 1 - El reloj de arena: pasar segundos a horas, minutos y segundos."""

total = 4000

horas = total // 3600
resto = total % 3600          # los segundos que no llegaron a formar una hora
minutos = resto // 60
segundos = resto % 60

print(f"{total} segundos = {horas} h {minutos} min {segundos} s")
print(f"Formato reloj: {horas:02}:{minutos:02}:{segundos:02}")
```

### Misión R01-N02-M2 · El Puente del Juicio

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Pasa quien tiene nivel 5 o más, **y** (llave **o**
magia), **y no** está maldito. Evaluá la regla para Kira (nivel 6, con llave),
Mia (nivel 5, maga, sin llave) y Zed (nivel 8, con llave, maldito). Después
probá la regla **sin paréntesis** con un aprendiz mago de nivel 1 y explicá
por qué cambia el resultado.

#### Criterio de aprobación

- Evalúa la regla con paréntesis para Kira (True), Mia (True) y Zed (False).
- Prueba la regla sin paréntesis con el aprendiz y muestra que cambia el resultado.
- Explica en un comentario que `and` se evalúa antes que `or`.

#### Salida esperada

```
Kira puede entrar: True
Mia puede entrar:  True
Zed puede entrar:  False
Aprendiz, SIN parentesis: True
Aprendiz, CON parentesis: False
```

#### Solución de referencia

```python
"""Mision 2 - ¿Quien puede entrar a la mazmorra?

Regla: nivel 5 o mas, Y (tener la llave O ser mago), Y NO estar maldito.
Los parentesis son OBLIGATORIOS: 'and' se evalua antes que 'or'.
"""

# Kira: nivel 6, con llave, no es maga, no esta maldita
nivel = 6
tiene_llave = True
es_mago = False
maldito = False
print("Kira puede entrar:", nivel >= 5 and (tiene_llave or es_mago) and not maldito)

# Mia: nivel 5, sin llave, pero es maga
nivel = 5
tiene_llave = False
es_mago = True
print("Mia puede entrar: ", nivel >= 5 and (tiene_llave or es_mago) and not maldito)

# Zed: nivel 8, con llave, pero MALDITO
nivel = 8
tiene_llave = True
es_mago = False
maldito = True
print("Zed puede entrar: ", nivel >= 5 and (tiene_llave or es_mago) and not maldito)

# Un aprendiz mago de nivel 1: sin parentesis la condicion cambia de significado.
#   nivel >= 5 and tiene_llave or es_mago and not maldito
#   se agrupa como:  (nivel >= 5 and tiene_llave) or (es_mago and not maldito)
nivel = 1
tiene_llave = False
es_mago = True
maldito = False
print("Aprendiz, SIN parentesis:", nivel >= 5 and tiene_llave or es_mago and not maldito)
print("Aprendiz, CON parentesis:", nivel >= 5 and (tiene_llave or es_mago) and not maldito)
```

### Misión R01-N02-M3 · Predicción

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con `ataque = 20` y `defensa = 6`, anotá qué da cada línea antes
de ejecutarla: `ataque - defensa * 2`, `(ataque - defensa) * 2`,
`ataque // defensa + 1`, `ataque % defensa ** 2`,
`not ataque > 10 or defensa`, `1 < ataque < 10`.

#### Criterio de aprobación

- Anota en comentarios la predicción de cada una de las seis líneas.
- Ejecuta y compara: explica al menos las que no acertó.

#### Salida esperada

```
8
28
4
20
6
False
```

#### Solución de referencia

```python
"""Mision 3 - Predecir el resultado (precedencia). Anotalos ANTES de correr."""

ataque = 20
defensa = 6
print(ataque - defensa * 2)          # 8:   * antes que -
print((ataque - defensa) * 2)        # 28
print(ataque // defensa + 1)         # 4:   20 // 6 = 3, mas 1
print(ataque % defensa ** 2)         # 20:  6 ** 2 = 36; 20 % 36 = 20
print(not ataque > 10 or defensa)    # 6:   (not True) or 6 -> False or 6 -> 6
print(1 < ataque < 10)               # False: 20 no es menor que 10
```

### Encargo R01-N02-E1 · El calendario del escriba

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El escriba necesita saber si un año es **bisiesto**: lo es si es divisible por 4
y no por 100, **o** si es divisible por 400. Escribí la expresión y probala con
1900, 2000, 2024 y 2026 (resultado: `False`, `True`, `True`, `False`).

#### Criterio de aprobación

- Escribe la regla del bisiesto en una sola expresión, con paréntesis.
- Da False, True, True y False para 1900, 2000, 2024 y 2026.

#### Salida esperada

```
1900 False
2000 True
2024 True
2026 False
```

#### Solución de referencia

```python
"""Encargo del Gremio - El calendario del escriba: ¿el anio es bisiesto?

Es bisiesto si es divisible por 4 y NO por 100, o si es divisible por 400.
"""

anio = 1900
print(anio, (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0)
anio = 2000
print(anio, (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0)
anio = 2024
print(anio, (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0)
anio = 2026
print(anio, (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0)
```

### Prueba del sello

#### ¿Qué dan `7 / 2`, `7 // 2` y `7 % 2`?

`3.5`, `3` y `1`.

#### ¿Qué diferencia hay entre `=` y `==`?

`=` **asigna** un valor a un nombre; `==` **compara** dos valores y da `True` o `False`.

#### ¿Qué devuelve `"" or "Anónimo"`? ¿Y `"Kira" or "Anónimo"`?

`"" or "Anónimo"` da `"Anónimo"` (el texto vacío es falso). `"Kira" or "Anónimo"` da `"Kira"`.

#### ¿Por qué `oro > 0 and 100 / oro > 10` no falla cuando `oro` es 0?

Por el cortocircuito: como `oro > 0` es falso, el `and` ya sabe que el resultado es falso y no evalúa la división.

#### ¿Cuándo se usa `is` y cuándo `==`?

`is` para preguntar por `None` (`x is None`); `==` para comparar valores (números, textos y todo lo demás).

#### ¿Cuánto vale `2 + 3 * 2 ** 2`?

`14`: primero `2 ** 2 = 4`, después `3 * 4 = 12`, y al final `2 + 12`.

### Soluciones (docente)

Material original: `17-Python/03-Operadores` (soluciones completas en `soluciones/`).

La misión 2 es la que más cuesta: pedir que escriban la condición del aprendiz agrupada a mano (`(a and b) or (c and not d)`) antes de ejecutar.

## R01-N03 · Strings: el texto

```meta
tipo: tema
padre: R01-N02
precio: 10
criatura: orco
temas: prog.cadenas
```

### Crónica

En la Gran Biblioteca del Valle, los pergaminos están escritos en runas desordenadas: nombres con espacios de más, palabras en mayúsculas y minúsculas mezcladas, mensajes que solo se leen al revés. La bibliotecaria te pide ayuda.

{mentor} sonríe: —Un texto es una **fila de letras**, {heroe}. Si sabés contarlas, cortarlas y transformarlas, ningún pergamino se te va a resistir.

### Objetivos

Manejar texto con soltura: acceder a caracteres por posición, cortar pedazos,
transformar con métodos, buscar y reemplazar, partir y unir, y alinear en
columnas.

### Antes de empezar

- Variables, `print`, f-strings (01).
- El tipo `str` y las conversiones (02).
- Los operadores `+`, `*` e `in` (03).

### Explicación

#### Crear textos
- Comillas simples o dobles: `'hola'` o `"hola"`. Elegí las que **no** aparezcan
  dentro del texto: `"el 'apóstrofo'"`.
- **Secuencias de escape** con `\`: `\n` (salto de línea), `\t` (tabulación),
  `\"` (comilla), `\\` (una barra invertida).
- **Triples comillas** (`"""..."""`): texto de varias líneas tal cual se escribe.

#### Largo, índices y cortes
Un texto es una **secuencia**: cada carácter tiene una posición (**índice**).

```
 S   E   R   P   I   E   N   T   E
 0   1   2   3   4   5   6   7   8     <- índices positivos
-9  -8  -7  -6  -5  -4  -3  -2  -1     <- índices negativos
```

- `len(runa)` → 9. `runa[0]` → `"S"` (**se empieza a contar desde 0**).
  `runa[-1]` → `"E"` (el último).
- **Slicing** `texto[inicio:fin:paso]`: desde `inicio` **hasta `fin` sin
  incluirlo**.
  - `runa[0:4]` → `"SERP"`, `runa[:4]` (desde el principio), `runa[4:]` (hasta el final).
  - `runa[-5:]` → los últimos 5.
  - `runa[::2]` → uno sí y uno no. `runa[::-1]` → **al revés**.
- Un índice fuera de rango es un error (`runa[20]`), pero un **corte** fuera de
  rango no: `runa[5:100]` devuelve lo que haya.

#### Los textos son inmutables
No se puede cambiar un carácter: `runa[0] = "Z"` da `TypeError`. Hay que armar un
texto nuevo: `"Z" + runa[1:]`. Por eso **todos los métodos devuelven un texto
nuevo** y el original queda igual: si querés conservar el cambio, **asignalo**:
`nombre = nombre.strip()`.

#### Métodos principales
| Método | Hace | `"  el Orco  "` → |
|---|---|---|
| `strip()` / `lstrip()` / `rstrip()` | saca espacios de los bordes (ambos / izquierda / derecha) | `"el Orco"` |
| `upper()` / `lower()` | todo en mayúsculas / minúsculas | `"  EL ORCO  "` |
| `title()` / `capitalize()` | Cada Palabra / solo la primera letra | |
| `replace(a, b)` | reemplaza todas las apariciones de `a` por `b` | |
| `count(x)` | cuántas veces aparece `x` | |
| `find(x)` | posición donde empieza `x`, o `-1` si no está | |
| `index(x)` | igual que `find`, pero da **error** si no está | |
| `startswith(x)` / `endswith(x)` | ¿empieza / termina con `x`? | |
| `isdigit()` / `isalpha()` | ¿son todos dígitos / todas letras? | |
| `split(sep)` | parte el texto en una **lista** de pedazos | |
| `sep.join(lista)` | une los pedazos de una lista con `sep` en el medio | |

Los métodos se pueden **encadenar**: `grito.strip().title()` aplica `strip` y al
resultado le aplica `title`.

`split` y `join` trabajan con **listas**, que se ven en 06. Por ahora alcanza con
saber que `"a,b,c".split(",")` da `['a', 'b', 'c']` y que `"-".join(...)` las
vuelve a unir.

#### Alinear en columnas (f-strings)
`{valor:<10}` a la izquierda, `{valor:>10}` a la derecha, `{valor:^10}`
centrado, en un ancho de 10. Se puede elegir el relleno: `{valor:*^10}`.

#### Unicode
Los acentos, la `ñ` y los símbolos son caracteres como cualquier otro:
`len("Ñandú")` es 5 y `"ñ".upper()` es `"Ñ"`.

### Código de ejemplo

```python
"""04 - Strings (texto).

Un str es una SECUENCIA de caracteres: se puede medir, recorrer por posicion,
cortar en pedazos y transformar con sus metodos. Es INMUTABLE: ningun metodo
cambia el texto original, todos devuelven uno nuevo.
"""

# =========================================================
# Crear textos
# =========================================================
simple = 'comillas simples'
doble = "comillas dobles: sirven si el texto tiene un 'apóstrofo'"
print(simple)
print(doble)

# Caracteres especiales con \  (secuencias de escape)
print("Línea 1\nLínea 2")          # \n = salto de linea
print("Nombre:\tKira")             # \t = tabulacion
print("Ofidia dijo: \"escribí\"")  # \" = comilla dentro del texto
print("C:\\valle\\mapa.txt")       # \\ = una barra invertida

# Texto de varias lineas con triples comillas
cartel = """=== POSADA DEL ROBLE ===
Cama: 5 monedas
Sopa: 2 monedas"""
print(cartel)

# =========================================================
# Largo, posiciones (indices) y cortes (slicing)
# =========================================================
runa = "SERPIENTE"
print("largo:", len(runa))         # 9 caracteres
print("primera:", runa[0])         # los indices empiezan en 0
print("tercera:", runa[2])
print("última:", runa[-1])         # indices negativos: desde el final
print("anteúltima:", runa[-2])

# texto[inicio:fin]  -> desde inicio HASTA fin, SIN incluir fin
print("runa[0:4] =", runa[0:4])    # 'SERP'
print("runa[:4]  =", runa[:4])     # sin inicio: desde el principio
print("runa[4:]  =", runa[4:])     # sin fin: hasta el final
print("runa[-5:] =", runa[-5:])    # los ultimos 5
print("runa[::2] =", runa[::2])    # de 2 en 2 (el tercer numero es el paso)
print("runa[::-1] =", runa[::-1])  # paso negativo: al reves

# =========================================================
# Operar con textos
# =========================================================
print("fuego" + "bola")            # concatenar (unir)
print("-" * 20)                    # repetir
print("¿'PIEN' en la runa?", "PIEN" in runa)

# Inmutable: no se puede cambiar un caracter. Se arma un texto NUEVO.
# runa[0] = "Z"                    # -> TypeError
nueva = "Z" + runa[1:]
print(runa, "->", nueva)

# =========================================================
# Metodos: texto.metodo(...)
# =========================================================
grito = "  kira LA valiente  "
print(f"[{grito.strip()}]")        # saca espacios de los bordes
print(f"[{grito.upper()}]")        # MAYUSCULAS
print(f"[{grito.lower()}]")        # minusculas
print(f"[{grito.strip().title()}]")        # Cada Palabra Con Mayuscula
print(f"[{grito.strip().capitalize()}]")   # Solo la primera
print(f"[{grito}]  <- el original no cambió")

frase = "el orco ataca, el orco huye"
print("replace:", frase.replace("orco", "ogro"))
print("count:", frase.count("orco"))
print("find:", frase.find("ataca"))       # posicion donde empieza
print("find (no está):", frase.find("dragon"))   # -1 si no lo encuentra
print("startswith:", frase.startswith("el"))
print("endswith:", frase.endswith("huye"))

# Preguntas sobre el contenido
print('"123".isdigit():', "123".isdigit())
print('"12a".isdigit():', "12a".isdigit())
print('"Kira".isalpha():', "Kira".isalpha())

# split parte el texto y join lo vuelve a unir.
# split devuelve una LISTA de textos: las listas se ven en 06.
partes = "espada,escudo,poción".split(",")
print("split:", partes)
print("join:", " + ".join(partes))
print("palabras:", "el   valle    duerme".split())   # sin argumento: por espacios

# =========================================================
# Alinear texto en f-strings:  {valor:<ancho}  {valor:>ancho}  {valor:^ancho}
# =========================================================
print(f"|{'Kira':<10}|{'Bron':>10}|{'Mia':^10}|")
print(f"|{'Zed':*^10}|")           # rellenar con un caracter

# =========================================================
# Unicode: acentos, ñ y simbolos son caracteres normales
# =========================================================
lugar = "Ñandú del Sur"
print(lugar, "- largo:", len(lugar), "- mayúsculas:", lugar.upper())
```

### Salida esperada

```
comillas simples
comillas dobles: sirven si el texto tiene un 'apóstrofo'
Línea 1
Línea 2
Nombre:	Kira
Ofidia dijo: "escribí"
C:\valle\mapa.txt
=== POSADA DEL ROBLE ===
Cama: 5 monedas
Sopa: 2 monedas
largo: 9
primera: S
tercera: R
última: E
anteúltima: T
runa[0:4] = SERP
runa[:4]  = SERP
runa[4:]  = IENTE
runa[-5:] = IENTE
runa[::2] = SRINE
runa[::-1] = ETNEIPRES
fuegobola
--------------------
¿'PIEN' en la runa? True
SERPIENTE -> ZERPIENTE
[kira LA valiente]
[  KIRA LA VALIENTE  ]
[  kira la valiente  ]
[Kira La Valiente]
[Kira la valiente]
[  kira LA valiente  ]  <- el original no cambió
replace: el ogro ataca, el ogro huye
count: 2
find: 8
find (no está): -1
startswith: True
endswith: True
"123".isdigit(): True
"12a".isdigit(): False
"Kira".isalpha(): True
split: ['espada', 'escudo', 'poción']
join: espada + escudo + poción
palabras: ['el', 'valle', 'duerme']
|Kira      |      Bron|   Mia    |
|***Zed****|
Ñandú del Sur - largo: 13 - mayúsculas: ÑANDÚ DEL SUR
```

### ¿Para qué sirve?

Casi todos los datos llegan como texto y **sucios**: un DNI con puntos, un correo con mayúsculas y espacios, un nombre escrito en minúscula. Limpiarlos (`strip`, `lower`, `replace`), separarlos (`split`) y darles formato para un reporte o un ticket (`ljust`, f-strings) es trabajo de todos los días en formularios, planillas, chats y bases de datos.

### Errores habituales

**Troll de la inmutabilidad** (`TypeError`):
```
>>> runa = "SERP"
>>> runa[0] = "Z"
TypeError: 'str' object does not support item assignment
```

**Orco: índice fuera de rango** (`IndexError`). Si el texto tiene 4 letras, los
índices válidos van de 0 a 3:
```
IndexError: string index out of range
```

**Goblin: `index` de algo que no está** (`ValueError: substring not found`).
Si no estás seguro de que esté, usá `find` y fijate si da `-1`.

**Ogros (corre, pero hace otra cosa):**
- Llamar al método y no guardar el resultado: `nombre.strip()` sola **no cambia**
  `nombre`. Hay que escribir `nombre = nombre.strip()`.
- Olvidar los paréntesis: `nombre.upper` (sin `()`) no llama al método; muestra
  algo como `<built-in method upper ...>`.
- Pensar que `texto[2:5]` incluye la posición 5: no la incluye.
- Comparar sin normalizar: `"Kira" == "kira"` es `False`. Compará
  `a.lower() == b.lower()`.

### Micro-misión R01-N03-P1 · El cartel que no se entiende

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Crear textos | "…" o '…' · \n salto de línea · \" comilla adentro · """varias líneas"""
recompensa: xp 10, oro 10
```

#### Escena
Adentro hay carteles por todos lados: colgados, apilados, pegados al techo. Una mujer alta de túnica lila, con el pelo negro recogido con horquillas, pasea entre ellos con una pluma en la mano.
—¡Por fin alguien que sabe runas! Soy **la Copista**. Me encargaron un cartel para la Posada y me sale todo en una sola línea, y con las comillas rotas. Tiene que decir *Se busca* arriba y, abajo, *"aprendiz" que sepa runas*, con las comillas.

#### Gheco sugiere
Dentro de un texto, la barra `\` anuncia un carácter especial: `\n` es un **salto de línea** y `\"` es una **comilla** que no cierra el texto. También podés escribir varias líneas entre triples comillas `"""…"""`.

#### Desafío
Arreglá el cartel con `\n` y `\"`.

#### Código inicial
```python
cartel = "Se busca: "aprendiz" que sepa runas"
print(cartel)
```

#### Salida esperada
```
Se busca:
"aprendiz" que sepa runas
```

#### Solución
```python
cartel = "Se busca:\n\"aprendiz\" que sepa runas"
print(cartel)
```

#### Al superarla
El cartel se dobla solo en dos renglones prolijos. La Copista aplaude con la pluma.
—¡Eso! Ahora, el resto…

#### Imagen
- Interior de la Casa de los Copistas: carteles colgados del techo, pilas de pergaminos, faroles verdes.
- La Copista, alta, túnica lila con cintas de texto holográfico flotando, pelo negro con horquillas, pluma en mano.
- Mia sostiene un cartel que se acomoda en dos renglones de luz.

### Micro-misión R01-N03-P2 · El mensaje al revés

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Índices y cortes | t[0] primero · t[-1] último · t[2:5] del 2 al 4 · t[::-1] al revés
recompensa: xp 10, oro 10
```

#### Escena
La Copista te pasa un papel viejo.
—Este llegó así. Todos los mensajes de la Aldea vienen al derecho, menos los de **un** cliente, que los escribe al revés para que no los lean los curiosos.
El papel dice: `otnirebaL le ne somev soN`.

#### Gheco sugiere
Cada letra de un texto tiene una **posición**, y se empieza a contar desde **0**: `t[0]` es la primera y `t[-1]`, la última. `t[2:5]` corta de la 2 a la 4 (la 5 no entra). Y `t[::-1]` recorre todo hacia atrás: lo da vuelta.

#### Desafío
Mostrá la primera letra, la última y el mensaje al derecho.

#### Código inicial
```python
mensaje = "otnirebaL le ne somev soN"
print(mensaje[___], mensaje[___])
print(mensaje[___])
```

#### Salida esperada
```
o N
Nos vemos en el Laberinto
```

#### Solución
```python
mensaje = "otnirebaL le ne somev soN"
print(mensaje[0], mensaje[-1])
print(mensaje[::-1])
```

#### Al superarla
*Nos vemos en el Laberinto.* La Copista se encoge de hombros.
—Así firma ese cliente. Nunca le vi la cara: deja los pedidos por debajo de la puerta.

#### Imagen
- Primer plano de un papel amarillento con letras al revés; sobre él, el mismo mensaje se da vuelta en el aire, letra por letra, en luz verde.
- La mano de Mia sostiene el papel; Gheco cuelga cabeza abajo de su brazo para leerlo «al derecho».

### Micro-misión R01-N03-P3 · La tinta que no se borra

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Textos inmutables | nombre.upper() da un texto NUEVO · para guardarlo: nombre = nombre.upper()
recompensa: xp 10, oro 10
```

#### Escena
—Los títulos van en mayúsculas —dice la Copista—. Pasá este a mayúsculas.
Escribís `titulo.upper()`, mostrás `titulo`… y sigue en minúsculas. Gheco suspira.

#### Gheco sugiere
Los textos en Python **no se modifican**: son como tinta que no se borra. `titulo.upper()` no cambia `titulo`: **devuelve un texto nuevo**. Si lo querés guardar, reasignalo: `titulo = titulo.upper()`. Por eso `titulo[0] = "X"` da error.

#### Desafío
Hacé que el título quede guardado en mayúsculas.

#### Código inicial
```python
titulo = "casa de los copistas"
titulo.upper()
print(titulo)
```

#### Salida esperada
```
CASA DE LOS COPISTAS
```

#### Solución
```python
titulo = "casa de los copistas"
titulo = titulo.upper()
print(titulo)
```

#### Al superarla
—Tinta que no se borra —repite la Copista, como si fuera un refrán—. Mi maestra decía que por eso se copia: el original no se toca nunca.

#### Imagen
- Un letrero de madera sobre la puerta de la Casa, que pasa de minúsculas a mayúsculas: CASA DE LOS COPISTAS, en letras de luz.
- La Copista lo mira con aprobación; Mia, con el pergamino en alto.

### Micro-misión R01-N03-P4 · Ordenar los carteles

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Métodos de texto | strip() saca espacios de las puntas · lower() · upper() · title() · replace("a", "b")
recompensa: xp 15, oro 15
```

#### Escena
El cartel más feo de todos es el de una oficina de la Aldea: tiene espacios por todos lados y mayúsculas mezcladas, como si lo hubiera escrito un goblin.
`"   oFIcina de LAS runas   "`
—Necesito que quede *Oficina De Las Runas*, sin espacios en las puntas.

#### Gheco sugiere
`strip()` saca los espacios de las puntas y `title()` pone en mayúscula la primera letra de cada palabra. Se pueden **encadenar**: `texto.strip().title()`.

#### Desafío
Limpiá el cartel encadenando los dos métodos. Los corchetes muestran dónde empieza y termina.

#### Código inicial
```python
cartel = "   oFIcina de LAS runas   "
limpio = cartel
print(f"[{limpio}]")
```

#### Salida esperada
```
[Oficina De Las Runas]
```

#### Solución
```python
cartel = "   oFIcina de LAS runas   "
limpio = cartel.strip().title()
print(f"[{limpio}]")
```

#### Al superarla
Los carteles de toda la casa se acomodan solos, como si hubieran estado esperando que alguien les dijera cómo. Uno, viejísimo, cae de un estante a tus pies.

#### Imagen
- Decenas de carteles que se ordenan solos en el aire de la Casa, letras que se acomodan.
- Uno muy viejo cae a los pies de Mia; la Copista se agacha a mirarlo.

### Micro-misión R01-N03-P5 · La firma del vitral

```meta
lugar: La Casa de los Copistas
personajes: Mia, Gheco, la Copista
carta: Alinear | f"{t:<10}" izquierda · f"{t:>8}" derecha · f"{t:^12}" centro · len() cuenta letras (también ñ y tildes)
recompensa: xp 15, oro 15
se abre: la primera nota del viajero en el grimorio (el cartel viejo con la firma del vitral)
```

#### Escena
El cartel viejo no es un cartel: es una **tabla de pedidos**, con tres columnas perfectas, escrita con una letra tan clara que da gusto leerla. Abajo, en una esquina, **el mismo vitral** del papelito de Baldo.
—Lo hizo un cliente hace muchísimos años —dice la Copista—. Me lo dejó como modelo: *«así se ordena un pedido»*. Nunca supe cómo lo hacía tan prolijo.
Gheco se frota las patas.
—Yo sí. Probemos.

#### Gheco sugiere
En un f-string, después de `:` podés decir el **ancho** y la **alineación**: `{texto:<10}` ocupa 10 lugares a la izquierda; `{texto:>8}`, 8 a la derecha; `{texto:^12}`, centrado. Así las columnas quedan derechas. Y `len("ñandú")` da 5: la ñ y las tildes cuentan como una letra.

#### Desafío
Armá la tabla con las columnas alineadas: el pedido a la izquierda (10 lugares) y la cantidad a la derecha (5 lugares).

#### Código inicial
```python
print(f"{'Pedido'}|{'Cant.'}")
print(f"{'Tinta'}|{3}")
print(f"{'Pergamino'}|{12}")
print(len("ñandú"))
```

#### Salida esperada
```
Pedido    |Cant.
Tinta     |    3
Pergamino |   12
5
```

#### Solución
```python
print(f"{'Pedido':<10}|{'Cant.':>5}")
print(f"{'Tinta':<10}|{3:>5}")
print(f"{'Pergamino':<10}|{12:>5}")
print(len("ñandú"))
```

#### Al superarla
Tu tabla queda igual de derecha que la del viajero. Le mostrás a la Copista el papelito de Baldo: el mismo vitral. Ella abre grandes los ojos.
—Ese cliente decía siempre una cosa: que el camino a las Terrazas de las Funciones **cruza el Laberinto de las Siete Salas**. Y que quien no sabe decidir, no sale.
Te guarda el cartel viejo en el pergamino, como quien entrega una herencia.

#### Imagen
- Un pergamino antiguo con una tabla de tres columnas perfectamente alineadas, letra clarísima; en la esquina inferior, un pequeño vitral dibujado en tinta.
- Mia sostiene al lado el papelito de Baldo con el mismo dibujo: los dos vitrales se iluminan a la vez.
- La Copista, sorprendida, con la mano en el pecho.

### Misión R01-N03-M1 · El nombre del héroe

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

A partir de `"   kira la VALIENTE   "`, obtené
`"Kira La Valiente"`, sus iniciales (`K.L.V.`) usando índices, el largo y el
nombre en mayúsculas centrado en 30 caracteres.

#### Criterio de aprobación

- Limpia el texto y lo muestra como `Kira La Valiente`.
- Arma las iniciales `K.L.V.` usando índices.
- Muestra el largo y el nombre en mayúsculas centrado en 30 caracteres.

#### Salida esperada

```
Nombre: [Kira La Valiente]
Iniciales: K.L.V.
Largo sin espacios de borde: 16
Para el cartel:        KIRA LA VALIENTE       |
```

#### Solución de referencia

```python
"""Mision 1 - El nombre del heroe, prolijo."""

entrada = "   kira la VALIENTE   "

limpio = entrada.strip().title()
print(f"Nombre: [{limpio}]")
print(f"Iniciales: {limpio[0]}.{limpio[5]}.{limpio[8]}.")
print(f"Largo sin espacios de borde: {len(limpio)}")
print(f"Para el cartel: {limpio.upper():^30}|")
```

### Misión R01-N03-M2 · La runa espejo

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Un **palíndromo** se lee igual al derecho y al revés.
Comprobá si `"Anita lava la tina"` lo es, ignorando mayúsculas y espacios.
Probá también con `"El orco ataca"`.

#### Criterio de aprobación

- Normaliza el texto (minúsculas y sin espacios) antes de comparar.
- Compara con el texto dado vuelta (`[::-1]`).
- Dice que "Anita lava la tina" es palíndromo y "El orco ataca" no.

#### Salida esperada

```
"Anita lava la tina" -> "anitalavalatina"
¿Es palíndromo? True
"El orco ataca" -> "elorcoataca"
¿Es palíndromo? False
```

#### Solución de referencia

```python
"""Mision 2 - La runa espejo: ¿la frase es un palindromo?

Un palindromo se lee igual al derecho y al reves (ignorando espacios y
mayusculas). Invertir un texto: texto[::-1]
"""

frase = "Anita lava la tina"
normalizada = frase.lower().replace(" ", "")
print(f'"{frase}" -> "{normalizada}"')
print("¿Es palíndromo?", normalizada == normalizada[::-1])

frase = "El orco ataca"
normalizada = frase.lower().replace(" ", "")
print(f'"{frase}" -> "{normalizada}"')
print("¿Es palíndromo?", normalizada == normalizada[::-1])
```

### Misión R01-N03-M3 · La tabla de la compañía

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Mostrá una tabla alineada con encabezados
`NOMBRE`, `CLASE` y `NIVEL`, con Kira (espadachina, 3), Bron (guerrero, 5),
Mia (maga, 4) y Zed (pícaro, 2). Los nombres y las clases, a la izquierda; el
nivel, a la derecha.

#### Criterio de aprobación

- Muestra los encabezados NOMBRE, CLASE y NIVEL.
- Nombres y clases alineados a la izquierda; el nivel, a la derecha.
- Las columnas quedan parejas en todas las filas.

#### Salida esperada

```
NOMBRE  CLASE        NIVEL
--------------------------
Kira    espadachina      3
Bron    guerrero         5
Mia     maga             4
Zed     picaro           2
```

#### Solución de referencia

```python
"""Mision 3 - La tabla de la compania, alineada con f-strings."""

print(f"{'NOMBRE':<8}{'CLASE':<12}{'NIVEL':>6}")
print("-" * 26)
print(f"{'Kira':<8}{'espadachina':<12}{3:>6}")
print(f"{'Bron':<8}{'guerrero':<12}{5:>6}")
print(f"{'Mia':<8}{'maga':<12}{4:>6}")
print(f"{'Zed':<8}{'picaro':<12}{2:>6}")
```

### Encargo R01-N03-E1 · Los correos del Gremio

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El Gremio guarda los correos de sus socios, pero cada uno lo escribe como
quiere: `"   Kira.Espada@Valle.COM "`. Normalizalo (sin espacios y en minúsculas),
separá el **usuario** (lo que va antes de la `@`) y el **dominio** (lo que va
después) usando `find` y cortes, y verificá que tenga una sola `@`.

#### Criterio de aprobación

- Normaliza el correo con `strip()` y `lower()`.
- Separa usuario y dominio con `find` y cortes.
- Verifica que tenga exactamente una `@`.

#### Salida esperada

```
normalizado: kira.espada@valle.com
usuario: kira.espada
dominio: valle.com
¿es del Valle? True
¿tiene una sola @? True
```

#### Solución de referencia

```python
"""Encargo del Gremio - El padron de correos del Gremio.

Los socios escriben su email de cualquier manera. Hay que normalizarlo y
separar usuario y dominio.
"""

email = "   Kira.Espada@Valle.COM "

email = email.strip().lower()
arroba = email.find("@")
usuario = email[:arroba]
dominio = email[arroba + 1:]

print("normalizado:", email)
print("usuario:", usuario)
print("dominio:", dominio)
print("¿es del Valle?", dominio.endswith("valle.com"))
print("¿tiene una sola @?", email.count("@") == 1)
```

### Prueba del sello

#### Si `t = "DRAGON"`, ¿qué dan `t[1]`, `t[-1]`, `t[1:4]` y `t[::-1]`?

`t[1]` es `"R"`, `t[-1]` es `"N"`, `t[1:4]` es `"RAG"` y `t[::-1]` es `"NOGARD"`.

#### ¿Por qué `nombre.upper()` no cambia `nombre`? ¿Cómo hacés para que sí cambie?

Porque los textos son **inmutables**: `upper()` devuelve un texto nuevo. Para que cambie hay que reasignar: `nombre = nombre.upper()`.

#### ¿Qué diferencia hay entre `find` e `index` cuando el texto no aparece?

`find` devuelve `-1`; `index` lanza `ValueError`.

#### ¿Qué devuelve `"a-b-c".split("-")`? ¿Y `"+".join(...)` sobre eso?

`["a", "b", "c"]`. Y `"+".join(["a", "b", "c"])` da `"a+b+c"`.

#### ¿Cómo mostrás un texto alineado a la derecha en 12 caracteres?

Con `f"{texto:>12}"` o `texto.rjust(12)`.

### Soluciones (docente)

Material original: `17-Python/04-Strings` (soluciones completas en `soluciones/`).

## R01-N04 · Decidir y repetir

```meta
tipo: tema
padre: R01-N03
precio: 10
criatura: ogro
temas: prog.condicionales, prog.bucles, err.validacion
```

### Crónica

El Laberinto de las Siete Salas no se cruza caminando derecho. En cada sala hay que **decidir**: si hay trampa, esquivar; si hay cofre, abrir; si aparece el jefe, huir. Y hay que **repetir**: avanzar sala por sala hasta encontrar la salida.

{mentor} te enseña las runas del camino: `if` para elegir, `while` y `for` para insistir, `break` para escapar a tiempo.

### Objetivos

Controlar qué se ejecuta y cuántas veces: condicionales (`if`/`elif`/`else`,
`match`), bucles (`while`, `for`, `range`), `break`/`continue`, `for ... else`, y
validar lo que escribe el usuario.

### Antes de empezar

- Tipos y valores "verdaderos"/"falsos" (02).
- Operadores de comparación y lógicos (03).
- Recorrer y cortar textos, `split`, `isdigit` (04).

### Explicación

#### Bloques e indentación
Una línea que termina en `:` abre un **bloque**: las líneas de abajo, con 4
espacios más de indentación, le pertenecen. El bloque termina cuando la
indentación vuelve atrás.

```python
if vida < 30:
    print("¡cuidado!")      # dentro del if
    print("tomá una poción")  # dentro del if
print("sigue el juego")     # fuera: se ejecuta siempre
```

#### `if` / `elif` / `else`
- Se evalúan **en orden** y se ejecuta **solo el primer** bloque cuya condición se
  cumple. `elif` y `else` son opcionales.
- La condición puede ser cualquier valor: se usa su verdad (02). `if not nombre:`
  significa "si el nombre está vacío".
- Se pueden **anidar** (`if` dentro de `if`), pero más de dos o tres niveles se
  vuelven difíciles de leer: conviene combinar condiciones con `and`/`or`.
- **Expresión condicional**: `a if condición else b` elige un valor en una línea:
  `mensaje = "pagás" if oro >= 5 else "dormís afuera"`.

#### `while`: repetir mientras se cumpla
```python
while antorchas > 0:
    antorchas -= 1
```
Si nada dentro del bucle cambia la condición, el bucle es **infinito** (se corta
con Ctrl+C). El patrón `while True:` + `break` sirve cuando la condición de salida
está en el medio del bloque.

#### `for`: repetir por cada elemento
`for letra in "ORCO":` ejecuta el bloque una vez por cada letra. **No es un
contador**: recorre los elementos de una secuencia (textos, y en 06–07 listas,
diccionarios…).

Para repetir **N veces** o recorrer números se usa `range`:
| Llamada | Genera |
|---|---|
| `range(3)` | 0, 1, 2 |
| `range(1, 4)` | 1, 2, 3 (el final **no** se incluye) |
| `range(10, 0, -3)` | 10, 7, 4, 1 |

Si no te interesa el número de vuelta, llamá `_` a la variable: `for _ in range(5):`.

#### `break` y `continue`
- `break` **termina** el bucle entero.
- `continue` **saltea** el resto de la vuelta actual y pasa a la siguiente.

#### `for ... else`
El `else` de un bucle se ejecuta **solo si el bucle terminó sin `break`**. Es la
forma de decir "busqué en todos lados y no lo encontré". **El `else` va alineado
con el `for`**, no con el `if` de adentro.

#### `match` / `case`
Compara un valor contra varios casos, en orden:
- `case "norte" | "n":` → uno u otro.
- `case "atacar" if vida > 30:` → una **guarda**: el caso solo aplica si se cumple.
- `case otro:` → **captura** cualquier valor en la variable `otro`.
- `case _:` → cualquier otra cosa, sin guardarla (el "por defecto").

Se ejecuta **solo el primer** caso que coincide.

#### Azar reproducible: `random`
`import random` trae el módulo de números al azar (los módulos se ven en 11).
`random.randint(1, 6)` da un entero entre 1 y 6, **ambos incluidos**.
`random.seed(42)` fija la **semilla**: con la misma semilla, la secuencia "al azar"
es **siempre la misma**. Sirve para repetir una partida o probar un programa.

#### Validar la entrada del usuario (`menu.py`)
El usuario puede escribir cualquier cosa. En vez de dejar que el programa se
rompa, **preguntá de nuevo** hasta recibir algo válido:
```python
cantidad_texto = input("¿Cuántas? ")
while not cantidad_texto.isdigit():
    cantidad_texto = input("Tiene que ser un número. ¿Cuántas? ")
```
El **operador morsa** `:=` asigna un valor y a la vez lo usa en la condición:
`while (opcion := input("> ")) != "0":` lee la opción, la guarda y la compara.

### Código de ejemplo

```python
"""05 - Control de flujo: decidir (if, match) y repetir (while, for).

Un BLOQUE es el grupo de lineas indentadas (4 espacios) debajo de una linea
que termina en ':'. El bloque se ejecuta o se repite segun la condicion.
"""

import random   # 'import' trae herramientas extra de Python (se ve en 11)

# =========================================================
# if / elif / else: elegir UN camino
# =========================================================
vida = 35
if vida <= 0:
    estado = "caída"
elif vida < 30:
    estado = "crítica"
elif vida < 70:
    estado = "herida"
else:
    estado = "sana"
print(f"vida {vida} -> {estado}")

# Se revisan en orden y se ejecuta SOLO el primero que se cumple.

# Un if dentro de otro (anidado)
tiene_llave = True
cofre_con_trampa = True
if tiene_llave:
    print("abrís el cofre...")
    if cofre_con_trampa:
        print("  ¡una aguja envenenada!")
else:
    print("el cofre está cerrado")

# La condicion puede ser cualquier valor: se usa su "verdad" (visto en 02)
nombre_del_gremio = ""
if not nombre_del_gremio:
    print("todavía no te uniste a ningún gremio")

# Expresion condicional (if en una linea): valor_si_si if condicion else valor_si_no
oro = 12
mensaje = "podés pagar la posada" if oro >= 5 else "dormís afuera"
print(mensaje)

# =========================================================
# while: repetir MIENTRAS la condicion sea verdadera
# =========================================================
antorchas = 3
while antorchas > 0:
    print(f"quedan {antorchas} antorchas")
    antorchas -= 1          # si no cambia nada, el bucle nunca termina
print("oscuridad total")

# =========================================================
# for: repetir UNA VEZ POR CADA elemento de una secuencia
# =========================================================
for letra in "ORCO":        # un texto es una secuencia de letras
    print("letra:", letra)

# range genera una secuencia de numeros
for turno in range(3):              # 0, 1, 2  (el final no se incluye)
    print("turno", turno)
for nivel in range(1, 4):           # 1, 2, 3
    print("nivel", nivel)
for cuenta in range(10, 0, -3):     # 10, 7, 4, 1  (paso negativo: hacia atras)
    print("cuenta", cuenta)

# Bucles anidados: por cada fila, todas las columnas
for fila in range(1, 4):
    linea = ""
    for columna in range(1, 4):
        linea += f"{fila * columna:4}"
    print(linea)

# =========================================================
# break y continue
# =========================================================
for sala in range(1, 8):
    if sala == 2:
        print(f"sala {sala}: vacía, seguís de largo")
        continue            # saltea el resto de ESTA vuelta
    if sala == 5:
        print(f"sala {sala}: ¡el jefe! salís del laberinto")
        break               # termina el bucle entero
    print(f"sala {sala}: explorada")

# =========================================================
# for ... else: el else corre si el bucle NO termino con break
# ("busque en todos lados y no lo encontre")
# =========================================================
buscado = "Z"
for letra in "SLIME":
    if letra == buscado:
        print(f"'{buscado}' encontrada")
        break
else:                       # alineado con el 'for', NO con el 'if'
    print(f"'{buscado}' no está en SLIME")

# =========================================================
# match: comparar un valor contra varios casos
# =========================================================
for comando in "norte n atacar huir bailar".split():   # split() visto en 04
    match comando:
        case "norte" | "n":                 # | = "o este o este"
            accion = "caminás hacia el norte"
        case "atacar" if vida > 30:         # guarda: el caso solo aplica si se cumple el if
            accion = "atacás con la espada"
        case "atacar":
            accion = "estás muy débil para atacar"
        case "huir":
            accion = "escapás"
        case otro:                          # captura cualquier otro valor en 'otro'
            accion = f"no conocés el comando '{otro}'"
    print(f"{comando:>7} -> {accion}")

# =========================================================
# random: azar reproducible con una semilla
# =========================================================
random.seed(42)             # misma semilla -> misma secuencia de "azar" siempre
tiradas = ""
for _ in range(10):         # '_' = no me interesa el numero de vuelta
    tiradas += str(random.randint(1, 6)) + " "
print("tiradas del dado:", tiradas.strip())

# Combate hasta que alguien cae
vida_kira = 20
vida_goblin = 15
ronda = 1
while vida_kira > 0 and vida_goblin > 0:
    golpe = random.randint(3, 7)
    vida_goblin -= golpe
    # max(a, b) devuelve el mayor: asi la vida no se muestra negativa
    print(f"ronda {ronda}: Kira pega {golpe}, goblin queda en {max(vida_goblin, 0)}")
    if vida_goblin <= 0:
        break
    golpe = random.randint(1, 5)
    vida_kira -= golpe
    print(f"          goblin pega {golpe}, Kira queda en {max(vida_kira, 0)}")
    ronda += 1
print("gana Kira" if vida_kira > 0 else "gana el goblin")
```

### Salida esperada

```
vida 35 -> herida
abrís el cofre...
  ¡una aguja envenenada!
todavía no te uniste a ningún gremio
podés pagar la posada
quedan 3 antorchas
quedan 2 antorchas
quedan 1 antorchas
oscuridad total
letra: O
letra: R
letra: C
letra: O
turno 0
turno 1
turno 2
nivel 1
nivel 2
nivel 3
cuenta 10
cuenta 7
cuenta 4
cuenta 1
   1   2   3
   2   4   6
   3   6   9
sala 1: explorada
sala 2: vacía, seguís de largo
sala 3: explorada
sala 4: explorada
sala 5: ¡el jefe! salís del laberinto
'Z' no está en SLIME
  norte -> caminás hacia el norte
      n -> caminás hacia el norte
 atacar -> atacás con la espada
   huir -> escapás
 bailar -> no conocés el comando 'bailar'
tiradas del dado: 6 1 1 6 3 2 2 2 6 1
ronda 1: Kira pega 7, goblin queda en 8
          goblin pega 1, Kira queda en 19
ronda 2: Kira pega 7, goblin queda en 1
          goblin pega 4, Kira queda en 15
ronda 3: Kira pega 3, goblin queda en 0
gana Kira
```

### ¿Para qué sirve?

Todo programa que "piensa" usa decisiones y bucles: un cajero automático repite el menú hasta que elegís salir, una app valida tu clave hasta que sea correcta, un sistema de alarmas revisa sensores cada segundo y decide si sonar. Recorrer una lista de ventas para sumar las del mes, o reintentar una conexión tres veces antes de rendirse, son bucles con `break`.

### Errores habituales

**Slime: olvidar los `:`**:
```
    if vida < 30
                ^
SyntaxError: expected ':'
```

**Slime: bloque sin indentar**:
```
    print("¡cuidado!")
    ^
IndentationError: expected an indented block after 'if' statement on line 1
```

**Ogros (corre, pero hace otra cosa):**
- **Bucle infinito**: un `while` cuya condición nunca cambia. Cortalo con Ctrl+C
  y revisá qué variable debería modificarse dentro del bucle.
- **`elif` en el orden equivocado**: si `vida < 70` va antes que `vida < 30`, el
  segundo nunca se ejecuta.
- **`else` del `for` mal indentado**: si queda alineado con el `if`, se ejecuta en
  **cada** vuelta que no coincide (este era un bug real de una versión anterior
  de este ejemplo).
- **`range(1, 10)` no incluye el 10.**
- **Error por uno** (*off-by-one*): dar una vuelta de más o de menos. Probá los
  bordes: la primera y la última vuelta.

### Micro-misión R01-N04-P1 · Sala 1: trampa o cofre

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: if / elif / else | se revisan en orden y corre SOLO el primero que se cumple · el bloque va indentado
recompensa: xp 10, oro 10
```

#### Escena
La primera sala es un cuadrado de piedra con tres baldosas brillantes en el piso. La runa de la puerta dice: *«Pisá la que te convenga.»*
Gheco olfatea.
—Si la baldosa tiene trampa, esquivala. Si no, y tiene un cofre, abrilo. Y si no hay nada… seguí caminando. Una sola decisión, Mia, en orden.

#### Gheco sugiere
`if` pregunta; si se cumple, corre su bloque (las líneas con sangría debajo). `elif` es «si no, ¿y esto?», y `else` es «en cualquier otro caso». Python revisa en orden y ejecuta **solo el primero** que se cumple.

#### Desafío
Completá la decisión para la baldosa del medio, que no tiene trampa pero sí cofre.

#### Código inicial
```python
trampa = False
cofre = True
if trampa:
    print("¡Esquivás la trampa!")
___ cofre:
    print("Abrís el cofre: 15 de oro.")
___:
    print("Seguís caminando.")
```

#### Salida esperada
```
Abrís el cofre: 15 de oro.
```

#### Solución
```python
trampa = False
cofre = True
if trampa:
    print("¡Esquivás la trampa!")
elif cofre:
    print("Abrís el cofre: 15 de oro.")
else:
    print("Seguís caminando.")
```

#### Al superarla
El cofre se abre con un chasquido y la puerta de la sala 1 se corre. Detrás, oscuridad total.

#### Imagen
- Una sala cuadrada de piedra con tres baldosas brillantes; un cofre abierto sobre la del medio.
- Mia de pie al lado, con el pergamino donde brillan `if`, `elif` y `else` como tres caminos.
- Gheco ilumina la sala con su propio brillo cian.

### Micro-misión R01-N04-P2 · Sala 2: hasta ver la luz

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: while | repite MIENTRAS se cumpla · lo de adentro tiene que cambiar la condición (o no termina nunca)
recompensa: xp 10, oro 10
```

#### Escena
La segunda sala es un pasillo oscuro. No se ve el final. La runa dice: *«Avanzá mientras no veas la luz.»*
—No sabemos cuántos pasos son —dice Gheco—. Pero sí sabemos **cuándo frenar**.

#### Gheco sugiere
`while condicion:` repite su bloque **mientras** la condición sea verdadera. Adentro algo tiene que cambiar para que alguna vez deje de cumplirse; si no, el bucle no termina nunca (y la plataforma lo corta a los 5 segundos).

#### Desafío
La luz aparece cuando la distancia llega a 0. Cada paso acorta 3 metros. Completá la condición y el paso.

#### Código inicial
```python
distancia = 12
pasos = 0
while ___:
    distancia ___ 3
    pasos += 1
    print(f"Paso {pasos}: faltan {distancia} m")
print("¡Se ve la luz!")
```

#### Salida esperada
```
Paso 1: faltan 9 m
Paso 2: faltan 6 m
Paso 3: faltan 3 m
Paso 4: faltan 0 m
¡Se ve la luz!
```

#### Solución
```python
distancia = 12
pasos = 0
while distancia > 0:
    distancia -= 3
    pasos += 1
    print(f"Paso {pasos}: faltan {distancia} m")
print("¡Se ve la luz!")
```

#### Al superarla
Al cuarto paso, una línea de luz verde aparece en el piso y marca la puerta de la sala 3.

#### Imagen
- Un pasillo de piedra oscurísimo; Mia avanza con una mano en la pared.
- Gheco ilumina apenas un metro adelante.
- Al fondo, una línea de luz verde en el piso marca la salida.

### Micro-misión R01-N04-P3 · Salas 3 y 4: contar las losas

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: for y range | for x in secuencia: · range(5) → 0..4 · range(1, 6) → 1..5 · range(0, 10, 2) de 2 en 2
recompensa: xp 10, oro 10
```

#### Escena
La tercera sala tiene cinco losas numeradas y la runa dice: *«Pisá cada una, en orden, y decí su número.»* La cuarta tiene losas solo en los números pares hasta el 8.
—Acá sí sabemos cuántas son —dice Gheco—. Eso es trabajo para `for`.

#### Gheco sugiere
`for x in range(1, 6):` repite **una vez por cada número** del 1 al 5 (el último no entra). `range(0, 9, 2)` va de 2 en 2: 0, 2, 4, 6, 8. Usá `for` cuando sabés cuántas vueltas hay, y `while` cuando no.

#### Desafío
Completá los dos `range`. En la sala 4, mostrá los números en una sola línea separados por espacio.

#### Código inicial
```python
for losa in range(___):
    print(f"Losa {losa}")
for losa in range(___):
    print(losa, end=" ")
print()
```

#### Salida esperada
```
Losa 1
Losa 2
Losa 3
Losa 4
Losa 5
0 2 4 6 8 
```

#### Solución
```python
for losa in range(1, 6):
    print(f"Losa {losa}")
for losa in range(0, 9, 2):
    print(losa, end=" ")
print()
```

#### Al superarla
Las losas se encienden una tras otra, como teclas de un piano de piedra. Dos puertas se abren seguidas.

#### Imagen
- Un piso de losas numeradas que se encienden en secuencia bajo los pies de Mia.
- Gheco salta de losa par en losa par.
- Números de luz flotan sobre cada losa.

### Micro-misión R01-N04-P4 · Sala 5: el jefe y la salida

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
criatura: ogro
carta: break y continue | break corta el bucle · continue salta a la vuelta siguiente · for…else: el else corre si no hubo break
recompensa: xp 15, oro 15
```

#### Escena
La quinta sala tiene seis puertas numeradas. Gheco escucha detrás de cada una: la 2 y la 4 están vacías, y detrás de la 5 ronca un **ogro**. La runa dice: *«Revisá las puertas en orden. Las vacías, salteálas. Si llegás al ogro, no pelees: salí corriendo.»*
—Y si revisamos todas y no está… —susurra Gheco— mejor todavía.

#### Gheco sugiere
Dentro de un bucle, `continue` **salta** directo a la vuelta siguiente, y `break` **corta** el bucle entero. Un `for` puede tener `else`: corre **solo si el bucle terminó sin `break`** («busqué en todos lados y no estaba»).

#### Desafío
Las vacías (2 y 4) se saltean con `continue`; en la del ogro (5), `break`. Completá.

#### Código inicial
```python
for puerta in range(1, 7):
    if puerta == 2 or puerta == 4:
        ___
    if puerta == 5:
        print(f"Puerta {puerta}: ¡el ogro! A correr.")
        ___
    print(f"Puerta {puerta}: un cofre")
else:
    print("No había ningún ogro.")
```

#### Salida esperada
```
Puerta 1: un cofre
Puerta 3: un cofre
Puerta 5: ¡el ogro! A correr.
```

#### Solución
```python
for puerta in range(1, 7):
    if puerta == 2 or puerta == 4:
        continue
    if puerta == 5:
        print(f"Puerta {puerta}: ¡el ogro! A correr.")
        break
    print(f"Puerta {puerta}: un cofre")
else:
    print("No había ningún ogro.")
```

#### Al superarla
Salís de la sala 5 sin hacer ruido, con el corazón en la garganta. El ogro ronca detrás de la puerta 5 y no se entera de nada. La puerta 6 queda sin abrir… y no importa.

#### Imagen
- Seis puertas de piedra en semicírculo; detrás de la quinta, entreabierta, se ve la sombra de un ogro enorme dormido.
- Mia y Gheco en puntas de pie, alejándose con el dedo en los labios.

### Micro-misión R01-N04-P5 · Sala 6: la puerta de los comandos

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: match / case | match valor: case "a": … case "b" | "c": … case _: (cualquier otro)
recompensa: xp 15, oro 15
```

#### Escena
La sexta puerta no tiene picaporte: tiene una **boca de piedra** que espera una palabra. Al lado, grabado: *«norte», «sur», «este» u «oeste». Cualquier otra cosa: la boca se ríe.*
—Es como un menú —dice Gheco—. Para cada palabra, una respuesta.

#### Gheco sugiere
`match` compara un valor contra varios casos y corre el primero que coincide. `case "este" | "oeste":` acepta cualquiera de los dos, y `case _:` es «cualquier otra cosa». Es más claro que una cadena larga de `elif`.

#### Desafío
La salida está al norte. Completá los casos.

#### Código inicial
```python
orden = input("¿Hacia dónde? ")
match orden:
    case "norte":
        print("La boca se abre: ¡la salida!")
    case "sur":
        print("Volvés por donde viniste.")
    case ___:
        print("Un muro. Probá otra dirección.")
    case ___:
        print("La boca se ríe de vos.")
```

#### Entrada
```
norte
```

#### Salida esperada
```
¿Hacia dónde? La boca se abre: ¡la salida!
```

#### Solución
```python
orden = input("¿Hacia dónde? ")
match orden:
    case "norte":
        print("La boca se abre: ¡la salida!")
    case "sur":
        print("Volvés por donde viniste.")
    case "este" | "oeste":
        print("Un muro. Probá otra dirección.")
    case _:
        print("La boca se ríe de vos.")
```

#### Al superarla
La boca de piedra se abre de par en par. Detrás, la última sala: una mesa redonda con **dos dados de hueso** y una runa más.

#### Imagen
- Una enorme boca de piedra en la pared que se abre; adentro, luz.
- Cuatro direcciones grabadas alrededor como una rosa de los vientos; «norte» brilla.
- Mia de pie frente a ella; Gheco cubre la cabeza por las dudas.

### Micro-misión R01-N04-P6 · Sala 7: los dados de la salida

```meta
lugar: El Laberinto de las Siete Salas
personajes: Mia, Gheco
carta: Azar reproducible | import random · random.seed(7) · random.randint(1, 6) · misma semilla → mismos números
recompensa: xp 15, oro 20
item: Espiral de Junco
se abre: el primer ítem que sirve en el juego: la Espiral de Junco (+2 vueltas en las expediciones, cuando se abran)
```

#### Escena
En la mesa hay dos dados y una runa: *«Tirá tres veces. Si la suma pasa de 8, el Laberinto te deja salir.»*
—¿Y si sale poco? —preguntás.
Gheco señala un número diminuto grabado en el borde de la mesa: **7**.
—Pista: estos dados están **hechizados con una semilla**. Con la misma semilla, siempre sale lo mismo. Así se prueban los programas con azar.

#### Gheco sugiere
`import random` trae la herramienta del azar. `random.randint(1, 6)` da un número entre 1 y 6 (los dos incluidos). Si antes llamás a `random.seed(7)`, la secuencia es **siempre la misma**: ideal para probar un programa.

#### Desafío
Fijá la semilla 7, tirá tres dados, mostralos y decí si salís.

#### Código inicial
```python
import random
___
dado1 = random.randint(1, 6)
dado2 = random.randint(1, 6)
dado3 = random.randint(1, 6)
suma = dado1 + dado2 + dado3
print(f"Tiradas: {dado1} {dado2} {dado3} · suma {suma}")
if suma > 8:
    print("¡Salís del Laberinto!")
else:
    print("Seguís adentro.")
```

#### Salida esperada
```
Tiradas: 3 2 4 · suma 9
¡Salís del Laberinto!
```

#### Solución
```python
import random
random.seed(7)
dado1 = random.randint(1, 6)
dado2 = random.randint(1, 6)
dado3 = random.randint(1, 6)
suma = dado1 + dado2 + dado3
print(f"Tiradas: {dado1} {dado2} {dado3} · suma {suma}")
if suma > 8:
    print("¡Salís del Laberinto!")
else:
    print("Seguís adentro.")
```

#### Al superarla
Los dados se quedan quietos y el piso de la sala gira despacio, como una escalera de caracol. Te deja afuera, en la ladera, bajo las estrellas. En la mesa quedó, enrollado, un **junco con forma de espiral**: lo guardás.
Ya es de noche y estás agotada. Allá abajo, junto al puente viejo, se ven las luces de **la Posada de la Serpiente**.

#### Imagen
- Una mesa redonda de piedra con dos dados de hueso; el número 7 grabado en el borde.
- El piso de la sala gira como una escalera de caracol de luz.
- Afuera, desde la ladera de noche, se ven las luces cálidas de la Posada de la Serpiente junto al río.
- Mia sostiene un junco enrollado en espiral; Gheco bosteza.

### Misión R01-N04-M1 · El ritmo de la forja

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Del 1 al 30, mostrá `Martillo` si el número es
múltiplo de 3, `Yunque` si es de 5, `MartilloYunque` si es de ambos, y el
número si no es de ninguno.

#### Criterio de aprobación

- Recorre del 1 al 30 con `for` y `range`.
- Revisa primero el caso de múltiplo de 3 **y** de 5.
- Muestra Martillo, Yunque, MartilloYunque o el número, según corresponda.

#### Salida esperada

```
1
2
Martillo
4
Yunque
Martillo
7
8
Martillo
Yunque
11
Martillo
13
14
MartilloYunque
16
17
Martillo
19
Yunque
Martillo
22
23
Martillo
Yunque
26
Martillo
28
29
MartilloYunque
```

#### Solución de referencia

```python
"""Mision 1 - El ritmo de la forja (el clasico FizzBuzz).

Del 1 al 30: multiplo de 3 -> "Martillo", de 5 -> "Yunque", de ambos -> "MartilloYunque".
Ojo con el ORDEN: el caso "de ambos" tiene que ir primero.
"""

for n in range(1, 31):
    if n % 3 == 0 and n % 5 == 0:
        print("MartilloYunque")
    elif n % 3 == 0:
        print("Martillo")
    elif n % 5 == 0:
        print("Yunque")
    else:
        print(n)
```

### Misión R01-N04-M2 · Combate con pociones

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Kira (30 de vida, 2 pociones) pelea contra un orco
(40 de vida). En su turno, si tiene menos de 10 de vida y le quedan pociones,
toma una (+15); si no, ataca con `randint(4, 9)`. El orco pega con
`randint(3, 8)`. Usá `random.seed(7)` para que siempre salga igual.

#### Criterio de aprobación

- Usa `random.seed(7)` para que el combate salga siempre igual.
- El bucle sigue mientras los dos tengan vida.
- Toma poción solo con menos de 10 de vida y si le quedan; si no, ataca.
- Muestra quién gana.

#### Salida esperada

```
turno 1: Kira pega 6 -> orco 34
         orco pega 4 -> Kira 26
turno 2: Kira pega 7 -> orco 27
         orco pega 8 -> Kira 18
turno 3: Kira pega 4 -> orco 23
         orco pega 3 -> Kira 15
turno 4: Kira pega 8 -> orco 15
         orco pega 3 -> Kira 12
turno 5: Kira pega 6 -> orco 9
         orco pega 7 -> Kira 5
turno 6: Kira toma una poción -> vida 20 (quedan 1)
         orco pega 3 -> Kira 17
turno 7: Kira pega 8 -> orco 1
         orco pega 4 -> Kira 13
turno 8: Kira pega 4 -> orco 0
¡Victoria!
```

#### Solución de referencia

```python
"""Mision 2 - Combate con pociones.

Kira (30 de vida, 2 pociones) contra un orco (40 de vida). Si en su turno
Kira tiene menos de 10 de vida y le quedan pociones, toma una (+15) en vez de atacar.
"""

import random

random.seed(7)
vida_kira = 30
vida_orco = 40
pociones = 2
turno = 1

while vida_kira > 0 and vida_orco > 0:
    if vida_kira < 10 and pociones > 0:
        pociones -= 1
        vida_kira += 15
        print(f"turno {turno}: Kira toma una poción -> vida {vida_kira} (quedan {pociones})")
    else:
        golpe = random.randint(4, 9)
        vida_orco -= golpe
        print(f"turno {turno}: Kira pega {golpe} -> orco {max(vida_orco, 0)}")
        if vida_orco <= 0:
            break
    golpe = random.randint(3, 8)
    vida_kira -= golpe
    print(f"         orco pega {golpe} -> Kira {max(vida_kira, 0)}")
    turno += 1

print("¡Victoria!" if vida_kira > 0 else "Kira cae... fin de la partida")
```

### Misión R01-N04-M3 · El acertijo de la serpiente

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Elegí un número secreto del 1 al 50 con
`random.seed(2026)` y `randint`. Pedile números al usuario hasta que acierte,
diciéndole "más alto" o "más bajo". Rechazá lo que no sea un número, contá los
intentos y dejá que escriba `me rindo` para terminar.

#### Criterio de aprobación

- Elige el número con `random.seed(2026)` y `randint(1, 50)`.
- Rechaza lo que no sea un número sin cortar el programa.
- Dice "más alto" o "más bajo", cuenta los intentos y acepta `me rindo`.

#### Entrada de ejemplo

```
25
mucho
4
10
8
```

#### Salida esperada

```
Tu número (o 'me rindo'):   Más bajo.
Tu número (o 'me rindo'):   Eso no es un número.
Tu número (o 'me rindo'):   Más alto.
Tu número (o 'me rindo'):   Más bajo.
Tu número (o 'me rindo'): ¡Correcto! Lo adivinaste en 4 intentos.
```

#### Solución de referencia

```python
"""Mision 3 - El acertijo de Ofidia: adivinar un numero del 1 al 50.

Pide numeros hasta acertar, avisa si es mayor o menor, rechaza lo que no sea
numero y cuenta los intentos. Si el usuario escribe 'me rindo', termina.
"""

import random

random.seed(2026)
secreto = random.randint(1, 50)
intentos = 0

while True:
    texto = input("Tu número (o 'me rindo'): ").strip().lower()
    if texto == "me rindo":
        print(f"El número era {secreto}.")
        break
    if not texto.isdigit():
        print("  Eso no es un número.")
        continue
    intentos += 1
    numero = int(texto)
    if numero < secreto:
        print("  Más alto.")
    elif numero > secreto:
        print("  Más bajo.")
    else:
        print(f"¡Correcto! Lo adivinaste en {intentos} intentos.")
        break
```

#### Pruebas

##### Se rinde
```entrada
10
me rindo
```
```salida
Tu número (o 'me rindo'):   Más bajo.
Tu número (o 'me rindo'): El número era 8.
```

##### Muchos inválidos
```entrada
x
51
0
4
10
8
```
```salida
Tu número (o 'me rindo'):   Eso no es un número.
Tu número (o 'me rindo'):   Más bajo.
Tu número (o 'me rindo'):   Más alto.
Tu número (o 'me rindo'):   Más alto.
Tu número (o 'me rindo'):   Más bajo.
Tu número (o 'me rindo'): ¡Correcto! Lo adivinaste en 5 intentos.
```

### Encargo R01-N04-E1 · El vuelto del cajero

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El cajero del mercado tiene que dar el vuelto con la **menor cantidad de
billetes** posible. Para un precio de $3270 pagado con $10000, mostrá cuántos
billetes de 1000, 500, 200, 100, 50, 20 y 10 entrega. Pista: `//` da cuántos
billetes entran y `%` lo que queda.

#### Criterio de aprobación

- Calcula el vuelto (6730) y recorre la lista de billetes con un bucle.
- Usa `//` para la cantidad de cada billete y `%` para lo que resta.
- Muestra solo los billetes que se entregan.

#### Salida esperada

```
Vuelto: $6730
  6 x $1000
  1 x $500
  1 x $200
  1 x $20
  1 x $10
```

#### Solución de referencia

```python
"""Encargo del Gremio - El cajero del mercado: dar el vuelto con la menor
cantidad de billetes posible.
"""

precio = 3270
pago = 10000
vuelto = pago - precio
print(f"Vuelto: ${vuelto}")

for texto in "1000 500 200 100 50 20 10".split():
    billete = int(texto)
    cantidad = vuelto // billete
    if cantidad > 0:
        print(f"  {cantidad} x ${billete}")
        vuelto = vuelto % billete

if vuelto > 0:
    print(f"  (quedan ${vuelto} en monedas)")
```

### Prueba del sello

#### ¿Qué números genera `range(2, 11, 3)`?

`2, 5, 8`: arranca en 2, suma 3 y se detiene antes de 11.

#### ¿Qué diferencia hay entre `break` y `continue`?

`break` **termina** el bucle; `continue` saltea lo que falta de esa vuelta y pasa a la siguiente.

#### ¿Cuándo se ejecuta el `else` de un `for`?

Cuando el `for` termina **sin** haber pasado por un `break`.

#### En un `match`, ¿qué diferencia hay entre `case _:` y `case otro:`?

`case _:` atrapa cualquier valor sin guardarlo; `case otro:` también atrapa cualquier valor, pero lo guarda en la variable `otro`.

#### ¿Para qué sirve `random.seed(...)`?

Para que los números "al azar" salgan siempre iguales: sirve para probar y comparar resultados.

#### ¿Cómo harías para pedir un número hasta que el usuario escriba uno válido?

Con un `while True:` que pide el dato, intenta convertirlo y hace `break` solo cuando la conversión funciona (por ejemplo, revisando con `.isdigit()` o con `try`/`except`).

### Soluciones (docente)

Material original: `17-Python/05-Control` (soluciones completas en `soluciones/`).

La misión 3 usa la pestaña Entrada: la de ejemplo prueba un texto inválido y "más alto/más bajo". Si ya vieron `try`/`except` por su cuenta, aceptarlo; el tema formal está en R02.

## R01-N05 · Listas y tuplas

```meta
tipo: tema
padre: R01-N04
precio: 10
criatura: orco
temas: col.listas, col.registros, col.matrices
```

### Crónica

Ya no viajás sin compañía: Bron, Mia y Zed se sumaron. Hay que llevar la cuenta de quién está, qué hay en la mochila, el ranking del torneo y el mapa de cada mazmorra.

—Para guardar **muchos** valores juntos —dice {mentor}—, el Valle tiene dos caravanas: la **lista**, que carga y descarga en cada pueblo, y la **tupla**, sellada con cera: lo que entra, no cambia.

### Objetivos

Guardar varios valores en una lista o en una tupla, modificarlos, ordenarlos,
recorrerlos, armar listas nuevas con *comprehensions*, manejar listas de listas
(mapas) y desempaquetar.

### Antes de empezar

- Índices y slicing en textos (04): funcionan igual en listas y tuplas.
- `for`, `if` y `match` (05).

### Explicación

#### Listas: `[...]`
Una **lista** es una secuencia **ordenada** y **modificable**:
`compania = ["Kira", "Bron", "Mia"]`. Se accede por índice (`compania[0]`,
`compania[-1]`), se corta (`compania[:2]`), se mide con `len` y se pregunta con
`in`, igual que un texto. `list("abc")` convierte un texto en la lista de sus
letras: `['a', 'b', 'c']`.

#### Métodos que modifican la lista
| Método | Hace |
|---|---|
| `lista[i] = x` | reemplaza el elemento de la posición `i` |
| `append(x)` | agrega `x` al final |
| `insert(i, x)` | inserta `x` en la posición `i` |
| `extend(otra)` o `+= otra` | agrega todos los elementos de `otra` |
| `remove(x)` | saca el **primer** `x` (error si no está) |
| `pop()` / `pop(i)` | saca y **devuelve** el último / el de la posición `i` |
| `sort()` / `sort(reverse=True)` | ordena la **misma** lista |
| `reverse()` | la invierte |
| `clear()` | la vacía |

Y los que solo consultan: `count(x)` (cuántas veces aparece), `index(x)` (en qué
posición está), más las funciones `len`, `min`, `max` y `sum`.

#### `sort()` o `sorted()`
- `lista.sort()` **modifica** la lista y **devuelve `None`**.
- `sorted(lista)` **no la toca** y devuelve una **lista nueva** ordenada.
- Las dos aceptan `reverse=True` y `key=función` (el criterio de orden, a fondo
  en 10). `key=str.lower` ordena sin distinguir mayúsculas.

#### Recorrer
- `for x in lista:` da cada elemento.
- `for i, x in enumerate(lista, start=1):` da la **posición y el elemento** en
  cada vuelta. Es mucho mejor que `for i in range(len(lista))`.

#### List comprehensions
La forma corta de armar una lista **a partir de otra**:
```python
[expresión  for elemento in secuencia  if condición]
dobles  = [d * 2 for d in danios]
fuertes = [d for d in danios if d >= 10]
```
Es lo mismo que un `for` con `append`, en una línea. Si queda muy larga o
difícil de leer, usá el `for` normal.

#### Listas anidadas: mapas y tablas
Una lista puede contener listas: `mapa[fila][columna]`. Es la forma natural de
representar un tablero, un mapa o una matriz. Para recorrerla, un `for` dentro de
otro (05).

#### Tuplas: `(...)`
Como una lista, pero **inmutable**: no se puede agregar, sacar ni cambiar
elementos. Se usan para datos que van juntos y no cambian: coordenadas
`(x, y)`, colores `(r, g, b)`, o un registro `(puntos, nombre)`.
- **La coma hace la tupla**, no los paréntesis: `(42,)` es una tupla;
  `(42)` es solo el número 42. `3, 7` también es una tupla.
- Las tuplas **se comparan elemento por elemento**: `(95, "Bron") > (95, "Ana")`,
  porque empatan en 95 y `"Bron"` > `"Ana"`. Por eso ordenar tuplas
  `(puntos, nombre)` ordena por puntos y desempata por nombre.

**¿Lista o tupla?** Si la colección **crece o cambia**, lista. Si es un
**registro fijo** de pocos valores, tupla. Además, las tuplas pueden ser claves
de diccionario (07) y las listas no.

#### Desempaquetado
Repartir los elementos de una secuencia en variables:
- `x, y = posicion` (tiene que haber tantas variables como elementos).
- `a, b = b, a` intercambia dos variables.
- `primero, *resto = lista`: el `*` junta en una lista "lo que sobra".
- En un `for`: `for nombre, nivel in [("Kira", 3), ("Bron", 5)]:`.
- Anidado: `for i, (puntos, nombre) in enumerate(ranking):`.

#### `match` con secuencias
`match` puede reconocer la **forma** de una tupla o lista y desempaquetarla:
```python
match orden:
    case ("mover", dx, dy):   # tres elementos y el primero es "mover"
    case ("atacar", objetivo):
    case ("descansar",):
```

### Código de ejemplo

```python
"""06 - Listas y tuplas: secuencias de valores.

list  -> secuencia que se puede MODIFICAR (agregar, sacar, cambiar).
tuple -> secuencia que NO se puede modificar (inmutable).
Las dos se indexan y se cortan igual que los textos (04).
"""

# =========================================================
# Crear listas y acceder por indice
# =========================================================
compania = ["Kira", "Bron", "Mia"]
vacia = []
mezcla = ["Kira", 3, 12.5, True]        # puede mezclar tipos (mejor no abusar)
print(compania, vacia, mezcla)
print("cantidad:", len(compania))
print("primera:", compania[0], "- última:", compania[-1])
print("las dos primeras:", compania[:2])

# =========================================================
# Modificar una lista
# =========================================================
compania[1] = "Bron el Enano"           # reemplazar por indice
compania.append("Zed")                  # agregar al final
compania.insert(0, "Ofidia")            # insertar en una posicion
print("después de agregar:", compania)

compania.remove("Ofidia")               # sacar por VALOR (el primero que encuentre)
ultimo = compania.pop()                 # sacar el ultimo y devolverlo
print("salió:", ultimo, "->", compania)
segundo = compania.pop(1)               # sacar por POSICION
print("salió:", segundo, "->", compania)

botin = ["poción", "llave"]
botin.extend(["gema", "gema"])          # agregar VARIOS (de otra lista)
botin += ["mapa"]                       # lo mismo con +=
print("botín:", botin)
print("¿cuántas gemas?", botin.count("gema"))
print("¿dónde está la llave?", botin.index("llave"))
print("¿hay mapa?", "mapa" in botin)

# =========================================================
# Ordenar: sort() cambia la lista; sorted() devuelve una NUEVA
# =========================================================
puntajes = [120, 45, 300, 87, 210]
ordenados = sorted(puntajes)            # nueva lista; 'puntajes' no cambia
print("sorted:", ordenados, "| original:", puntajes)
puntajes.sort(reverse=True)             # ordena la MISMA lista (de mayor a menor)
print("sort(reverse=True):", puntajes)
print("top 3:", puntajes[:3])
print("min / max / suma:", min(puntajes), max(puntajes), sum(puntajes))

nombres = ["zed", "Kira", "bron", "Mia"]
print("sorted:", sorted(nombres))                   # mayusculas primero (03)
# key= recibe una FUNCION que dice por que valor ordenar (se ve a fondo en 10)
print("sin distinguir mayúsculas:", sorted(nombres, key=str.lower))

# =========================================================
# Recorrer
# =========================================================
for nombre in compania:
    print("en la compañía:", nombre)

# enumerate da la posicion Y el valor en cada vuelta
for i, item in enumerate(botin, start=1):
    print(f"  {i}. {item}")

# =========================================================
# List comprehension: armar una lista nueva desde otra, en una linea
#   [expresion  for elemento in secuencia  if condicion]
# =========================================================
danios = [12, 3, 25, 8, 17]
dobles = [d * 2 for d in danios]
fuertes = [d for d in danios if d >= 10]
etiquetas = [f"{d}!" if d >= 20 else str(d) for d in danios]
print("dobles:", dobles)
print("fuertes:", fuertes)
print("etiquetas:", etiquetas)

# =========================================================
# Listas anidadas: el mapa de una mazmorra (lista de filas)
# =========================================================
mapa = [
    ["#", "#", "#", "#", "#"],
    ["#", "K", ".", "G", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", "#", "#", "#", "#"],
]
print("fila 1:", mapa[1])
print("celda (1, 3):", mapa[1][3])      # mapa[fila][columna]
mapa[2][1] = "P"                        # dejar una pocion
for fila in mapa:
    print("".join(fila))                # join une la fila en un texto (04)
pisos = sum([fila.count(".") for fila in mapa])
print("casillas de piso libres:", pisos)

# =========================================================
# Tuplas: como una lista, pero inmutable
# =========================================================
posicion = (3, 7)
colores = ("rojo", "verde", "azul")
solo_uno = (42,)                        # la COMA hace la tupla, no el parentesis
tambien_tupla = 3, 7                    # los parentesis son opcionales
print(posicion, colores, solo_uno, tambien_tupla, type(solo_uno))
print("x =", posicion[0], "| y =", posicion[1])
# posicion[0] = 9                       # -> TypeError: las tuplas no se modifican

# =========================================================
# Desempaquetado: repartir los elementos en variables
# =========================================================
x, y = posicion
print(f"x={x} y={y}")

a = "espada"
b = "escudo"
a, b = b, a                             # intercambiar sin variable auxiliar
print("intercambio:", a, b)

primero, *resto = [10, 20, 30, 40]      # * junta "lo que sobra" en una lista
print("primero:", primero, "| resto:", resto)
*otros, ultimo = "S", "L", "I", "M", "E"
print("otros:", otros, "| último:", ultimo)

for nombre, nivel in [("Kira", 3), ("Bron", 5)]:   # desempaquetar en el for
    print(f"{nombre} es nivel {nivel}")

# =========================================================
# match con secuencias: reconocer la FORMA de un comando
# =========================================================
for orden in [("mover", 2, -1), ("atacar", "orco"), ("descansar",), ("volar", 1, 2, 3)]:
    match orden:
        case ("mover", dx, dy):
            print(f"te movés {dx} en x y {dy} en y")
        case ("atacar", objetivo):
            print(f"atacás al {objetivo}")
        case ("descansar",):
            print("descansás")
        case _:
            print(f"orden desconocida: {orden}")
```

### Salida esperada

```
['Kira', 'Bron', 'Mia'] [] ['Kira', 3, 12.5, True]
cantidad: 3
primera: Kira - última: Mia
las dos primeras: ['Kira', 'Bron']
después de agregar: ['Ofidia', 'Kira', 'Bron el Enano', 'Mia', 'Zed']
salió: Zed -> ['Kira', 'Bron el Enano', 'Mia']
salió: Bron el Enano -> ['Kira', 'Mia']
botín: ['poción', 'llave', 'gema', 'gema', 'mapa']
¿cuántas gemas? 2
¿dónde está la llave? 1
¿hay mapa? True
sorted: [45, 87, 120, 210, 300] | original: [120, 45, 300, 87, 210]
sort(reverse=True): [300, 210, 120, 87, 45]
top 3: [300, 210, 120]
min / max / suma: 45 300 762
sorted: ['Kira', 'Mia', 'bron', 'zed']
sin distinguir mayúsculas: ['bron', 'Kira', 'Mia', 'zed']
en la compañía: Kira
en la compañía: Mia
  1. poción
  2. llave
  3. gema
  4. gema
  5. mapa
dobles: [24, 6, 50, 16, 34]
fuertes: [12, 25, 17]
etiquetas: ['12', '3', '25!', '8', '17']
fila 1: ['#', 'K', '.', 'G', '#']
celda (1, 3): G
#####
#K.G#
#P#.#
#####
casillas de piso libres: 2
(3, 7) ('rojo', 'verde', 'azul') (42,) (3, 7) <class 'tuple'>
x = 3 | y = 7
x=3 y=7
intercambio: escudo espada
primero: 10 | resto: [20, 30, 40]
otros: ['S', 'L', 'I', 'M'] | último: E
Kira es nivel 3
Bron es nivel 5
te movés 2 en x y -1 en y
atacás al orco
descansás
orden desconocida: ('volar', 1, 2, 3)
```

### ¿Para qué sirve?

Las listas están en todas partes: los productos de un carrito, los mensajes de un chat, las notas de un curso, las canciones de una playlist. Ordenar (`sorted`), filtrar (comprehensions) y sacar promedios son las operaciones que hace cualquier planilla. Las tuplas guardan datos que van juntos y no cambian: una coordenada `(lat, lon)`, una fecha `(día, mes, año)`, un registro `(puntos, nombre)`.

### Errores habituales

**Orco: índice fuera de rango** (`IndexError: list index out of range`). Con 3
elementos, los índices válidos van de 0 a 2 (o de -1 a -3).

**Orco: sacar de una lista vacía** (`IndexError: pop from empty list`).

**Goblin: `remove` de algo que no está** (`ValueError: list.remove(x): x not in
list`). Preguntá antes con `if x in lista:`.

**Troll: modificar una tupla**
(`TypeError: 'tuple' object does not support item assignment`).

**Goblin: desempaquetar con otra cantidad**
(`ValueError: too many values to unpack (expected 2)`).

**Ogros (corre, pero hace otra cosa):**
- `ordenada = lista.sort()` → `ordenada` vale `None`, porque `sort()` no
  devuelve nada. Usá `sorted(lista)`.
- `lista.append(otra_lista)` mete la lista **entera como un solo elemento**. Para
  agregar sus elementos, `extend`.
- Sacar elementos de una lista **mientras la recorrés con `for`** saltea
  elementos. Armá una lista nueva con una comprehension.
- `(42)` no es una tupla: falta la coma.

### Micro-misión R01-N05-P1 · Lo que hay en la mochila

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco
carta: Listas | [a, b, c] · lista[0] primero · lista[-1] último · len(lista)
recompensa: xp 10, oro 10
```

#### Escena
La Posada huele a pan y a río. Te sentás junto al fuego y vaciás la mochila sobre la mesa: el pergamino, la llave del puente y la espiral de junco.
—Anotalo —dice Gheco—. Un aventurero que no sabe qué lleva, no sabe qué puede hacer.

#### Gheco sugiere
Una **lista** guarda varios valores en orden, entre corchetes: `["a", "b"]`. Se cuenta desde 0, igual que en los textos: `lista[0]` es el primero y `lista[-1]`, el último. `len(lista)` dice cuántos hay.

#### Desafío
Mostrá lo primero, lo último y cuántas cosas hay.

#### Código inicial
```python
mochila = ["pergamino", "llave del puente", "espiral de junco"]
print(mochila[___])
print(mochila[___])
print(len(___))
```

#### Salida esperada
```
pergamino
espiral de junco
3
```

#### Solución
```python
mochila = ["pergamino", "llave del puente", "espiral de junco"]
print(mochila[0])
print(mochila[-1])
print(len(mochila))
```

#### Al superarla
Un chico descalzo, con un farol verde en la punta de una pértiga, mira tu mochila desde la mesa de al lado. No deja de mirar el pergamino.

#### Imagen
- Interior cálido de la Posada de la Serpiente: fuego, mesas de madera, faroles verdes.
- Sobre la mesa de Mia: un pergamino, una llave verde y un junco en espiral.
- En la mesa de al lado, Tilo (14, pelo castaño con una hoja enredada, pañuelo verde, pértiga con farol verde) mira con curiosidad.

### Micro-misión R01-N05-P2 · Tilo se suma

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Agregar a una lista | lista.append(x) al final · lista.insert(0, x) al principio
recompensa: xp 10, oro 10
```

#### Escena
—Soy **Tilo** —dice el chico—. Sé todo del río, pero no sé leer las runas. Quiero subir a las Terrazas. ¿Me llevan?
Gheco te mira. Vos mirás la lista de la compañía, que hasta ahora tenía dos nombres.

#### Gheco sugiere
`lista.append(x)` agrega `x` **al final**. La lista cambia ahí mismo: no hace falta volver a asignarla.

#### Desafío
Sumá a Tilo a la compañía.

#### Código inicial
```python
compania = ["Mia", "Gheco"]
___
print(compania)
print(f"Somos {len(compania)}")
```

#### Salida esperada
```
['Mia', 'Gheco', 'Tilo']
Somos 3
```

#### Solución
```python
compania = ["Mia", "Gheco"]
compania.append("Tilo")
print(compania)
print(f"Somos {len(compania)}")
```

#### Al superarla
Tilo sonríe con toda la cara. —¿Y eso para qué sirve? —pregunta, señalando el pergamino. Es la primera de muchas veces que lo va a preguntar.

#### Imagen
- Tilo, de pie, con la pértiga y el farol verde, extiende la mano a Mia.
- Sobre la mesa, el pergamino muestra una lista que crece: Mia, Gheco, Tilo.
- Gheco, sobre el hombro de Mia, desconfiado pero sonriendo.

### Micro-misión R01-N05-P3 · Sacar lo que sobra

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Sacar de una lista | lista.remove(x) por valor · lista.pop() el último · x in lista para preguntar
recompensa: xp 10, oro 10
```

#### Escena
Tilo vacía su bolsa: un anzuelo, una piedra lisa, **otra piedra lisa** y un pan.
—Dos piedras no —dice Gheco—. Pesan.

#### Gheco sugiere
`lista.remove(x)` saca **la primera** aparición de `x` (si no está, da error: preguntá antes con `x in lista`). `lista.pop()` saca y devuelve el último.

#### Desafío
Sacá una de las piedras y comé el pan (el último).

#### Código inicial
```python
bolsa = ["anzuelo", "piedra lisa", "piedra lisa", "pan"]
bolsa.___("piedra lisa")
comido = bolsa.___()
print(f"Te comés: {comido}")
print(bolsa)
```

#### Salida esperada
```
Te comés: pan
['anzuelo', 'piedra lisa']
```

#### Solución
```python
bolsa = ["anzuelo", "piedra lisa", "piedra lisa", "pan"]
bolsa.remove("piedra lisa")
comido = bolsa.pop()
print(f"Te comés: {comido}")
print(bolsa)
```

#### Al superarla
Tilo se guarda la piedra que queda. —Es para hacer sapito en el río —explica, muy serio.

#### Imagen
- Primer plano de la mesa: un anzuelo, un pan y dos piedras lisas; una de ellas se desvanece en partículas.
- Tilo masticando el pan; Mia anotando en el pergamino.

### Micro-misión R01-N05-P4 · El orden de la guardia

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Ordenar | lista.sort() cambia la lista · sorted(lista) devuelve una nueva · reverse=True al revés
recompensa: xp 10, oro 10
```

#### Escena
Para dormir tranquilos, alguien tiene que hacer guardia. Deciden ir por orden alfabético… pero Gheco quiere ver también el orden al revés, «por si acaso».

#### Gheco sugiere
`sorted(lista)` devuelve una lista **nueva** ordenada y deja la original como estaba. `lista.sort()` la ordena **ahí mismo**. Las dos aceptan `reverse=True`.

#### Desafío
Mostrá la guardia en orden y al revés, sin cambiar la lista original.

#### Código inicial
```python
compania = ["Tilo", "Mia", "Gheco"]
print(___)
print(___)
print(compania)
```

#### Salida esperada
```
['Gheco', 'Mia', 'Tilo']
['Tilo', 'Mia', 'Gheco']
['Tilo', 'Mia', 'Gheco']
```

#### Solución
```python
compania = ["Tilo", "Mia", "Gheco"]
print(sorted(compania))
print(sorted(compania, reverse=True))
print(compania)
```

#### Al superarla
Le toca a Gheco la primera guardia. Se duerme a los tres minutos.

#### Imagen
- La Posada de noche, casi a oscuras; Gheco «de guardia» dormido sobre una silla, brillando suave.
- Mia y Tilo durmiendo en catres; sobre la mesa, el pergamino con la lista ordenada.

### Micro-misión R01-N05-P5 · Pasar lista

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Recorrer | for x in lista: · for i, x in enumerate(lista, start=1): posición y valor
recompensa: xp 10, oro 10
```

#### Escena
—Antes de salir se pasa lista —dice Tilo—. Mi papá lo hace con los balseros: uno, dos, tres.

#### Gheco sugiere
`for x in lista:` recorre los elementos de a uno. Si además querés el número de cada uno, `enumerate(lista, start=1)` te da la **posición y el valor** juntos.

#### Desafío
Pasá lista numerando desde 1.

#### Código inicial
```python
compania = ["Mia", "Gheco", "Tilo"]
for ___ in ___:
    print(f"{numero}. {nombre}: ¡presente!")
```

#### Salida esperada
```
1. Mia: ¡presente!
2. Gheco: ¡presente!
3. Tilo: ¡presente!
```

#### Solución
```python
compania = ["Mia", "Gheco", "Tilo"]
for numero, nombre in enumerate(compania, start=1):
    print(f"{numero}. {nombre}: ¡presente!")
```

#### Al superarla
«¡Presente!», grita Gheco tan fuerte que despierta a medio salón.

#### Imagen
- Amanecer en la puerta de la Posada: Mia, Tilo y Gheco en fila, como soldaditos.
- Números de luz (1, 2, 3) flotan sobre sus cabezas.

### Micro-misión R01-N05-P6 · Provisiones para el doble

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Comprehension | [expresión for x in lista] · con filtro: [x for x in lista if condición]
recompensa: xp 15, oro 15
item: Morral de la Posada
```

#### Escena
El posadero les vende provisiones, pero el camino es largo: hace falta el **doble** de cada cosa. Y de paso, quedarse solo con lo que cueste menos de 5.

#### Gheco sugiere
Una *comprehension* arma una lista nueva desde otra en una línea: `[p * 2 for p in cantidades]`. Con un `if` al final, filtra: `[p for p in precios if p < 5]`.

#### Desafío
Doblá las cantidades y filtrá los precios baratos.

#### Código inicial
```python
cantidades = [2, 1, 3]
precios = [3, 8, 4, 12]
dobles = ___
baratos = ___
print(dobles)
print(baratos)
```

#### Salida esperada
```
[4, 2, 6]
[3, 4]
```

#### Solución
```python
cantidades = [2, 1, 3]
precios = [3, 8, 4, 12]
dobles = [c * 2 for c in cantidades]
baratos = [p for p in precios if p < 5]
print(dobles)
print(baratos)
```

#### Al superarla
El posadero, sorprendido por lo rápido de la cuenta, les regala un **morral** de cuero con muchos bolsillos.

#### Imagen
- El mostrador de la Posada con bolsas de provisiones que se duplican en el aire.
- El posadero entrega un morral de cuero lleno de bolsillos a Mia.

### Micro-misión R01-N05-P7 · El mapa del camino

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo
carta: Listas anidadas | mapa[fila][columna] · una lista de filas, cada fila una lista
recompensa: xp 15, oro 15
```

#### Escena
Tilo dibuja en la mesa el camino a la Ermita como una grilla: `.` es camino y `#` es piedra. La ermita está en la última fila, a la derecha.

#### Gheco sugiere
Una lista puede tener listas adentro: un **mapa** es una lista de filas. `mapa[1][2]` es la fila 1, columna 2 (siempre desde 0).

#### Desafío
Mostrá qué hay en la esquina de la ermita (última fila, última columna) y en la casilla del medio.

#### Código inicial
```python
mapa = [
    [".", "#", "."],
    [".", ".", "#"],
    ["#", ".", "E"],
]
print(mapa[___][___])
print(mapa[___][___])
```

#### Salida esperada
```
E
.
```

#### Solución
```python
mapa = [
    [".", "#", "."],
    [".", ".", "#"],
    ["#", ".", "E"],
]
print(mapa[2][2])
print(mapa[1][1])
```

#### Al superarla
—E de Ermita —dice Tilo—. Ahí vive un viejo que sabe el nombre de todos los bichos.

#### Imagen
- Una grilla de 3×3 dibujada con tiza sobre la mesa de la Posada; una casilla con una E brilla.
- Tilo con la tiza en la mano; Mia sigue el dedo de Tilo sobre la grilla.

### Micro-misión R01-N05-P8 · Coordenadas que no cambian

```meta
lugar: La Posada de la Serpiente
personajes: Mia, Gheco, Tilo, el Profe
carta: Tuplas | (x, y) como una lista que no se cambia · desempaquetar: fila, col = posicion
recompensa: xp 15, oro 20
se abre: las expediciones del jugador (el Profe explica el mapa, el temporizador y los establos)
```

#### Escena
Un hombre de barba canosa y sobretodo negro con líneas cian se sienta a la mesa sin pedir permiso. Toma notas en una tableta de luz.
—Soy **el Profe**, el Cronista del Gremio. Anoto las hazañas de los aprendices. La ermita está fija en el mapa, chicos: anótenla como algo que **no cambia**.

#### Gheco sugiere
Una **tupla** es como una lista, pero entre paréntesis y **no se puede modificar**: ideal para coordenadas. Se puede **desempaquetar**: `fila, col = (2, 2)` reparte cada valor en su variable.

#### Desafío
Guardá la ermita como tupla y desempaquetala.

#### Código inicial
```python
ermita = ___
fila, col = ___
print(f"Fila {fila}, columna {col}")
```

#### Salida esperada
```
Fila 2, columna 2
```

#### Solución
```python
ermita = (2, 2)
fila, col = ermita
print(f"Fila {fila}, columna {col}")
```

#### Al superarla
El Profe asiente y les muestra su tablero: un mapa del Valle con lugares que se pueden **recorrer**.
—Mientras estudian, pueden mandar a explorar. Les explico cómo funcionan los establos y las expediciones.
Antes de irse, comenta al pasar que vio bajar hacia las Forjas a una espadachina de pelo corto, con un mechón cian.

#### Imagen
- El Profe (barba canosa, anteojos, sobretodo negro con líneas cian) sentado a la mesa con su tableta holográfica.
- Sobre la tableta, un mapa del Valle con puntos brillantes para explorar.
- Mia y Tilo inclinados para ver; Gheco, fascinado.

### Misión R01-N05-M1 · La mochila

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Empezá con `["antorcha", "cuerda", "poción"]`. Agregá
dos gemas, una llave oxidada y pan. Usá la poción (sacala solo si está), tirá
lo último que agarró, ordená la mochila y mostrala numerada con `enumerate`,
junto con cuántas gemas tiene.

#### Criterio de aprobación

- Agrega los objetos con `append`/`extend`.
- Saca la poción solo si está (`in`) y tira lo último con `pop()`.
- Muestra la mochila ordenada y numerada con `enumerate`, y cuántas gemas hay (`count`).

#### Salida esperada

```
al salir: ['antorcha', 'cuerda', 'poción']
después del cofre: ['antorcha', 'cuerda', 'poción', 'gema', 'gema', 'llave oxidada', 'pan']
tomó la poción
tiró: pan
mochila ordenada (5 objetos):
  1. antorcha
  2. cuerda
  3. gema
  4. gema
  5. llave oxidada
gemas: 2
```

#### Solución de referencia

```python
"""Mision 1 - La mochila de Kira."""

mochila = ["antorcha", "cuerda", "poción"]
print("al salir:", mochila)

mochila.append("gema")
mochila.append("gema")
mochila.extend(["llave oxidada", "pan"])
print("después del cofre:", mochila)

# Usar la poción: sacarla SOLO si está (remove da error si no la encuentra)
if "poción" in mochila:
    mochila.remove("poción")
    print("tomó la poción")

# Tirar lo último que agarró
tirado = mochila.pop()
print("tiró:", tirado)

mochila.sort()
print(f"mochila ordenada ({len(mochila)} objetos):")
for i, objeto in enumerate(mochila, start=1):
    print(f"  {i}. {objeto}")
print("gemas:", mochila.count("gema"))
```

### Misión R01-N05-M2 · El ranking del torneo

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con los resultados
`[(120, "Kira"), (95, "Bron"), (150, "Mia"), (95, "Ana"), (60, "Zed")]`,
mostrá el ranking de mayor a menor con puestos, el podio (solo nombres, con
una comprehension) y el promedio de puntos. ¿En qué orden quedan Bron y Ana, y
por qué?

#### Criterio de aprobación

- Ordena de mayor a menor con `sorted(..., reverse=True)`.
- Arma el podio con una comprehension.
- Calcula el promedio de puntos.
- Explica en un comentario el orden de Bron y Ana (desempata por el segundo valor de la tupla).

#### Salida esperada

```
RANKING
1. Mia    150
2. Kira   120
3. Bron    95
4. Ana     95
5. Zed     60
podio: ['Mia', 'Kira', 'Bron']
promedio: 104.0
```

#### Solución de referencia

```python
"""Mision 2 - El ranking del torneo.

Truco: guardar cada resultado como (puntos, nombre). Las tuplas se comparan
elemento por elemento: primero por puntos y, si empatan, por nombre.
Asi sorted() ordena por puntos sin nada extra.
"""

resultados = [(120, "Kira"), (95, "Bron"), (150, "Mia"), (95, "Ana"), (60, "Zed")]

ranking = sorted(resultados, reverse=True)
print("RANKING")
for puesto, (puntos, nombre) in enumerate(ranking, start=1):
    print(f"{puesto}. {nombre:<5} {puntos:>4}")

podio = [nombre for puntos, nombre in ranking[:3]]
print("podio:", podio)
promedio = sum([puntos for puntos, nombre in resultados]) / len(resultados)
print(f"promedio: {promedio:.1f}")
```

### Misión R01-N05-M3 · El mapa de la mazmorra

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Armá el mapa como lista de listas (`list("#K..G.#")`
convierte cada fila). Encontrá la posición de Kira (`K`) con dos `for` y
`enumerate`, contá las gemas (`G`) y, si a su derecha hay piso (`.`), movela.
Mostrá el mapa antes y después.

#### Criterio de aprobación

- Arma el mapa como lista de listas.
- Encuentra a K con dos `for` y `enumerate`.
- Cuenta las gemas y mueve a K solo si a la derecha hay piso.
- Muestra el mapa antes y después.

#### Salida esperada

```
Kira está en fila 1, columna 1
gemas en el mapa: 3
Kira avanza a la derecha
#######
#.K.G.#
#.#G#.#
#G....#
#######
```

#### Solución de referencia

```python
"""Mision 3 - El mapa de la mazmorra.

Encontrar a Kira (K), contar las gemas (G) y moverla una casilla a la derecha
si ahi hay piso ('.').
"""

mapa = [
    list("#######"),
    list("#K..G.#"),
    list("#.#G#.#"),
    list("#G....#"),
    list("#######"),
]

fila_k = -1
col_k = -1
gemas = 0
for f, fila in enumerate(mapa):
    for c, celda in enumerate(fila):
        if celda == "K":
            fila_k = f
            col_k = c
        elif celda == "G":
            gemas += 1

print(f"Kira está en fila {fila_k}, columna {col_k}")
print("gemas en el mapa:", gemas)

if mapa[fila_k][col_k + 1] == ".":
    mapa[fila_k][col_k] = "."
    mapa[fila_k][col_k + 1] = "K"
    print("Kira avanza a la derecha")

for fila in mapa:
    print("".join(fila))
```

### Encargo R01-N05-E1 · Las notas de la escuela

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

La escuela del pueblo tiene las notas `[7, 4, 9, 6, 10, 3, 8, 6, 5]`. Calculá el
promedio, la nota más alta y la más baja, cuántos aprobaron (nota 6 o más), las
notas desaprobadas de mayor a menor y las tres mejores notas.

#### Criterio de aprobación

- Calcula promedio, máxima y mínima con `sum`, `len`, `max` y `min`.
- Cuenta los aprobados (6 o más).
- Muestra las desaprobadas de mayor a menor y las tres mejores notas.

#### Salida esperada

```
notas: [7, 4, 9, 6, 10, 3, 8, 6, 5]
promedio: 6.44
más alta: 10 | más baja: 3
aprobados: 6 de 9
desaprobadas (de mayor a menor): [5, 4, 3]
las 3 mejores: [10, 9, 8]
```

#### Solución de referencia

```python
"""Encargo del Gremio - Las notas de la escuela del pueblo."""

notas = [7, 4, 9, 6, 10, 3, 8, 6, 5]

promedio = sum(notas) / len(notas)
aprobadas = [n for n in notas if n >= 6]
desaprobadas = [n for n in notas if n < 6]

print("notas:", notas)
print(f"promedio: {promedio:.2f}")
print("más alta:", max(notas), "| más baja:", min(notas))
print(f"aprobados: {len(aprobadas)} de {len(notas)}")
print("desaprobadas (de mayor a menor):", sorted(desaprobadas, reverse=True))
print("las 3 mejores:", sorted(notas, reverse=True)[:3])
```

### Prueba del sello

#### ¿Qué diferencia hay entre `append` y `extend`? ¿Y entre `remove` y `pop`?

`append` agrega **un** elemento (aunque sea una lista); `extend` agrega **cada** elemento de otra colección. `remove` saca por **valor**; `pop` saca por **posición** (la última si no se dice) y la devuelve.

#### ¿Qué devuelve `lista.sort()`? ¿Y `sorted(lista)`?

`lista.sort()` ordena la misma lista y devuelve `None`; `sorted(lista)` devuelve una lista **nueva** ordenada y no toca la original.

#### Si `m = [[1, 2], [3, 4]]`, ¿cuánto vale `m[1][0]`?

`3`: la fila 1 es `[3, 4]` y su elemento 0 es 3.

#### ¿Cómo creás una tupla de un solo elemento?

Con una coma: `(5,)`. Sin la coma, `(5)` es solo el número 5.

#### ¿Qué valen `a` y `resto` después de `a, *resto = "SLIME"`?

`a` vale `"S"` y `resto` vale `["L", "I", "M", "E"]`.

#### ¿Cuándo conviene una tupla en lugar de una lista?

Cuando los datos van juntos y **no deberían cambiar** (una coordenada, una fecha), o cuando hace falta usarlos como clave de un diccionario.

### Soluciones (docente)

Material original: `17-Python/06-Listas-Tuplas` (soluciones completas en `soluciones/`).

## R01-N06 · Diccionarios y conjuntos

```meta
tipo: tema
padre: R01-N05
precio: 10
criatura: orco
temas: col.mapas, col.conjuntos
```

### Crónica

La bibliotecaria del Valle te entrega el **Bestiario**: un libro donde cada criatura tiene su página, con su vida, su ataque y sus debilidades.

—No lo leas de principio a fin, {heroe} —te advierte—. **Buscá por el nombre**.

Esa noche, Mia anota qué hechizos conoce cada integrante de la compañía, sin repetir ninguno, para saber cuáles comparten y cuáles faltan.

### Objetivos

Usar diccionarios para buscar por clave, modificarlos, recorrerlos, anidarlos y
contar con ellos; usar conjuntos para eliminar repetidos y comparar grupos; y
elegir la estructura correcta para cada problema.

### Antes de empezar

- Listas, tuplas, desempaquetado y comprehensions (06).
- `for`, `if` (05).

### Explicación

#### Diccionarios: `{clave: valor}`
Un diccionario guarda **pares clave → valor**. En lugar de buscar por posición
(como en una lista), **se busca por clave**:
```python
kira = {"nombre": "Kira", "vida": 100, "nivel": 3}
kira["vida"]        # 100
```
- Las claves **no se repiten**. Si asignás una clave que ya existe, se reemplaza
  su valor.
- Las claves tienen que ser **inmutables**: textos, números, tuplas. Una lista no
  puede ser clave (`TypeError: unhashable type: 'list'`).
- Los valores pueden ser **cualquier cosa**, incluso listas u otros diccionarios.
- Mantienen el **orden en que se insertaron** las claves.

#### Leer sin romperse
| Forma | Si la clave no existe |
|---|---|
| `d[clave]` | error `KeyError` |
| `d.get(clave)` | devuelve `None` |
| `d.get(clave, defecto)` | devuelve `defecto` |
| `clave in d` | `False` (pregunta **por claves**, no por valores) |

#### Modificar
| Operación | Hace |
|---|---|
| `d[clave] = valor` | agrega o reemplaza |
| `d.update({...})` | agrega o reemplaza varias a la vez |
| `d.pop(clave)` | saca la clave y **devuelve** su valor |
| `del d[clave]` | borra la clave |
| `d.setdefault(clave, defecto)` | si no existe, la crea con `defecto`; devuelve el valor |

#### Recorrer
- `for clave in d:` recorre las **claves**.
- `d.keys()`, `d.values()` y `d.items()` dan claves, valores y pares.
- `for clave, valor in d.items():` es la forma más común.
- **No agregues ni borres claves mientras recorrés el mismo diccionario**
  (`RuntimeError`). Recorré una copia (`list(d)`) o armá uno nuevo.

#### Dict comprehension
`{clave: valor for ... in ... if ...}`:
```python
baratos = {item: p for item, p in precios.items() if p < 50}
```

#### Estructuras anidadas
Un diccionario de diccionarios (o de listas) modela datos reales:
`bestiario["orco"]["vida"]`, `bestiario["orco"]["debil_a"][0]`. Se lee de
izquierda a derecha: primero la criatura, después el dato.

#### Contar
El patrón más común: `conteo[x] = conteo.get(x, 0) + 1`. El módulo
`collections` de la biblioteca de Python trae dos ayudas:
- **`Counter(lista)`** cuenta todo de una vez; `.most_common(n)` da los n más
  frecuentes.
- **`defaultdict(list)`** crea automáticamente el valor inicial (una lista vacía)
  la primera vez que usás una clave: sirve para **agrupar**.

(`from collections import Counter` trae esas herramientas; los imports se ven
en 11.)

#### Conjuntos: `{a, b, c}`
Un **set** guarda valores **sin repetir** y **sin orden** (no tiene índices).
- `set()` crea uno vacío. **Ojo**: `{}` es un diccionario vacío, no un set.
- `add(x)`, `remove(x)` (error si no está), `discard(x)` (sin error).
- `set(lista)` elimina los repetidos de una lista.
- Para mostrarlo siempre en el mismo orden, `sorted(conjunto)`.

| Operación | Símbolo | Da |
|---|---|---|
| intersección | `a & b` | lo que está en los dos |
| unión | `a \| b` | lo que está en alguno |
| diferencia | `a - b` | lo de `a` que no está en `b` |
| diferencia simétrica | `a ^ b` | lo que está en uno solo |
| subconjunto | `a <= b` | ¿todo `a` está en `b`? |

Y la *set comprehension*: `{nombre[0] for nombre in nombres}`.

#### ¿Qué estructura elijo?
| Necesito… | Uso | Buscar si algo está |
|---|---|---|
| una secuencia ordenada que cambia | `list` | lento con muchos datos (revisa uno por uno) |
| un registro fijo de pocos valores | `tuple` | lento (igual que la lista) |
| buscar datos por un nombre o id | `dict` | **rápido** (no importa el tamaño) |
| saber si algo está, sin repetidos | `set` | **rápido** |

Buscar con `in` en una lista de un millón de elementos puede revisarlos todos;
en un `set` o un `dict` es prácticamente instantáneo, gracias a una técnica
llamada *hashing*. Por eso las claves tienen que ser inmutables. Cuánto tarda
cada operación se mide en 31 (Rendimiento).

### Código de ejemplo

```python
"""07 - Diccionarios y conjuntos.

dict -> guarda pares CLAVE: VALOR. Se busca por clave, no por posicion.
set  -> guarda valores SIN repetir y sin orden. Ideal para "¿esta o no esta?".
"""

# "from modulo import nombre" trae herramientas de la biblioteca de Python (se ve en 11)
from collections import Counter, defaultdict

# =========================================================
# Crear un diccionario y leer valores
# =========================================================
kira = {"nombre": "Kira", "clase": "espadachina", "vida": 100, "nivel": 3}
print(kira)
print("nombre:", kira["nombre"])
print("cantidad de claves:", len(kira))

# get: leer SIN error si la clave no existe (devuelve None o un valor por defecto)
print("armadura:", kira.get("armadura"))
print("armadura:", kira.get("armadura", 0))
print("¿tiene 'vida'?", "vida" in kira)      # 'in' pregunta por CLAVES

# =========================================================
# Modificar
# =========================================================
kira["vida"] -= 25                  # cambiar el valor de una clave existente
kira["mana"] = 40                   # clave nueva -> se agrega
kira.update({"nivel": 4, "oro": 15})   # varias a la vez
print("después de la pelea:", kira)

oro = kira.pop("oro")               # sacar una clave y devolver su valor
del kira["mana"]                    # borrar una clave
print(f"sacó {oro} de oro ->", kira)

# setdefault: devuelve el valor; si la clave no existe, antes la crea con el defecto
kira.setdefault("hechizos", 0)
kira.setdefault("vida", 999)        # ya existe: no la cambia
print("setdefault:", kira)

# =========================================================
# Recorrer
# =========================================================
for clave in kira:                  # recorre las CLAVES
    print("clave:", clave)
print("claves:", list(kira.keys()))
print("valores:", list(kira.values()))
for clave, valor in kira.items():   # pares (clave, valor)
    print(f"  {clave:>9}: {valor}")

# =========================================================
# Dict comprehension y diccionarios anidados
# =========================================================
precios = {"poción": 8, "antorcha": 3, "espada": 120, "escudo": 90}
baratos = {item: p for item, p in precios.items() if p < 50}
con_descuento = {item: round(p * 0.9) for item, p in precios.items()}
print("baratos:", baratos)
print("con 10% off:", con_descuento)

bestiario = {
    "slime": {"vida": 10, "ataque": 2, "debil_a": ["fuego"]},
    "orco": {"vida": 45, "ataque": 8, "debil_a": ["hielo", "rayo"]},
}
print("vida del orco:", bestiario["orco"]["vida"])
print("el orco es débil a:", ", ".join(bestiario["orco"]["debil_a"]))
bestiario["ogro"] = {"vida": 90, "ataque": 12, "debil_a": []}
for criatura, datos in bestiario.items():
    print(f"  {criatura:<6} vida {datos['vida']:>3}  ataque {datos['ataque']:>2}")

# Las claves tienen que ser INMUTABLES: textos, numeros, tuplas. Listas no.
tesoros = {(2, 3): "cofre", (5, 1): "gema"}     # posicion (fila, col) -> objeto
print("en (2, 3) hay:", tesoros[(2, 3)])

# =========================================================
# Contar: el patron mas comun con diccionarios
# =========================================================
botin = ["gema", "poción", "gema", "oro", "gema", "poción"]
conteo = {}
for item in botin:
    conteo[item] = conteo.get(item, 0) + 1
print("conteo a mano:", conteo)

# collections.Counter hace lo mismo (y mas)
contador = Counter(botin)
print("Counter:", contador)
print("lo más común:", contador.most_common(1))

# collections.defaultdict: crea el valor por defecto solo, al acceder
por_puesto = defaultdict(list)          # si la clave no existe, arranca con una lista vacia
for nombre, puesto in [("Kira", "vanguardia"), ("Mia", "retaguardia"), ("Bron", "vanguardia")]:
    por_puesto[puesto].append(nombre)
print("formación:", dict(por_puesto))

# =========================================================
# Conjuntos (set): sin repetidos, sin orden
# =========================================================
vistos = {"slime", "orco", "slime", "goblin"}   # el repetido desaparece
print("criaturas vistas:", sorted(vistos))       # sorted para mostrarlo ordenado
vacio = set()                                    # OJO: {} es un DICT vacio
print("set vacío:", vacio, "| {} es:", type({}))
vistos.add("ogro")
vistos.discard("dragón")         # discard: no da error si no esta (remove si)
print("¿vio un orco?", "orco" in vistos)
print("cantidad:", len(vistos))

# Sacar repetidos de una lista
tiradas = [3, 6, 3, 1, 6, 6, 2]
print("valores distintos:", sorted(set(tiradas)))

# Operaciones de conjuntos
kira_sabe = {"espada", "escudo", "fuego"}
mia_sabe = {"fuego", "hielo", "curación"}
print("las dos saben:", sorted(kira_sabe & mia_sabe))    # interseccion
print("entre las dos:", sorted(kira_sabe | mia_sabe))    # union
print("solo Kira:", sorted(kira_sabe - mia_sabe))        # diferencia
print("una sola:", sorted(kira_sabe ^ mia_sabe))         # diferencia simetrica
print("¿{'fuego'} está incluido en lo de Kira?", {"fuego"} <= kira_sabe)

# Set comprehension
iniciales = {nombre[0] for nombre in ["Kira", "Kael", "Mia", "Bron"]}
print("iniciales:", sorted(iniciales))
```

### Salida esperada

```
{'nombre': 'Kira', 'clase': 'espadachina', 'vida': 100, 'nivel': 3}
nombre: Kira
cantidad de claves: 4
armadura: None
armadura: 0
¿tiene 'vida'? True
después de la pelea: {'nombre': 'Kira', 'clase': 'espadachina', 'vida': 75, 'nivel': 4, 'mana': 40, 'oro': 15}
sacó 15 de oro -> {'nombre': 'Kira', 'clase': 'espadachina', 'vida': 75, 'nivel': 4}
setdefault: {'nombre': 'Kira', 'clase': 'espadachina', 'vida': 75, 'nivel': 4, 'hechizos': 0}
clave: nombre
clave: clase
clave: vida
clave: nivel
clave: hechizos
claves: ['nombre', 'clase', 'vida', 'nivel', 'hechizos']
valores: ['Kira', 'espadachina', 75, 4, 0]
     nombre: Kira
      clase: espadachina
       vida: 75
      nivel: 4
   hechizos: 0
baratos: {'poción': 8, 'antorcha': 3}
con 10% off: {'poción': 7, 'antorcha': 3, 'espada': 108, 'escudo': 81}
vida del orco: 45
el orco es débil a: hielo, rayo
  slime  vida  10  ataque  2
  orco   vida  45  ataque  8
  ogro   vida  90  ataque 12
en (2, 3) hay: cofre
conteo a mano: {'gema': 3, 'poción': 2, 'oro': 1}
Counter: Counter({'gema': 3, 'poción': 2, 'oro': 1})
lo más común: [('gema', 3)]
formación: {'vanguardia': ['Kira', 'Bron'], 'retaguardia': ['Mia']}
criaturas vistas: ['goblin', 'orco', 'slime']
set vacío: set() | {} es: <class 'dict'>
¿vio un orco? True
cantidad: 4
valores distintos: [1, 2, 3, 6]
las dos saben: ['fuego']
entre las dos: ['curación', 'escudo', 'espada', 'fuego', 'hielo']
solo Kira: ['escudo', 'espada']
una sola: ['curación', 'escudo', 'espada', 'hielo']
¿{'fuego'} está incluido en lo de Kira? True
iniciales: ['B', 'K', 'M']
```

### ¿Para qué sirve?

Un diccionario es la forma de buscar **por clave**: el DNI de una persona, el código de un producto, el usuario de una cuenta. Contar palabras de un texto, votos de una elección o ventas por vendedor se hace con diccionarios (`Counter`). Los conjuntos sacan repetidos al instante y comparan grupos: qué alumnos cursan las dos materias, qué permisos le faltan a un usuario.

### Errores habituales

**Orco: clave que no existe** (`KeyError: 'b'`). Usá `get` o preguntá con `in`.

**Goblin: lista como clave** (`TypeError: unhashable type: 'list'`). Usá una
tupla.

**Goblin: acceder a un set por índice**
(`TypeError: 'set' object is not subscriptable`). Los sets no tienen posiciones.

**Troll: modificar el diccionario mientras lo recorrés**
(`RuntimeError: dictionary changed size during iteration`).

**Ogros (corre, pero hace otra cosa):**
- `vacio = {}` y después `vacio.add(x)`: es un diccionario, no un set.
- `"Kira" in personaje` busca entre las **claves**, no entre los valores. Para
  valores: `"Kira" in personaje.values()`.
- Esperar que un `set` mantenga el orden de inserción: no lo hace.

### Micro-misión R01-N06-P1 · La página del slime

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Diccionarios | {clave: valor} · d["clave"] lee · las claves no se repiten
recompensa: xp 10, oro 10
```

#### Escena
El Ermitaño los mira con un solo ojo; el otro es un monóculo de luz cian.
—¿Quieren el Bestiario? Primero lean una página. Cada criatura tiene sus datos con nombre: vida, ataque, debilidad.

#### Gheco sugiere
Un **diccionario** guarda pares **clave: valor** entre llaves. Se lee por la clave, no por la posición: `slime["vida"]`.

#### Desafío
Mostrá la vida y la debilidad del slime.

#### Código inicial
```python
slime = {"vida": 10, "ataque": 2, "debilidad": "fuego"}
print(slime[___])
print(slime[___])
```

#### Salida esperada
```
10
fuego
```

#### Solución
```python
slime = {"vida": 10, "ataque": 2, "debilidad": "fuego"}
print(slime["vida"])
print(slime["debilidad"])
```

#### Al superarla
—Lee —gruñe el Ermitaño—. Bien. Una página no es un libro.

#### Imagen
- Interior de una ermita de madera llena de libros y frascos; un bicho de luz revolotea.
- El Ermitaño (capa de musgo con capucha, barba gris, monóculo cian, bastón con orbe) sostiene un libro abierto en la página del slime.
- Mia, Tilo y Gheco leen por encima de su hombro.

### Micro-misión R01-N06-P2 · La página que falta

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
criatura: orco
carta: get | d.get(clave) da None si no está · d.get(clave, "por defecto") · d[clave] da KeyError
recompensa: xp 10, oro 10
```

#### Escena
Tilo busca la página del **troll**, que es la que más miedo le da. El libro tiembla y no la encuentra: un orco chiquito asoma entre las hojas.

#### Gheco sugiere
Pedir una clave que no existe con `d[clave]` da `KeyError` (el grito del orco). `d.get(clave, "algo")` devuelve el valor si está y, si no, lo que le digas.

#### Desafío
Buscá al troll sin que aparezca el orco.

#### Código inicial
```python
vida = {"slime": 10, "goblin": 15, "orco": 30}
print(vida["troll"])
```

#### Salida esperada
```
No está anotado
```

#### Solución
```python
vida = {"slime": 10, "goblin": 15, "orco": 30}
print(vida.get("troll", "No está anotado"))
```

#### Al superarla
—No está anotado porque nadie volvió para contarlo —dice el Ermitaño. Tilo traga saliva.

#### Imagen
- Un orco diminuto asoma entre las páginas del Bestiario con la boca abierta, gritando KeyError.
- Tilo da un salto hacia atrás; Mia escribe `get` en el pergamino y el orco se esconde.

### Micro-misión R01-N06-P3 · Anotar lo que viste

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Modificar un diccionario | d[clave] = valor agrega o cambia · del d[clave] borra
recompensa: xp 10, oro 10
```

#### Escena
Le contás al Ermitaño el goblin del mercado. Era más fuerte de lo que dice el libro: tenía 20 de vida, no 15. Y el murciélago de la cueva, que nadie anotó, tenía 8.

#### Gheco sugiere
`d[clave] = valor` **cambia** el valor si la clave existe y la **agrega** si no.

#### Desafío
Corregí al goblin y agregá al murciélago.

#### Código inicial
```python
vida = {"slime": 10, "goblin": 15}
___
___
print(vida)
```

#### Salida esperada
```
{'slime': 10, 'goblin': 20, 'murciélago': 8}
```

#### Solución
```python
vida = {"slime": 10, "goblin": 15}
vida["goblin"] = 20
vida["murciélago"] = 8
print(vida)
```

#### Al superarla
El Ermitaño moja la pluma y lo anota él mismo, con letra temblorosa. —Nadie me había traído datos nuevos en años.

#### Imagen
- El Ermitaño escribe en el Bestiario a la luz de su bastón; una página nueva muestra un murciélago.
- Gheco imita a un murciélago colgado de una viga.

### Micro-misión R01-N06-P4 · Leer el Bestiario entero

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Recorrer un diccionario | for clave, valor in d.items(): · d.keys() · d.values()
recompensa: xp 10, oro 10
```

#### Escena
—Si lo van a llevar, sepan qué hay adentro —dice el Ermitaño—. Léanmelo en voz alta.

#### Gheco sugiere
`d.items()` da los pares **clave y valor** juntos, para recorrerlos con un `for`.

#### Desafío
Mostrá cada criatura con su vida.

#### Código inicial
```python
vida = {"slime": 10, "goblin": 20, "murciélago": 8}
for ___ in ___:
    print(f"{nombre}: {v} de vida")
```

#### Salida esperada
```
slime: 10 de vida
goblin: 20 de vida
murciélago: 8 de vida
```

#### Solución
```python
vida = {"slime": 10, "goblin": 20, "murciélago": 8}
for nombre, v in vida.items():
    print(f"{nombre}: {v} de vida")
```

#### Al superarla
El bicho de luz se posa en el hombro de Gheco. Se miran. Se caen bien.

#### Imagen
- Mia lee en voz alta el Bestiario; nombres de criaturas flotan en el aire como fantasmas de luz.
- El bicho de luz y Gheco, frente a frente, curiosos.

### Micro-misión R01-N06-P5 · Contar las huellas

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Contar con un diccionario | cuenta[x] = cuenta.get(x, 0) + 1
recompensa: xp 15, oro 15
```

#### Escena
Afuera de la ermita hay huellas en el barro. Tilo, que sabe leer huellas aunque no runas, las va nombrando. El Ermitaño quiere saber **cuántas de cada una**.

#### Gheco sugiere
El patrón para contar: un diccionario vacío y, por cada cosa, `cuenta[x] = cuenta.get(x, 0) + 1`. La primera vez `get` da 0.

#### Desafío
Completá la línea que cuenta.

#### Código inicial
```python
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
cuenta = {}
for h in huellas:
    ___
print(cuenta)
```

#### Salida esperada
```
{'slime': 3, 'goblin': 2, 'troll': 1}
```

#### Solución
```python
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
cuenta = {}
for h in huellas:
    cuenta[h] = cuenta.get(h, 0) + 1
print(cuenta)
```

#### Al superarla
Hay **una** huella de troll. Fresca. Tilo deja de sonreír.

#### Imagen
- Barro con huellas de distintos tamaños; una enorme, de troll, en primer plano.
- Tilo agachado señalando las huellas; contadores de luz flotan sobre cada tipo.

### Micro-misión R01-N06-P6 · El contador del Ermitaño

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Counter | from collections import Counter · Counter(lista) · .most_common(1)
recompensa: xp 10, oro 10
```

#### Escena
El Ermitaño se ríe por primera vez. —Eso que hicieron a mano ya existe hecho. Miren.

#### Gheco sugiere
`Counter(lista)` cuenta todo de una vez y `.most_common(1)` da el más repetido, con su cantidad.

#### Desafío
Usá `Counter` para saber cuál huella aparece más.

#### Código inicial
```python
from collections import Counter
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
cuenta = ___
print(cuenta.most_common(1))
```

#### Salida esperada
```
[('slime', 3)]
```

#### Solución
```python
from collections import Counter
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
cuenta = Counter(huellas)
print(cuenta.most_common(1))
```

#### Al superarla
—Los slimes siempre ganan en cantidad —dice el Ermitaño—. Por eso hay que aprender a vencerlos rápido.

#### Imagen
- El Ermitaño con el bastón en alto; del orbe sale un contador holográfico.
- Mia, admirada; Tilo, todavía mirando la huella del troll.

### Micro-misión R01-N06-P7 · Sin repetir

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Conjuntos | set(lista) sin repetidos ni orden · {a, b} · x in conjunto es muy rápido
recompensa: xp 10, oro 10
```

#### Escena
—Para el índice del libro, cada criatura una sola vez —pide el Ermitaño.

#### Gheco sugiere
Un **conjunto** (`set`) guarda cada valor **una sola vez** y sin orden. `set(lista)` saca los repetidos. Para mostrarlo prolijo, `sorted(conjunto)`.

#### Desafío
Armá el índice sin repetidos y en orden alfabético.

#### Código inicial
```python
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
indice = ___
print(sorted(indice))
```

#### Salida esperada
```
['goblin', 'slime', 'troll']
```

#### Solución
```python
huellas = ["slime", "goblin", "slime", "slime", "goblin", "troll"]
indice = set(huellas)
print(sorted(indice))
```

#### Al superarla
El índice del Bestiario se escribe solo en la primera página.

#### Imagen
- La primera página del Bestiario con un índice que se escribe solo, en tinta verde.
- El bicho de luz ilumina cada palabra a medida que aparece.

### Micro-misión R01-N06-P8 · Las debilidades en común

```meta
lugar: La Ermita del Bestiario
personajes: Mia, Gheco, Tilo, el Ermitaño
carta: Operaciones de conjuntos | a & b los dos · a | b alguno · a - b solo el primero
recompensa: xp 15, oro 20
item: El Bestiario
se abre: la ficha de criaturas del Bestiario en el inventario
```

#### Escena
—Última lección —dice el Ermitaño—. El troll es débil al fuego y a la luz. El goblin, a la luz y al agua. ¿Qué les sirve contra los dos?

#### Gheco sugiere
`a & b` da lo que está **en los dos**; `a | b`, lo que está **en alguno**; `a - b`, lo que está en `a` pero **no** en `b`.

#### Desafío
Mostrá lo que sirve contra los dos y lo que sirve solo contra el troll.

#### Código inicial
```python
troll = {"fuego", "luz"}
goblin = {"luz", "agua"}
print(troll ___ goblin)
print(troll ___ goblin)
```

#### Salida esperada
```
{'luz'}
{'fuego'}
```

#### Solución
```python
troll = {"fuego", "luz"}
goblin = {"luz", "agua"}
print(troll & goblin)
print(troll - goblin)
```

#### Al superarla
El Ermitaño cierra el libro y te lo pone en las manos: **el Bestiario** es tuyo.
—La luz sirve contra los dos. Y la van a necesitar: el camino a las Terrazas pasa por **debajo del puente viejo**. Ahí vive el troll de la huella.

#### Imagen
- El Ermitaño entrega el Bestiario a Mia; el libro brilla al cambiar de manos.
- Dos círculos de luz se cruzan en el aire: en la intersección, la palabra «luz».
- Por la ventana, a lo lejos, se ve un puente viejo de piedra sobre el río.

### Misión R01-N06-M1 · El bestiario

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Armá un diccionario de criaturas (slime, goblin, orco), cada
una con `vida`, `ataque` y una lista `debil_a`. Agregá el ogro, listá con una
comprehension las criaturas débiles al fuego, encontrá la de más vida
recorriendo el diccionario y buscá `"dragón"` sin que el programa falle.

#### Criterio de aprobación

- Cada criatura es un diccionario con `vida`, `ataque` y `debil_a`.
- Lista las débiles al fuego con una comprehension.
- Encuentra la de más vida recorriendo el diccionario.
- Busca "dragón" con `get` o `in`, sin que el programa falle.

#### Salida esperada

```
débiles al fuego: ['slime', 'ogro']
la más resistente: ogro (90 de vida)
'dragón' no está en el bestiario todavía
```

#### Solución de referencia

```python
"""Mision 1 - El bestiario del Valle."""

bestiario = {
    "slime": {"vida": 10, "ataque": 2, "debil_a": ["fuego"]},
    "goblin": {"vida": 20, "ataque": 5, "debil_a": ["luz"]},
    "orco": {"vida": 45, "ataque": 8, "debil_a": ["hielo", "rayo"]},
}

# agregar una criatura nueva
bestiario["ogro"] = {"vida": 90, "ataque": 12, "debil_a": ["fuego", "veneno"]}

# ¿quienes son debiles al fuego?
debiles_fuego = [nombre for nombre, datos in bestiario.items() if "fuego" in datos["debil_a"]]
print("débiles al fuego:", debiles_fuego)

# la criatura con mas vida (recorriendo y recordando la mejor)
mas_fuerte = ""
vida_max = -1
for nombre, datos in bestiario.items():
    if datos["vida"] > vida_max:
        vida_max = datos["vida"]
        mas_fuerte = nombre
print(f"la más resistente: {mas_fuerte} ({vida_max} de vida)")

# buscar sin error aunque no exista
buscada = "dragón"
datos = bestiario.get(buscada)
if datos is None:
    print(f"'{buscada}' no está en el bestiario todavía")
```

### Misión R01-N06-M2 · El reparto del botín

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

De la lista de objetos que soltaron los enemigos,
contá cuántos hay de cada uno con `Counter`, mostrá los dos más comunes y
calculá el valor total con un diccionario de precios (lo que no tiene precio
vale 0).

#### Criterio de aprobación

- Cuenta los objetos con `Counter` y muestra los dos más comunes.
- Calcula el valor total con el diccionario de precios, usando 0 para lo que no tiene precio (`get(obj, 0)`).

#### Salida esperada

```
botín: {'oro': 4, 'gema': 2, 'poción': 2, 'hueso': 1}
total de objetos: 9
los 2 más comunes: [('oro', 4), ('gema', 2)]
  oro     x4  = 4
  gema    x2  = 50
  poción  x2  = 16
  hueso   x1  = 0
valor total: 70
```

#### Solución de referencia

```python
"""Mision 2 - El reparto del botin."""

from collections import Counter

caidas = ["oro", "gema", "oro", "poción", "oro", "gema", "hueso", "oro", "poción"]

botin = Counter(caidas)
print("botín:", dict(botin))
print("total de objetos:", sum(botin.values()))
print("los 2 más comunes:", botin.most_common(2))

# precio de cada objeto y valor total del botin
precios = {"oro": 1, "gema": 25, "poción": 8}
total = 0
for objeto, cantidad in botin.items():
    precio = precios.get(objeto, 0)          # el hueso no vale nada
    total += precio * cantidad
    print(f"  {objeto:<7} x{cantidad}  = {precio * cantidad}")
print("valor total:", total)
```

### Misión R01-N06-M3 · Las habilidades de la compañía

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con los conjuntos de habilidades de Kira,
Mia y Bron: ¿qué saben los tres?, ¿qué saben entre todos?, ¿qué sabe solo
Mia? La Torre del Hielo exige `{"hielo", "escudo", "sigilo"}`: ¿la compañía lo
cubre? ¿Qué les falta?

#### Criterio de aprobación

- Responde las tres preguntas con `&`, `|` y `-`.
- Verifica si la compañía cubre la Torre del Hielo con `<=` (o `issubset`).
- Muestra lo que les falta.

#### Salida esperada

```
los tres saben: ['fuego']
entre todos: ['curación', 'escudo', 'espada', 'fuego', 'hacha', 'hielo', 'rayo']
solo Mia: ['curación', 'hielo', 'rayo']
¿la compañía cubre todo? False
les falta aprender: ['sigilo']
```

#### Solución de referencia

```python
"""Mision 3 - Las habilidades de la compania."""

kira = {"espada", "escudo", "fuego"}
mia = {"fuego", "hielo", "curación", "rayo"}
bron = {"hacha", "escudo", "fuego"}

print("los tres saben:", sorted(kira & mia & bron))
print("entre todos:", sorted(kira | mia | bron))
print("solo Mia:", sorted(mia - kira - bron))

# habilidades que exige la Torre del Hielo
requeridas = {"hielo", "escudo", "sigilo"}
tiene_la_compania = kira | mia | bron
print("¿la compañía cubre todo?", requeridas <= tiene_la_compania)
print("les falta aprender:", sorted(requeridas - tiene_la_compania))
```

### Encargo R01-N06-E1 · Las estadísticas del pregonero

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El pregonero quiere estadísticas de un aviso del pueblo: cantidad de palabras,
cuántas son distintas, las tres más repetidas y si aparece la palabra "oro".
Pasá todo a minúsculas y sacá los signos de puntuación antes de contar.

#### Criterio de aprobación

- Pasa a minúsculas y saca los signos de puntuación antes de contar.
- Muestra la cantidad de palabras, las distintas (con un set) y las tres más repetidas.
- Dice si aparece "oro".

#### Salida esperada

```
palabras en total: 23
palabras distintas: 15
las 3 más repetidas: [('se', 3), ('herrero', 3), ('el', 2)]
¿aparece 'oro'? True
```

#### Solución de referencia

```python
"""Encargo del Gremio - Contar palabras en un aviso del pueblo."""

from collections import Counter

aviso = """Se busca herrero. El herrero debe saber forjar espadas,
y el herrero debe saber templar escudos. Se paga bien, se paga en oro."""

# normalizar: minusculas y sin signos de puntuacion
limpio = aviso.lower()
for signo in ".,;:":
    limpio = limpio.replace(signo, "")
palabras = limpio.split()

conteo = Counter(palabras)
print("palabras en total:", len(palabras))
print("palabras distintas:", len(set(palabras)))
print("las 3 más repetidas:", conteo.most_common(3))
print("¿aparece 'oro'?", "oro" in conteo)
```

### Prueba del sello

#### ¿Qué diferencia hay entre `d["x"]` y `d.get("x")` cuando la clave no existe?

`d["x"]` lanza `KeyError`; `d.get("x")` devuelve `None` (o el valor por defecto que le pases).

#### ¿Por qué una tupla puede ser clave y una lista no?

Porque las claves tienen que ser **inmutables** (hasheables): una tupla no cambia; una lista sí.

#### ¿Qué recorre `for x in diccionario`?

Las **claves**. Para los valores, `.values()`; para los dos, `.items()`.

#### ¿Cómo sacás los repetidos de una lista?

Convirtiéndola en conjunto: `set(lista)` (o `list(dict.fromkeys(lista))` si importa el orden).

#### ¿Qué da `{1, 2, 3} - {2, 3, 4}`? ¿Y `{1, 2} <= {1, 2, 3}`?

`{1}` (lo que está en el primero y no en el segundo). Y `True`: `{1, 2}` está incluido en `{1, 2, 3}`.

#### Tenés que guardar 10.000 nombres de usuario y preguntar muchas veces si uno

Un **set**: preguntar si algo está (`in`) es casi instantáneo, mientras que en una lista hay que recorrerla entera.

### Soluciones (docente)

Material original: `17-Python/07-Diccionarios-Conjuntos` (soluciones completas en `soluciones/`).

## R01-N07 · Referencias, mutabilidad y copias

```meta
tipo: tema
padre: R01-N06
precio: 10
criatura: troll
temas: prog.referencias
```

### Crónica

Antes de entrar a la cueva del troll, anotás la lista de la compañía "por las dudas". Cuando Bron cae y lo tachás de la lista, descubrís con horror que tu anotación **también** lo perdió. No escribiste dos listas: escribiste **dos nombres para la misma lista**.

{mentor} suspira: —Ese es el troll más traicionero del Valle, {heroe}. No lo vas a ver venir: el programa no da error, simplemente hace otra cosa.

### Objetivos

Entender qué es realmente una variable en Python, distinguir **modificar** de
**reasignar**, reconocer qué tipos son mutables e inmutables, y copiar datos
correctamente (copia superficial y profunda).

### Antes de empezar

- Listas, tuplas y listas anidadas (06).
- Diccionarios y conjuntos (07).
- El operador `is` (03).

### Explicación

#### Las variables son etiquetas, no cajas
`compania = ["Kira", "Bron"]` crea **un objeto lista** y le pega la etiqueta
`compania`. Después, `equipo = compania` **no copia nada**: pega una segunda
etiqueta **al mismo objeto**.

```
compania ──┐
           ├──►  ["Kira", "Bron"]
equipo  ───┘
```

Si modificás el objeto por un nombre (`equipo.append("Mia")`), el cambio **se ve
por el otro**, porque es el mismo objeto. A esto se le dice **alias**.

#### Identidad: `is` e `id()`
- `id(x)` da un número que identifica al objeto (su "documento").
- `a is b` pregunta si son **el mismo objeto** (`id(a) == id(b)`).
- `a == b` pregunta si **valen lo mismo**.

Dos listas `[1, 2, 3]` creadas por separado son `==` pero **no** son `is`. Por
eso la regla de 03: `is` solo para `None`, `==` para comparar valores.

#### Modificar o reasignar
| Operación | Qué hace | ¿Lo ven los alias? |
|---|---|---|
| `lista.append(x)`, `lista[0] = x`, `d["k"] = v`, `lista += [x]` | **modifica** el objeto | **sí** |
| `lista = [...]`, `x = x + 1` | **reasigna**: la etiqueta pasa a otro objeto | no |

#### Mutables e inmutables
| Inmutables (no se pueden modificar) | Mutables (se pueden modificar) |
|---|---|
| `int`, `float`, `bool`, `str`, `tuple`, `None`, `frozenset` | `list`, `dict`, `set` |

Con los inmutables el problema del alias **no existe**: `vida -= 30` crea un
número nuevo y mueve la etiqueta; cualquier otro nombre sigue apuntando al valor
viejo. `nombre.upper()` crea un texto nuevo.

**Una tupla es inmutable, pero sus elementos pueden no serlo**:
`("Kira", ["poción"])` no deja cambiar qué hay en cada posición, pero la lista de
adentro sí se puede modificar.

#### Copias superficiales (*shallow*)
Crean un **objeto nuevo** con **los mismos elementos adentro**:
- Listas: `lista.copy()`, `lista[:]`, `list(lista)`.
- Diccionarios: `d.copy()`, `dict(d)`. Sets: `s.copy()`.

Alcanza cuando los elementos son inmutables (números, textos). **Pero si hay
listas o diccionarios adentro, esos se comparten**:
```
mapa ────────►  [ fila0, fila1 ]
mapa_copia ──►  [ fila0, fila1 ]     <- lista nueva, pero las MISMAS filas
```

#### Copias profundas (*deep*)
`copy.deepcopy(x)` (del módulo `copy`) copia **todo, en todos los niveles**. Es lo
que necesitás para un punto de guardado, un "deshacer" o una plantilla que se
reutiliza.

#### La trampa de la grilla
`[["."] * 3] * 3` **no** crea 3 filas: crea **una** fila y 3 referencias a ella.
Lo correcto es `[["."] * 3 for _ in range(3)]`: la comprehension crea una fila
nueva en cada vuelta.

#### ¿Y al pasar datos a una función?
Pasa exactamente lo mismo: la función recibe **otra etiqueta al mismo objeto**.
Si la función modifica una lista que recibió, el cambio se ve afuera. Lo vas a
practicar en 09.

### Código de ejemplo

```python
"""08 - Referencias, mutabilidad y copias.

En Python una variable NO es una caja que contiene un valor: es una ETIQUETA
pegada a un objeto. Dos etiquetas pueden estar pegadas al MISMO objeto.
Si ese objeto se puede modificar (lista, dict, set), el cambio se ve desde
las dos etiquetas. Ese es el troll mas traicionero del Valle.
"""

import copy

# =========================================================
# 1. Dos nombres, un mismo objeto (alias)
# =========================================================
compania = ["Kira", "Bron"]
equipo = compania                 # NO copia: 'equipo' es otra etiqueta del MISMO objeto
equipo.append("Mia")
print("compania:", compania)      # ¡tambien tiene a Mia!
print("¿mismo objeto?", equipo is compania)          # is: ¿es el mismo objeto?
print("¿mismo id?", id(equipo) == id(compania))      # id(): identidad del objeto

# =========================================================
# 2. Reasignar NO es modificar
# =========================================================
equipo = ["Zed"]                  # la etiqueta 'equipo' pasa a OTRO objeto nuevo
print("compania:", compania, "| equipo:", equipo)    # compania no cambio

# =========================================================
# 3. Los inmutables no tienen este problema
# =========================================================
vida = 100
vida_guardada = vida
vida -= 30                        # crea un int NUEVO y mueve la etiqueta 'vida'
print("vida:", vida, "| guardada:", vida_guardada)   # la guardada sigue en 100

nombre = "kira"
otro = nombre
nombre = nombre.upper()           # los str tampoco se modifican: se crea uno nuevo
print("nombre:", nombre, "| otro:", otro)

# =========================================================
# 4. == compara VALORES; is compara IDENTIDAD
# =========================================================
a = [1, 2, 3]
b = [1, 2, 3]
print("a == b:", a == b)          # True: valen lo mismo
print("a is b:", a is b)          # False: son dos listas distintas
c = a
print("a is c:", a is c)          # True: misma lista

# =========================================================
# 5. Copias superficiales (shallow): una lista NUEVA con los MISMOS elementos
# =========================================================
original = ["espada", "escudo"]
copia1 = original.copy()
copia2 = original[:]              # un corte completo tambien copia
copia3 = list(original)
copia1.append("arco")
print("original:", original, "| copia1:", copia1)
print("¿son el mismo objeto?", copia1 is original, copia2 is original, copia3 is original)

# =========================================================
# 6. La trampa: copia superficial de algo ANIDADO
# =========================================================
mapa = [["#", "."], [".", "#"]]
mapa_copia = mapa.copy()          # copia la lista de afuera, NO las filas de adentro
mapa_copia[0][1] = "K"            # modifica una fila... compartida
print("mapa original:", mapa)     # ¡el original tambien cambio!
print("¿la fila 0 es la misma?", mapa[0] is mapa_copia[0])

# 7. copy.deepcopy: copia TODO, en profundidad
mapa = [["#", "."], [".", "#"]]
mapa_profundo = copy.deepcopy(mapa)
mapa_profundo[0][1] = "K"
print("original:", mapa, "| copia profunda:", mapa_profundo)

# Lo mismo con diccionarios que tienen listas adentro
kira = {"nombre": "Kira", "mochila": ["poción"]}
clon_sup = kira.copy()            # superficial: comparte la mochila
clon_prof = copy.deepcopy(kira)   # profunda: mochila propia
clon_sup["mochila"].append("gema")
clon_prof["mochila"].append("mapa")
print("kira:", kira)
print("clon superficial:", clon_sup)
print("clon profundo:", clon_prof)

# =========================================================
# 8. La trampa de la grilla:  [[0] * 3] * 3
# =========================================================
mala = [["."] * 3] * 3            # ¡3 etiquetas a la MISMA fila!
mala[0][0] = "X"
print("grilla mala:", mala)       # la X aparece en las 3 filas

buena = [["."] * 3 for _ in range(3)]    # la comprehension crea una fila NUEVA por vuelta
buena[0][0] = "X"
print("grilla buena:", buena)

# =========================================================
# 9. Una tupla inmutable... que contiene algo mutable
# =========================================================
registro = ("Kira", ["poción"])
# registro[1] = []                # TypeError: la tupla no deja cambiar SUS elementos
registro[1].append("gema")        # pero la lista de adentro SI se puede modificar
print("registro:", registro)
```

### Salida esperada

```
compania: ['Kira', 'Bron', 'Mia']
¿mismo objeto? True
¿mismo id? True
compania: ['Kira', 'Bron', 'Mia'] | equipo: ['Zed']
vida: 70 | guardada: 100
nombre: KIRA | otro: kira
a == b: True
a is b: False
a is c: True
original: ['espada', 'escudo'] | copia1: ['espada', 'escudo', 'arco']
¿son el mismo objeto? False False False
mapa original: [['#', 'K'], ['.', '#']]
¿la fila 0 es la misma? True
original: [['#', '.'], ['.', '#']] | copia profunda: [['#', 'K'], ['.', '#']]
kira: {'nombre': 'Kira', 'mochila': ['poción', 'gema']}
clon superficial: {'nombre': 'Kira', 'mochila': ['poción', 'gema']}
clon profundo: {'nombre': 'Kira', 'mochila': ['poción', 'mapa']}
grilla mala: [['X', '.', '.'], ['X', '.', '.'], ['X', '.', '.']]
grilla buena: [['X', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
registro: ('Kira', ['poción', 'gema'])
```

### ¿Para qué sirve?

Entender las referencias evita los bugs más difíciles de encontrar: una plantilla de factura que "se ensucia" con los datos del cliente anterior, un "deshacer" que no deshace porque el respaldo era la misma lista, una configuración compartida que un módulo cambia sin avisar. Copiar bien (`copy`, `deepcopy`) es lo que permite guardar partidas, versiones de un documento o el estado anterior de un formulario.

### Errores habituales

Este tema casi nunca da error: da **resultados equivocados**. Es territorio del
**troll**.
- **"Hice una copia" con `=`**: `respaldo = lista` no copia. Usá `lista.copy()`.
- **Copia superficial de datos anidados**: `mapa.copy()` comparte las filas. Usá
  `copy.deepcopy(mapa)`.
- **`[[0] * n] * m`**: todas las filas son la misma. Usá una comprehension.
- **Confundir `is` con `==`**: `a is b` puede ser `False` aunque `a == b` sea
  `True`.
- **Esperar que `+=` se comporte igual en todos los tipos**: en una lista
  modifica el objeto (lo ven los alias); en un número, un texto o una tupla crea
  uno nuevo.

Para cazar al troll: `print(a is b)` o `print(id(a), id(b))` te dicen si dos
nombres son el mismo objeto.

### Micro-misión R01-N07-P1 · La anotación de respaldo

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: Alias | b = a NO copia: son dos nombres para la MISMA lista · lo que cambia por uno, cambia por el otro
recompensa: xp 15, oro 15
```

#### Escena
Antes de entrar, anotás la compañía «por las dudas», en una segunda lista. Adentro, el piso cede y **Tilo cae** por un pozo. Lo sacás de la lista… y al mirar la de respaldo, **Tilo tampoco está**.
Desde la oscuridad, el troll se ríe.

#### Gheco sugiere
`respaldo = compania` **no hace una copia**: da otro nombre a **la misma** lista. Lo que le hacés por un nombre, se ve por el otro. Ejecutalo y mirá.

#### Desafío
Ejecutá el código y completá lo que imprime el respaldo. Después, cambiá la segunda línea para que el respaldo sea una copia de verdad: `compania.copy()`.

#### Código inicial
```python
compania = ["Mia", "Gheco", "Tilo"]
respaldo = compania
compania.remove("Tilo")
print(compania)
print(respaldo)
```

#### Salida esperada
```
['Mia', 'Gheco']
['Mia', 'Gheco', 'Tilo']
```

#### Solución
```python
compania = ["Mia", "Gheco", "Tilo"]
respaldo = compania.copy()
compania.remove("Tilo")
print(compania)
print(respaldo)
```

#### Al superarla
En el respaldo verdadero, Tilo sigue anotado. Y desde el fondo del pozo se escucha su voz: —¡Estoy bien! ¡Me raspé!
Te das cuenta de algo: **leíste** que `=` no copia, y aun así te equivocaste. Hasta que no lo **probaste**, no lo entendiste.

#### Imagen
- Boca de una cueva bajo un puente viejo de piedra, oscura, con ojos amarillos al fondo.
- Mia, de rodillas al borde de un pozo, con el pergamino donde dos listas brillan unidas por un mismo hilo.
- Gheco ilumina el pozo; abajo, la mano de Tilo saludando.

### Micro-misión R01-N07-P2 · Reasignar no es modificar

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: Reasignar | a = a + [x] crea una lista NUEVA (el alias no la ve) · a.append(x) cambia la MISMA
recompensa: xp 10, oro 10
```

#### Escena
Gheco quiere entender la trampa del troll. —¿Y si en lugar de `append` sumo con `+`?

#### Gheco sugiere
`a.append(x)` **modifica** la lista. `a = a + [x]` arma una lista **nueva** y hace que `a` apunte a ella: el otro nombre sigue apuntando a la vieja.

#### Desafío
Completá: el primer resultado tiene que mostrar que `b` no cambió.

#### Código inicial
```python
a = ["llave"]
b = a
a = ___
print(a)
print(b)
```

#### Salida esperada
```
['llave', 'bestiario']
['llave']
```

#### Solución
```python
a = ["llave"]
b = a
a = a + ["bestiario"]
print(a)
print(b)
```

#### Al superarla
—Entonces el troll no me engaña si sé si estoy **cambiando** algo o **apuntando** a otra cosa —dice Gheco, orgulloso de la frase.

#### Imagen
- Dos etiquetas de luz con flechas: una apunta a una caja vieja, la otra a una caja nueva.
- Gheco explicándole a Tilo con gestos exagerados.

### Micro-misión R01-N07-P3 · ¿El mismo o igual?

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: == frente a is | == ¿valen lo mismo? · is ¿son el MISMO objeto? · is solo para None
recompensa: xp 10, oro 10
```

#### Escena
En la cueva hay dos cofres idénticos. El troll susurra: «Son el mismo». Gheco no le cree.

#### Gheco sugiere
`==` pregunta si **valen lo mismo**. `is` pregunta si son **el mismo objeto**. Dos listas iguales pueden ser objetos distintos. Para comparar valores usá siempre `==` (y `is` solo con `None`).

#### Desafío
Completá las dos comparaciones.

#### Código inicial
```python
cofre1 = ["oro", "gema"]
cofre2 = ["oro", "gema"]
print(cofre1 ___ cofre2)
print(cofre1 ___ cofre2)
```

#### Salida esperada
```
True
False
```

#### Solución
```python
cofre1 = ["oro", "gema"]
cofre2 = ["oro", "gema"]
print(cofre1 == cofre2)
print(cofre1 is cofre2)
```

#### Al superarla
—Iguales, pero no el mismo —dice Tilo—. Como dos piedras lisas.

#### Imagen
- Dos cofres idénticos uno al lado del otro, iluminados por Gheco.
- Sobre ellos, `==` brilla en verde y `is` en rojo.
- Unos ojos amarillos miran desde la oscuridad.

### Micro-misión R01-N07-P4 · La copia que no alcanza

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: Copia superficial | lista.copy() copia la de afuera, pero las de ADENTRO siguen compartidas
recompensa: xp 15, oro 15
```

#### Escena
Copiás el mapa de la cueva antes de marcar el camino. Marcás una casilla en el original… y **la copia también aparece marcada**. El troll se ríe más fuerte.

#### Gheco sugiere
`.copy()` copia **la lista de afuera**, pero si adentro hay listas (las filas del mapa), esas se **comparten**. Es una copia **superficial**.

#### Desafío
Ejecutalo y mirá cómo la copia también cambia. No hay que arreglar nada todavía: completá el `print` de la copia.

#### Código inicial
```python
mapa = [[".", "."], [".", "."]]
copia = mapa.copy()
mapa[0][0] = "X"
print(mapa)
```

#### Salida esperada
```
[['X', '.'], ['.', '.']]
[['X', '.'], ['.', '.']]
```

#### Solución
```python
mapa = [[".", "."], [".", "."]]
copia = mapa.copy()
mapa[0][0] = "X"
print(mapa)
print(copia)
```

#### Al superarla
—Las filas son las mismas —dice Mia—. Necesito copiar **todo**, hasta el fondo.

#### Imagen
- Dos mapas de piedra lado a lado; la misma X aparece en los dos a la vez, unida por un hilo de luz.
- Mia frunce el ceño, pensando.

### Micro-misión R01-N07-P5 · Copiar hasta el fondo

```meta
lugar: La Cueva del Troll
personajes: Mia, Gheco, Tilo
criatura: troll
carta: Copia profunda | import copy · copy.deepcopy(x) copia todo, también lo de adentro
recompensa: xp 15, oro 20
item: Espejo del Troll
```

#### Escena
El troll sale de la sombra: enorme, con piel de piedra y musgo. Para vencerlo hay que cruzar marcando el camino **sin arruinar** el mapa de respaldo.

#### Gheco sugiere
`copy.deepcopy(mapa)` copia la lista **y todo lo que tiene adentro**. Lo que cambies en el original ya no toca la copia.

#### Desafío
Usá `deepcopy` para que el respaldo quede limpio.

#### Código inicial
```python
import copy
mapa = [[".", "."], [".", "."]]
respaldo = mapa.copy()
mapa[0][0] = "X"
print(respaldo)
```

#### Salida esperada
```
[['.', '.'], ['.', '.']]
```

#### Solución
```python
import copy
mapa = [[".", "."], [".", "."]]
respaldo = copy.deepcopy(mapa)
mapa[0][0] = "X"
print(respaldo)
```

#### Al superarla
Con el mapa limpio encontrás la salida, y con la luz de Gheco (la debilidad del Bestiario) el troll retrocede hasta convertirse en piedra. Donde estaba, queda un **espejo** de bordes de musgo.
Tilo, raspado, se apoya en vos para caminar. —Dicen que en las Terrazas hay un hechizo de curación que se escribe **una sola vez** —dice, apretando los dientes.

#### Imagen
- El troll (enorme, piel de piedra y musgo, ojos amarillos) se vuelve estatua bajo la luz cian de Gheco.
- En el suelo, un espejo con bordes de musgo refleja a Mia.
- Tilo, raspado, apoyado en el hombro de Mia.

### Misión R01-N07-M1 · El bug del troll

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Este código pierde a Bron también en el respaldo.
Explicá por qué y arreglalo:
```python
compania = ["Kira", "Bron", "Mia", "Zed"]
respaldo = compania
compania.remove("Bron")
compania = respaldo
```

#### Criterio de aprobación

- Explica en un comentario por qué `respaldo = compania` no copia la lista.
- Arregla el respaldo con `.copy()` (o `list(...)`).
- Muestra que el respaldo conserva a Bron.

#### Código inicial

```python
compania = ["Kira", "Bron", "Mia", "Zed"]
respaldo = compania
compania.remove("Bron")
compania = respaldo
print(compania)
```

#### Salida esperada

```
después de la batalla: ['Kira', 'Mia', 'Zed']
respaldo: ['Kira', 'Bron', 'Mia', 'Zed']
compañía restaurada: ['Kira', 'Bron', 'Mia', 'Zed']
```

#### Solución de referencia

```python
"""Mision 1 - El bug del troll.

Version con el bug: el "respaldo" era un alias, asi que se perdia junto con
la compania original:

    respaldo = compania          # <- no copia nada
    compania.remove("Bron")      # Bron cae en batalla...
    compania = respaldo          # ...y el respaldo TAMBIEN lo perdio

Arreglo: hacer una COPIA antes de la batalla.
"""

compania = ["Kira", "Bron", "Mia", "Zed"]

respaldo = compania.copy()       # lista nueva con los mismos nombres
compania.remove("Bron")
print("después de la batalla:", compania)
print("respaldo:", respaldo)

compania = respaldo              # ahora si se recupera
print("compañía restaurada:", compania)
```

### Misión R01-N07-M2 · El punto de guardado

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Guardá un checkpoint de un mapa (lista de listas)
antes de mover a Kira y juntar la gema, y después volvé al checkpoint.
Mostrá también qué habría pasado con una copia superficial.

#### Criterio de aprobación

- Guarda el checkpoint con `copy.deepcopy`.
- Mueve a K y junta la gema; después vuelve al checkpoint y lo muestra igual que al principio.
- Muestra qué habría pasado con una copia superficial.

#### Salida esperada

```
mapa actual:
  #####
  #..K#
  #####
vuelta al checkpoint:
  #####
  #K.G#
  #####
¿la copia superficial se ensució? True
```

#### Solución de referencia

```python
"""Mision 2 - El punto de guardado del mapa.

El mapa es una lista de listas: una copia superficial compartiria las filas.
Para un checkpoint de verdad hace falta deepcopy.
"""

import copy

mapa = [
    list("#####"),
    list("#K.G#"),
    list("#####"),
]

checkpoint = copy.deepcopy(mapa)

# Kira avanza y junta la gema
mapa[1][1] = "."
mapa[1][3] = "K"
print("mapa actual:")
for fila in mapa:
    print("  " + "".join(fila))

# ¡trampa! vuelve al checkpoint
mapa = copy.deepcopy(checkpoint)     # otra copia: el checkpoint queda intacto para la proxima
print("vuelta al checkpoint:")
for fila in mapa:
    print("  " + "".join(fila))

# Con .copy() el checkpoint se habria "ensuciado":
malo = mapa.copy()
mapa[1][2] = "X"
print("¿la copia superficial se ensució?", malo[1][2] == "X")
```

### Misión R01-N07-M3 · Predicción

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Anotá qué muestra cada bloque antes de ejecutarlo:
```python
a = [1, 2]; b = a; b += [3]; print(a)
x = (1, 2); y = x; y += (3,); print(x, y)
n = 5; m = n; m += 1; print(n, m)
filas = [[0] * 2] * 2; filas[1][0] = 9; print(filas)
d = {"items": []}; e = d.copy(); e["items"].append("gema"); print(d)
```

#### Criterio de aprobación

- Anota la predicción de cada bloque en un comentario.
- Ejecuta y explica los casos que no acertó (sobre todo `[[0] * 2] * 2` y `d.copy()`).

#### Salida esperada

```
[1, 2, 3]
(1, 2) (1, 2, 3)
5 6
[[9, 0], [9, 0]]
{'items': ['gema']}
```

#### Solución de referencia

```python
"""Mision 3 - Predecir antes de correr (respuestas en los comentarios)."""

a = [1, 2]
b = a
b += [3]            # += en una lista MODIFICA el objeto (como extend)
print(a)            # [1, 2, 3]

x = (1, 2)
y = x
y += (3,)           # las tuplas son inmutables: += crea una tupla NUEVA
print(x, y)         # (1, 2) (1, 2, 3)

n = 5
m = n
m += 1
print(n, m)         # 5 6

filas = [[0] * 2] * 2
filas[1][0] = 9
print(filas)        # [[9, 0], [9, 0]]  -> la misma fila dos veces

d = {"items": []}
e = d.copy()
e["items"].append("gema")
print(d)            # {'items': ['gema']}  -> copia superficial
```

### Encargo R01-N07-E1 · Las facturas de la herrería

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

La herrería tiene una **plantilla de factura** (un diccionario con el negocio,
el cliente y una lista de ítems vacía). Generá una factura para Kira (espada
$120, afilado $10) y otra para Bron (hacha $95) **a partir de la plantilla**,
mostralas con su total y comprobá que la plantilla quedó vacía.

#### Criterio de aprobación

- Genera cada factura con `copy.deepcopy` de la plantilla.
- Muestra las dos facturas con su total.
- Comprueba que la plantilla sigue con la lista de ítems vacía.

#### Salida esperada

```
Herrería del Roble - cliente: Kira
   espada     $  120
   afilado    $   10
   TOTAL      $  130
Herrería del Roble - cliente: Bron
   hacha      $   95
   TOTAL      $   95
¿la plantilla quedó vacía? True
```

#### Solución de referencia

```python
"""Encargo del Gremio - Facturas a partir de una plantilla.

Cada cliente necesita su PROPIA factura. Si se usara la plantilla (o una
copia superficial), todos compartirian la misma lista de items.
"""

import copy

plantilla = {"negocio": "Herrería del Roble", "cliente": "", "items": []}

clientes = {
    "Kira": [("espada", 120), ("afilado", 10)],
    "Bron": [("hacha", 95)],
}

facturas = []
for cliente, compras in clientes.items():
    factura = copy.deepcopy(plantilla)
    factura["cliente"] = cliente
    for item in compras:
        factura["items"].append(item)
    facturas.append(factura)

for f in facturas:
    total = sum([precio for nombre, precio in f["items"]])
    print(f"{f['negocio']} - cliente: {f['cliente']}")
    for nombre, precio in f["items"]:
        print(f"   {nombre:<10} ${precio:>5}")
    print(f"   {'TOTAL':<10} ${total:>5}")

print("¿la plantilla quedó vacía?", plantilla["items"] == [])
```

### Prueba del sello

#### Después de `a = [1]` y `b = a`, ¿cuántas listas hay?

**Una sola** lista, con dos nombres (`a` y `b`) que apuntan a ella.

#### ¿Qué diferencia hay entre `b = a`, `b = a.copy()` y `b = copy.deepcopy(a)`?

`b = a` no copia nada: son dos nombres para el mismo objeto. `a.copy()` copia el contenedor pero comparte lo de adentro (copia superficial). `copy.deepcopy(a)` copia todo, también lo anidado.

#### ¿Por qué `x = 5; y = x; y += 1` no cambia `x`, pero con listas sí?

Porque los números son **inmutables**: `y += 1` crea un número nuevo y `y` pasa a apuntarlo. Las listas son **mutables**: `+=` las modifica en el lugar, y los dos nombres ven el cambio.

#### ¿Qué tiene de malo `[[0] * 3] * 3`? ¿Cómo se escribe bien?

Crea **una** fila y la repite tres veces: cambiar una fila cambia "las tres". Se escribe `[[0] * 3 for _ in range(3)]`.

#### ¿Se puede modificar una lista que está dentro de una tupla?

Sí: la tupla no cambia (sigue apuntando a la misma lista), pero la lista de adentro sí se puede modificar.

### Soluciones (docente)

Material original: `17-Python/08-Referencias-Copias` (soluciones completas en `soluciones/`).

## R01-N08 · Funciones

```meta
tipo: tema
padre: R01-N07
precio: 10
criatura: troll
temas: prog.funciones
```

### Crónica

Mia está cansada de escribir el mismo hechizo de curación, runa por runa, cada vez que alguien se lastima. {mentor} le muestra un truco antiguo: escribir el hechizo **una sola vez**, ponerle un **nombre** y, desde entonces, invocarlo por su nombre diciendo a quién y cuánto curar.

—Así nacen los **conjuros**, {heroe}. Un buen conjuro hace una sola cosa y la hace bien.

### Objetivos

Definir y llamar funciones, pasarles datos de todas las formas que permite
Python, devolver resultados, documentarlas, evitar la trampa del valor por
defecto mutable y dividir un programa en funciones chicas.

### Antes de empezar

- Control de flujo (05).
- Listas, tuplas, desempaquetado (06) y diccionarios (07).
- Referencias y mutabilidad (08): explica qué pasa cuando una función recibe una
  lista.

### Explicación

#### Definir y llamar
```python
def calcular_danio(ataque, defensa):     # definición: nombre + parámetros + ':'
    danio = ataque - defensa             # cuerpo indentado
    return danio                         # resultado

golpe = calcular_danio(12, 5)            # llamada: la función se ejecuta ahora
```
- Definir una función **no la ejecuta**: solo la guarda con ese nombre.
- Los **parámetros** (`ataque`, `defensa`) son los nombres que usa la función; los
  **argumentos** (`12`, `5`) son los valores que se le pasan al llamarla.
- **`return`** devuelve un valor y **termina** la función en ese momento. Una
  función sin `return` devuelve `None`.
- La función tiene que estar **definida antes** de la línea que la llama.

#### Formas de pasar argumentos
| Forma | Ejemplo | Para qué |
|---|---|---|
| por posición | `crear_enemigo("orco", 45, 8)` | pocos argumentos, orden obvio |
| por nombre | `crear_enemigo("ogro", jefe=True)` | claridad; el orden no importa |
| valor por defecto | `def f(nombre, vida=30)` | argumentos opcionales |
| solo por nombre | `def f(objeto, *, cantidad)` | obligar a escribir `cantidad=` |
| cantidad variable | `def f(*golpes)` | llega como **tupla** |
| nombrados variables | `def f(**atributos)` | llega como **diccionario** |

Al **llamar**, `*` y `**` hacen lo contrario: `f(*lista)` pasa cada elemento como
argumento y `f(**dic)` pasa cada clave como argumento con nombre.

Los parámetros con valor por defecto van **después** de los que no tienen.

#### Devolver varios valores
`return x + dx, y + dy` devuelve **una tupla**, que se desempaqueta al recibirla:
`nx, ny = mover(3, 4, 1, -1)`.

#### Docstrings
El texto entre `"""` en la primera línea del cuerpo es la **documentación** de la
función. Explica **qué hace**, qué recibe y qué devuelve. `help(curar)` la
muestra, los editores la usan al autocompletar y también queda guardada en
`curar.__doc__`.

#### Qué recibe realmente una función (conexión con 08)
Un parámetro es **otra etiqueta al mismo objeto** que se le pasó:
- Si la función **modifica** una lista o un diccionario (`append`, `d[k] = v`),
  el cambio **se ve afuera**.
- Si **reasigna** el parámetro (`mochila = []`), solo cambia la etiqueta local;
  afuera no pasa nada.

Si una función no debería tocar los datos que recibe, que trabaje sobre una
**copia** y devuelva el resultado nuevo.

#### La trampa del valor por defecto mutable
El valor por defecto se crea **una sola vez**, cuando se define la función. Con
`def f(x, mochila=[])`, **todas las llamadas comparten la misma lista**. La forma
correcta es usar `None` y crear la lista adentro:
```python
def bien_agregar(objeto, mochila=None):
    if mochila is None:
        mochila = []
```

#### ¿Cuándo crear una función?
- Cuando un bloque de código **se repite**.
- Cuando un bloque hace **una tarea con nombre propio** ("calcular el daño",
  "mostrar el ranking"): aunque se use una sola vez, el programa se lee mejor.
- Cuando una función **se hace larga** (más de 20–30 líneas) o hace varias cosas,
  partila en funciones más chicas.

Una buena función tiene un **nombre que es un verbo** (`calcular_danio`,
`mostrar_turnos`), hace **una sola cosa**, recibe lo que necesita por parámetros
y **devuelve** el resultado, en lugar de imprimirlo o modificar variables de
afuera.

### Código de ejemplo

```python
"""09 - Funciones.

Una funcion es un bloque de codigo con NOMBRE: se define una vez y se usa
(se "llama") todas las veces que haga falta. Recibe datos (parametros) y
puede devolver un resultado (return).
"""


# =========================================================
# Definir y llamar
# =========================================================
def saludar():
    print("¡Bienvenida al Valle!")


saludar()           # llamar = nombre + parentesis
saludar()


# =========================================================
# Parametros y return
# =========================================================
def calcular_danio(ataque, defensa):
    """Devuelve el daño de un golpe. Nunca menos de 1."""
    danio = ataque - defensa
    if danio < 1:
        return 1            # return termina la funcion en ese momento
    return danio


golpe = calcular_danio(12, 5)        # el resultado se puede guardar...
print("golpe:", golpe)
print("golpe débil:", calcular_danio(3, 10))    # ...o usar directo

# Sin return, la funcion devuelve None
resultado = saludar()
print("saludar() devolvió:", resultado)


# =========================================================
# Argumentos por posicion y por nombre, valores por defecto
# =========================================================
def crear_enemigo(nombre, vida=30, ataque=5, jefe=False):
    return {"nombre": nombre, "vida": vida, "ataque": ataque, "jefe": jefe}


print(crear_enemigo("slime"))                       # usa los valores por defecto
print(crear_enemigo("orco", 45, 8))                 # por posicion
print(crear_enemigo("ogro", jefe=True, vida=90))    # por nombre: el orden no importa


# Solo por nombre: los parametros despues de * se TIENEN que nombrar
def comprar(objeto, *, cantidad, precio_unitario):
    return cantidad * precio_unitario


print("total:", comprar("poción", cantidad=3, precio_unitario=8))
# comprar("poción", 3, 8)   -> TypeError: obliga a escribir cantidad= y precio_unitario=


# =========================================================
# Devolver varios valores (en realidad, una tupla)
# =========================================================
def mover(x, y, dx, dy):
    return x + dx, y + dy


nx, ny = mover(3, 4, 1, -1)          # desempaquetado (06)
print("nueva posición:", nx, ny)


# =========================================================
# *args y **kwargs: cantidad variable de argumentos
# =========================================================
def danio_total(*golpes):            # golpes llega como TUPLA
    return sum(golpes)


print("combo:", danio_total(5, 8, 3, 10))


def describir(nombre, **atributos):  # atributos llega como DICCIONARIO
    print(f"{nombre}:")
    for clave, valor in atributos.items():
        print(f"  {clave} = {valor}")


describir("Mia", clase="maga", nivel=4, hechizo="rayo")

# Al LLAMAR, * y ** hacen lo contrario: desarman una lista o un dict en argumentos
golpes = [2, 2, 6]
print("combo:", danio_total(*golpes))
stats = {"vida": 60, "ataque": 9}
print(crear_enemigo("troll", **stats))


# =========================================================
# Docstrings: la documentacion de la funcion
# =========================================================
def curar(vida, cantidad, vida_maxima=100):
    """Cura 'cantidad' puntos sin pasarse de la vida maxima.

    Recibe la vida actual y devuelve la vida nueva.
    """
    return min(vida + cantidad, vida_maxima)


print("curada:", curar(85, 30))
print("docstring:", curar.__doc__.splitlines()[0])     # help(curar) la muestra entera


# =========================================================
# Pasar datos a una funcion: recibe una etiqueta al MISMO objeto (08)
# =========================================================
def agregar_botin(mochila, objeto):
    mochila.append(objeto)           # MODIFICA la lista que le pasaron


def reiniciar(mochila):
    mochila = []                     # REASIGNA solo la etiqueta local: afuera no cambia nada


mochila_kira = ["antorcha"]
agregar_botin(mochila_kira, "gema")
reiniciar(mochila_kira)
print("mochila de Kira:", mochila_kira)


# =========================================================
# La trampa del valor por defecto mutable
# =========================================================
# El valor por defecto se crea UNA sola vez, cuando se define la funcion.
def mal_agregar(objeto, mochila=[]):     # NO hagas esto
    mochila.append(objeto)
    return mochila


print(mal_agregar("poción"))             # ['poción']
print(mal_agregar("llave"))              # ['poción', 'llave']  <- ¡la misma lista!


def bien_agregar(objeto, mochila=None):  # la forma correcta
    if mochila is None:
        mochila = []
    mochila.append(objeto)
    return mochila


print(bien_agregar("poción"))            # ['poción']
print(bien_agregar("llave"))             # ['llave']


# =========================================================
# Dividir un programa en funciones chicas
# =========================================================
def tirar_iniciativa(nombre, agilidad):
    return agilidad * 2 + len(nombre)


def ordenar_turnos(personajes):
    """Recibe [(nombre, agilidad), ...] y devuelve los nombres en orden de turno."""
    con_iniciativa = [(tirar_iniciativa(n, a), n) for n, a in personajes]
    return [nombre for iniciativa, nombre in sorted(con_iniciativa, reverse=True)]


def mostrar_turnos(orden):
    for i, nombre in enumerate(orden, start=1):
        print(f"  turno {i}: {nombre}")


compania = [("Kira", 7), ("Bron", 4), ("Mia", 6), ("Zed", 9)]
mostrar_turnos(ordenar_turnos(compania))
```

### Salida esperada

```
¡Bienvenida al Valle!
¡Bienvenida al Valle!
golpe: 7
golpe débil: 1
¡Bienvenida al Valle!
saludar() devolvió: None
{'nombre': 'slime', 'vida': 30, 'ataque': 5, 'jefe': False}
{'nombre': 'orco', 'vida': 45, 'ataque': 8, 'jefe': False}
{'nombre': 'ogro', 'vida': 90, 'ataque': 5, 'jefe': True}
total: 24
nueva posición: 4 3
combo: 26
Mia:
  clase = maga
  nivel = 4
  hechizo = rayo
combo: 10
{'nombre': 'troll', 'vida': 60, 'ataque': 9, 'jefe': False}
curada: 100
docstring: Cura 'cantidad' puntos sin pasarse de la vida maxima.
mochila de Kira: ['antorcha', 'gema']
['poción']
['poción', 'llave']
['poción']
['llave']
  turno 1: Zed
  turno 2: Kira
  turno 3: Mia
  turno 4: Bron
```

### ¿Para qué sirve?

Las funciones son la forma de no repetirse y de dividir un problema grande en partes chicas que se prueban por separado: `calcular_iva(precio)`, `validar_dni(texto)`, `enviar_correo(destino, mensaje)`. Todo sistema real es un montón de funciones que se llaman entre sí; las bibliotecas que vas a usar (para web, datos o juegos) son colecciones de funciones que escribió otra persona.

### Errores habituales

**Goblin: faltan argumentos**
(`TypeError: f() missing 1 required positional argument: 'b'`).

**Goblin: argumentos de más o por posición cuando van por nombre**
(`TypeError: comprar() takes 1 positional argument but 3 were given`).

**Esqueleto: usar afuera una variable que se creó adentro de la función**
(`NameError: name 'x' is not defined`). Lo que se crea en una función es
**local** (se ve a fondo en 10): para usarlo afuera, **devolvelo** con `return`.

**Ogros (corre, pero hace otra cosa):**
- **Olvidar el `return`**: la función calcula todo, pero devuelve `None`.
- **Imprimir en lugar de devolver**: `print(resultado)` adentro de la función no
  permite usar el resultado afuera.
- **Olvidar los paréntesis**: `saludar` (sin `()`) no llama a la función.
- **El valor por defecto mutable** (`mochila=[]`).
- **Modificar sin querer** una lista o un diccionario que recibió la función.

### Micro-misión R01-N08-P1 · El hechizo con nombre

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: def | def nombre(): define · nombre() la llama · se escribe UNA vez y se usa muchas
recompensa: xp 10, oro 10
```

#### Escena
Llegás a las Terrazas con Tilo colgado de tu hombro. {mentor} los espera junto a una cascada.
—Cansada de escribir runa por runa el mismo hechizo, ¿no? Escribilo **una vez**, ponele **nombre** y llamalo cuando quieras.

#### Gheco sugiere
`def curar():` define una **función**: un bloque con nombre. No hace nada hasta que la **llamás** con `curar()`. Podés llamarla todas las veces que quieras.

#### Desafío
Definí `curar` y llamala dos veces.

#### Código inicial
```python
___
    print("Una luz verde cierra un raspón.")

curar()
curar()
```

#### Salida esperada
```
Una luz verde cierra un raspón.
Una luz verde cierra un raspón.
```

#### Solución
```python
def curar():
    print("Una luz verde cierra un raspón.")

curar()
curar()
```

#### Al superarla
Dos raspones de Tilo se cierran. —Me quedan como diez —se queja, pero se le escapa una sonrisa.

#### Imagen
- Terrazas verdes escalonadas con cascadas; Ofidia, de pie junto al agua, serena.
- Mia apoya la mano en el brazo de Tilo: una luz verde sale de su pergamino.
- Gheco hace de enfermero con una venda en la cola.

### Micro-misión R01-N08-P2 · A quién y cuánto

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: Parámetros | def curar(nombre, puntos): · se llama con curar("Tilo", 5) · cada llamada, sus valores
recompensa: xp 10, oro 10
```

#### Escena
—Un hechizo que siempre hace lo mismo sirve poco —dice {mentor}—. Decile **a quién** curar y **cuánto**.

#### Gheco sugiere
Entre los paréntesis de `def` van los **parámetros**: nombres que reciben los valores que le pasás al llamar.

#### Desafío
Agregá los parámetros y curá a Tilo con 5 y a Gheco con 1.

#### Código inicial
```python
def curar(___):
    print(f"{nombre} recupera {puntos} de vida.")

curar("Tilo", 5)
curar("Gheco", 1)
```

#### Salida esperada
```
Tilo recupera 5 de vida.
Gheco recupera 1 de vida.
```

#### Solución
```python
def curar(nombre, puntos):
    print(f"{nombre} recupera {puntos} de vida.")

curar("Tilo", 5)
curar("Gheco", 1)
```

#### Al superarla
—¿Y a mí por qué? —pregunta Gheco. —Por las dudas —contesta Tilo.

#### Imagen
- Dos haces de luz verde salen del pergamino: uno grande hacia Tilo, uno chiquito hacia Gheco.
- Ofidia observa, con las serpientes de su corona atentas.

### Micro-misión R01-N08-P3 · El hechizo que devuelve

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: return | return valor devuelve un resultado · sin return, la función devuelve None
recompensa: xp 15, oro 15
```

#### Escena
—Mostrar no alcanza —dice {mentor}—. Quiero que el hechizo me **dé** la vida nueva, para anotarla.

#### Gheco sugiere
`return` **devuelve** un valor a quien llamó: `nueva = curar(4, 10)`. `print` solo muestra; `return` entrega. Sin `return`, la función devuelve `None`.

#### Desafío
Hacé que `curar` devuelva la vida nueva.

#### Código inicial
```python
def curar(vida, puntos):
    ___

vida_tilo = 4
vida_tilo = curar(vida_tilo, 10)
print(f"Tilo tiene {vida_tilo} de vida.")
```

#### Salida esperada
```
Tilo tiene 14 de vida.
```

#### Solución
```python
def curar(vida, puntos):
    return vida + puntos

vida_tilo = 4
vida_tilo = curar(vida_tilo, 10)
print(f"Tilo tiene {vida_tilo} de vida.")
```

#### Al superarla
Tilo se para solo, por primera vez desde la cueva. Sin `return`, el pergamino había dicho «Tilo tiene None de vida», y Gheco casi se desmaya.

#### Imagen
- Tilo de pie por sus propios medios, con la pértiga.
- Sobre el pergamino, un número que vuelve volando hacia Mia como una flecha de luz: `return 14`.

### Micro-misión R01-N08-P4 · Por defecto, una poción chica

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: Valores por defecto | def f(x, y=10): · f(1) usa 10 · f(1, y=25) por nombre
recompensa: xp 10, oro 10
```

#### Escena
—Casi siempre curás 10 —observa Gheco—. ¿Y si el 10 viniera solo, y solo lo decís cuando es otra cosa?

#### Gheco sugiere
`def curar(vida, puntos=10):` hace que `puntos` valga 10 si no lo pasás. Y al llamar podés nombrar el argumento: `curar(4, puntos=25)`, que se lee mejor.

#### Desafío
Poné 10 por defecto y usá el nombre en la segunda llamada.

#### Código inicial
```python
def curar(vida, puntos___):
    return vida + puntos

print(curar(4))
print(curar(4, ___))
```

#### Salida esperada
```
14
29
```

#### Solución
```python
def curar(vida, puntos=10):
    return vida + puntos

print(curar(4))
print(curar(4, puntos=25))
```

#### Al superarla
{mentor} asiente. —Ya escribís hechizos como los del Valle. Subamos.

#### Imagen
- Ofidia sube por una escalera de piedra entre cascadas; Mia, Tilo y Gheco la siguen.
- En el aire, dos frascos de poción: uno chico (10) y uno grande (25).

### Micro-misión R01-N08-P5 · Dos resultados

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: Devolver varios | return a, b devuelve una tupla · se desempaqueta: x, y = f()
recompensa: xp 10, oro 10
```

#### Escena
En el segundo nivel, una fuente revisa a quien bebe y dice dos cosas: cuánta vida tiene y si está **en peligro** (menos de 10).

#### Gheco sugiere
Una función puede devolver varios valores separados por coma: `return vida, vida < 10`. Llegan como una tupla, y la desempaquetás como en la Posada: `v, peligro = revisar(7)`.

#### Desafío
Devolvé los dos valores.

#### Código inicial
```python
def revisar(vida):
    return ___

v, peligro = revisar(7)
print(f"Vida {v}. ¿En peligro? {peligro}")
```

#### Salida esperada
```
Vida 7. ¿En peligro? True
```

#### Solución
```python
def revisar(vida):
    return vida, vida < 10

v, peligro = revisar(7)
print(f"Vida {v}. ¿En peligro? {peligro}")
```

#### Al superarla
Tilo bebe. La fuente dice 14 y «no». Él insiste en que se siente en peligro igual.

#### Imagen
- Una fuente de piedra con forma de serpiente que muestra dos números de luz sobre el agua.
- Tilo bebiendo con las manos; Gheco controlando el resultado.

### Micro-misión R01-N08-P6 · Tantas pociones como quieras

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: *args | def f(*valores): recibe cualquier cantidad · adentro, valores es una tupla
recompensa: xp 15, oro 15
```

#### Escena
—¿Y si quiero tomar dos pociones? ¿Y tres? —pregunta Tilo—. ¿Hay que escribir un hechizo para cada cantidad?

#### Gheco sugiere
Con `*` antes del parámetro, la función acepta **cualquier cantidad** de valores: `def tomar(*pociones):`. Adentro, `pociones` es una tupla que podés recorrer.

#### Desafío
Completá el parámetro y el total.

#### Código inicial
```python
def tomar(___):
    total = 0
    for p in pociones:
        total += p
    return total

print(tomar(10))
print(tomar(10, 25, 5))
```

#### Salida esperada
```
10
40
```

#### Solución
```python
def tomar(*pociones):
    total = 0
    for p in pociones:
        total += p
    return total

print(tomar(10))
print(tomar(10, 25, 5))
```

#### Al superarla
—Tres juntas no —advierte {mentor}—. Dan hipo de magia. —Tilo ya las tomó.

#### Imagen
- Tilo con tres frascos vacíos y un hipo que suelta burbujas verdes.
- Ofidia se tapa la boca para no reírse.

### Micro-misión R01-N08-P7 · La bolsa que nadie vació

```meta
lugar: Las Terrazas de las Funciones
personajes: Mia, Gheco, Tilo, Ofidia
carta: Default mutable | NUNCA def f(x, bolsa=[]) · usar bolsa=None y adentro: if bolsa is None: bolsa = []
recompensa: xp 15, oro 20
item: Pociones de Curación
```

#### Escena
{mentor} te da su hechizo para armar bolsas de pociones. Lo usás para Tilo y después para Gheco… y **la bolsa de Gheco aparece con la poción de Tilo adentro**.
—Ah —dice {mentor}—. La trampa más vieja del Valle.

#### Gheco sugiere
El valor por defecto se crea **una sola vez**, cuando se define la función. Si es una lista, **todas las llamadas comparten la misma**. Usá `None` y creá la lista adentro.

#### Desafío
Arreglá la función para que cada bolsa sea nueva.

#### Código inicial
```python
def armar_bolsa(pocion, bolsa=[]):
    bolsa.append(pocion)
    return bolsa

print(armar_bolsa("vida"))
print(armar_bolsa("maná"))
```

#### Salida esperada
```
['vida']
['maná']
```

#### Solución
```python
def armar_bolsa(pocion, bolsa=None):
    if bolsa is None:
        bolsa = []
    bolsa.append(pocion)
    return bolsa

print(armar_bolsa("vida"))
print(armar_bolsa("maná"))
```

#### Al superarla
Cada uno con su bolsa, y en cada bolsa **pociones de curación** de verdad. Tilo, curado, salta en una pierna para demostrarlo.
{mentor} señala hacia arriba, donde las terrazas se meten en la montaña. —Ahí hay una cueva donde las palabras solo existen adentro. Cuidado con lo que gritan.

#### Imagen
- Dos bolsas de cuero, cada una con su poción brillante; un hilo de luz que las unía se corta.
- Tilo saltando en una pierna, curado.
- Ofidia señala hacia la boca de una cueva en lo alto de las terrazas.

### Misión R01-N08-M1 · La bolsa de dados

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí `tirar(cantidad, caras=6)`, que tire `cantidad`
dados de `caras` lados y devuelva la suma. Probá `tirar(3)` y
`tirar(2, caras=20)` con `random.seed(10)`.

#### Criterio de aprobación

- Define `tirar(cantidad, caras=6)` y devuelve la suma con `return`.
- Prueba `tirar(3)` y `tirar(2, caras=20)` con `random.seed(10)`.

#### Salida esperada

```
3 dados de 6: 10
2 dados de 20: 35
1 dado de 4: 1
```

#### Solución de referencia

```python
"""Mision 1 - La bolsa de dados."""

import random


def tirar(cantidad, caras=6):
    """Tira 'cantidad' dados de 'caras' lados y devuelve la suma."""
    total = 0
    for _ in range(cantidad):
        total += random.randint(1, caras)
    return total


random.seed(10)
print("3 dados de 6:", tirar(3))
print("2 dados de 20:", tirar(2, caras=20))
print("1 dado de 4:", tirar(1, 4))
```

### Misión R01-N08-M2 · Formar la compañía

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí `crear_compania(*nombres, vida=100)`, que
devuelva una lista de diccionarios, uno por nombre. ¿Qué devuelve si no le
pasás nombres?

#### Criterio de aprobación

- Define `crear_compania(*nombres, vida=100)`.
- Devuelve una lista de diccionarios, uno por nombre.
- Muestra qué devuelve sin nombres (una lista vacía).

#### Salida esperada

```
[{'nombre': 'Kira', 'vida': 100}, {'nombre': 'Bron', 'vida': 100}, {'nombre': 'Mia', 'vida': 100}]
[{'nombre': 'Zed', 'vida': 70}]
[]
```

#### Solución de referencia

```python
"""Mision 2 - Formar la compania."""


def crear_compania(*nombres, vida=100):
    """Devuelve una lista con un personaje (dict) por cada nombre."""
    return [{"nombre": nombre, "vida": vida} for nombre in nombres]


print(crear_compania("Kira", "Bron", "Mia"))
print(crear_compania("Zed", vida=70))
print(crear_compania())                 # sin nombres: lista vacia
```

### Misión R01-N08-M3 · La bendición del templo

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí `aplicar_buff(stats, **cambios)`, que sume
cada valor de `cambios` a la estadística correspondiente y **devuelva un
diccionario nuevo** sin modificar el original. Si la estadística no existía,
empieza en 0.

#### Criterio de aprobación

- Define `aplicar_buff(stats, **cambios)`.
- Devuelve un diccionario **nuevo** y el original queda igual.
- Una estadística que no existía empieza en 0.

#### Salida esperada

```
original: {'vida': 80, 'ataque': 12, 'defensa': 4}
bendecida: {'vida': 80, 'ataque': 17, 'defensa': 6, 'suerte': 1}
```

#### Solución de referencia

```python
"""Mision 3 - La bendicion del templo (aplicar un buff).

Devuelve un diccionario NUEVO: el original no se modifica (ver 08).
"""


def aplicar_buff(stats, **cambios):
    nuevos = stats.copy()                # copia: no tocamos el dict que nos pasaron
    for clave, extra in cambios.items():
        nuevos[clave] = nuevos.get(clave, 0) + extra
    return nuevos


kira = {"vida": 80, "ataque": 12, "defensa": 4}
bendecida = aplicar_buff(kira, ataque=5, defensa=2, suerte=1)
print("original:", kira)
print("bendecida:", bendecida)
```

### Encargo R01-N08-E1 · El precio del mercado

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El mercado necesita `precio_final(precio, *, descuento=0.0, iva=0.21)`: primero
aplica el descuento y después el IVA, redondeando a 2 decimales. `descuento` e
`iva` se pasan **solo por nombre** para no confundirlos. Documentala con un
docstring. Con $1000 da `1210.0`; con 10 % de descuento, `1089.0`.

#### Criterio de aprobación

- `descuento` e `iva` son solo por nombre (el `*` en la firma).
- Aplica primero el descuento y después el IVA, redondeando a 2 decimales.
- Tiene docstring. Con $1000 da 1210.0 y con 10 % de descuento, 1089.0.

#### Salida esperada

```
1210.0
1089.0
994.5
Aplica primero el descuento y despues el IVA.
```

#### Solución de referencia

```python
"""Encargo del Gremio - El precio final en el mercado."""


def precio_final(precio, *, descuento=0.0, iva=0.21):
    """Aplica primero el descuento y despues el IVA.

    descuento e iva van como fraccion: 0.10 = 10 %.
    Se tienen que pasar por nombre para no confundirlos.
    """
    con_descuento = precio * (1 - descuento)
    return round(con_descuento * (1 + iva), 2)


print(precio_final(1000))
print(precio_final(1000, descuento=0.10))
print(precio_final(1000, descuento=0.10, iva=0.105))
print(precio_final.__doc__.splitlines()[0])
```

### Prueba del sello

#### ¿Qué devuelve una función que no tiene `return`?

`None`.

#### ¿Qué diferencia hay entre un parámetro y un argumento?

El **parámetro** es el nombre en la definición (`def curar(vida)`); el **argumento** es el valor que se pasa al llamarla (`curar(30)`).

#### En `def f(a, *args, b=1, **kwargs)`, ¿qué llega en `args` y qué en `kwargs`?

En `args`, una **tupla** con los argumentos posicionales que sobran; en `kwargs`, un **diccionario** con los argumentos por nombre que no tienen parámetro propio.

#### ¿Para qué sirve el `*` solo en `def comprar(objeto, *, cantidad)`?

Obliga a pasar `cantidad` **por nombre**: `comprar("poción", cantidad=2)`.

#### Si una función hace `lista.append(x)` sobre la lista que recibió, ¿se ve el

Con `append`, sí: modifica la misma lista que tiene quien llamó. Con `lista = []`, no: solo cambia el nombre local, la lista de afuera queda igual.

#### ¿Por qué no se usa `[]` como valor por defecto?

Porque el valor por defecto se crea **una sola vez**, al definir la función, y todas las llamadas comparten esa misma lista. Se usa `None` y se crea la lista adentro.

### Soluciones (docente)

Material original: `17-Python/09-Funciones` (soluciones completas en `soluciones/`).

## R01-N09 · Alcance, funciones como objetos y recursión

```meta
tipo: tema
padre: R01-N08
precio: 10
criatura: esqueleto
temas: prog.alcance, prog.recursion, func.lambdas, func.orden-superior
```

### Crónica

En la Cueva de los Ecos, cada palabra que pronunciás adentro de una cámara **solo existe en esa cámara**. Mia descubre que sus conjuros se pueden **guardar en un grimorio** y pasar de mano en mano como cualquier otro objeto. Y Zed encuentra un cofre que tiene cofres adentro, que a su vez tienen más cofres…

—Para abrirlos todos, {heroe} —dice {mentor}—, hace falta un conjuro que se invoque **a sí mismo**.

### Objetivos

Saber dónde existe cada variable (alcance), usar funciones como valores
(guardarlas, pasarlas, devolverlas), escribir `lambda` para criterios de orden
y resolver problemas con recursión.

### Antes de empezar

- Funciones: parámetros, `return`, docstrings (09).
- Listas anidadas y diccionarios (06, 07).
- Referencias (08): las funciones también son objetos con etiquetas.

### Explicación

#### Alcance (*scope*): dónde existe cada nombre
Cuando usás un nombre, Python lo busca en este orden (**LEGB**):
1. **L**ocal: dentro de la función actual.
2. **E**nvolvente (*enclosing*): en la función que contiene a la actual, si hay una.
3. **G**lobal: en el archivo, afuera de toda función.
4. **B**uilt-in: lo que trae Python (`print`, `len`, `max`…).

Reglas prácticas:
- Una variable creada **adentro** de una función es **local**: nace cuando se
  llama a la función y desaparece cuando termina.
- Una función puede **leer** variables globales sin hacer nada especial.
- Si una función **asigna** un nombre, ese nombre es **local** en toda la función,
  aunque exista una global con el mismo nombre. Por eso `n += 1` sobre una global
  da `UnboundLocalError`.
- **`global x`** permite reasignar una variable global. Casi siempre es mejor
  **recibir el valor por parámetro y devolver el nuevo**: el código queda más
  claro y más fácil de probar.
- **`nonlocal x`** permite reasignar una variable de la función envolvente.
- **Cuidado con tapar nombres de Python**: `max = 10` hace que `max(...)` deje de
  funcionar en ese archivo. No uses `list`, `dict`, `max`, `sum`, `input` ni
  `id` como nombres de variables.

#### Las funciones son objetos
`def fuego(...)` crea un objeto función y le pega la etiqueta `fuego`. Por eso:
- Se puede asignar: `hechizo = fuego` (sin paréntesis) y después `hechizo("orco")`.
- Se puede guardar en listas y diccionarios: un **grimorio**
  `{"fuego": fuego, "rayo": rayo}` reemplaza una cadena larga de `if`/`elif`.
- Se puede **pasar como argumento**: `lanzar_a_todos(rayo, objetivos)`.
- Se puede **devolver** desde otra función: `crear_contador_de_golpes()` devuelve
  la función `golpear`, que además **recuerda** la variable `total` de la función
  que la creó. Eso se llama **closure** y es la base de los decoradores (23).

`fuego` es la función; `fuego("orco")` es **llamarla** y obtener su resultado.

#### `lambda`
Una función chica, sin nombre, de **una sola expresión**:
`lambda p: p["vida"]` equivale a `def f(p): return p["vida"]`.
Su uso típico es el parámetro `key=` de `sorted`, `min` y `max`, que recibe **una
función que dice por qué valor comparar**:
```python
sorted(compania, key=lambda p: p["vida"], reverse=True)
sorted(compania, key=lambda p: (-p["nivel"], p["nombre"]))   # dos criterios
max(compania, key=lambda p: p["vida"])
```
Si la lógica necesita más de una expresión, o se va a reutilizar, escribí un
`def` con nombre. Guardar una lambda en una variable (`doble = lambda x: ...`)
funciona, pero la guía de estilo prefiere `def` (se ve en 28).

#### Recursión
Una función **recursiva** se llama a sí misma con un problema **más chico**.
Siempre tiene dos partes:
1. **Caso base**: el problema es tan chico que se resuelve directo, **sin**
   llamarse de nuevo (`n == 0`, casilla que es pared, cofre vacío).
2. **Caso recursivo**: se llama a sí misma con un problema que se **acerca** al
   caso base (`n - 1`, la casilla vecina, el cofre de adentro).

Brilla con estructuras **anidadas o ramificadas**: cofres dentro de cofres,
carpetas dentro de carpetas, mapas (*flood fill*: explorar todo lo conectado),
árboles de decisiones (la IA de 41).

Cada llamada ocupa memoria hasta que termina. Python limita la profundidad
(`sys.getrecursionlimit()`, normalmente 1000): pasarse da `RecursionError`. Para
repetir algo miles de veces seguidas, un bucle es mejor.

### Código de ejemplo

```python
"""10 - Alcance, funciones como objetos y recursion.

1. Alcance: DONDE existe cada nombre (local, de la funcion que envuelve,
   global, o de Python).
2. Las funciones son valores: se guardan, se pasan y se devuelven.
3. Recursion: una funcion que se llama a si misma para resolver un problema
   mas chico.
"""

# =========================================================
# 1. Alcance (scope): regla LEGB
#    Python busca un nombre en: Local -> Envolvente -> Global -> Built-in
# =========================================================
reino = "Valle de la Serpiente"          # GLOBAL: definido afuera de toda funcion


def presentarse():
    nombre = "Kira"                       # LOCAL: solo existe dentro de presentarse
    print(f"{nombre} del {reino}")        # 'reino' no es local: lo encuentra en global


presentarse()

# Una asignacion adentro de una funcion crea una variable LOCAL nueva,
# aunque exista una global con el mismo nombre (la "tapa").
nivel = 1


def subir_nivel_mal():
    nivel = 99                            # otra variable, local; la global no cambia
    return nivel


subir_nivel_mal()
print("nivel global:", nivel)

# 'global' permite REASIGNAR la variable global. Usalo poco: es mejor devolver valores.
enemigos_derrotados = 0


def registrar_victoria():
    global enemigos_derrotados
    enemigos_derrotados += 1


registrar_victoria()
registrar_victoria()
print("derrotados:", enemigos_derrotados)

# Mejor: sin global, recibir el valor y devolver el nuevo
def sumar_victoria(total):
    return total + 1


victorias = sumar_victoria(sumar_victoria(0))
print("victorias:", victorias)

# Built-in: print, len, max, sum... tambien son nombres. Se pueden TAPAR sin querer.
print("max de la lista:", max([3, 9, 4]))
# max = 10               <- a partir de aca, max(...) daria TypeError: 'int' object is not callable


# =========================================================
# Funciones dentro de funciones y 'nonlocal'
# =========================================================
def crear_contador_de_golpes():
    total = 0                             # variable de la funcion ENVOLVENTE

    def golpear(danio):
        nonlocal total                    # reasignar la variable de la funcion de afuera
        total += danio
        return total

    return golpear                        # devuelve LA FUNCION, sin llamarla


contar = crear_contador_de_golpes()
print("golpes acumulados:", contar(5), contar(8), contar(3))
# 'golpear' recuerda 'total' aunque crear_contador_de_golpes ya termino: eso es un CLOSURE (23)


# =========================================================
# 2. Las funciones son objetos: se guardan en variables...
# =========================================================
def bola_de_fuego(objetivo):
    return f"🔥 {objetivo} arde"


def rayo(objetivo):
    return f"⚡ {objetivo} queda aturdido"


def curacion(objetivo):
    return f"✨ {objetivo} recupera vida"


hechizo = bola_de_fuego                   # SIN parentesis: la funcion misma, no su resultado
print(hechizo("el orco"))

# ...en diccionarios (una "tabla de acciones", en lugar de muchos if/elif)
grimorio = {"fuego": bola_de_fuego, "rayo": rayo, "cura": curacion}
for palabra, objetivo in [("rayo", "el goblin"), ("cura", "Bron"), ("fuego", "el slime")]:
    print(grimorio[palabra](objetivo))


# ...y se pasan como argumento a otras funciones
def lanzar_a_todos(hechizo, objetivos):
    return [hechizo(o) for o in objetivos]


print(lanzar_a_todos(rayo, ["orco", "ogro"]))

# =========================================================
# lambda: una funcion chica, sin nombre, de UNA expresion
# =========================================================
doble = lambda x: x * 2                   # igual que: def doble(x): return x * 2
print("doble de 21:", doble(21))

compania = [("Kira", 3, 90), ("Bron", 5, 140), ("Mia", 4, 70)]   # (nombre, nivel, vida)
por_nivel = sorted(compania, key=lambda p: p[1])        # key: que valor usar para ordenar
print("por nivel:", [p[0] for p in por_nivel])
print("más vida:", max(compania, key=lambda p: p[2])[0])


# =========================================================
# 3. Recursion: la funcion se llama a si misma
# =========================================================
def cuenta_regresiva(n):
    if n == 0:                            # CASO BASE: aca se corta
        print("¡se abre el portal!")
        return
    print(n)
    cuenta_regresiva(n - 1)               # CASO RECURSIVO: un problema mas chico


cuenta_regresiva(3)


def factorial(n):
    """n! = n * (n-1) * ... * 1"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


print("5! =", factorial(5))


def contar_tesoros(cofre):
    """Un cofre puede tener monedas (int) y otros cofres (listas) adentro."""
    total = 0
    for cosa in cofre:
        if isinstance(cosa, list):
            total += contar_tesoros(cosa)     # abrir el cofre de adentro
        else:
            total += cosa
    return total


cofre_del_rey = [10, [5, 5, [20]], 3, [[1, 1], 50]]
print("tesoro total:", contar_tesoros(cofre_del_rey))

# Recursion sobre un mapa: explorar todas las casillas conectadas (flood fill)
cueva = [
    list("#########"),
    list("#..#....#"),
    list("#..#.##.#"),
    list("####.#..#"),
    list("#....#..#"),
    list("#########"),
]


def explorar(mapa, f, c):
    """Marca con '~' todas las casillas de piso alcanzables desde (f, c)."""
    if mapa[f][c] != ".":                 # pared o ya visitada: caso base
        return 0
    mapa[f][c] = "~"
    return 1 + (explorar(mapa, f + 1, c) + explorar(mapa, f - 1, c)
                + explorar(mapa, f, c + 1) + explorar(mapa, f, c - 1))


print("casillas de la cámara grande:", explorar(cueva, 1, 4))
for fila in cueva:
    print("".join(fila))

# Toda llamada ocupa memoria hasta que termina. Python pone un limite de profundidad:
import sys

print("límite de recursión:", sys.getrecursionlimit())
# factorial(5000)   -> RecursionError: maximum recursion depth exceeded
```

### Salida esperada

```
Kira del Valle de la Serpiente
nivel global: 1
derrotados: 2
victorias: 2
max de la lista: 9
golpes acumulados: 5 13 16
🔥 el orco arde
⚡ el goblin queda aturdido
✨ Bron recupera vida
🔥 el slime arde
['⚡ orco queda aturdido', '⚡ ogro queda aturdido']
doble de 21: 42
por nivel: ['Kira', 'Mia', 'Bron']
más vida: Bron
3
2
1
¡se abre el portal!
5! = 120
tesoro total: 95
casillas de la cámara grande: 15
#########
#..#~~~~#
#..#~##~#
####~#~~#
#~~~~#~~#
#########
límite de recursión: 1000
```

### ¿Para qué sirve?

Pasar funciones como valores es lo que hace un botón en una app ("cuando lo toquen, llamá a esta función"), o `sorted(..., key=...)` para ordenar productos por precio. La recursión recorre estructuras que tienen cosas adentro de cosas: carpetas con subcarpetas, comentarios con respuestas, el menú de una página web, un árbol genealógico.

### Errores habituales

**Esqueleto: modificar una global sin `global`**:
```
UnboundLocalError: cannot access local variable 'n' where it is not associated with a value
```

**Goblin: tapar una función de Python** (`max = 10` y después `max([1, 2])`):
```
TypeError: 'int' object is not callable
```

**Recursión sin caso base, o que no se acerca a él**:
```
RecursionError: maximum recursion depth exceeded
```

**Ogros (corre, pero hace otra cosa):**
- Guardar `hechizo = fuego()` (con paréntesis): guardás el **resultado**, no la
  función.
- Asignar adentro de una función creyendo que cambia la global: se crea una
  local con el mismo nombre y la global queda igual.
- Un caso recursivo que **no devuelve** el resultado de la llamada
  (`factorial(n - 1)` sin `return n * ...`).

### Micro-misión R01-N09-P1 · Lo que se dice adentro

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
criatura: esqueleto
carta: Alcance local | lo que se crea dentro de una función solo existe ahí · para sacarlo: return
recompensa: xp 10, oro 10
```

#### Escena
Tilo grita «¡HOLA!» dentro de la primera cámara y el eco responde. Afuera, le pide al eco que repita… y aparece un **esqueleto**: un nombre sin cuerpo.

#### Gheco sugiere
Una variable creada **dentro** de una función es **local**: afuera no existe (por eso `NameError`). Si la necesitás afuera, **devolvela** con `return`.

#### Desafío
Hacé que la cámara devuelva el eco y guardalo afuera.

#### Código inicial
```python
def camara():
    eco = "¡HOLA! ¡hola! hola…"

camara()
print(eco)
```

#### Salida esperada
```
¡HOLA! ¡hola! hola…
```

#### Solución
```python
def camara():
    eco = "¡HOLA! ¡hola! hola…"
    return eco

eco = camara()
print(eco)
```

#### Al superarla
El esqueleto se desarma en huesitos que se caen en las piedras. Tilo los junta de recuerdo; Gheco le dice que no.

#### Imagen
- Una cámara redonda de piedra con ondas de sonido visibles rebotando en las paredes.
- Afuera, un esqueleto torpe hecho de letras sueltas se desarma.
- Tilo con las manos llenas de huesitos; Gheco negando con la cabeza.

### Micro-misión R01-N09-P2 · El contador de la cueva

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
carta: global | para CAMBIAR una variable de afuera desde una función: global x · mejor: recibir y devolver
recompensa: xp 10, oro 10
```

#### Escena
Gheco quiere contar cuántas veces gritaron en la cueva. Escribe una función que suma 1… y el pergamino se queja.

#### Gheco sugiere
Si una función **asigna** una variable, Python la toma como local, aunque exista afuera (`UnboundLocalError`). `global gritos` le avisa que es la de afuera. Funciona, pero se usa poco: casi siempre es mejor recibir el valor y devolverlo.

#### Desafío
Agregá la línea que falta.

#### Código inicial
```python
gritos = 0

def gritar():
    gritos += 1

gritar()
gritar()
print(f"Gritaron {gritos} veces")
```

#### Salida esperada
```
Gritaron 2 veces
```

#### Solución
```python
gritos = 0

def gritar():
    global gritos
    gritos += 1

gritar()
gritar()
print(f"Gritaron {gritos} veces")
```

#### Al superarla
—Funciona —dice Gheco—, pero ahora la cueva entera sabe cuánto gritamos. Prefiero que los secretos queden en su cámara.

#### Imagen
- Gheco con un ábaco de piedra contando gritos; números de eco flotan.
- Tilo con las manos alrededor de la boca, gritando.

### Micro-misión R01-N09-P3 · El grimorio de conjuros

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
carta: Funciones como valores | se guardan en variables y diccionarios · acciones["luz"]() la llama
recompensa: xp 15, oro 15
```

#### Escena
En una cámara hay un atril con un libro: cada página tiene un nombre y, al decirlo, el conjuro se lanza solo. Mia se da cuenta de que **sus** hechizos también se pueden guardar así.

#### Gheco sugiere
Una función es un valor más: se puede guardar en un diccionario **sin paréntesis** (`"luz": luz`) y llamarla después con `acciones["luz"]()`. Es una tabla de acciones: reemplaza muchos `if`.

#### Desafío
Completá la tabla y llamá al conjuro que pide la orden.

#### Código inicial
```python
def luz():
    print("La cueva se ilumina.")

def calma():
    print("Los ecos se callan.")

acciones = {"luz": ___, "calma": ___}
orden = "luz"
acciones[orden]___
```

#### Salida esperada
```
La cueva se ilumina.
```

#### Solución
```python
def luz():
    print("La cueva se ilumina.")

def calma():
    print("Los ecos se callan.")

acciones = {"luz": luz, "calma": calma}
orden = "luz"
acciones[orden]()
```

#### Al superarla
La cueva se ilumina y, por primera vez, ven el fondo: un pasillo que sube.

#### Imagen
- Un atril de piedra con un libro abierto; de sus páginas salen conjuros como luciérnagas.
- La cueva iluminada de golpe; Mia con el pergamino en alto.

### Micro-misión R01-N09-P4 · Hechizos de una línea

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
carta: lambda | lambda x: expresión · función chica sin nombre · típico en sorted(lista, key=lambda x: x[1])
recompensa: xp 15, oro 15
```

#### Escena
Para cruzar el pasillo hay que enfrentar a las criaturas de la menos a la más fuerte. Tilo tiene la lista de criaturas con su vida.

#### Gheco sugiere
`lambda c: c[1]` es una función de una línea, sin nombre. `sorted(lista, key=...)` usa esa función para saber **por qué valor** ordenar: acá, por la vida (la posición 1 de cada tupla).

#### Desafío
Ordená por vida, de menor a mayor.

#### Código inicial
```python
criaturas = [("murciélago", 8), ("goblin", 20), ("slime", 10)]
for nombre, vida in sorted(criaturas, key=___):
    print(nombre, vida)
```

#### Salida esperada
```
murciélago 8
slime 10
goblin 20
```

#### Solución
```python
criaturas = [("murciélago", 8), ("goblin", 20), ("slime", 10)]
for nombre, vida in sorted(criaturas, key=lambda c: c[1]):
    print(nombre, vida)
```

#### Al superarla
Murciélago, slime, goblin: uno por uno, cada vez más fácil porque cada vez saben más. Al final del pasillo hay un cofre.

#### Imagen
- Un pasillo de piedra que sube; tres siluetas de criaturas en fila de menor a mayor.
- Al final, un cofre que brilla.

### Micro-misión R01-N09-P5 · Cofres dentro de cofres

```meta
lugar: La Cueva de los Ecos
personajes: Mia, Gheco, Tilo
carta: Recursión | una función que se llama a sí misma · siempre con un caso que termina
recompensa: xp 15, oro 20
item: Cofre de los Ecos
```

#### Escena
Tilo abre el cofre: adentro hay monedas **y otro cofre**. Y adentro de ese, monedas y otro cofre más. —¿Cuántas monedas hay en total?

#### Gheco sugiere
Una función **recursiva** se llama a sí misma con algo más chico: si encuentra otro cofre (una lista), se cuenta a sí misma adentro. `isinstance(x, list)` pregunta si `x` es una lista. El caso que termina: los números se suman y listo.

#### Desafío
Completá la llamada recursiva.

#### Código inicial
```python
def contar(cofre):
    total = 0
    for cosa in cofre:
        if isinstance(cosa, list):
            total += ___
        else:
            total += cosa
    return total

cofre = [5, [3, [2, 1]], 4]
print(contar(cofre))
```

#### Salida esperada
```
15
```

#### Solución
```python
def contar(cofre):
    total = 0
    for cosa in cofre:
        if isinstance(cosa, list):
            total += contar(cosa)
        else:
            total += cosa
    return total

cofre = [5, [3, [2, 1]], 4]
print(contar(cofre))
```

#### Al superarla
Quince monedas. El cofre más chico, del tamaño de una nuez, se queda con vos: cuando lo acercás al oído, repite lo último que dijiste.
Tu pergamino, mientras tanto, se enrolla solo: ya es tan largo que no encontrás nada. Arriba de la cueva, en la cima de las Terrazas, está **la Casa de los Tomos**.

#### Imagen
- Una serie de cofres uno dentro de otro, abiertos como muñecas rusas, con monedas brillando en cada uno.
- Mia sostiene el cofre más pequeño junto a su oreja.
- El pergamino de Mia, larguísimo, enrollado en el piso.

### Misión R01-N09-M1 · El grimorio de Mia

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Escribí tres hechizos como funciones
`(objetivo, poder)`, guardalos en un diccionario y escribí
`lanzar(palabra, objetivo, poder=2)`, que busque el hechizo con `get` y lo
ejecute, o avise si no existe.

#### Criterio de aprobación

- Define tres hechizos como funciones `(objetivo, poder)`.
- Los guarda en un diccionario (sin paréntesis: la función, no su resultado).
- `lanzar` busca con `get` y avisa si el hechizo no existe.

#### Salida esperada

```
el ogro recibe 6 de daño de fuego
el troll queda congelado 3 turnos
Bron recupera 10 de vida
'volar' no es un hechizo conocido
```

#### Solución de referencia

```python
"""Mision 1 - El grimorio de Mia: una tabla de hechizos."""


def fuego(objetivo, poder):
    return f"{objetivo} recibe {poder * 3} de daño de fuego"


def hielo(objetivo, poder):
    return f"{objetivo} queda congelado {poder} turnos"


def curar(objetivo, poder):
    return f"{objetivo} recupera {poder * 5} de vida"


GRIMORIO = {"fuego": fuego, "hielo": hielo, "curar": curar}


def lanzar(palabra, objetivo, poder=2):
    hechizo = GRIMORIO.get(palabra)          # la FUNCION, o None si no existe
    if hechizo is None:
        return f"'{palabra}' no es un hechizo conocido"
    return hechizo(objetivo, poder)


print(lanzar("fuego", "el ogro"))
print(lanzar("hielo", "el troll", poder=3))
print(lanzar("curar", "Bron"))
print(lanzar("volar", "Mia"))
```

### Misión R01-N09-M2 · Ordenar la compañía

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con una lista de diccionarios (`nombre`, `nivel`,
`vida`), ordenala por vida (de mayor a menor), por nombre y por nivel (de
mayor a menor, desempatando por nombre), y encontrá la de menos vida. Todo
con `key=lambda`.

#### Criterio de aprobación

- Ordena por vida (de mayor a menor), por nombre y por nivel desempatando por nombre.
- Usa `key=lambda` en todos los casos.
- Encuentra la de menos vida con `min(..., key=...)`.

#### Salida esperada

```
por vida: ['Bron', 'Kira', 'Zed', 'Mia']
por nombre: ['Bron', 'Kira', 'Mia', 'Zed']
por nivel: [('Bron', 5), ('Mia', 4), ('Zed', 4), ('Kira', 3)]
la de menos vida: Mia
```

#### Solución de referencia

```python
"""Mision 2 - Ordenar la compania de varias formas (key= con lambda)."""

compania = [
    {"nombre": "Kira", "nivel": 3, "vida": 90},
    {"nombre": "Bron", "nivel": 5, "vida": 140},
    {"nombre": "Mia", "nivel": 4, "vida": 70},
    {"nombre": "Zed", "nivel": 4, "vida": 85},
]

por_vida = sorted(compania, key=lambda p: p["vida"], reverse=True)
print("por vida:", [p["nombre"] for p in por_vida])

por_nombre = sorted(compania, key=lambda p: p["nombre"])
print("por nombre:", [p["nombre"] for p in por_nombre])

# dos criterios: nivel de mayor a menor y, a igual nivel, por nombre
por_nivel = sorted(compania, key=lambda p: (-p["nivel"], p["nombre"]))
print("por nivel:", [(p["nombre"], p["nivel"]) for p in por_nivel])

print("la de menos vida:", min(compania, key=lambda p: p["vida"])["nombre"])
```

### Misión R01-N09-M3 · Las cámaras de la cueva

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Usá la función `explorar` para contar **cuántas
cámaras separadas** tiene una cueva y el tamaño de cada una. Pista: recorré
todas las casillas y, cada vez que encuentres un piso sin explorar, es una
cámara nueva.

#### Criterio de aprobación

- Recorre todas las casillas y cuenta una cámara nueva por cada piso sin explorar.
- Usa la función recursiva `explorar` para marcar cada cámara entera.
- Muestra la cantidad de cámaras (3) y el tamaño de cada una.

#### Código inicial

```python
cueva = [
    list("###########"),
    list("#..#...#..#"),
    list("#..#.#.####"),
    list("####.#....#"),
    list("#.......#.#"),
    list("###########"),
]


def explorar(mapa, f, c):
    """Marca con '~' todas las casillas de piso alcanzables desde (f, c) y devuelve cuántas son."""
    if mapa[f][c] != ".":
        return 0
    mapa[f][c] = "~"
    return 1 + (explorar(mapa, f + 1, c) + explorar(mapa, f - 1, c)
                + explorar(mapa, f, c + 1) + explorar(mapa, f, c - 1))


# Tu código: contá las cámaras separadas y el tamaño de cada una
```

#### Salida esperada

```
cámaras encontradas: 3
tamaño de cada una: [4, 18, 2]
```

#### Solución de referencia

```python
"""Mision 3 - ¿Cuantas camaras separadas tiene la cueva?

Recorrer todas las casillas: cada vez que se encuentra un piso sin explorar,
es una camara nueva; se explora entera (flood fill) para no contarla dos veces.
"""

cueva = [
    list("###########"),
    list("#..#...#..#"),
    list("#..#.#.####"),
    list("####.#....#"),
    list("#.......#.#"),
    list("###########"),
]


def explorar(mapa, f, c):
    if mapa[f][c] != ".":
        return 0
    mapa[f][c] = "~"
    return 1 + (explorar(mapa, f + 1, c) + explorar(mapa, f - 1, c)
                + explorar(mapa, f, c + 1) + explorar(mapa, f, c - 1))


camaras = []
for f in range(len(cueva)):
    for c in range(len(cueva[f])):
        if cueva[f][c] == ".":
            camaras.append(explorar(cueva, f, c))

print("cámaras encontradas:", len(camaras))
print("tamaño de cada una:", camaras)
```

### Encargo R01-N09-E1 · El archivo del escriba

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

El escriba guarda su archivo en carpetas dentro de carpetas: un diccionario
donde cada valor es un número (un archivo, en KB) u otro diccionario (una
subcarpeta). Escribí una función recursiva que calcule el **tamaño total** y otra
que muestre el árbol **con sangría** según la profundidad, con el tamaño de cada
carpeta.

#### Criterio de aprobación

- Una función recursiva calcula el tamaño total (caso base: un número).
- Otra muestra el árbol con sangría según la profundidad y el tamaño de cada carpeta.

#### Salida esperada

```
cartas.txt  12 KB
mapas/  (555 KB)
    valle.png  340 KB
    cuevas/  (215 KB)
        cueva1.png  120 KB
        cueva2.png  95 KB
cuentas/  (99 KB)
    2025.csv  48 KB
    2026.csv  51 KB
TOTAL: 666 KB
```

#### Solución de referencia

```python
"""Encargo del Gremio - El archivo del escriba: tamano total de carpetas anidadas.

Una carpeta es un dict: nombre -> tamano en KB (archivo) o otro dict (subcarpeta).
"""

archivo = {
    "cartas.txt": 12,
    "mapas": {
        "valle.png": 340,
        "cuevas": {"cueva1.png": 120, "cueva2.png": 95},
    },
    "cuentas": {"2025.csv": 48, "2026.csv": 51},
}


def tamanio(carpeta):
    total = 0
    for contenido in carpeta.values():
        if isinstance(contenido, dict):
            total += tamanio(contenido)      # recursion: sumar la subcarpeta
        else:
            total += contenido
    return total


def mostrar(carpeta, nivel=0):
    for nombre, contenido in carpeta.items():
        sangria = "    " * nivel
        if isinstance(contenido, dict):
            print(f"{sangria}{nombre}/  ({tamanio(contenido)} KB)")
            mostrar(contenido, nivel + 1)
        else:
            print(f"{sangria}{nombre}  {contenido} KB")


mostrar(archivo)
print("TOTAL:", tamanio(archivo), "KB")
```

### Prueba del sello

#### ¿En qué orden busca Python un nombre (LEGB)?

**L**ocal (la función), **E**nclosing (las funciones que la contienen), **G**lobal (el archivo) y **B**uilt-in (lo que trae Python).

#### ¿Por qué `contador += 1` adentro de una función da error si `contador` es

Porque `+=` asigna, y toda asignación adentro de una función crea una variable **local**; al leerla antes de asignarla, no existe. Se resuelve con `global contador` o, mejor, pasando el valor como parámetro y devolviendo el nuevo con `return`.

#### ¿Qué diferencia hay entre `f` y `f()`?

`f` es la función misma (un objeto que se puede guardar o pasar); `f()` la **llama** y da su resultado.

#### Escribí una `lambda` que, dado un personaje `(nombre, nivel)`, devuelva su nivel.

`lambda p: p[1]`.

#### ¿Cuáles son las dos partes de toda función recursiva?

El **caso base** (cuándo termina sin volver a llamarse) y el **caso recursivo** (se llama a sí misma con un problema más chico).

#### ¿Qué pasa si la recursión nunca llega al caso base?

Se llama sin fin hasta superar el límite de Python y aparece `RecursionError: maximum recursion depth exceeded`.

### Soluciones (docente)

Material original: `17-Python/10-Alcance-Recursion` (soluciones completas en `soluciones/`).

## R01-N10 · Módulos y paquetes

```meta
tipo: tema
padre: R01-N09
precio: 10
criatura: esqueleto
temas: prog.modulos
```

### Crónica

Tu pergamino ya es tan largo que se enrolla solo y no hay forma de encontrar nada. {mentor} te lleva a la Biblioteca del Valle, donde cada saber tiene su **tomo** (un módulo) y los tomos de un mismo tema comparten **estante** (un paquete).

—Además, {heroe}, la biblioteca ya tiene cientos de tomos escritos por otros magos. **No reinventes lo que ya está escrito**.

### Objetivos

Partir un programa en varios archivos, importar de todas las formas, armar un
paquete, entender `__name__ == "__main__"`, evitar los imports circulares y
conocer la biblioteca estándar de Python.

### Antes de empezar

- Funciones (09) y alcance (10).
- Listas y diccionarios (06, 07): los personajes del paquete `juego` son
  diccionarios.
- Ya usaste `import random` (05) y `from collections import Counter` (07): acá
  se explica qué hacen.

### Explicación

#### Módulo = un archivo `.py`
Cualquier archivo `.py` es un **módulo**. `import dados` busca `dados.py`, **lo
ejecuta una sola vez** (la primera vez que se importa) y te da acceso a sus
nombres como `dados.tirar(...)`.

#### Formas de importar
| Forma | Se usa como | Cuándo |
|---|---|---|
| `import math` | `math.sqrt(2)` | la forma más clara: se ve de dónde viene cada cosa |
| `from math import sqrt, pi` | `sqrt(2)` | pocos nombres muy usados |
| `import juego.combate as cmb` | `cmb.pelea(...)` | nombres largos; alias muy conocidos (`import numpy as np`) |
| `from math import *` | `sqrt(2)` | **evitalo**: trae todo sin avisar y puede tapar tus nombres |

Los imports van **arriba de todo** en el archivo, en este orden: primero la
biblioteca estándar, después las bibliotecas externas y al final tus módulos.

#### Paquete = una carpeta con `__init__.py`
```
juego/
  __init__.py      <- corre al hacer 'import juego'
  __main__.py      <- corre con 'python3 -m juego'
  personajes.py    <- juego.personajes
  combate.py       <- juego.combate
```
- `__init__.py` suele **re-exportar** lo principal: así se puede escribir
  `from juego import pelea` sin saber en qué archivo está.
- `__all__` lista lo que el paquete considera público.
- **Import relativo**: dentro del paquete, `from .personajes import describir`
  (el `.` significa "este paquete"). **Import absoluto**:
  `from juego.personajes import describir`. Los dos funcionan **dentro** del
  paquete; el relativo evita repetir el nombre del paquete.

#### `if __name__ == "__main__":`
Cada módulo tiene la variable `__name__`:
- Vale `"__main__"` en el archivo que **ejecutaste** (`python3 main.py`).
- Vale el **nombre del módulo** (`"juego.personajes"`) cuando se **importa**.

Por eso este bloque permite que un archivo sea a la vez **biblioteca** (se
importa sin que pase nada) y **programa** (hace algo al ejecutarlo): una prueba
rápida o una demo.

#### Cómo encuentra Python los módulos
Busca en `sys.path`, en orden:
1. **La carpeta del archivo que ejecutaste** (por eso `import dados` funciona si
   `dados.py` está al lado).
2. La biblioteca estándar.
3. Las bibliotecas instaladas con `pip` (se ve en 25).

Consecuencia: si llamás a tu archivo `random.py` o `math.py`, **tapás** el módulo
de Python. No uses nombres de módulos existentes para tus archivos.

#### `python3 -m`
`python3 -m juego` ejecuta el paquete (su `__main__.py`); `python3 -m json.tool`
ejecuta un módulo de la biblioteca. Con `-m`, Python arma los imports **desde la
carpeta actual**, como si el paquete se importara.

#### Imports circulares
Si `tienda.py` importa `inventario.py` **e** `inventario.py` importa
`tienda.py`, al arrancar uno de los dos queda **a medio cargar** y aparece:
```
ImportError: cannot import name 'stock' from partially initialized module 'inventario' (most likely due to a circular import)
```
Casi siempre significa que el diseño está enredado. **Solución**: mover lo que
comparten a un **tercer módulo** que no importe a ninguno de los dos
(`tienda → precios ← inventario`).

#### La biblioteca estándar (`stdlib.py`)
Python viene con "las pilas incluidas":
| Módulo | Para qué |
|---|---|
| `math` | raíces, `pi`, `floor`/`ceil`, `hypot`, `isclose` |
| `random` | azar: `randint`, `choice`, `sample`, `shuffle`, `uniform`, `seed` |
| `statistics` | `mean`, `median`, `mode` |
| `datetime` | fechas (`date`), fecha y hora (`datetime`), duraciones (`timedelta`), `strftime`/`strptime` |
| `decimal` | dinero y decimales **exactos** (`Decimal("0.1")`) |
| `collections` | `Counter`, `defaultdict` (07), `namedtuple`, `deque` (31) |
| `copy` | `copy`, `deepcopy` (08) |
| `pathlib`, `json`, `csv` | archivos y datos (17, 18) |
| `os`, `sys`, `shutil`, `subprocess` | el sistema operativo (36) |
| `re` | expresiones regulares (37) |

**Biblioteca estándar o externa**: la estándar viene con Python. Las externas
(`pygame`, `numpy`, `requests`…) se instalan aparte con `pip` o `apt` (25).

### Código de ejemplo

```python
"""11 - Recorrido por la biblioteca estandar ("pilas incluidas").

Python trae cientos de modulos listos para usar, sin instalar nada.
Aca, los que mas vas a necesitar al principio.
"""

import math
import random
import statistics
from collections import namedtuple
from datetime import date, datetime, timedelta
from decimal import Decimal

# =========================================================
# math: funciones matematicas
# =========================================================
print("raíz de 144:", math.sqrt(144))
print("pi:", round(math.pi, 4))
print("floor(2.7) / ceil(2.1):", math.floor(2.7), math.ceil(2.1))   # hacia abajo / hacia arriba
print("distancia de (0,0) a (3,4):", math.hypot(3, 4))
print("0.1 + 0.2 == 0.3?", 0.1 + 0.2 == 0.3, "| isclose:", math.isclose(0.1 + 0.2, 0.3))

# =========================================================
# random: azar (con semilla, para que la salida sea siempre igual)
# =========================================================
random.seed(3)
cofre = ["gema", "oro", "poción", "llave", "mapa"]
print("choice:", random.choice(cofre))           # uno al azar
print("sample:", random.sample(cofre, 2))        # 2 distintos al azar
random.shuffle(cofre)                            # mezcla la lista (la modifica)
print("shuffle:", cofre)
print("uniform:", round(random.uniform(1.0, 2.0), 3))   # decimal entre 1 y 2

# =========================================================
# statistics: estadistica basica
# =========================================================
tiempos = [182, 95, 240, 130, 95, 310]
print("media:", round(statistics.mean(tiempos), 1), "| mediana:", statistics.median(tiempos),
      "| moda:", statistics.mode(tiempos))

# =========================================================
# datetime: fechas y duraciones
# =========================================================
llegada = date(2026, 9, 7)                       # anio, mes, dia
hoy = date(2026, 9, 26)                          # fija para que la salida no cambie
print("días en el Valle:", (hoy - llegada).days)
print("dentro de 30 días:", hoy + timedelta(days=30))
print("formateada:", hoy.strftime("%d/%m/%Y"))
momento = datetime(2026, 9, 26, 21, 5)
print("hora del ritual:", momento.strftime("%H:%M"))
print("desde texto:", datetime.strptime("07/09/2026 08:30", "%d/%m/%Y %H:%M"))
# date.today() y datetime.now() dan la fecha y hora reales

# =========================================================
# decimal: cuentas de dinero EXACTAS (sin el error de float, visto en 02)
# =========================================================
print("float:", 0.1 + 0.2, "| Decimal:", Decimal("0.1") + Decimal("0.2"))
precio = Decimal("19.99")
print("3 espadas:", precio * 3)

# =========================================================
# collections.namedtuple: una tupla con nombres de campo
# =========================================================
Punto = namedtuple("Punto", ["x", "y"])
p = Punto(3, 7)
print(p, "| x =", p.x, "| y =", p[1])
```

### Salida esperada

```
raíz de 144: 12.0
pi: 3.1416
floor(2.7) / ceil(2.1): 2 3
distancia de (0,0) a (3,4): 5.0
0.1 + 0.2 == 0.3? False | isclose: True
choice: oro
sample: ['mapa', 'oro']
shuffle: ['oro', 'gema', 'mapa', 'llave', 'poción']
uniform: 1.606
media: 175.3 | mediana: 156.0 | moda: 95
días en el Valle: 19
dentro de 30 días: 2026-10-26
formateada: 26/09/2026
hora del ritual: 21:05
desde texto: 2026-09-07 08:30:00
float: 0.30000000000000004 | Decimal: 0.3
3 espadas: 59.97
Punto(x=3, y=7) | x = 3 | y = 7
```

### ¿Para qué sirve?

Ningún programa real vive en un solo archivo: una tienda online separa usuarios, productos y pagos en módulos distintos. La biblioteca estándar resuelve lo de todos los días (fechas con `datetime`, archivos con `pathlib`, dinero exacto con `decimal`, azar con `random`) y las bibliotecas externas suman el resto: web, datos, juegos. Saber importar y organizar es lo que permite trabajar en equipo.

### Errores habituales

**Esqueleto: el módulo no existe o no está donde Python busca**:
```
ModuleNotFoundError: No module named 'dragones'
```
Revisá el nombre, que el archivo esté en la misma carpeta que el que ejecutás, o
que la biblioteca esté instalada.

**Import relativo en un archivo ejecutado directamente**:
```
$ python3 juego/combate.py
ImportError: attempted relative import with no known parent package
```
Un archivo con `from .algo import ...` es parte de un paquete: ejecutá el
programa principal (`python3 main.py`) o usá `python3 -m juego`.

**Import circular**: ver la explicación de arriba.

**Ogros (corre, pero hace otra cosa):**
- **Un archivo tuyo que se llama como un módulo de Python** (`random.py`):
  `import random` importa el tuyo, y `random.randint` "no existe".
- **Código suelto en un módulo** (sin `if __name__ == "__main__":`): se ejecuta
  cada vez que alguien lo importa.
- **`from x import *`**: un nombre importado tapa uno tuyo sin avisar.

### Micro-misión R01-N10-P1 · El tomo de los números

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: import | import math · math.sqrt(16) · math.ceil(2.1) → 3 · math.pi
recompensa: xp 10, oro 10
```

#### Escena
—¡Ustedes! —La Copista los recibe entre estantes que llegan al techo—. Acá cada saber tiene su **tomo**. No hace falta escribirlo todo de nuevo: se pide prestado.
Tilo quiere saber cuántos viajes de balsa necesita para 21 pasajeros si entran 5 por viaje.

#### Gheco sugiere
`import math` trae el tomo de matemática. Se usa con un punto: `math.ceil(x)` redondea **hacia arriba**, `math.sqrt(x)` es la raíz.

#### Desafío
Calculá los viajes redondeando hacia arriba.

#### Código inicial
```python
___
pasajeros = 21
lugares = 5
print(math.ceil(pasajeros / lugares))
```

#### Salida esperada
```
5
```

#### Solución
```python
import math
pasajeros = 21
lugares = 5
print(math.ceil(pasajeros / lugares))
```

#### Al superarla
—Cinco viajes —dice Tilo—. Mi papá siempre decía cuatro y dejaba a uno en la orilla.

#### Imagen
- Una biblioteca circular en la cima de las terrazas: estantes altísimos, tomos con lomos de colores, una cúpula con estrellas.
- La Copista (túnica lila, horquillas) baja un tomo con el símbolo π.
- Tilo contando con los dedos.

### Micro-misión R01-N10-P2 · Traer solo lo que usás

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: from … import | from statistics import mean · import algo as alias
recompensa: xp 10, oro 10
```

#### Escena
—No hace falta bajar el tomo entero si querés una sola página —dice la Copista—. Quiero el promedio de las vidas del Bestiario.

#### Gheco sugiere
`from statistics import mean` trae **solo** `mean`, y se usa sin el prefijo: `mean(lista)`.

#### Desafío
Traé `mean` y calculá el promedio.

#### Código inicial
```python
vidas = [10, 20, 8, 30]
print(mean(vidas))
```

#### Salida esperada
```
17
```

#### Solución
```python
from statistics import mean
vidas = [10, 20, 8, 30]
print(mean(vidas))
```

#### Al superarla
La Copista anota «17» en una ficha y la guarda en el tomo del Bestiario. —Promedio de criaturas: diecisiete. Lindo número.

#### Imagen
- Una sola página que sale volando de un tomo cerrado hacia las manos de Mia.
- La Copista anotando en una ficha.

### Micro-misión R01-N10-P3 · El calendario del viaje

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: datetime | from datetime import date, timedelta · date(2026, 10, 7) + timedelta(days=30) · .strftime("%d/%m/%Y")
recompensa: xp 15, oro 15
```

#### Escena
—Si salimos hoy, el 7 de octubre, y el viaje a la Gran Biblioteca dura 30 días… ¿qué día llegamos? —pregunta Mia.

#### Gheco sugiere
`date(año, mes, día)` es una fecha y `timedelta(days=30)`, una duración: se pueden sumar. `.strftime("%d/%m/%Y")` la muestra como día/mes/año.

#### Desafío
Calculá la llegada y mostrala en formato argentino.

#### Código inicial
```python
from datetime import date, timedelta
salida = date(2026, 10, 7)
llegada = ___
print(llegada.strftime(___))
```

#### Salida esperada
```
06/11/2026
```

#### Solución
```python
from datetime import date, timedelta
salida = date(2026, 10, 7)
llegada = salida + timedelta(days=30)
print(llegada.strftime("%d/%m/%Y"))
```

#### Al superarla
—Seis de noviembre —dice la Copista—. Si no se demoran en el Paso. —Y se queda callada, mirando por la ventana.

#### Imagen
- Un calendario de piedra con días que pasan como hojas al viento.
- La Copista mira por la ventana con preocupación.

### Micro-misión R01-N10-P4 · El vuelto exacto

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: Decimal | from decimal import Decimal · Decimal("0.1") con comillas · cuentas de dinero exactas
recompensa: xp 10, oro 10
```

#### Escena
Te acordás del vuelto de Baldo: `0.1 + 0.2` no daba `0.3`. La Copista sonríe. —Para la plata hay un tomo especial.

#### Gheco sugiere
`Decimal("0.1")` guarda el decimal **exacto** (escribilo entre comillas). Con `Decimal`, `0.1 + 0.2` da justo `0.3`.

#### Desafío
Rehacé la cuenta de Baldo con `Decimal`.

#### Código inicial
```python
a = 0.1
b = 0.2
print(a + b)
print(a + b == 0.3)
```

#### Salida esperada
```
0.3
True
```

#### Solución
```python
from decimal import Decimal
a = Decimal("0.1")
b = Decimal("0.2")
print(a + b)
print(a + b == Decimal("0.3"))
```

#### Al superarla
—La próxima vez que veas a Baldo, decíselo —ríe Gheco—. Va a tener que inventar otra excusa.

#### Imagen
- Dos monedas que se suman en el aire dando un 0.3 perfecto, sin grietas.
- Gheco riéndose a carcajadas.

### Micro-misión R01-N10-P5 · Fichas con nombre

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: namedtuple | from collections import namedtuple · Criatura = namedtuple("Criatura", "nombre vida") · c.vida
recompensa: xp 10, oro 10
item: Estante Portátil
```

#### Escena
—Las tuplas son prolijas —dice la Copista—, pero `c[1]` no dice nada. ¿No sería mejor `c.vida`?

#### Gheco sugiere
`namedtuple` crea un tipo de tupla con **nombres de campo**: `Criatura("slime", 10)` y después `c.nombre`, `c.vida`.

#### Desafío
Creá el tipo y mostrá los campos por su nombre.

#### Código inicial
```python
from collections import namedtuple
Criatura = ___
c = Criatura("slime", 10)
print(f"{c.nombre} tiene {c.vida} de vida")
```

#### Salida esperada
```
slime tiene 10 de vida
```

#### Solución
```python
from collections import namedtuple
Criatura = namedtuple("Criatura", "nombre vida")
c = Criatura("slime", 10)
print(f"{c.nombre} tiene {c.vida} de vida")
```

#### Al superarla
La Copista te deja ordenar tu pergamino en **tomos**: uno de textos, uno de listas, uno de hechizos. Por fin encontrás todo.

#### Imagen
- El pergamino de Mia se separa en tres tomos pequeños que se acomodan en un estante portátil.
- La Copista aprueba con la cabeza.

### Micro-misión R01-N10-P6 · El tomo firmado

```meta
lugar: La Casa de los Tomos
personajes: Mia, Gheco, Tilo, la Copista
carta: __name__ | if __name__ == "__main__": · lo de adentro corre solo si ejecutás ESE archivo, no si lo importan
recompensa: xp 15, oro 20
se abre: la segunda nota del viajero en el grimorio
```

#### Escena
En el estante más alto, Tilo encuentra un tomo finito con **el vitral** en el lomo. Es un módulo, escrito con la letra clarísima del viajero. Termina con una línea que Mia no entiende: `if __name__ == "__main__":`.

#### Gheco sugiere
Cada archivo tiene un nombre interno: `__name__`. Si lo **ejecutás**, vale `"__main__"`. Si otro archivo lo **importa**, vale el nombre del archivo. Por eso `if __name__ == "__main__":` separa «lo que hago si me ejecutan» de «lo que presto si me importan».

#### Desafío
Ejecutalo así como está: el pergamino es el archivo que se ejecuta. Completá la condición.

#### Código inicial
```python
def saludo():
    return "Para quien llegue."

if __name__ == ___:
    print(saludo())
```

#### Salida esperada
```
Para quien llegue.
```

#### Solución
```python
def saludo():
    return "Para quien llegue."

if __name__ == "__main__":
    print(saludo())
```

#### Al superarla
*Para quien llegue.* Es la misma frase que todavía no pudiste leer en la marca de agua de tu pergamino; lo sentís aunque no sepas por qué. Guardás el tomo en el grimorio: **la segunda nota del viajero**.
Por la ventana de la Casa se ve el **Paso** que sube al Bastión de las Escamas. Algo enorme se mueve ahí. Tiene muchas cabezas.

#### Imagen
- Un tomo finito con un vitral en el lomo, abierto en las manos de Mia; la última línea brilla.
- Por la ventana circular, a lo lejos, la silueta de una hidra de muchas cabezas sobre un paso de montaña.
- Tilo y Gheco pegados al vidrio.

### Misión R01-N10-M1 · Tu propio módulo

```meta
entrega: archivo
monedas: 4
xp: 10
entorno: local
extensiones: py, zip
```

#### Consigna

Escribí `dados.py` con `tirar(caras=6)`, `tirar_varios(cantidad, caras=6)` y `con_ventaja(caras=20)` (tira dos y se queda con el mayor), con una prueba en el bloque `__main__`. Usalo desde otro archivo con `import dados` y con `from dados import con_ventaja`.

Esta misión se resuelve **en tu compu**, porque necesita dos archivos: comprimilos en un .zip y subilo.

#### Criterio de aprobación

- `dados.py` tiene `tirar`, `tirar_varios` y `con_ventaja`, con una prueba en el bloque `if __name__ == "__main__":`.
- Otro archivo lo usa con `import dados` y con `from dados import con_ventaja`.
- Se entrega un .zip con los dos archivos (o los dos .py).

#### Solución de referencia

```python
# ===== dados.py =====
"""Mision 1 - Modulo propio 'dados': herramientas de azar reutilizables.

Se usa desde otro archivo con:   import dados
Probarlo solo:                   python3 dados.py
"""

import random


def tirar(caras=6):
    return random.randint(1, caras)


def tirar_varios(cantidad, caras=6):
    return [tirar(caras) for _ in range(cantidad)]


def con_ventaja(caras=20):
    """Tira dos dados y se queda con el mayor."""
    return max(tirar(caras), tirar(caras))


if __name__ == "__main__":
    random.seed(0)
    print("prueba de dados.py:", tirar_varios(5))

# ===== mision1_usar_dados.py =====
"""Mision 1 - Usar el modulo propio 'dados' (tiene que estar en la misma carpeta)."""

import random

import dados
from dados import con_ventaja

random.seed(42)          # dados usa el mismo modulo random: la semilla lo afecta
print("un d6:", dados.tirar())
print("tres d8:", dados.tirar_varios(3, caras=8))
print("con ventaja:", con_ventaja())
print("dados.__name__ desde acá:", dados.__name__)
```

### Misión R01-N10-M2 · El calendario de la aventura

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Con `datetime`: Kira llegó el 7/9/2026, hoy
es 26/9/2026 y la luna llena es el 26/10/2026. ¿Cuántos días lleva? ¿Cuántos
faltan? Mostrá las próximas 4 guardias (una cada 3 días) con la fecha y el día
de la semana **en castellano** (pista: `fecha.weekday()` da 0 para el lunes).

#### Criterio de aprobación

- Usa `date` y `timedelta`.
- Muestra los días de viaje (19) y los que faltan para la luna llena (30).
- Muestra las próximas 4 guardias con la fecha y el día en castellano (una lista propia con `weekday()`).

#### Salida esperada

```
días de viaje: 19
faltan para la luna llena: 30 días
  guardia 1: 29/09 (martes)
  guardia 2: 02/10 (viernes)
  guardia 3: 05/10 (lunes)
  guardia 4: 08/10 (jueves)
```

#### Solución de referencia

```python
"""Mision 2 - El calendario de la aventura (datetime)."""

from datetime import date, timedelta

inicio = date(2026, 9, 7)
luna_llena = date(2026, 10, 26)
hoy = date(2026, 9, 26)
# %A daria el dia en ingles (depende del idioma del sistema): mejor una lista propia
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

print("días de viaje:", (hoy - inicio).days)
print("faltan para la luna llena:", (luna_llena - hoy).days, "días")

# una guardia cada 3 dias, las proximas 4
for i in range(1, 5):
    guardia = hoy + timedelta(days=3 * i)
    print(f"  guardia {i}: {guardia.strftime('%d/%m')} ({DIAS[guardia.weekday()]})")
```

### Misión R01-N10-M3 · Romper el círculo

```meta
entrega: archivo
monedas: 4
xp: 10
entorno: local
extensiones: py, zip
```

#### Consigna

`tienda.py` importa `inventario.py` y viceversa, y el programa no arranca. Reorganizalo con un tercer módulo `precios` para que ninguno de los dos se importe mutuamente.

Se resuelve **en tu compu** (son varios archivos): entregá un .zip con los módulos.

#### Criterio de aprobación

- Ni `tienda.py` ni `inventario.py` se importan entre sí.
- Lo que compartían pasa a un tercer módulo `precios.py`.
- El programa arranca y funciona igual que antes.

#### Solución de referencia

```python
# ===== mision3_precios.py =====
"""Mision 3 - Romper un import circular.

Antes:  tienda.py importaba inventario.py (para ver el stock) e inventario.py
importaba tienda.py (para saber los precios). Al arrancar, Python queda con un
modulo a medio cargar y da:
    ImportError: cannot import name 'stock' from partially initialized module
    'inventario' (most likely due to a circular import)

Arreglo: lo que los dos necesitan (los precios) se mueve a un TERCER modulo,
que no importa a ninguno. Ahora tienda -> precios <- inventario.
"""

PRECIOS = {"poción": 8, "antorcha": 3, "espada": 120}


def precio(objeto):
    return PRECIOS.get(objeto, 0)

# ===== mision3_inventario.py =====
"""Mision 3 - El inventario: usa precios, sin importar la tienda."""

from mision3_precios import precio

mochila = {"poción": 3, "antorcha": 5}
valor = sum([precio(objeto) * cantidad for objeto, cantidad in mochila.items()])
print("valor de la mochila:", valor)

# ===== mision3_tienda.py =====
"""Mision 3 - La tienda: usa precios, sin importar el inventario."""

from mision3_precios import precio

carrito = ["poción", "poción", "espada"]
print("total del carrito:", sum([precio(o) for o in carrito]))
```

### Encargo R01-N10-E1 · El módulo de los comerciantes

```meta
entrega: archivo
monedas: 1
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

Los comerciantes quieren un módulo `conversiones.py` que todos puedan importar:
`celsius_a_fahrenheit(c)` y `convertir_moneda(cantidad, de, a)` entre cobre,
plata y oro (1 oro = 10 plata = 100 cobre), con `Decimal` y 2 decimales exactos.
Usalo desde otro archivo con un alias.

#### Criterio de aprobación

- `conversiones.py` tiene `celsius_a_fahrenheit(c)` y `convertir_moneda(cantidad, de, a)`.
- La moneda usa `Decimal` y 2 decimales exactos (1 oro = 10 plata = 100 cobre).
- Otro archivo lo importa con un alias (`import conversiones as conv`).

#### Solución de referencia

```python
# ===== conversiones.py =====
"""Encargo del Gremio - Modulo 'conversiones' para todos los comerciantes."""

from decimal import ROUND_HALF_UP, Decimal

# cuantas monedas de cobre vale cada moneda
TASAS = {"cobre": Decimal("1"), "plata": Decimal("10"), "oro": Decimal("100")}


def celsius_a_fahrenheit(c):
    return c * 9 / 5 + 32


def convertir_moneda(cantidad, de, a):
    """Convierte entre monedas del Valle con decimales exactos (2 decimales)."""
    en_cobre = Decimal(str(cantidad)) * TASAS[de]
    resultado = en_cobre / TASAS[a]
    return resultado.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


if __name__ == "__main__":
    print("prueba:", convertir_moneda(1, "oro", "plata"))

# ===== gremio_usar_conversiones.py =====
"""Encargo del Gremio - Dos comerciantes usan el mismo modulo."""

import conversiones as conv

print("forja a 1250 °C =", conv.celsius_a_fahrenheit(1250), "°F")
print("3.5 de oro =", conv.convertir_moneda(3.5, "oro", "plata"), "de plata")
print("47 de cobre =", conv.convertir_moneda(47, "cobre", "oro"), "de oro")
```

### Prueba del sello

#### ¿Qué diferencia hay entre `import math` y `from math import sqrt`?

`import math` trae el módulo entero y se usa con el prefijo (`math.sqrt`); `from math import sqrt` trae solo ese nombre y se usa directo (`sqrt`).

#### ¿Para qué sirve `__init__.py`? ¿Y `__main__.py`?

`__init__.py` marca una carpeta como **paquete** (y se ejecuta al importarlo); `__main__.py` es lo que se ejecuta al correr el paquete con `python -m paquete`.

#### ¿Cuánto vale `__name__` en el archivo que ejecutás? ¿Y en uno importado?

En el archivo que ejecutás vale `"__main__"`; en uno importado vale el nombre del módulo (por ejemplo `"dados"`).

#### ¿Por qué no conviene llamar `random.py` a un archivo tuyo?

Porque `import random` importaría **tu** archivo en lugar del de la biblioteca estándar (Python busca primero en la carpeta del programa).

#### ¿Qué es un import circular y cómo se resuelve?

Dos módulos que se importan entre sí: uno queda a medio cargar cuando el otro lo necesita. Se resuelve moviendo lo compartido a un tercer módulo.

#### ¿Qué diferencia hay entre la biblioteca estándar y una biblioteca externa?

La **estándar** viene con Python (`math`, `datetime`, `random`); una **externa** hay que instalarla con `pip` (por ejemplo `pygame` o `pandas`).

### Soluciones (docente)

Material original: `17-Python/11-Modulos` (soluciones completas en `soluciones/`).

El ejemplo del nodo es `stdlib.py` (corre en el navegador). El de paquetes (`main.py` + `juego/`) necesita varios archivos: mostrarlo en clase desde la carpeta original. Las misiones 1 y 3 y el encargo se entregan como archivo porque requieren varios módulos.

## R01-N11 · Jefe: la Hidra de las Mil Runas

```meta
tipo: jefe
padre: R01-N10
precio: 10
criatura: dragon
insignia: Sello de la Hidra
insignia_descripcion: Venciste a la Hidra de las Mil Runas: dominás los fundamentos de Python.
usa: prog.funciones, err.validacion, col.mapas
```

### Crónica

A la salida del Valle te espera la **Hidra de las Mil Runas**. Cada vez que le cortás una cabeza con un hechizo mal escrito, le crecen dos.

—No se la vence con un solo conjuro, {heroe} —dice {mentor}—. Se la vence con **todo** lo que aprendiste, bien ordenado: variables, decisiones, bucles, listas, diccionarios y funciones, cada cosa en su lugar.

### Objetivos

- Resolver un problema completo combinando todo lo del bloque.
- Dividir el programa en funciones chicas, cada una con una sola tarea.
- Validar lo que escribe el usuario sin que el programa se corte.

### Antes de empezar

Todos los nodos de Fundamentos. Este es un **proyecto integrador**: no hay teoría nueva.

### Explicación

#### Cómo se enfrenta a un jefe

Un problema grande asusta; varios problemas chicos, no. Antes de escribir código:

1. **Leé la consigna entera** y anotá qué datos hay (precios, inventario, oro) y qué estructura conviene para cada uno (¿lista? ¿diccionario?).
2. **Partí el problema en funciones**: una para comprar, otra para vender, otra para mostrar. Cada una recibe lo que necesita y **devuelve** el resultado.
3. **Armá el bucle principal** al final: lee una orden, decide qué función llamar y muestra el mensaje.
4. **Probá de a poco**: primero que compre, después que venda, después los errores. Usá la pestaña **Entrada** con varias órdenes, una por línea.

#### Un bucle de órdenes

Casi todos los programas interactivos tienen la misma forma:

```python
while True:
    partes = input("> ").strip().lower().split()
    if not partes:
        continue                      # línea vacía: pedir otra
    if partes[0] == "salir":
        break
    # … decidir qué hacer con partes[0], partes[1]…
```

`split()` separa la orden en palabras: `"comprar pocion 3"` → `["comprar", "pocion", "3"]`.

#### Funciones que no mienten

Una función que puede fallar (no alcanza el oro, el objeto no existe) **no debería cambiar nada** cuando falla. Revisá primero, modificá después:

```python
def comprar(inventario, oro, objeto, cantidad):
    if objeto not in PRECIOS:
        return oro, f"No vendemos {objeto}."   # nada cambió
    ...
```

### ¿Para qué sirve?

Este es el esqueleto de muchísimos programas reales: el sistema de caja de un kiosco, un gestor de stock, un bot que responde órdenes en un chat, la consola de administración de un servidor. Leer órdenes, validarlas, llamar a la función correcta y mostrar un resultado claro es lo que hace cualquier software que atiende a una persona.

### Errores habituales

La Hidra combina a todas las criaturas del bloque:

- **Goblin**: comparar `"3"` con un número. Convertí con `int()` **después** de verificar con `.isdigit()`.
- **Orco**: `partes[2]` cuando el usuario escribió solo `comprar pocion` → `IndexError`. Revisá `len(partes)` antes de usar las posiciones.
- **Orco**: `inventario[objeto]` de un objeto que no tenés → `KeyError`. Usá `inventario.get(objeto, 0)`.
- **Ogro**: descontar el oro **antes** de revisar si alcanza, y quedar con oro negativo.
- **Troll**: una función que modifica el inventario "a medias" y después falla.

### Micro-misión R01-N11-P1 · La cabeza del esqueleto

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo
criatura: esqueleto
carta: Leer un NameError | «name 'x' is not defined»: una variable mal escrita o usada antes de crearla
recompensa: xp 15, oro 15
```

#### Escena
La primera cabeza de la Hidra tiene forma de calavera. Grita `NameError` y tu hechizo de luz se apaga.

#### Gheco sugiere
Leé el error de abajo hacia arriba: dice **qué nombre** no existe. Casi siempre es una letra cambiada o una mayúscula.

#### Desafío
Encontrá el nombre mal escrito y corregilo.

#### Código inicial
```python
def ataque(fuerza, arma):
    return fuerza + arma

fuerza_mia = 12
arma_mia = 5
print(ataque(fuerza_mia, arma_Mia))
```

#### Salida esperada
```
17
```

#### Solución
```python
def ataque(fuerza, arma):
    return fuerza + arma

fuerza_mia = 12
arma_mia = 5
print(ataque(fuerza_mia, arma_mia))
```

#### Al superarla
La cabeza de calavera se deshace. La Hidra ruge con las que le quedan.

#### Imagen
- La Hidra de las Mil Runas en el paso de montaña: cuerpo de serpiente gigante, cabezas distintas; una con forma de calavera grita «NameError».
- Mia, firme, con el pergamino en alto; Tilo detrás con la pértiga; Gheco ilumina.

### Micro-misión R01-N11-P2 · La cabeza del goblin

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo
criatura: goblin
carta: Leer un TypeError | «can only concatenate str (not "int") to str»: mezclaste texto y número
recompensa: xp 15, oro 15
```

#### Escena
La segunda cabeza es verde y flaca, con sonrisa de goblin. Tu hechizo de daño explota en chispas: `TypeError`.

#### Gheco sugiere
Un `TypeError` dice que mezclaste tipos que no se combinan, como texto y número con `+`. La solución más clara: un f-string.

#### Desafío
Arreglá el mensaje del daño.

#### Código inicial
```python
danio = 17
print("Le hacés " + danio + " de daño")
```

#### Salida esperada
```
Le hacés 17 de daño
```

#### Solución
```python
danio = 17
print(f"Le hacés {danio} de daño")
```

#### Al superarla
La cabeza del goblin cae. Tilo grita de alegría y la Hidra lo mira; él se esconde detrás de vos.

#### Imagen
- Una cabeza verde de la Hidra con sonrisa de goblin explota en chispas.
- Tilo festejando y escondiéndose a la vez.

### Micro-misión R01-N11-P3 · La cabeza del orco

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo
criatura: orco
carta: Leer un IndexError | «list index out of range»: pediste una posición que no existe (se cuenta desde 0)
recompensa: xp 15, oro 15
```

#### Escena
La tercera cabeza tiene colmillos de orco. Para cortarla hay que golpear **cada** cabeza de una lista, pero tu bucle siempre se pasa de una.

#### Gheco sugiere
Si una lista tiene 3 elementos, las posiciones son 0, 1 y 2. `range(len(lista) + 1)` se pasa. Lo más simple: recorrer la lista directamente, sin posiciones.

#### Desafío
Arreglá el bucle.

#### Código inicial
```python
cabezas = ["orco", "ogro", "hidra"]
for i in range(len(cabezas) + 1):
    print(f"Golpe a la cabeza {cabezas[i]}")
```

#### Salida esperada
```
Golpe a la cabeza orco
Golpe a la cabeza ogro
Golpe a la cabeza hidra
```

#### Solución
```python
cabezas = ["orco", "ogro", "hidra"]
for cabeza in cabezas:
    print(f"Golpe a la cabeza {cabeza}")
```

#### Al superarla
La cabeza de orco cae. Quedan dos: la del ogro y la central, la más grande.

#### Imagen
- Una cabeza con colmillos de orco cae; las cabezas restantes se agitan.
- Mia corre entre las rocas del paso.

### Micro-misión R01-N11-P4 · La cabeza del ogro

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo
criatura: ogro
carta: Errores de lógica | el programa corre sin errores… y da mal · se vencen probando con un caso que sabés calcular
recompensa: xp 20, oro 20
```

#### Escena
La cabeza del ogro no grita. Tu hechizo corre, no explota, no da error… y la cabeza no cae. El promedio de tus golpes da cualquier cosa.

#### Gheco sugiere
Un **ogro** no deja traceback: el programa termina tranquilo y el resultado está mal. Se vence **probando**: con 10, 20 y 30, el promedio tiene que dar 20. ¿Da?

#### Desafío
Encontrá el error de lógica.

#### Código inicial
```python
golpes = [10, 20, 30]
promedio = sum(golpes) / len(golpes) + 1
print(f"Promedio: {promedio}")
```

#### Salida esperada
```
Promedio: 20.0
```

#### Solución
```python
golpes = [10, 20, 30]
promedio = sum(golpes) / len(golpes)
print(f"Promedio: {promedio}")
```

#### Al superarla
La cabeza del ogro se derrumba en silencio, como cayó cada uno de sus errores: sin avisar.

#### Imagen
- Una cabeza de ogro de la Hidra se derrumba sin ruido.
- Mia, concentrada, comprueba una cuenta en el pergamino con el dedo.

### Micro-misión R01-N11-P5 · La cabeza central

```meta
lugar: El Paso de la Hidra
personajes: Mia, Gheco, Tilo, Ofidia
criatura: dragón
carta: Dividir para vencer | un problema grande = funciones chicas, cada una probada
recompensa: xp 25, oro 30
```

#### Escena
Queda la cabeza central, la más grande. Cada vez que le pegás con un hechizo largo y enredado, le crecen dos. {mentor}, desde lejos, dice una sola frase:
—Dividí.

#### Gheco sugiere
Un problema grande se vence **en partes**: una función que hace una sola cosa, otra que hace otra, y una que las junta. Cada parte se prueba sola.

#### Desafío
Completá las dos funciones chicas; la tercera ya las usa.

#### Código inicial
```python
def danio(fuerza, arma):
    ___

def sigue_viva(vida):
    ___

def combate(vida, fuerza, arma):
    turnos = 0
    while sigue_viva(vida):
        vida -= danio(fuerza, arma)
        turnos += 1
    return turnos

print(f"Cae en {combate(100, 12, 5)} turnos")
```

#### Salida esperada
```
Cae en 6 turnos
```

#### Solución
```python
def danio(fuerza, arma):
    return fuerza + arma

def sigue_viva(vida):
    return vida > 0

def combate(vida, fuerza, arma):
    turnos = 0
    while sigue_viva(vida):
        vida -= danio(fuerza, arma)
        turnos += 1
    return turnos

print(f"Cae en {combate(100, 12, 5)} turnos")
```

#### Al superarla
Seis golpes limpios, uno detrás de otro. La Hidra cae y el Paso queda en silencio.
Mirás tu túnica: **las runas del borde, desde los pies hasta la cintura, brillan en violeta**. Ya no se apagan.
{mentor} se acerca despacio. —En el Valle bajo aprendiste lo más difícil: que se aprende **escribiendo**. Arriba está el Bastión de las Escamas, y adentro, la Gran Biblioteca. Ahí te esperan cosas que no vas a poder leer sin equivocarte.

#### Imagen
- La cabeza central de la Hidra se desploma en el paso de montaña; polvo y runas que se apagan.
- Mia de pie, con la túnica encendida en violeta desde los pies hasta la cintura.
- Ofidia se acerca; Tilo y Gheco abrazados de alegría.
- Al fondo, el Bastión de las Escamas recortado contra la aurora.

### Misión R01-N11-M1 · La tienda del Valle

```meta
entrega: codigo
monedas: 6
xp: 30
```

#### Consigna

Escribí la tienda del Valle. Empezás con **100 de oro** y el inventario vacío. Los precios son:

```python
PRECIOS = {"pocion": 12, "antorcha": 3, "cuerda": 5, "espada": 60}
```

El programa lee órdenes hasta que escribas `salir`:

- `comprar <objeto> <cantidad>`: descuenta el oro y suma al inventario. Si el objeto no existe o no alcanza el oro, avisa y no cambia nada.
- `vender <objeto> <cantidad>`: se vende a **la mitad** del precio (división entera). Si no tenés suficientes, avisa.
- `inventario`: muestra el oro y los objetos, ordenados y alineados.
- Cualquier otra cosa: muestra cómo se usa, sin cortar el programa.

Al salir, muestra el inventario final. Usá **una función por orden**.

#### Criterio de aprobación

- Tiene funciones separadas para comprar, vender y mostrar; el bucle principal solo decide cuál llamar.
- Nunca queda oro negativo ni cantidades negativas.
- Una orden mal escrita (objeto inexistente, cantidad que no es número, faltan palabras) muestra un aviso y el programa sigue.
- Con la entrada de ejemplo, el resultado final es 70 de oro y 2 pociones.

#### Código inicial

```python
PRECIOS = {"pocion": 12, "antorcha": 3, "cuerda": 5, "espada": 60}

inventario = {}
oro = 100

# 1. Escribí las funciones comprar, vender y mostrar.
# 2. Escribí el bucle que lee órdenes hasta "salir".
```

#### Entrada de ejemplo

```
comprar pocion 3
comprar espada 2
comprar dragon 1
vender pocion 1
comprar cuerda muchas
inventario
salir
```

#### Salida esperada

```
> Compraste 3 pocion por 36.
> No te alcanza: 2 espada cuestan 120.
> No vendemos dragon.
> Vendiste 1 pocion por 6.
> Usá: comprar <objeto> <cantidad>, vender <objeto> <cantidad>, inventario o salir.
> Oro: 70
  pocion      2
> ¡Hasta la próxima!
Oro: 70
  pocion      2
```

#### Solución de referencia

```python
"""Jefe de Fundamentos - La tienda del Valle."""

PRECIOS = {"pocion": 12, "antorcha": 3, "cuerda": 5, "espada": 60}


def comprar(inventario, oro, objeto, cantidad):
    """Devuelve el oro que queda y un mensaje. No cambia nada si no alcanza."""
    if objeto not in PRECIOS:
        return oro, f"No vendemos {objeto}."
    costo = PRECIOS[objeto] * cantidad
    if costo > oro:
        return oro, f"No te alcanza: {cantidad} {objeto} cuestan {costo}."
    inventario[objeto] = inventario.get(objeto, 0) + cantidad
    return oro - costo, f"Compraste {cantidad} {objeto} por {costo}."


def vender(inventario, oro, objeto, cantidad):
    """Se vende a la mitad del precio. No cambia nada si no tenés suficientes."""
    if inventario.get(objeto, 0) < cantidad:
        return oro, f"No tenés {cantidad} {objeto}."
    inventario[objeto] -= cantidad
    if inventario[objeto] == 0:
        del inventario[objeto]
    pago = PRECIOS[objeto] // 2 * cantidad
    return oro + pago, f"Vendiste {cantidad} {objeto} por {pago}."


def mostrar(inventario, oro):
    print(f"Oro: {oro}")
    for objeto, cantidad in sorted(inventario.items()):
        print(f"  {objeto:<10}{cantidad:>3}")


inventario = {}
oro = 100
while True:
    partes = input("> ").strip().lower().split()
    if not partes:
        continue
    orden = partes[0]
    if orden == "salir":
        break
    if orden == "inventario":
        mostrar(inventario, oro)
        continue
    if orden not in ("comprar", "vender") or len(partes) != 3 or not partes[2].isdigit():
        print("Usá: comprar <objeto> <cantidad>, vender <objeto> <cantidad>, inventario o salir.")
        continue
    objeto, cantidad = partes[1], int(partes[2])
    if orden == "comprar":
        oro, mensaje = comprar(inventario, oro, objeto, cantidad)
    else:
        oro, mensaje = vender(inventario, oro, objeto, cantidad)
    print(mensaje)

print("¡Hasta la próxima!")
mostrar(inventario, oro)
```

#### Pruebas

##### Sin oro para vender
```entrada
vender espada 1
inventario
salir
```
```salida
> No tenés 1 espada.
> Oro: 100
> ¡Hasta la próxima!
Oro: 100
```

##### Gasta todo
```entrada
comprar espada 1
comprar cuerda 8
comprar antorcha 1
inventario
salir
```
```salida
> Compraste 1 espada por 60.
> Compraste 8 cuerda por 40.
> No te alcanza: 1 antorcha cuestan 3.
> Oro: 0
  cuerda      8
  espada      1
> ¡Hasta la próxima!
Oro: 0
  cuerda      8
  espada      1
```

##### Órdenes raras
```entrada
volar
comprar
salir
```
```salida
> Usá: comprar <objeto> <cantidad>, vender <objeto> <cantidad>, inventario o salir.
> Usá: comprar <objeto> <cantidad>, vender <objeto> <cantidad>, inventario o salir.
> ¡Hasta la próxima!
Oro: 100
```

### Misión R01-N11-M2 · El informe de la batalla

```meta
entrega: codigo
monedas: 6
xp: 30
```

#### Consigna

La compañía anotó cada golpe de la batalla como una tupla `(criatura, daño, turno)`:

```python
golpes = [
    ("slime", 12, 1), ("goblin", 7, 1), ("slime", 9, 2), ("orco", 15, 2),
    ("goblin", 11, 3), ("slime", 4, 3), ("orco", 20, 4), ("hidra", 30, 4),
    ("hidra", 25, 5), ("goblin", 6, 5),
]
VIDA = {"slime": 20, "goblin": 30, "orco": 40, "hidra": 80}
```

Armá el informe:

1. Una función `danio_por_criatura(registro)` que devuelva un diccionario con el daño total de cada criatura.
2. Mostrá cada criatura con su daño, de mayor a menor, y qué porcentaje de su vida representa.
3. La criatura que recibió más golpes (con `Counter`) y el daño promedio por golpe con un decimal.
4. Una función `derrotadas(totales, vidas)` que devuelva un **conjunto** con las criaturas cuyo daño alcanzó su vida. Mostrá las derrotadas y las que siguen en pie.

#### Criterio de aprobación

- `danio_por_criatura` y `derrotadas` son funciones que reciben los datos y **devuelven** el resultado (no usan variables globales).
- El listado está ordenado de mayor a menor daño con `sorted(..., key=lambda ...)`.
- `derrotadas` devuelve un `set` y las que siguen en pie se calculan con una resta de conjuntos.

#### Salida esperada

```
Daño por criatura:
  hidra     55  (69% de su vida)
  orco      35  (88% de su vida)
  slime     25  (125% de su vida)
  goblin    24  (80% de su vida)
La más golpeada: slime
Daño promedio por golpe: 13.9
Derrotadas: ['slime']
Siguen en pie: ['goblin', 'hidra', 'orco']
```

#### Solución de referencia

```python
"""Jefe de Fundamentos - El informe de la batalla."""
from collections import Counter

# (criatura, daño que recibió, turno)
golpes = [
    ("slime", 12, 1), ("goblin", 7, 1), ("slime", 9, 2), ("orco", 15, 2),
    ("goblin", 11, 3), ("slime", 4, 3), ("orco", 20, 4), ("hidra", 30, 4),
    ("hidra", 25, 5), ("goblin", 6, 5),
]
VIDA = {"slime": 20, "goblin": 30, "orco": 40, "hidra": 80}


def danio_por_criatura(registro):
    total = {}
    for criatura, danio, _turno in registro:
        total[criatura] = total.get(criatura, 0) + danio
    return total


def derrotadas(totales, vidas):
    return {criatura for criatura, danio in totales.items() if danio >= vidas[criatura]}


totales = danio_por_criatura(golpes)
print("Daño por criatura:")
for criatura, danio in sorted(totales.items(), key=lambda par: par[1], reverse=True):
    print(f"  {criatura:<8}{danio:>4}  ({danio / VIDA[criatura]:.0%} de su vida)")

golpeadas = Counter(criatura for criatura, _d, _t in golpes)
print("La más golpeada:", golpeadas.most_common(1)[0][0])
print(f"Daño promedio por golpe: {sum(d for _c, d, _t in golpes) / len(golpes):.1f}")
print("Derrotadas:", sorted(derrotadas(totales, VIDA)))
print("Siguen en pie:", sorted(set(VIDA) - derrotadas(totales, VIDA)))
```

### Encargo R01-N11-E1 · La libreta del almacén

```meta
entrega: codigo
monedas: 2
xp: 20
```

#### Consigna

El almacén del pueblo anota los fiados en una libreta. Escribí un programa que lea órdenes hasta `cerrar`:

- `anotar <cliente> <monto>`: suma el monto a la deuda del cliente.
- `pagar <cliente> <monto>`: la resta (sin dejarla negativa).
- `libreta`: muestra los clientes que deben algo, de mayor a menor deuda, y el total.

#### Criterio de aprobación

- Usa un diccionario cliente → deuda y funciones para cada orden.
- Valida las órdenes y los montos sin cortar el programa.
- La libreta sale ordenada de mayor a menor deuda, con el total.

### Prueba del sello

#### ¿Por qué conviene que `comprar` revise todo antes de modificar el inventario?

Para que, si algo falla (no existe el objeto, no alcanza el oro), el estado quede exactamente como estaba. Si modifica primero y falla después, queda "a medias".

#### ¿Qué estructura usarías para el inventario y por qué?

Un diccionario objeto → cantidad: se busca por nombre al instante y se actualiza con `get(objeto, 0) + cantidad`.

#### ¿Cómo evitás el `IndexError` cuando el usuario escribe una orden incompleta?

Revisando `len(partes)` antes de usar `partes[1]` o `partes[2]`.

#### ¿Qué ventaja tiene que las funciones devuelvan el oro en lugar de modificar una variable global?

Se pueden probar por separado y no hay sorpresas: todo lo que cambia entra por los parámetros y sale por el `return`.

### Soluciones (docente)

Proyecto integrador nuevo (no está en la carpeta original). Tiempo estimado: una clase y media. Sugerencia: resolver en clase la primera función (`comprar`) entre todos y dejar el resto como misión.
