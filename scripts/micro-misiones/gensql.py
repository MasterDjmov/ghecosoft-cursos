"""Micro-misiones con SQL (y Java) en el mismo nodo: las de SQL se ejecutan con SQLite, con el MISMO formato que el
ejecutor del navegador (resources/js/workers/sql.worker.js): por cada consulta que devuelve filas, una línea con
las columnas y una por fila, separadas por « | »; NULL como NULL; los números enteros sin decimales; las consultas
separadas por una línea vacía; la base empieza vacía y con las claves foráneas activadas.

    python3 scripts/micro-misiones/gensql.py java_s01.py          # comprueba y muestra las salidas
    python3 scripts/micro-misiones/gensql.py java_s01.py --apply  # además las escribe en el curso
"""
import importlib.util
import re
import sqlite3
import sys

from genjava import BASE, FILES, ROOT, fix, java, m  # noqa: F401  (m se usa desde los datos)
from to_course import insert


def fmt(value):
    if value is None:
        return "NULL"
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else repr(value)
    if isinstance(value, bytes):
        return "[blob]"
    return str(value)


def run_sql(code):
    """Devuelve (salida, error) como el worker: sentencia por sentencia, cortando en el primer error."""
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("PRAGMA foreign_keys = ON;")
    blocks, buf, error = [], "", None
    try:
        for line in code.split("\n"):
            buf += line + "\n"
            if sqlite3.complete_statement(buf):
                cur = db.execute(buf)
                if cur.description:
                    cols = [d[0] for d in cur.description]
                    rows = [" | ".join(fmt(v) for v in row) for row in cur.fetchall()]
                    blocks.append("\n".join([" | ".join(cols), *rows]))
                buf = ""
        if buf.strip():
            raise sqlite3.OperationalError("sentencia incompleta: " + buf.strip()[:40])
    except sqlite3.Error as e:
        error = str(e)
    finally:
        db.close()
    return "\n\n".join(blocks), error


def execute(s):
    if s.get("lenguaje", "java") == "sql":
        out, err = run_sql(s["solucion"])
        if err:
            raise SystemExit(f"{s['id']}: la solución falla\n{err}")
        out2, err2 = run_sql(s["inicial"])
        if not err2 and out2 == out:
            raise SystemExit(f"{s['id']}: el código inicial ya da la salida esperada")
        return out
    rc, out, err = java(s["solucion"], s.get("entrada") or "")
    if rc != 0:
        raise SystemExit(f"{s['id']}: la solución falla\n{err}")
    rc2, out2, _ = java(s["inicial"], s.get("entrada") or "")
    if rc2 == 0 and out2 == out:
        raise SystemExit(f"{s['id']}: el código inicial ya da la salida esperada")
    return out


def block(s, expected):
    lang = s.get("lenguaje", "java")
    meta = [f"lugar: {s['lugar']}", f"personajes: {s['personajes']}"]
    if s.get("criatura"):
        meta.append(f"criatura: {s['criatura']}")
    meta += [f"carta: {s['carta']}", f"recompensa: {s['recompensa']}"]
    if s.get("item"):
        meta.append(f"item: {s['item']}")
    out = [f"### Micro-misión {s['id']} · {s['titulo']}", "", "```meta", *meta, "```", "",
           "#### Escena", fix(s["escena"]), "", "#### Gheco sugiere", fix(s["sugiere"]), "",
           "#### Desafío", fix(s["desafio"]), "", "#### Código inicial", f"```{lang}", s["inicial"].rstrip("\n"), "```", ""]
    if s.get("entrada"):
        out += ["#### Entrada", "```", s["entrada"].rstrip("\n"), "```", ""]
    out += ["#### Salida esperada", "```", expected, "```", "",
            "#### Solución", f"```{lang}", s["solucion"].rstrip("\n"), "```", "",
            "#### Al superarla", fix(s["al_superar"]), "",
            "#### Imagen", *[f"- {line}" for line in s["imagen"]], ""]
    return "\n".join(out)


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("d", BASE + sys.argv[1])
    data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data)
    apply = "--apply" in sys.argv
    total = 0
    for node in data.NODOS:
        code = node["titulo"].split(" ·")[0]
        blocks = []
        for s in node["misiones"]:
            expected = execute(s)
            print(f"== {s['id']} ({s.get('lenguaje', 'java')})\n{expected}")
            blocks.append(block(s, expected))
            total += 1
        if apply:
            insert(ROOT + "cursos/java/" + FILES[code[:3]], code, blocks)
    print("ok", total, "(escritas en el curso)" if apply else "")
