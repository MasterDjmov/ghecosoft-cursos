// El corazón del compilador de TypeScript del navegador (D115, fase 5): revisa los tipos y pasa el código a JavaScript,
// todo en memoria (sin disco). Lo usa el worker (workers/typescript.worker.js) y lo prueba scripts/ts-micro con Node.
// No toca la página ni la red: recibe el compilador (`ts`), los .d.ts y los archivos del alumno.

export const MAIN = 'main.ts';
const DEFAULT_LIB = 'lib.esnext.full.d.ts';

/** Las opciones del Mirador: estrictas, como `tsc --init`, y para el JavaScript más nuevo (lo corre la caja). */
export function compilerOptions(ts) {
    return {
        target: ts.ScriptTarget.ES2022,
        module: ts.ModuleKind.ESNext,
        moduleResolution: ts.ModuleResolutionKind.Bundler,
        // Cada archivo es un módulo, como en la caja: sin "use strict" agregado y con `await` suelto.
        moduleDetection: ts.ModuleDetectionKind.Force,
        lib: [DEFAULT_LIB],
        strict: true,
        noImplicitOverride: true,
        useDefineForClassFields: true,
        skipLibCheck: true,
        sourceMap: true,
        removeComments: false,
        newLine: ts.NewLineKind.LineFeed,
        types: [],
    };
}

// Los .d.ts se leen una sola vez: lib.dom.d.ts solo tarda casi un segundo en armarse.
const libCache = new Map();

/**
 * @param {object} ts el compilador
 * @param {Record<string, string>} libs los .d.ts (nombre → texto)
 * @param {Record<string, string>} files los archivos del alumno: main.ts y los que importa (vec2.ts…)
 * @returns {{diagnostics: Array<{code: string, line: number|null, column: number|null, file: string|null, message: string}>,
 *   js: Record<string, string>, maps: Record<string, number[]>}}
 */
export function compile(ts, libs, files) {
    const options = compilerOptions(ts);
    const output = {};
    const bare = (name) => name.replace(/^\/+/, '');
    const host = {
        getSourceFile(name, languageVersion) {
            const key = bare(name);
            if (files[key] !== undefined) return ts.createSourceFile(key, files[key], languageVersion, true);
            if (libs[key] === undefined) return undefined;
            if (!libCache.has(key)) libCache.set(key, ts.createSourceFile(key, libs[key], languageVersion, false));
            return libCache.get(key);
        },
        getDefaultLibFileName: () => `/${DEFAULT_LIB}`,
        getDefaultLibLocation: () => '/',
        writeFile: (name, text) => { output[bare(name)] = text; },
        getCurrentDirectory: () => '/',
        getDirectories: () => [],
        directoryExists: () => true,
        fileExists: (name) => files[bare(name)] !== undefined || libs[bare(name)] !== undefined,
        readFile: (name) => files[bare(name)] ?? libs[bare(name)],
        getCanonicalFileName: (name) => name,
        useCaseSensitiveFileNames: () => true,
        getNewLine: () => '\n',
    };

    const program = ts.createProgram(Object.keys(files).map((name) => `/${name}`), options, host);
    const diagnostics = ts.getPreEmitDiagnostics(program)
        .filter((d) => d.category === ts.DiagnosticCategory.Error)
        .filter((d) => !d.file || files[bare(d.file.fileName)] !== undefined)
        .map((d) => {
            const position = d.file && d.start !== undefined ? d.file.getLineAndCharacterOfPosition(d.start) : null;
            return {
                code: `TS${d.code}`,
                line: position ? position.line + 1 : null,
                column: position ? position.character + 1 : null,
                file: d.file ? bare(d.file.fileName) : null,
                message: ts.flattenDiagnosticMessageText(d.messageText, '\n'),
            };
        })
        .sort((a, b) => (a.file === MAIN ? 0 : 1) - (b.file === MAIN ? 0 : 1) || (a.line ?? 0) - (b.line ?? 0));

    if (diagnostics.length) return { diagnostics, js: {}, maps: {} };

    program.emit();
    const js = {};
    const maps = {};
    for (const [name, text] of Object.entries(output)) {
        if (!name.endsWith('.js')) continue;
        // Sin el «export {}» que TypeScript agrega a los módulos sin exports, ni el renglón del source map.
        js[name] = text.replace(/\n\/\/# sourceMappingURL=.*$/, '\n').replace(/^export \{\};\n?/m, '');
        const map = output[`${name}.map`];
        if (map) maps[name] = lineMap(JSON.parse(map).mappings);
    }

    return { diagnostics: [], js, maps };
}

/** De los «mappings» del source map: para cada línea del JavaScript (desde 1), la línea del TypeScript de donde salió. */
export function lineMap(mappings) {
    const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    const lines = [0];
    let sourceLine = 0;
    for (const generated of mappings.split(';')) {
        let first = null;
        for (const segment of generated.split(',')) {
            if (!segment) continue;
            const values = [];
            let value = 0;
            let shift = 0;
            for (const char of segment) {
                const digit = CHARS.indexOf(char);
                value += (digit & 31) << shift;
                if (digit & 32) {
                    shift += 5;
                } else {
                    values.push(value & 1 ? -(value >> 1) : value >> 1);
                    value = 0;
                    shift = 0;
                }
            }
            if (values.length >= 4) {
                sourceLine += values[2];
                first ??= sourceLine + 1;
            }
        }
        lines.push(first ?? lines[lines.length - 1]);
    }

    return lines;
}
