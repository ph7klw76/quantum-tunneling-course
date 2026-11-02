"""Reproducible local build: python build.py assets|audio|render|video|lite|all."""
from pathlib import Path
import argparse,json,os,re,shutil,subprocess,sys,textwrap,wave
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from course.lesson import SEGMENTS,CHAPTERS

def run(args,**kw):
    print('RUN:',*map(str,args),flush=True)
    subprocess.run(list(map(str,args)),cwd=ROOT,check=True,**kw)

def ffmpeg():
    return shutil.which('ffmpeg') or __import__('imageio_ffmpeg').get_ffmpeg_exe()

def stamp(t,srt=False):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}' if srt else f'{m+h*60:02}:{s:02}'

def assets():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from PIL import Image,ImageDraw,ImageFont
    out=ROOT/'outputs/equations';out.mkdir(parents=True,exist_ok=True)
    eqs={'schrodinger':r'$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2}+V(x)\psi=E\psi$',
         'exact':r'$T=\left[1+\frac{V_0^2\sinh^2(\kappa a)}{4E(V_0-E)}\right]^{-1},\quad\kappa=\frac{\sqrt{2m(V_0-E)}}{\hbar}$'}
    for name,eq in eqs.items():
        fig=plt.figure(figsize=(15,2),facecolor='#091522');fig.text(.5,.5,eq,ha='center',va='center',color='white',fontsize=35)
        fig.savefig(out/f'{name}.png',dpi=140,facecolor=fig.get_facecolor(),bbox_inches='tight');plt.close(fig)
    im=Image.new('RGB',(1280,720),'#091522');d=ImageDraw.Draw(im)
    fontpath=Path('C:/Windows/Fonts/arialbd.ttf')
    if not fontpath.exists():fontpath=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
    f=lambda n:ImageFont.truetype(str(fontpath),n)
    d.text((70,50),'CAN AN ELECTRON',font=f(62),fill='#FFFFFF')
    d.text((70,125),'PASS THROUGH A WALL?',font=f(68),fill='#F6C978')
    d.rectangle((570,300,780,610),fill='#4A4334',outline='#F6C978',width=5)
    xs=np.linspace(60,1200,700);ys=[]
    from course.physics import wavefunction
    p,_=wavefunction((xs-570)/470,a=210/470)
    for xx,yy in zip(xs,p.real):ys.append((int(xx),int(460-65*yy)))
    d.line(ys,fill='#63E4DB',width=7)
    d.text((70,620),'QUANTUM TUNNELING  |  PREDICT. TEST. EXPLAIN.',font=f(30),fill='#B6C8D6')
    im.save(ROOT/'outputs/thumbnail.png');im.save(ROOT/'website/dist/thumbnail.png')

def audio_legacy():
    synth=os.environ.get('ESPEAK_BIN') or shutil.which('espeak-ng') or str(ROOT/'tools/espeak/eSpeak NG/espeak-ng.exe')
    if not Path(synth).exists() and not shutil.which(synth):raise RuntimeError('Set ESPEAK_BIN to the offline espeak-ng executable.')
    out=ROOT/'narration';out.mkdir(exist_ok=True)
    speech_env=os.environ.copy()
    if (Path(synth).parent/'espeak-ng-data').is_dir(): speech_env['ESPEAK_DATA_PATH']=str(Path(synth).parent)
    cues=[];timeline=[];clock=0;transcript=[]
    for s in SEGMENTS:
        chunks=[]
        for sent in re.split(r'(?<=[.!?])\s+',s['text']):
            # Each caption is synthesized separately: its true WAV duration anchors sync.
            chunks.extend(textwrap.wrap(sent,105,break_long_words=False,break_on_hyphens=False))
        pieces=[];local=.25;local_cues=[];rate=22050
        for j,chunk in enumerate(chunks):
            target=out/f"{s['index']:02}_{j:02}.wav"
            txt=target.with_suffix('.txt');txt.write_text(chunk,encoding='utf-8')
            subprocess.run([synth,'-v','en-us','-s','165','-p','42','-a','140','-f',str(txt),'-w',str(target)],check=True,stdout=subprocess.DEVNULL,env=speech_env)
            with wave.open(str(target),'rb') as w:
                assert w.getnchannels()==1 and w.getsampwidth()==2
                rate=w.getframerate();raw=w.readframes(w.getnframes());dur=w.getnframes()/rate
            pieces.append(raw);local_cues.append((local,local+dur,chunk));local+=dur
        speech=local
        duration=max(s['duration'],np.ceil((speech+(6 if s['kind']=='predict' else .6))*30)/30)
        with wave.open(str(out/f"segment{s['index']:02}.wav"),'wb') as w:
            w.setparams((1,2,rate,0,'NONE','not compressed'));w.writeframes(b'\0\0'*round(.25*rate))
            for raw in pieces:w.writeframes(raw)
            w.writeframes(b'\0\0'*max(0,round((duration-speech)*rate)))
        cues.extend((clock+a,clock+b,c) for a,b,c in local_cues)
        timeline.append({**s,'start':clock,'duration':duration,'speech_end':clock+speech})
        transcript.append(f"## {stamp(clock)} — {s['title']}\n\n{s['text']}\n")
        clock+=duration
    (out/'timeline.json').write_text(json.dumps(timeline,indent=2),encoding='utf-8')
    (out/'transcript.md').write_text('# Can an Electron Pass Through a Wall?\n\n'+'\n'.join(transcript),encoding='utf-8')
    (out/'lecture.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a,True)} --> {stamp(b,True)}\n'+ '\n'.join(textwrap.wrap(c,53)) for i,(a,b,c) in enumerate(cues))+'\n',encoding='utf-8')
    print(f'Audio duration: {clock:.3f} s; {len(cues)} precisely anchored captions',flush=True)
    if not 600<=clock<=720: raise ValueError('Editorial duration outside the requested 10–12 minute range; adjust narration rate or text.')
    shutil.copy(out/'lecture.srt',ROOT/'website/dist/lecture.srt')

def neural_python():
    configured=os.environ.get('NEURAL_PYTHON')
    if configured:return configured
    path=ROOT/('.venv-tts/Scripts/python.exe' if os.name=='nt' else '.venv-tts/bin/python')
    if not path.exists():raise RuntimeError('Install requirements-neural.txt in .venv-tts, or set NEURAL_PYTHON. See docs/neural-narration.md.')
    return str(path)

def audio():
    run([neural_python(),'scripts/neural_narration.py','render'])

def voices():
    run([neural_python(),'scripts/neural_narration.py','samples'])

def render(smoke=False):
    scenes=['Segment00'] if smoke else [f'Segment{i:02d}' for i in range(len(SEGMENTS))]
    run([sys.executable,'-m','manim','video/scenes.py',*scenes,'--resolution','1920,1080','--fps','30',
         '--media_dir','outputs/manim','--disable_caching','--verbosity','WARNING'])

def compose():
    out=ROOT/'outputs';clips=out/'clips';clips.mkdir(exist_ok=True)
    timeline=json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8'))
    for s in timeline:
        i=s['index'];source=next((out/'manim/videos/scenes').rglob(f'Segment{i:02d}.mp4'))
        target=clips/f'{i:02}.mp4'
        if target.exists() and target.stat().st_mtime>max(source.stat().st_mtime,(ROOT/f'narration/segment{i:02d}.wav').stat().st_mtime):continue
        run([ffmpeg(),'-hide_banner','-loglevel','error','-y','-stream_loop','-1','-i',source,'-i',ROOT/f'narration/segment{i:02d}.wav',
             '-t',str(s['duration']),'-map','0:v:0','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',target])
    listing=clips/'concat.txt';listing.write_text('\n'.join(f"file '{i:02}.mp4'" for i in range(len(timeline))),encoding='utf-8')
    master=out/'Quantum_Tunneling_Narration.wav'
    if not master.exists() or 'voice_profile' not in timeline[0]:
        # Preserve explicit legacy support without reintroducing per-clip AAC gaps.
        wavs=clips/'audio-concat.txt';wavs.write_text('\n'.join("file '"+str(ROOT/f'narration/segment{s["index"]:02d}.wav').replace('\\','/')+"'" for s in timeline),encoding='utf-8')
        run([ffmpeg(),'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',wavs,'-c:a','pcm_s24le','-ar','48000',master])
    metadata=out/'chapters.ffmetadata';lines=[';FFMETADATA1','title=Can an Electron Pass Through a Wall? — Quantum Tunneling Explained']
    for i,title in enumerate(CHAPTERS):
        start=timeline[i*4]['start'];end=timeline[(i+1)*4]['start'] if i<6 else timeline[-1]['start']+timeline[-1]['duration']
        lines.extend(['[CHAPTER]','TIMEBASE=1/1000',f'START={round(start*1000)}',f'END={round(end*1000)}',f'title={title}'])
    metadata.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    run([ffmpeg(),'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',listing,'-i',master,
         '-i',ROOT/'narration/lecture.srt','-f','ffmetadata','-i',metadata,'-map','0:v:0','-map','1:a:0','-map','2:s:0','-map_metadata','3','-map_chapters','3',
         '-vf','setpts=N/(30*TB)','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','30','-fps_mode','cfr','-video_track_timescale','30000',
         '-c:a','aac','-b:a','192k','-c:s','mov_text','-metadata:s:a:0','language=eng','-metadata:s:s:0','language=eng',
         '-movflags','+faststart',out/'Quantum_Tunneling_Lecture.mp4'])
    shutil.copy(out/'Quantum_Tunneling_Lecture.mp4',ROOT/'website/dist/lecture.mp4')
    shutil.copy(ROOT/'narration/lecture.srt',out/'Quantum_Tunneling_Lecture.srt')
    # HTML5 captions require WebVTT, converted from the same timed master.
    run([ffmpeg(),'-hide_banner','-loglevel','error','-y','-i',ROOT/'narration/lecture.srt',ROOT/'website/dist/lecture.vtt'])

def lite():
    run([sys.executable,'-m','jupyterlite_core','build','--lite-dir',ROOT/'lab','--contents','files','--output-dir',ROOT/'website/dist/lab'])

def narrate():
    """One-command upgrade after free checkpoint setup; preserve the existing lab."""
    voices();audio()
    run([sys.executable,'scripts/author.py','--skip-notebook'])
    if not all(any((ROOT/'outputs/manim/videos/scenes').rglob(f'Segment{i:02d}.mp4')) for i in range(len(SEGMENTS))):
        assets();render()
    compose()
    run([sys.executable,'scripts/verify.py','physics','video','captions','audio','javascript'])
    run([neural_python(),'scripts/verify_neural.py'])
    run([sys.executable,'scripts/update_neural_report.py'])
    run([sys.executable,'scripts/docs_site.py'])
    run([sys.executable,'scripts/package.py'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['assets','audio','audio-espeak','voices','narrate','render','smoke','video','lite','all']);a=p.parse_args()
    (ROOT/'website/dist').mkdir(parents=True,exist_ok=True)
    if a.stage=='all':
        assets();audio();run([sys.executable,'scripts/author.py']);run([sys.executable,'scripts/docs_site.py']);render();compose();lite()
    elif a.stage=='smoke':render(True)
    else:{'assets':assets,'audio':audio,'audio-espeak':audio_legacy,'voices':voices,'narrate':narrate,'render':render,'video':compose,'lite':lite}[a.stage]()
