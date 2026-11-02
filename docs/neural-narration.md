# Local neural narration: Chatterbox with Kokoro fallback

This project now has a separate speech environment so PyTorch/NumPy requirements do not disturb the working Manim/JupyterLite environment. All speech inference and verification run locally. Initial installation downloads free packages and model weights; no paid API, subscription, account or uploaded voice recording is required. The existing eSpeak version is archived under `outputs/archive/espeak-original/` when neural generation first runs.

## Install

Use Python 3.12 on the tested Windows computer. The installed NVIDIA RTX 4050 has 6 GB VRAM. Chatterbox's original English model is the primary engine; Kokoro-82M is the configured fallback.

```powershell
python -m venv .venv-tts
.\.venv-tts\Scripts\python.exe -m pip install --timeout 180 torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
.\.venv-tts\Scripts\python.exe -m pip install --timeout 180 -r requirements-neural.txt
.\.venv-tts\Scripts\python.exe -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
.\.venv-tts\Scripts\python.exe scripts/neural_narration.py fetch
```

Linux: create `.venv-tts` with `python3 -m venv`, use `.venv-tts/bin/python`, and use the appropriate official PyTorch CUDA wheel index for your hardware, or its CPU build. Linux commands are instructions, not a claim that this Windows build was tested on Linux. `NEURAL_PYTHON` can point the Manim build to a different speech-environment interpreter. CPU inference is supported, but may be slower.

`fetch` records exact Hugging Face commit hashes and local snapshot paths in `narration/model-lock.json`, preserves those revisions on subsequent fetches, caches first-use components, and saves upstream license evidence. On another computer, run fetch to resolve those same revisions to new local paths. Caches are under `tools/neural-cache`, excluded from source distributions.

`requirements-neural-lock.txt` records the actual complete speech environment, including the official English model wheel. For a closer rebuild, first install the matching CUDA PyTorch build as above, then install that lock file. Choose an appropriate PyTorch build for a different platform; identical numerical/audio bytes across hardware are not promised.

## Compare, select and generate

```powershell
.\.venv-tts\Scripts\python.exe scripts/neural_narration.py samples
.\.venv-tts\Scripts\python.exe scripts/neural_narration.py render
.\.venv\Scripts\python.exe scripts/author.py
.\.venv\Scripts\python.exe build.py video
```

`python build.py voices` and `python build.py audio` also invoke the isolated speech environment automatically. `python build.py all` uses neural narration by default. Explicit `audio-espeak` is retained only for the old reproducible baseline; neural generation does not silently substitute that voice.

After installation/fetch, **`python build.py narrate`** runs the full upgrade: comparison samples, cached/rechecked narration, retimed quizzes/chapters, continuous-master MP4, automated verification, reports and ZIPs. It preserves the existing computational notebook and reuses existing Manim panels, rendering them only if missing.

Three 24-bit WAV samples use the same script, including curiosity, a prediction prompt, Schrödinger, wavefunction, kappa, Planck's constant and an energy-conservation reveal:

1. **Warm lecturer:** Chatterbox conditioned on a locally generated, Apache-licensed Kokoro Heart stock-voice reference, with moderate expressiveness and deliberate guidance.
2. **Curious storyteller:** Chatterbox's built-in voice with a more expressive delivery for comparison.
3. **Kokoro Heart:** the official Apache-licensed `af_heart` voicepack, a calm English fallback.

These are generic model voices, not an attempt to imitate a named lecturer. The warm and fallback samples compare two models using the same licensed stock-voice family; they are not three claims of distinct human identities. Listen to `outputs/voice_samples/*.wav`; see `comparison.json`. Word-error rates screen intelligibility and hallucinations; they are **not** objective ratings of human naturalness. The default editorial preference is the warm reading, subject to intelligibility checks. Change `selected_profile` in `narration/voice-config.json` to choose another. If Chatterbox cannot load or a synthesis stage fails, the runner logs that failure and attempts the configured Kokoro fallback for the lecture.

## Scientific pronunciation and delivery

Canonical captions retain scientific spelling. The pronunciation dictionary changes only model input: Chatterbox receives phonetic respellings where needed; Kokoro receives Misaki phoneme overrides. “Schrödinger” uses an English SHROH-ding-er reading; “wavefunction” is voiced as “wave function”; kappa is KAP-uh; Planck's is PLANKS. The spoken lesson explicitly explains that h-bar is Planck's constant divided by two pi.

Question marks guide interrogative intonation. Prediction scenes receive a restrained expressiveness increase and at least 6.5 seconds of reasoning silence after the spoken question. Paragraph/sentence boundaries supply shorter pauses. There are no artificial cough/laugh effects or unsupported SSML tags. Long explanations are synthesized in coherent sentence groups rather than arbitrary caption-width fragments.

## Synchronization and mastering

Each synthesized chunk is cached by canonical text, pronunciation dictionary, model revision, voice parameters and seed. Local faster-whisper transcribes it and produces word timestamps. The pipeline retries high-error chunks, matches the edited script to those timestamps, and writes canonical SRT cues. Interpolated unmatched ASR words are recorded through anchor counts; the transcript is never rewritten to match an ASR physics mistake.

The measured speech durations set each scene's start/end, rounded up to 30-fps boundaries. Scenes extend when needed; speech is not artificially accelerated to satisfy an old timestamp. Prediction holds remain after the narration. Re-running `scripts/author.py` regenerates quiz times, chapters and H5P authoring data against the new timeline. The existing native Manim animation loops fill each measured slot. This synchronizes narration to its teaching panel; it is not a newly animated derivation or a time-resolved electron trajectory.

The complete narration is mastered once using two-pass EBU R128 normalization, nominal −16 LUFS with −1.5 dB true-peak headroom, then delivered as **48 kHz, mono, 24-bit PCM WAV**. Native model synthesis is 24 kHz; upsampling does not invent higher-frequency source detail. Segment WAVs are cut from that same mastered file. The final MP4 encodes the continuous master once as AAC, avoiding seams from concatenating separate AAC tracks. Its visual frames are restamped and encoded as constant 30-fps H.264 with a fixed track timescale, preventing fractional-frame drift and chapter-timestamp overflow from concatenated MP4 segments. The MP4 includes selectable English subtitles and chapters, and the standalone SRT remains the YouTube upload master.

## Verification and limits

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/verify.py physics video captions audio javascript
.\.venv-tts\Scripts\python.exe scripts/verify_neural.py
```

The neural audit checks actual model/sample execution, independent speech recognition, waveform/format/loudness, segment bounds, subtitle coverage, scene timing, prediction holds and complete video decoding. See the generated neural report for actual results. Automated checks cannot certify that every listener will find a voice convincingly human; the three samples allow direct comparison. No YouTube upload, hosting deployment or H5P host test is performed by this upgrade. Public GitHub Pages deployment is handled by the separate workflow in `.github/workflows/deploy.yml`; see [github-pages.md](github-pages.md).

## Licensing

- [Chatterbox code](https://github.com/resemble-ai/chatterbox) and [official checkpoint](https://huggingface.co/ResembleAI/chatterbox): MIT. The expressive sample uses built-in conditioning; the selected warm profile uses a synthetic reference generated locally from the official Kokoro `af_heart` voicepack. Its source text and SHA-256 are recorded. Chatterbox's built-in audio watermark is retained.
- [Kokoro-82M checkpoint and official voicepacks](https://huggingface.co/hexgrad/Kokoro-82M): Apache 2.0. Its model card documents its training-data and attribution notices; saved under `docs/tts-licenses/`.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper): local ASR for verification, not a narration service. The downloaded OpenAI Whisper-derived model has its upstream license.
- eSpeak NG is used by Kokoro only for out-of-dictionary phonemization. Its GPL software license remains separate; it is not the final speech synthesizer in the neural build.

Retain upstream notices when redistributing model/software binaries. This project distributes generated teaching assets and integration code; model caches and environment binaries are not embedded in its course ZIPs. Original course code remains MIT and original lesson content/visuals remain CC BY 4.0.
