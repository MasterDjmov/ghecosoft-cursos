"""Micro-misiones de C (D98): compila cada solución con gcc -std=c11 -Wall -Wextra (como el Clang del navegador) y la
ejecuta; la salida esperada sale de ahí, nunca a mano. Comprueba que la solución compile SIN advertencias, que el
código inicial NO dé ya esa salida y que nada dependa de la máquina: en el navegador C corre en wasm32 (long y los
punteros miden 4 bytes y rand() da otra secuencia que en Linux o Windows), así que no se aceptan `%p`, `sizeof(long)`,
`sizeof` de punteros ni `rand()`. Las inserta en cursos/c/ antes de las prácticas.

    python3 scripts/micro-misiones/genc.py c_r01.py          # comprueba y muestra las salidas
    python3 scripts/micro-misiones/genc.py c_r01.py --apply  # además las escribe en el curso
    python3 scripts/micro-misiones/genc.py c_r01.py --json x.json  # los casos para probarlos en Chrome (ctest.mjs)
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

FILES = {"R00": "00-curso.md", "R01": "01-templar-el-metal.md", "R02": "02-pasillos-numerados.md",
         "R03": "03-las-minas.md", "R04": "04-el-archivo.md", "R05": "05-prueba-del-temple.md",
         "S01": "06-senda-forja-viva.md", "S02": "07-senda-automatas.md"}

# Lo que da distinto en el navegador (wasm32) que en la compu del alumno.
NOT_PORTABLE = [(r"%p", "%p muestra direcciones"), (r"sizeof\s*\(\s*(unsigned\s+)?long\b", "sizeof(long) es 4 en el navegador"),
                (r"sizeof\s*\([^)]*\*\s*\)", "sizeof de un puntero es 4 en el navegador"), (r"\brand\s*\(", "rand() da otra secuencia")]


def m(**kw):
    for k in ("inicial", "solucion"):
        kw[k] = textwrap.dedent(kw[k]).lstrip("\n")
    return kw


def c(code, stdin=""):
    """Compila y corre. Devuelve (código de salida, salida, errores, advertencias)."""
    with tempfile.TemporaryDirectory() as tmp:
        src, exe = os.path.join(tmp, "main.c"), os.path.join(tmp, "programa")
        open(src, "w", encoding="utf-8").write(code)
        built = subprocess.run(["gcc", "-std=c11", "-Wall", "-Wextra", src, "-lm", "-o", exe], capture_output=True, text=True, cwd=tmp)
        if built.returncode != 0:
            return built.returncode, "", built.stderr, built.stderr
        r = subprocess.run([exe], input=stdin, capture_output=True, text=True, timeout=10, cwd=tmp)
    return r.returncode, r.stdout.rstrip("\n"), r.stderr, built.stderr


def fix(text):
    return textwrap.dedent(text).strip().replace("{heroe}", "Kira")


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
           "#### Desafío", fix(s["desafio"]), "", "#### Código inicial", "```c", s["inicial"].rstrip("\n"), "```", ""]
    if s.get("entrada"):
        out += ["#### Entrada", "```", s["entrada"].rstrip("\n"), "```", ""]
    out += ["#### Salida esperada", "```", expected, "```", "",
            "#### Solución", "```c", s["solucion"].rstrip("\n"), "```", "",
            "#### Al superarla", fix(s["al_superar"]), "",
            "#### Imagen", *[f"- {line}" for line in s["imagen"]], ""]
    return "\n".join(out)


def check(s):
    for pattern, why in NOT_PORTABLE:
        if re.search(pattern, s["solucion"]):
            raise SystemExit(f"{s['id']}: no es portable ({why})")
    stdin = s.get("entrada") or ""
    rc, expected, err, warnings = c(s["solucion"], stdin)
    if rc != 0:
        raise SystemExit(f"{s['id']}: la solución falla\n{err}")
    if warnings.strip():
        raise SystemExit(f"{s['id']}: la solución tiene advertencias\n{warnings}")
    if not expected.strip():
        raise SystemExit(f"{s['id']}: la solución no muestra nada")
    if expected != expected.lstrip():
        raise SystemExit(f"{s['id']}: la salida empieza con espacios (el navegador y el servidor la recortan distinto)")
    if any(line != line.rstrip() for line in expected.split("\n")):
        raise SystemExit(f"{s['id']}: hay renglones que terminan en espacio (el navegador compara la salida exacta)")
    rc2, out2, _, _ = c(s["inicial"], stdin)
    if rc2 == 0 and out2 == expected:
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
            insert(ROOT + "cursos/c/" + FILES[code[:3]], code, blocks)
    if "--json" in sys.argv:
        json.dump(cases, open(sys.argv[sys.argv.index("--json") + 1], "w"), ensure_ascii=False)
    print("ok", total, "(escritas en el curso)" if apply else "")
