"""Reuse original local masters, record provenance and generate Remotion data."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from course.publication import make_events
from scripts.author import QUIZZES

def main():
    p=argparse.ArgumentParser();p.add_argument('--media-root',type=Path);p.add_argument('--events-only',action='store_true');a=p.parse_args()
    timeline=json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8'))
    candidates=[a.media_root] if a.media_root else [ROOT,ROOT.parent.parent]
    media_root=next((r for r in candidates if r and (r/'outputs/Quantum_Tunneling_Lecture.mp4').exists() and (r/'outputs/Quantum_Tunneling_Narration.wav').exists()),None)
    words_path=ROOT/'course/narration_words.json'
    if media_root and (media_root/'narration/neural').exists():
        words=[]
        for scene in timeline:
            for chunk in scene.get('chunks',[]):
                alignment=media_root/Path(chunk['file'].replace('\\','/')).with_suffix('.json')
                if alignment.exists():
                    for word in json.loads(alignment.read_text(encoding='utf-8'))['asr']['words']:
                        words.append(dict(scene=scene['index'],word=word['word'],start_seconds=scene['start']+chunk['start']+word['start'],end_seconds=scene['start']+chunk['start']+word['end']))
        words_path.write_text(json.dumps(words,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    words=json.loads(words_path.read_text(encoding='utf-8')) if words_path.exists() else []
    events=make_events(timeline,(ROOT/'narration/lecture.srt').read_text(encoding='utf-8'),QUIZZES,words)
    for target in [ROOT/'course/publication_events.json',ROOT/'remotion/src/generated/events.json']:
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(events,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    if a.events_only:
        print('Generated authoritative events:',events['duration_frames'],'frames');return
    if not media_root:raise FileNotFoundError('Supply --media-root pointing to the existing MP4/WAV project, or rebuild the original masters. Never download a substitute from YouTube.')
    public=ROOT/'remotion/public/media';public.mkdir(parents=True,exist_ok=True)
    provenance=[]
    for original,name in [('Quantum_Tunneling_Lecture.mp4','baseline.mp4'),('Quantum_Tunneling_Narration.wav','narration.wav')]:
        source=media_root/'outputs'/original;target=public/name
        if not target.exists() or target.stat().st_size!=source.stat().st_size:shutil.copy2(source,target)
        provenance.append(dict(file=name,source_filename=original,bytes=source.stat().st_size,sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
    (ROOT/'outputs/remotion-media-provenance.json').write_text(json.dumps(dict(media=provenance,original_audio_muted=True,continuous_wav_master=True),indent=2)+'\n',encoding='utf-8')
    print('Prepared original media and',len(events['scenes']),'scenes;',len(events['quizzes']),'prediction holds;',events['duration_frames'],'frames.')

if __name__=='__main__':main()
