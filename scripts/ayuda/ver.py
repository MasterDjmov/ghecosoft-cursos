# D123: muestra desafío, código inicial, solución y salida de las micro-misiones SIN Pasos (para escribirlos).
import re,sys,glob
# uso: ver.py carpeta COD1 COD2 ... (prefijo: R01-N01 muestra todas las de ese nodo)
files=sorted(glob.glob(sys.argv[1]+'/*.md'))
txt=''.join(open(f).read() for f in files)
for m in re.finditer(r'^### Micro-misión (\S+) · (.*?)\n(.*?)(?=^### |^## |\Z)', txt, re.S|re.M):
    code=m.group(1)
    if not any(code.startswith(p) for p in sys.argv[2:]): continue
    b=m.group(3)
    if '#### Pasos' in b: continue
    def sec(n):
        x=re.search(r'^#### '+n+r'\n(.*?)(?=^#### |\Z)', b, re.S|re.M)
        return x.group(1).strip() if x else ''
    strip=lambda t: re.sub(r'^```\w*\n|```$','',t.strip()).strip()
    print(f'=== {code} · {m.group(2)}\nDESAFIO: {sec("Desafío")}\nINICIAL:\n{strip(sec("Código inicial"))}\nSOL:\n{strip(sec("Solución"))}\nSALIDA:\n{strip(sec("Salida esperada"))}\n')
