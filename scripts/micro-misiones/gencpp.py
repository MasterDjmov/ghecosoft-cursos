"""Micro-misiones de C++ (D100): compila cada solución con g++ -std=c++20 -Wall -Wextra y la ejecuta; la salida
esperada sale de ahí, nunca a mano. Comprueba que la solución compile SIN advertencias, que el código inicial NO dé
ya esa salida y que nada dependa de la máquina. En el navegador C++ corre en wasm32 con libc++ (en la compu del
alumno, con libstdc++ o la de su compilador), así que no se aceptan: `rand()`, las distribuciones de <random> (cada
biblioteca las calcula distinto; `std::mt19937` crudo sí es igual en todas), `random_device`, `typeid`, `std::hash`,
`%p`, `sizeof(long)` ni `sizeof` de punteros. Los `unordered_map` y `unordered_set` se aceptan solo si nunca se
muestra su orden (se marca la misión con `orden_libre=True` después de revisarlo). Las inserta en cursos/cpp/.

    python3 scripts/micro-misiones/gencpp.py cpp_r01.py          # comprueba y muestra las salidas
    python3 scripts/micro-misiones/gencpp.py cpp_r01.py --apply  # además las escribe en el curso
    python3 scripts/micro-misiones/gencpp.py cpp_r01.py --json x.json  # los casos para probarlos en Chrome
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

FILES = {"R00": "00-curso.md", "R01": "01-los-cimientos.md", "R02": "02-los-planos.md",
         "R03": "03-los-talleres-modernos.md", "R04": "04-la-gran-biblioteca.md", "R05": "05-el-taller-del-juego.md",
         "R06": "06-los-vitrales.md", "S01": "07-senda-linterna-magica.md"}

# Lo que da distinto en el navegador (wasm32 con libc++) que en la compu del alumno.
NOT_PORTABLE = [(r"%p", "%p muestra direcciones"), (r"sizeof\s*\(\s*(unsigned\s+)?long\b", "sizeof(long) es 4 en el navegador"),
                (r"sizeof\s*\([^)]*\*\s*\)", "sizeof de un puntero es 4 en el navegador"), (r"\brand\s*\(", "rand() da otra secuencia"),
                (r"_distribution\b", "las distribuciones de <random> dan otra secuencia en cada biblioteca"),
                (r"random_device", "random_device no se repite"), (r"\btypeid\b", "typeid().name() cambia con el compilador"),
                (r"std::hash\b", "std::hash cambia con la biblioteca")]


def m(**kw):
    for k in ("inicial", "solucion"):
        kw[k] = textwrap.dedent(kw[k]).lstrip("\n")
    return kw


def cpp(code, stdin=""):
    """Compila y corre en una carpeta vacía. Devuelve (código de salida, salida, errores, advertencias)."""
    with tempfile.TemporaryDirectory() as tmp:
        src, exe = os.path.join(tmp, "main.cpp"), os.path.join(tmp, "programa")
        open(src, "w", encoding="utf-8").write(code)
        built = subprocess.run(["g++", "-std=c++20", "-Wall", "-Wextra", src, "-o", exe], capture_output=True, text=True, cwd=tmp)
        if built.returncode != 0:
            return built.returncode, "", built.stderr, built.stderr
        r = subprocess.run([exe], input=stdin, capture_output=True, text=True, timeout=10, cwd=tmp)
    return r.returncode, r.stdout.rstrip("\n"), r.stderr, built.stderr


def fix(text):
    return textwrap.dedent(text).strip().replace("{heroe}", "Bron")


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
           "#### Desafío", fix(s["desafio"]), "", "#### Código inicial", "```cpp", s["inicial"].rstrip("\n"), "```", ""]
    if s.get("entrada"):
        out += ["#### Entrada", "```", s["entrada"].rstrip("\n"), "```", ""]
    out += ["#### Salida esperada", "```", expected, "```", "",
            "#### Solución", "```cpp", s["solucion"].rstrip("\n"), "```", "",
            "#### Al superarla", fix(s["al_superar"]), "",
            "#### Imagen", *[f"- {line}" for line in s["imagen"]], ""]
    return "\n".join(out)


def check(s):
    for pattern, why in NOT_PORTABLE:
        if re.search(pattern, s["solucion"]):
            raise SystemExit(f"{s['id']}: no es portable ({why})")
    if "unordered_" in s["solucion"] and not s.get("orden_libre"):
        raise SystemExit(f"{s['id']}: usa unordered_*: revisá que no se muestre su orden y marcala con orden_libre=True")
    stdin = s.get("entrada") or ""
    rc, expected, err, warnings = cpp(s["solucion"], stdin)
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
    if any(ord(ch) > 127 for ch in expected):
        raise SystemExit(f"{s['id']}: la salida tiene tildes o eñes (en la consola de Windows se ven mal al pegarlas)")
    rc2, out2, _, _ = cpp(s["inicial"], stdin)
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
            insert(ROOT + "cursos/cpp/" + FILES[code[:3]], code, blocks)
    if "--json" in sys.argv:
        json.dump(cases, open(sys.argv[sys.argv.index("--json") + 1], "w"), ensure_ascii=False)
    print("ok", total, "(escritas en el curso)" if apply else "")
