import importlib.util, sys
sys.path.insert(0, '.')
from gen import run, check_start
spec = importlib.util.spec_from_file_location("d", sys.argv[1]); d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
n = 0
for node in d.NODOS:
    for m in node["misiones"]:
        out = run(m["solucion"], m.get("entrada") or "")
        assert check_start(m["inicial"], m["solucion"], m.get("entrada") or ""), m["id"]
        n += 1
        if "-v" in sys.argv: print("==", m["id"]); print(out)
print("ok", n)
