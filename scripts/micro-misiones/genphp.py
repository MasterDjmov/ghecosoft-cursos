"""Micro-misiones de PHP (D105): corre cada solución con el PHP 8.3 de la compu (`php`), con la misma zona horaria
y los mismos avisos que el PHP del navegador del alumno, y la salida esperada sale de ahí, nunca a mano. Comprueba
que la solución no dé avisos (Warning, Notice, Deprecated), que el código inicial NO dé ya esa salida y que nada
dependa del reloj ni del azar sin semilla: no se aceptan `time()`, `date()` sin fecha fija, `microtime`,
`random_int`, `rand()` ni `mt_rand()` sin `mt_srand(semilla)`, `uniqid` ni `password_hash` mostrado (cambia cada
vez). Cada ejecución corre en una carpeta vacía nueva, como en el navegador. Las inserta en cursos/php/.

    python3 scripts/micro-misiones/genphp.py php_r01.py          # comprueba y muestra las salidas
    python3 scripts/micro-misiones/genphp.py php_r01.py --apply  # además las escribe en el curso
    python3 scripts/micro-misiones/genphp.py php_r01.py --json x.json  # los casos para probarlos en Chrome
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap

BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
ROOT = os.path.abspath(BASE + "../..") + "/"
sys.path.insert(0, BASE)
from to_course import insert  # noqa: E402

FILES = {"R00": "00-curso.md", "R01": "01-el-muelle-de-las-primeras-cartas.md", "R02": "02-el-astillero-de-los-moldes.md",
         "R03": "03-la-oficina-de-correos.md", "R04": "04-la-bodega-del-puerto.md", "R05": "05-el-faro.md",
         "S01": "06-senda-de-la-arena.md", "S02": "07-senda-de-la-ciudadela.md", "S03": "08-senda-de-los-mensajes-veloces.md",
         "S04": "09-senda-del-escaparate.md"}

# Lo que da distinto en cada ejecución o en cada compu.
NOT_PORTABLE = [(r"\btime\s*\(", "time() cambia cada vez"), (r"\bmicrotime\b|\bhrtime\b", "el reloj cambia cada vez"),
                (r"\bdate\s*\(\s*['\"][^'\"]*['\"]\s*\)", "date() sin fecha usa la hora de ahora"),
                (r"new\s+DateTime(Immutable)?\s*\(\s*\)|new\s+DateTime(Immutable)?\s*\(\s*['\"](now|today)", "la fecha de hoy cambia"),
                (r"\brandom_int\b|\brandom_bytes\b|\buniqid\b|\blcg_value\b", "da otro resultado cada vez"),
                (r"\brand\s*\(", "rand() sin semilla da otra secuencia"), (r"\bshuffle\s*\(|\barray_rand\s*\(|\bstr_shuffle\b", "mezcla al azar sin semilla"),
                (r"\bgetenv\b|\$_ENV|\$_SERVER\[['\"](REQUEST_TIME|HOME|PWD)", "depende de la compu"),
                (r"\bsleep\s*\(|\busleep\s*\(", "el navegador corta a los 5 segundos"),
                (r"NumberFormatter|IntlDateFormatter|Collator|\bgrapheme_|\bnumfmt_", "intl puede no estar en el PHP del navegador")]

# El navegador corre PHP 8.3 (`php` en esta compu puede ser otra versión).
PHP = ["php8.3", "-d", "date.timezone=America/Argentina/Buenos_Aires", "-d", "display_errors=1", "-d", "error_reporting=-1",
       "-d", "html_errors=0", "-d", "log_errors=0"]


def m(**kw):
    for k in ("inicial", "solucion"):
        kw[k] = textwrap.dedent(kw[k]).lstrip("\n")
    return kw


def php(code, stdin=""):
    """Corre en una carpeta vacía. Devuelve (código de salida, salida, errores)."""
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "main.php"), "w", encoding="utf-8").write(code)
        try:
            r = subprocess.run(PHP + ["main.php"], input=stdin, capture_output=True, text=True, timeout=10, cwd=tmp)
        except subprocess.TimeoutExpired:
            return 124, "", "se pasó de tiempo"
    return r.returncode, r.stdout.rstrip("\n"), r.stderr


def fix(text):
    return textwrap.dedent(text).strip().replace("{heroe}", "Nilo")


def block(s, expected):
    meta = [f"lugar: {s['lugar']}", f"personajes: {s['personajes']}"]
    if s.get("criatura"):
        meta.append(f"criatura: {s['criatura']}")
    meta += [f"carta: {s['carta']}", f"recompensa: {s['recompensa']}"]
    if s.get("item"):
        meta.append(f"item: {s['item']}")
    if s.get("se_abre"):
        meta.append("se abre: " + re.sub(r"\*\*", "", s["se_abre"]).rstrip("."))
    out = [f"### Micro-misión {s['id']} · {s['titulo']}", "", "```meta", *meta, "```", "",
           "#### Escena", fix(s["escena"]), "", "#### Gheco sugiere", fix(s["sugiere"]), "",
           "#### Desafío", fix(s["desafio"]), "", "#### Código inicial", "```php", s["inicial"].rstrip("\n"), "```", ""]
    if s.get("entrada"):
        out += ["#### Entrada", "```", s["entrada"].rstrip("\n"), "```", ""]
    out += ["#### Salida esperada", "```", expected, "```", "",
            "#### Solución", "```php", s["solucion"].rstrip("\n"), "```", "",
            "#### Al superarla", fix(s["al_superar"]), "",
            "#### Imagen", *[f"- {line}" for line in s["imagen"]], ""]
    return "\n".join(out)


WARN = re.compile(r"^(PHP )?(Warning|Notice|Deprecated|Fatal error|Parse error)", re.M)


def check(s):
    sol = s["solucion"]
    if not sol.startswith("<?php"):
        raise SystemExit(f"{s['id']}: la solución tiene que empezar con <?php")
    for pattern, why in NOT_PORTABLE:
        if re.search(pattern, sol):
            raise SystemExit(f"{s['id']}: no es portable ({why})")
    if re.search(r"\bmt_rand\s*\(", sol) and not re.search(r"\bmt_srand\s*\(\s*\d", sol):
        raise SystemExit(f"{s['id']}: mt_rand() necesita mt_srand(semilla) para dar siempre lo mismo")
    stdin = s.get("entrada") or ""
    rc, expected, err = php(sol, stdin)
    if rc != 0 and not s.get("sale_con_error"):
        raise SystemExit(f"{s['id']}: la solución termina con código {rc}\n{expected}\n{err}")
    if WARN.search(expected) or WARN.search(err):
        raise SystemExit(f"{s['id']}: la solución da avisos\n{expected}\n{err}")
    if not expected.strip():
        raise SystemExit(f"{s['id']}: la solución no muestra nada")
    if expected != expected.lstrip():
        raise SystemExit(f"{s['id']}: la salida empieza con espacios (el navegador y el servidor la recortan distinto)")
    if any(line != line.rstrip() for line in expected.split("\n")):
        raise SystemExit(f"{s['id']}: hay renglones que terminan en espacio (el navegador compara la salida exacta)")
    rc2, out2, _ = php(s["inicial"], stdin)
    if out2 == expected:
        raise SystemExit(f"{s['id']}: el código inicial ya da la salida esperada")
    return expected


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("d", BASE + sys.argv[1])
    data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data)
    apply = "--apply" in sys.argv
    cases = []
    total = 0
    for node in data.NODOS:
        code = node["titulo"].split(" ·")[0]
        blocks = []
        for s in node["misiones"]:
            expected = check(s)
            print(f"== {s['id']}\n{expected}")
            blocks.append(block(s, expected))
            cases.append({"name": s["id"], "code": s["solucion"], "stdin": s.get("entrada") or "", "expected": expected})
            total += 1
        if apply:
            insert(ROOT + "cursos/php/" + FILES[code[:3]], code, blocks)
    if "--json" in sys.argv:
        json.dump(cases, open(sys.argv[sys.argv.index("--json") + 1], "w"), ensure_ascii=False)
    print("ok", total, "(escritas en el curso)" if apply else "")
