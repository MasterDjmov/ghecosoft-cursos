// Compila y ejecuta C# en el navegador: Roslyn y el runtime de .NET en WebAssembly (scripts/csharp-runner, armado en
// public/toolchains/csharp). Nada corre en el servidor. Consola, teclado y carpeta son de mentira (Runner.cs).
const BASE = new URL('/toolchains/csharp/_framework/', self.location.origin).href;

async function gunzipped(url) {
    const response = await fetch(`${url}.gz`);
    if (!response.ok) throw new Error(`No se pudo bajar ${url} (${response.status})`);
    let bytes = new Uint8Array(await response.arrayBuffer());
    // Algunos servidores mandan el .gz con Content-Encoding y el navegador ya lo descomprimió.
    if (bytes[0] === 0x1f && bytes[1] === 0x8b) {
        bytes = new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
    }

    return new Response(bytes, { headers: { 'Content-Type': url.endsWith('.wasm') ? 'application/wasm' : 'application/octet-stream' } });
}

// La Bóveda (Acto V): el SQLite en WebAssembly de las micro-misiones de SQL (sql.js), que es sincrónico, así que el
// programa de C# le habla en el acto (Prelude/Sqlite.cs → Runner.Sql). Se baja solo si el programa lo usa, y cada
// ejecución empieza con una base vacía en memoria.
let SQL = null;
let db = null;

async function loadSql() {
    if (SQL) return;
    const [{ default: initSqlJs }, { default: wasmUrl }] = await Promise.all([
        import('sql.js/dist/sql-wasm.js'),
        import('sql.js/dist/sql-wasm.wasm?url'),
    ]);
    SQL = await initSqlJs({ locateFile: () => wasmUrl });
}

globalThis.csharpSql = (request) => {
    const { sql, values } = JSON.parse(request);
    if (!SQL) return JSON.stringify({ error: 'SQLite no está cargado' });
    if (!db) {
        db = new SQL.Database();
        db.run('PRAGMA foreign_keys = ON;');
    }
    const results = [];
    try {
        for (const statement of db.iterateStatements(sql)) {
            if (Object.keys(values).length > 0) statement.bind(values);
            const columns = statement.getColumnNames();
            const rows = [];
            while (statement.step()) {
                rows.push(statement.get().map((v) => (v instanceof Uint8Array ? null : v)));
            }
            statement.free();
            results.push({ columns, rows, changes: columns.length > 0 ? 0 : db.getRowsModified() });
        }
    } catch (error) {
        return JSON.stringify({ error: String(error?.message ?? error) });
    }

    return JSON.stringify({ results });
};

let exportsReady = null;
let currentId = 0;
let warming = true;

globalThis.csharpCompiled = () => {
    if (!warming) postMessage({ id: currentId, type: 'compiled' });
};

async function load() {
    // El runtime, si ve un worker, cree que es un hilo secundario y se queda esperando al principal: acá es el único.
    self.importScripts = undefined;
    self.window = self;
    self.document = { baseURI: self.location.href, currentScript: null, addEventListener() {}, removeEventListener() {} };
    const { dotnet } = await import(/* @vite-ignore */ `${BASE}dotnet.js`);
    const runtime = await dotnet
        .withApplicationCulture('es-AR')
        .withResourceLoader((type, name, defaultUri) => {
            if (type === 'dotnetjs' || /\.js(\?|$)/.test(defaultUri)) return defaultUri;

            return gunzipped(defaultUri.split('?')[0]);
        })
        .create();
    // Los mensajes del compilador, en español.
    await runtime.INTERNAL?.loadSatelliteAssemblies?.(['es']);
    const assembly = await runtime.getAssemblyExports(runtime.getConfig().mainAssemblyName);
    // La primera compilación es la que más tarda: se hace acá, mientras dice «Cargando».
    await assembly.Runner.Run('System.Console.Write("");', '');
    warming = false;

    return assembly.Runner;
}

self.onmessage = async ({ data }) => {
    currentId = data.id;
    try {
        const first = !exportsReady;
        exportsReady ??= load();
        const runner = await exportsReady;
        if (first) postMessage({ id: data.id, type: 'loaded' });
        if (/Microsoft\.Data\.Sqlite|SqliteConnection/.test(data.code)) await loadSql();
        db?.close();
        db = null;
        const started = performance.now();
        const result = JSON.parse(await runner.Run(data.code, data.stdin ?? ''));
        db?.close();
        db = null;
        postMessage({ id: data.id, type: 'done', ...result, ms: Math.round(performance.now() - started) });
    } catch (error) {
        postMessage({ id: data.id, type: 'failed', message: error?.message ?? String(error) });
    }
};
