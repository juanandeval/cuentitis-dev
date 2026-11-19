#!/usr/bin/env python3
"""Valida lecturas.json antes de subirlo. Uso: python3 validate.py"""
import json, re, sys
TOPICS={"Animales","Dinosaurios","Espacio","Fútbol","Princesas y reyes","Superhéroes","Piratas","Coches","Cocina","Ciencia","Dragones","Robots","Naturaleza y medioambiente","Música","Misterios y detectives","¿Sabías que...?"}
# tramo: (palabras mín, máx, media palabras/frase mín, máx en narración)
LIM={"5-6":(350,550,7,13),"7-8":(380,600,8,15),"9-10":(450,650,11,18),"11-12":(450,650,14,22)}
err=0; warn=0; ids=set()
def bad(i,m):
    global err; err+=1; print(f"✗ {i}: {m}")
def note(i,m):
    global warn; warn+=1; print(f"! {i}: {m}")
MARK=re.compile(r"\[en:([^|\]]+)\|([^\]]+)\]")
SUFFIX=re.compile(r"\[en:[^|\]]+\|[^\]]+\][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
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
    if not isinstance(eng,list): bad(i,"english debe ser una lista"); eng=[]
    if len(marks)!=len(eng): bad(i,"las marcas [en:…|…] no coinciden con la lista english")
    if len(eng)>5: note(i,"más de 5 palabras en inglés")
    if any(not isinstance(e,dict) or not str(e.get("en","")).strip() or not str(e.get("es","")).strip() for e in eng): bad(i,"entrada english incompleta")
    english_pairs={(e.get("en"),e.get("es")) for e in eng if isinstance(e,dict)}
    for en,es in marks:
        if (en,es) not in english_pairs: bad(i,f"la marca [en:{en}|{es}] no coincide exactamente con english")
    if len({e.get("en") for e in eng if isinstance(e,dict)})!=len(eng): bad(i,"palabra inglesa repetida en english")
    if any(SUFFIX.search(p) for p in ps_raw): bad(i,"hay una terminación fuera de los corchetes [en:…|…]")
    if "¿Sabías que...?" in r.get("topics",[]):
        refs=r.get("sources",[])
        if not refs: bad(i,"las lecturas de ¿Sabías que...? necesitan fuentes")
        if any(not str(src.get("url","")).startswith("https://") for src in refs):
            bad(i,"fuente de ¿Sabías que...? sin URL segura")
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
        options=q.get("options",[])
        if not isinstance(options,list) or len(options)!=opts: bad(i,f"pregunta {k}: debe tener {opts} opciones")
        elif any(not isinstance(option,str) or not option.strip() for option in options): bad(i,f"pregunta {k}: todas las opciones deben ser textos no vacíos (sin null)")
        n_options=len(options) if isinstance(options,list) else 0
        if type(q.get("answer")) is not int or not 0<=q["answer"]<n_options: bad(i,f"pregunta {k}: answer inválido")
        if not isinstance(q.get("why"),str) or not q["why"].strip(): bad(i,f"pregunta {k}: falta una explicación why")
print(f"{len(data)} lecturas, {err} errores, {warn} avisos"); sys.exit(1 if err else 0)
