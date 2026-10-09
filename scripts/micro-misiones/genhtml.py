"""Micro-misiones de HTML y CSS (D102): cada una trae qué revisa el inspector, y la salida esperada es el informe
del inspector (resources/js/runners/inspector.js) sobre la solución, corrido en Chrome con inspect.mjs: nunca a
mano. Comprueba que ningún pedido esté mal escrito, que la solución dé un informe y que el código inicial NO dé ya
ese informe. Las inserta en cursos/html/.

    python3 scripts/micro-misiones/genhtml.py html_r01.py          # comprueba y muestra los informes
    python3 scripts/micro-misiones/genhtml.py html_r01.py --apply  # además las escribe en el curso
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

FILES = {"R00": "00-curso.md", "R01": "01-el-plomo.md", "R02": "02-los-vidrios.md", "R03": "03-las-plantillas.md",
         "R04": "04-el-gran-ventanal.md"}

BROKEN = ("(pedido mal escrito)", "(selector mal escrito)")


def m(**kw):
    for k in ("inicial", "solucion", "inspector"):
        kw[k] = textwrap.dedent(kw[k]).strip("\n")
    return kw


def fix(text):
    return textwrap.dedent(text).strip().replace("{heroe}", "Iris")


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
           "#### Desafío", fix(s["desafio"]), "", "#### Código inicial", "```html", s["inicial"], "```", "",
           "#### Inspector", "```", s["inspector"], "```", "",
           "#### Salida esperada", "```", expected, "```", "",
           "#### Solución", "```html", s["solucion"], "```", "",
           "#### Al superarla", fix(s["al_superar"]), "",
           "#### Imagen", *[f"- {line}" for line in s["imagen"]], ""]
    return "\n".join(out)


def inspect_all(cases):
    """{nombre: informe}, corriendo el inspector en Chrome."""
    with tempfile.TemporaryDirectory() as tmp:
        src, out = os.path.join(tmp, "casos.json"), os.path.join(tmp, "informes.json")
        json.dump(cases, open(src, "w", encoding="utf-8"), ensure_ascii=False)
        subprocess.run(["node", BASE + "inspect.mjs", src, out], check=True)
        return json.load(open(out, encoding="utf-8"))


def check(s, reports):
    expected, starter = reports[s["id"]], reports[s["id"] + ":inicial"]
    if not expected.strip():
        raise SystemExit(f"{s['id']}: el inspector no pide nada")
    for line in expected.split("\n"):
        if line.endswith(BROKEN):
            raise SystemExit(f"{s['id']}: {line}")
    if starter == expected:
        raise SystemExit(f"{s['id']}: el código inicial ya da el informe esperado")
    return expected


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("d", BASE + sys.argv[1])
    data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data)
    apply = "--apply" in sys.argv
    steps = [s for node in data.NODOS for s in node["misiones"]]
    cases = [c for s in steps for c in ({"name": s["id"], "code": s["solucion"], "checks": s["inspector"]},
                                         {"name": s["id"] + ":inicial", "code": s["inicial"], "checks": s["inspector"]})]
    reports = inspect_all(cases)
    total = 0
    for node in data.NODOS:
        code = node["titulo"].split(" ·")[0]
        blocks = []
        for s in node["misiones"]:
            expected = check(s, reports)
            print(f"== {s['id']}\n{expected}")
            blocks.append(block(s, expected))
            total += 1
        if apply:
            insert(ROOT + "cursos/html/" + FILES[code[:3]], code, blocks)
    print("ok", total, "(escritas en el curso)" if apply else "")
