// Ejecuta Java en la compu del docente (D69): scripts/JavaRunner.java (abierto en una terminal) compila con
// javac y corre con java. No hay un compilador libre y completo de Java para el navegador (D67). Solo para
// corregir: el código del alumno nunca se ejecuta en el servidor.

export const START_COMMAND = 'java scripts/JavaRunner.java';

const notRunning = () =>
    'No encuentro el ejecutor de Java en tu compu. Abrí una terminal en la carpeta del proyecto y corré:\n'
    + `  ${START_COMMAND}\n`
    + `(Si ya está abierto y esta página es otra, agregale --origin ${window.location.origin}.)`;

/**
 * @returns {Promise<{output: string, error: string|null, diagnostics: string, stderr?: string, ms: number, timedOut?: boolean}>}
 */
export async function runJava(code, { stdin = '', url, timeout = 5000, onStatus } = {}) {
    onStatus?.('Compilando en tu compu…');
    let data;
    try {
        const response = await fetch(`${url}/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, stdin }),
            signal: AbortSignal.timeout(timeout + 30000),
        });
        data = await response.json();
    } catch (e) {
        return { output: '', error: notRunning(), diagnostics: '', ms: 0 };
    }

    if (!data.compiled) {
        return { output: '', error: 'No compila.', diagnostics: data.diagnostics, ms: 0, compileError: true };
    }
    const cut = data.truncated ? '\n(La salida era muy larga: se muestra el principio.)' : '';
    if (data.timedOut) {
        return { output: data.output, error: `Se cortó a los ${timeout / 1000} segundos. ¿Hay un bucle que no termina?${cut}`, diagnostics: data.diagnostics, ms: data.ms, timedOut: true };
    }
    const errors = data.errors.trim();
    const error = data.exit !== 0 ? `El programa terminó con código ${data.exit}.${errors ? '\n' + errors : ''}${cut}` : (cut || null);

    return { output: data.output, error, diagnostics: data.diagnostics, stderr: data.exit === 0 ? errors : '', ms: data.ms };
}
