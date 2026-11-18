# RAMA S03 · Senda de la Fundición de Don Péndulo: máquinas que cambian de estado

```meta
tipo: senda
posicion: 8
```

## S03-N01 · La caldera con estados

```meta
tipo: tema
padre: R03-N03
precio: 3
moneda: comodin
criatura: ogre
temas: diseno.maquina-estados
usa: cal.tipos, func.orden-superior
```

### Crónica

Don Péndulo baja con Rigel a la **fundición** del Mirador, debajo de la montaña. Ahí trabaja la fogonera, con su pala y su delantal de cuero, alimentando la caldera grande que mueve los engranajes del Planisferio.

—La caldera tiene sus humores —dice el relojero—. Está apagada, calentando, lista o rota. Y en cada estado tiene cosas distintas: cuando calienta, tiene temperatura; cuando está lista, tiene presión; cuando se rompe, tiene un motivo. El Vidriero lo anotaba todo en una pizarra. A veces la pizarra decía «apagada, 300 grados», y nadie entendía nada.

—Con una unión discriminada —dice Gheco—, esa pizarra no se puede escribir.

### Objetivos

- Describir una máquina con una unión discriminada: cada estado con sus propios datos.
- Escribir transiciones como funciones puras: reciben un estado y devuelven el siguiente.
- Aplicar una lista de pasos con `reduce` y guardar el historial.
- Ver que los estados imposibles ni siquiera compilan.

### Antes de empezar

- Uniones discriminadas (R03-N02), `never` y los guardias propios (R03-N03).

### Explicación

#### Un estado, sus datos
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number }
  | { estado: 'rota'; motivo: string };
```
Con un `boolean` y campos opcionales (`encendida`, `temperatura?`, `rota?`), se pueden escribir combinaciones sin sentido. Con la unión, **solo existen los cuatro estados de verdad**.

#### Transiciones puras
```typescript
function encender(c: Caldera): Caldera {
  if (c.estado !== 'apagada') return c;          // en otro estado, no hace nada
  return { estado: 'calentando', temperatura: 20 };
}
```
No cambian la caldera que reciben: devuelven una nueva. Así se puede guardar el historial y volver atrás.

#### Muchos pasos
```typescript
type Paso = (c: Caldera) => Caldera;
const final = pasos.reduce((c, paso) => paso(c), inicial);
```

### Código de ejemplo

```typescript
type Caldera = { estado: 'apagada' } | { estado: 'calentando'; temperatura: number };

function describir(c: Caldera): string {
  return c.estado === 'apagada' ? 'fría' : `${c.temperatura} grados`;
}
console.log(describir({ estado: 'apagada' }), '·', describir({ estado: 'calentando', temperatura: 70 }));
```

### Salida esperada

```
fría · 70 grados
```

### ¿Para qué sirve?

Casi todo lo que tiene botones es una máquina de estados: un pedido (armado, pagado, enviado, entregado), una partida (menú, jugando, pausa, fin), un formulario (escribiendo, mandando, mandado, error). Modelarlo bien evita los errores más difíciles: los de «esto no debería poder pasar».

### Errores habituales

**Ogro: un estado imposible.** `{ estado: 'apagada', temperatura: 300 }` no compila (TS2353): la apagada no tiene temperatura.

**Esqueleto: usar un dato del estado equivocado.** `c.presion` sin preguntar `c.estado === 'lista'` no compila (TS2339).

**Goblin: cambiar la caldera recibida.** Una transición devuelve una nueva: si cambia la vieja, el historial miente.

### Micro-misión S03-N01-P1 · La pizarra de la fogonera

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, Don Péndulo
criatura: ogre
carta: Unión con datos por estado | cada case usa sus datos · el never avisa el estado que falta · 'rota' tiene su motivo
recompensa: xp 10, oro 10
```

#### Escena
Rigel escribe la pizarra nueva de la fogonera: una frase por cada estado de la caldera. Se olvidó del estado **rota**, y el compilador lo encuentra.

#### Gheco sugiere
El `default` con `never` deja de compilar si falta un caso. La caldera rota tiene un `motivo`: usalo en la frase.

#### Desafío
Agregá el caso de la caldera rota.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí ``case 'rota': return `rota: ${c.motivo}`;``.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number }
  | { estado: 'rota'; motivo: string };

function pizarra(c: Caldera): string {
  switch (c.estado) {
    case 'apagada': return 'apagada';
    case 'calentando': return `calentando: ${c.temperatura} grados`;
    case 'lista': return `lista: ${c.presion} atmósferas`;
    ___
    default: {
      const nunca: never = c;
      return nunca;
    }
  }
}

const dia: Caldera[] = [
  { estado: 'apagada' },
  { estado: 'calentando', temperatura: 60 },
  { estado: 'lista', presion: 8 },
  { estado: 'rota', motivo: 'se tapó la chimenea' },
];
for (const c of dia) console.log(pizarra(c));
```

#### Salida esperada
```
apagada
calentando: 60 grados
lista: 8 atmósferas
rota: se tapó la chimenea
```

#### Solución
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number }
  | { estado: 'rota'; motivo: string };

function pizarra(c: Caldera): string {
  switch (c.estado) {
    case 'apagada': return 'apagada';
    case 'calentando': return `calentando: ${c.temperatura} grados`;
    case 'lista': return `lista: ${c.presion} atmósferas`;
    case 'rota': return `rota: ${c.motivo}`;
    default: {
      const nunca: never = c;
      return nunca;
    }
  }
}

const dia: Caldera[] = [
  { estado: 'apagada' },
  { estado: 'calentando', temperatura: 60 },
  { estado: 'lista', presion: 8 },
  { estado: 'rota', motivo: 'se tapó la chimenea' },
];
for (const c of dia) console.log(pizarra(c));
```

#### Al superarla
La fogonera lee la pizarra nueva y se ríe: —Por fin dice por qué se rompió.

#### Imagen
- Una fundición steampunk bajo la montaña: una caldera enorme de cobre con manómetros, una pizarra con cuatro renglones (sin texto legible).
- Un ogro de cuerda chiquito con un trapo tapando la chimenea.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa de relojero en un ojo) señala la pizarra; Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) escribe con tiza; Gheco persigue al ogro.

### Micro-misión S03-N01-P2 · Encender, solo si está apagada

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, Don Péndulo
carta: Transición pura | recibe una Caldera y devuelve otra · si no es su estado, devuelve la misma · nunca cambia la que recibe
recompensa: xp 10, oro 10
```

#### Escena
Si alguien aprieta **encender** con la caldera ya calentando, la vieja pizarra la volvía a 20 grados. Don Péndulo quiere que solo encienda si está apagada.

#### Gheco sugiere
Primero se pregunta: si no está apagada, se devuelve tal cual. Si está apagada, arranca a calentar en 20 grados.

#### Desafío
Completá la pregunta del principio.

#### Pasos
1. Buscá el `___` en `encender`.
2. Cambialo por `if (c.estado !== 'apagada') return c;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number };

function encender(c: Caldera): Caldera {
  ___
  return { estado: 'calentando', temperatura: 20 };
}

const mostrar = (c: Caldera) => JSON.stringify(c);
console.log(mostrar(encender({ estado: 'apagada' })));
console.log(mostrar(encender({ estado: 'calentando', temperatura: 85 })));
console.log(mostrar(encender({ estado: 'lista', presion: 9 })));
```

#### Salida esperada
```
{"estado":"calentando","temperatura":20}
{"estado":"calentando","temperatura":85}
{"estado":"lista","presion":9}
```

#### Solución
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number };

function encender(c: Caldera): Caldera {
  if (c.estado !== 'apagada') return c;
  return { estado: 'calentando', temperatura: 20 };
}

const mostrar = (c: Caldera) => JSON.stringify(c);
console.log(mostrar(encender({ estado: 'apagada' })));
console.log(mostrar(encender({ estado: 'calentando', temperatura: 85 })));
console.log(mostrar(encender({ estado: 'lista', presion: 9 })));
```

#### Al superarla
El botón de encender ya no hace macanas. Don Péndulo le da una palmada en la espalda a Rigel que casi lo tira.

#### Imagen
- Un panel de bronce con una palanca roja de encendido y un manómetro marcando caliente.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) le da una palmada a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) se tambalea; Gheco se agarra de la palanca.

### Micro-misión S03-N01-P3 · De calentando a lista

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco
carta: Cambiar de estado con datos | calentar suma grados · a los 100 pasa a lista con presion · cada estado con sus datos
recompensa: xp 10, oro 10
```

#### Escena
La fogonera echa carbón y la caldera sube de temperatura. Cuando llega a **100 grados**, pasa a estar **lista**, con 10 atmósferas de presión.

#### Gheco sugiere
Si está calentando, se suman los grados. Después se decide: con 100 o más, está lista; si no, sigue calentando con la temperatura nueva.

#### Desafío
Completá el `return` de `calentar`.

#### Pasos
1. Buscá el `___` en `calentar`.
2. Cambialo por `return t >= 100 ? { estado: 'lista', presion: 10 } : { estado: 'calentando', temperatura: t };`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number };

function calentar(c: Caldera, grados: number): Caldera {
  if (c.estado !== 'calentando') return c;
  const t = c.temperatura + grados;
  ___
}

let caldera: Caldera = { estado: 'calentando', temperatura: 20 };
for (const palada of [30, 30, 30]) {
  caldera = calentar(caldera, palada);
  console.log(JSON.stringify(caldera));
}
```

#### Salida esperada
```
{"estado":"calentando","temperatura":50}
{"estado":"calentando","temperatura":80}
{"estado":"lista","presion":10}
```

#### Solución
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number };

function calentar(c: Caldera, grados: number): Caldera {
  if (c.estado !== 'calentando') return c;
  const t = c.temperatura + grados;
  return t >= 100 ? { estado: 'lista', presion: 10 } : { estado: 'calentando', temperatura: t };
}

let caldera: Caldera = { estado: 'calentando', temperatura: 20 };
for (const palada of [30, 30, 30]) {
  caldera = calentar(caldera, palada);
  console.log(JSON.stringify(caldera));
}
```

#### Al superarla
Con la tercera palada, el silbato de la caldera suena: está lista. Los engranajes del techo empiezan a girar.

#### Imagen
- La caldera de cobre con el silbato soltando vapor y los engranajes del techo girando.
- La fogonera (mujer fuerte con delantal de cuero, pañuelo en la cabeza y una pala) echa la última palada de carbón.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) se tapa los oídos; Gheco salta con el silbato.

### Micro-misión S03-N01-P4 · El día de la caldera

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, Don Péndulo
carta: Pasos con reduce | type Paso = (c: Caldera) => Caldera · pasos.reduce((c, paso) => paso(c), inicial) · el historial se guarda
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo quiere ver el día completo de la caldera: encender, tres paladas y apagar. Rigel arma la lista de pasos y la aplica de a uno, anotando cada estado.

#### Gheco sugiere
Cada paso es una función `Caldera → Caldera`. `reduce` los aplica en orden: el resultado de uno es la entrada del siguiente. Adentro, se guarda cada estado en el historial.

Ojo: como `inicial` arranca apagada, TypeScript cree que el acumulador es **solo** «apagada». Con `reduce<Caldera>` le decís que puede ser cualquier estado de la caldera.

#### Desafío
Completá el `reduce`.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `pasos.reduce<Caldera>((c, paso) => { const nueva = paso(c); historial.push(nueva.estado); return nueva; }, inicial)`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number };
type Paso = (c: Caldera) => Caldera;

const encender: Paso = (c) => (c.estado === 'apagada' ? { estado: 'calentando', temperatura: 20 } : c);
const palada: Paso = (c) => {
  if (c.estado !== 'calentando') return c;
  const t = c.temperatura + 30;
  return t >= 100 ? { estado: 'lista', presion: 10 } : { estado: 'calentando', temperatura: t };
};
const apagar: Paso = () => ({ estado: 'apagada' });

const inicial: Caldera = { estado: 'apagada' };
const pasos: Paso[] = [encender, palada, palada, palada, apagar];
const historial: string[] = [inicial.estado];

const final = ___;

console.log(historial.join(' → '));
console.log(`Terminó: ${final.estado}`);
```

#### Salida esperada
```
apagada → calentando → calentando → calentando → lista → apagada
Terminó: apagada
```

#### Solución
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number };
type Paso = (c: Caldera) => Caldera;

const encender: Paso = (c) => (c.estado === 'apagada' ? { estado: 'calentando', temperatura: 20 } : c);
const palada: Paso = (c) => {
  if (c.estado !== 'calentando') return c;
  const t = c.temperatura + 30;
  return t >= 100 ? { estado: 'lista', presion: 10 } : { estado: 'calentando', temperatura: t };
};
const apagar: Paso = () => ({ estado: 'apagada' });

const inicial: Caldera = { estado: 'apagada' };
const pasos: Paso[] = [encender, palada, palada, palada, apagar];
const historial: string[] = [inicial.estado];

const final = pasos.reduce<Caldera>((c, paso) => { const nueva = paso(c); historial.push(nueva.estado); return nueva; }, inicial);

console.log(historial.join(' → '));
console.log(`Terminó: ${final.estado}`);
```

#### Al superarla
El día de la caldera queda escrito en una tira de papel, como un telegrama. Don Péndulo lo cuelga en la pared.

#### Imagen
- Una tira de papel larga saliendo de una máquina de escribir de bronce, con flechas dibujadas.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) cuelga la tira con una chinche.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) sostiene la punta; Gheco enredado en el papel.

### Micro-misión S03-N01-P5 · La pizarra que miente

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, Don Péndulo
criatura: skeleton
carta: Estados imposibles | { estado: 'apagada', temperatura } no compila · c.presion solo después de preguntar c.estado === 'lista'
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo encuentra la vieja pizarra del Vidriero, pasada a código. Tiene los dos errores de siempre: una caldera **apagada con temperatura** y una válvula que se abre sin preguntar si la caldera está lista.

#### Gheco sugiere
Esta misión no se ejecuta: el compilador revisa los tipos. Arreglá las dos cosas hasta que diga **Compila sin errores**:
- la caldera apagada no tiene `temperatura`: sacala;
- para usar `c.presion`, primero preguntá `c.estado === 'lista'`.

#### Desafío
Arreglá los dos errores.

#### Pasos
1. Tocá **Ejecutar**: salen dos errores con su línea.
2. Cambiá `{ estado: 'apagada', temperatura: 300 }` por `{ estado: 'apagada' }`.
3. Cambiá `return c.presion > 5;` por `return c.estado === 'lista' && c.presion > 5;`.
4. Tocá **Ejecutar**. Tiene que decir `Compila sin errores`.

#### Compilador
sí

#### Código inicial
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number };

const vieja: Caldera = { estado: 'apagada', temperatura: 300 };

function puedeAbrirValvula(c: Caldera): boolean {
  return c.presion > 5;
}

console.log(puedeAbrirValvula(vieja));
```

#### Salida esperada
```
Compila sin errores
```

#### Solución
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'lista'; presion: number };

const vieja: Caldera = { estado: 'apagada' };

function puedeAbrirValvula(c: Caldera): boolean {
  return c.estado === 'lista' && c.presion > 5;
}

console.log(puedeAbrirValvula(vieja));
```

#### Al superarla
Don Péndulo borra la pizarra vieja con la manga. —Ahora no se puede escribir una mentira —dice—. Ojalá hubiera tenido esto el Vidriero.

#### Imagen
- Una pizarra vieja con un renglón tachado y una válvula de bronce con un candado.
- Un esqueleto de alambre chiquito intentando abrir la válvula.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) borra la pizarra con la manga; Rigel (chico flaco con pecas, antiparras de latón) cierra el candado; Gheco espanta al esqueleto.

## S03-N02 · La tabla de transiciones

```meta
tipo: tema
padre: S03-N01
precio: 10
criatura: goblin
temas: diseno.maquina-estados
usa: cal.tipos, col.mapas
```

### Crónica

La fogonera tiene un tablero de botones: **encender**, **calentar**, **romper** (cuando algo sale mal), **arreglar** y **apagar**. Pero no todos los botones sirven en todos los estados: no se puede arreglar una caldera que no está rota, ni calentar una apagada.

Don Péndulo saca un cuaderno del Vidriero con una **tabla**: una fila por estado, una columna por botón, y en cada casillero, a qué estado se pasa. Los casilleros vacíos son los botones que no hacen nada.

### Objetivos

- Escribir una tabla de transiciones: `Record<Estado, Partial<Record<Evento, Estado>>>`.
- Pasar al siguiente estado con la tabla, y quedarse igual si el botón no sirve.
- Ver cómo el compilador encuentra eventos mal escritos y filas que faltan.
- Escribir eventos con datos (una unión de eventos) y una función que los aplica.
- Listar los botones que sirven en cada estado.

### Antes de empezar

- S03-N01.
- `Record` y `Partial` (R03-N04).

### Explicación

#### La tabla
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  rota: { arreglar: 'apagada' },
};
```
- `Record<Estado, …>`: tiene que haber **una fila por cada estado**.
- `Partial<Record<Evento, Estado>>`: en cada fila, **algunos** botones.

#### El siguiente
```typescript
const siguiente = (e: Estado, ev: Evento): Estado => TABLA[e][ev] ?? e;
```
Si el casillero está vacío, `TABLA[e][ev]` es `undefined` y `??` deja el estado como estaba.

#### Eventos con datos
Cuando un evento trae información (cuántos grados, por qué se rompió), se usa una unión de eventos:
```typescript
type Accion = { tipo: 'calentar'; grados: number } | { tipo: 'romper'; motivo: string } | { tipo: 'apagar' };
```

### Código de ejemplo

```typescript
type Estado = 'apagada' | 'prendida';
type Evento = 'encender' | 'apagar';
const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = { apagada: { encender: 'prendida' }, prendida: { apagar: 'apagada' } };
console.log(TABLA.apagada.encender, TABLA.apagada.apagar ?? '(no hace nada)');
```

### Salida esperada

```
prendida (no hace nada)
```

### ¿Para qué sirve?

Una tabla de transiciones se lee de un vistazo, se dibuja como un diagrama y se cambia sin tocar el resto del programa. Los videojuegos, los protocolos de red y los procesos de una empresa se describen así.

### Errores habituales

**Goblin: un evento mal escrito.** `'encendr'` no es un `Evento` (TS2345).

**Ogro: una fila que falta.** Si falta un estado en la tabla, el `Record` lo marca (TS2741).

**Troll: un botón que hace algo donde no debe.** Si el casillero tiene un destino equivocado, el compilador no lo sabe: eso se prueba ejecutando.

### Micro-misión S03-N02-P1 · El casillero vacío

```meta
lugar: El tablero de la fogonera
personajes: Rigel, Gheco
carta: siguiente con la tabla | TABLA[e][ev] ?? e · el casillero vacío deja el estado igual
recompensa: xp 10, oro 10
```

#### Escena
Rigel prueba todos los botones en orden. Algunos no deberían hacer nada.

#### Gheco sugiere
Se busca el casillero: fila del estado, columna del evento. Si está vacío, da `undefined`, y con `?? e` el estado queda igual.

#### Desafío
Completá `siguiente`.

#### Pasos
1. Buscá el `___` en `siguiente`.
2. Cambialo por `return TABLA[e][ev] ?? e;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  rota: { arreglar: 'apagada' },
};

function siguiente(e: Estado, ev: Evento): Estado {
  ___
}

let estado: Estado = 'apagada';
const botones: Evento[] = ['calentar', 'encender', 'arreglar', 'calentar', 'romper', 'apagar', 'arreglar'];
for (const b of botones) {
  const antes = estado;
  estado = siguiente(estado, b);
  console.log(`${b}: ${antes === estado ? `(nada, sigue ${estado})` : `${antes} → ${estado}`}`);
}
```

#### Salida esperada
```
calentar: (nada, sigue apagada)
encender: apagada → calentando
arreglar: (nada, sigue calentando)
calentar: calentando → lista
romper: lista → rota
apagar: (nada, sigue rota)
arreglar: rota → apagada
```

#### Solución
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  rota: { arreglar: 'apagada' },
};

function siguiente(e: Estado, ev: Evento): Estado {
  return TABLA[e][ev] ?? e;
}

let estado: Estado = 'apagada';
const botones: Evento[] = ['calentar', 'encender', 'arreglar', 'calentar', 'romper', 'apagar', 'arreglar'];
for (const b of botones) {
  const antes = estado;
  estado = siguiente(estado, b);
  console.log(`${b}: ${antes === estado ? `(nada, sigue ${estado})` : `${antes} → ${estado}`}`);
}
```

#### Al superarla
Los botones que no sirven ya no hacen nada raro. Gheco aprieta todos a la vez para probar, y la caldera ni se mueve.

#### Imagen
- Un tablero de bronce con cinco botones grandes y una tabla de casilleros grabada al lado.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) señala un casillero.
- Gheco aprieta todos los botones con las patas y la cola.

### Micro-misión S03-N02-P2 · El botón mal escrito

```meta
lugar: El tablero de la fogonera
personajes: Rigel, Gheco
criatura: goblin
carta: Eventos con nombre fijo | 'encendr' no es un Evento (TS2345) · el compilador encuentra el botón que no existe
recompensa: xp 10, oro 10
```

#### Escena
Un goblin de cuerda cambió una etiqueta del tablero: ahora dice **encendr**. En la vieja fundición, ese botón no hacía nada y nadie sabía por qué.

#### Gheco sugiere
`siguiente` solo acepta un `Evento`. Leé el error y corregí el nombre.

#### Desafío
Corregí el botón.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `'encendr'` por `'encender'`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  rota: { arreglar: 'apagada' },
};
const siguiente = (e: Estado, ev: Evento): Estado => TABLA[e][ev] ?? e;

console.log(siguiente('apagada', 'encendr'));
```

#### Salida esperada
```
calentando
```

#### Solución
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  rota: { arreglar: 'apagada' },
};
const siguiente = (e: Estado, ev: Evento): Estado => TABLA[e][ev] ?? e;

console.log(siguiente('apagada', 'encender'));
```

#### Al superarla
La etiqueta vuelve a decir **encender**. El goblin se va con la «e» robada en la boca.

#### Imagen
- Una etiqueta de bronce con letras sueltas, una de ellas en la boca de un goblin chiquito con un engranaje en la espalda.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) atornilla la etiqueta.
- Gheco persigue al goblin.

### Micro-misión S03-N02-P3 · La fila que falta

```meta
lugar: El tablero de la fogonera
personajes: Rigel, Gheco, Don Péndulo
criatura: ogre
carta: Record exige todas las filas | falta el estado 'rota' en la tabla (TS2741) · se agrega con su botón arreglar
recompensa: xp 10, oro 10
```

#### Escena
En el cuaderno del Vidriero falta una página: la de la caldera **rota**. Por eso, cuando se rompía, nadie sabía cómo arreglarla.

#### Gheco sugiere
`Record<Estado, …>` exige una fila por estado. Leé el error: dice cuál falta. Agregala con su único botón: `arreglar` lleva a `apagada`.

#### Desafío
Agregá la fila de la caldera rota.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. En el `___`, escribí `rota: { arreglar: 'apagada' },`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  ___
};
const siguiente = (e: Estado, ev: Evento): Estado => TABLA[e][ev] ?? e;

console.log(siguiente('rota', 'arreglar'));
```

#### Salida esperada
```
apagada
```

#### Solución
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  rota: { arreglar: 'apagada' },
};
const siguiente = (e: Estado, ev: Evento): Estado => TABLA[e][ev] ?? e;

console.log(siguiente('rota', 'arreglar'));
```

#### Al superarla
Don Péndulo pega una página nueva en el cuaderno del Vidriero, con su letra temblorosa: *Rota: arreglar, y vuelve a empezar.*

#### Imagen
- Un cuaderno viejo abierto con una página nueva pegada con cinta, escrita con otra letra.
- Un ogro de cuerda chiquito con la página arrancada en la mano.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) escribe; Rigel (chico flaco con pecas, antiparras de latón) sostiene el cuaderno; Gheco recupera la página.

### Micro-misión S03-N02-P4 · Botones que traen datos

```meta
lugar: El tablero de la fogonera
personajes: Rigel, Gheco
carta: Unión de acciones | type Accion = { tipo: 'calentar'; grados } | { tipo: 'romper'; motivo } | … · aplicar(c, a) con un switch
recompensa: xp 15, monedas 5
```

#### Escena
El botón **calentar** ahora tiene una perilla: cuántos grados. Y el botón **romper** pide escribir el motivo. Rigel junta todo en una sola función que recibe la caldera y la acción.

#### Gheco sugiere
Cada acción es un objeto con su `tipo` y sus datos. En el `switch`, el compilador sabe qué datos tiene cada una. Falta el caso `'romper'`: pasa a rota con el motivo de la acción.

#### Desafío
Completá el caso `'romper'`.

#### Pasos
1. Buscá el `___` en `aplicar`.
2. Cambialo por `case 'romper': return { estado: 'rota', motivo: a.motivo };`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'rota'; motivo: string };
type Accion =
  | { tipo: 'encender' }
  | { tipo: 'calentar'; grados: number }
  | { tipo: 'romper'; motivo: string };

function aplicar(c: Caldera, a: Accion): Caldera {
  switch (a.tipo) {
    case 'encender': return c.estado === 'apagada' ? { estado: 'calentando', temperatura: 20 } : c;
    case 'calentar': return c.estado === 'calentando' ? { estado: 'calentando', temperatura: c.temperatura + a.grados } : c;
    ___
  }
}

const acciones: Accion[] = [{ tipo: 'encender' }, { tipo: 'calentar', grados: 45 }, { tipo: 'romper', motivo: 'una piedra en el caño' }];
let caldera: Caldera = { estado: 'apagada' };
for (const a of acciones) {
  caldera = aplicar(caldera, a);
  console.log(`${a.tipo}: ${JSON.stringify(caldera)}`);
}
```

#### Salida esperada
```
encender: {"estado":"calentando","temperatura":20}
calentar: {"estado":"calentando","temperatura":65}
romper: {"estado":"rota","motivo":"una piedra en el caño"}
```

#### Solución
```typescript
type Caldera =
  | { estado: 'apagada' }
  | { estado: 'calentando'; temperatura: number }
  | { estado: 'rota'; motivo: string };
type Accion =
  | { tipo: 'encender' }
  | { tipo: 'calentar'; grados: number }
  | { tipo: 'romper'; motivo: string };

function aplicar(c: Caldera, a: Accion): Caldera {
  switch (a.tipo) {
    case 'encender': return c.estado === 'apagada' ? { estado: 'calentando', temperatura: 20 } : c;
    case 'calentar': return c.estado === 'calentando' ? { estado: 'calentando', temperatura: c.temperatura + a.grados } : c;
    case 'romper': return { estado: 'rota', motivo: a.motivo };
  }
}

const acciones: Accion[] = [{ tipo: 'encender' }, { tipo: 'calentar', grados: 45 }, { tipo: 'romper', motivo: 'una piedra en el caño' }];
let caldera: Caldera = { estado: 'apagada' };
for (const a of acciones) {
  caldera = aplicar(caldera, a);
  console.log(`${a.tipo}: ${JSON.stringify(caldera)}`);
}
```

#### Al superarla
La caldera se rompe… pero esta vez la pizarra dice exactamente por qué. La fogonera saca la piedra del caño con la pala.

#### Imagen
- Un caño de cobre abierto con una piedra adentro y vapor saliendo.
- La fogonera (mujer fuerte con delantal de cuero, pañuelo en la cabeza y una pala) saca la piedra.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) gira una perilla de grados; Gheco señala la piedra.

### Micro-misión S03-N02-P5 · Los botones que sirven

```meta
lugar: El tablero de la fogonera
personajes: Rigel, Gheco, Don Péndulo
carta: Object.keys tipado | Object.keys da string[] · como la tabla es nuestra, se puede decir as Evento[] · se encienden solo los que sirven
recompensa: xp 15, monedas 5
```

#### Escena
Don Péndulo quiere que en el tablero se **iluminen** solo los botones que sirven en el estado de ahora. Rigel los saca de la fila de la tabla.

#### Gheco sugiere
`Object.keys(TABLA[e])` da los botones de esa fila, pero como `string[]`: TypeScript no promete que un objeto no tenga claves de más. Acá la tabla la escribimos nosotros, así que se puede decir `as Evento[]`.

#### Desafío
Completá `permitidos`.

#### Pasos
1. Buscá el `___` en `permitidos`.
2. Cambialo por `return Object.keys(TABLA[e]) as Evento[];`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  rota: { arreglar: 'apagada' },
};

function permitidos(e: Estado): Evento[] {
  ___
}

for (const e of ['apagada', 'calentando', 'lista', 'rota'] as const) {
  console.log(`${e}: ${permitidos(e).join(', ')}`);
}
```

#### Salida esperada
```
apagada: encender
calentando: calentar, romper, apagar
lista: romper, apagar
rota: arreglar
```

#### Solución
```typescript
type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar' | 'apagar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota', apagar: 'apagada' },
  lista: { romper: 'rota', apagar: 'apagada' },
  rota: { arreglar: 'apagada' },
};

function permitidos(e: Estado): Evento[] {
  return Object.keys(TABLA[e]) as Evento[];
}

for (const e of ['apagada', 'calentando', 'lista', 'rota'] as const) {
  console.log(`${e}: ${permitidos(e).join(', ')}`);
}
```

#### Al superarla
En el tablero, solo se encienden los botones que sirven. La fogonera ya no tiene que adivinar.

#### Imagen
- El tablero de bronce con dos botones encendidos con luz ámbar y tres apagados.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) mira con la lupa.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) enchufa un cable; Gheco ilumina con una linterna.

## S03-N03 · La máquina genérica

```meta
tipo: tema
padre: S03-N02
precio: 10
criatura: troll
temas: diseno.maquina-estados, poo.genericos
usa: poo.clases, js.dom, js.eventos, js.almacenamiento, err.validacion
```

### Crónica

En la fundición no hay solo una caldera: está el **ascensor** que sube a la Cúpula, el **semáforo** de las vagonetas y la **compuerta** del agua. Cada uno tiene su tabla. Rigel se da cuenta de que todos funcionan igual: un estado, una tabla y botones.

—Una sola máquina para todas —dice Gheco—. Genérica: le pasás los estados y los eventos, y ella hace el resto.

### Objetivos

- Escribir una clase genérica `Maquina<E extends string, V extends string>`.
- Usarla para máquinas distintas sin escribir los tipos a mano (los infiere de la tabla).
- Avisar cuando se entra a un estado (funciones guardadas en un `Map`).
- Manejar el ascensor de la fundición desde una página.
- Guardar el estado en el almacenamiento y cargarlo con un guardia.

### Antes de empezar

- S03-N02.
- Clases (R02-N01) y genéricos con restricciones (R02-N06 y N07).

### Explicación

#### La máquina
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];
  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }
  get actual(): E { return this.estado; }
  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return false;
    this.estado = destino;
    this.historial.push(destino);
    return true;
  }
}
```

#### Los tipos salen solos
```typescript
type Luz = 'verde' | 'amarillo' | 'rojo';
const semaforo = new Maquina<Luz, 'pasar'>('verde', { verde: { pasar: 'amarillo' }, amarillo: { pasar: 'rojo' }, rojo: { pasar: 'verde' } });
semaforo.enviar('pasar');    // ✓
semaforo.enviar('saltar');   // ✗ no es un evento del semáforo
```

#### Cargar un estado guardado
Lo que viene del almacenamiento es un `string | null`. Antes de usarlo como estado, un guardia pregunta si es una de las filas de la tabla.

### Código de ejemplo

```typescript
class Interruptor<E extends string> {
  constructor(public estado: E, private readonly opuesto: Record<E, E>) {}
  tocar(): void { this.estado = this.opuesto[this.estado]; }
}
const luz = new Interruptor<'prendida' | 'apagada'>('apagada', { prendida: 'apagada', apagada: 'prendida' });
luz.tocar();
console.log(luz.estado);
```

### Salida esperada

```
prendida
```

### ¿Para qué sirve?

Escribir una vez y usar muchas: así se arman las bibliotecas que usa todo el mundo (en JavaScript hay bibliotecas enteras de máquinas de estados, como XState). Con genéricos, cada máquina conserva sus propios nombres y el compilador los cuida.

### Errores habituales

**Troll: devolver `true` aunque no pasó nada.** El que llama cree que la máquina cambió.

**Goblin: un evento de otra máquina.** `semaforo.enviar('arreglar')` no compila: los eventos son de cada máquina.

**Esqueleto: cargar un estado guardado sin revisar.** Si alguien escribió cualquier cosa en el almacenamiento, la máquina queda en un estado que no existe.

### Micro-misión S03-N03-P1 · Una máquina para todo

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, Don Péndulo
carta: Maquina<E, V> | estado y tabla privados · enviar(evento) busca el destino · si no hay, devuelve false y no cambia
recompensa: xp 10, oro 10
```

#### Escena
Rigel escribe la máquina genérica y la prueba con la caldera. Falta lo más importante de `enviar`: que no haga nada si el botón no sirve.

#### Gheco sugiere
Si el casillero está vacío (`destino === undefined`), se devuelve `false` y el estado no cambia.

#### Desafío
Completá la pregunta en `enviar`.

#### Pasos
1. Buscá el `___` en `enviar`.
2. Cambialo por `if (destino === undefined) return false;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];

  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }

  get actual(): E {
    return this.estado;
  }

  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    ___
    this.estado = destino;
    this.historial.push(destino);
    return true;
  }
}

type Estado = 'apagada' | 'calentando' | 'lista';
type Evento = 'encender' | 'calentar' | 'apagar';
const caldera = new Maquina<Estado, Evento>('apagada', {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', apagar: 'apagada' },
  lista: { apagar: 'apagada' },
});

for (const ev of ['calentar', 'encender', 'calentar', 'encender', 'apagar'] as const) {
  console.log(`${ev}: ${caldera.enviar(ev) ? 'sí' : 'no'} (${caldera.actual})`);
}
console.log(caldera.historial.join(' → '));
```

#### Salida esperada
```
calentar: no (apagada)
encender: sí (calentando)
calentar: sí (lista)
encender: no (lista)
apagar: sí (apagada)
apagada → calentando → lista → apagada
```

#### Solución
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];

  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }

  get actual(): E {
    return this.estado;
  }

  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return false;
    this.estado = destino;
    this.historial.push(destino);
    return true;
  }
}

type Estado = 'apagada' | 'calentando' | 'lista';
type Evento = 'encender' | 'calentar' | 'apagar';
const caldera = new Maquina<Estado, Evento>('apagada', {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', apagar: 'apagada' },
  lista: { apagar: 'apagada' },
});

for (const ev of ['calentar', 'encender', 'calentar', 'encender', 'apagar'] as const) {
  console.log(`${ev}: ${caldera.enviar(ev) ? 'sí' : 'no'} (${caldera.actual})`);
}
console.log(caldera.historial.join(' → '));
```

#### Al superarla
Don Péndulo mira la clase un rato largo. —Una sola pieza que sirve para todas las máquinas —murmura—. Como un buen engranaje.

#### Imagen
- Un engranaje maestro de bronce en el centro de la fundición, conectado a una caldera, un ascensor y un semáforo.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) lo examina con la lupa.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) aceita el engranaje; Gheco montado en un diente.

### Micro-misión S03-N03-P2 · El semáforo de las vagonetas

```meta
lugar: Las vías de la fundición
personajes: Rigel, Gheco
criatura: goblin
carta: La misma máquina, otra tabla | Maquina<Luz, 'pasar'> · cada máquina con sus eventos · uno de otra no compila
recompensa: xp 10, oro 10
```

#### Escena
Las vagonetas de carbón tienen un semáforo de tres luces. Rigel usa la misma máquina, con otra tabla. Un goblin dejó una línea que le manda **arreglar** al semáforo.

#### Gheco sugiere
El semáforo solo entiende `'pasar'`. Leé el error y borrá la línea que manda `'arreglar'`.

#### Desafío
Sacá el evento que no es del semáforo.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Borrá la línea `semaforo.enviar('arreglar');`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];
  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }
  get actual(): E {
    return this.estado;
  }
  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return false;
    this.estado = destino;
    this.historial.push(destino);
    return true;
  }
}

type Luz = 'verde' | 'amarillo' | 'rojo';
const semaforo = new Maquina<Luz, 'pasar'>('verde', {
  verde: { pasar: 'amarillo' },
  amarillo: { pasar: 'rojo' },
  rojo: { pasar: 'verde' },
});

semaforo.enviar('pasar');
semaforo.enviar('arreglar');
semaforo.enviar('pasar');
semaforo.enviar('pasar');
console.log(semaforo.historial.join(' → '));
```

#### Salida esperada
```
verde → amarillo → rojo → verde
```

#### Solución
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];
  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }
  get actual(): E {
    return this.estado;
  }
  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return false;
    this.estado = destino;
    this.historial.push(destino);
    return true;
  }
}

type Luz = 'verde' | 'amarillo' | 'rojo';
const semaforo = new Maquina<Luz, 'pasar'>('verde', {
  verde: { pasar: 'amarillo' },
  amarillo: { pasar: 'rojo' },
  rojo: { pasar: 'verde' },
});

semaforo.enviar('pasar');
semaforo.enviar('pasar');
semaforo.enviar('pasar');
console.log(semaforo.historial.join(' → '));
```

#### Al superarla
El semáforo de las vagonetas da la vuelta completa. Una vagoneta cargada de carbón pasa en verde.

#### Imagen
- Unas vías angostas con un semáforo de tres luces de vidrio y una vagoneta de carbón pasando.
- Un goblin chiquito con un engranaje en la espalda escondido detrás del semáforo con una llave inglesa.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) le saca la llave al goblin; Gheco viaja arriba de la vagoneta.

### Micro-misión S03-N03-P3 · Avisar al entrar

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco
carta: Avisos por estado | Map<E, Array<() => void>> · alEntrar(estado, fn) guarda · enviar llama a los de ese estado
recompensa: xp 10, oro 10
```

#### Escena
Cuando la caldera pasa a **lista**, tiene que sonar el silbato. Cuando pasa a **rota**, tiene que sonar la campana de alarma. Rigel le agrega a la máquina una forma de **avisar al entrar** a un estado.

#### Gheco sugiere
Se guardan funciones en un `Map`, por estado. `alEntrar` agrega una a la lista de ese estado (o arranca una lista nueva). `enviar` ya llama a las del destino.

#### Desafío
Completá `alEntrar`.

#### Pasos
1. Buscá el `___` en `alEntrar`.
2. Cambialo por `this.avisos.set(estado, [...(this.avisos.get(estado) ?? []), fn]);`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
class Maquina<E extends string, V extends string> {
  private readonly avisos = new Map<E, Array<() => void>>();

  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {}

  alEntrar(estado: E, fn: () => void): void {
    ___
  }

  enviar(evento: V): void {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return;
    this.estado = destino;
    for (const aviso of this.avisos.get(destino) ?? []) aviso();
  }
}

type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar';
const caldera = new Maquina<Estado, Evento>('apagada', {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota' },
  lista: { romper: 'rota' },
  rota: { arreglar: 'apagada' },
});

caldera.alEntrar('lista', () => console.log('🔔 ¡Fiuuu! Silbato: caldera lista'));
caldera.alEntrar('rota', () => console.log('🚨 Campana de alarma'));
caldera.alEntrar('rota', () => console.log('📋 Aviso a Don Péndulo'));

for (const ev of ['encender', 'calentar', 'romper', 'arreglar'] as const) {
  console.log(`> ${ev}`);
  caldera.enviar(ev);
}
```

#### Salida esperada
```
> encender
> calentar
🔔 ¡Fiuuu! Silbato: caldera lista
> romper
🚨 Campana de alarma
📋 Aviso a Don Péndulo
> arreglar
```

#### Solución
```typescript
class Maquina<E extends string, V extends string> {
  private readonly avisos = new Map<E, Array<() => void>>();

  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {}

  alEntrar(estado: E, fn: () => void): void {
    this.avisos.set(estado, [...(this.avisos.get(estado) ?? []), fn]);
  }

  enviar(evento: V): void {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return;
    this.estado = destino;
    for (const aviso of this.avisos.get(destino) ?? []) aviso();
  }
}

type Estado = 'apagada' | 'calentando' | 'lista' | 'rota';
type Evento = 'encender' | 'calentar' | 'romper' | 'arreglar';
const caldera = new Maquina<Estado, Evento>('apagada', {
  apagada: { encender: 'calentando' },
  calentando: { calentar: 'lista', romper: 'rota' },
  lista: { romper: 'rota' },
  rota: { arreglar: 'apagada' },
});

caldera.alEntrar('lista', () => console.log('🔔 ¡Fiuuu! Silbato: caldera lista'));
caldera.alEntrar('rota', () => console.log('🚨 Campana de alarma'));
caldera.alEntrar('rota', () => console.log('📋 Aviso a Don Péndulo'));

for (const ev of ['encender', 'calentar', 'romper', 'arreglar'] as const) {
  console.log(`> ${ev}`);
  caldera.enviar(ev);
}
```

#### Al superarla
El silbato suena justo cuando tiene que sonar, y la campana también. Gheco se tapa los oídos con la cola.

#### Imagen
- Un silbato de bronce soltando vapor y una campana de alarma colgada de una viga, sonando.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) conecta un cable de la caldera a la campana.
- Gheco se tapa los oídos con la cola.

### Micro-misión S03-N03-P4 · El ascensor de la Cúpula

```meta
lugar: El ascensor de la fundición
personajes: Rigel, Gheco, Don Péndulo
carta: La máquina en la página | botones con click · enviar el evento · pintar el piso y el historial
recompensa: xp 15, monedas 5
```

#### Escena
El ascensor de jaula sube de la fundición al taller y del taller a la Cúpula. Tiene dos botones de bronce: **subir** y **bajar**. Rigel conecta la máquina a la página: el cartel muestra el piso, y abajo, el recorrido.

#### Gheco sugiere
Cada botón llama a `enviar` con su evento y después a `pintar`. Falta conectar el botón de subir.

#### Desafío
Conectá el botón de subir.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `subir.addEventListener('click', () => { ascensor.enviar('subir'); pintar(); });`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #1a1206; color: #e8d9b0; padding: 20px; }
  #piso { font-size: 22px; color: #f2c14e; }
  button { font-size: 16px; padding: 6px 14px; background: #8d6e3f; color: #fff7e0; border: 0; border-radius: 6px; }
</style>
<p id="piso"></p>
<button id="subir">▲ Subir</button>
<button id="bajar">▼ Bajar</button>
<p id="recorrido"></p>
```

#### Eventos
```
click #subir
click #subir
click #subir
click #bajar
```

#### Estado
```
#piso
#recorrido
```

#### Código inicial
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];
  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }
  get actual(): E {
    return this.estado;
  }
  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return false;
    this.estado = destino;
    this.historial.push(destino);
    return true;
  }
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

type Piso = 'fundición' | 'taller' | 'cúpula';
const ascensor = new Maquina<Piso, 'subir' | 'bajar'>('fundición', {
  fundición: { subir: 'taller' },
  taller: { subir: 'cúpula', bajar: 'fundición' },
  cúpula: { bajar: 'taller' },
});

const piso = obtenerElemento<HTMLParagraphElement>('#piso');
const recorrido = obtenerElemento<HTMLParagraphElement>('#recorrido');
const subir = obtenerElemento<HTMLButtonElement>('#subir');
const bajar = obtenerElemento<HTMLButtonElement>('#bajar');

function pintar(): void {
  piso.textContent = `Piso: ${ascensor.actual}`;
  recorrido.textContent = ascensor.historial.join(' → ');
}

___
bajar.addEventListener('click', () => { ascensor.enviar('bajar'); pintar(); });
pintar();
```

#### Salida esperada
```
── Estado ──
#piso: Piso: taller
#recorrido: fundición → taller → cúpula → taller
```

#### Solución
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];
  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }
  get actual(): E {
    return this.estado;
  }
  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return false;
    this.estado = destino;
    this.historial.push(destino);
    return true;
  }
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

type Piso = 'fundición' | 'taller' | 'cúpula';
const ascensor = new Maquina<Piso, 'subir' | 'bajar'>('fundición', {
  fundición: { subir: 'taller' },
  taller: { subir: 'cúpula', bajar: 'fundición' },
  cúpula: { bajar: 'taller' },
});

const piso = obtenerElemento<HTMLParagraphElement>('#piso');
const recorrido = obtenerElemento<HTMLParagraphElement>('#recorrido');
const subir = obtenerElemento<HTMLButtonElement>('#subir');
const bajar = obtenerElemento<HTMLButtonElement>('#bajar');

function pintar(): void {
  piso.textContent = `Piso: ${ascensor.actual}`;
  recorrido.textContent = ascensor.historial.join(' → ');
}

subir.addEventListener('click', () => { ascensor.enviar('subir'); pintar(); });
bajar.addEventListener('click', () => { ascensor.enviar('bajar'); pintar(); });
pintar();
```

#### Al superarla
El tercer **subir** no hace nada: ya está en la Cúpula. El ascensor no atraviesa el techo, como le pasaba al del Vidriero una vez.

#### Imagen
- Un ascensor de jaula de bronce subiendo por un pozo de piedra, con una aguja de pisos arriba.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) adentro de la jaula, agarrado de la baranda.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) aprieta el botón de subir; Gheco mira para abajo, mareado.

### Micro-misión S03-N03-P5 · Donde lo dejaste

```meta
lugar: El ascensor de la fundición
personajes: Rigel, Gheco
criatura: skeleton
carta: Cargar con un guardia | localStorage da string | null · esPiso(x): x is Piso con in · si no sirve, el piso de arranque
recompensa: xp 15, monedas 5
```

#### Escena
Cuando la fundición se apaga de noche, el ascensor se queda donde estaba. A la mañana, tiene que arrancar en ese piso. Pero un esqueleto de alambre escribió en la memoria **sótano**, que no existe.

#### Gheco sugiere
Lo que viene del almacenamiento es `string | null`. El guardia `esPiso` pregunta si es una fila de la tabla (`x in TABLA`). Si no sirve, se arranca en la fundición.

#### Desafío
Completá el guardia.

#### Pasos
1. Buscá el `___` en `esPiso`.
2. Cambialo por `return x !== null && x in TABLA;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Almacenamiento
```
local ascensor = sótano
```

#### Estado
```
local ascensor
```

#### Código inicial
```typescript
type Piso = 'fundición' | 'taller' | 'cúpula';
const TABLA: Record<Piso, Partial<Record<'subir' | 'bajar', Piso>>> = {
  fundición: { subir: 'taller' },
  taller: { subir: 'cúpula', bajar: 'fundición' },
  cúpula: { bajar: 'taller' },
};

function esPiso(x: string | null): x is Piso {
  ___
}

function cargar(): Piso {
  const guardado = localStorage.getItem('ascensor');
  return esPiso(guardado) ? guardado : 'fundición';
}

console.log(`Arranca en: ${cargar()}`);
localStorage.setItem('ascensor', 'cúpula');
console.log(`Arranca en: ${cargar()}`);
```

#### Salida esperada
```
Arranca en: fundición
Arranca en: cúpula
── Estado ──
local ascensor: cúpula
```

#### Solución
```typescript
type Piso = 'fundición' | 'taller' | 'cúpula';
const TABLA: Record<Piso, Partial<Record<'subir' | 'bajar', Piso>>> = {
  fundición: { subir: 'taller' },
  taller: { subir: 'cúpula', bajar: 'fundición' },
  cúpula: { bajar: 'taller' },
};

function esPiso(x: string | null): x is Piso {
  return x !== null && x in TABLA;
}

function cargar(): Piso {
  const guardado = localStorage.getItem('ascensor');
  return esPiso(guardado) ? guardado : 'fundición';
}

console.log(`Arranca en: ${cargar()}`);
localStorage.setItem('ascensor', 'cúpula');
console.log(`Arranca en: ${cargar()}`);
```

#### Al superarla
El ascensor no baja a ningún sótano imaginario. El esqueleto de alambre se queda esperando en el pozo, aburrido.

#### Imagen
- El pozo del ascensor visto desde arriba, con un esqueleto de alambre chiquito sentado en el fondo, aburrido.
- La aguja de pisos marcando la cúpula.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) mira para abajo por la reja; Gheco le saca la lengua al esqueleto.

## S03-N04 · Jefe: el Gólem de Vapor Desbocado

```meta
tipo: jefe
padre: S03-N03
precio: 10
criatura: dragon
insignia: Llave de la Fundición
insignia_descripcion: Calmaste al Gólem de Vapor Desbocado: máquinas de estados tipadas, con su tabla, sus avisos y su memoria.
usa: diseno.maquina-estados, poo.genericos, poo.clases, cal.tipos, js.dom, js.eventos
```

### Crónica

Una mañana, la fundición tiembla. Del fondo, detrás de la caldera, sale un **gólem de vapor**: una mole de hierro y cobre, con una caldera en el pecho y los ojos de vidrio rojo. Es el gólem de carga que construyeron el Vidriero y **Tesla** hace años, cuando el Mirador se estaba levantando. Lleva años quieto, y esta mañana se despertó solo… y desbocado: camina, frena, se calienta y descarga vapor sin ningún orden.

Por el tubo neumático llega una cápsula de la Ciudadela de los Artífices, con la letra apurada de Tesla: *«Rigel: el gólem tiene una máquina de estados adentro, pero su tabla se rompió con los años. Arreglale la tabla y se calma. No lo apagues a golpes: es un amigo viejo.»*

### Objetivos

- Integrar toda la Senda: estados con datos, tabla de transiciones, la máquina genérica, avisos y la página.
- Encontrar con el compilador lo que está roto en la tabla del gólem.
- Agregar una regla con condición: si se calienta de más, se descarga solo.

### Antes de empezar

- Toda la Senda de la Fundición (S03-N01 a N03).

### Explicación

#### Las trampas del gólem (y la verdad)
| El gólem hace… | La verdad |
|---|---|
| un estado que no está en la tabla | `Record` exige todas las filas |
| un botón que lleva a un estado que no existe | el destino tiene que ser un `Estado` |
| se calienta sin parar | una regla con condición lo frena |
| un evento nuevo sin atender | el `never` del `switch` lo encuentra |

### Micro-misión S03-N04-P1 · La tabla rota del gólem

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, Don Péndulo, el Gólem de Vapor
criatura: goblin
carta: Trampa 1 | leer los errores de la tabla · el compilador muestra primero el destino que no existe (TS2322) · la fila que falta aparece después
recompensa: xp 15, monedas 3
```

#### Escena
Rigel copia la tabla del gólem, tal como está grabada en su espalda. Antes de arreglarla, quiere saber **cuántas** cosas están rotas.

#### Gheco sugiere
Esta misión no se ejecuta: el compilador revisa la tabla. Hay dos roturas:
- un botón lleva a un estado que no existe;
- falta la fila de un estado.

Pero el compilador, cuando un objeto tiene un error **adentro**, avisa ese primero y recién después mira si le falta algo. Por eso ahora vas a ver uno solo. Es normal: se arregla uno y aparece el siguiente.

#### Desafío
Tocá **Ejecutar** y leé qué está roto.

#### Pasos
1. Leé la tabla buscando las dos roturas.
2. Tocá **Ejecutar**: sale un solo error, `TS2322` en la línea 6 (`'volando'` no es un `Estado`).
3. Si querés, cambiá `'volando'` por `'quieto'` y volvé a ejecutar: aparece el otro (`TS2741`, la fila que falta). Después dejalo como estaba para comparar.

#### Compilador
sí

#### Código inicial
```typescript
type Estado = 'quieto' | 'caminando' | 'cargando' | 'descargando';
type Evento = 'andar' | 'frenar' | 'cargar' | 'soltar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  quieto: { andar: 'caminando', cargar: 'cargando' },
  caminando: { frenar: 'quieto', soltar: 'volando' },
  cargando: { soltar: 'descargando' },
};
```

#### Salida esperada
```
TS2322 en la línea 6
```

#### Solución
```typescript
type Estado = 'quieto' | 'caminando' | 'cargando' | 'descargando';
type Evento = 'andar' | 'frenar' | 'cargar' | 'soltar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  quieto: { andar: 'caminando', cargar: 'cargando' },
  caminando: { frenar: 'quieto', soltar: 'volando' },
  cargando: { soltar: 'descargando' },
};
```

#### Al superarla
Don Péndulo marca con tiza las dos roturas en la espalda del gólem. El gólem gruñe, pero se deja.

#### Imagen
- Un gólem de vapor enorme de hierro y cobre, con una caldera en el pecho y ojos de vidrio rojo, de espaldas, con una tabla grabada.
- Un goblin chiquito con un engranaje en la espalda colgado de la tabla, rascando una letra.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) marca con tiza subido a una escalera; Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) sostiene la escalera; Gheco espanta al goblin.

### Micro-misión S03-N04-P2 · La tabla arreglada

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, el Gólem de Vapor
criatura: ogre
carta: Trampa 2 | la fila descargando: soltar lleva a quieto · el destino 'volando' no existe: soltar lleva a quieto · el gólem obedece
recompensa: xp 15, monedas 3
```

#### Escena
Ahora sí, Rigel arregla la tabla del gólem: un gólem caminando que suelta la carga no sale **volando**, se queda **quieto**. Y el gólem que descarga, al terminar, también queda quieto.

#### Gheco sugiere
Dos cambios:
- `soltar: 'volando'` pasa a `soltar: 'quieto'`;
- falta la fila: `descargando: { frenar: 'quieto' },`.

#### Desafío
Arreglá la tabla.

#### Pasos
1. Cambiá `soltar: 'volando'` por `soltar: 'quieto'`.
2. En el `___`, escribí `descargando: { frenar: 'quieto' },`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Estado = 'quieto' | 'caminando' | 'cargando' | 'descargando';
type Evento = 'andar' | 'frenar' | 'cargar' | 'soltar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  quieto: { andar: 'caminando', cargar: 'cargando' },
  caminando: { frenar: 'quieto', soltar: 'volando' },
  cargando: { soltar: 'descargando' },
  ___
};

let golem: Estado = 'quieto';
const recorrido: Estado[] = [golem];
for (const ev of ['cargar', 'soltar', 'frenar', 'andar', 'soltar'] as const) {
  golem = TABLA[golem][ev] ?? golem;
  recorrido.push(golem);
}
console.log(recorrido.join(' → '));
```

#### Salida esperada
```
quieto → cargando → descargando → quieto → caminando → quieto
```

#### Solución
```typescript
type Estado = 'quieto' | 'caminando' | 'cargando' | 'descargando';
type Evento = 'andar' | 'frenar' | 'cargar' | 'soltar';

const TABLA: Record<Estado, Partial<Record<Evento, Estado>>> = {
  quieto: { andar: 'caminando', cargar: 'cargando' },
  caminando: { frenar: 'quieto', soltar: 'quieto' },
  cargando: { soltar: 'descargando' },
  descargando: { frenar: 'quieto' },
};

let golem: Estado = 'quieto';
const recorrido: Estado[] = [golem];
for (const ev of ['cargar', 'soltar', 'frenar', 'andar', 'soltar'] as const) {
  golem = TABLA[golem][ev] ?? golem;
  recorrido.push(golem);
}
console.log(recorrido.join(' → '));
```

#### Al superarla
El gólem da unos pasos, levanta una caja, la suelta y se queda quieto. Ya no hace cosas al azar.

#### Imagen
- El gólem de vapor de hierro y cobre bajando una caja con cuidado, con los ojos de vidrio rojo más tranquilos.
- Un ogro de cuerda chiquito, decepcionado, con una llave rota en la mano.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) dirige al gólem con un cuaderno; Gheco sentado en la caja.

### Micro-misión S03-N04-P3 · Que no se recaliente

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, Don Péndulo, el Gólem de Vapor
criatura: troll
carta: Trampa 3 | una regla con condición · si la presión pasa de 10, descarga vapor solo · el estado con sus datos
recompensa: xp 15, monedas 3
```

#### Escena
La caldera del pecho del gólem sube de presión con cada paso. Si pasa de 10, explota en una nube de vapor. Don Péndulo pide una regla: **si pasa de 10, descarga vapor sola** y vuelve a 0.

#### Gheco sugiere
En el caso `'andar'`, después de sumar presión, se pregunta: si pasó de 10, el gólem pasa a `'descargando'`; si no, sigue caminando con la presión nueva.

#### Desafío
Completá la regla.

#### Pasos
1. Buscá el `___` en `aplicar`.
2. Cambialo por `return presion > 10 ? { estado: 'descargando' } : { estado: 'caminando', presion };`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Golem = { estado: 'quieto' } | { estado: 'caminando'; presion: number } | { estado: 'descargando' };
type Accion = { tipo: 'andar'; pasos: number } | { tipo: 'frenar' };

function aplicar(g: Golem, a: Accion): Golem {
  switch (a.tipo) {
    case 'andar': {
      if (g.estado === 'descargando') return g;
      const presion = (g.estado === 'caminando' ? g.presion : 0) + a.pasos * 2;
      ___
    }
    case 'frenar':
      return { estado: 'quieto' };
  }
}

let golem: Golem = { estado: 'quieto' };
for (const a of [{ tipo: 'andar', pasos: 2 }, { tipo: 'andar', pasos: 3 }, { tipo: 'andar', pasos: 1 }, { tipo: 'frenar' }] as Accion[]) {
  golem = aplicar(golem, a);
  console.log(JSON.stringify(golem));
}
```

#### Salida esperada
```
{"estado":"caminando","presion":4}
{"estado":"caminando","presion":10}
{"estado":"descargando"}
{"estado":"quieto"}
```

#### Solución
```typescript
type Golem = { estado: 'quieto' } | { estado: 'caminando'; presion: number } | { estado: 'descargando' };
type Accion = { tipo: 'andar'; pasos: number } | { tipo: 'frenar' };

function aplicar(g: Golem, a: Accion): Golem {
  switch (a.tipo) {
    case 'andar': {
      if (g.estado === 'descargando') return g;
      const presion = (g.estado === 'caminando' ? g.presion : 0) + a.pasos * 2;
      return presion > 10 ? { estado: 'descargando' } : { estado: 'caminando', presion };
    }
    case 'frenar':
      return { estado: 'quieto' };
  }
}

let golem: Golem = { estado: 'quieto' };
for (const a of [{ tipo: 'andar', pasos: 2 }, { tipo: 'andar', pasos: 3 }, { tipo: 'andar', pasos: 1 }, { tipo: 'frenar' }] as Accion[]) {
  golem = aplicar(golem, a);
  console.log(JSON.stringify(golem));
}
```

#### Al superarla
Al tercer paso, el gólem suelta una nube de vapor por las orejas, despacito, y se calma. Don Péndulo aplaude con los guantes de cuero.

#### Imagen
- El gólem de vapor soltando vapor por las orejas, con un manómetro en el pecho bajando.
- Un troll de cuerda chiquito empapado de vapor.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo) aplaude; Rigel (chico flaco con pecas, antiparras de latón) anota la presión; Gheco se seca con un trapo.

### Micro-misión S03-N04-P4 · El panel del gólem

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, el Gólem de Vapor
carta: Trampa 4 | el estado como clase CSS · los botones envían eventos · el panel siempre muestra la verdad
recompensa: xp 15, monedas 3
```

#### Escena
Para manejar al gólem sin subirse, Rigel arma un **panel** en la pared: un botón por evento, el estado escrito y una lámpara que cambia de color según el estado.

#### Gheco sugiere
La lámpara toma el color de una clase CSS con el nombre del estado: `lampara.className = maquina.actual`. Falta esa línea en `pintar`.

#### Desafío
Completá la línea de la lámpara.

#### Pasos
1. Buscá el `___` en `pintar`.
2. Cambialo por `lampara.className = golem.actual;`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #1a1206; color: #e8d9b0; padding: 20px; }
  #lampara { width: 40px; height: 40px; border-radius: 50%; background: #555; }
  #lampara.quieto { background: #4caf50; }
  #lampara.caminando { background: #f2c14e; }
  #lampara.cargando { background: #4fc3f7; }
  #lampara.descargando { background: #e57373; }
  button { margin: 2px; padding: 6px 10px; background: #8d6e3f; color: #fff7e0; border: 0; border-radius: 6px; }
</style>
<div id="lampara"></div>
<p id="estado"></p>
<button data-evento="andar">Andar</button>
<button data-evento="frenar">Frenar</button>
<button data-evento="cargar">Cargar</button>
<button data-evento="soltar">Soltar</button>
```

#### Eventos
```
click [data-evento=cargar]
click [data-evento=soltar]
```

#### Estado
```
#estado
#lampara @class
```

#### Código inicial
```typescript
class Maquina<E extends string, V extends string> {
  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {}
  get actual(): E {
    return this.estado;
  }
  enviar(evento: V): void {
    this.estado = this.tabla[this.estado][evento] ?? this.estado;
  }
}

type Estado = 'quieto' | 'caminando' | 'cargando' | 'descargando';
type Evento = 'andar' | 'frenar' | 'cargar' | 'soltar';
const EVENTOS: readonly Evento[] = ['andar', 'frenar', 'cargar', 'soltar'];
const esEvento = (x: string | undefined): x is Evento => EVENTOS.some((e) => e === x);

const golem = new Maquina<Estado, Evento>('quieto', {
  quieto: { andar: 'caminando', cargar: 'cargando' },
  caminando: { frenar: 'quieto', soltar: 'quieto' },
  cargando: { soltar: 'descargando' },
  descargando: { frenar: 'quieto' },
});

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const lampara = obtenerElemento<HTMLDivElement>('#lampara');
const cartel = obtenerElemento<HTMLParagraphElement>('#estado');

function pintar(): void {
  cartel.textContent = `El gólem está ${golem.actual}`;
  ___
}

for (const boton of document.querySelectorAll<HTMLButtonElement>('button')) {
  boton.addEventListener('click', () => {
    const ev = boton.dataset.evento;
    if (esEvento(ev)) golem.enviar(ev);
    pintar();
  });
}
pintar();
```

#### Salida esperada
```
── Estado ──
#estado: El gólem está descargando
#lampara @class: descargando
```

#### Solución
```typescript
class Maquina<E extends string, V extends string> {
  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {}
  get actual(): E {
    return this.estado;
  }
  enviar(evento: V): void {
    this.estado = this.tabla[this.estado][evento] ?? this.estado;
  }
}

type Estado = 'quieto' | 'caminando' | 'cargando' | 'descargando';
type Evento = 'andar' | 'frenar' | 'cargar' | 'soltar';
const EVENTOS: readonly Evento[] = ['andar', 'frenar', 'cargar', 'soltar'];
const esEvento = (x: string | undefined): x is Evento => EVENTOS.some((e) => e === x);

const golem = new Maquina<Estado, Evento>('quieto', {
  quieto: { andar: 'caminando', cargar: 'cargando' },
  caminando: { frenar: 'quieto', soltar: 'quieto' },
  cargando: { soltar: 'descargando' },
  descargando: { frenar: 'quieto' },
});

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const lampara = obtenerElemento<HTMLDivElement>('#lampara');
const cartel = obtenerElemento<HTMLParagraphElement>('#estado');

function pintar(): void {
  cartel.textContent = `El gólem está ${golem.actual}`;
  lampara.className = golem.actual;
}

for (const boton of document.querySelectorAll<HTMLButtonElement>('button')) {
  boton.addEventListener('click', () => {
    const ev = boton.dataset.evento;
    if (esEvento(ev)) golem.enviar(ev);
    pintar();
  });
}
pintar();
```

#### Al superarla
La lámpara del panel se pone roja: el gólem descarga. Rigel aprieta **frenar** y vuelve el verde. El gólem, del otro lado de la fundición, mira el panel con curiosidad.

#### Imagen
- Un panel de bronce en la pared con una lámpara roja encendida y cuatro botones grandes.
- El gólem de vapor de hierro y cobre a lo lejos, inclinando la cabeza con curiosidad hacia el panel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) con la mano sobre el botón de frenar; Gheco imita a la lámpara poniéndose rojo.

### Micro-misión S03-N04-P5 · Jefe: el gólem se calma

```meta
lugar: La fundición del Mirador
personajes: Rigel, Gheco, Don Péndulo, el Gólem de Vapor, Tesla
carta: La máquina completa | Maquina<E, V> con historial y avisos · la tabla entera · se guarda dónde quedó · nada imposible compila
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
Rigel junta todas las piezas: la máquina genérica con su historial, la tabla arreglada del gólem, los avisos y la memoria de dónde quedó. Para que el gólem se calme del todo, tiene que hacer un día de trabajo completo sin un solo paso imposible.

#### Gheco sugiere
Junta toda la Senda. Al final del día, la máquina guarda su estado en la memoria para la mañana siguiente. Falta esa línea: se guarda en el aviso de `'quieto'`, así queda guardado cada vez que el gólem se detiene.

#### Desafío
Completá el aviso que guarda el estado.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `golem.alEntrar('quieto', () => localStorage.setItem('golem', golem.actual));`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Estado
```
local golem
```

#### Código inicial
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];
  private readonly avisos = new Map<E, Array<() => void>>();

  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }

  get actual(): E {
    return this.estado;
  }

  alEntrar(estado: E, fn: () => void): void {
    this.avisos.set(estado, [...(this.avisos.get(estado) ?? []), fn]);
  }

  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return false;
    this.estado = destino;
    this.historial.push(destino);
    for (const aviso of this.avisos.get(destino) ?? []) aviso();
    return true;
  }
}

type Estado = 'quieto' | 'caminando' | 'cargando' | 'descargando';
type Evento = 'andar' | 'frenar' | 'cargar' | 'soltar';

const golem = new Maquina<Estado, Evento>('quieto', {
  quieto: { andar: 'caminando', cargar: 'cargando' },
  caminando: { frenar: 'quieto', soltar: 'quieto' },
  cargando: { soltar: 'descargando' },
  descargando: { frenar: 'quieto' },
});

golem.alEntrar('descargando', () => console.log('  (vapor por las orejas)'));
___

const dia: Evento[] = ['cargar', 'andar', 'soltar', 'frenar', 'andar', 'frenar', 'cargar'];
let imposibles = 0;
for (const ev of dia) {
  if (!golem.enviar(ev)) imposibles++;
}
console.log(golem.historial.join(' → '));
console.log(`Pasos imposibles que no hizo: ${imposibles}`);
console.log(`Quedó en: ${golem.actual} · guardado: ${localStorage.getItem('golem')}`);
```

#### Salida esperada
```
  (vapor por las orejas)
quieto → cargando → descargando → quieto → caminando → quieto → cargando
Pasos imposibles que no hizo: 1
Quedó en: cargando · guardado: quieto
── Estado ──
local golem: quieto
```

#### Solución
```typescript
class Maquina<E extends string, V extends string> {
  readonly historial: E[];
  private readonly avisos = new Map<E, Array<() => void>>();

  constructor(private estado: E, private readonly tabla: Record<E, Partial<Record<V, E>>>) {
    this.historial = [estado];
  }

  get actual(): E {
    return this.estado;
  }

  alEntrar(estado: E, fn: () => void): void {
    this.avisos.set(estado, [...(this.avisos.get(estado) ?? []), fn]);
  }

  enviar(evento: V): boolean {
    const destino = this.tabla[this.estado][evento];
    if (destino === undefined) return false;
    this.estado = destino;
    this.historial.push(destino);
    for (const aviso of this.avisos.get(destino) ?? []) aviso();
    return true;
  }
}

type Estado = 'quieto' | 'caminando' | 'cargando' | 'descargando';
type Evento = 'andar' | 'frenar' | 'cargar' | 'soltar';

const golem = new Maquina<Estado, Evento>('quieto', {
  quieto: { andar: 'caminando', cargar: 'cargando' },
  caminando: { frenar: 'quieto', soltar: 'quieto' },
  cargando: { soltar: 'descargando' },
  descargando: { frenar: 'quieto' },
});

golem.alEntrar('descargando', () => console.log('  (vapor por las orejas)'));
golem.alEntrar('quieto', () => localStorage.setItem('golem', golem.actual));

const dia: Evento[] = ['cargar', 'andar', 'soltar', 'frenar', 'andar', 'frenar', 'cargar'];
let imposibles = 0;
for (const ev of dia) {
  if (!golem.enviar(ev)) imposibles++;
}
console.log(golem.historial.join(' → '));
console.log(`Pasos imposibles que no hizo: ${imposibles}`);
console.log(`Quedó en: ${golem.actual} · guardado: ${localStorage.getItem('golem')}`);
```

#### Al superarla
El gólem termina su día de trabajo sin un paso fuera de lugar. Los ojos de vidrio pasan del rojo a un ámbar tranquilo. Se sienta junto a la caldera, como un perro viejo, y suelta un suspiro de vapor.

Por el tubo llega otra cápsula de **Tesla**, con un dibujo del gólem cuando era nuevo, al lado del Vidriero y de un Tesla mucho más chico: *«Sabía que ibas a poder. Cuidámelo.»* Don Péndulo le cuelga a Rigel del cinturón **la Llave de la Fundición**, la que abre todas las máquinas de abajo de la montaña.

#### Imagen
- La fundición en calma: el gólem de vapor de hierro y cobre sentado junto a la caldera, con los ojos de vidrio color ámbar.
- Un dibujo viejo en papel, dentro de una cápsula abierta, con tres figuras al lado del gólem (sin caras detalladas).
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) recibe una llave grande de bronce de Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa en un ojo); la fogonera (mujer fuerte con delantal de cuero, pañuelo en la cabeza y una pala) saluda desde lejos; Gheco acurrucado contra el gólem.
