"""Arma las micro-misiones en markdown y verifica cada solución ejecutándola (la salida esperada sale de ahí)."""
import importlib.util
import subprocess
import sys
import tempfile
import textwrap

TMP = tempfile.mkdtemp()


def run(code, stdin=""):
    r = subprocess.run([sys.executable, "-c", code], input=stdin, capture_output=True, text=True, timeout=10, cwd=TMP)
    if r.returncode != 0:
        raise SystemExit(f"La solución falla:\n{code}\n{r.stderr}")
    return r.stdout.rstrip("\n")


def check_start(start, solution, stdin=""):
    """El código inicial tiene que fallar o dar otra cosa (si no, el desafío no enseña nada)."""
    r = subprocess.run([sys.executable, "-c", start], input=stdin, capture_output=True, text=True, timeout=10, cwd=TMP)
    return r.returncode != 0 or r.stdout.rstrip("\n") != run(solution, stdin)


def render(m):
    expected = run(m["solucion"], m.get("entrada", ""))
    if not check_start(m["inicial"], m["solucion"], m.get("entrada", "")):
        raise SystemExit(f"{m['id']}: el código inicial ya da la salida esperada")
    meta = [f"lugar: {m['lugar']}", f"personajes: {m['personajes']}"]
    if m.get("criatura"):
        meta.append(f"criatura: {m['criatura']}")
    meta += [f"carta: {m['carta']}", f"recompensa: {m['recompensa']}"]
    if m.get("item"):
        meta.append(f"item: {m['item']}")
    meta.append(f"imagen: {m['id']}")
    out = [f"#### Micro-misión {m['id']} · {m['titulo']}", "", "```meta", *meta, "```", "",
           "**Escena.**", textwrap.dedent(m["escena"]).strip(), "",
           "**Gheco sugiere.**", textwrap.dedent(m["sugiere"]).strip(), "",
           f"**Desafío.** {textwrap.dedent(m['desafio']).strip()}", "",
           "```python", m["inicial"].rstrip("\n"), "```", ""]
    if m.get("entrada"):
        out += ["**Entrada.**", "```", m["entrada"].rstrip("\n"), "```", ""]
    out += ["**Salida esperada.**", "```", expected, "```", "",
            f"**Solución.** {m['solucion_txt']}", "",
            "**Al superarla.**", textwrap.dedent(m["al_superar"]).strip(), ""]
    if m.get("se_abre"):
        out += [f"**Se abre:** {m['se_abre']}", ""]
    out += ["**Imagen.**", *[f"- {line}" for line in m["imagen"]], "", "---", ""]
    return "\n".join(out)


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("datos", sys.argv[1])
    datos = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(datos)
    parts = []
    for node in datos.NODOS:
        parts += [f"### {node['titulo']}", "", textwrap.dedent(node.get("intro", "")).strip(), ""]
        parts += [render(m) for m in node["misiones"]]
        if node.get("cierre"):
            parts += [f"> {node['cierre']}", "", "---", ""]
    print("\n".join(parts))
