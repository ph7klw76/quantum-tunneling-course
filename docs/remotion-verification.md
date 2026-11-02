# Executed Remotion upgrade verification

Verified locally on 3 November 2026, from main commit `76781c6a528b87ba80c38f2f2d9900f20b6b0a4f`, on the `remotion-polish` feature branch. These are executed results, not promises of a new YouTube upload or deployment.

## Finished video

`outputs/Quantum_Tunneling_Lecture_Remotion.mp4` is 34,889,453 bytes: H.264/AAC, 1920×1080, 30 fps, yuv420p with limited-range BT.709, 21,421 frames and 714.033333 seconds. Complete FFmpeg decoding passed. FFprobe and PyAV agree on the delivery metadata. The file contains one narration track, seven named chapters and 193 embedded English caption cues matching the separately delivered SRT.

Integrated loudness is −16.25 LUFS and true peak is −1.39 dBTP. Audio correlations with the original continuous Chatterbox WAV at 5, 350 and 695 seconds exceed 0.99999. Original Manim audio is muted, and the source WAV is encoded once at the final mux. See [video verification](../outputs/remotion-video-verification.json), [FFprobe output](../outputs/remotion-ffprobe.json), [media hashes](../outputs/remotion-media-provenance.json) and [delivery checksum](../outputs/remotion-delivery.json).

Rendered equations, prediction cards, caption proof, thumbnail and extracted delivery frames were inspected. Compare the [baseline frame](../outputs/remotion-baseline-frame.png) with the [polished exact-result frame](../outputs/remotion-actual-frame-8650.png) and [laboratory invitation](../outputs/remotion-actual-frame-20700.png). This is visual inspection and signal verification; it is not a new human-listening study of voice naturalness.

## Quiz synchronization

All 28 scene boundaries and the total frame count match the original baseline. Each quiz retains a 6–10 second reasoning hold before answer revelation. Actual desktop and phone H5P playback crossed each timestamp and paused within 0.15 seconds in the polished-MP4 tests.

| ID | Original → polished | Review explanation |
|---|---|---|
| Q1 | 00:50 → 00:50 | 0 s |
| Q2 | 02:24 → 02:24 | 76 s |
| Q3 | 04:15 → 04:15 | 177.33 s |
| Q4 | 06:02 → 06:02 | 291.37 s |
| Q5 | 07:39 → 07:39 | 400.23 s |
| Q6 | 09:19 → 09:19 | 485.97 s |
| Q7 | 10:48 → 10:48 | 600.5 s |

See the [render-validated timing report](../outputs/remotion-timing-report.json). Wrong answers, scientific feedback, review seeking, native question reset/retry and correct scores passed for all seven. The five-concept Summary scored 5/5. The Summary's pre-existing tip serialization failure was corrected in the generator and verified through its real controls.

The creator supplied the new polished YouTube upload, `https://youtu.be/Kbknh_vEjSc` (public title: Quantum Tunneling Lecture Remotion). The [YouTube H5P test](../outputs/browser/h5p-learning-paths.json) and isolated polished-MP4 tests on [desktop](../outputs/browser/h5p-polished-learning-paths.json) and [phone](../outputs/browser/h5p-polished-learning-paths-phone.json) are separate evidence. Native MP4 review jumps produced seven specific aborted-play warnings per run, recorded as `mediaInterruptions`; playback, pause, feedback, seeking, retry and scoring assertions passed. Other page errors remain test failures. The new YouTube-source run reported no page errors.

## Science, site and laboratory

- 18 Python unit tests passed: dimensional/domain/limit checks, independent boundary and ODE solutions, current, narration and publication timing.
- TypeScript checking and all three Remotion manifest tests passed.
- The desktop notebook executed all eight code cells without errors.
- The actual JupyterLite/Pyodide notebook executed in Chromium, produced three plots and agreed with Python: T=0.142361995, R=0.857638005. All original code cells are preserved; a Markdown guide maps Q1–Q7 to investigations.
- JavaScript/Python comparisons passed for 95 wave samples and five parameter cases; 45 asset links and six website scripts passed checks at `/quantum-tunneling-course/`.
- Desktop (1440), tablet (820) and phone (390) layouts passed navigation, chapter and overflow checks. Native H5P and standalone exports were rebuilt using the retained official Video 1.6.81 adapter.

See [course checks](../outputs/course-checks.json) and [browser results](../outputs/browser/results.json). Hosted-runner YouTube initialization is explicitly startup-only; local real streaming and polished-MP4 interaction tests supply separate playback evidence.

## Publication boundary

The feature branch now selects the verified new YouTube upload in the common configuration and regenerated native H5P/HTML. It does not deploy on branch pushes. The pre-upgrade Pages site returned HTTP 200 for all ten checked resources; see [baseline live-site evidence](../outputs/remotion-live-existing-site.json). Final publication is verified by the deployment workflow for the merged revision and a separate live playback run.

The upload URL was supplied by the creator, and actual playback was tested. No native YouTube quiz installation, YouTube caption upload or LMS grade persistence is claimed. See [safe publication](publish-remotion.md) for future activation and rollback. Remotion 4.0.540 individual free-use eligibility was confirmed by the creator. Large media masters remain local.

## Public delivery verification

[PR #1](https://github.com/ph7klw76/quantum-tunneling-course/pull/1) merged as `c1b3e71f35a6657571a4ae713991e033eb3e3cec`. Its [Pages build, deployment and HTTPS verification](https://github.com/ph7klw76/quantum-tunneling-course/actions/runs/41499549300) all succeeded. The actual public index, configuration, interactive HTML and native package hashes match that revision; all ten requested resources returned HTTP 200. See [published-file evidence](../outputs/remotion-live-published.json).

The public integrated Watch & Question section streamed the confirmed new video, its parent chapter buttons sought the same H5P player, and playback naturally crossed Q1 and paused. See [integrated playback](../outputs/browser/h5p-playback.json). All seven public standalone H5P quiz paths and the 5/5 Summary also passed at phone width with no page errors; see [public phone learning paths](../outputs/browser/h5p-live-learning-paths-phone.json).

The first integrated test attempts timed out while polling readiness with animation frames inside a lazy iframe. Direct diagnostics showed the correct video ID and loaded metadata. Timer polling resolved the test's offscreen-frame throttling; the strengthened test also asserts the player's actual source URL. This follow-up changes verification code and evidence, with no change to the published lesson content.
