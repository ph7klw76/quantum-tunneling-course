/* Shared YouTube player. All course paths remain relative for GitHub Pages. */
'use strict';
window.CourseVideo = class CourseVideo {
  constructor(id) {
    this.listeners = [];
    this.pendingTime = null;
    this.ready = false;
    this.element = document.getElementById(id);
    const url = new URL(window.COURSE_CONFIG.youtubeUrl);
    const videoId = url.hostname === 'youtu.be' ? url.pathname.slice(1) : url.searchParams.get('v');
    if (!/^[\w-]{11}$/.test(videoId || '')) throw new Error('Invalid YouTube video URL');
    const previous = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => { if (previous) previous(); this.init(videoId); };
    if (window.YT && YT.Player) this.init(videoId);
    else if (!document.querySelector('script[data-youtube-api]')) {
      const script = document.createElement('script');
      script.src = 'https://www.youtube.com/iframe_api';
      script.dataset.youtubeApi = 'true';
      document.head.append(script);
    }
  }
  init(videoId) {
    if (this.player) return;
    this.player = new YT.Player(this.element.id, {
      host: 'https://www.youtube-nocookie.com', videoId,
      playerVars: {playsinline: 1, rel: 0, origin: location.origin, cc_load_policy: 1, cc_lang_pref: 'en'},
      events: {
        onReady: () => { this.ready = true; if (this.pendingTime !== null) this.seek(this.pendingTime); },
        onStateChange: e => { if (e.data === 1 && this.locked) this.pause(); },
        onError: () => {
          document.querySelectorAll('[data-video-status]').forEach(e => {
            e.textContent = 'YouTube could not play here. Open the lecture on YouTube, or continue with the questions below.';
          });
        }
      }
    });
    this.timer = setInterval(() => {
      if (this.ready) this.listeners.forEach(fn => fn(this.player.getCurrentTime()));
    }, 250);
  }
  seek(seconds) { this.pendingTime = seconds; if (this.ready) this.player.seekTo(seconds, true); }
  play() { if (this.ready) this.player.playVideo(); return Promise.resolve(); }
  pause() { if (this.ready) this.player.pauseVideo(); }
  onTime(fn) { this.listeners.push(fn); }
};
