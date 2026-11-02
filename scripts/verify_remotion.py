"""Decode the actual render and compare its audio with the continuous local WAV."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import av
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--video',type=Path,default=ROOT/'outputs/Quantum_Tunneling_Lecture_Remotion.mp4');p.add_argument('--sample',action='store_true');a=p.parse_args()
    events=json.loads((ROOT/'course/publication_events.json').read_text(encoding='utf-8'))
    video=av.open(str(a.video));stream=video.streams.video[0]
    expected=1800 if a.sample else events['duration_frames']
    assert (stream.width,stream.height)==(1920,1080) and stream.average_rate==30 and stream.frames==expected
    assert stream.codec_context.name=='h264' and stream.codec_context.format.name=='yuv420p'
    assert (stream.codec_context.color_range,stream.codec_context.colorspace,stream.codec_context.color_primaries,stream.codec_context.color_trc)==(1,1,1,1),'Expected limited-range BT.709 delivery'
    assert len(video.streams.audio)==1 and video.streams.audio[0].codec_context.name=='aac'
    assert abs(video.duration/1e6-expected/30)<1/30
    chapters=video.chapters();embedded_captions=0
    if not a.sample:
        assert len(chapters)==len(events['chapters'])
        for chapter,event in zip(chapters,events['chapters']):
            assert abs(float(chapter['start']*chapter['time_base'])-event['start_seconds'])<1/30
            assert chapter['metadata']['title']==event['title']
        assert len(video.streams.subtitles)==1 and video.streams.subtitles[0].metadata['language']=='eng'
        # mov_text includes empty packets for gaps, so compare only visible cues.
        text=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(a.video),'-map','0:s:0','-c:s','srt','-f','srt','-'],capture_output=True,check=True).stdout.decode('utf-8-sig')
        import srt
        extracted=list(srt.parse(text));assert [c.content for c in extracted]==[c['text'] for c in events['captions']]
        for cue,event in zip(extracted,events['captions']):
            assert abs(cue.start.total_seconds()-event['start_seconds'])<.005 and abs(cue.end.total_seconds()-event['end_seconds'])<.005
        embedded_captions=len(extracted)
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg,'-v','error','-xerror','-i',str(a.video),'-f','null','-'],check=True)
    master=ROOT/'remotion/public/media/narration.wav'
    def audio(path,at):
        r=subprocess.run([ffmpeg,'-v','error','-ss',str(at),'-i',str(path),'-t','4','-map','0:a:0','-ar','48000','-ac','1','-f','f32le','-'],capture_output=True,check=True)
        return np.frombuffer(r.stdout,dtype=np.float32).astype(float)
    correlations=[]
    for at in ([5,30,55] if a.sample else [5,350,695]):
        x,y=audio(a.video,at),audio(master,at);n=min(len(x),len(y));x=x[:n];y=y[:n]
        correlations.append(float(np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))))
    assert min(correlations)>.995,'Rendered audio is misaligned or mixed with duplicate narration'
    meter=subprocess.run([ffmpeg,'-hide_banner','-i',str(a.video),'-af','loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    start=meter.stderr.rfind('{');measurements=json.JSONDecoder().raw_decode(meter.stderr[start:])[0]
    assert -17.2<float(measurements['input_i'])<-15.2 and float(measurements['input_tp'])<-1
    result=dict(status='PASS',edition='sample' if a.sample else 'full',file=a.video.name,frames=stream.frames,duration_seconds=video.duration/1e6,resolution=[1920,1080],fps=30,codec='H.264/AAC',pixel_format='yuv420p',color_space='limited BT.709',audio_tracks=1,chapters=len(chapters),embedded_caption_cues=embedded_captions,full_decode=True,audio_correlations=correlations,integrated_lufs=float(measurements['input_i']),true_peak_db=float(measurements['input_tp']))
    name='remotion-sample-verification.json' if a.sample else 'remotion-video-verification.json'
    (ROOT/'outputs'/name).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))

if __name__=='__main__':main()
