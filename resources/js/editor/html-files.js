// Solapas del visor de HTML y CSS: una página con un solo <style> (y, si tiene, un solo <script> sin src) se muestra como
// tres archivos —index.html, estilos.css y app.js—, como en un proyecto de verdad. Lo que se guarda, se dibuja, se
// entrega y se comprueba sigue siendo un único documento: join() lo vuelve a armar, y si no se tocó nada da
// exactamente el original (así «Restaurar» y los inspectores no notan la diferencia).

const STYLE = /([ \t]*)<style\b([^>]*)>([\s\S]*?)<\/style>/gi;
const SCRIPT = /([ \t]*)<script\b([^>]*)>([\s\S]*?)<\/script>/gi;

const KINDS = {
    css: { name: 'estilos.css', language: 'css', tag: 'style', link: (i) => `${i}<link rel="stylesheet" href="estilos.css">`, find: /[ \t]*<link\b[^>]*\bhref\s*=\s*["']estilos\.css["'][^>]*>/i, before: /<\/head>/i },
    js: { name: 'app.js', language: 'javascript', tag: 'script', link: (i) => `${i}<script src="app.js"></script>`, find: /[ \t]*<script\b[^>]*\bsrc\s*=\s*["']app\.js["'][^>]*>\s*<\/script>/i, before: /<\/body>/i },
};

/** Lo que tienen en común las líneas con texto (para mostrar el CSS sin la sangría del <style>). */
function commonIndent(text) {
    const lines = text.split('\n').filter((l) => l.trim() !== '');
    if (lines.length === 0) return '';
    return lines.map((l) => l.match(/^[ \t]*/)[0]).reduce((a, b) => {
        let i = 0;
        while (i < a.length && a[i] === b[i]) i++;
        return a.slice(0, i);
    });
}

function piece(kind, match) {
    const [whole, indent, attrs, inner] = match;
    const inside = commonIndent(inner);
    const text = inner.split('\n').map((l) => (l.startsWith(inside) ? l.slice(inside.length) : l.trimStart())).join('\n').replace(/^\s*\n/, '').replace(/\s+$/, '');
    return { kind, whole, indent, attrs, inside: inside || `${indent}  `, text };
}

/**
 * Separa la página en archivos, o null si no corresponde (sin <style> ni <script>, o con más de uno: ahí se ve entera).
 *
 * @returns {{ files: {name: string, language: string, text: string}[], join: (texts: string[]) => string } | null}
 */
export function splitHtml(code) {
    const styles = [...code.matchAll(STYLE)];
    const scripts = [...code.matchAll(SCRIPT)];
    const inline = scripts.filter((m) => !/\bsrc\s*=/i.test(m[2]));
    if (styles.length > 1 || inline.length > 1 || (styles.length === 0 && inline.length === 0)) return null;
    // Si ya enlaza un estilos.css o un app.js de verdad, no se puede usar ese nombre para la solapa.
    if (KINDS.css.find.test(code) || KINDS.js.find.test(code)) return null;

    const pieces = [];
    let page = code;
    if (styles.length) pieces.push(piece('css', styles[0]));
    if (inline.length) pieces.push(piece('js', inline[0]));
    for (const p of pieces) page = page.replace(p.whole, KINDS[p.kind].link(p.indent));

    const files = [{ name: 'index.html', language: 'html', text: page }, ...pieces.map((p) => ({ name: KINDS[p.kind].name, language: KINDS[p.kind].language, text: p.text }))];

    const join = (texts) => {
        let html = texts[0];
        pieces.forEach((p, i) => {
            const k = KINDS[p.kind];
            const text = texts[i + 1];
            const block = text === p.text
                ? p.whole
                : `${p.indent}<${k.tag}${p.attrs}>\n${text.split('\n').map((l) => (l.trim() === '' ? '' : p.inside + l)).join('\n')}\n${p.indent}</${k.tag}>`;
            // Donde está el <link> (o el <script src>); si lo borró, igual se suma antes de </head> o </body>.
            if (k.find.test(html)) html = html.replace(k.find, () => block);
            else if (k.before.test(html)) html = html.replace(k.before, (end) => `${block}\n${end}`);
            else html += `\n${block}`;
        });
        return html;
    };

    return { files, join };
}
