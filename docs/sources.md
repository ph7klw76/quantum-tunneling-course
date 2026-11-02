# Sources, licenses and verification boundaries

## Scientific references

- [OpenStax University Physics Volume 3, 7.6: Quantum Tunneling](https://openstax.org/books/university-physics-volume-3/pages/7-6-the-quantum-tunneling-of-particles-through-potential-barriers): finite-barrier physics and transmission. The course equations and animations are original implementations, with results independently cross-checked numerically.
- [NIST CODATA fundamental constants](https://physics.nist.gov/cuu/Constants/): free-electron mass and reduced Planck constant. The code states the numerical constants and their precision; electron volt conversion is exact in SI.
- [Nobel Prize in Physics 1986](https://www.nobelprize.org/prizes/physics/1986/summary/): historical STM context. No experimental device dataset is represented as original evidence in this course.
- [Binnig, Rohrer, Gerber & Weibel, Surface Studies by Scanning Tunneling Microscopy, Physical Review Letters 49, 57 (1982)](https://doi.org/10.1103/PhysRevLett.49.57): primary experimental STM reference for further reading.
- [Tersoff & Hamann, Theory and Application for the Scanning Tunneling Microscope, Physical Review Letters 50, 1998 (1983)](https://doi.org/10.1103/PhysRevLett.50.1998): primary reference on the link between STM current and electronic structure.

The lossless stationary rectangular-barrier calculation is not a realistic full device-current model. Identical asymptotic potentials and masses are essential to the simple T=|t|² relation. The wave curves are scattering-state amplitudes, not particle trajectories. Parameter-sweep animations compare stationary solutions rather than modeling physical wall motion. Synthetic notebook data are explicitly labelled.

## Platform references checked for this build

- [YouTube native quizzes help](https://support.google.com/youtube/answer/7124474?hl=en)
- [H5P Interactive Video tutorial](https://h5p.org/node/691)
- [H5P Interactive Video content type](https://h5p.com/content-types/interactive-video)
- [JupyterLite GitHub Pages deployment](https://jupyterlite.readthedocs.io/en/stable/quickstart/deploy.html)
- [JupyterLite content indexing](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html)
- [Manim Community documentation](https://docs.manim.community/en/stable/)
- [Official eSpeak NG releases](https://github.com/espeak-ng/espeak-ng/releases)

These platforms can change. Follow their current controls and destination-host policy. Source code and manifests are authoritative for the local build's pinned versions.

## Licensing

Original code: MIT, see `LICENSE`. Original lesson text, assessments, thumbnail and rendered educational visuals: CC BY 4.0, see `CONTENT_LICENSE.md`. Suggested attribution: “Can an Electron Pass Through a Wall? — Applied Quantum Lab, 2026; CC BY 4.0.” You may replace that credit with the final publication's author credit while retaining any third-party notices.

The neural upgrade uses **Chatterbox TTS** as the primary local speech model (MIT), with **Kokoro-82M** and its official `af_heart` voicepack as the fallback (Apache 2.0). No named individual's voice recording is cloned. See `docs/neural-narration.md`, the saved upstream license notices in `docs/tts-licenses`, and the actual selected-engine record in `outputs/neural-narration-report.json`. The earlier eSpeak NG 1.52.0 narration is retained only as an archived baseline. Kokoro can use eSpeak NG (GPL) for phonemization; it does not use the old eSpeak narration audio. This project does not include third-party music, stock photos or copied illustrations. Fonts are system-rendered; font binaries are not distributed. Matplotlib, NumPy, SciPy, Manim, Pyodide and JupyterLite retain their upstream licenses; see installed package metadata and the JupyterLite build's license notices.

`tools/` is a local build cache, not part of the distributable source. To redistribute an engine binary or vendor other dependencies, also provide their required license/source notices. Downloading dependencies from the recorded official sources is the default reproducible setup.

## Public course and verification

The lecture is hosted on [YouTube](https://youtu.be/WCA_t3ttAAI), and the [source repository](https://github.com/ph7klw76/quantum-tunneling-course) contains the workflow and test reports. Native H5P and HTML exports are in the [lesson guide](h5p-guide.html). H5P bundles preserve upstream notices; see `h5p/THIRD_PARTY.md` in the repository.

The local neural lecture was verified at 1920×1080, 30 fps, with 193 measured subtitle cues and all 28 scene slots synchronized. Its selected engine is Chatterbox (`chatterbox_warm`). Local WAV/MP4 masters and model caches are excluded from GitHub. Workflow run logs show the actual outcome for each published revision.

JupyterLite initializes a real browser Python runtime and downloads public packages on first use. YouTube playback requires access to YouTube. Standalone H5P practice, subtitles and the notebook download provide alternative paths. GitHub Pages does not provide a gradebook; import the native package into your LMS for account-linked reporting.
