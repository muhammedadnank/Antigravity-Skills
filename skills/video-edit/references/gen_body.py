# Hebrew body caption generator — HORIZONTAL (1920x1080).
# Generates compositions/components/caption-body.html from transcript.json.
# Supports 13 pill-rendered styles + 2 external (kinetic-slam, parallax-layers).
#
# Per-segment style overrides:
#   caption_styles.json {"assignments": {"<seg_idx>": {"style": "<id>"}}}
#   Styles routed to EXTERNAL_STYLES are skipped here and emitted in
#   caption_external.json for the agent to wire as dedicated sub-comps.
import json, os, re, io

BODY_START = 0.0
BODY_END_GUESS = 179.5
RUN_LEN = 3
MAX_WORDS = 4

# Style id (picker)  ->  internal short code (this generator)
STYLE_SHORT = {
    "editorial-emphasis": "ed",
    "matrix-decode":      "mx",
    "typewriter":         "tw",
    "neon-glow":          "ng",
    "split-reveal":       "sr",
    "mask-wipe":          "mw",
    "marquee-rail":       "mr",
    "stamp-impact":       "si",
    "liquid-fill":        "lf",
    "glitch-rgb":         "gr",
    "soft-fade":          "sf",
    "bold-underline":     "bu",
    "highlight-marker":   "hm",
}
# 2 styles take over the whole frame, can't sit in the pill — host wires them.
EXTERNAL_STYLES = {"kinetic-slam", "parallax-layers"}

CORRECTIONS = {
    "קלוט": "קלוד", "לקלוט": "לקלוד", "מקלוט": "מקלוד",
    "המאמם": "המהמם", "התירוף": "הטירוף", "מהתחלס": "מהתחלה",
    "מזגיר": "מזכיר", "אשמחים": "אשמח", "ערב": "ערך",
    "אישות": "שוט", "מהמדהים": "המהמם", "החתונה": "תחתונה",
    "הרגע": "האריה", "מודי": "דפי",
}
STOP = set(
    "של את על אם כי לא מה זה יש אין גם רק אני אתה הוא היא הם הן אנחנו ואז אבל או הזה הזאת אנו כך איך למה איפה מתי שם פה כאן עוד היה היא הייתי להיות יהיה תהיה ה ש ל ב מ ו כ".split()
)


def correct(tok):
    m = re.match(r"^(\S+?)([.,!?]*)$", tok)
    core, tail = (m.group(1), m.group(2)) if m else (tok, "")
    if core in CORRECTIONS:
        core = CORRECTIONS[core]
    return core + tail


def load_words():
    data = json.load(open("transcript.json", encoding="utf-8"))
    words = []
    for si, seg in enumerate(data):
        for w in seg["words"]:
            t = correct(w["word"].strip())
            if not t:
                continue
            words.append({"t": t, "s": w["start"], "e": w["end"], "seg": si})
    return [w for w in words if BODY_START <= w["s"] < BODY_END_GUESS]


def load_style_overrides():
    if not os.path.exists("caption_styles.json"):
        return {}
    try:
        doc = json.load(open("caption_styles.json", encoding="utf-8"))
    except Exception:
        return {}
    out = {}
    for k, v in (doc.get("assignments") or {}).items():
        try:
            out[int(k)] = (v or {}).get("style")
        except (ValueError, TypeError):
            continue
    return {k: v for k, v in out.items() if v}


STYLE_OVERRIDES = load_style_overrides()


def group_words(words):
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt["s"] - w["e"]) if nxt else 99
        seg_change = bool(nxt and nxt["seg"] != w["seg"])
        ends_sentence = bool(re.search(r"[.?!]$", w["t"]))
        if ends_sentence or seg_change or len(cur) >= MAX_WORDS or gap > 0.34 or nxt is None:
            groups.append(cur)
            cur = []
    merged = []
    for g in groups:
        if len(g) == 1 and merged and len(merged[-1]) < 5:
            merged[-1].extend(g)
        else:
            merged.append(g)
    return merged


def emph_index(g):
    best, bi = -1, 0
    for i, w in enumerate(g):
        core = re.sub(r"[^֐-׿\w]", "", w["t"])
        score = len(core) + (3 if core not in STOP else 0)
        if score > best:
            best, bi = score, i
    return bi


def build():
    words = load_words()
    if not words:
        raise SystemExit("no words in body range — check transcript")
    groups = group_words(words)
    data, external = [], []
    for gi, g in enumerate(groups):
        default_short = "ed" if (gi // RUN_LEN) % 2 == 0 else "mx"
        seg_idx = g[0]["seg"]
        override = STYLE_OVERRIDES.get(seg_idx)
        if override in EXTERNAL_STYLES:
            external.append({
                "seg": seg_idx, "style": override,
                "start": round(g[0]["s"] - BODY_START - 0.05, 3),
                "end": round(g[-1]["e"] - BODY_START, 3),
                "text": " ".join(w["t"] for w in g),
            })
            continue
        st = STYLE_SHORT.get(override, default_short)
        ei = emph_index(g) if st == "ed" else -1
        s = max(0.0, round(g[0]["s"] - BODY_START - 0.05, 3))
        data.append({
            "s": s,
            "raw_e": round(g[-1]["e"] - BODY_START, 3),
            "st": st,
            "ovr": override or None,
            "words": [{"t": w["t"], "emph": (i == ei)} for i, w in enumerate(g)],
        })
    for i, d in enumerate(data):
        d["e"] = data[i + 1]["s"] if i + 1 < len(data) else round(d["raw_e"] + 0.6, 3)
        del d["raw_e"]
    duration = round(data[-1]["e"] + 0.15, 2)
    return data, duration, external


DATA, DURATION, EXTERNAL_GROUPS = build()
counts = {}
for d in DATA:
    counts[d["st"]] = counts.get(d["st"], 0) + 1
print(f"{len(DATA)} body groups, styles: {counts}, duration {DURATION}s")
if EXTERNAL_GROUPS:
    with open("caption_external.json", "w", encoding="utf-8") as f:
        json.dump({"groups": EXTERNAL_GROUPS}, f, ensure_ascii=False, indent=2)
    print(f"{len(EXTERNAL_GROUPS)} external groups -> caption_external.json")

DATA_JSON = json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))

TEMPLATE = r"""<!doctype html>
<html lang="he" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Body Captions — Hebrew (Horizontal)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Rubik:wght@500;700;800;900&family=JetBrains+Mono:wght@700&display=swap"
      rel="stylesheet"
    />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      *, *::before, *::after { box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; margin: 0; overflow: hidden; background: transparent; }
      #caption-body { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: transparent; pointer-events: none; }
      #cb-stage { position: absolute; inset: 0; }
      .cg {
        position: absolute; left: 1180px; bottom: 96px;
        transform: translateX(-50%); transform-origin: 50% 100%;
        opacity: 0; will-change: transform, opacity;
      }
      /* base pill (liquid-glass) */
      .pill {
        position: relative; direction: rtl;
        display: flex; flex-wrap: nowrap; align-items: baseline; justify-content: center;
        gap: 0 18px; max-width: 1140px; white-space: nowrap;
        background: linear-gradient(168deg, rgba(52,54,78,0.78) 0%, rgba(18,19,30,0.83) 54%, rgba(9,10,17,0.87) 100%);
        border: 1.6px solid rgba(255,255,255,0.22);
        border-radius: 30px; padding: 20px 46px;
        box-shadow: 0 30px 72px rgba(0,0,0,0.55), inset 0 2px 0 rgba(255,255,255,0.42), inset 0 -18px 36px rgba(0,0,0,0.46);
        overflow: hidden;
      }
      .pill::before { content:""; position:absolute; left:0; right:0; top:0; height:52%;
        background: linear-gradient(180deg, rgba(255,255,255,0.24), rgba(255,255,255,0)); pointer-events:none; }
      .pill::after { content:""; position:absolute; inset:0; border-radius:30px;
        box-shadow: inset 0 0 26px rgba(255,255,255,0.07); pointer-events:none; }

      /* style: matrix */
      .pill.mx { border-color: rgba(0,255,120,0.42);
        box-shadow: 0 30px 72px rgba(0,0,0,0.55), 0 0 54px rgba(0,255,90,0.22),
          inset 0 2px 0 rgba(170,255,205,0.42), inset 0 -18px 36px rgba(0,0,0,0.46); }
      /* style: neon-glow */
      .pill.ng { border-color: rgba(255,61,166,0.6);
        box-shadow: 0 30px 72px rgba(0,0,0,0.55), 0 0 60px rgba(255,61,166,0.55), 0 0 120px rgba(255,61,166,0.35),
          inset 0 2px 0 rgba(255,200,230,0.55), inset 0 -18px 36px rgba(0,0,0,0.5); }
      /* style: marquee-rail (wide pill that slides) */
      .pill.mr { border-color: rgba(255,210,74,0.55); border-radius: 12px; }
      /* style: stamp-impact */
      .pill.si { border-color: rgba(255,90,140,0.55); border-radius: 0;
        box-shadow: 0 30px 72px rgba(0,0,0,0.55), 0 0 0 4px rgba(255,90,140,0.18), inset 0 2px 0 rgba(255,200,210,0.4); }
      /* style: glitch-rgb */
      .pill.gr { border-color: rgba(255,255,255,0.35); }
      /* style: soft-fade */
      .pill.sf { border-color: rgba(255,255,255,0.14);
        background: linear-gradient(168deg, rgba(20,22,32,0.55), rgba(8,9,16,0.65)); }
      /* style: highlight-marker — yellow stroke behind text */
      .pill.hm { border-color: rgba(255,210,74,0.32); }
      /* style: bold-underline */
      .pill.bu { border-color: rgba(255,255,255,0.18); }
      /* style: liquid-fill */
      .pill.lf { border-color: rgba(255,61,166,0.45); }
      /* style: split-reveal */
      .pill.sr { border-color: rgba(255,255,255,0.3); }
      /* style: mask-wipe */
      .pill.mw { border-color: rgba(0,200,255,0.45);
        box-shadow: 0 30px 72px rgba(0,0,0,0.55), 0 0 48px rgba(0,200,255,0.25),
          inset 0 2px 0 rgba(180,235,255,0.45), inset 0 -18px 36px rgba(0,0,0,0.46); }
      /* style: typewriter */
      .pill.tw { border-color: rgba(255,255,255,0.28); }

      /* word base */
      .w { display: inline-block; opacity: 0; line-height: 1.05; font-family: "Rubik", sans-serif; }
      /* editorial */
      .w-ed { font-weight: 700; font-size: 60px; color: #f5f0d0; }
      .w-ed-emph { font-weight: 900; font-size: 76px; color: #ffffff;
        text-shadow: 0 0 24px rgba(255,255,255,0.25); }
      /* matrix */
      .w-mx { font-weight: 800; font-size: 56px; color: #00ff41; letter-spacing: 0.01em;
        text-shadow: 0 0 22px rgba(0,255,65,0.5); font-family: "JetBrains Mono", monospace; }
      /* typewriter */
      .w-tw { font-weight: 700; font-size: 60px; color: #f5f0d0;
        font-family: "JetBrains Mono", monospace; letter-spacing: 0.04em; }
      .w-tw::after { content: "_"; color: #ffd24a; margin-right: 2px;
        animation: tw-caret 0.6s steps(2,end) infinite; }
      @keyframes tw-caret { 0%,49%{opacity:1} 50%,100%{opacity:0} }
      /* neon-glow */
      .w-ng { font-weight: 900; font-size: 68px; color: #fff;
        text-shadow: 0 0 6px #ff3da6, 0 0 16px #ff3da6, 0 0 38px rgba(255,61,166,0.85);
        animation: ng-pulse 1.4s ease-in-out infinite alternate; }
      @keyframes ng-pulse { from{filter:brightness(1)} to{filter:brightness(1.35)} }
      /* split-reveal — letters split top/bottom */
      .w-sr { font-weight: 900; font-size: 66px; color: #fff; }
      /* mask-wipe */
      .w-mw { font-weight: 800; font-size: 64px; color: #e6f6ff;
        text-shadow: 0 0 18px rgba(0,200,255,0.65); }
      /* marquee-rail */
      .w-mr { font-weight: 800; font-size: 60px; color: #ffd24a;
        text-shadow: 0 0 14px rgba(255,210,74,0.55); letter-spacing: 0.02em; }
      /* stamp-impact */
      .w-si { font-weight: 900; font-size: 78px; color: #fff;
        text-shadow: 3px 0 0 rgba(255,61,166,0.85), -3px 0 0 rgba(0,200,255,0.8); }
      /* liquid-fill */
      .w-lf { font-weight: 900; font-size: 66px;
        background-image: linear-gradient(180deg, #ffffff 0%, #ffd24a 45%, #ff3da6 100%);
        background-size: 100% 220%; background-position: 0 0;
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent; color: transparent; }
      /* glitch-rgb */
      .w-gr { font-weight: 900; font-size: 66px; color: #fff;
        text-shadow: 2px 0 0 #ff3da6, -2px 0 0 #00e5ff; }
      /* soft-fade */
      .w-sf { font-weight: 600; font-size: 54px; color: #f5f0d0; letter-spacing: 0.01em; }
      /* bold-underline */
      .w-bu { font-weight: 900; font-size: 64px; color: #fff;
        position: relative; padding-bottom: 6px; }
      .w-bu::after {
        content:""; position:absolute; left:0; right:100%; bottom:0; height:6px;
        background: linear-gradient(90deg, #ff3da6, #ffd24a); transition: right 0.18s ease;
      }
      .w-bu.lit::after { right: 0; }
      /* highlight-marker — yellow brush */
      .w-hm { font-weight: 800; font-size: 62px; color: #181820; position: relative; z-index: 1;
        padding: 0 4px; }
      .w-hm::before {
        content:""; position:absolute; left:0; right:100%; top: 18%; bottom: 10%;
        background: #ffd24a; transform: skewX(-8deg); z-index: -1;
        transition: right 0.22s ease;
      }
      .w-hm.lit::before { right: 0; }

      .sc, .rl { display: none; }
    </style>
  </head>
  <body>
    <div
      id="caption-body"
      data-composition-id="caption-body"
      data-timeline-locked
      data-start="0"
      data-duration="__DURATION__"
      data-fps="30"
      data-width="1920"
      data-height="1080"
    >
      <div id="cb-stage"></div>
    </div>
    <script>
      (function () {
        window.__timelines = window.__timelines || {};
        function mulberry32(a){return function(){a|=0;a=(a+0x6d2b79f5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
        var GLYPH="אבגדהוזחטיכלמנסעפצקרשתאבגדהוזחטיכ";
        function scr(seed,n){var r=mulberry32(seed),s="";for(var i=0;i<n;i++)s+=GLYPH[Math.floor(r()*GLYPH.length)];return s;}
        function fit(text, weight, max){var c=fit._c||(fit._c=document.createElement("canvas").getContext("2d"));var size=60,min=30;while(size>min){c.font=weight+" "+size+"px Rubik";if(c.measureText(text).width<=max)break;size-=2;}return size;}

        var DATA = __DATA__;
        var stage = document.getElementById("cb-stage");
        var tl = gsap.timeline({ paused: true });

        function buildLetters(text) {
          var frag = document.createDocumentFragment();
          for (var i = 0; i < text.length; i++) {
            var s = document.createElement("span");
            s.className = "ch";
            s.style.display = "inline-block";
            s.style.opacity = "0";
            s.textContent = text[i];
            frag.appendChild(s);
          }
          return frag;
        }

        DATA.forEach(function (g, gi) {
          var cg = document.createElement("div");
          cg.className = "cg"; cg.id = "cg-" + gi;
          var pill = document.createElement("div");
          pill.className = "pill " + g.st;
          var joined = g.words.map(function(w){return w.t;}).join(" ");
          var weight = (g.st === "mx" || g.st === "tw") ? "800" : (g.st === "sf" ? "600" : "700");
          var fs = fit(joined, weight, 1060);

          g.words.forEach(function (w, wi) {
            var sp = document.createElement("span");
            sp.id = "w-" + gi + "-" + wi;
            var cls = "w";
            if (g.st === "ed") {
              cls += " " + (w.emph ? "w-ed-emph" : "w-ed");
              sp.style.fontSize = (w.emph ? Math.round(fs * 1.26) : fs) + "px";
              sp.textContent = w.t;
            } else if (g.st === "mx") {
              cls += " w-mx"; sp.style.fontSize = fs + "px";
              var letters = w.t.replace(/[^֐-׿]/g, "");
              var n = Math.max(2, Math.min(7, letters.length || w.t.length));
              var rl = document.createElement("span"); rl.className = "rl"; rl.id = "rl-"+gi+"-"+wi; rl.textContent = w.t;
              var s0 = document.createElement("span"); s0.className = "sc"; s0.id = "s0-"+gi+"-"+wi; s0.textContent = scr(gi*97+wi, n);
              var s1 = document.createElement("span"); s1.className = "sc"; s1.id = "s1-"+gi+"-"+wi; s1.textContent = scr(gi*97+wi+5000, n);
              sp.appendChild(rl); sp.appendChild(s0); sp.appendChild(s1);
            } else if (g.st === "tw") {
              cls += " w-tw"; sp.style.fontSize = fs + "px";
              sp.appendChild(buildLetters(w.t));
            } else {
              cls += " w-" + g.st;
              sp.style.fontSize = fs + "px";
              sp.textContent = w.t;
            }
            sp.className = cls;
            pill.appendChild(sp);
          });
          cg.appendChild(pill); stage.appendChild(cg);
        });

        DATA.forEach(function (g, gi) {
          var cg = document.getElementById("cg-" + gi);
          var pill = cg.firstChild;

          // Group enter / exit (style-aware)
          var inDur = 0.46, outDur = 0.18, outAt = g.e;
          if (g.st === "sf") { inDur = 0.7; outDur = 0.45; }
          if (g.st === "si") { inDur = 0.28; outDur = 0.14; }
          if (g.st === "mr") { inDur = 0.55; outDur = 0.25; }
          if (g.st === "mw") { inDur = 0.6; outDur = 0.2; }
          if (g.st === "sr") { inDur = 0.5; outDur = 0.2; }

          var enterFrom = { opacity: 0, y: 32, scaleX: 1.16, scaleY: 0.72 };
          var enterTo   = { opacity: 1, y: 0, scaleX: 1, scaleY: 1, duration: inDur, ease: "elastic.out(1, 0.78)" };

          if (g.st === "si") {
            enterFrom = { opacity: 0, scaleX: 2.4, scaleY: 2.4, rotation: -4 };
            enterTo   = { opacity: 1, scaleX: 1, scaleY: 1, rotation: 0, duration: inDur, ease: "expo.out" };
          } else if (g.st === "mr") {
            enterFrom = { opacity: 0, x: 300, scaleX: 1.05 };
            enterTo   = { opacity: 1, x: 0, scaleX: 1, duration: inDur, ease: "power3.out" };
          } else if (g.st === "sr") {
            enterFrom = { opacity: 0, scaleY: 0.02 };
            enterTo   = { opacity: 1, scaleY: 1, duration: inDur, ease: "expo.out" };
          } else if (g.st === "mw") {
            enterFrom = { opacity: 1, clipPath: "polygon(0 0, 0 0, 0 100%, 0 100%)" };
            enterTo   = { opacity: 1, clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)", duration: inDur, ease: "power3.inOut" };
          } else if (g.st === "sf") {
            enterFrom = { opacity: 0, scale: 0.96 };
            enterTo   = { opacity: 1, scale: 1, duration: inDur, ease: "sine.out" };
          }
          tl.fromTo(cg, enterFrom, enterTo, g.s);

          // Per-word reveal
          g.words.forEach(function (w, wi) {
            var el = document.getElementById("w-" + gi + "-" + wi);
            var wt = g.s + 0.05 + wi * 0.07;

            if (g.st === "mx") {
              var rl = document.getElementById("rl-"+gi+"-"+wi);
              var s0 = document.getElementById("s0-"+gi+"-"+wi);
              var s1 = document.getElementById("s1-"+gi+"-"+wi);
              tl.set(el, { opacity: 1 }, wt);
              tl.set(s0, { display: "inline" }, wt);
              tl.set(s0, { display: "none" }, wt + 0.09);
              tl.set(s1, { display: "inline" }, wt + 0.09);
              tl.set(s1, { display: "none" }, wt + 0.18);
              tl.set(rl, { display: "inline" }, wt + 0.18);
            } else if (g.st === "tw") {
              tl.set(el, { opacity: 1 }, wt);
              var chs = el.querySelectorAll(".ch");
              chs.forEach(function (ch, ci) {
                tl.set(ch, { opacity: 1 }, wt + ci * 0.045);
              });
            } else if (g.st === "lf") {
              tl.set(el, { opacity: 1 }, wt);
              tl.fromTo(el, { backgroundPosition: "0 100%" }, { backgroundPosition: "0 0", duration: 0.32, ease: "power2.out" }, wt);
            } else if (g.st === "bu" || g.st === "hm") {
              tl.fromTo(el, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }, wt);
              tl.call(function (e) { e.classList.add("lit"); }, [el], wt + 0.05);
            } else if (g.st === "gr") {
              tl.fromTo(el, { opacity: 0, x: -10 }, { opacity: 1, x: 0, duration: 0.18, ease: "power2.out" }, wt);
              tl.to(el, { x: 4, duration: 0.04, yoyo: true, repeat: 3 }, wt + 0.02);
            } else if (g.st === "si") {
              tl.fromTo(el, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.16, ease: "power4.out" }, wt);
            } else if (g.st === "mr") {
              tl.fromTo(el, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.22, ease: "power2.out" }, wt);
            } else if (g.st === "sf") {
              tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "sine.out" }, wt);
            } else if (g.st === "sr") {
              tl.fromTo(el, { opacity: 0, y: -18 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, wt);
            } else if (g.st === "mw") {
              tl.set(el, { opacity: 1 }, wt);
            } else if (g.st === "ng") {
              tl.fromTo(el, { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(1.6)" }, wt);
            } else {
              tl.fromTo(el, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.22, ease: "power2.out" }, wt);
            }
          });

          // Exit
          if (g.st === "mw") {
            tl.to(cg, { opacity: 0, clipPath: "polygon(100% 0, 100% 0, 100% 100%, 100% 100%)", duration: outDur, ease: "power3.in" }, outAt - outDur);
          } else if (g.st === "mr") {
            tl.to(cg, { opacity: 0, x: -300, duration: outDur, ease: "power2.in" }, outAt - outDur);
          } else if (g.st === "sf") {
            tl.to(cg, { opacity: 0, scale: 1.03, duration: outDur, ease: "sine.in" }, outAt - outDur);
          } else if (g.st === "sr") {
            tl.to(cg, { opacity: 0, scaleY: 0.02, duration: outDur, ease: "power3.in" }, outAt - outDur);
          } else {
            tl.to(cg, { opacity: 0, y: -20, scaleY: 0.8, duration: outDur, ease: "power2.in" }, outAt - outDur);
          }
          tl.set(cg, { opacity: 0, visibility: "hidden" }, outAt);
        });

        window.__timelines["caption-body"] = tl;
      })();
    </script>
  </body>
</html>
"""

html = TEMPLATE.replace("__DURATION__", str(DURATION)).replace("__DATA__", DATA_JSON)
with io.open("compositions/components/caption-body.html", "w", encoding="utf-8") as f:
    f.write(html)
print("wrote compositions/components/caption-body.html")
