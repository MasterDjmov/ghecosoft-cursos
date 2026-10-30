// Los errores de JavaScript en criollo (D115): el mensaje del navegador se deja entre paréntesis, para que el alumno
// aprenda a leerlo, y arriba va qué quiere decir. Las criaturas son las del bestiario de la Feria
// (historias/javascript.md § 8).

const RUNTIME = [
    [/^(.+) is not defined$/, 'esqueleto', '«$1» no existe: ¿está bien escrito (las mayúsculas cuentan)? ¿Lo declaraste con let o const?'],
    [/^Cannot access '(.+)' before initialization$/, 'esqueleto', 'Usaste «$1» antes del renglón donde lo declarás.'],
    [/^Assignment to constant variable\.$/, 'ogro', 'Quisiste cambiar una const: si el valor tiene que cambiar, declarala con let.'],
    [/^Cannot read properties of (undefined|null) \(reading '(.+)'\)$/, 'troll', 'Quisiste leer «.$2» de algo que es $1 (todavía no tiene valor, o no existe).'],
    [/^Cannot set properties of (undefined|null) \(setting '(.+)'\)$/, 'troll', 'Quisiste cambiar «.$2» de algo que es $1.'],
    [/^(.+) is not a function$/, 'esqueleto', '«$1» no es una función: no se puede llamar con ( ).'],
    [/^(.+) is not a constructor$/, 'esqueleto', '«$1» no es una clase: no se puede usar con new.'],
    [/^(.+) is not iterable/, 'orco', '«$1» no se puede recorrer con for…of ni desarmar con [ ] (no es un arreglo).'],
    [/^Class constructor (.+) cannot be invoked without 'new'$/, 'goblin', 'La clase «$1» se usa con new: new $1(…).'],
    [/^Maximum call stack size exceeded$/, 'troll', 'Una función se llama a sí misma sin fin (le falta el caso que corta).'],
    [/^Invalid array length$/, 'orco', 'El largo de un arreglo tiene que ser un número entero y positivo.'],
    [/^Unexpected token .* in JSON|is not valid JSON|^Unexpected end of JSON input/, 'slime', 'Ese texto no es un JSON válido (¿llegó cortado, o es texto común?).'],
    [/^Failed to fetch$/, 'troll', 'El pedido no salió: la caja no tiene internet. Pedile al Puerto: fetch(\'/puerto/…\').'],
    [/^Failed to execute 'querySelector'|is not a valid selector/, 'slime', 'El selector está mal escrito (¿falta el # de un id o el . de una clase?).'],
    [/^Cannot convert undefined or null to object$/, 'troll', 'Le pasaste undefined o null a algo que necesita un objeto.'],
    [/^Do not know how to serialize a BigInt$/, 'goblin', 'JSON no sabe guardar un BigInt: pasalo a texto antes.'],
    [/^Converting circular structure to JSON/, 'troll', 'El objeto se contiene a sí mismo: JSON no lo puede escribir.'],
    [/^Failed to resolve module specifier "?'?([^"']+)/, 'esqueleto', 'No hay ningún archivo «$1» en la caja: revisá el nombre (y que empiece con ./).'],
    [/does not provide an export named '?(.+?)'?$/, 'esqueleto', 'Ese archivo no exporta «$1»: revisá el nombre o agregale export.'],
    [/^Private field '(.+)' must be declared in an enclosing class$/, 'esqueleto', 'El campo privado «$1» se declara adentro de la clase antes de usarlo.'],
    [/^Cannot read private member/, 'esqueleto', 'Ese objeto no tiene ese campo privado (es de otra clase).'],
];

/**
 * @param {{name: string, message: string, line: number|null, thrown?: boolean, promise?: boolean}} error
 * @returns {string} lo que se muestra debajo de la salida
 */
export function explainError(error) {
    if (!error) return '';
    const where = error.line ? ` en la línea ${error.line}${error.file ? ` de ${error.file}` : ''}` : '';
    const original = error.thrown ? `throw ${error.message}` : `${error.name}: ${error.message}`;
    const intro = error.promise ? `Una promesa falló y nadie la atajó con catch${where}` : `Error${where}`;
    for (const [pattern, , text] of RUNTIME) {
        const found = String(error.message).match(pattern);
        if (found) return `✗ ${intro}: ${text.replace(/\$(\d)/g, (all, n) => found[Number(n)])}\n  (${original})`;
    }

    return `✗ ${intro}.\n  (${original})`;
}

/** La criatura del bestiario que trae ese error (para la tarjeta del error), o null. */
export function creatureFor(error) {
    if (!error) return null;
    if (error.name === 'SyntaxError') return 'slime';
    for (const [pattern, creature] of RUNTIME) if (pattern.test(String(error.message))) return creature;
    return error.name === 'TypeError' ? 'goblin' : null;
}
