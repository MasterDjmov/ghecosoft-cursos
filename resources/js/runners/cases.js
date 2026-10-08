// Corrección asistida (D73): corre la entrega de un alumno con cada caso (el ejemplo y las pruebas de la
// práctica) en el navegador del docente —o, en Java, en su compu (D69)— y compara la salida. Es una ayuda
// para corregir: la decisión sigue siendo del docente. El código del alumno nunca se ejecuta en el servidor.

/** Igual que en el servidor (LocalCodeRunner): sin espacios al final de cada línea ni líneas vacías en las puntas. */
export function normalize(text) {
    return String(text ?? '').replace(/\r\n/g, '\n').replace(/[ \t]+$/gm, '').replace(/^\n+|\n+$/g, '');
}

/**
 * Un caso pasa si la salida coincide y el programa no se cortó. Un código de salida distinto de 0 (exit(1)
 * o sys.exit(1) que pide la consigna) no lo hace fallar.
 */
function passes(result, expected) {
    if (result.compileError || result.timedOut || result.unavailable || result.crashed) return false;
    const deliberateExit = !result.error || /terminó con código|^SystemExit/.test(result.error);

    return deliberateExit && normalize(result.output) === normalize(expected);
}

async function runOne(language, code, stdin, options) {
    if (language === 'java') {
        const { runJava } = await import('./java.js');
        return runJava(code, { stdin, url: options.javaRunnerUrl, timeout: options.timeout });
    }
    if (language === 'sql') {
        const { runSql } = await import('./sql.js');
        return runSql(code, { timeout: options.timeout });
    }
    if (language === 'php') {
        const { runPhp } = await import('./php.js');
        return runPhp(code, { stdin, timeout: options.timeout });
    }
    const { runPython } = await import('./python.js');
    const result = await runPython(code, { stdin, url: options.pyodideUrl, timeout: options.timeout });

    return result.loadFailed ? { ...result, unavailable: true } : result;
}

/**
 * @param {{language: string, code: string, cases: Array<{label: string, input: string, expected: string}>,
 *          pyodideUrl?: string, javaRunnerUrl?: string, timeout?: number, onStatus?: (s: string) => void}} options
 * @returns {Promise<{results: Array<object>, passed: number, total: number, unavailable: string|null}>}
 */
export async function runCases({ language, code, cases, onStatus, ...options }) {
    let raw;
    if (language === 'c' || language === 'cpp') {
        const { runCppMany } = await import('./cpp.js');
        raw = await runCppMany(code, cases.map((c) => c.input), { language, timeout: options.timeout, onStatus });
    } else {
        raw = [];
        for (const [i, item] of cases.entries()) {
            onStatus?.(`Probando ${i + 1} de ${cases.length}…`);
            const result = await runOne(language, code, item.input, options);
            raw.push(result);
            // Si el ejecutor no está (Java sin JavaRunner, Python o PHP que no cargan), no tiene sentido seguir.
            if (result.unavailable) break;
        }
    }

    const unavailable = raw.find((r) => r.unavailable)?.error ?? null;
    const results = cases.map((item, i) => {
        const result = raw[i] ?? { output: '', error: null };
        return { ...item, output: result.output ?? '', error: result.error, compileError: Boolean(result.compileError), timedOut: Boolean(result.timedOut), passed: passes(result, item.expected) };
    });

    return { results, passed: results.filter((r) => r.passed).length, total: results.length, unavailable };
}

/**
 * Para mostrar la diferencia: cada línea de lo esperado y de lo obtenido, marcando las que no coinciden.
 *
 * @returns {Array<{expected: string|null, got: string|null, same: boolean}>}
 */
export function diffLines(expected, got) {
    const want = normalize(expected).split('\n');
    const have = normalize(got).split('\n');
    const lines = [];
    for (let i = 0; i < Math.max(want.length, have.length); i++) {
        const a = want[i] ?? null;
        const b = have[i] ?? null;
        lines.push({ expected: a, got: b, same: a !== null && b !== null && a.replace(/[ \t]+$/, '') === b.replace(/[ \t]+$/, '') });
    }

    return lines;
}
