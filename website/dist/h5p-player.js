/* Same-origin bridge: chapter buttons and responsive sizing for the embedded H5P lesson. */
'use strict';
window.CourseH5PVideo = class CourseH5PVideo {
  constructor(id) {
    this.frame = document.getElementById(id);
    this.pendingSeek = null;
    this.pendingPlay = false;
    this.frame.addEventListener('load', () => this.connect());
    this.timer = setInterval(() => { this.connect(); this.flush(); }, 250);
    window.addEventListener('pagehide', () => {
      clearInterval(this.timer);
      if (this.observer) this.observer.disconnect();
    }, {once:true});
    this.connect();
  }
  connect() {
    const doc = this.frame.contentDocument;
    if (!doc || !doc.body) return;
    if (doc !== this.doc) {
      this.doc = doc;
      if (this.observer) this.observer.disconnect();
      this.observer = new ResizeObserver(() => requestAnimationFrame(() => this.resize()));
      this.observer.observe(doc.body);
    }
    const instance = this.frame.contentWindow.H5P?.instances?.[0];
    if (instance && instance !== this.instance) {
      this.instance = instance;
      instance.on('resize', () => requestAnimationFrame(() => this.resize()));
      this.resize();
    }
  }
  resize() {
    const content = this.doc?.querySelector('.h5p-content');
    if (!content) return;
    const height = Math.ceil(content.getBoundingClientRect().height) + 2;
    if (height > 100 && Math.abs(height - this.frame.getBoundingClientRect().height) > 1) {
      this.frame.style.height = height + 'px';
    }
  }
  flush() {
    if (!(this.instance?.video?.getDuration?.() > 0)) return;
    if (this.pendingSeek !== null) {
      this.instance.seek(this.pendingSeek);
      this.pendingSeek = null;
    }
    if (this.pendingPlay) {
      this.instance.play();
      this.pendingPlay = false;
    }
  }
  seek(seconds) { this.pendingSeek = seconds; this.flush(); }
  play() { this.pendingPlay = true; this.flush(); }
};
