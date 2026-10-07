// Ejecuta Java en la compu de quien lo usa: scripts/JavaRunner.java (abierto en una terminal) compila con javac
// y corre con java. El docente lo usa al corregir (D69); el alumno, para probar su propio código (D85), con el
// paquete que baja de Herramientas → Ejecutor de Java. No hay un compilador libre y completo de Java para el
// navegador (D67). El código del alumno nunca se ejecuta en el servidor.

export const START_COMMAND = 'java scripts/JavaRunner.java';

// Sin respuesta puede ser que el ejecutor no esté abierto o que el navegador no deje a la página hablarle a la
// compu (Chrome y Firefox piden permiso de «red local» para 127.0.0.1 desde un sitio de internet).
const notRunning = (helpUrl) => helpUrl ? notRunningStudent(helpUrl) :
    'No me pude comunicar con el ejecutor de Java de tu compu.\n\n'
    + '1. Si el navegador preguntó si este sitio puede acceder a otros dispositivos o apps de tu red local, tocá Permitir. '
    + 'Si lo rechazaste: candado (o ícono) a la izquierda de la dirección → Configuración del sitio → «Acceso a la red local» → Permitir, y recargá.\n'
    + '2. Si no está abierto, abrí una terminal en la carpeta del proyecto y corré:\n'
    + `  ${START_COMMAND}\n`
    + `   (si la página es otra, agregale --origin ${window.location.origin}).\n`
    + '3. Mientras tanto, «Probar en la terminal» (debajo) arma un comando para correrlo a mano.';

// Para el alumno: abrir el ejecutor (o instalarlo) y dar permiso de red local.
const notRunningStudent = (helpUrl) =>
    'Java se ejecuta en tu compu, con el Ejecutor de Java abierto, y no me pude comunicar con él.\n\n'
    + '1. ¿Lo tenés abierto? Hacé doble clic en «Iniciar-ejecutor» (en la carpeta donde lo descomprimiste) y dejá esa ventana abierta.\n'
    + '2. Si el navegador preguntó si este sitio puede acceder a tu red local, tocá Permitir. '
    + 'Si lo rechazaste: candado a la izquierda de la dirección → Configuración del sitio → «Acceso a la red local» → Permitir, y recargá.\n'
    + `3. ¿Todavía no lo instalaste? Seguí los pasos de ${new URL(helpUrl, window.location.href).href}\n\n`
    + 'Sin el ejecutor podés seguir escribiendo y entregar tu práctica: el profe la ejecuta al corregir.';

/**
 * @returns {Promise<{output: string, error: string|null, diagnostics: string, stderr?: string, ms: number, timedOut?: boolean}>}
 */
export async function runJava(code, { stdin = '', url, helpUrl = null, timeout = 5000, onStatus } = {}) {
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
        return { output: '', error: notRunning(helpUrl), diagnostics: '', ms: 0, unavailable: true };
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
