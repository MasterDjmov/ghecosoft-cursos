# CURSO

```meta
slug: python
titulo: Python: El Valle de la Serpiente
lenguaje: python
nivel: desde_cero
descripcion_corta: Python completo desde cero: de la primera runa a tus propias herramientas.
precio_raiz: 10
dias_abono: 30
destacado: si
publicado: si
```

### Descripción

Aprendé **Python completo, desde cero**. No hace falta saber programar: cada tema se explica antes de usarse.

Cada tema es un **nodo** del árbol. En cada uno leés la explicación, probás el ejemplo en el navegador y resolvés las **misiones**: al aprobarlas ganás escamas para abrir el siguiente. Cada rama termina con un **jefe**, un proyecto que junta todo lo que aprendiste.

Al final del camino principal llegás a la **Encrucijada**, de donde salen las Sendas optativas: videojuegos con pygame y Python aplicado (datos, inteligencia artificial y robótica).

> Claridad antes que complejidad. La historia motiva; la explicación técnica enseña.

### Temario

- Primeros programas, tipos y operadores
- Textos, decisiones y bucles
- Listas, tuplas, diccionarios y conjuntos
- Funciones, alcance, recursión y módulos
- Clases, herencia y polimorfismo
- Excepciones, JSON y CSV
- Generadores, programación funcional y decoradores
- Anotaciones de tipos, asyncio y rendimiento

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | escama | escamas | f | La moneda del Valle: se gana aprobando misiones obligatorias y abre los nodos del curso. | | curso |
| mentor.name | Ofidia | | f | Serpiente sabia, guardiana del Valle de la Serpiente. | Nadie sabe cuántos años tiene. Enseñó la lengua del Valle a todos los que cruzaron el portal antes que vos, y todavía se acuerda de sus errores. | curso |
| world.region | Valle de la Serpiente | | m | La región del mundo cuya lengua arcana es Python. | | curso |
| story.course_intro | Bienvenida al Valle | | f | | Cruzaste el portal y despertaste en {mundo}, {heroe}, con un pergamino en blanco en la mano.<br><br>Soy {mentor}. En este mundo la magia no se recita: **se escribe**. Todo lo que escribas en ese pergamino, el Intérprete lo va a leer y lo va a hacer realidad, línea por línea.<br><br>Cada tema que domines rompe un sello; cada misión aprobada te da escamas para abrir el siguiente. | curso |
| story.branch_completed | ¡Rama completada! | | f | | —Bien hecho, {heroe} —dice {mentor}—. Otra parte del Valle ya habla tu lengua. | curso |
| story.course_completed | ¡Dominaste la lengua del Valle! | | f | | {mentor} te entrega la última escama. —Ya no sos aprendiz, {heroe}. El Valle es tuyo. Desde la Encrucijada salen caminos que pocos recorren: elegí tu Senda. | curso |
| beast.slime | slime | slimes | m | Nace de los errores de sintaxis e indentación. | Los slimes brotan de las comillas sin cerrar, los paréntesis olvidados y las sangrías torcidas. Son débiles, pero están en todos lados: el programa ni siquiera arranca hasta que los eliminás. | curso |
| beast.goblin | goblin | goblins | m | Nace de mezclar tipos que no combinan. | Los goblins roban en silencio: suman texto con números, convierten lo que no se puede convertir. Su firma es el TypeError y el ValueError. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de los nombres que no existen. | Los esqueletos son nombres sin cuerpo: una variable mal escrita, una mayúscula de más, algo que se usa antes de crearse. Gritan NameError y AttributeError. | curso |
| beast.orc | orco | orcos | m | Nace de los índices y las claves que no existen. | Los orcos atacan cuando pedís el elemento que no está: el índice fuera de rango, la clave que nadie guardó. Su grito es IndexError o KeyError. | curso |
| beast.ogre | ogro | ogros | m | Nace de los errores de lógica: el programa corre, pero hace otra cosa. | El ogro es el más traicionero: no hay traceback ni mensaje. El programa termina tranquilo… y el resultado está mal. Solo lo vence quien prueba sus programas. | curso |
| beast.troll | troll | trolls | m | Nace del estado compartido: dos nombres que tocan el mismo objeto. | El troll vive debajo de los puentes entre variables: cambiás una lista acá y aparece cambiada allá. Se alimenta de alias, defaults mutables y variables globales. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: un problema grande hecho de problemas chicos. | Un dragón no se vence de un golpe. Se lo divide en partes, se vence cada una y recién entonces cae. | curso |

## R00-N01 · Clase 0 · Hola, Python

```meta
tipo: raiz
criatura: slime
temas: prog.entorno, prog.salida, prog.entrada
```

### Crónica

Despertás en un valle desconocido, con un pergamino en blanco en la mano. Una serpiente enorme te observa: es **{mentor}**, la guardiana del Valle.

—Acá la magia no se recita, {heroe}: se **escribe** —te dice—. Todo lo que escribas en ese pergamino, el Intérprete lo va a leer y lo va a hacer realidad, línea por línea.

### Objetivos

- Escribir y ejecutar tus primeros programas en Python.
- Mostrar texto con `print`, guardar valores en variables y pedir datos con `input`.
- **Leer los mensajes de error** (el traceback) de abajo hacia arriba.

### Antes de empezar

Nada: este es el punto de partida. En la plataforma podés ejecutar Python directamente en el navegador. Si además querés tenerlo en tu compu, instalá Python 3 (en Ubuntu ya viene: probá `python3 --version`).

### Explicación

#### Qué es Python y qué es "ejecutar"

Un programa es un archivo de texto con instrucciones. **Python** es el lenguaje en que las escribimos, y el **intérprete** es el programa que lee ese archivo y hace lo que dice, **de arriba hacia abajo, una línea por vez**. Los archivos de Python terminan en `.py`.

```bash
python3 hola.py        # el intérprete lee y ejecuta hola.py
```

#### El REPL: probar de a una línea

Si en la terminal escribís solo `python3`, se abre el **REPL** (*Read-Eval-Print Loop*). Aparece `>>>` y cada línea que escribís se ejecuta al instante. Es ideal para probar cosas chicas:

```
>>> 2 + 3
5
>>> nombre = "Kira"
>>> nombre
'Kira'
>>> exit()
```

#### `print`: mostrar en pantalla

- `print("texto")` muestra el texto y pasa a la línea siguiente.
- `print(a, b, c)` muestra varios valores separados por un espacio.
- `sep=" | "` cambia ese separador. `end=""` evita el salto de línea final.
- El texto va entre comillas: `"así"` o `'así'`. Sin comillas, Python cree que es un **nombre** de variable.

#### Comentarios y docstrings

- `# comentario`: Python lo ignora. Es para las personas que leen el código.
- `"""texto"""` al principio de un archivo es el **docstring**: la descripción del programa.

#### Variables

Una variable es un **nombre que apunta a un valor**: `oro = 15`.

- El `=` **no** significa "es igual": significa "que `oro` apunte a 15".
- Se puede reasignar: `oro = oro + 10` calcula `oro + 10` con el valor viejo y después hace que `oro` apunte al resultado.
- Nombres válidos: letras, números y `_`, sin empezar con número. Por convención se usan minúsculas con guion bajo: `vida_maxima`, no `VidaMaxima`.
- **Mayúsculas y minúsculas importan**: `vida` y `Vida` son dos nombres distintos.

#### f-strings: texto con valores adentro

`f"Tenés {oro} monedas"`: la `f` antes de las comillas permite poner **expresiones** entre `{ }`. Python las calcula y las inserta en el texto: `f"Te faltan {100 - oro}"`.

#### `input`: pedirle datos al usuario

`nombre = input("¿Cómo te llamás? ")` muestra la pregunta, espera a que el usuario escriba y apriete Enter, y guarda lo que escribió. **Siempre devuelve texto**: si el usuario escribe `17`, recibís `"17"`. Para usarlo como número: `int(input(...))` (se ve a fondo en el próximo nodo).

En la plataforma, lo que "tipea" el usuario va en la pestaña **Entrada** de la consola: una línea por cada `input()`.

#### La indentación es parte del lenguaje

Los espacios al principio de la línea **tienen significado** en Python: marcan qué líneas pertenecen a un bloque (lo vas a usar con `if` y los bucles). Una línea con espacios de más, sin motivo, es un error.

### Código de ejemplo

```python
"""Hola Python: print, comentarios, variables y f-strings."""

# Esto es un comentario: todo lo que sigue a '#' en la línea se ignora.

# --- print: mostrar texto ---
print("Hola, Codexia")
print("Kira", "despierta", "en", "el", "Valle")

# sep= cambia el separador y end= lo que va al final.
print("fuego", "agua", "tierra", sep=" | ")
print("Cargando", end="")
print("...", end="")
print(" listo")

# --- variables: un NOMBRE que apunta a un VALOR ---
nombre = "Kira"
nivel = 1
oro = 15

print("Heroína:", nombre)
print("Nivel:", nivel, "- Oro:", oro)

# Una variable se puede reasignar.
oro = oro + 10
print("Encontró un cofre. Oro:", oro)

# --- f-strings: valores incrustados entre llaves ---
print(f"{nombre} tiene {oro} monedas de oro")
print(f"Le faltan {100 - oro} para comprar una espada")

print("Fin del primer pergamino")
```

### Salida esperada

```
Hola, Codexia
Kira despierta en el Valle
fuego | agua | tierra
Cargando... listo
Heroína: Kira
Nivel: 1 - Oro: 15
Encontró un cofre. Oro: 25
Kira tiene 25 monedas de oro
Le faltan 75 para comprar una espada
Fin del primer pergamino
```

### ¿Para qué sirve?

Todo programa, por grande que sea, empieza con esto: guardar datos en variables, mostrarlos y pedirle datos a quien lo usa. Un cajero automático te pide la clave (`input`), guarda tu saldo (una variable) y te muestra un ticket (`print` con formato). Con Python se hacen páginas web, análisis de datos, inteligencia artificial, robots y juegos: todo arranca con líneas como estas.

### Errores habituales

Cuando algo sale mal, Python muestra un **pergamino de la maldición**: el *traceback*. **Leelo de abajo hacia arriba**:

1. **La última línea** dice **qué** pasó: el tipo de error y una descripción.
2. **Arriba**, `File "...", line N` dice **dónde**: el archivo y el número de línea.
3. Las marcas `^^^^` señalan la parte exacta de la línea.

**Slime: comillas sin cerrar** (`SyntaxError`). El programa no llega a ejecutarse ni una línea:

```
  File "slime.py", line 1
    print("Un slime aparece)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

**Slime: indentación de más** (`IndentationError`):

```
  File "slime.py", line 2
    vida = 30
IndentationError: unexpected indent
```

**Esqueleto: nombre que no existe** (`NameError`). Python hasta te sugiere la corrección:

```
NameError: name 'Vida' is not defined. Did you mean: 'vida'?
```

**Goblin: convertir un texto que no es un número** (`ValueError`), por ejemplo si escribís `diez` en vez de `10`:

```
ValueError: invalid literal for int() with base 10: 'diez'
```

Otros clásicos:

- **Olvidar las comillas**: `print(Hola)` → `NameError` (busca una variable `Hola`).
- **Escribir `Print`** con mayúscula → `NameError`.
- **Sumar texto y número**: `"Oro: " + 15` → `TypeError`. Usá una f-string.

### Misión R00-N01-M1 · La ficha de personaje

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Guardá en variables el **nombre**, la **clase**, el **nivel**, la **vida** y el **oro** de tu personaje, y mostralos como una ficha.

Al menos una línea tiene que usar `sep=`.

#### Criterio de aprobación

- Usa cinco variables (nombre, clase, nivel, vida y oro).
- Muestra los cinco datos en una ficha prolija, con un título.
- Al menos un `print` usa `sep=`.

#### Código inicial

```python
# Tu ficha de personaje
nombre = "Kira"
```

#### Solución de referencia

```python
nombre = "Kira"
clase = "espadachina"
nivel = 1
vida = 100
oro = 15

print("=== FICHA DE PERSONAJE ===")
print(f"Nombre: {nombre}")
print(f"Clase:  {clase}")
print(f"Nivel:  {nivel}")
print("Vida", vida, "Oro", oro, sep=" | ")
print(f"{nombre} la {clase} está lista para la aventura.")
```

### Misión R00-N01-M2 · La bolsa de oro

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Empezás con 25 de oro. Comprás una poción (8), vendés una piel de lobo (12) y pagás la posada (20).

Usá **una sola** variable `oro`, reasignala en cada paso y mostrá cuánto queda después de cada movimiento.

#### Criterio de aprobación

- Usa una sola variable `oro` y la reasigna en cada paso (`oro = oro - 8`…).
- Muestra el oro después de cada movimiento.
- El resultado final es 9.

#### Salida esperada

```
Oro inicial: 25
Compra una poción (8): quedan 17
Vende una piel de lobo (12): ahora tiene 29
Paga la posada (20): quedan 9
```

#### Solución de referencia

```python
oro = 25
print(f"Oro inicial: {oro}")

oro = oro - 8
print(f"Compra una poción (8): quedan {oro}")

oro = oro + 12
print(f"Vende una piel de lobo (12): ahora tiene {oro}")

oro = oro - 20
print(f"Paga la posada (20): quedan {oro}")
```

### Misión R00-N01-M3 · Cazar al slime

```meta
entrega: codigo
monedas: 4
xp: 10
```

#### Consigna

Este programa tiene **tres** errores. Ejecutalo, leé el traceback, corregí el error y volvé a ejecutar, hasta que funcione. Encontralos **de a uno**, leyendo cada pergamino de abajo hacia arriba.

#### Criterio de aprobación

- El programa corre sin errores.
- Se corrigieron los tres errores: la comilla sin cerrar, la indentación de más y el nombre `Vida`.

#### Código inicial

```python
print("Un slime aparece)
    vida = 30
print(f"Vida del slime: {Vida}")
```

#### Salida esperada

```
Un slime aparece
Vida del slime: 30
```

#### Solución de referencia

```python
# 1. faltaba cerrar las comillas
# 2. sobraba indentación al principio de la línea
# 3. 'Vida' con mayúscula no existe (Python distingue mayúsculas)
print("Un slime aparece")
vida = 30
print(f"Vida del slime: {vida}")
```

### Encargo R00-N01-E1 · El ticket de la panadería

```meta
entrega: codigo
monedas: 1
xp: 15
```

#### Consigna

La panadería del pueblo necesita imprimir tickets. Con tres variables (pan $1200, facturas $900, torta $4500), calculá el total y mostrá un ticket prolijo con el nombre del negocio, cada producto con su precio y el total.

#### Criterio de aprobación

- Usa una variable por producto y calcula el total con una suma.
- El ticket muestra el nombre del negocio, los tres productos y el total ($6600).

#### Solución de referencia

```python
pan = 1200
facturas = 900
torta = 4500

total = pan + facturas + torta

print("PANADERÍA EL ROBLE")
print("------------------")
print(f"Pan ........ ${pan}")
print(f"Facturas ... ${facturas}")
print(f"Torta ...... ${torta}")
print("------------------")
print(f"TOTAL ...... ${total}")
```

### Prueba del sello

#### ¿Qué diferencia hay entre `print("oro")` y `print(oro)`?

La primera muestra el texto `oro`. La segunda muestra el **valor** de la variable `oro` (y da `NameError` si no existe).

#### ¿Qué valor tiene `oro` después de `oro = 5` y `oro = oro * 2`?

`10`: el lado derecho se calcula con el valor viejo (5 × 2) y después `oro` pasa a apuntar al resultado.

#### ¿Qué tipo de dato devuelve siempre `input()`?

Texto (`str`), aunque el usuario escriba un número. Para usarlo como número hay que convertirlo con `int()` o `float()`.

#### En un traceback, ¿dónde está el tipo de error y dónde el número de línea?

El tipo de error está en la **última línea**. El número de línea está más arriba, en `File "...", line N`.

#### ¿Por qué `Vida` y `vida` no son la misma variable?

Porque Python distingue mayúsculas de minúsculas: son dos nombres distintos.

### Soluciones (docente)

Tiempo estimado: una clase de 60 a 90 minutos. Material original: `17-Python/01-Hola-Python`.

La misión 3 es clave: que lean el traceback **antes** de tocar el código. Si corrigen los tres errores de una sola vez sin ejecutar, pedirles que cuenten qué decía cada pergamino.
