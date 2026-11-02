> Historical local rendering guide. Public deployment instructions and current hosting status are in [github-pages.md](github-pages.md). Generated MP4/WAV masters are local artifacts and are excluded from GitHub.

# Can an Electron Pass Through a Wall?

An implemented open educational course for applied quantum mechanics, materials science, physics and electronic engineering. The finite-barrier calculation uses E=0.50 eV, V0=1.00 eV, a=0.45 nm and free-electron mass by default: **T=0.1423619955**, **R=0.8576380045**. This is a stationary 1D elastic model with identical leads, not a particle trajectory or a full device transport model.

The neural narration upgrade is implemented in `scripts/neural_narration.py`: local Chatterbox, a tested Kokoro-82M fallback, three comparison samples, scientific pronunciation overrides, word-timed captions and continuous-master audio/video assembly. Read `docs/neural-narration.md` for the isolated speech-environment setup and rebuild commands. No paid service is used. Public hosting is configured separately in the Pages workflow.

## Start with the finished artifacts

- `outputs/Quantum_Tunneling_Lecture.mp4`: 1920×1080, 30 fps, H.264/yuv420p, AAC narration; 11:54 actual duration. Generated from 28 Manim CE panels, with real equations, wavefunctions, densities, energy diagrams, parameter scans, STM and interface illustrations, and seven prediction pauses.
- `outputs/Quantum_Tunneling_Narration.wav`: mastered 48 kHz, 24-bit PCM speech. `outputs/voice_samples/` contains three comparison WAVs and a browser player.
- `narration/lecture.srt`, `narration/transcript.md`, `narration/timeline.json`: timed English subtitles, narration transcript and actual timeline. Local neural AI narration; no real person's voice recording or music.
- `video/scenes.py`, `course/physics.py`, `tests/test_physics.py`: editable Manim source, stable exact model, independent boundary-matching/ODE calculations and tests.
- `outputs/thumbnail.png`, `outputs/youtube_description.md`, `quizzes/youtube_quizzes.csv`, `quizzes/youtube_quizzes.md`: upload artwork, title/description/actual chapters and seven native quiz editorial entries.
- `h5p/authoring.json`, `docs/h5p-guide.md`: fully structured H5P authoring specification and precise Lumi/Moodle workflow. **This JSON is not an importable .h5p package.** No authoring host is connected; import/playback/reporting must be tested there. See `h5p/host-validation.csv`.
- `lab/Quantum_Tunneling_Lab.ipynb`: independent executable notebook; `lab/files/` is its JupyterLite content source; `lab/jupyter_lite_config.json` and `requirements-lite.txt` define the browser build.
- `website/dist/`: responsive companion with an exact interactive simulation, chapter player, feedback questions, browser lab launcher, assessment and H5P guide. `interactive.html` is a working local HTML timed-question player, separate from H5P.
- `docs/assessment.md`: pretest, posttest, 14-day retention assessment, unfamiliar transfer problem, independent assignment and five separate rubric scores.
- `outputs/verification.json`: executed automated checks. `outputs/build-report.md` records browser/host limits and publication state.

## View locally

Use HTTP, not a `file://` page, so JavaScript data, workers, captions and JupyterLite can load. In a terminal from this folder:

```powershell
python scripts/serve.py
```

Open `http://127.0.0.1:8765/`. The lab launch URL is `http://127.0.0.1:8765/lab/lab/index.html?path=Quantum_Tunneling_Lab.ipynb`. Its first launch needs network access to Pyodide/packages. Students edit the parameter cell and rerun; notebook widgets are deliberately omitted. Download completed work because notebook edits live in the browser's origin-specific storage. Desktop Jupyter is an alternative when browser runtime access is blocked.

## Windows installation and rebuild

Python 3.12 is recommended. Install Git and a supported Python distribution. Manim CE's Cairo/Pango dependencies are available as wheels for this tested Windows/Python combination; if another platform lacks wheels, follow the official Manim installation instructions.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --timeout 180 -r requirements.txt
```

Install the separate neural speech environment using `docs/neural-narration.md`, fetch the free models once, and generate the comparison samples. Then build with:

```powershell
.\.venv\Scripts\python.exe build.py all
.\.venv\Scripts\python.exe scripts/verify.py
.\.venv-tts\Scripts\python.exe scripts/verify_neural.py
```

Rendering uses Manim CE and mathtext, so TeX is not required. The FFmpeg executable comes from `imageio-ffmpeg` if FFmpeg is not on PATH. `ffprobe` is not required; media metadata is inspected with PyAV and the complete file is decoded with FFmpeg. Explicit `build.py audio-espeak` retains the old baseline for comparison, archived in `outputs/archive/espeak-original`; it is not the neural fallback.

## Linux installation and rebuild

On Debian/Ubuntu, install the relevant system packages (these commands require normal administrator privileges):

```bash
sudo apt update
sudo apt install python3-venv python3-dev build-essential pkg-config libcairo2-dev libpango1.0-dev ffmpeg espeak-ng fonts-dejavu-core
python3 -m venv .venv
.venv/bin/python -m pip install --timeout 180 -r requirements.txt
# Set up .venv-tts and fetch its free checkpoints as documented first.
.venv/bin/python build.py all
.venv/bin/python scripts/verify.py
.venv-tts/bin/python scripts/verify_neural.py
```

For Linux, the build must not override eSpeak's packaged system data directory with `/usr/bin`; set `ESPEAK_DATA_PATH` only if you intentionally use a portable data directory. `build.py` detects adjacent portable data. Confirm your distribution's supported dependencies against official Manim docs. Linux commands/configuration are supplied; this delivery was actually rendered on Windows.

## Build stages and reproducibility

```text
python build.py assets       # mathtext equations and original thumbnail
python build.py voices       # three local voice comparisons
python build.py audio        # neural WAV master/segments, ASR word anchors and timeline
python scripts/author.py     # quizzes, H5P specification, notebook and publication text
python scripts/docs_site.py # render educational guides into the website
python build.py smoke        # one full-HD Manim render
python build.py render       # all 28 Manim panels, 4 s per seamless loop
python build.py video        # loop each panel to its measured narration segment and compose MP4
python build.py lite         # indexed browser notebook + Pyodide kernel extension
python scripts/verify.py     # physics, full decode, caption coverage, audio, JS, notebook, Lite assets
```

`python build.py all` runs all build stages. Content lives in `course/lesson.py`; update it there, then regenerate the audio, editorial exports and video together. Neural caption cues use local ASR word timestamps matched back to the edited scientific script. Actual narration durations determine chapter and quiz times, with explicit reasoning pauses. The composer loops the existing mathematically consistent animations to fill each measured panel and encodes the continuous audio master once. Parameter sweeps compare stationary solutions, rather than simulate physical wall motion. No synthetic experimental dataset is presented as measured evidence.

Run `python scripts/package.py` to produce source and publication ZIPs after verification. The source archive excludes local virtual environments, engine binaries and build caches. Rebuilding need not be byte-identical across OS/font/FFmpeg versions, but numerical checks and content timing are explicit. `requirements.txt` pins the major rendering and browser components; installed versions are recorded in `outputs/environment.json`.

## GitHub Pages deployment

Use [github-pages.md](github-pages.md) and `.github/workflows/deploy.yml`. The public site streams YouTube. Do not commit MP4/WAV masters. Native H5P and HTML exports are supplied; see the current H5P guide.

## Upload, author and assess

Follow `docs/youtube-upload.md` to upload the video, captions, artwork and seven native quizzes manually. No API for installing native quizzes is assumed. Follow `docs/h5p-guide.md` to import the supplied native `.h5p`, test YouTube playback in the destination H5P host, and use uploaded MP4/captions if blocked. H5P and JupyterLite are external companion applications; they do not run as arbitrary applications inside YouTube.

Use the five-outcome rubric and original computational work to judge understanding. Quiz completion is only formative practice. No learner account, grades service or tracking database is included in the standalone site; local questions keep state only in memory.

## License

Original code MIT; original educational text and visuals CC BY 4.0. Chatterbox is MIT; Kokoro-82M and the official stock voicepack are Apache 2.0. The warm voice's conditioning reference is synthesized from that licensed stock voice. No named lecturer is imitated. See `docs/neural-narration.md`, `docs/tts-licenses`, `LICENSE`, `CONTENT_LICENSE.md` and `docs/sources.md` for scientific sources and dependency licensing.
