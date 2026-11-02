# GitHub Pages build and publication

Repository: https://github.com/ph7klw76/quantum-tunneling-course

Website: https://ph7klw76.github.io/quantum-tunneling-course/

The workflow `.github/workflows/deploy.yml` tests and builds the site on every push to `main`, then publishes the Pages artifact. Pages must use **GitHub Actions** as its build source in repository Settings → Pages. Deployment uses the built-in `GITHUB_TOKEN`; no personal access token, paid API or subscription is needed.

## Reproduce the public build

Use Python 3.12, Node 24 and pnpm 11.25.0:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate; Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements-ci.txt
pnpm --dir webtools install --frozen-lockfile
python -m unittest discover -s tests -v
python scripts/check_course.py
python scripts/build_pages.py --base-path /quantum-tunneling-course/
node scripts/check-site.cjs outputs/physics-fixtures.json outputs/pages
python scripts/serve.py --directory outputs/pages --base-path /quantum-tunneling-course/ --port 8765
```

Open http://127.0.0.1:8765/quantum-tunneling-course/. In another terminal, run `node webtools/test-site.cjs` after installing Chromium with `pnpm --dir webtools exec playwright install chromium`. Tests use an isolated browser against this project's server. The JupyterLite test executes the actual notebook in a browser Pyodide kernel, which needs access to its public package/runtime CDN on first use.

Navigation, scripts, captions and activity paths are relative. JupyterLite is built with the repository prefix. The public artifact contains no MP4 or WAV; video is hosted at https://youtu.be/WCA_t3ttAAI. Local masters remain in `outputs/` and are excluded from GitHub.

## Rebuild H5P

The committed native `.h5p` package includes its playable upstream source libraries. Committed HTML exports are used directly by Pages, so deployment does not depend on H5P Hub availability.

```sh
python scripts/fetch_h5p.py
python scripts/author_h5p.py
node webtools/h5p-build.cjs
```

Review `h5p/upstream-lock.json` when upstream changes. Hub URLs may serve newer versions over time; preserve the native package for the exact original library set. Core/editor revisions and bundle hashes are recorded. `tools/h5p/` is an ignored local cache. See `h5p/THIRD_PARTY.md` for licensing.

The H5P Hub's Interactive Video bundle includes an older YouTube adapter. The fetch/build scripts explicitly install official **H5P.Video 1.6.81**, pinned to commit `0293f342d757b5d7623ba841e1e513365ae42495`. It uses YouTube's public `getIframe()` API instead of private player properties, fixing a black-video startup error. The native package contains this update too. Importing it into an LMS requires a compatible H5P core (1.28 or newer).

## Verification scope

CI checks physics conservation and independent ODE agreement, pronunciation/text alignment helpers, caption/quiz timing, full desktop notebook execution, JavaScript/Python agreement, internal paths at the repository prefix, mobile layouts, actual H5P answer/feedback/retry behavior, YouTube player initialization and visible iframe geometry, and the notebook in browser Pyodide. Reports and screenshots are uploaded as workflow artifacts. The final job requests the published page and key resources over HTTPS.

YouTube streaming did not advance on the hosted GitHub runner, so its CI check explicitly reports startup only. Full real-video playback and the first timed quiz pause are tested with `node webtools/test-h5p-playback.cjs` from a video-accessible network. To test the published export directly in PowerShell: set `$env:H5P_TEST_URL` to the public lesson URL and run that command. The script checks advancing playback time, a visible video frame, the actual question, and a stable paused time, and saves screenshots and JSON evidence. It does not mock the video API.

An automated check cannot certify an LMS's gradebook or a viewer's YouTube/network policy. Those are destination-specific checks.

The main Watch & Question section embeds the same-origin H5P export directly. `website/dist/h5p-player.js` sizes the iframe to its content and forwards chapter selections to H5P, preserving its timed questions. The interactive-video card was merged into this section. To check real playback and chapter jumps on the merged page, set `H5P_EMBEDDED=true` and run `node webtools/test-h5p-playback.cjs`; `H5P_TEST_URL` can select the published course home page.
