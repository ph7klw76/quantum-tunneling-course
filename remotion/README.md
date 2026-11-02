# Quantum Tunneling Remotion production

This React/TypeScript workspace polishes the existing Manim lecture without changing its scientific timeline. It has editable `QuantumPolished`, `QuantumBaseline` and `QuantumThumbnail` compositions. The delivery edition preserves **21,421 frames at 30 fps** (714.033333 seconds).

The original scientific animation is muted and reused inside the new layout. Equation cards use Python-exported numerical values, and their emphasis beats use the existing local ASR word timestamps. Prediction cards show all options without identifying the correct answer. The original continuous WAV is muxed once for delivery, avoiding extra narration tracks and chapter-boundary audio seams.

## Local setup

Use Python 3.12, Node 24 and pnpm 11.25.0. Activate the project Python environment first.

```sh
python -m pip install -r requirements-production.txt
pnpm --dir remotion install --frozen-lockfile
pnpm --dir webtools install --frozen-lockfile
python scripts/prepare_remotion.py --media-root /path/to/original/course
python scripts/sync_publication.py
pnpm --dir remotion typecheck
pnpm --dir remotion test
```

Run the commands above from the repository root; run `pnpm --dir remotion preview` to edit the composition in Studio. Media preparation copies the original `outputs/Quantum_Tunneling_Lecture.mp4` and `outputs/Quantum_Tunneling_Narration.wav` into ignored `public/media/`. If they are absent, rebuild them using the existing Manim/narration instructions; do not scrape the YouTube upload.

For Windows, the renderer defaults to the headless Chromium installed by the pinned webtools Playwright version. Install it with `pnpm --dir webtools exec playwright install chromium`. Set `REMOTION_BROWSER_EXECUTABLE` if your location differs. On Linux, use `pnpm --dir remotion exec remotion browser ensure` or set that variable to a compatible installed headless browser. `PYTHON`, `FFMPEG_BINARY` and `REMOTION_CONCURRENCY` can override executable locations and rendering concurrency. Four render workers were used on the local 16 GB machine.

## Render and verify

```sh
pnpm --dir remotion render:sample
pnpm --dir remotion render:baseline
pnpm --dir remotion stills
pnpm --dir remotion render:full
python scripts/verify_remotion.py
python scripts/sync_publication.py --render outputs/Quantum_Tunneling_Lecture_Remotion.mp4 --rebuild-h5p
```

`render:sample` and `render:baseline` produce 60-second A/B samples. Studio can preview the complete original or polished composition. `render:full` caches seven video-only chapter renders keyed to the composition, event manifest, media hashes and package lock, then concatenates them and muxes the original WAV, captions and chapter metadata. Interrupted chapters use temporary filenames and are rerendered on retry. Completed chapters are reusable. No production rendering runs in the Pages workflow.

The full output is `outputs/Quantum_Tunneling_Lecture_Remotion.mp4`. `verify` checks full decode, 1920×1080, 30 fps, H.264/AAC, limited-range BT.709/yuv420p, one audio track, speech/master correlation and measured loudness. Separate SRT/VTT are generated; optional burned captions are controlled by `showCaptions`, which defaults to false to reduce visual clutter.

## Licensing

Remotion **4.0.540 is source-available under its own license**, not unrestricted OSI open-source software. Individual use was confirmed for this production and qualifies under the bundled Free License. `production-eligibility.json` records that basis; institutional/commercial reuse must assess its own eligibility against the version used. The full render command checks that declaration and purchases nothing.

See `docs/remotion-licenses/`, `docs/remotion-production.md` and `docs/publish-remotion.md`. The original React integration code is MIT; source dependencies retain their own licenses. MP4/WAV masters, model weights, render caches and local environments are excluded from GitHub.
