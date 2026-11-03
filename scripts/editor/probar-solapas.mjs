#!/usr/bin/env node
// Prueba de las solapas del visor de HTML y CSS (resources/js/editor/html-files.js): en cada bloque ```html de los
// cursos, separar en index.html / estilos.css / app.js y volver a juntar sin tocar nada tiene que dar el original
// exacto, y lo que se escribe en el CSS (o el JS) tiene que llegar a la página.
//
//   node scripts/editor/probar-solapas.mjs [cursos/html cursos/javascript …]
import fs from 'node:fs';
import path from 'node:path';
import { splitHtml } from '../../resources/js/editor/html-files.js';

const folders = process.argv.slice(2).length ? process.argv.slice(2) : ['cursos/html', 'cursos/javascript'];
let total = 0;
let split = 0;
const problems = [];
for (const folder of folders) {
    for (const file of fs.readdirSync(folder).filter((f) => f.endsWith('.md'))) {
        const text = fs.readFileSync(path.join(folder, file), 'utf8');
        for (const m of text.matchAll(/```html\n([\s\S]*?)\n```/g)) {
            total++;
            const s = splitHtml(m[1]);
            if (!s) continue;
            split++;
            const texts = s.files.map((f) => f.text);
            if (s.join(texts) !== m[1]) problems.push(`${folder}/${file}: no vuelve igual`);
            texts.slice(1).forEach((_, i) => {
                const edited = [...texts];
                edited[i + 1] += '\n/* prueba-solapas */';
                const tag = s.files[i + 1].name.endsWith('.css') ? 'style' : 'script';
                if (!new RegExp(`<${tag}[^>]*>[\\s\\S]*prueba-solapas[\\s\\S]*</${tag}>`).test(s.join(edited))) problems.push(`${folder}/${file}: lo editado en ${s.files[i + 1].name} no llega`);
            });
        }
    }
}
problems.slice(0, 10).forEach((p) => console.log('  ✗', p));
console.log(`${split} de ${total} bloques se separan en archivos; ${problems.length ? `${problems.length} con problemas` : 'todos vuelven exactos'}.`);
process.exit(problems.length ? 1 : 0);
