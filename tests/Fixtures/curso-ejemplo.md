# CURSO

```meta
slug: python-import
titulo: Python desde cero (importado)
lenguaje: python
descripcion_corta: Tu primera lengua: clara y legible.
precio_raiz: 10
dias_abono: 30
publicado: no
```

### Descripción

Aprendé Python desde el primer `print` hasta tus propios programas.

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | escama | escamas | f | Se gana aprobando misiones del Valle. | | |
| mentor.name | Ofidia | | f | Serpiente sabia del Valle. | Guarda las escamas del Valle desde siempre. | |
| world.name | Aetheria | | f | El mundo donde la magia se escribe. | | |
| beast.hydra | hidra | hidras | f | Nace de clases mal armadas. | | |

## R00-N01 · Clase 0 · Preparar el entorno

```meta
tipo: raiz
criatura: slime
```

### Crónica

Cruzás el portal y caés sobre el pasto del Valle.

### Objetivos

- Ejecutar tu primer `print()`.

### Explicación (Mia)

#### Tu primer programa

`print()` muestra texto en la pantalla.

```python
# Esto es un comentario: el título de arriba NO es una sección
print("Hola")
```

### Código de ejemplo

```python
print("Hola, mundo")
```

### Salida esperada

```
Hola, mundo
```

### ¿Para qué sirve? (Bron)

Mostrar resultados en cualquier programa.

### Errores habituales (Zed)

Si no cerrás el paréntesis aparece un slime.

### Misión R00-N01-M1 · Instalá Python

```meta
entrega: ninguna
entorno: local
xp: 5
```

#### Consigna

Instalá Python 3 y verificá la versión.

### Misión R00-N01-M2 · Tu primer programa

```meta
entrega: codigo
monedas: 10
xp: 10
```

#### Consigna

Mostrá tu nombre y tu ciudad en dos líneas.

#### Criterio de aprobación

- Usa `print()` dos veces.

#### Solución de referencia

```python
print("Kira")
print("La Rioja")
```

### Encargo R00-N01-E1 · Ticket del Gremio

```meta
monedas: 3
xp: 15
```

#### Consigna

Mostrá un ticket con tres productos.

### Prueba del sello

#### ¿Qué muestra print(1 + 1)?

2

#### ¿Dónde está el tipo de error en el traceback?

En la última línea.

### Soluciones (docente)

Tiempo estimado: 60 minutos.

# RAMA R01 · Primeros hechizos

## R01-N01 · Variables

```meta
tipo: tema
padre: R00-N01
precio: 10
criatura: esqueleto
```

### Explicación

Una variable es un nombre que apunta a un valor.

### Misión R01-N01-M1 · Guardá tu oro

```meta
monedas: 10
xp: 10
```

#### Consigna

Guardá 15 en `oro` y mostralo.

#### Criterio

- Usa una variable llamada `oro`.

#### Entrada de ejemplo

```
15
```

#### Salida esperada

```
15
```

## R01-N02 · Jefe: el Rey Slime

```meta
tipo: jefe
padre: R01-N01
precio: 10
insignia: Cazador de slimes
insignia_descripcion: Venciste al Rey Slime.
```

### Crónica

El Rey Slime bloquea el camino.

### Misión R01-N02-M1 · Ficha de personaje

```meta
entrega: codigo
monedas: 10
xp: 50
```

#### Consigna

Armá la ficha de tu héroe.

#### Criterio de aprobación

- Pide nombre y clase.

# RAMA R90 · Extras

```meta
tipo: extra
posicion: 99
```

## R90-N01 · f-strings a fondo

```meta
tipo: extra
padre: R01-N01
precio: 3
moneda: comodin
```

### Explicación

Formato de números con f-strings.

### Misión R90-N01-M1 · Ticket alineado

```meta
monedas: 0
xp: 15
```

#### Consigna

Mostrá tres precios alineados a la derecha.

#### Criterio de aprobación

- Usa `:>` en las f-strings.
