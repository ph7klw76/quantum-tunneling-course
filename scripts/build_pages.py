"""Build a repository-subpath-safe GitHub Pages artifact without video binaries."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-path', default='/quantum-tunneling-course/')
    parser.add_argument('--output', default='outputs/pages')
    parser.add_argument('--skip-lab', action='store_true')
    args = parser.parse_args()
    base = '/' + args.base_path.strip('/') + '/' if args.base_path.strip('/') else '/'
    dest = (ROOT / args.output).resolve()
    assert dest.is_relative_to(ROOT) and dest != ROOT and 'outputs' in dest.parts
    dest.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'website/dist'
    for item in source.iterdir():
        if item.name in {'lab','.git','.openai'} or item.suffix.lower() in {'.mp4','.wav','.zip'}:
            continue
        if item.is_dir():
            shutil.copytree(item,dest/item.name,dirs_exist_ok=True)
        else:
            shutil.copy2(item,dest/item.name)
    # Never let a stale local video slip into a deployment artifact.
    forbidden = list(dest.rglob('*.mp4')) + list(dest.rglob('*.wav'))
    assert not forbidden, f'Unexpected media in Pages build: {forbidden}'
    shutil.copy2(ROOT/'h5p/Quantum_Tunneling_Interactive.h5p',dest/'h5p/Quantum_Tunneling_Interactive.h5p')
    for filename in ['LICENSE','CONTENT_LICENSE.md']:
        shutil.copy2(ROOT/filename,dest/filename)
    if not args.skip_lab:
        subprocess.run([sys.executable,'-m','jupyterlite_core','build','--lite-dir',str(ROOT/'lab'),'--contents',str(ROOT/'lab/files'),'--output-dir',str(dest/'lab'),'--base-url',base+'lab/'],check=True,cwd=ROOT)
    (dest/'.nojekyll').touch()
    info = dict(base_path=base,youtube_url='https://youtu.be/WCA_t3ttAAI',h5p='h5p/quantum-tunneling.html',notebook='lab/lab/index.html?path=Quantum_Tunneling_Lab.ipynb',files=sum(p.is_file() for p in dest.rglob('*')))
    (dest/'build-info.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(info))

if __name__ == '__main__':
    main()
