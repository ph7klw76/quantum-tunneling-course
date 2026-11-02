"""Explicit source allowlist: no credentials, models, environments or media masters."""
from pathlib import Path
import hashlib
import json
ROOT=Path(__file__).resolve().parents[1]
files=set()
for name in ['README.md','LICENSE','CONTENT_LICENSE.md','.gitignore','build.py']:
    files.add(ROOT/name)
files.update(ROOT.glob('requirements*.txt'))
for folder in ['course','video','tests','scripts','docs','quizzes','h5p','.github']:
    for p in (ROOT/folder).rglob('*'):
        if p.is_file() and not any(x in p.parts for x in ['__pycache__','node_modules','.git','.openai']) and p.suffix not in ['.pyc','.log']:
            files.add(p)
for p in (ROOT/'narration').iterdir():
    if p.is_file() and p.suffix in ['.json','.md','.srt']:files.add(p)
for name in ['Quantum_Tunneling_Lab.ipynb','jupyter_lite_config.json','jupyter-lite.json','files/Quantum_Tunneling_Lab.ipynb']:
    files.add(ROOT/'lab'/name)
for p in (ROOT/'website/dist').iterdir():
    if p.is_file() and p.suffix not in ['.mp4','.wav','.zip']:files.add(p)
files.update((ROOT/'website/dist/h5p').glob('*.html'))
for name in ['package.json','pnpm-lock.yaml','pnpm-workspace.yaml','h5p-build.cjs','test-site.cjs','test-h5p-playback.cjs']:
    files.add(ROOT/'webtools'/name)
for name in ['youtube_description.md','neural-verification.json','neural-narration-report.json','course-checks.json','browser/results.json']:
    p=ROOT/'outputs'/name
    if p.exists():files.add(p)
manifest=[]
for p in sorted(files):
    data=p.read_bytes();relative=p.relative_to(ROOT).as_posix()
    assert len(data)<10*1024*1024, f'Oversized source: {relative}'
    assert p.suffix not in ['.mp4','.wav'], relative
    binary=b'\0' in data or p.suffix in ['.png','.h5p']
    manifest.append(dict(path=relative,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),binary=binary))
out=ROOT/'outputs/publication-manifest.json';out.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(files=len(manifest),bytes=sum(x['bytes'] for x in manifest),largest=sorted(manifest,key=lambda x:x['bytes'],reverse=True)[:3]),indent=2))
