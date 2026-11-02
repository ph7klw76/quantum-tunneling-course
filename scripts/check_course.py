"""Portable scientific/course checks; no video renderer or neural models needed."""
import json
from pathlib import Path
import sys
import numpy as np
import nbformat
from nbclient import NotebookClient
import srt

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from course.physics import transmission,wavefunction

out=ROOT/'outputs';out.mkdir(exist_ok=True)
cases=[]
for E,V,a in [(.5,1,.45),(.5,1,.9),(.1,.9,.25),(.89,.9,1.2),(.5,1,0)]:
    x=np.linspace(-.8,a+.9,19);p,_=wavefunction(x,E,V,a)
    cases.append(dict(E=E,V=V,a=a,T=transmission(E,V,a),x=x.tolist(),p=[[float(z.real),float(z.imag)] for z in p]))
(out/'physics-fixtures.json').write_text(json.dumps(cases),encoding='utf-8')
timeline=json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8'))
cues=list(srt.parse((ROOT/'narration/lecture.srt').read_text(encoding='utf-8')))
assert ' '.join(' '.join(c.content.split()) for c in cues)==' '.join(' '.join(s['text'].split()) for s in timeline)
assert all(0<=c.start.total_seconds()<c.end.total_seconds() for c in cues)
assert all(a.end<=b.start for a,b in zip(cues,cues[1:]))
questions=json.loads((ROOT/'quizzes/quizzes.json').read_text(encoding='utf-8'))
for q in questions:
    slot=next(s for s in timeline if s['start']<=q['time_seconds']<s['start']+s['duration'])
    assert slot['kind']=='predict' and slot['speech_end']<=q['time_seconds']
    assert slot['start']+slot['duration']-q['time_seconds']>5
book=nbformat.read(ROOT/'lab/files/Quantum_Tunneling_Lab.ipynb',as_version=4)
nbformat.validate(book)
executed=NotebookClient(book,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT/'lab')}}).execute()
nbformat.write(executed,out/'Quantum_Tunneling_Lab_executed.ipynb')
report=dict(physics_fixture_samples=95,subtitle_cues=len(cues),synchronized_quizzes=len(questions),executed_notebook_code_cells=sum(c.cell_type=='code' for c in book.cells),notebook_errors=0)
(out/'course-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
