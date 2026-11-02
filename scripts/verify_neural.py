"""Verify the actual neural master, captions and final audiovisual timing."""
from pathlib import Path
import json,math,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np,soundfile as sf
import av
from course.lesson import SEGMENTS
from scripts.neural_narration import ffmpeg

def main():
    report=json.loads((ROOT/'outputs/neural-narration-report.json').read_text(encoding='utf-8'))
    timeline=json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8'))
    master=ROOT/'outputs/Quantum_Tunneling_Narration.wav'
    info=sf.info(master);assert info.samplerate==48000 and info.subtype=='PCM_24' and info.channels==1
    data,rate=sf.read(master,dtype='float32');duration=len(data)/rate
    expected=sum(s['duration'] for s in timeline);assert abs(duration-expected)<1/rate+.00001
    assert np.all(np.isfinite(data)) and np.max(abs(data))<1
    for s in timeline:
        info_seg=sf.info(ROOT/f'narration/segment{s["index"]:02d}.wav')
        assert info_seg.samplerate==rate and info_seg.subtype=='PCM_24'
        assert abs(info_seg.duration-s['duration'])<1/rate+.00001
        assert s['speech_end']<s['start']+s['duration']
        if s['kind']=='predict':assert s['start']+s['duration']-s['speech_end']>=6.49
    # Derive measured loudness and true peak from the final PCM file, not config.
    loud=subprocess.run([ffmpeg(),'-hide_banner','-i',str(master),'-af','loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    measured=json.loads(re.findall(r'\{[^{}]+"input_i"[^{}]+\}',loud.stderr,re.S)[-1])
    assert abs(float(measured['input_i'])+16)<.6
    assert float(measured['input_tp'])<=-1.35
    # Entire MP4 decode, dimensions, audio and optional subtitle track.
    video=ROOT/'outputs/Quantum_Tunneling_Lecture.mp4';c=av.open(str(video));v=c.streams.video[0];a=c.streams.audio[0]
    assert (v.width,v.height)==(1920,1080) and v.codec_context.name=='h264' and v.average_rate==30
    assert a.codec_context.name=='aac' and a.codec_context.sample_rate==48000
    assert c.streams.subtitles and c.streams.subtitles[0].codec_context.name=='mov_text'
    assert abs(c.duration/1e6-duration)<.08
    assert abs(float(v.duration*v.time_base)-duration)<.05
    subprocess.run([ffmpeg(),'-hide_banner','-loglevel','error','-xerror','-i',str(video),'-f','null','-'],check=True)
    # Check actual muxed audio follows the master without accumulating clip offsets.
    decoded=np.concatenate([f.to_ndarray().reshape(-1) for f in av.open(str(video)).decode(audio=0)])
    correlations=[]
    for position in [.5,duration*.5,duration-6]:
        start=round(position*rate);n=rate*3
        x=data[start:start+n];y=decoded[start:start+n]
        assert len(x)==len(y)==n
        value=float(np.corrcoef(x,y)[0,1]);assert value>.98;correlations.append(value)
    sample_report=json.loads((ROOT/'outputs/voice_samples/comparison.json').read_text(encoding='utf-8'))
    assert len(sample_report['samples'])==3
    for s in sample_report['samples']:
        sample=sf.info(ROOT/s['file']);assert sample.subtype=='PCM_24' and sample.samplerate==24000
    result={'status':'PASS','profile':report['profile'],'engine':report['engine'],
        'master':{'sample_rate':rate,'bit_depth':24,'channels':1,'duration_seconds':duration,'measured_integrated_lufs':float(measured['input_i']),'measured_true_peak_db':float(measured['input_tp'])},
        'video':{'size':[v.width,v.height],'fps':30,'codec':'H.264','audio':'AAC 48 kHz','embedded_subtitles':'English mov_text','complete_decode':True,'audio_master_correlations':correlations},
        'samples':3,'scenes':len(timeline),'minimum_prediction_hold_seconds':min(s['start']+s['duration']-s['speech_end'] for s in timeline if s['kind']=='predict'),
        'speech_audit':{'chunks':report['chunk_count'],'mean_word_error_rate':report['mean_wer'],'max_word_error_rate':report['max_wer']},
        'perceptual_limit':'Automatic intelligibility and signal checks are not a human listening study or a certified naturalness rating.'}
    (ROOT/'outputs/neural-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
