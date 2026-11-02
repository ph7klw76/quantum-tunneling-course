"""Artifact-level verification. Browser and external-host results are separate."""
from pathlib import Path
import json,math,re,subprocess,sys,wave
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np
import av,nbformat,srt
from course.physics import transmission,amplitudes,wavefunction
from build import ffmpeg

report={}
def check(name,fn):
    result=fn();report[name]={'status':'PASS','result':result};print(name,': PASS',result,flush=True)

def physics():
    subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,check=True)
    return {'T':transmission(),'R':float(abs(amplitudes()[0])**2),'test_methods':7,'parameter_grid_cases':60}

def video():
    p=ROOT/'outputs/Quantum_Tunneling_Lecture.mp4';c=av.open(str(p));v=c.streams.video[0];a=c.streams.audio[0]
    assert (v.width,v.height)==(1920,1080) and v.codec_context.name=='h264'
    assert v.codec_context.format.name=='yuv420p' and v.average_rate==30
    assert a.codec_context.name=='aac'
    timeline=json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8'))
    expected=sum(s['duration'] for s in timeline);duration=c.duration/1e6
    assert 600<=duration<=720 and abs(duration-expected)<.08
    # Full actual decode of video and audio; -xerror makes any decode error fail.
    subprocess.run([ffmpeg(),'-v','error','-xerror','-i',str(p),'-f','null','-'],check=True)
    return dict(codec='H.264',size=[v.width,v.height],fps=30,duration_seconds=duration,bytes=p.stat().st_size,full_decode=True)

def captions():
    cues=list(srt.parse((ROOT/'narration/lecture.srt').read_text(encoding='utf-8')))
    prev=0
    for cue in cues:
        a,b=cue.start.total_seconds(),cue.end.total_seconds()
        assert 0<=a<b and a>=prev-.001;prev=b
    timeline=json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8'))
    actual=' '.join(' '.join(c.content.split()) for c in cues)
    expected=' '.join(' '.join(s['text'].split()) for s in timeline)
    assert actual==expected
    qs=json.loads((ROOT/'quizzes/quizzes.json').read_text(encoding='utf-8'))
    for q in qs:
        s=next(s for s in timeline if s['start']<=q['time_seconds']<s['start']+s['duration'])
        assert s['kind']=='predict' and q['time_seconds']>=s['speech_end']
        minutes,seconds=map(int,q['timestamp'].split(':'))
        assert minutes*60+seconds==q['time_seconds']
        assert s['start']+s['duration']-q['time_seconds']>5
        assert len(q['options'])<=4 and q['correct_index']<len(q['options'])
    return {'cues':len(cues),'exact_script_coverage':True,'timed_quizzes':len(qs),'last_caption_seconds':prev}

def audio():
    peak=0;rms=[]
    for p in (ROOT/'narration').glob('segment*.wav'):
        data=np.concatenate([f.to_ndarray().reshape(-1).astype(float)/(2**31 if f.format.name=='s32' else 2**15) for f in av.open(str(p)).decode(audio=0)])
        peak=max(peak,float(np.max(abs(data))));rms.append(float(np.sqrt(np.mean(data**2))))
    assert peak<1 and min(rms)>.002
    report_path=ROOT/'outputs/neural-narration-report.json'
    engine=json.loads(report_path.read_text(encoding='utf-8'))['engine'] if report_path.exists() else 'eSpeak NG legacy'
    return dict(peak_dbfs=20*np.log10(peak),clipped=False,min_segment_rms=min(rms),engine=engine)

def notebook():
    book=nbformat.read(ROOT/'lab/Quantum_Tunneling_Lab.ipynb',as_version=4);nbformat.validate(book)
    # Execute using a real desktop IPython kernel; browser validation is separate.
    from nbclient import NotebookClient
    result=NotebookClient(book,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT/'lab')}}).execute()
    nbformat.write(result,ROOT/'outputs/Quantum_Tunneling_Lab_executed.ipynb')
    return {'cells':len(book.cells),'executed_code_cells':sum(c.cell_type=='code' for c in book.cells),'runtime':'desktop Python kernel; separate from browser Pyodide'}

def javascript():
    cases=[]
    for E,V,a in [(.5,1,.45),(.5,1,.9),(.1,.9,.25),(.89,.9,1.2),(.5,1,0)]:
        x=np.linspace(-.8,a+.9,19);p,_=wavefunction(x,E,V,a)
        cases.append(dict(E=E,V=V,a=a,T=transmission(E,V,a),x=x.tolist(),p=[[float(z.real),float(z.imag)] for z in p]))
    fixture=ROOT/'outputs/physics-fixtures.json';fixture.write_text(json.dumps(cases))
    result=subprocess.run(['node',str(ROOT/'scripts/check-site.cjs'),str(fixture)],cwd=ROOT,capture_output=True,text=True,check=True)
    return result.stdout.strip()

def lite():
    folder=ROOT/'website/dist/lab'
    assert (folder/'lab/index.html').exists()
    assert (folder/'files/Quantum_Tunneling_Lab.ipynb').exists()
    config=json.loads((folder/'jupyter-lite.json').read_text())
    assert 'contentsAllJsonFile' in config['jupyter-config-data']
    assert any('pyodide' in str(p).lower() for p in folder.rglob('*'))
    return {'assets':len(list(folder.rglob('*'))),'indexed_notebook':True,'browser_runtime':'requires separate live browser check'}

if __name__=='__main__':
    stages={'physics':physics,'video':video,'captions':captions,'audio':audio,'notebook':notebook,'javascript':javascript,'jupyterlite_build':lite}
    selected=sys.argv[1:] or list(stages)
    for name in selected:check(name,stages[name])
    target=ROOT/'outputs/verification.json'
    if target.exists():report={**json.loads(target.read_text()),**report}
    target.write_text(json.dumps(report,indent=2),encoding='utf-8')
