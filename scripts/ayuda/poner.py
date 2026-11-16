# D123: inserta los Pasos (#### Pasos, después de #### Desafío) desde un .txt con bloques «@@ CODIGO».
import re,sys,glob
# uso: poner.py carpeta pasos.txt   (pasos.txt: bloques "@@ CODIGO" seguidos del texto)
files=sorted(glob.glob(sys.argv[1]+'/*.md'))
data=open(sys.argv[2]).read()
pasos={k.strip():v.strip() for k,v in re.findall(r'^@@ (\S+)\n(.*?)(?=^@@ |\Z)', data, re.S|re.M)}
done=set()
for f in files:
    s=open(f).read(); orig=s
    for code,text in pasos.items():
        i=s.find(f'### Micro-misión {code} ')
        if i<0: continue
        j=s.find('\n### ',i+5); j=len(s) if j<0 else j
        k=s.find('\n## ',i+5)
        if 0<=k<j: j=k
        block=s[i:j]
        if '#### Pasos' in block: done.add(code); continue
        new=re.sub(r'(#### Desafío\n.*?\n)\n(#### )', lambda m: m.group(1)+'\n#### Pasos\n'+text+'\n\n'+m.group(2), block, count=1, flags=re.S)
        assert new!=block, code
        s=s[:i]+new+s[j:]; done.add(code)
    if s!=orig: open(f,'w').write(s)
print('faltan:', set(pasos)-done or 'ninguna', '| puestas:', len(done))
