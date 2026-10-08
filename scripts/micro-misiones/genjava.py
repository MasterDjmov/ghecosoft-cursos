"""Micro-misiones de Java: ejecuta cada solución con el JDK de esta compu (la salida esperada sale de ahí, nunca a
mano), comprueba que el código inicial NO dé ya esa salida y las inserta en cursos/java/ antes de las prácticas.

    python3 scripts/micro-misiones/genjava.py java_r01.py          # comprueba y muestra las salidas
    python3 scripts/micro-misiones/genjava.py java_r01.py --apply  # además las escribe en el curso
"""
import importlib.util
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

FILES = {"R00": "00-curso.md", "R01": "01-la-aduana-del-compilador.md", "R02": "02-la-academia-de-los-moldes.md",
         "R03": "03-los-archivos-imperiales.md", "R04": "04-las-corrientes-del-imperio.md",
         "R05": "05-la-torre-del-arquitecto.md"}


def m(**kw):
    for k in ("inicial", "solucion"):
        kw[k] = textwrap.dedent(kw[k]).lstrip("\n")
    return kw


def java(code, stdin=""):
    """Compila y corre como el ejecutor (D85): el archivo se llama como la clase pública."""
    found = re.search(r"public\s+(?:final\s+)?class\s+(\w+)", code)
    name = found.group(1) if found else "Main"
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, name + ".java")
        open(path, "w", encoding="utf-8").write(code)
        r = subprocess.run(["java", "-Dfile.encoding=UTF-8", "-Dstdout.encoding=UTF-8", path], input=stdin,
                           capture_output=True, text=True, timeout=30, cwd=tmp)
    return r.returncode, r.stdout.rstrip("\n"), r.stderr


def fix(text):
    return textwrap.dedent(text).strip().replace("{heroe}", "Zed")


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
           "#### Desafío", fix(s["desafio"]), "", "#### Código inicial", "```java", s["inicial"].rstrip("\n"), "```", ""]
    if s.get("entrada"):
        out += ["#### Entrada", "```", s["entrada"].rstrip("\n"), "```", ""]
    out += ["#### Salida esperada", "```", expected, "```", "",
            "#### Solución", "```java", s["solucion"].rstrip("\n"), "```", "",
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
            stdin = s.get("entrada") or ""
            rc, expected, err = java(s["solucion"], stdin)
            if rc != 0:
                raise SystemExit(f"{s['id']}: la solución falla\n{err}")
            rc2, out2, _ = java(s["inicial"], stdin)
            if rc2 == 0 and out2 == expected:
                raise SystemExit(f"{s['id']}: el código inicial ya da la salida esperada")
            print(f"== {s['id']}\n{expected}")
            blocks.append(block(s, expected))
            total += 1
        if apply:
            insert(ROOT + "cursos/java/" + FILES[code[:3]], code, blocks)
    print("ok", total, "(escritas en el curso)" if apply else "")
