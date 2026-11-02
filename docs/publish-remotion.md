# Publish the polished lecture without interrupting the current course

The original YouTube URL is `https://youtu.be/WCA_t3ttAAI`, retained for rollback. The creator supplied the separately uploaded polished edition at `https://youtu.be/Kbknh_vEjSc`; its public metadata and actual H5P streaming were verified before activation on this feature branch. YouTube cannot replace the binary under an existing ID. The commands below also document the workflow for future editions; a source pull request or local MP4 alone is not an upload.

## Review the concrete upload kit

- `outputs/Quantum_Tunneling_Lecture_Remotion.mp4`: full 1080p H.264/AAC delivery.
- `outputs/Quantum_Tunneling_Lecture_Remotion.srt` and `.vtt`: synchronized captions.
- `outputs/Quantum_Tunneling_Remotion_Thumbnail.png`: original scientific thumbnail.
- `outputs/youtube_description_polished.md` and `outputs/chapters_polished.txt`.
- `quizzes/youtube_quizzes.csv` and `.md`: seven manually enterable native YouTube quiz entries.
- `outputs/remotion-video-verification.json` and `outputs/remotion-timing-report.json`: executed delivery and timing evidence.

An absent full MP4 or a timing report marked `PREPARED_NOT_RENDER_VERIFIED` means production is unfinished. Review the actual file and verification reports before uploading.

## Upload the new video

If a supported authenticated uploader is available, obtain the required publication approval for the finished artifact and use that route. Otherwise use YouTube Studio's video upload flow manually: select the verified MP4, add the description and thumbnail, upload the English SRT, and enter the seven native quizzes where your channel supports them. Review 1080p processing, chapters, captions, audio and all prediction holds. Native quizzes require channel support and manual entry; no API installation is assumed.

Copy the actual new watch/share URL after the upload is available. Confirm playback and embedding from a viewer context. Do not paste the old URL and label it polished. Do not fabricate an upload date or assume an unverified placeholder is live.

## Activate the confirmed new URL on the feature branch

The common configuration is `course/publication_config.json`. First verify metadata without modifying it:

```sh
python scripts/configure_video.py --url ACTUAL_NEW_YOUTUBE_URL
```

After reviewing the full render and confirming the new video's actual playback:

```sh
python scripts/configure_video.py --url ACTUAL_NEW_YOUTUBE_URL --activate
python scripts/sync_publication.py --render outputs/Quantum_Tunneling_Lecture_Remotion.mp4 --rebuild-h5p
python scripts/build_pages.py --base-path /quantum-tunneling-course/
node scripts/check-site.cjs outputs/physics-fixtures.json outputs/pages
node webtools/test-site.cjs
node webtools/test-h5p-learning.cjs
```

The activation script requires a verified full render and a new ID, and validates public oEmbed metadata. That metadata check alone is not playback verification; run the actual H5P tests too. If Node is not on PATH, set `NODE_BINARY`; if tests use a shared Python environment, set `PYTHON` to its executable.

Regenerated deliverables include the real native `.h5p`, the all-in-one HTML export and the standalone questions. The Watch & Question section continues to embed the same H5P player. Current code uses the tested Video 1.6.81 adapter, rather than the broken private YouTube property access. In Lumi Desktop, open the native package, preview each question and export HTML using your installed version's export action. Check the required H5P core compatibility before LMS import.

## Pull request, merge and live checks

Commit the regenerated source/assets to `remotion-polish`, update the pull request with the real upload URL and actual test results, and obtain merge/publication approval when required by the current session or repository. Do not merge merely to make a draft visible. The existing Pages workflow deploys `main`; the branch's production-source workflow does not deploy or rerender the full video.

After the approved merge, verify the successful workflow for that exact commit, request the real HTTPS course resources, compare a distinguishing served artifact with source, and run the public H5P playback test with `H5P_EMBEDDED=true` and `H5P_TEST_URL` set to the course URL. Check desktop and phone playback, chapter jumps, all quiz paths and JupyterLite. Record actual results. GitHub Pages does not persist individual grades; LMS/LRS reporting requires a supported authenticated service.

## Roll back

The old upload remains available. Set the active URL back to `original_youtube_url` through `scripts/configure_video.py --url ORIGINAL_URL --activate --rollback`, regenerate H5P/site files, test and make a normal reviewed revert/update commit. Preserve branch history and the new upload for diagnosis; do not force-push or delete working media as a rollback mechanism.
