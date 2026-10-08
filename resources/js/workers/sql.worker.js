// SQL en el navegador (SQLite en WebAssembly, sql.js): cada ejecución empieza con una base vacía en memoria, en
// un worker que se corta si tarda. El código del alumno nunca se ejecuta en el servidor.
import initSqlJs from 'sql.js/dist/sql-wasm.js';
import wasmUrl from 'sql.js/dist/sql-wasm.wasm?url';

let SQL = null;

/** Un valor como lo muestra la consola: NULL, los enteros sin decimales y los textos tal cual. */
function format(value) {
    if (value === null) return 'NULL';
    if (value instanceof Uint8Array) return '[blob]';
    return String(value);
}

self.onmessage = async ({ data }) => {
    const { id, code } = data;
    try {
        if (!SQL) {
            SQL = await initSqlJs({ locateFile: () => wasmUrl });
            self.postMessage({ id, type: 'loaded' });
        }
    } catch (e) {
        self.postMessage({ id, type: 'failed', message: String(e?.message ?? e) });
        return;
    }

    const start = performance.now();
    const db = new SQL.Database();
    const blocks = [];
    let error = null;
    try {
        db.run('PRAGMA foreign_keys = ON;');
        // Sentencia por sentencia: si una falla, lo anterior ya se mostró.
        for (const statement of db.iterateStatements(code)) {
            const columns = statement.getColumnNames();
            const rows = [];
            while (statement.step()) {
                rows.push(statement.get().map(format).join(' | '));
            }
            if (columns.length > 0) {
                blocks.push([columns.join(' | '), ...rows].join('\n'));
            }
            statement.free();
        }
    } catch (e) {
        error = `Error de SQL: ${String(e?.message ?? e)}`;
    } finally {
        db.close();
    }
    self.postMessage({ id, type: 'done', output: blocks.join('\n\n'), error, ms: Math.round(performance.now() - start) });
};
