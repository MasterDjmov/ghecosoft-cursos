"""Escribe las micro-misiones en el formato del importador y las inserta en los .md del curso de Python."""
import importlib.util
import re
import sys
import textwrap

import os

BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
ROOT = os.path.abspath(BASE + "../..") + "/"
sys.path.insert(0, BASE)
from gen import run  # noqa: E402


def load(f):
    spec = importlib.util.spec_from_file_location("d", BASE + f)
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    return d.NODOS


def fix(text):
    # La historia de Python es la de Mia (D84): {heroe} todavía es el héroe del alumno.
    return textwrap.dedent(text).strip().replace("{heroe}", "Mia")


def block(m):
    meta = [f"lugar: {m['lugar']}", f"personajes: {m['personajes']}"]
    if m.get("criatura"):
        meta.append(f"criatura: {m['criatura']}")
    meta += [f"carta: {m['carta']}", f"recompensa: {m['recompensa']}"]
    if m.get("item"):
        meta.append(f"item: {m['item']}")
    if m.get("se_abre"):
        meta.append("se abre: " + re.sub(r"\*\*", "", m["se_abre"]).rstrip("."))
    out = [f"### Micro-misión {m['id']} · {m['titulo']}", "", "```meta", *meta, "```", "",
           "#### Escena", fix(m["escena"]), "",
           "#### Gheco sugiere", fix(m["sugiere"]), "",
           "#### Desafío", fix(m["desafio"]), "",
           "#### Código inicial", "```python", m["inicial"].rstrip("\n"), "```", ""]
    if m.get("entrada"):
        out += ["#### Entrada", "```", m["entrada"].rstrip("\n"), "```", ""]
    out += ["#### Salida esperada", "```", m["expected"], "```", "",
            "#### Solución", *(["```python", m["solucion"].rstrip("\n"), "```"] if m.get("solucion_es_codigo", True) else [m["solucion"]]), "",
            "#### Al superarla", fix(m["al_superar"]), "",
            "#### Imagen", *[f"- {line}" for line in m["imagen"]], ""]
    return "\n".join(out)


def from_doc(doc, node_prefix):
    """Convierte las micro-misiones escritas a mano en el documento (Clase 0 y nodo 1)."""
    parts = re.split(r"^#### Micro-misión ", doc, flags=re.M)[1:]
    steps = []
    for p in parts:
        head, body = p.split("\n", 1)
        sid, title = [x.strip() for x in head.split("·", 1)]
        if not sid.startswith(node_prefix):
            continue
        body = body.split("\n---")[0].split("\n> Después")[0].split("\n### ")[0]
        meta = re.search(r"```meta\n(.*?)\n```", body, re.S).group(1)
        meta_d = dict(line.split(": ", 1) for line in meta.splitlines() if ": " in line)

        def label(name, nxt):
            mm = re.search(r"^\*\*" + name + r"\.?\*\*\s*(.*?)(?=\n\*\*(?:" + nxt + r")\.?\*\*|\Z)", body, re.S | re.M)
            return mm.group(1).strip() if mm else ""

        labels = "Escena|Gheco sugiere|Desafío|Entrada|Salida esperada|Solución|Al superarla|Se abre|Imagen"
        escena = label("Escena", labels)
        sugiere = label("Gheco sugiere", labels)
        desafio_full = label("Desafío", labels)
        code = re.search(r"```python\n(.*?)\n```", desafio_full, re.S)
        desafio = desafio_full.split("```")[0].strip()
        entrada = re.search(r"```\n(.*?)\n```", label("Entrada", labels), re.S)
        salida = re.search(r"```\n(.*?)\n```", label("Salida esperada", labels), re.S).group(1)
        solucion = label("Solución", labels)
        sol_code = re.search(r"```python\n(.*?)\n```", solucion, re.S)
        al = label("Al superarla", labels)
        se_abre = re.search(r"\*\*Se abre:\*\*\s*(.*)", body)
        imagen = [l[2:] for l in label("Imagen", labels).splitlines() if l.startswith("- ")]
        sol_text = sol_code.group(1) if sol_code else solucion
        if re.fullmatch(r"`[^`]+`\.?", sol_text.strip()):
            sol_text = sol_text.strip().rstrip(".").strip("`")
        m = {
            "id": sid, "titulo": title, "lugar": meta_d["lugar"], "personajes": meta_d["personajes"],
            "criatura": meta_d.get("criatura"), "carta": meta_d["carta"], "recompensa": meta_d["recompensa"],
            "item": meta_d.get("item"), "se_abre": se_abre.group(1) if se_abre else None,
            "escena": escena, "sugiere": sugiere, "desafio": desafio,
            "inicial": code.group(1) if code else "", "entrada": entrada.group(1) + "\n" if entrada else None,
            "expected": salida, "solucion": sol_text, "solucion_es_codigo": "\n" in sol_text or bool(re.fullmatch(r"[\w\s=+\-*/().,\"'{}\[\]:|%·¿?áéíóúñ!¡]+", sol_text)) and not sol_text.startswith(("Cerrar", "Sobraba")), "al_superar": al, "imagen": imagen,
        }
        steps.append(m)
    return steps


def insert(path, node_code, blocks):
    text = open(path).read()
    # Se vuelven a escribir: se sacan las que ya estaban de este nodo.
    text = re.sub(r"### Micro-misión " + re.escape(node_code) + r"-P\d+ ·.*?(?=^### |^## |\Z)", "", text, flags=re.S | re.M)
    start = text.index(f"## {node_code} ·")
    nxt = re.search(r"^## ", text[start + 3:], re.M)
    end = start + 3 + nxt.start() if nxt else len(text)
    section = text[start:end]
    first_practice = re.search(r"^### (Misión|Encargo|Práctica|Desafío) " + re.escape(node_code), section, re.M)
    pos = start + first_practice.start()
    text = text[:pos] + "\n".join(blocks) + "\n" + text[pos:]
    open(path, "w").write(text)


FILES = {"r02": "02-objetos-errores.md", "r03": "03-iteracion-calidad.md", "s01": "04-senda-arena.md", "s02": "05-senda-reino.md"}

if __name__ == "__main__":
    # python3 scripts/micro-misiones/to_course.py s01.py s02.py  → las inserta (o reescribe) en cursos/python/
    for f in sys.argv[1:]:
        for n in load(f):
            code = n["titulo"].split(" ·")[0]
            for m in n["misiones"]:
                m["expected"] = run(m["solucion"], m.get("entrada", "") or "")
            insert(ROOT + "cursos/python/" + FILES[f.split(".")[0]], code, [block(m) for m in n["misiones"]])
            print(code, len(n["misiones"]))
