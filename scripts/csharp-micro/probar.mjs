// Corre en Chrome, con el ejecutor del navegador, cada solución del curso de C# y la compara con su salida esperada;
// también el ejemplo de cada nodo, y revisa que el código inicial no dé ya la salida. Antes de reimportar:
//   node scripts/csharp-micro/probar.mjs cursos/csharp
import fs from 'node:fs';
import path from 'node:path';
import { openChrome } from './chrome.mjs';

const folder = process.argv[2] ?? 'cursos/csharp';
const block = (text, title) => {
    const at = text.search(new RegExp(`^#{3,4} ${title}\\s*$`, 'm'));
    if (at < 0) return null;
    const after = text.slice(at);
    const match = after.match(/```[\w]*\n([\s\S]*?)\n?```/);
    return match ? match[1] : null;
};
const clean = (s) => (s ?? '').split('\n').map((l) => l.trimEnd()).join('\n').trimEnd();

const items = [];
for (const file of fs.readdirSync(folder).filter((f) => f.endsWith('.md')).sort()) {
    const text = fs.readFileSync(path.join(folder, file), 'utf8');
    for (const part of text.split(/^(?=### (?:Micro-misión|Encargo|Misión) |## R\d+-N\d+ )/m)) {
        const head = part.split('\n')[0];
        if (head.startsWith('## ')) {
            const code = block(part, 'Código de ejemplo');
            if (code) items.push({ id: `${head.slice(3, 10)} ejemplo`, code, want: block(part, 'Salida esperada'), stdin: block(part, 'Entrada de ejemplo') ?? '' });
        } else if (head.startsWith('### ')) {
            const id = head.match(/R\d+-N\d+-\w+/)?.[0];
            const code = block(part, 'Solución') ?? block(part, 'Solución de referencia');
            const start = head.startsWith('### Micro') ? block(part, 'Código inicial') : null;
            items.push({ id, code, start, want: block(part, 'Salida esperada'), stdin: block(part, 'Entrada') ?? block(part, 'Entrada de ejemplo') ?? '' });
        }
    }
}

const chrome = await openChrome();
let bad = 0;
for (const item of items) {
    const got = await chrome.run(item.code, { stdin: item.stdin });
    const problems = [];
    if (got.error) problems.push(`error: ${got.error}`);
    if (clean(got.output) !== clean(item.want)) problems.push(`salida:\n${got.output}\nesperada:\n${item.want}`);
    if (got.stderr) problems.push(`avisos: ${got.stderr}`);
    if (item.start !== null && item.start !== undefined) {
        const first = await chrome.run(item.start, { stdin: item.stdin });
        if (!first.error && clean(first.output) === clean(item.want)) problems.push('el código inicial ya da la salida');
    }
    console.log(`${problems.length ? '✗' : '✓'} ${item.id}${problems.length ? `\n    ${problems.join('\n    ')}` : ''}`);
    bad += problems.length ? 1 : 0;
}
chrome.close();
console.log(bad ? `${bad} de ${items.length} con problemas` : `${items.length} de ${items.length}`);
process.exit(bad ? 1 : 0);
