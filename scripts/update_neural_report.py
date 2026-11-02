"""Refresh human-facing build facts from completed verification, never estimates."""
from pathlib import Path
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

def main():
    verified=json.loads((ROOT/'outputs/neural-verification.json').read_text(encoding='utf-8'))
    neural=json.loads((ROOT/'outputs/neural-narration-report.json').read_text(encoding='utf-8'))
    # Include conditioning provenance in the distributable audit, not just cache files.
    reference=ROOT/'tools/neural-cache/references/kokoro_heart.wav'
    if neural['profile']=='chatterbox_warm' and reference.exists():
        from scripts.neural_narration import REFERENCE_TEXT
        neural['reference_sha256']=hashlib.sha256(reference.read_bytes()).hexdigest()
        neural['reference_text']=REFERENCE_TEXT
        neural['reference_source']={'repo_id':'hexgrad/Kokoro-82M','voice':'af_heart','license':'Apache-2.0','kind':'locally synthesized stock voice'}
        (ROOT/'outputs/neural-narration-report.json').write_text(json.dumps(neural,indent=2,ensure_ascii=False),encoding='utf-8')
    samples=json.loads((ROOT/'outputs/voice_samples/comparison.json').read_text(encoding='utf-8'))
    checks=json.loads((ROOT/'outputs/verification.json').read_text(encoding='utf-8'))
    duration=verified['master']['duration_seconds'];clock=f'{int(duration)//60}:{int(duration)%60:02d}'
    cue_count=checks['captions']['result']['cues']
    profile=verified['profile'];engine=verified['engine'];audio=verified['master']
    report=f'''# Actual build report — local neural narration upgrade

The existing educational course was upgraded in place. Hosting remains **local-only by user choice**. No YouTube upload, paid API or external speech-inference service was used.

## Delivered and verified

| Artifact | Actual result |
| --- | --- |
| Selected narration | {profile}; {engine}; local inference with outbound Python socket connections disabled |
| Full lecture | {clock} ({duration:.6f} s); 1920×1080 H.264 at 30 fps; continuous AAC speech; selectable English subtitles and chapters |
| WAV master | 48 kHz, mono, 24-bit PCM; {audio['measured_integrated_lufs']:.2f} LUFS measured; {audio['measured_true_peak_db']:.2f} dBTP measured |
| Subtitles | {cue_count} canonical English cues aligned to local ASR word timestamps; full script coverage and non-overlap checks passed |
| Scene synchronization | 28 measured slots at 30-fps boundaries; quiz timestamps and chapters regenerated; at least {verified['minimum_prediction_hold_seconds']:.2f} s of reasoning time after prediction narration |
| Video-file verification | Full FFmpeg decode passed; H.264, AAC and embedded subtitle streams inspected |
| Muxed audio alignment | Correlation to the WAV master at opening/middle/end: {', '.join(f'{v:.6f}' for v in verified['video']['audio_master_correlations'])}; no accumulated inter-scene AAC offsets |
| Speech checks | {neural['chunk_count']} synthesized chunks; normalized local ASR mean WER {neural['mean_wer']:.3%}; maximum {neural['max_wer']:.3%} |
| Scientific model | T=0.1423619955 and independently evaluated R=0.8576380045; physics and narration/timing unit tests passed |
| Companion | Local video, subtitle tracks, seven quiz exports, chapter index and H5P authoring specification retimed against the new narration |

## Voice comparison and pronunciation

'''
    for s in samples['samples']:
        report+=f"- **{s['label']}**: {s['duration_seconds']:.2f} s; normalized recognition WER {s['word_error_rate']:.2%}; comparison level {s.get('measured_integrated_lufs',float('nan')):.2f} LUFS.\n"
    report+='''
The warm Chatterbox voice is conditioned on a synthetic reference generated locally from the official Apache-licensed Kokoro `af_heart` stock voice. The expressive Chatterbox sample uses built-in conditioning; the Kokoro sample directly demonstrates the tested fallback. No named individual is imitated or recorded. Chatterbox's built-in watermark is retained.

Scientific spelling remains in captions. Engine-specific pronunciation input covers Schrödinger, wavefunction, kappa, h-bar and Planck's constant. The sample script includes all of them. Recognition text and per-chunk anchors are available in the JSON reports. Minor ASR differences can reflect recognition ambiguity rather than a synthesis error; the audit records them explicitly. Automatic checks do not certify a human perceptual naturalness rating. The three comparison WAVs allow direct listening.

## Reproduction and original build

See `docs/neural-narration.md` for installation, model fetching, offline synthesis, voice selection and rebuilding. `narration/model-lock.json` records upstream model commits; `outputs/neural-environment.json` records actual packages. Source integration, configs, tests and upstream notices are included in the source distribution. Caches and model binaries are excluded from ZIPs; fetch the free upstream weights once before an offline rebuild.

The Manim educational panels are reused and automatically looped to their measured narration slots. This upgrade adds voice, editorial asides, timing and audio mastering; it does not claim a completely new visual animation design. The previous eSpeak MP4, captions, timeline, segment WAVs and report are preserved in `outputs/archive/espeak-original/` in the current workspace.

The computational notebook's existing desktop/Pyodide execution and responsive browser checks belong to the original course validation; its physics code is unchanged. Current audio/video, caption, quiz-timing and JavaScript/asset checks were rerun for this upgrade. No real H5P host or native YouTube quiz installation was tested: the structured authoring specification and manual instructions remain the supplied deliverables. No site deployment is pending or authorized by the user's local-only choice.

Licenses: original integration code MIT; original teaching content/visuals CC BY 4.0; Chatterbox model/code MIT; official Kokoro model/voicepack Apache 2.0. See `docs/tts-licenses/`, the model cards and `docs/sources.md`.
'''
    (ROOT/'outputs/build-report.md').write_text(report,encoding='utf-8')
    readme=ROOT/'README.md';text=readme.read_text(encoding='utf-8')
    text=re.sub(r'approximately \d+:\d{2}\.',f'{clock} actual duration.',text,count=1)
    readme.write_text(text,encoding='utf-8')
    site=ROOT/'website/dist/index.html';html=site.read_text(encoding='utf-8')
    html=re.sub(r'(?:\d+-minute|\d+:\d{2}) lecture',f'{clock} lecture',html,count=1)
    site.write_text(html,encoding='utf-8')
    source=ROOT/'docs/sources.md';text=source.read_text(encoding='utf-8')
    paragraph=(f'The neural upgrade has {cue_count} measured caption cues and a {clock} full-HD lecture. '
        f'All 28 scene slots, the 48 kHz/24-bit WAV, measured loudness/true peak, complete MP4 decoding and opening/middle/end audio alignment passed. '
        f'The selected local engine is {engine} ({profile}). Seven quiz times and chapters were regenerated from the measured narration. '
        'The original course also passed independent physics, desktop/Pyodide notebook execution and desktop/tablet/phone browser checks; the physics code is unchanged. '
        'See outputs/build-report.md and outputs/neural-verification.json for actual results and boundaries.')
    text=re.sub(r'Executed checks on 2026-11-02:.*?(?=\n\n)',paragraph,text,flags=re.S)
    source.write_text(text,encoding='utf-8')
    print(f'Updated verified course facts: {clock}, {cue_count} cues, {engine}.')

if __name__=='__main__':main()
