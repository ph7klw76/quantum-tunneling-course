# YouTube publication and native quizzes

No YouTube upload or account action has been performed. Files are upload-ready local artifacts; publication needs your channel account.

1. Open YouTube Studio, choose **Create → Upload videos**, and select `outputs/Quantum_Tunneling_Lecture.mp4`.
2. Copy the title and description from `outputs/youtube_description.md`. Replace its companion, source and H5P URL placeholders with real published URLs. The H5P link should point to your tested host; use the companion timed-question player while the H5P host is being prepared.
3. Upload `outputs/thumbnail.png`. Set the appropriate audience and other channel settings. Under Subtitles, select English and upload `narration/lecture.srt` **with timing**. Preview captions and check specialist pronunciations and numerical values.
4. In the upload flow's **Video elements** step, click **Add** beside **Quiz**, if available. For an existing video, open the **Details** or **Editor** pane and locate Quizzes.
5. For each row of `quizzes/youtube_quizzes.csv`, choose its timestamp, paste the question and up to four options, mark the single correct answer and paste the explanation. Review all fields before saving. The Markdown version is easier to read during manual entry.
6. Save each quiz. YouTube's current help says saved quizzes must be deleted and recreated to change them. Check the video from a separate viewer account and from a phone. Availability and viewer behavior can differ; the visible Manim pause prompts and external activities remain usable if native quizzes are unavailable.
7. Review chapters against the actual video and description. This build derives chapter times from measured audio, not the originally suggested times. Check audio, captions, all chapter boundaries and video processing quality. Choose visibility and publish when your channel review is complete.
8. Put the actual YouTube watch URL in `website/dist/config.js`, rebuild/redeploy the site, and use that URL in your H5P authoring project if desired. The local MP4 remains available as a fallback.

CSV export is an editorial aid. No public API upload of native quiz interactions is assumed or attempted. Native quizzes, H5P and the browser laboratory have different capabilities and reporting.

Verified documentation on 2026-11-02: [YouTube Help: Create a post, including quizzes in Studio](https://support.google.com/youtube/answer/7124474?hl=en). It documents up to ten quizzes per video, timestamp selection, four answer options, one correct answer, and the upload/Details/Editor routes.
