// El inspector de HTML y CSS (D102): las micro-misiones de HTML se comprueban leyendo el código del alumno SIN
// ejecutarlo. DOMParser arma un documento inerte (no corre scripts ni carga imágenes) y un lector de CSS propio
// lee las reglas de los <style>, igual en todos los navegadores. El informe es texto y se compara con el esperado
// como una salida (NodeStep::accepts). La vista previa sigue en su caja sin permisos (D76): acá no se dibuja nada.
//
// Cada renglón de los pedidos da uno o más renglones del informe («pedido: valor»):
//   !doctype                              → el doctype («html») o (no hay)
//   h1                                    → el texto de cada h1 (espacios juntos), (vacío) o (no hay)
//   nav a #                               → cuántos hay
//   img @alt                              → el atributo de cada uno, (vacío) si está sin valor, (no tiene) si falta
//   css .tarjeta { padding }              → el valor de la última regla con ese selector, o (no hay)
//   css @media (min-width: 768px) | .grilla { display }   → lo mismo, adentro de ese @media
// Los renglones vacíos y los que empiezan con // no piden nada.

const MAX_MATCHES = 20;

const squish = (text) => String(text ?? '').replace(/\s+/g, ' ').trim();

/** Un selector escrito de muchas formas, de una sola: espacios juntos y uno solo alrededor de > + ~ y de las comas. */
function normalizeSelector(selector) {
    return squish(selector).replace(/\s*([>+~])\s*/g, ' $1 ').replace(/\s*,\s*/g, ', ');
}

/** «( min-width:768PX )» → «(min-width: 768px)». */
function normalizeMedia(media) {
    return squish(media).toLowerCase().replace(/\(\s*/g, '(').replace(/\s*\)/g, ')').replace(/\s*:\s*/g, ': ');
}

/** El valor de una propiedad: espacios juntos, «, » en las listas y minúsculas fuera de las comillas. */
function normalizeValue(value) {
    return squish(value)
        .replace(/\s*,\s*/g, ', ')
        .replace(/\(\s+/g, '(')
        .replace(/\s+\)/g, ')')
        .split(/("[^"]*"|'[^']*')/)
        .map((part, i) => (i % 2 ? part : part.toLowerCase()))
        .join('');
}

/** Dónde cierra la llave que abre en `open` (o el final, si no cierra). */
function closingBrace(css, open) {
    let depth = 0;
    for (let i = open; i < css.length; i++) {
        if (css[i] === '{') depth++;
        else if (css[i] === '}' && --depth === 0) return i;
    }

    return css.length;
}

/** Las reglas del CSS, en orden: [{ media, selectors: [...], declarations: [[prop, value], ...] }]. */
export function parseCss(css, media = '') {
    const text = String(css ?? '').replace(/\/\*[\s\S]*?\*\//g, '');
    const rules = [];
    let at = 0;
    while (at < text.length) {
        const open = text.indexOf('{', at);
        if (open === -1) break;
        let prelude = text.slice(at, open);
        // Lo que termina en ; antes de la llave (@import "…";) no es una regla.
        const statement = prelude.lastIndexOf(';');
        if (statement !== -1) prelude = prelude.slice(statement + 1);
        prelude = squish(prelude);
        const close = closingBrace(text, open);
        const body = text.slice(open + 1, close);
        at = close + 1;

        if (/^@media\b/i.test(prelude)) {
            rules.push(...parseCss(body, normalizeMedia(prelude.slice(6))));
        } else if (/^@(layer|supports)\b/i.test(prelude)) {
            rules.push(...parseCss(body, media));
        } else if (prelude) {
            const declarations = body.split(';').map((d) => d.split(':')).filter((p) => p.length > 1)
                .map(([prop, ...rest]) => [squish(prop).toLowerCase(), normalizeValue(rest.join(':'))]);
            rules.push({ media, selectors: prelude.split(',').map(normalizeSelector), declarations });
        }
    }

    return rules;
}

function cssValue(rules, request) {
    const match = request.match(/^(?:@media\s+(.+?)\s*\|\s*)?(.+?)\s*\{\s*([^}]+?)\s*\}$/i);
    if (!match) return '(pedido mal escrito)';
    const media = match[1] ? normalizeMedia(match[1]) : '';
    const selector = normalizeSelector(match[2]);
    const prop = squish(match[3]).toLowerCase();
    let value = '(no hay)';
    for (const rule of rules) {
        if (rule.media !== media || !rule.selectors.includes(selector)) continue;
        for (const [name, v] of rule.declarations) if (name === prop) value = v;
    }

    return value;
}

function query(doc, selector) {
    try {
        return Array.from(doc.querySelectorAll(selector)).slice(0, MAX_MATCHES);
    } catch {
        return null;
    }
}

/** El informe del inspector para ese código y esos pedidos (texto, un renglón por resultado). */
export function inspect(code, checks) {
    const doc = new DOMParser().parseFromString(String(code ?? ''), 'text/html');
    const css = Array.from(doc.querySelectorAll('style')).map((s) => s.textContent).join('\n');
    const rules = parseCss(css);
    const lines = [];

    for (const raw of String(checks ?? '').split('\n')) {
        const request = squish(raw);
        if (!request || request.startsWith('//')) continue;

        if (request === '!doctype') {
            lines.push(`${request}: ${doc.doctype ? doc.doctype.name.toLowerCase() : '(no hay)'}`);
            continue;
        }
        if (/^css\s/i.test(request)) {
            lines.push(`${request}: ${cssValue(rules, request.slice(4).trim())}`);
            continue;
        }

        const count = request.match(/^(.+?)\s+#$/);
        const attribute = request.match(/^(.+?)\s+@([\w:-]+)$/);
        const selector = count ? count[1] : attribute ? attribute[1] : request;
        const found = query(doc, selector);
        if (found === null) {
            lines.push(`${request}: (selector mal escrito)`);
        } else if (count) {
            lines.push(`${request}: ${found.length}`);
        } else if (!found.length) {
            lines.push(`${request}: (no hay)`);
        } else {
            for (const el of found) {
                const value = attribute
                    ? el.hasAttribute(attribute[2]) ? squish(el.getAttribute(attribute[2])) || '(vacío)' : '(no tiene)'
                    : squish(el.textContent) || '(vacío)';
                lines.push(`${request}: ${value}`);
            }
        }
    }

    return lines.join('\n');
}
