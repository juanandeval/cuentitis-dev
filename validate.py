#!/usr/bin/env python3
"""Valida lecturas.json antes de subirlo. Uso: python3 validate.py"""
import json, re, sys
TOPICS={"Animales","Dinosaurios","Espacio","Fútbol","Princesas y reyes","Superhéroes","Piratas","Coches","Cocina","Ciencia","Dragones","Robots"}
# tramo: (palabras mín, máx, media palabras/frase mín, máx en narración)
LIM={"5-6":(350,550,7,13),"7-8":(380,600,8,15),"9-10":(450,650,11,18),"11-12":(450,650,14,22)}
err=0; warn=0; ids=set()
def bad(i,m):
    global err; err+=1; print(f"✗ {i}: {m}")
def note(i,m):
    global warn; warn+=1; print(f"! {i}: {m}")
MARK=re.compile(r"\[en:([^|\]]+)\|([^\]]+)\]")
def clean(t): return MARK.sub(lambda m:m.group(2),t)
def sentences(t): return [x for x in re.split(r"(?<=[.!?…])\s+",t.strip()) if x]
data=json.load(open("lecturas.json",encoding="utf-8"))
for r in data:
    i=r.get("id","(sin id)")
    if i in ids: bad(i,"id repetido")
    ids.add(i)
    b=r.get("band")
    if b not in LIM: bad(i,"band inválido"); continue
    if r.get("hero") not in {"niño","niña","neutro"}: bad(i,"hero inválido")
    if not r.get("topics") or not set(r["topics"])<=TOPICS: bad(i,"topics inválidos")
    ps_raw=r.get("paragraphs",[]); ps=[clean(p) for p in ps_raw]; n=sum(len(p.split()) for p in ps)
    marks=[m for p in ps_raw for m in MARK.findall(p)]
    eng=r.get("english",[])
    if len(marks)!=len(eng): bad(i,"las marcas [en:…|…] no coinciden con la lista english")
    if len(eng)>5: note(i,"más de 5 palabras en inglés")
    if any(not e.get("es") for e in eng): bad(i,"palabra en inglés sin significado")
    lo,hi,smin,smax=LIM[b]
    if not lo<=n<=hi: note(i,f"{n} palabras (tramo {b}: {lo}-{hi})")
    narr=[s for p in ps if not p.startswith("—") for s in sentences(p)]
    if narr:
        avg=sum(len(s.split()) for s in narr)/len(narr)
        if not smin<=avg<=smax: note(i,f"frases de {avg:.1f} palabras de media (tramo {b}: {smin}-{smax})")
        run=m=0
        for s in narr:
            run=run+1 if len(s.split())<6 else 0; m=max(m,run)
        if b not in("5-6",) and m>=3: note(i,f"{m} frases cortas seguidas")
    if any("«" in p and "—" in p for p in ps): note(i,"diálogo mezclado entre « » y raya")
    qs=r.get("questions",[])
    if len(qs)!=5: bad(i,"debe tener 5 preguntas")
    opts=3 if b in("5-6","7-8") else 4
    for k,q in enumerate(qs,1):
        if len(q.get("options",[]))!=opts: bad(i,f"pregunta {k}: debe tener {opts} opciones")
        if not isinstance(q.get("answer"),int) or not 0<=q["answer"]<len(q.get("options",[])): bad(i,f"pregunta {k}: answer inválido")
print(f"{len(data)} lecturas, {err} errores, {warn} avisos"); sys.exit(1 if err else 0)
