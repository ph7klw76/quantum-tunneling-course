# Quantum Tunneling — Can an Electron Pass Through a Wall?

[Open the interactive course](https://ph7klw76.github.io/quantum-tunneling-course/) · [Watch the lecture](https://youtu.be/WCA_t3ttAAI) · [Deployment and tests](https://github.com/ph7klw76/quantum-tunneling-course/actions/workflows/deploy.yml)

An open undergraduate Applied Quantum Mechanics course combining a narrated Manim lecture, genuine H5P activities, an interactive finite-barrier simulation and a JupyterLite Python laboratory.

The default free-electron model uses E = 0.50 eV, V₀ = 1.00 eV and a = 0.45 nm, giving **T = 0.1423619955** and **R = 0.8576380045**. It is a stationary, elastic, one-dimensional model with identical leads. The wavefunction is a probability amplitude; its plotted curve is not a particle trajectory.

## Learn

- Explore exact wavefunctions, probability density and transmission with the responsive simulation.
- Watch the 11:54 lecture, with chapter navigation and downloadable English subtitles.
- Complete seven H5P questions with feedback, retries and review jumps, then a five-concept Summary. Standalone H5P questions also work without YouTube.
- Execute the notebook in a real browser Pyodide kernel: match boundaries, check current conservation, compare an independent ODE solution and investigate synthetic transport evidence.
- Complete the independent transfer investigation, assessment and rubric.

## Project files

| Path | Contents |
|---|---|
| `video/scenes.py`, `build.py` | 28 Manim scenes and synchronized lecture assembly |
| `course/` | Stable exact model, boundary matching and independent numerical solver |
| `narration/` | Script, pronunciation rules, measured timeline and 193-cue SRT |
| `scripts/neural_narration.py` | Local Chatterbox integration, Kokoro-82M fallback and voice comparisons |
| `h5p/` | Native `.h5p`, editable parameters, authoring specification and license notices |
| `lab/` | Executable notebook and JupyterLite build configuration |
| `website/dist/` | Public website source and Lumi-exported H5P HTML |
| `quizzes/`, `docs/` | Learning activities, assessments and YouTube materials |
| `tests/`, `webtools/test-site.cjs` | Scientific and real-browser verification |
| `.github/workflows/deploy.yml` | Automatic test, build, deploy and live HTTPS verification |

## Build and test

See [GitHub Pages instructions](docs/github-pages.md) for the complete reproducible public build. Python 3.12, Node 24 and pnpm 11.25.0 are used in CI.

```sh
python -m pip install -r requirements-ci.txt
pnpm --dir webtools install --frozen-lockfile
python -m unittest discover -s tests -v
python scripts/check_course.py
python scripts/build_pages.py --base-path /quantum-tunneling-course/
node scripts/check-site.cjs outputs/physics-fixtures.json outputs/pages
python scripts/serve.py --directory outputs/pages --base-path /quantum-tunneling-course/
```

Visit http://127.0.0.1:8765/quantum-tunneling-course/. To run the isolated browser checks, install Chromium with `pnpm --dir webtools exec playwright install chromium`, then run `node webtools/test-site.cjs`.

Pushes to `main` trigger GitHub Actions. Set repository **Settings → Pages → Source → GitHub Actions** if creating a new deployment. The workflow publishes only after checks pass and requests the deployed URL to verify it. Run logs and uploaded verification artifacts show the actual results for each revision.

## Rebuild the narrated lecture

[Neural narration instructions](docs/neural-narration.md) document the isolated speech environment, pinned model revisions, scientific pronunciation, three comparison samples, subtitle alignment and Manim synchronization. Chatterbox is the selected local engine; Kokoro-82M is the tested fallback. Both run without paid APIs. [Local rendering instructions](docs/local-build.md) preserve the full video workflow.

Generated MP4/WAV masters, speech models, environment folders and caches are excluded from GitHub. The website streams the actual YouTube lecture. Rebuilding the video requires the documented local dependencies and model downloads; it is independent of Pages deployment.

## Licenses and limits

Original code: [MIT](LICENSE). Original lesson text, assessments and visuals: [CC BY 4.0](CONTENT_LICENSE.md). H5P, Lumi, speech models and runtime dependencies retain their upstream licenses; see [H5P notices](h5p/THIRD_PARTY.md) and [speech notices](docs/tts-licenses).

YouTube and the Pyodide package CDN must be reachable on the viewer's network. GitHub Pages practice is not a gradebook. Import the native H5P into your LMS and verify student-account reporting before assigning grades. No LMS reporting or native YouTube quiz installation is claimed.
