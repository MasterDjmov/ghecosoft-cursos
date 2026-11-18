# RAMA S04 · Senda de las Herramientas del Calibre: una biblioteca de tipos propia

```meta
tipo: senda
posicion: 9
```

## S04-N01 · Result de verdad

```meta
tipo: tema
padre: R04-N08
precio: 3
moneda: comodin
criatura: skeleton
temas: err.opcionales
usa: poo.genericos, func.orden-superior, cal.tipos
```

### Crónica

Rigel nunca se separa de su **calibre de latón**, el que le regaló Tesla: mide todo, desde un tornillo hasta una estrella. Una noche, Astrea lo mira trabajar y le hace notar algo: —Cada programa del Mirador vuelve a escribir lo mismo: el `Result`, el guardia, la validación. ¿Por qué no armás una **caja de herramientas**, como tu calibre, que sirva para todos?

Nima se entusiasma: —En la Feria, Sila tenía una caja así para el Archivo. La llamaba «las herramientas». Todo el mundo la usaba.

Así nace `calibre.ts`: la biblioteca de herramientas del Mirador.

### Objetivos

- Fabricar resultados con dos funciones: `ok(valor)` y `error(mensaje)`.
- Transformar el valor de un `Result` sin abrirlo (`mapear`).
- Encadenar pasos que pueden fallar (`luego`).
- Sacar el valor con uno de repuesto (`valorO`).
- Juntar una lista de resultados en uno solo (`todos`).

### Antes de empezar

- `Result<T>` y los errores tipados (R04-N01).
- Genéricos (R02-N06) y funciones que reciben funciones (R01-N04).

### Explicación

#### Fabricar resultados
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function ok<T>(valor: T): Result<T> { return { ok: true, valor }; }
function error(mensaje: string): Result<never> { return { ok: false, error: mensaje }; }
```
`error` devuelve `Result<never>`: no tiene valor, así que sirve donde se espere cualquier `Result<T>`.

#### Trabajar sin abrir
```typescript
mapear(ok(4), (x) => x * 2);          // ok(8)
mapear(error('no'), (x) => x * 2);    // error('no'): la función ni se llama
```

#### Encadenar pasos que fallan
`luego` es como `mapear`, pero la función también devuelve un `Result`: si el primer paso falla, el segundo no se hace.

### Código de ejemplo

```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });

function dividir(a: number, b: number): Result<number> {
  return b === 0 ? { ok: false, error: 'división por cero' } : ok(a / b);
}
console.log(dividir(10, 4), dividir(1, 0));
```

### Salida esperada

```
{ ok: true, valor: 2.5 } { ok: false, error: 'división por cero' }
```

### ¿Para qué sirve?

Muchas bibliotecas (y lenguajes como Rust) trabajan así: el error no se lanza, se devuelve, y unas pocas funciones permiten combinarlos. El código queda como una receta: «leé, convertí, validá», y si algo falla en el medio, el error llega hasta el final sin romper nada.

### Errores habituales

**Esqueleto: usar `r.valor` sin preguntar `r.ok`.** No compila: puede ser un error.

**Troll: lanzar en vez de devolver.** Si un paso lanza, el que llama tiene que acordarse del `try`. Si devuelve un `Result`, el compilador se lo recuerda.

**Ogro: tragarse el error.** `valorO` está bien cuando hay un valor de repuesto razonable; si no, mejor mostrar el error.

### Micro-misión S04-N01-P1 · Las dos primeras herramientas

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Astrea
criatura: skeleton
carta: ok y error | ok<T>(valor) devuelve { ok: true, valor } · error(mensaje) es Result<never> · sirve para cualquier T
recompensa: xp 10, oro 10
```

#### Escena
Rigel abre un cajón vacío en su mesa de trabajo y lo rotula **calibre.ts**. Las primeras dos herramientas son las más simples: una que fabrica un resultado bueno y otra que fabrica uno malo.

#### Gheco sugiere
`ok` arma el objeto con `ok: true` y el valor. Como el nombre del campo y de la variable es el mismo, alcanza con escribir `valor`.

#### Desafío
Completá el `return` de `ok`.

#### Pasos
1. Buscá el `___` en `ok`.
2. Cambialo por `{ ok: true, valor }`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function ok<T>(valor: T): Result<T> {
  return ___;
}

function error(mensaje: string): Result<never> {
  return { ok: false, error: mensaje };
}

function raiz(x: number): Result<number> {
  return x < 0 ? error('no hay raíz de un negativo') : ok(Math.sqrt(x));
}

for (const x of [49, -4]) {
  const r = raiz(x);
  console.log(r.ok ? `raíz de ${x}: ${r.valor}` : `✗ ${r.error}`);
}
```

#### Salida esperada
```
raíz de 49: 7
✗ no hay raíz de un negativo
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };

function ok<T>(valor: T): Result<T> {
  return { ok: true, valor };
}

function error(mensaje: string): Result<never> {
  return { ok: false, error: mensaje };
}

function raiz(x: number): Result<number> {
  return x < 0 ? error('no hay raíz de un negativo') : ok(Math.sqrt(x));
}

for (const x of [49, -4]) {
  const r = raiz(x);
  console.log(r.ok ? `raíz de ${x}: ${r.valor}` : `✗ ${r.error}`);
}
```

#### Al superarla
Dos herramientas brillan en el cajón: una con un tilde y otra con una cruz.

#### Imagen
- Una mesa de trabajo steampunk con un cajón abierto rotulado con una placa de latón, y dos herramientas adentro (una con un tilde grabado, otra con una cruz).
- Astrea (lechuza con anteojos de latón y chaleco azul) mira el cajón.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) sostiene un calibre de latón; Gheco adentro del cajón.

### Micro-misión S04-N01-P2 · Trabajar sin abrir

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Nima
carta: mapear<T, U> | si r.ok, aplica f y devuelve ok(f(valor)) · si no, devuelve el error tal cual · la f ni se llama
recompensa: xp 10, oro 10
```

#### Escena
Nima mide la distancia de una flecha en pasos y la quiere en metros. Pero la medición puede haber fallado. Rigel arma una herramienta que convierte el valor **solo si hay valor**.

#### Gheco sugiere
Si `r.ok`, se aplica la función y se envuelve en `ok`. Si no, se devuelve `r` como está: TypeScript sabe que es un error, y un error sirve como `Result<U>`.

#### Desafío
Completá el `return` de `mapear`.

#### Pasos
1. Buscá el `___` en `mapear`.
2. Cambialo por `r.ok ? ok(f(r.valor)) : r`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

function mapear<T, U>(r: Result<T>, f: (x: T) => U): Result<U> {
  return ___;
}

const enPasos: Result<number>[] = [ok(40), error('la flecha se perdió en el bosque')];
for (const m of enPasos) {
  const enMetros = mapear(m, (pasos) => `${pasos * 0.75} metros`);
  console.log(enMetros.ok ? enMetros.valor : `✗ ${enMetros.error}`);
}
```

#### Salida esperada
```
30 metros
✗ la flecha se perdió en el bosque
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

function mapear<T, U>(r: Result<T>, f: (x: T) => U): Result<U> {
  return r.ok ? ok(f(r.valor)) : r;
}

const enPasos: Result<number>[] = [ok(40), error('la flecha se perdió en el bosque')];
for (const m of enPasos) {
  const enMetros = mapear(m, (pasos) => `${pasos * 0.75} metros`);
  console.log(enMetros.ok ? enMetros.valor : `✗ ${enMetros.error}`);
}
```

#### Al superarla
Nima anota los 30 metros en su carcaj. La flecha perdida queda anotada como perdida, sin que el programa se rompa.

#### Imagen
- Una cinta métrica de latón desenrollada en el piso del taller, con una flecha al final.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas, arco verde) mide con pasos largos.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) anota; Gheco sentado sobre la flecha.

### Micro-misión S04-N01-P3 · Un paso después del otro

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Astrea
criatura: troll
carta: luego<T, U> | como mapear, pero f devuelve un Result · si el primer paso falla, el segundo no se hace
recompensa: xp 10, oro 10
```

#### Escena
Astrea anota alturas de estrellas escritas a mano. Primero hay que **leer** el número del texto (puede no ser un número), y después **revisar** que esté entre 0 y 90 grados (puede no estarlo).

#### Gheco sugiere
`luego` encadena: si el primer resultado está bien, se le pasa el valor al segundo paso, que devuelve su propio `Result`. Si el primero falló, se devuelve ese error.

#### Desafío
Completá el `return` de `luego`.

#### Pasos
1. Buscá el `___` en `luego`.
2. Cambialo por `r.ok ? f(r.valor) : r`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

function luego<T, U>(r: Result<T>, f: (x: T) => Result<U>): Result<U> {
  return ___;
}

const leerNumero = (s: string): Result<number> => (Number.isNaN(Number(s)) || s.trim() === '' ? error(`«${s}» no es un número`) : ok(Number(s)));
const altura = (g: number): Result<number> => (g >= 0 && g <= 90 ? ok(g) : error(`${g} grados no es una altura`));

for (const anotado of ['45', 'mucho', '120']) {
  const r = luego(leerNumero(anotado), altura);
  console.log(r.ok ? `✓ ${r.valor} grados` : `✗ ${r.error}`);
}
```

#### Salida esperada
```
✓ 45 grados
✗ «mucho» no es un número
✗ 120 grados no es una altura
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

function luego<T, U>(r: Result<T>, f: (x: T) => Result<U>): Result<U> {
  return r.ok ? f(r.valor) : r;
}

const leerNumero = (s: string): Result<number> => (Number.isNaN(Number(s)) || s.trim() === '' ? error(`«${s}» no es un número`) : ok(Number(s)));
const altura = (g: number): Result<number> => (g >= 0 && g <= 90 ? ok(g) : error(`${g} grados no es una altura`));

for (const anotado of ['45', 'mucho', '120']) {
  const r = luego(leerNumero(anotado), altura);
  console.log(r.ok ? `✓ ${r.valor} grados` : `✗ ${r.error}`);
}
```

#### Al superarla
Cada anotación de Astrea pasa por los dos pasos. Las que fallan dicen exactamente en cuál.

#### Imagen
- Una línea de montaje de bronce con dos estaciones: una lee papelitos, la otra los mide con un transportador.
- Un troll de cuerda chiquito atascado en la primera estación con un papel que dice algo sin números.
- Astrea (lechuza con anteojos de latón y chaleco azul) pone papelitos en la cinta; Rigel (chico flaco con pecas, antiparras de latón) gira una manivela; Gheco saca al troll.

### Micro-misión S04-N01-P4 · Con repuesto

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Nima
carta: valorO<T> | si r.ok, el valor · si no, el repuesto · el tipo del repuesto es el mismo T
recompensa: xp 15, monedas 5
```

#### Escena
El tablero del Mirador muestra el volumen del silbato. Si la configuración guardada está rota, tiene que usar un volumen de repuesto, sin quejarse.

#### Gheco sugiere
`valorO` saca el valor si lo hay; si no, devuelve el repuesto. El repuesto es del mismo tipo `T` que el valor.

#### Desafío
Completá el `return` de `valorO`.

#### Pasos
1. Buscá el `___` en `valorO`.
2. Cambialo por `r.ok ? r.valor : repuesto`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

function valorO<T>(r: Result<T>, repuesto: T): T {
  return ___;
}

const leerVolumen = (s: string): Result<number> => {
  const n = Number(s);
  return Number.isInteger(n) && n >= 0 && n <= 10 ? ok(n) : error('volumen roto');
};

for (const guardado of ['7', 'fuertísimo', '42']) {
  console.log(`Guardado «${guardado}» → volumen ${valorO(leerVolumen(guardado), 5)}`);
}
```

#### Salida esperada
```
Guardado «7» → volumen 7
Guardado «fuertísimo» → volumen 5
Guardado «42» → volumen 5
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

function valorO<T>(r: Result<T>, repuesto: T): T {
  return r.ok ? r.valor : repuesto;
}

const leerVolumen = (s: string): Result<number> => {
  const n = Number(s);
  return Number.isInteger(n) && n >= 0 && n <= 10 ? ok(n) : error('volumen roto');
};

for (const guardado of ['7', 'fuertísimo', '42']) {
  console.log(`Guardado «${guardado}» → volumen ${valorO(leerVolumen(guardado), 5)}`);
}
```

#### Al superarla
El silbato suena a volumen 5 aunque alguien haya escrito «fuertísimo» en la configuración. Nima se ríe: fue ella.

#### Imagen
- Un silbato de bronce con una perilla de volumen marcando la mitad.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) silba disimulando, con un papelito escondido.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) la mira de reojo; Gheco señala el papelito.

### Micro-misión S04-N01-P5 · Todos o ninguno

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Astrea
carta: todos<T> | recorre la lista · el primer error se devuelve · si no hay ninguno, ok con todos los valores
recompensa: xp 15, monedas 5
```

#### Escena
Astrea mide las cuatro estrellas de una constelación. Si **alguna** medición falló, no sirve dibujar la constelación: hay que avisar cuál.

#### Gheco sugiere
Se recorren los resultados. Al primer error, se devuelve ese error. Si se llega al final, se devuelve `ok` con la lista de valores.

#### Desafío
Completá la línea del error en `todos`.

#### Pasos
1. Buscá el `___` en `todos`.
2. Cambialo por `if (!r.ok) return r;`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

function todos<T>(rs: readonly Result<T>[]): Result<T[]> {
  const valores: T[] = [];
  for (const r of rs) {
    ___
    valores.push(r.valor);
  }
  return ok(valores);
}

const lira = todos([ok(8), ok(3), ok(4), ok(2)]);
const orion = todos([ok(7), error('Bellatrix tapada por una nube'), ok(6), error('Saiph muy baja')]);

console.log(lira.ok ? `Lira: ${lira.valor.join(', ')}` : `✗ ${lira.error}`);
console.log(orion.ok ? `Orión: ${orion.valor.join(', ')}` : `✗ ${orion.error}`);
```

#### Salida esperada
```
Lira: 8, 3, 4, 2
✗ Bellatrix tapada por una nube
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

function todos<T>(rs: readonly Result<T>[]): Result<T[]> {
  const valores: T[] = [];
  for (const r of rs) {
    if (!r.ok) return r;
    valores.push(r.valor);
  }
  return ok(valores);
}

const lira = todos([ok(8), ok(3), ok(4), ok(2)]);
const orion = todos([ok(7), error('Bellatrix tapada por una nube'), ok(6), error('Saiph muy baja')]);

console.log(lira.ok ? `Lira: ${lira.valor.join(', ')}` : `✗ ${lira.error}`);
console.log(orion.ok ? `Orión: ${orion.valor.join(', ')}` : `✗ ${orion.error}`);
```

#### Al superarla
La Lira se dibuja entera. Orión espera a que pase la nube. Astrea le da a Rigel una **estrella de latón** por la caja de herramientas.

#### Imagen
- Dos constelaciones en un mapa de vidrio: una completa y brillante, otra con una nube tapando una estrella.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) guarda la herramienta en el cajón; Gheco sopla la nube.

## S04-N02 · Validadores y tipos condicionales

```meta
tipo: tema
padre: S04-N01
precio: 10
criatura: ogre
temas: err.validacion, cal.tipos
usa: poo.genericos, func.orden-superior, func.closures
```

### Crónica

La segunda gaveta de `calibre.ts` es para los **validadores**: funciones que reciben cualquier cosa (`unknown`) y devuelven un `Result` con el valor ya revisado. Astrea quiere usarlos para las fichas de los **vigías**: los voluntarios que se anotan para cuidar el Mirador de noche.

—Lo lindo —dice Gheco— es que el validador dice qué tipo sale. Y con un truco del compilador, el tipo de la ficha entera sale solo, sin escribirlo dos veces.

### Objetivos

- Escribir validadores: `type Validador<T> = (x: unknown) => Result<T>`.
- Fabricar validadores con datos (`numeroEntre(10, 99)`), con clausuras.
- Conocer los **tipos condicionales** (`A extends B ? X : Y`) e `infer`.
- Armar el validador de un objeto entero a partir de un esquema, con el tipo calculado.
- Validar listas con un validador de elementos.

### Antes de empezar

- S04-N01.
- Tipos sacados de otros (R03-N05) y tipos que fabrican tipos (R03-N06).

### Explicación

#### Un validador
```typescript
type Validador<T> = (x: unknown) => Result<T>;

const texto = (): Validador<string> => (x) =>
  typeof x === 'string' && x.trim() !== '' ? ok(x.trim()) : error('tiene que ser un texto');
```

#### Validadores con datos
```typescript
const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);
```
La función de adentro **recuerda** `min` y `max` (es una clausura).

#### Tipos condicionales
Un tipo puede preguntar algo:
```typescript
type EsTexto<T> = T extends string ? 'sí' : 'no';
type A = EsTexto<'hola'>;   // 'sí'
type B = EsTexto<42>;       // 'no'
```
Y con `infer` puede **sacar** una parte de otro tipo:
```typescript
type DeValidador<V> = V extends Validador<infer T> ? T : never;
type D = DeValidador<Validador<number>>;   // number
```
Se lee: «si `V` es un validador de algo, llamá `T` a ese algo y devolvelo». Así está hecho por dentro `ReturnType`, que ya usaste en el Telescopio.

#### El tipo de la ficha, calculado
```typescript
type Esquema = Record<string, Validador<unknown>>;
type Forma<S extends Esquema> = { [K in keyof S]: DeValidador<S[K]> };

const validarVigia = objeto({ nombre: texto(), edad: numeroEntre(10, 99) });
// Validador<{ nombre: string; edad: number }>
```

### Código de ejemplo

```typescript
type Contenido<C> = C extends Array<infer E> ? E : C;
const a: Contenido<string[]> = 'hola';
const b: Contenido<number> = 7;
console.log(a, b);
```

### Salida esperada

```
hola 7
```

### ¿Para qué sirve?

Así funcionan bibliotecas muy usadas, como Zod: escribís el esquema una sola vez y de ahí sale **el validador** (que revisa al ejecutar) y **el tipo** (que revisa al compilar). Nunca se desincronizan.

### Errores habituales

**Ogro: escribir el tipo y el esquema por separado.** Si cambia uno y no el otro, el validador deja pasar algo que el tipo no permite.

**Goblin: un validador que devuelve el valor sin revisar.** Si devuelve `ok(x)` sin preguntar, `x` sigue siendo `unknown` y no compila.

**Esqueleto: `infer` afuera de un `extends`.** Solo se puede usar en la pregunta de un tipo condicional.

### Micro-misión S04-N02-P1 · El primer validador

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Astrea
criatura: goblin
carta: Validador<T> | (x: unknown) => Result<T> · pregunta typeof antes de devolver ok · recorta los espacios
recompensa: xp 10, oro 10
```

#### Escena
El primer validador de la gaveta revisa los **nombres** de los vigías: tiene que ser un texto, y no vacío.

#### Gheco sugiere
Primero se pregunta si `x` es un texto y si, sin espacios, tiene algo. Si sí, `ok` con el texto recortado. Si no, `error`.

#### Desafío
Completá la pregunta del validador.

#### Pasos
1. Buscá el `___` en `texto`.
2. Cambialo por `typeof x === 'string' && x.trim() !== ''`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

const texto = (): Validador<string> => (x) => (___ ? ok(x.trim()) : error('tiene que ser un texto'));

const validarNombre = texto();
for (const anotado of ['  Lucía ', '', 42, null]) {
  const r = validarNombre(anotado);
  console.log(r.ok ? `✓ «${r.valor}»` : `✗ ${r.error}`);
}
```

#### Salida esperada
```
✓ «Lucía»
✗ tiene que ser un texto
✗ tiene que ser un texto
✗ tiene que ser un texto
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

const texto = (): Validador<string> => (x) => (typeof x === 'string' && x.trim() !== '' ? ok(x.trim()) : error('tiene que ser un texto'));

const validarNombre = texto();
for (const anotado of ['  Lucía ', '', 42, null]) {
  const r = validarNombre(anotado);
  console.log(r.ok ? `✓ «${r.valor}»` : `✗ ${r.error}`);
}
```

#### Al superarla
El validador deja pasar a Lucía (sin los espacios) y frena todo lo demás.

#### Imagen
- Un tamiz de latón con papelitos cayendo: uno pasa, tres se quedan arriba.
- Un goblin chiquito con un engranaje en la espalda intentando meter un número por el tamiz.
- Astrea (lechuza con anteojos de latón y chaleco azul) sacude el tamiz; Rigel (chico flaco con pecas, antiparras de latón) mira; Gheco atrapa el papel que pasó.

### Micro-misión S04-N02-P2 · Validadores con medida

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Nima
carta: Fabricar validadores | numeroEntre(min, max) devuelve un Validador<number> · la función de adentro recuerda min y max
recompensa: xp 10, oro 10
```

#### Escena
Los vigías tienen que tener entre 10 y 99 años, y las guardias duran entre 1 y 8 horas. Rigel arma una sola herramienta que fabrica un validador para cada rango.

#### Gheco sugiere
`numeroEntre` recibe el rango y devuelve una función. Esa función, cuando la llamás, todavía se acuerda de `min` y `max`.

#### Desafío
Completá la pregunta del validador.

#### Pasos
1. Buscá el `___` en `numeroEntre`.
2. Cambialo por `typeof x === 'number' && x >= min && x <= max`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  ___ ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);

const edad = numeroEntre(10, 99);
const horas = numeroEntre(1, 8);
const mostrar = (r: Result<number>) => (r.ok ? `✓ ${r.valor}` : `✗ ${r.error}`);

console.log(`edad 14: ${mostrar(edad(14))}`);
console.log(`edad 7: ${mostrar(edad(7))}`);
console.log(`horas 3: ${mostrar(horas(3))}`);
console.log(`horas '3': ${mostrar(horas('3'))}`);
```

#### Salida esperada
```
edad 14: ✓ 14
edad 7: ✗ tiene que ser un número de 10 a 99
horas 3: ✓ 3
horas '3': ✗ tiene que ser un número de 1 a 8
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);

const edad = numeroEntre(10, 99);
const horas = numeroEntre(1, 8);
const mostrar = (r: Result<number>) => (r.ok ? `✓ ${r.valor}` : `✗ ${r.error}`);

console.log(`edad 14: ${mostrar(edad(14))}`);
console.log(`edad 7: ${mostrar(edad(7))}`);
console.log(`horas 3: ${mostrar(horas(3))}`);
console.log(`horas '3': ${mostrar(horas('3'))}`);
```

#### Al superarla
Nima prueba anotar a su hermanito de 7 años como vigía. El validador no lo deja. —Bueno —dice—, el año que viene.

#### Imagen
- Una regla de latón con dos topes ajustables que marcan un rango.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro) con un papel de inscripción rechazado, encogiéndose de hombros.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) ajusta los topes; Gheco mide su propia cola.

### Micro-misión S04-N02-P3 · Sacar el tipo de adentro

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Astrea
criatura: ogre
carta: Tipos condicionales con infer | V extends Validador<infer T> ? T : never · saca el tipo que valida · así está hecho ReturnType
recompensa: xp 10, oro 10
```

#### Escena
Astrea quiere saber, solo mirando un validador, qué tipo devuelve. Rigel escribe un tipo que **pregunta** y **saca** esa parte.

#### Gheco sugiere
Esta misión no se ejecuta: el compilador revisa los tipos. `DeValidador<V>` pregunta si `V` es un validador de algo; si sí, llama `T` a ese algo y lo devuelve. Cuando lo escribas bien, las tres líneas de abajo compilan.

#### Desafío
Escribí el tipo `DeValidador`.

#### Pasos
1. Tocá **Ejecutar**: el `___` no compila.
2. Cambialo por `V extends Validador<infer T> ? T : never`.
3. Tocá **Ejecutar**. Tiene que decir `Compila sin errores`.

#### Compilador
sí

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;

declare const texto: () => Validador<string>;
declare const numeroEntre: (min: number, max: number) => Validador<number>;

type DeValidador<V> = ___;

const nombre: DeValidador<ReturnType<typeof texto>> = 'Lucía';
const edad: DeValidador<ReturnType<typeof numeroEntre>> = 14;
const nada: DeValidador<string> = undefined as never;
```

#### Salida esperada
```
Compila sin errores
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;

declare const texto: () => Validador<string>;
declare const numeroEntre: (min: number, max: number) => Validador<number>;

type DeValidador<V> = V extends Validador<infer T> ? T : never;

const nombre: DeValidador<ReturnType<typeof texto>> = 'Lucía';
const edad: DeValidador<ReturnType<typeof numeroEntre>> = 14;
const nada: DeValidador<string> = undefined as never;
```

#### Al superarla
Astrea asiente despacio. —El compilador pregunta, igual que vos. Solo que pregunta por tipos.

#### Imagen
- Una lupa de latón enfocando una caja transparente con otra caja adentro, y una flecha que saca la de adentro.
- Un ogro de cuerda chiquito intentando abrir la caja de afuera a martillazos.
- Astrea (lechuza con anteojos de latón y chaleco azul) sostiene la lupa; Rigel (chico flaco con pecas, antiparras de latón) saca la caja de adentro; Gheco aplaude.

### Micro-misión S04-N02-P4 · La ficha del vigía

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Astrea
carta: objeto(esquema) | el esquema dice el validador de cada campo · Forma<S> calcula el tipo · el primer campo que falla da el error
recompensa: xp 15, monedas 5
```

#### Escena
Ya hay validadores para el nombre y para la edad. Rigel arma el de la **ficha entera** del vigía, a partir de un esquema. El tipo de la ficha sale solo.

#### Gheco sugiere
Se recorre cada campo del esquema y se valida su valor. Al primer campo que falla, se devuelve el error con el nombre del campo. Falta esa línea.

#### Desafío
Completá la línea del error en `objeto`.

#### Pasos
1. Buscá el `___` en `objeto`.
2. Cambialo por ``if (!r.ok) return error(`${clave}: ${r.error}`);``.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });
const texto = (): Validador<string> => (x) => (typeof x === 'string' && x.trim() !== '' ? ok(x.trim()) : error('tiene que ser un texto'));
const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);

type DeValidador<V> = V extends Validador<infer T> ? T : never;
type Esquema = Record<string, Validador<unknown>>;
type Forma<S extends Esquema> = { [K in keyof S]: DeValidador<S[K]> };

function objeto<S extends Esquema>(esquema: S): Validador<Forma<S>> {
  return (x) => {
    if (typeof x !== 'object' || x === null) return error('no es una ficha');
    const campos = x as Record<string, unknown>;
    const salida: Record<string, unknown> = {};
    for (const clave of Object.keys(esquema)) {
      const r = esquema[clave](campos[clave]);
      ___
      salida[clave] = r.valor;
    }
    return ok(salida as Forma<S>);
  };
}

const validarVigia = objeto({ nombre: texto(), edad: numeroEntre(10, 99) });

for (const ficha of [{ nombre: 'Lucía', edad: 14 }, { nombre: 'Tomás', edad: 6 }, { edad: 30 }]) {
  const r = validarVigia(ficha);
  console.log(r.ok ? `✓ ${r.valor.nombre.toUpperCase()} (${r.valor.edad + 1} el año que viene)` : `✗ ${r.error}`);
}
```

#### Salida esperada
```
✓ LUCÍA (15 el año que viene)
✗ edad: tiene que ser un número de 10 a 99
✗ nombre: tiene que ser un texto
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });
const texto = (): Validador<string> => (x) => (typeof x === 'string' && x.trim() !== '' ? ok(x.trim()) : error('tiene que ser un texto'));
const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);

type DeValidador<V> = V extends Validador<infer T> ? T : never;
type Esquema = Record<string, Validador<unknown>>;
type Forma<S extends Esquema> = { [K in keyof S]: DeValidador<S[K]> };

function objeto<S extends Esquema>(esquema: S): Validador<Forma<S>> {
  return (x) => {
    if (typeof x !== 'object' || x === null) return error('no es una ficha');
    const campos = x as Record<string, unknown>;
    const salida: Record<string, unknown> = {};
    for (const clave of Object.keys(esquema)) {
      const r = esquema[clave](campos[clave]);
      if (!r.ok) return error(`${clave}: ${r.error}`);
      salida[clave] = r.valor;
    }
    return ok(salida as Forma<S>);
  };
}

const validarVigia = objeto({ nombre: texto(), edad: numeroEntre(10, 99) });

for (const ficha of [{ nombre: 'Lucía', edad: 14 }, { nombre: 'Tomás', edad: 6 }, { edad: 30 }]) {
  const r = validarVigia(ficha);
  console.log(r.ok ? `✓ ${r.valor.nombre.toUpperCase()} (${r.valor.edad + 1} el año que viene)` : `✗ ${r.error}`);
}
```

#### Al superarla
Rigel no escribió en ningún lado que `r.valor.nombre` es un texto y `r.valor.edad` un número: el compilador lo sacó del esquema. Astrea guarda la herramienta en la gaveta con mucho cuidado.

#### Imagen
- Una ficha de cartón pasando por una máquina de latón con dos ranuras (una para letras, otra para números).
- Astrea (lechuza con anteojos de latón y chaleco azul) guarda una herramienta en una gaveta con terciopelo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) pone una ficha en la máquina; Gheco sale por la otra punta con la ficha aprobada.

### Micro-misión S04-N02-P5 · Validar listas

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Nima
carta: lista(v) | un Validador<T[]> a partir de un Validador<T> · Array.isArray · el error dice en qué posición
recompensa: xp 15, monedas 5
```

#### Escena
Nima trae la lista de guardias de la semana: las horas de cada noche. Rigel arma un validador de **listas** que usa el de cada elemento, y dice en qué posición está el problema.

#### Gheco sugiere
Si no es un arreglo, error. Si lo es, se valida cada elemento con `v`. Al primero que falla, se devuelve el error con su posición.

#### Desafío
Completá el recorrido en `lista`.

#### Pasos
1. Buscá el `___` en `lista`.
2. Cambialo por ``const r = v(x[i]); if (!r.ok) return error(`posición ${i}: ${r.error}`); valores.push(r.valor);``.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });
const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);

const lista = <T,>(v: Validador<T>): Validador<T[]> => (x) => {
  if (!Array.isArray(x)) return error('no es una lista');
  const valores: T[] = [];
  for (let i = 0; i < x.length; i++) {
    ___
  }
  return ok(valores);
};

const validarSemana = lista(numeroEntre(1, 8));
for (const semana of [[2, 4, 3, 8], [2, 12, 3], 'tres']) {
  const r = validarSemana(semana);
  console.log(r.ok ? `✓ ${r.valor.reduce((a, b) => a + b, 0)} horas en total` : `✗ ${r.error}`);
}
```

#### Salida esperada
```
✓ 17 horas en total
✗ posición 1: tiene que ser un número de 1 a 8
✗ no es una lista
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });
const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);

const lista = <T,>(v: Validador<T>): Validador<T[]> => (x) => {
  if (!Array.isArray(x)) return error('no es una lista');
  const valores: T[] = [];
  for (let i = 0; i < x.length; i++) {
    const r = v(x[i]); if (!r.ok) return error(`posición ${i}: ${r.error}`); valores.push(r.valor);
  }
  return ok(valores);
};

const validarSemana = lista(numeroEntre(1, 8));
for (const semana of [[2, 4, 3, 8], [2, 12, 3], 'tres']) {
  const r = validarSemana(semana);
  console.log(r.ok ? `✓ ${r.valor.reduce((a, b) => a + b, 0)} horas en total` : `✗ ${r.error}`);
}
```

#### Al superarla
La semana de 17 horas queda aprobada. La de 12 horas seguidas, no: —Nadie cuida el Mirador 12 horas sin dormir —dice Nima.

#### Imagen
- Un calendario de latón con siete casilleros, uno marcado en rojo.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) bosteza exageradamente señalando el casillero rojo.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) tacha el casillero; Gheco duerme encima del calendario.

## S04-N03 · El formulario que valida

```meta
tipo: tema
padre: S04-N02
precio: 10
criatura: goblin
temas: js.formularios
usa: err.validacion, js.dom, js.eventos, js.almacenamiento, cal.tipos
```

### Crónica

Astrea cuelga en la entrada del Mirador un cartel: *Se buscan vigías*. Para anotarse, hay un **formulario**: nombre, edad y turno (temprano, medianoche o madrugada). Rigel lo conecta a las herramientas del calibre: cada campo se valida, cada error se muestra al lado de su campo, y la ficha se guarda solo si está todo bien.

### Objetivos

- Leer los campos de un formulario con su tipo (`valueAsNumber`, el `value` de un `select`).
- Convertir el valor de un `select` en una unión con un guardia.
- Mostrar un error al lado de cada campo con `Partial<Record<Campo, string>>`.
- Validar mientras se escribe.
- Guardar la ficha en el almacenamiento y volver a leerla con el validador.

### Antes de empezar

- S04-N01 y S04-N02.
- La página tipada (R04-N04).

### Explicación

#### Leer con tipo
```typescript
const edad = obtenerElemento<HTMLInputElement>('#edad');
edad.value;          // string: '14'
edad.valueAsNumber;  // number: 14 (o NaN si está vacío)
```

#### Un error por campo
```typescript
type Campo = 'nombre' | 'edad' | 'turno';
type Errores = Partial<Record<Campo, string>>;
```
`Partial`: solo están los campos que tienen error.

#### Validar al escribir
El evento `input` salta con cada letra. Validar ahí ayuda a corregir antes de mandar; pero el error se muestra recién cuando el campo tiene algo escrito, para no retar a nadie antes de tiempo.

### Código de ejemplo

```typescript
type Campo = 'nombre' | 'edad';
const errores: Partial<Record<Campo, string>> = {};
errores.edad = 'es muy chico';
console.log(errores, 'nombre' in errores);
```

### Salida esperada

```
{ edad: 'es muy chico' } false
```

### ¿Para qué sirve?

Todos los formularios de la web hacen esto: inscripciones, compras, registros. Un formulario que dice **qué** está mal y **dónde**, antes de mandar, es la diferencia entre que la gente lo complete o lo abandone.

### Errores habituales

**Goblin: el número como texto.** `edad.value` es un `string`: `'14' + 1` da `'141'`. Con `valueAsNumber` es un número.

**Ogro: un error para todo el formulario.** «Algo está mal» no ayuda. Un error al lado de cada campo, sí.

**Esqueleto: confiar en el `select`.** Su `value` es un `string` cualquiera: se pasa por un guardia antes de usarlo como `Turno`.

### Micro-misión S04-N03-P1 · La edad como número

```meta
lugar: La entrada del Mirador
personajes: Rigel, Gheco, Astrea
criatura: goblin
carta: valueAsNumber | value es string · valueAsNumber es number (NaN si está vacío) · con el número se puede sumar
recompensa: xp 10, oro 10
```

#### Escena
El formulario calcula en qué año el vigía cumple la mayoría de edad. Con `edad.value`, para alguien de 14 da un año rarísimo.

#### Gheco sugiere
`edad.value` es texto: `'14'`. Leé el error del compilador y usá `valueAsNumber`, que ya es un número.

#### Desafío
Leé la edad como número.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `edad.value` por `edad.valueAsNumber`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #0b1326; color: #e8d9b0; padding: 20px; }
  input { padding: 6px; background: #1a2440; color: #f2c14e; border: 2px solid #8d6e3f; }
  #vista { color: #f2c14e; }
</style>
<label>Edad: <input id="edad" type="number"></label>
<p id="vista"></p>
```

#### Eventos
```
escribir #edad 14
```

#### Estado
```
#vista
```

#### Código inicial
```typescript
function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const edad = obtenerElemento<HTMLInputElement>('#edad');
const vista = obtenerElemento<HTMLParagraphElement>('#vista');

edad.addEventListener('input', () => {
  const años: number = edad.value;
  vista.textContent = Number.isNaN(años) ? 'Escribí tu edad' : `Faltan ${18 - años} años para los 18`;
});
```

#### Salida esperada
```
── Estado ──
#vista: Faltan 4 años para los 18
```

#### Solución
```typescript
function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const edad = obtenerElemento<HTMLInputElement>('#edad');
const vista = obtenerElemento<HTMLParagraphElement>('#vista');

edad.addEventListener('input', () => {
  const años: number = edad.valueAsNumber;
  vista.textContent = Number.isNaN(años) ? 'Escribí tu edad' : `Faltan ${18 - años} años para los 18`;
});
```

#### Al superarla
El formulario hace la cuenta bien: faltan 4 años. Astrea sonríe: no hace falta ser mayor para cuidar estrellas.

#### Imagen
- Un formulario de pergamino en un atril de latón, con un campo para la edad.
- Un goblin chiquito con un engranaje en la espalda pegando comillas alrededor de un número.
- Astrea (lechuza con anteojos de latón y chaleco azul) señala el formulario; Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) despega las comillas; Gheco mira.

### Micro-misión S04-N03-P2 · El turno elegido

```meta
lugar: La entrada del Mirador
personajes: Rigel, Gheco, Nima
criatura: skeleton
carta: El select con un guardia | value es string · esTurno(x): x is Turno con includes · después ya es la unión
recompensa: xp 10, oro 10
```

#### Escena
El formulario tiene un desplegable con los tres turnos. Para el programa, lo elegido es un texto cualquiera. Rigel lo pasa por un guardia para convertirlo en un `Turno`.

#### Gheco sugiere
`TURNOS.includes(x)` no anda directo: `includes` de un `readonly Turno[]` pide un `Turno`. Se usa `TURNOS.some((t) => t === x)`, que acepta cualquier texto.

#### Desafío
Completá el guardia `esTurno`.

#### Pasos
1. Buscá el `___` en `esTurno`.
2. Cambialo por `return TURNOS.some((t) => t === x);`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #0b1326; color: #e8d9b0; padding: 20px; }
  select { padding: 6px; background: #1a2440; color: #f2c14e; border: 2px solid #8d6e3f; }
  #vista { color: #f2c14e; }
</style>
<label>Turno:
  <select id="turno">
    <option value="">Elegí…</option>
    <option value="temprano">Temprano</option>
    <option value="medianoche">Medianoche</option>
    <option value="madrugada">Madrugada</option>
  </select>
</label>
<p id="vista"></p>
```

#### Eventos
```
elegir #turno medianoche
```

#### Estado
```
#vista
```

#### Código inicial
```typescript
const TURNOS = ['temprano', 'medianoche', 'madrugada'] as const;
type Turno = (typeof TURNOS)[number];
const HORA: Record<Turno, string> = { temprano: '20 a 24', medianoche: '0 a 4', madrugada: '4 a 8' };

function esTurno(x: string): x is Turno {
  ___
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const turno = obtenerElemento<HTMLSelectElement>('#turno');
const vista = obtenerElemento<HTMLParagraphElement>('#vista');

turno.addEventListener('change', () => {
  const elegido = turno.value;
  vista.textContent = esTurno(elegido) ? `Turno ${elegido}: de ${HORA[elegido]} h` : 'Elegí un turno';
});
```

#### Salida esperada
```
── Estado ──
#vista: Turno medianoche: de 0 a 4 h
```

#### Solución
```typescript
const TURNOS = ['temprano', 'medianoche', 'madrugada'] as const;
type Turno = (typeof TURNOS)[number];
const HORA: Record<Turno, string> = { temprano: '20 a 24', medianoche: '0 a 4', madrugada: '4 a 8' };

function esTurno(x: string): x is Turno {
  return TURNOS.some((t) => t === x);
}

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const turno = obtenerElemento<HTMLSelectElement>('#turno');
const vista = obtenerElemento<HTMLParagraphElement>('#vista');

turno.addEventListener('change', () => {
  const elegido = turno.value;
  vista.textContent = esTurno(elegido) ? `Turno ${elegido}: de ${HORA[elegido]} h` : 'Elegí un turno';
});
```

#### Al superarla
Nima elige medianoche, el turno de las estrellas fugaces. El formulario le dice el horario exacto.

#### Imagen
- Un desplegable de latón con tres placas: un sol poniente, una luna llena y un amanecer.
- Un esqueleto de alambre chiquito colgando una placa falsa.
- Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro) elige la luna; Rigel (chico flaco con pecas, antiparras de latón) saca la placa falsa; Gheco mira la luna.

### Micro-misión S04-N03-P3 · Cada error en su lugar

```meta
lugar: La entrada del Mirador
personajes: Rigel, Gheco, Astrea
criatura: ogre
carta: Partial<Record<Campo, string>> | un error por campo · se escribe en el span de ese campo · el que no tiene error queda vacío
recompensa: xp 10, oro 10
```

#### Escena
Al mandar el formulario con datos malos, aparecía un cartel enorme: *Algo está mal*. Astrea quiere un error **al lado de cada campo**.

#### Gheco sugiere
`validar` devuelve un `Partial<Record<Campo, string>>`. En `mostrar`, para cada campo, se escribe su error en su `span` (o nada, si no tiene). Falta esa línea.

#### Desafío
Completá la línea de `mostrar`.

#### Pasos
1. Buscá el `___` en `mostrar`.
2. Cambialo por ``obtenerElemento<HTMLSpanElement>(`#error-${campo}`).textContent = errores[campo] ?? '';``.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #0b1326; color: #e8d9b0; padding: 20px; }
  input { padding: 6px; background: #1a2440; color: #f2c14e; border: 2px solid #8d6e3f; }
  .error { color: #e57373; margin-left: 8px; }
  p { margin: 8px 0; }
</style>
<form>
  <p><label>Nombre: <input id="nombre"></label><span class="error" id="error-nombre"></span></p>
  <p><label>Edad: <input id="edad" type="number"></label><span class="error" id="error-edad"></span></p>
  <button>Anotarme</button>
</form>
```

#### Eventos
```
escribir #nombre Tomás
escribir #edad 7
enviar form
```

#### Estado
```
#error-nombre
#error-edad
```

#### Código inicial
```typescript
type Campo = 'nombre' | 'edad';
type Errores = Partial<Record<Campo, string>>;
const CAMPOS: readonly Campo[] = ['nombre', 'edad'];

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const nombre = obtenerElemento<HTMLInputElement>('#nombre');
const edad = obtenerElemento<HTMLInputElement>('#edad');

function validar(): Errores {
  const errores: Errores = {};
  if (nombre.value.trim() === '') errores.nombre = 'escribí tu nombre';
  const años = edad.valueAsNumber;
  if (Number.isNaN(años) || años < 10 || años > 99) errores.edad = 'tiene que ser de 10 a 99';
  return errores;
}

function mostrar(errores: Errores): void {
  for (const campo of CAMPOS) {
    ___
  }
}

obtenerElemento<HTMLFormElement>('form').addEventListener('submit', (e: SubmitEvent) => {
  e.preventDefault();
  mostrar(validar());
});
```

#### Salida esperada
```
── Estado ──
#error-nombre: (vacío)
#error-edad: tiene que ser de 10 a 99
```

#### Solución
```typescript
type Campo = 'nombre' | 'edad';
type Errores = Partial<Record<Campo, string>>;
const CAMPOS: readonly Campo[] = ['nombre', 'edad'];

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const nombre = obtenerElemento<HTMLInputElement>('#nombre');
const edad = obtenerElemento<HTMLInputElement>('#edad');

function validar(): Errores {
  const errores: Errores = {};
  if (nombre.value.trim() === '') errores.nombre = 'escribí tu nombre';
  const años = edad.valueAsNumber;
  if (Number.isNaN(años) || años < 10 || años > 99) errores.edad = 'tiene que ser de 10 a 99';
  return errores;
}

function mostrar(errores: Errores): void {
  for (const campo of CAMPOS) {
    obtenerElemento<HTMLSpanElement>(`#error-${campo}`).textContent = errores[campo] ?? '';
  }
}

obtenerElemento<HTMLFormElement>('form').addEventListener('submit', (e: SubmitEvent) => {
  e.preventDefault();
  mostrar(validar());
});
```

#### Al superarla
El nombre de Tomás está bien; la edad, no, y el error aparece justo al lado. Tomás entiende enseguida qué pasó.

#### Imagen
- El formulario de pergamino con una marca roja al lado de un solo campo.
- Un ogro de cuerda chiquito con un cartel enorme que dice algo sin texto legible, que nadie mira.
- Astrea (lechuza con anteojos de latón y chaleco azul) señala la marca roja; Rigel (chico flaco con pecas, antiparras de latón) asiente; Gheco le saca el cartel al ogro.

### Micro-misión S04-N03-P4 · Mientras escribís

```meta
lugar: La entrada del Mirador
personajes: Rigel, Gheco, Nima
carta: Validar con input | cada campo valida al escribir · el error aparece solo si el campo tiene algo · la ayuda llega antes de mandar
recompensa: xp 15, monedas 5
```

#### Escena
Nima prefiere que el formulario avise **mientras** escribe, no al final. Pero que no la rete antes de empezar.

#### Gheco sugiere
Se escucha el evento `input` del campo de edad. Si tiene algo escrito, se valida y se muestra el error (o se borra). Falta conectar el evento.

#### Desafío
Conectá el evento `input` de la edad.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `edad.addEventListener('input', () => revisar(edad, 'edad'));`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #0b1326; color: #e8d9b0; padding: 20px; }
  input { padding: 6px; background: #1a2440; color: #f2c14e; border: 2px solid #8d6e3f; }
  .error { color: #e57373; margin-left: 8px; }
</style>
<p><label>Nombre: <input id="nombre"></label><span class="error" id="error-nombre"></span></p>
<p><label>Edad: <input id="edad" type="number"></label><span class="error" id="error-edad"></span></p>
```

#### Eventos
```
escribir #edad 120
```

#### Estado
```
#error-nombre
#error-edad
```

#### Código inicial
```typescript
type Campo = 'nombre' | 'edad';

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const REGLAS: Record<Campo, (campo: HTMLInputElement) => string | null> = {
  nombre: (c) => (c.value.trim() === '' ? 'escribí tu nombre' : null),
  edad: (c) => (c.valueAsNumber >= 10 && c.valueAsNumber <= 99 ? null : 'tiene que ser de 10 a 99'),
};

function revisar(input: HTMLInputElement, campo: Campo): void {
  const span = obtenerElemento<HTMLSpanElement>(`#error-${campo}`);
  span.textContent = input.value === '' ? '' : (REGLAS[campo](input) ?? '');
}

const nombre = obtenerElemento<HTMLInputElement>('#nombre');
const edad = obtenerElemento<HTMLInputElement>('#edad');
nombre.addEventListener('input', () => revisar(nombre, 'nombre'));
___
```

#### Salida esperada
```
── Estado ──
#error-nombre: (vacío)
#error-edad: tiene que ser de 10 a 99
```

#### Solución
```typescript
type Campo = 'nombre' | 'edad';

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const REGLAS: Record<Campo, (campo: HTMLInputElement) => string | null> = {
  nombre: (c) => (c.value.trim() === '' ? 'escribí tu nombre' : null),
  edad: (c) => (c.valueAsNumber >= 10 && c.valueAsNumber <= 99 ? null : 'tiene que ser de 10 a 99'),
};

function revisar(input: HTMLInputElement, campo: Campo): void {
  const span = obtenerElemento<HTMLSpanElement>(`#error-${campo}`);
  span.textContent = input.value === '' ? '' : (REGLAS[campo](input) ?? '');
}

const nombre = obtenerElemento<HTMLInputElement>('#nombre');
const edad = obtenerElemento<HTMLInputElement>('#edad');
nombre.addEventListener('input', () => revisar(nombre, 'nombre'));
edad.addEventListener('input', () => revisar(edad, 'edad'));
```

#### Al superarla
Nima escribe 120 de edad, en broma, y el formulario le avisa al instante. El nombre, que todavía está vacío, no dice nada.

#### Imagen
- El formulario de pergamino con un campo brillando en rojo mientras se escribe.
- Nima (trenza negra con hilo amarillo, chaqueta de cuero negra) escribe con una pluma, riéndose.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) la mira; Gheco imita a un viejito de 120 años con bastón.

### Micro-misión S04-N03-P5 · Anotado en el libro

```meta
lugar: La entrada del Mirador
personajes: Rigel, Gheco, Astrea
carta: Guardar y releer | si no hay errores, JSON.stringify al almacenamiento · al leerlo, JSON.parse y el validador · nunca se confía en lo guardado
recompensa: xp 15, monedas 5
```

#### Escena
Cuando la ficha está bien, se guarda en el **libro de vigías** (el almacenamiento del Mirador). Al día siguiente, Astrea la vuelve a leer, pasándola por el validador por si alguien tocó el libro.

#### Gheco sugiere
Si la ficha valida, se guarda con `JSON.stringify`. Falta esa línea, en el caso bueno.

#### Desafío
Completá la línea que guarda la ficha.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `localStorage.setItem('vigia', JSON.stringify(r.valor));`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #0b1326; color: #e8d9b0; padding: 20px; }
  input { padding: 6px; background: #1a2440; color: #f2c14e; border: 2px solid #8d6e3f; }
  #aviso { color: #f2c14e; }
</style>
<form>
  <p><label>Nombre: <input id="nombre"></label></p>
  <p><label>Edad: <input id="edad" type="number"></label></p>
  <button>Anotarme</button>
</form>
<p id="aviso"></p>
```

#### Eventos
```
escribir #nombre Lucía
escribir #edad 14
enviar form
```

#### Estado
```
#aviso
local vigia
```

#### Código inicial
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

const validarVigia: Validador<{ nombre: string; edad: number }> = (x) => {
  if (typeof x !== 'object' || x === null) return error('no es una ficha');
  if (!('nombre' in x) || typeof x.nombre !== 'string' || x.nombre.trim() === '') return error('nombre: escribí tu nombre');
  if (!('edad' in x) || typeof x.edad !== 'number' || x.edad < 10 || x.edad > 99) return error('edad: tiene que ser de 10 a 99');
  return ok({ nombre: x.nombre.trim(), edad: x.edad });
};

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const nombre = obtenerElemento<HTMLInputElement>('#nombre');
const edad = obtenerElemento<HTMLInputElement>('#edad');
const aviso = obtenerElemento<HTMLParagraphElement>('#aviso');

obtenerElemento<HTMLFormElement>('form').addEventListener('submit', (e: SubmitEvent) => {
  e.preventDefault();
  const r = validarVigia({ nombre: nombre.value, edad: edad.valueAsNumber });
  if (!r.ok) {
    aviso.textContent = `✗ ${r.error}`;
    return;
  }
  ___
  const releido = validarVigia(JSON.parse(localStorage.getItem('vigia') ?? 'null'));
  aviso.textContent = releido.ok ? `Anotada: ${releido.valor.nombre}, ${releido.valor.edad} años` : `✗ el libro está roto`;
});
```

#### Salida esperada
```
── Estado ──
#aviso: Anotada: Lucía, 14 años
local vigia: {"nombre":"Lucía","edad":14}
```

#### Solución
```typescript
type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
type Validador<T> = (x: unknown) => Result<T>;
const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

const validarVigia: Validador<{ nombre: string; edad: number }> = (x) => {
  if (typeof x !== 'object' || x === null) return error('no es una ficha');
  if (!('nombre' in x) || typeof x.nombre !== 'string' || x.nombre.trim() === '') return error('nombre: escribí tu nombre');
  if (!('edad' in x) || typeof x.edad !== 'number' || x.edad < 10 || x.edad > 99) return error('edad: tiene que ser de 10 a 99');
  return ok({ nombre: x.nombre.trim(), edad: x.edad });
};

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const nombre = obtenerElemento<HTMLInputElement>('#nombre');
const edad = obtenerElemento<HTMLInputElement>('#edad');
const aviso = obtenerElemento<HTMLParagraphElement>('#aviso');

obtenerElemento<HTMLFormElement>('form').addEventListener('submit', (e: SubmitEvent) => {
  e.preventDefault();
  const r = validarVigia({ nombre: nombre.value, edad: edad.valueAsNumber });
  if (!r.ok) {
    aviso.textContent = `✗ ${r.error}`;
    return;
  }
  localStorage.setItem('vigia', JSON.stringify(r.valor));
  const releido = validarVigia(JSON.parse(localStorage.getItem('vigia') ?? 'null'));
  aviso.textContent = releido.ok ? `Anotada: ${releido.valor.nombre}, ${releido.valor.edad} años` : `✗ el libro está roto`;
});
```

#### Al superarla
Lucía queda anotada en el libro de vigías. Esa noche hace su primera guardia, y ve una estrella fugaz. Astrea le da a Rigel una **estrella de latón**.

#### Imagen
- Un libro grande de cuero con un renglón nuevo escrito con tinta dorada.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da una ficha con una estrella a Rigel.
- Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) cierra el libro; Gheco mira por la ventana una estrella fugaz.

## S04-N04 · Jefe: la Urraca de Cobre

```meta
tipo: jefe
padre: S04-N03
precio: 10
criatura: dragon
insignia: Caja del Calibre
insignia_descripcion: Recuperaste las herramientas que robó la Urraca de Cobre: una biblioteca de tipos propia, en su módulo, que todos pueden usar sin romperla.
usa: js.modulos, err.validacion, err.opcionales, poo.genericos, cal.build, js.fetch, js.formularios
```

### Crónica

Una mañana, el taller de Rigel está revuelto. Faltan herramientas, otras están cambiadas de cajón, y en la ventana hay plumas de metal. Desde el techo del Mirador, un pájaro de cobre con ojos de vidrio verde mira todo con la cabeza ladeada: **la Urraca de Cobre**. Le gusta todo lo que brilla, y las herramientas del calibre brillan mucho.

—No te las va a devolver —dice Nima—. Pero si ponés las herramientas en un **módulo**, con sus tipos y sus reglas, todos los programas del Mirador las usan desde ahí, y la Urraca no puede cambiar nada sin que el compilador lo note.

### Objetivos

- Guardar la biblioteca en su propio módulo (`calibre.ts`) e importarla.
- Usar `import type` cuando se trae solo un tipo (`verbatimModuleSyntax`).
- Usar una biblioteca vieja de JavaScript con su archivo de declaraciones `.d.ts`.
- Usar la biblioteca en una página y con lo que llega del Puerto.

### Antes de empezar

- Toda la Senda (S04-N01 a N03).
- Módulos tipados (R03-N07) y `.d.ts` (R04-N08).

### Explicación

#### La biblioteca en un módulo
```typescript
// calibre.ts
export type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
export const texto = (): Validador<string> => …;

// main.ts
import { texto, type Result } from './calibre.js';
```

#### `import type` obligatorio
Con la opción `verbatimModuleSyntax`, el compilador **exige** marcar con `type` lo que solo es un tipo. Así, al pasar a JavaScript, se sabe exactamente qué se borra y qué queda.

#### Las trampas de la Urraca (y la verdad)
| La Urraca dice… | La verdad |
|---|---|
| "copiá las herramientas en cada programa" | una sola biblioteca, importada: se arregla una vez |
| "importá el tipo como si fuera un valor" | con `verbatimModuleSyntax`, `type` es obligatorio |
| "la biblioteca vieja acepta cualquier cosa" | su `.d.ts` dice qué acepta |
| "lo que llega del Puerto ya está bien" | pasa por el validador, como todo |

### Micro-misión S04-N04-P1 · Las herramientas en su caja

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Nima, la Urraca de Cobre
criatura: goblin
carta: Trampa 1 | la biblioteca en calibre.ts · import { … } from './calibre.js' · una sola copia para todos
recompensa: xp 15, monedas 3
```

#### Escena
La Urraca se llevó las copias de las herramientas que estaban en cada programa. Rigel deja **una sola copia** en `calibre.ts`, y el programa de los vigías la importa.

#### Gheco sugiere
Mirá el archivo `calibre.ts` en el tablero: exporta `texto` y `numeroEntre`. Se importan con su nombre, desde `'./calibre.js'` (con `.js`, aunque el archivo sea `.ts`).

#### Desafío
Completá el `import`.

#### Pasos
1. Buscá el `___` en la primera línea.
2. Cambialo por `import { numeroEntre, texto } from './calibre.js';`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Archivos
calibre.ts
```typescript
export type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
export type Validador<T> = (x: unknown) => Result<T>;

export const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
export const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

export const texto = (): Validador<string> => (x) =>
  typeof x === 'string' && x.trim() !== '' ? ok(x.trim()) : error('tiene que ser un texto');

export const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);
```

#### Código inicial
```typescript
___

const nombre = texto();
const edad = numeroEntre(10, 99);

for (const [n, e] of [['Lucía', 14], ['', 20], ['Tomás', 6]] as const) {
  const rn = nombre(n);
  const re = edad(e);
  console.log(rn.ok && re.ok ? `✓ ${rn.valor} (${re.valor})` : `✗ ${!rn.ok ? rn.error : !re.ok ? re.error : ''}`);
}
```

#### Salida esperada
```
✓ Lucía (14)
✗ tiene que ser un texto
✗ tiene que ser un número de 10 a 99
```

#### Solución
```typescript
import { numeroEntre, texto } from './calibre.js';

const nombre = texto();
const edad = numeroEntre(10, 99);

for (const [n, e] of [['Lucía', 14], ['', 20], ['Tomás', 6]] as const) {
  const rn = nombre(n);
  const re = edad(e);
  console.log(rn.ok && re.ok ? `✓ ${rn.valor} (${re.valor})` : `✗ ${!rn.ok ? rn.error : !re.ok ? re.error : ''}`);
}
```

#### Al superarla
La caja del calibre queda cerrada con un candado de latón. Los programas sacan las herramientas de ahí, y la Urraca ya no tiene copias que robar.

#### Imagen
- Una caja de herramientas de latón con candado, rotulada con una placa, y cables de cobre que salen hacia varias máquinas.
- Una urraca mecánica de cobre con ojos de vidrio verde, posada en la ventana, mirando la caja con codicia.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) cierra el candado; Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) vigila a la urraca; Gheco abraza la caja.

### Micro-misión S04-N04-P2 · Solo el tipo

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, la Urraca de Cobre
criatura: skeleton
carta: Trampa 2 | con verbatimModuleSyntax, un tipo se importa con type (TS1484) · import { texto, type Result } · el tipo se borra al compilar
recompensa: xp 15, monedas 3
```

#### Escena
La Urraca cambió la configuración del Mirador: ahora el compilador es más estricto con los `import`. El programa trae `Result` como si fuera un valor, y no compila.

#### Gheco sugiere
Mirá el `tsconfig` en el tablero: `verbatimModuleSyntax`. Con esa opción, lo que es **solo un tipo** se marca con `type` en el `import`. Leé el error.

#### Desafío
Marcá el tipo en el `import`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `import { Result, texto } from './calibre.js';` por `import { type Result, texto } from './calibre.js';`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### tsconfig
```json
{ "verbatimModuleSyntax": true }
```

#### Archivos
calibre.ts
```typescript
export type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
export type Validador<T> = (x: unknown) => Result<T>;

export const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
export const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

export const texto = (): Validador<string> => (x) =>
  typeof x === 'string' && x.trim() !== '' ? ok(x.trim()) : error('tiene que ser un texto');
```

#### Código inicial
```typescript
import { Result, texto } from './calibre.js';

function saludo(r: Result<string>): string {
  return r.ok ? `¡Hola, ${r.valor}!` : `✗ ${r.error}`;
}

console.log(saludo(texto()('Rigel')));
console.log(saludo(texto()('   ')));
```

#### Salida esperada
```
¡Hola, Rigel!
✗ tiene que ser un texto
```

#### Solución
```typescript
import { type Result, texto } from './calibre.js';

function saludo(r: Result<string>): string {
  return r.ok ? `¡Hola, ${r.valor}!` : `✗ ${r.error}`;
}

console.log(saludo(texto()('Rigel')));
console.log(saludo(texto()('   ')));
```

#### Al superarla
El `import` queda prolijo: lo que es valor, como valor; lo que es tipo, como tipo. La Urraca se rasca la cabeza con una pata: el compilador entendió el truco.

#### Imagen
- Una etiqueta de latón con la palabra grabada «type» (única palabra legible) pegada a una caja transparente.
- Un esqueleto de alambre chiquito intentando sacar algo de la caja transparente, que está vacía.
- La urraca mecánica de cobre confundida en la ventana; Rigel (chico flaco con pecas, antiparras de latón, chaleco marrón) pega la etiqueta; Gheco la alisa.

### Micro-misión S04-N04-P3 · El reloj de Don Péndulo

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Don Péndulo, la Urraca de Cobre
criatura: ogre
carta: Trampa 3 | reloj.js es JavaScript viejo · reloj.d.ts dice qué acepta · horaDe('90') no compila (TS2345): pide un número
recompensa: xp 15, monedas 3
```

#### Escena
Don Péndulo tiene una biblioteca **vieja**, en JavaScript, que convierte minutos en horas de reloj. Para usarla en el Mirador, escribió su `.d.ts`. La Urraca le pasó los minutos como texto, y en JavaScript eso daba una hora disparatada.

#### Gheco sugiere
Mirá `reloj.d.ts` en el tablero: `horaDe` pide un `number`. Leé el error y pasá el número sin comillas.

#### Desafío
Pasale un número a `horaDe`.

#### Pasos
1. Tocá **Ejecutar** y leé el error.
2. Cambiá `horaDe('90')` por `horaDe(90)`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Archivos
reloj.js
```javascript
export function horaDe(minutos) {
  const h = Math.floor(minutos / 60);
  const m = minutos % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
}
```

reloj.d.ts
```typescript
/** Pasa minutos desde la medianoche a una hora de reloj: 90 → "01:30". */
export function horaDe(minutos: number): string;
```

#### Código inicial
```typescript
import { horaDe } from './reloj.js';

console.log(`La guardia empieza a las ${horaDe(0)}`);
console.log(`Cambio de vigía a las ${horaDe('90')}`);
console.log(`Termina a las ${horaDe(240)}`);
```

#### Salida esperada
```
La guardia empieza a las 00:00
Cambio de vigía a las 01:30
Termina a las 04:00
```

#### Solución
```typescript
import { horaDe } from './reloj.js';

console.log(`La guardia empieza a las ${horaDe(0)}`);
console.log(`Cambio de vigía a las ${horaDe(90)}`);
console.log(`Termina a las ${horaDe(240)}`);
```

#### Al superarla
El reloj de Don Péndulo da la hora justa. —Cuarenta años usando esa biblioteca —dice el relojero— y es la primera vez que alguien me avisa antes de equivocarme.

#### Imagen
- Un reloj de bolsillo antiguo abierto, con engranajes a la vista, conectado con un cable a un tablero.
- Un ogro de cuerda chiquito con un papel con comillas dibujadas.
- Don Péndulo (relojero muy viejo, barba blanca, delantal de cuero, lupa de relojero en un ojo) sostiene el reloj; Rigel (chico flaco con pecas, antiparras de latón) lee el tablero; Gheco mira el péndulo hipnotizado.

### Micro-misión S04-N04-P4 · El formulario con la caja

```meta
lugar: La entrada del Mirador
personajes: Rigel, Gheco, Astrea, la Urraca de Cobre
carta: Trampa 4 | la página usa calibre.ts · objeto(esquema) valida el formulario entero · el aviso muestra el primer error o la ficha
recompensa: xp 15, monedas 3
```

#### Escena
La Urraca cambió el formulario de vigías por uno falso, sin validar. Rigel lo arma de nuevo, ahora con la caja del calibre: el validador de la ficha sale de la biblioteca.

#### Gheco sugiere
`objeto` viene de `calibre.ts`. Falta armar el validador de la ficha con su esquema: un nombre de texto y una edad de 10 a 99.

#### Desafío
Completá el validador de la ficha.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `const validarVigia = objeto({ nombre: texto(), edad: numeroEntre(10, 99) });`.
3. Tocá **Ejecutar** y compará con el estado esperado.

#### Página
```html
<style>
  body { font-family: Georgia, serif; background: #0b1326; color: #e8d9b0; padding: 20px; }
  input { padding: 6px; background: #1a2440; color: #f2c14e; border: 2px solid #8d6e3f; }
  #aviso { color: #f2c14e; }
</style>
<form>
  <p><label>Nombre: <input id="nombre"></label></p>
  <p><label>Edad: <input id="edad" type="number"></label></p>
  <button>Anotarme</button>
</form>
<p id="aviso"></p>
```

#### Eventos
```
escribir #nombre Bruno
escribir #edad 9
enviar form
```

#### Estado
```
#aviso
```

#### Archivos
calibre.ts
```typescript
export type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
export type Validador<T> = (x: unknown) => Result<T>;

export const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
export const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

export const texto = (): Validador<string> => (x) =>
  typeof x === 'string' && x.trim() !== '' ? ok(x.trim()) : error('tiene que ser un texto');

export const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);

type DeValidador<V> = V extends Validador<infer T> ? T : never;
type Esquema = Record<string, Validador<unknown>>;
export type Forma<S extends Esquema> = { [K in keyof S]: DeValidador<S[K]> };

export function objeto<S extends Esquema>(esquema: S): Validador<Forma<S>> {
  return (x) => {
    if (typeof x !== 'object' || x === null) return error('no es una ficha');
    const campos = x as Record<string, unknown>;
    const salida: Record<string, unknown> = {};
    for (const clave of Object.keys(esquema)) {
      const r = esquema[clave](campos[clave]);
      if (!r.ok) return error(`${clave}: ${r.error}`);
      salida[clave] = r.valor;
    }
    return ok(salida as Forma<S>);
  };
}
```

#### Código inicial
```typescript
import { numeroEntre, objeto, texto } from './calibre.js';

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const nombre = obtenerElemento<HTMLInputElement>('#nombre');
const edad = obtenerElemento<HTMLInputElement>('#edad');
const aviso = obtenerElemento<HTMLParagraphElement>('#aviso');

___

obtenerElemento<HTMLFormElement>('form').addEventListener('submit', (e: SubmitEvent) => {
  e.preventDefault();
  const r = validarVigia({ nombre: nombre.value, edad: edad.valueAsNumber });
  aviso.textContent = r.ok ? `Anotado: ${r.valor.nombre} (${r.valor.edad})` : `✗ ${r.error}`;
});
```

#### Salida esperada
```
── Estado ──
#aviso: ✗ edad: tiene que ser un número de 10 a 99
```

#### Solución
```typescript
import { numeroEntre, objeto, texto } from './calibre.js';

function obtenerElemento<T extends Element>(selector: string): T {
  const el = document.querySelector<T>(selector);
  if (!el) throw new Error(`Falta ${selector} en la página`);
  return el;
}

const nombre = obtenerElemento<HTMLInputElement>('#nombre');
const edad = obtenerElemento<HTMLInputElement>('#edad');
const aviso = obtenerElemento<HTMLParagraphElement>('#aviso');

const validarVigia = objeto({ nombre: texto(), edad: numeroEntre(10, 99) });

obtenerElemento<HTMLFormElement>('form').addEventListener('submit', (e: SubmitEvent) => {
  e.preventDefault();
  const r = validarVigia({ nombre: nombre.value, edad: edad.valueAsNumber });
  aviso.textContent = r.ok ? `Anotado: ${r.valor.nombre} (${r.valor.edad})` : `✗ ${r.error}`;
});
```

#### Al superarla
Bruno, de 9 años, se queda con las ganas: el formulario le avisa con amabilidad que todavía no puede. La Urraca, en el techo, deja caer el formulario falso.

#### Imagen
- El formulario de pergamino en su atril, con un sello de la caja del calibre en una esquina.
- Un chico chiquito de 9 años con gorro de lana, decepcionado pero sonriente.
- Astrea (lechuza con anteojos de latón y chaleco azul) le da al chico un dibujo de estrella de consuelo; Rigel (chico flaco con pecas, antiparras de latón) mira; la urraca mecánica de cobre suelta un papel desde el techo; Gheco lo atrapa.

### Micro-misión S04-N04-P5 · Jefe: la Urraca devuelve todo

```meta
lugar: El taller de Rigel, en el Mirador
personajes: Rigel, Gheco, Nima, Astrea, la Urraca de Cobre
carta: La caja completa | lista(objeto(esquema)) de calibre.ts · lo del Puerto pasa por el validador · un solo lugar para todas las herramientas
recompensa: xp 50, oro 50, monedas 1
```

#### Escena
La Urraca hace su último intento: cambia la lista de héroes que llega del Puerto, para que el Mirador muestre cualquier cosa. Rigel valida la lista entera con las herramientas de la caja: una **lista** de **fichas**, cada una con su nombre y su nivel.

#### Gheco sugiere
Junta toda la Senda. `lista` y `objeto` vienen de `calibre.ts`. Falta armar el validador: una lista de objetos con `nombre` de texto y `nivel` de 1 a 10.

#### Desafío
Completá el validador de la lista.

#### Pasos
1. Buscá el `___`.
2. Cambialo por `const validarHeroes = lista(objeto({ nombre: texto(), nivel: numeroEntre(1, 10) }));`.
3. Tocá **Ejecutar** y compará con la salida esperada.

#### Archivos
calibre.ts
```typescript
export type Result<T> = { ok: true; valor: T } | { ok: false; error: string };
export type Validador<T> = (x: unknown) => Result<T>;

export const ok = <T,>(valor: T): Result<T> => ({ ok: true, valor });
export const error = (mensaje: string): Result<never> => ({ ok: false, error: mensaje });

export const texto = (): Validador<string> => (x) =>
  typeof x === 'string' && x.trim() !== '' ? ok(x.trim()) : error('tiene que ser un texto');

export const numeroEntre = (min: number, max: number): Validador<number> => (x) =>
  typeof x === 'number' && x >= min && x <= max ? ok(x) : error(`tiene que ser un número de ${min} a ${max}`);

type DeValidador<V> = V extends Validador<infer T> ? T : never;
type Esquema = Record<string, Validador<unknown>>;
export type Forma<S extends Esquema> = { [K in keyof S]: DeValidador<S[K]> };

export function objeto<S extends Esquema>(esquema: S): Validador<Forma<S>> {
  return (x) => {
    if (typeof x !== 'object' || x === null) return error('no es una ficha');
    const campos = x as Record<string, unknown>;
    const salida: Record<string, unknown> = {};
    for (const clave of Object.keys(esquema)) {
      const r = esquema[clave](campos[clave]);
      if (!r.ok) return error(`${clave}: ${r.error}`);
      salida[clave] = r.valor;
    }
    return ok(salida as Forma<S>);
  };
}

export const lista = <T,>(v: Validador<T>): Validador<T[]> => (x) => {
  if (!Array.isArray(x)) return error('no es una lista');
  const valores: T[] = [];
  for (let i = 0; i < x.length; i++) {
    const r = v(x[i]);
    if (!r.ok) return error(`posición ${i}: ${r.error}`);
    valores.push(r.valor);
  }
  return ok(valores);
};
```

#### Código inicial
```typescript
import { lista, numeroEntre, objeto, texto } from './calibre.js';

___

const delPuerto: unknown = await (await fetch('/puerto/heroes')).json();
const buena = validarHeroes(delPuerto);
console.log(buena.ok ? `✓ ${buena.valor.map((h) => `${h.nombre} ${h.nivel}`).join(' · ')}` : `✗ ${buena.error}`);

const cambiadaPorLaUrraca: unknown = [{ nombre: 'Mia', nivel: 5 }, { nombre: 'Urraca', nivel: 99 }];
const falsa = validarHeroes(cambiadaPorLaUrraca);
console.log(falsa.ok ? '✓ pasó' : `✗ ${falsa.error}`);
```

#### Salida esperada
```
✓ Mia 5 · Kira 6 · Nilo 4 · Nima 1
✗ posición 1: nivel: tiene que ser un número de 1 a 10
```

#### Solución
```typescript
import { lista, numeroEntre, objeto, texto } from './calibre.js';

const validarHeroes = lista(objeto({ nombre: texto(), nivel: numeroEntre(1, 10) }));

const delPuerto: unknown = await (await fetch('/puerto/heroes')).json();
const buena = validarHeroes(delPuerto);
console.log(buena.ok ? `✓ ${buena.valor.map((h) => `${h.nombre} ${h.nivel}`).join(' · ')}` : `✗ ${buena.error}`);

const cambiadaPorLaUrraca: unknown = [{ nombre: 'Mia', nivel: 5 }, { nombre: 'Urraca', nivel: 99 }];
const falsa = validarHeroes(cambiadaPorLaUrraca);
console.log(falsa.ok ? '✓ pasó' : `✗ ${falsa.error}`);
```

#### Al superarla
La lista falsa no pasa: la Urraca se había anotado como heroína de nivel 99. Avergonzada, baja del techo y deja sobre la mesa todo lo que se llevó: tornillos, una lupa, dos llaves… y un botón dorado del chaleco de Rigel que él creía perdido.

Desde ese día, la Urraca vive en el taller: le encanta mirar cómo brillan las herramientas, ahora que están todas en su caja. Astrea graba en la tapa **la Caja del Calibre**, el sello de la biblioteca del Mirador.

#### Imagen
- El taller de Rigel ordenado, con una caja de herramientas de latón abierta y todas sus herramientas brillando en su lugar.
- La urraca mecánica de cobre con ojos de vidrio verde, posada mansa sobre la caja, devolviendo un botón dorado.
- Rigel (chico de 16, flaco, pecas, pelo castaño revuelto, antiparras de latón, camisa azul, chaleco marrón) recibe el botón; Nima (trenza negra alta con hilo amarillo, chaqueta corta de cuero negro con costuras amarillas) se ríe; Astrea (lechuza con anteojos de latón y chaleco azul) graba la tapa con un punzón; Gheco acaricia a la urraca.
