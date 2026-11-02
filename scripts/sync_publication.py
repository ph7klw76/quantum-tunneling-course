"""Generate every publication time from one frame manifest, optionally verifying a final render."""
import argparse
from datetime import timedelta
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import srt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from course.publication import make_events
from scripts.author import QUIZZES,main as author

def main():
    p=argparse.ArgumentParser();p.add_argument('--render',type=Path);p.add_argument('--rebuild-h5p',action='store_true');a=p.parse_args()
    baseline=json.loads((ROOT/'course/publication_baseline.json').read_text(encoding='utf-8'))
    timeline=json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8'))
    words=json.loads((ROOT/'course/narration_words.json').read_text(encoding='utf-8'))
    events=make_events(timeline,(ROOT/'narration/lecture.srt').read_text(encoding='utf-8'),QUIZZES,words)
    actual=None
    if a.render:
        import av
        container=av.open(str(a.render));video=container.streams.video[0]
        assert (video.width,video.height)==(1920,1080) and video.average_rate==30 and video.frames==events['duration_frames']
        assert abs(container.duration/1e6-events['duration_seconds'])<1/30
        actual=dict(file=a.render.name,frames=video.frames,duration_seconds=container.duration/1e6,codec=video.codec_context.name,bytes=a.render.stat().st_size)
    for target in [ROOT/'course/publication_events.json',ROOT/'remotion/src/generated/events.json']:
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(events,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    author(skip_notebook=True)
    cues=[srt.Subtitle(index=i+1,start=timedelta(seconds=c['start_seconds']),end=timedelta(seconds=c['end_seconds']),content=c['text']) for i,c in enumerate(events['captions'])]
    captions=srt.compose(cues)
    def stamp(value):
        ms=round(value*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000)
        return f'{h:02}:{m:02}:{sec:02}.{ms:03}'
    vtt='WEBVTT\n\n'+'\n\n'.join(f"{stamp(c['start_seconds'])} --> {stamp(c['end_seconds'])}\n{c['text']}" for c in events['captions'])+'\n'
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    for target in [ROOT/'narration/lecture.srt',ROOT/'website/dist/lecture.srt',out/'Quantum_Tunneling_Lecture_Remotion.srt']:target.write_text(captions,encoding='utf-8')
    for target in [ROOT/'website/dist/lecture.vtt',out/'Quantum_Tunneling_Lecture_Remotion.vtt']:target.write_text(vtt,encoding='utf-8')
    metadata=[';FFMETADATA1'];chapter_lines=[]
    for i,c in enumerate(events['chapters']):
        end=events['chapters'][i+1]['start_frame'] if i+1<len(events['chapters']) else events['duration_frames']
        metadata.extend(['[CHAPTER]','TIMEBASE=1/30',f"START={c['start_frame']}",f'END={end}',f"title={c['title']}"])
        second=round(c['start_seconds']);chapter_lines.append(f'{second//60:02}:{second%60:02} '+c['title'])
    (out/'chapters.ffmetadata').write_text('\n'.join(metadata)+'\n',encoding='utf-8')
    (out/'chapters_polished.txt').write_text('\n'.join(chapter_lines)+'\n',encoding='utf-8')
    description=(out/'youtube_description.md').read_text(encoding='utf-8')
    before,after=description.split('CHAPTERS\n',1);_,tail=after.split('\n\n',1)
    (out/'youtube_description_polished.md').write_text(before.replace('Quantum Tunneling Explained','Quantum Tunneling — Polished Applied Quantum Lab')+'CHAPTERS\n'+'\n'.join(chapter_lines)+'\n\n'+tail,encoding='utf-8')
    cfg=json.loads((ROOT/'course/publication_config.json').read_text(encoding='utf-8'))
    (ROOT/'website/dist/config.js').write_text('window.COURSE_CONFIG='+json.dumps(dict(youtubeUrl=cfg['active_youtube_url'],h5pUrl='h5p/quantum-tunneling.html',repositoryUrl=cfg['repository_url']),separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
    rows=[]
    for old,new in zip(baseline['quizzes'],events['quizzes']):
        delta=new['time_seconds']-old['time_seconds'];assert delta==0,'Preserve mode cannot silently move a quiz'
        assert 6<=new['reasoning_silence_seconds']<=10
        rows.append(dict(id=new['id'],old_seconds=old['time_seconds'],new_seconds=new['time_seconds'],delta_seconds=delta,remediation_old=old['remediation_seconds'],remediation_new=new['remediation_seconds'],silence_seconds=new['reasoning_silence_seconds'],answer_reveal_seconds=new['answer_reveal_frame']/30))
    assert events['duration_frames']==baseline['duration_frames']
    report=dict(status='PASS' if actual else 'PREPARED_NOT_RENDER_VERIFIED',mode='preserve',render=actual,source_duration_frames=baseline['duration_frames'],final_duration_frames=events['duration_frames'],duration_delta_frames=0,scenes=len(events['scenes']),narration_chunks=len(events['narration']),subtitle_cues=len(cues),canonical_caption_coverage=True,word_aligned_highlights=len(events['highlight_beats']),quizzes=rows,chapters=events['chapters'],active_video_url=cfg['active_youtube_url'],polished_video_uploaded=bool(cfg['polished_youtube_url']),notes=['YouTube chapter display times round to the nearest second; video and H5P use precise frames.','This is not evidence of a new YouTube upload.'])
    (out/'remotion-timing-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if a.rebuild_h5p:
        subprocess.run([sys.executable,str(ROOT/'scripts/author_h5p.py')],cwd=ROOT,check=True)
        node=os.environ.get('NODE_BINARY') or shutil.which('node')
        if not node:raise RuntimeError('Put Node on PATH or set NODE_BINARY')
        subprocess.run([node,str(ROOT/'webtools/h5p-build.cjs')],cwd=ROOT,check=True)
    # Content hashes give returning learners the matching URL/config/export revision.
    index_path=ROOT/'website/dist/index.html';index=index_path.read_text(encoding='utf-8')
    for resource in ['config.js','h5p/quantum-tunneling.html']:
        digest=hashlib.sha256((ROOT/'website/dist'/resource).read_bytes()).hexdigest()[:12]
        index=re.sub(r'(?<=src=")'+re.escape(resource)+r'(?:\?[^"\s]*)?(?=")',resource+'?v='+digest,index)
    index_path.write_text(index,encoding='utf-8',newline='\n')
    print(json.dumps(dict(status=report['status'],frames=events['duration_frames'],quiz_deltas=[r['delta_seconds'] for r in rows],subtitle_cues=len(cues))))

if __name__=='__main__':main()
