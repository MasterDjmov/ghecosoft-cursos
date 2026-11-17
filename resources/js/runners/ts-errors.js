// Los errores de tipos de TypeScript en criollo (D115, fase 5). El mensaje del compilador (en español, el oficial de
// TypeScript) va tal cual, y debajo la criatura y qué quiere decir. Las criaturas son las del bestiario del Mirador
// (historias/typescript.md § 8). El programa NO se ejecuta si hay errores de tipos: en el Mirador, la pieza que no
// encaja traba el mecanismo antes de girar.

const EXPLAIN = {
    // Slime: la escritura.
    TS1002: ['Slime', 'hay un texto sin cerrar: faltan las comillas del final.'],
    TS1003: ['Slime', 'el compilador esperaba un nombre ahí.'],
    TS1005: ['Slime', 'falta un signo que el compilador esperaba (mirá el mensaje: dice cuál).'],
    TS1109: ['Slime', 'el compilador esperaba un valor ahí y no hay nada.'],
    TS1128: ['Slime', 'sobra algo: casi siempre una llave `}` de más.'],
    TS1136: ['Slime', 'en un objeto, cada propiedad va con `nombre: valor`.'],
    TS1160: ['Slime', 'hay un texto con `` ` `` sin cerrar.'],
    // Goblin: el tipo no encaja.
    TS2322: ['Goblin', 'el valor no encaja con el tipo de la variable (o de la propiedad).'],
    TS2345: ['Goblin', 'le pasaste a la función un valor de otro tipo que el que pide.'],
    TS2362: ['Goblin', 'la cuenta necesita números a la izquierda del signo.'],
    TS2363: ['Goblin', 'la cuenta necesita números a la derecha del signo.'],
    TS2365: ['Goblin', 'ese signo no se puede usar con esos tipos.'],
    TS2367: ['Goblin', 'esa comparación nunca puede dar verdadero: los tipos no tienen nada en común.'],
    TS2352: ['Goblin', 'ese `as` convierte a un tipo que no tiene nada que ver: probablemente es un error.'],
    TS2678: ['Goblin', 'ese `case` no es ninguna de las opciones de la unión: ¿está bien escrito?'],
    TS2769: ['Goblin', 'ninguna de las formas de llamar a esa función acepta esos valores.'],
    TS18046: ['Goblin', 'esa variable es `unknown`: antes de usarla, preguntá qué es (con `typeof`, `instanceof` o `in`).'],
    // Esqueleto: lo que no existe.
    TS2304: ['Esqueleto', 'ese nombre no existe: revisá cómo lo escribiste, mayúsculas incluidas.'],
    TS2339: ['Esqueleto', 'ese tipo no tiene esa propiedad (o ese método): revisá el nombre o el tipo.'],
    TS2551: ['Esqueleto', 'esa propiedad no existe: el mensaje te sugiere el nombre parecido.'],
    TS2552: ['Esqueleto', 'ese nombre no existe: el mensaje te sugiere el parecido.'],
    TS2554: ['Esqueleto', 'la función pide otra cantidad de valores que los que le pasaste.'],
    TS2555: ['Esqueleto', 'a la función le faltan valores.'],
    TS2307: ['Esqueleto', 'no hay ningún archivo con ese nombre para importar (se importa con `./nombre.js`).'],
    TS2882: ['Esqueleto', 'ese archivo no tiene tipos: hace falta su `.d.ts` (aunque sea uno que solo diga que existe).'],
    TS2664: ['Esqueleto', 'un `declare module` con una ruta relativa no se puede usar en un módulo: escribí la declaración en un archivo `.d.ts`.'],
    TS2724: ['Esqueleto', 'ese archivo no exporta ese nombre; el mensaje te sugiere el parecido.'],
    TS2305: ['Esqueleto', 'ese archivo no exporta ese nombre: revisá el nombre o agregale `export`.'],
    TS2741: ['Esqueleto', 'al objeto le falta una propiedad que el tipo pide.'],
    TS2739: ['Esqueleto', 'al objeto le faltan propiedades que el tipo pide.'],
    TS2353: ['Esqueleto', 'el objeto tiene una propiedad que el tipo no conoce: ¿está bien escrita?'],
    TS2454: ['Esqueleto', 'usás la variable antes de darle un valor.'],
    TS2448: ['Esqueleto', 'usás la variable antes del renglón donde la declarás.'],
    TS2564: ['Esqueleto', 'la propiedad no tiene valor: dáselo al declararla o en el constructor.'],
    TS2420: ['Esqueleto', 'la clase dice que cumple una interfaz, pero le falta algo de ella.'],
    TS2515: ['Esqueleto', 'la clase hereda de una abstracta y le falta escribir uno de sus métodos.'],
    TS2344: ['Esqueleto', 'ese tipo no cumple lo que pide el genérico (por ejemplo, un nombre de propiedad que no existe en un Pick u Omit).'],
    TS2576: ['Esqueleto', 'eso es `static`: es del molde, no de cada objeto. Se usa con el nombre de la clase (`Clase.nombre`).'],
    TS2416: ['Goblin', 'el método de la clase de abajo no encaja con el de la clase de arriba (otros tipos en los parámetros o en lo que devuelve).'],
    // Orco: los límites (lo que capaz que no está).
    TS2531: ['Orco', 'ese valor puede ser `null`: preguntá antes si está (`if (x)`) o usá `?.`.'],
    TS2532: ['Orco', 'ese valor puede ser `undefined`: preguntá antes si está o usá `?.` y `??`.'],
    TS18047: ['Orco', 'ese valor puede ser `null`: preguntá antes si está (`if (x)`) o usá `?.`.'],
    TS18048: ['Orco', 'ese valor puede ser `undefined`: preguntá antes si está o usá `?.` y `??`.'],
    TS2493: ['Orco', 'la tupla no tiene esa posición: es de largo fijo.'],
    TS7053: ['Orco', 'no se puede usar ese valor como clave de ese objeto: el tipo no lo permite.'],
    // Ogro: la lógica y las reglas.
    TS2588: ['Ogro', 'es una `const`: no se puede cambiar. Si tiene que cambiar, declarala con `let`.'],
    TS2540: ['Ogro', 'esa propiedad es `readonly`: no se puede cambiar.'],
    TS2341: ['Ogro', 'esa propiedad es `private`: solo se usa adentro de su clase.'],
    TS2445: ['Ogro', 'esa propiedad es `protected`: solo se usa en su clase y en las que heredan.'],
    TS18013: ['Ogro', 'ese campo `#privado` solo se usa adentro de su clase.'],
    TS2511: ['Ogro', 'una clase `abstract` no se puede crear con `new`: se crea una de las que heredan.'],
    TS2366: ['Ogro', 'la función promete devolver un valor, pero hay un camino que no devuelve nada.'],
    TS2355: ['Ogro', 'la función dice qué tipo devuelve, pero no tiene `return`.'],
    TS7006: ['Ogro', 'el parámetro no tiene tipo: en el Mirador toda pieza lleva su medida (`nombre: string`).'],
    TS7005: ['Ogro', 'la variable quedó con tipo `any`: decile qué tipo tiene.'],
    TS4114: ['Ogro', 'ese método reemplaza al de la clase de arriba: escribí `override` adelante.'],
    TS2375: ['Orco', 'con `exactOptionalPropertyTypes`, una propiedad opcional se omite: no se le pone `undefined`.'],
    TS7030: ['Ogro', 'hay un camino de la función que no devuelve nada (`noImplicitReturns`): agregá el `return` que falta.'],
    TS6133: ['Ogro', 'eso se declaró y no se usa nunca (`noUnusedLocals`): borralo, o usalo.'],
    TS6196: ['Ogro', 'ese tipo se declaró y no se usa nunca: borralo, o usalo.'],
    // Troll: el tiempo.
    TS1308: ['Troll', '`await` solo se usa adentro de una función `async`.'],
    TS2801: ['Troll', 'eso es una promesa: le falta el `await` para tener el valor.'],
};

/** La criatura de un error de tipos (para la tarjeta del error), o null. */
export function typeCreature(code) {
    return EXPLAIN[code]?.[0]?.toLowerCase() ?? null;
}

/**
 * El texto que se muestra cuando no compila: cada error con su línea, el mensaje del compilador y la explicación.
 *
 * @param {Array<{code: string, line: number|null, file: string|null, message: string}>} diagnostics
 */
export function explainTypeErrors(diagnostics) {
    const shown = diagnostics.slice(0, 6);
    const header = diagnostics.length === 1
        ? '✗ El Mirador no arrancó: una pieza no encaja (el programa no se ejecutó).'
        : `✗ El Mirador no arrancó: ${diagnostics.length} piezas no encajan (el programa no se ejecutó).`;
    const parts = shown.map((d) => {
        const where = d.line ? `Línea ${d.line}${d.file && d.file !== 'main.ts' ? ` de ${d.file}` : ''}` : 'En la configuración';
        const [creature, text] = EXPLAIN[d.code] ?? [null, null];
        return `${where}: ${d.message}\n  ${creature ? `${creature}: ${text} ` : ''}(${d.code})`;
    });
    if (diagnostics.length > shown.length) parts.push(`… y ${diagnostics.length - shown.length} más. Arreglá los de arriba primero: muchas veces los otros desaparecen solos.`);

    return [header, ...parts].join('\n\n');
}

/** Para las micro-misiones de tipo Compilador: los errores en renglones cortos, como la «Salida esperada». */
export function summarizeTypeErrors(diagnostics) {
    if (!diagnostics.length) return 'Compila sin errores';

    return diagnostics.map((d) => `${d.code} en la línea ${d.line ?? '?'}${d.file && d.file !== 'main.ts' ? ` de ${d.file}` : ''}`).join('\n');
}
