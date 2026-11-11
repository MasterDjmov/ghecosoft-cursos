// Los errores de C# con su criatura y una explicación corta. Los mensajes de error se muestran tal cual los da el compilador.
const COMPILER = {
    CS1002: ['Slime', 'te falta el `;` al final de la orden.'],
    CS1003: ['Slime', 'falta un signo que el compilador esperaba.'],
    CS1010: ['Slime', 'hay un texto sin cerrar: faltan las comillas de cierre.'],
    CS1026: ['Slime', 'hay un paréntesis sin cerrar.'],
    CS1513: ['Slime', 'hay una llave `{` sin cerrar.'],
    CS1022: ['Slime', 'sobra una llave `}`.'],
    CS0029: ['Goblin', 'el tipo no encaja: ese valor no se puede guardar en esa variable.'],
    CS0266: ['Goblin', 'esa conversión puede perder datos: si la querés, pedila con un cast, como `(int)`.'],
    CS0019: ['Goblin', 'ese operador no se puede usar con esos tipos.'],
    CS0664: ['Goblin', 'un número con decimales es `double`: para `decimal` lleva `m` (`9.5m`), y para `float`, `f`.'],
    CS1503: ['Goblin', 'le estás pasando un valor de otro tipo.'],
    CS0103: ['Esqueleto', 'ese nombre no existe: revisá cómo lo escribiste, mayúsculas incluidas.'],
    CS0117: ['Esqueleto', 'eso no existe en esa clase: revisá el nombre.'],
    CS1061: ['Esqueleto', 'ese tipo no tiene ese método o propiedad: revisá el nombre.'],
    CS0165: ['Esqueleto', 'usás una variable antes de darle un valor.'],
    CS0128: ['Esqueleto', 'ya hay una variable con ese nombre.'],
    CS0131: ['Goblin', 'a la izquierda del `=` tiene que ir una variable.'],
    CS0200: ['Troll', 'esa propiedad es de solo lectura.'],
    CS0841: ['Esqueleto', 'usás la variable antes de declararla.'],
};

const CURSES = {
    FormatException: ['Goblin', 'ese texto no se puede convertir al tipo que pediste. Con `TryParse` no se rompe.'],
    InvalidCastException: ['Goblin', 'esa conversión no se puede hacer.'],
    OverflowException: ['Goblin', 'el número no entra en ese tipo.'],
    DivideByZeroException: ['Ogro', 'dividiste un entero por cero.'],
    IndexOutOfRangeException: ['Orco', 'pediste una posición que no existe en el arreglo.'],
    ArgumentOutOfRangeException: ['Orco', 'te fuiste de los límites: esa posición no existe.'],
    KeyNotFoundException: ['Orco', 'esa clave no está en el diccionario.'],
    NullReferenceException: ['Troll', 'usaste algo que vale `null`: no hay nada ahí.'],
    FileNotFoundException: ['Esqueleto', 'ese archivo no existe (acá la carpeta arranca vacía).'],
    SqliteException: ['Esqueleto', 'la Bóveda no entendió el SQL: mirá el mensaje (una tabla o columna que no existe, una restricción que no se cumple…). Acá la base arranca vacía en cada ejecución.'],
    InvalidOperationException: ['Ogro', 'eso no se puede hacer en este momento (por ejemplo, usar la conexión antes de `Open()`, o pedirle algo a una colección vacía).'],
    TaskCanceledException: ['Ogro', 'la tarea se canceló antes de terminar.'],
    OperationCanceledException: ['Ogro', 'la tarea se canceló antes de terminar.'],
    HttpRequestException: ['Esqueleto', 'el pedido no llegó a ningún lado: en el navegador no hay red. Hablale a la ventanilla con `app.CreateClient()`.'],
};

export function explainCsharpErrors(errors = []) {
    const seen = new Set();
    const hints = [];
    for (const line of errors) {
        const code = line.match(/\b(CS\d{4})\b/)?.[1];
        if (code && COMPILER[code] && !seen.has(code)) {
            seen.add(code);
            hints.push(`${COMPILER[code][0]}: ${COMPILER[code][1]}`);
        }
    }

    return `El programa no llegó a arrancar: no pasó el ensayo general.\n\n${errors.join('\n')}${hints.length ? `\n\n${hints.join('\n')}` : ''}`;
}

export function explainCurse(scroll) {
    const name = scroll.match(/^(?:[\w.]+\.)?(\w+Exception)/)?.[1];
    const hint = name && CURSES[name] ? `\n\n${CURSES[name][0]}: ${CURSES[name][1]}` : '';

    return `Maldición: el programa arrancó y se rompió en el medio.\n\n${scroll}${hint}`;
}
