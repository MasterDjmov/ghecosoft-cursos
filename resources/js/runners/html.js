// HTML y CSS (D76): la página del alumno se dibuja en un <iframe sandbox=""> (sin JavaScript, sin formularios,
// sin ventanas nuevas y con un origen propio: no ve nada de la plataforma) y con una CSP que no la deja salir a
// internet, salvo las imágenes de la plataforma y las fuentes de Google. Nada corre en el servidor.
//
// Tailwind: si la página trae <style type="text/tailwindcss"> (como el Tailwind oficial del navegador), se
// compila acá afuera y a la caja llega solo el CSS resultante.

/** La política de la caja: se agrega primero, y una CSP que escriba el alumno solo puede restringir más. */
function policy() {
    const origin = window.location.origin;

    return [
        "default-src 'none'",
        `img-src ${origin} data: blob:`,
        "style-src 'unsafe-inline' https://fonts.googleapis.com",
        'font-src https://fonts.gstatic.com data:',
        "form-action 'none'",
        "base-uri 'none'",
    ].join('; ');
}

/** Agrega la CSP lo antes posible sin romper el DOCTYPE (si quedara antes, la página se dibujaría en modo quirks). */
function withPolicy(html) {
    const meta = `<meta http-equiv="Content-Security-Policy" content="${policy()}">`;
    const head = html.match(/<head(\s[^>]*)?>/i);
    if (head) {
        const at = head.index + head[0].length;
        return html.slice(0, at) + meta + html.slice(at);
    }
    const start = html.match(/^\s*(<!doctype[^>]*>)?\s*(<html(\s[^>]*)?>)?/i);
    const at = start ? start[0].length : 0;

    return html.slice(0, at) + meta + html.slice(at);
}

const TAILWIND_BLOCK = /<style\b[^>]*type\s*=\s*["']text\/tailwindcss["'][^>]*>([\s\S]*?)<\/style>/gi;

/** Las clases que aparecen en la página (class="…"): con eso Tailwind sabe qué utilidades generar. */
function candidates(html) {
    const found = new Set();
    for (const match of html.matchAll(/\bclass\s*=\s*(["'])([\s\S]*?)\1/gi)) {
        for (const token of match[2].split(/\s+/)) {
            if (token) found.add(token);
        }
    }

    return [...found];
}

/**
 * Arma el documento para la caja.
 *
 * @returns {Promise<{html: string, error: string|null, ms: number}>}
 */
export async function buildPreview(code) {
    const started = performance.now();
    let html = String(code ?? '');
    let error = null;

    const blocks = [...html.matchAll(TAILWIND_BLOCK)];
    if (blocks.length > 0) {
        try {
            const { compileTailwind } = await import('./tailwind.js');
            const css = await compileTailwind(blocks.map((b) => b[1]).join('\n'), candidates(html));
            let first = true;
            html = html.replace(TAILWIND_BLOCK, () => {
                const replacement = first ? `<style>${css.replace(/<\/style/gi, '<\\/style')}</style>` : '';
                first = false;
                return replacement;
            });
        } catch (e) {
            // Un error en el CSS de Tailwind (una directiva mal escrita): se muestra la página sin ese CSS.
            error = 'Tailwind: ' + (e?.message ?? String(e));
            html = html.replace(TAILWIND_BLOCK, '');
        }
    }

    return { html: withPolicy(html), error, ms: Math.round(performance.now() - started) };
}
