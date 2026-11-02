"""Produce portable source and complete ready-to-serve course ZIPs."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
TOP=['README.md','LICENSE','CONTENT_LICENSE.md','requirements.txt','requirements-ci.txt','requirements-production.txt','requirements-lite.txt','requirements-neural.txt','requirements-neural-lock.txt','build.py','.gitignore']
DIRS=['course','tests','video','scripts','docs','quizzes','h5p','lab','narration','.github','website','webtools','remotion']
def include(p,built):
    rel=p.relative_to(ROOT);parts=rel.parts
    if '__pycache__' in parts or '.openai' in parts or '.git' in parts or 'node_modules' in parts:return False
    if any(x.startswith('.doit') for x in parts):return False
    if parts[0]=='remotion' and ('.bundle' in parts or '.cache' in parts or parts[1:3]==('public','media')):return False
    if p.suffix in ('.pyc','.log','.db'):return False
    if parts[:2]==('narration','neural'):return False
    if parts[0]=='narration' and p.suffix not in ('.md','.srt','.json'):return False
    if parts[0]=='lab' and len(parts)>1 and parts[1] not in ('files','Quantum_Tunneling_Lab.ipynb','jupyter-lite.json','jupyter_lite_config.json'):return False
    if not built and parts[:3]==('website','dist','lab'):return False
    if not built and rel.as_posix()=='website/dist/lecture.mp4':return False
    return True

def package(built):
    name='Quantum_Tunneling_Complete' if built else 'Quantum_Tunneling_Source'
    candidates=[ROOT/f for f in TOP]
    for folder in DIRS:candidates.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and include(p,built))
    candidates.extend(p for p in (ROOT/'outputs').iterdir() if p.is_file() and p.name!='downloads.json' and p.suffix in ('.json','.md','.png','.jpg','.ipynb'))
    if built:
        for filename in ['Quantum_Tunneling_Lecture.mp4','Quantum_Tunneling_Lecture_Remotion.mp4']:
            if (ROOT/'outputs'/filename).exists():candidates.append(ROOT/'outputs'/filename)
        master=ROOT/'outputs/Quantum_Tunneling_Narration.wav'
        if master.exists():candidates.append(master)
        samples=ROOT/'outputs/voice_samples'
        if samples.exists():candidates.extend(p for p in samples.rglob('*') if p.is_file() and p.suffix in ('.wav','.json','.md','.html'))
    target=ROOT/'outputs'/f'{name}.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
        for p in sorted(set(candidates)):z.write(p,p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(target) as z:assert z.testzip() is None
    return dict(file=target.name,bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest())

if __name__=='__main__':
    result=[package(False),package(True)]
    (ROOT/'outputs/downloads.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
