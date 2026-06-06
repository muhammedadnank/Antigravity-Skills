/* ============================================================
   parallax.js — virtual-scroll frame scrubber

   The document does NOT scroll. We intercept wheel / touch /
   keyboard input and convert it into a 0..1 virtualProgress
   that drives the frame index and the scene fades.
   ============================================================ */

(function () {
  'use strict';

  // ---------- utils ----------
  const pad   = (n, w) => String(n).padStart(w, '0');
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

  // trapezoidal fade for a scene over [start..end]
  function trapFade(progress, start, end, fadeRatio = 0.25) {
    if (progress <= start || progress >= end) return 0;
    const t = (progress - start) / (end - start);
    const fIn  = Math.min(1, t / fadeRatio);
    const fOut = Math.min(1, (1 - t) / fadeRatio);
    return Math.max(0, Math.min(fIn, fOut));
  }

  // ---------- FrameScrubber ----------
  class FrameScrubber {
    constructor({ canvas, folder, frameCount, padWidth = 3, prefix = 'frame-', ext = 'jpg' }) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.folder = folder;
      this.frameCount = frameCount;
      this.padWidth = padWidth;
      this.prefix = prefix;
      this.ext = ext;
      this.frames = new Array(frameCount);
      this.loaded = 0;
      this.target = 0;
      this.current = 0;
      this.lastDrawn = -1;
      this.dpr = Math.min(2, window.devicePixelRatio || 1);
    }

    framePath(i) {
      return `${this.folder}/${this.prefix}${pad(i + 1, this.padWidth)}.${this.ext}`;
    }

    preload(onProgress) {
      const tasks = [];
      for (let i = 0; i < this.frameCount; i++) {
        tasks.push(new Promise((resolve) => {
          const img = new Image();
          img.decoding = 'async';
          const done = () => {
            this.loaded += 1;
            onProgress && onProgress(this.loaded, this.frameCount);
            resolve();
          };
          img.onload = done;
          img.onerror = done;
          img.src = this.framePath(i);
          this.frames[i] = img;
        }));
      }
      return Promise.all(tasks);
    }

    resize() {
      const w = window.innerWidth;
      const h = window.innerHeight;
      this.canvas.width  = Math.round(w * this.dpr);
      this.canvas.height = Math.round(h * this.dpr);
      this.canvas.style.width  = w + 'px';
      this.canvas.style.height = h + 'px';
      this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
      this.lastDrawn = -1;
      this.draw(this.current);
    }

    draw(frameIdx) {
      const i = clamp(Math.round(frameIdx), 0, this.frameCount - 1);
      if (i === this.lastDrawn) return;
      const img = this.frames[i];
      if (!img || !img.complete || !img.naturalWidth) return;
      const cw = this.canvas.width  / this.dpr;
      const ch = this.canvas.height / this.dpr;
      const iw = img.naturalWidth;
      const ih = img.naturalHeight;
      const scale = Math.max(cw / iw, ch / ih);  // cover
      const dw = iw * scale;
      const dh = ih * scale;
      const dx = (cw - dw) * 0.5;
      const dy = (ch - dh) * 0.5;
      this.ctx.clearRect(0, 0, cw, ch);
      this.ctx.drawImage(img, dx, dy, dw, dh);
      this.lastDrawn = i;
    }

    setTarget(progress01) {
      this.target = clamp(progress01, 0, 1) * (this.frameCount - 1);
    }

    snapTo(progress01) {
      const v = clamp(progress01, 0, 1) * (this.frameCount - 1);
      this.target = v;
      this.current = v;
      this.draw(v);
    }

    tick() {
      const diff = this.target - this.current;
      if (Math.abs(diff) < 0.005) {
        if (this.current !== this.target) {
          this.current = this.target;
          this.draw(this.current);
        }
        return;
      }
      this.current += diff * 0.22;
      this.draw(this.current);
    }
  }

  // ---------- ParallaxPage (virtual scroll) ----------
  class ParallaxPage {
    constructor({ folder, frameCount, scrollBudget = 2800, prefix, padWidth, ext }) {
      this.canvas = document.querySelector('.bg-canvas');
      this.scenes = Array.from(document.querySelectorAll('.scene'));
      this.loaderEl = document.querySelector('.loader');
      this.progressTextEl = document.querySelector('.loader-progress');
      this.progressBarEl = document.querySelector('.loader-bar-fill');
      this.scrollBarEl = document.querySelector('.scroll-progress-bar');
      this.scrollHintEl = document.querySelector('.scroll-hint');
      this.frameCounterEl = document.querySelector('.frame-counter');

      // Strip undefined so FrameScrubber's defaults still apply.
      const scrubberOpts = { canvas: this.canvas, folder, frameCount };
      if (prefix    !== undefined) scrubberOpts.prefix    = prefix;
      if (padWidth  !== undefined) scrubberOpts.padWidth  = padWidth;
      if (ext       !== undefined) scrubberOpts.ext       = ext;
      this.scrubber = new FrameScrubber(scrubberOpts);

      // Virtual scroll: 0..1 progress driven by wheel / touch / keys.
      // scrollBudget is the number of accumulated input pixels for a
      // full 0→1 traversal. ~2800px ≈ 3-4 trackpad swipes / ~28 mouse
      // wheel notches — feels deliberate but not exhausting.
      this.virtualProgress = 0;
      this.scrollBudget = scrollBudget;

      this.interactive = false;
      this._raf = this._raf.bind(this);
    }

    async start() {
      document.documentElement.classList.add('scrub-page');
      document.body.classList.add('scrub-page');

      requestAnimationFrame(this._raf);

      await this.scrubber.preload((loaded, total) => {
        const pct = Math.round((loaded / total) * 100);
        if (this.progressTextEl) this.progressTextEl.textContent = pct + '%';
        if (this.progressBarEl)  this.progressBarEl.style.right = (100 - pct) + '%';
      });

      this.scrubber.resize();
      this.scrubber.snapTo(0);

      await new Promise(r => setTimeout(r, 220));

      if (this.loaderEl) this.loaderEl.classList.add('hidden');
      if (this.scrollHintEl) this.scrollHintEl.classList.add('show');

      this._update();
      this._attachInputs();
      this.interactive = true;
    }

    _attachInputs() {
      // ---- wheel ----
      window.addEventListener('wheel', (e) => {
        if (!this.interactive) return;
        e.preventDefault();
        let dy = e.deltaY;
        if (e.deltaMode === 1)      dy *= 16;                   // lines
        else if (e.deltaMode === 2) dy *= window.innerHeight;   // pages
        this.virtualProgress = clamp(
          this.virtualProgress + dy / this.scrollBudget, 0, 1
        );
        this._update();
      }, { passive: false });

      // ---- touch ----
      let touchY = null;
      window.addEventListener('touchstart', (e) => {
        touchY = e.touches[0].clientY;
      }, { passive: true });

      window.addEventListener('touchmove', (e) => {
        if (touchY == null || !this.interactive) return;
        // don't hijack scrolls that start on links/buttons
        if (e.target.closest('a, button')) return;
        e.preventDefault();
        const y = e.touches[0].clientY;
        const dy = touchY - y; // finger up ⇒ positive (advance)
        touchY = y;
        this.virtualProgress = clamp(
          this.virtualProgress + (dy * 2.4) / this.scrollBudget, 0, 1
        );
        this._update();
      }, { passive: false });

      window.addEventListener('touchend',  () => { touchY = null; });
      window.addEventListener('touchcancel', () => { touchY = null; });

      // ---- keyboard ----
      window.addEventListener('keydown', (e) => {
        if (!this.interactive) return;
        // ignore when typing in a form field (none here, but safe)
        if (/^(input|textarea|select)$/i.test(e.target.tagName)) return;

        const SMALL = 0.035;
        const BIG   = 0.10;
        let d = null;
        switch (e.key) {
          case 'ArrowDown':
          case 'j':         d =  SMALL; break;
          case 'ArrowUp':
          case 'k':         d = -SMALL; break;
          case 'PageDown':
          case ' ':         d =  BIG;   break;
          case 'PageUp':    d = -BIG;   break;
          case 'Home':
            e.preventDefault();
            this.virtualProgress = 0; this._update(); return;
          case 'End':
            e.preventDefault();
            this.virtualProgress = 1; this._update(); return;
          default: return;
        }
        e.preventDefault();
        this.virtualProgress = clamp(this.virtualProgress + d, 0, 1);
        this._update();
      });

      // ---- resize ----
      window.addEventListener('resize', () => {
        this.scrubber.resize();
        this._update();
      });
      window.addEventListener('orientationchange', () => {
        this.scrubber.resize();
        this._update();
      });
    }

    _update() {
      const p = this.virtualProgress;
      this.scrubber.setTarget(p);

      // scenes — fade + slight upward translate as they appear
      for (const scene of this.scenes) {
        const start = parseFloat(scene.dataset.start);
        const end   = parseFloat(scene.dataset.end);
        const ratio = scene.dataset.fade ? parseFloat(scene.dataset.fade) : 0.25;
        const op = trapFade(p, start, end, ratio);
        scene.style.opacity = op.toFixed(3);
        const ty = (1 - op) * 26;
        scene.style.transform = `translate3d(0, ${ty}px, 0)`;
        scene.style.visibility    = op > 0.001 ? 'visible' : 'hidden';
        scene.style.pointerEvents = op > 0.5   ? 'auto'    : 'none';
      }

      // top scroll-progress bar reflects virtual progress
      if (this.scrollBarEl) this.scrollBarEl.style.transform = `scaleX(${p})`;

      // scroll hint
      if (this.scrollHintEl) {
        if (p > 0.02) this.scrollHintEl.classList.remove('show');
        else          this.scrollHintEl.classList.add('show');
      }

      // frame counter (1-based) — width matches total
      if (this.frameCounterEl) {
        const total = this.scrubber.frameCount;
        const idx = clamp(Math.round(p * (total - 1)), 0, total - 1) + 1;
        const w = String(total).length;
        this.frameCounterEl.textContent = `${pad(idx, w)} / ${pad(total, w)}`;
      }
    }

    _raf() {
      this.scrubber.tick();
      requestAnimationFrame(this._raf);
    }
  }

  window.ParallaxPage  = ParallaxPage;
  window.FrameScrubber = FrameScrubber;
})();
