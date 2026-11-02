"""Frame-accurate publication events derived from the measured scientific lesson."""
from __future__ import annotations
import hashlib
import math
from pathlib import Path
import srt
from course.lesson import SEGMENTS, CHAPTERS
from course.physics import transmission, amplitudes, wavefunction
import numpy as np

FPS=30

def to_frame(seconds: float) -> int:
    return round(seconds*FPS)

def make_events(timeline: list[dict], caption_text: str, quiz_definitions: list[tuple], words: list[dict] | None=None) -> dict:
    if len(timeline)!=len(SEGMENTS):raise ValueError('Measured timeline must cover the canonical lesson')
    duration=to_frame(timeline[-1]['start']+timeline[-1]['duration'])
    scenes=[];narration=[]
    for i,(slot,lesson) in enumerate(zip(timeline,SEGMENTS)):
        if slot['index']!=i or slot['text']!=lesson['text']:raise ValueError('Narration and lesson source disagree')
        start=to_frame(slot['start']);end=to_frame(timeline[i+1]['start']) if i+1<len(timeline) else duration
        scenes.append(dict(index=i,title=lesson['title'],focus=lesson['focus'],kind=lesson['kind'],chapter=slot['chapter'],start_frame=start,end_frame=end,duration_frames=end-start,start_seconds=start/FPS,end_seconds=end/FPS,speech_end_seconds=slot['speech_end'],speech_end_frame=math.ceil(slot['speech_end']*FPS)))
        for chunk in slot.get('chunks',[]):
            a=slot['start']+chunk['start'];b=a+chunk['duration']
            narration.append(dict(scene=i,start_seconds=a,end_seconds=b,start_frame=to_frame(a),end_frame=to_frame(b),text=chunk['text']))
    quizzes=[]
    for i,(scene,question,options,correct,explanation,remedial) in enumerate(quiz_definitions):
        slot=timeline[scene];at=float(math.ceil(slot['speech_end']+.2));end=scenes[scene]['end_frame']
        if slot['kind']!='predict' or end/FPS-at<5:raise ValueError('Question must have a genuine prediction hold')
        quizzes.append(dict(id=f'Q{i+1}',scene=scene,time_seconds=at,frame=to_frame(at),question=question,options=options,correct_index=correct,explanation=explanation,remediation_frame=scenes[remedial]['start_frame'],remediation_seconds=round(scenes[remedial]['start_seconds'],2),hold_start_frame=math.ceil(slot['speech_end']*FPS),hold_end_frame=end,reasoning_silence_seconds=end/FPS-slot['speech_end'],answer_reveal_frame=end))
    captions=[]
    for cue in srt.parse(caption_text):
        a=cue.start.total_seconds();b=cue.end.total_seconds()
        if not 0<=a<b<=duration/FPS:raise ValueError('Subtitle outside render bounds')
        captions.append(dict(id=cue.index,start_seconds=a,end_seconds=b,start_frame=math.floor(a*FPS),end_frame=math.ceil(b*FPS),text=cue.content))
    if ' '.join(c['text'] for c in captions).split()!=' '.join(s['text'] for s in timeline).split():raise ValueError('Captions do not cover canonical narration exactly')
    beats=[]
    for scene,key,tokens in [(8,'curvature',['curvature']),(8,'potential',['potential']),(8,'total',['total']),(8,'kappa',['kappa']),(8,'outside',['outside']),(11,'result',['point','0.14','14']),(11,'ensemble',['thousand','10,000','10000','000']),(11,'conservation',['currents'])]:
        word=next((w for w in words or [] if w['scene']==scene and w['word'].lower().strip('.,:;?!') in tokens),None)
        if word:beats.append(dict(scene=scene,key=key,frame=to_frame(word['start_seconds']),source='local ASR word timestamp'))
    _,_,_,t=amplitudes();T=transmission()
    x=np.linspace(-.8,1.35,240);psi,_=wavefunction(x)
    curve=[dict(x=float(a),real=float(b.real),density=float(abs(b)**2)) for a,b in zip(x,psi)]
    return dict(schema_version=1,timing_mode='preserve',fps=FPS,width=1920,height=1080,duration_frames=duration,duration_seconds=duration/FPS,source_caption_sha256=hashlib.sha256(caption_text.encode()).hexdigest(),scenes=scenes,narration=narration,highlight_beats=beats,quizzes=quizzes,chapters=[dict(index=i,title=title,start_frame=scenes[4*i]['start_frame'],start_seconds=scenes[4*i]['start_seconds']) for i,title in enumerate(CHAPTERS)],captions=captions,summary=dict(display_before_end_seconds=3,end_screen_frame=duration-16),laboratory_cta=dict(start_frame=scenes[-1]['start_frame'],end_frame=duration),physics=dict(E_eV=.5,V0_eV=1,a_nm=.45,T=T,R=abs(amplitudes()[0])**2,transmitted_amplitude_abs2=abs(t)**2,doubled_width_nm=.9,T_doubled=transmission(a=.9),wave_samples=curve))
