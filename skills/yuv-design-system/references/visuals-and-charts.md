# Visuals, infographics & charts — thinking in pictures

Yuval prefers visual explanation over prose wherever possible. This file covers chart skinning, infographic patterns, dynamic diagrams, and big-stat layouts — all in the YUV.AI palette.

**Default principle:** if something can be a chart, a diagram, or a counter, it should be. Prose is the fallback, not the lead.

---

## Color encoding (do not deviate)

### Fly High mode (default)

| Role | Hex | When |
|---|---|---|
| Primary series / "us" / current state | `#5E17EB` (purple) | The line / bar / segment that's the story |
| Highlight / hero data point / "after" | `#FFEC00` (yellow) | The one stat that matters most |
| Secondary series (1) | `#3D0DA8` (purple-dark) | When you need a second purple-family series |
| Secondary series (2) | `#1A1A1A` (charcoal) | Neutral comparator |
| Tertiary / "background" series | `#D4D6D6` (grey-dark) | Quiet comparator / context series |
| Grid / axes | `rgba(0,0,0,0.10)` | Always faint, never coloured |
| Axis labels | `#000` Anton uppercase 11px tracking 0.2em | Style of every label |
| Tick numbers | `#1A1A1A` Inter 500 12px | Quiet but readable |

### Warm Editorial mode

| Role | Hex | When |
|---|---|---|
| Primary series | `#FF1464` (pink) | The story line / bar |
| Highlight | `#E5FF00` (yellow) | The hero stat |
| Secondary | `#1A1A1A` / `#8B8680` (charcoal / warm-gray) | Neutral / quiet |
| Grid | `rgba(10,10,10,0.10)` | |

### Banned

- Rainbow / categorical-with-many-colors palettes (`d3.schemeCategory10`, Chart.js default rainbow). Pick categorical OR sequential, never both.
- Blue, slate, indigo, emerald, cyan, anything from default chart palettes.
- Coloured gridlines.
- 3D bar charts.
- Pie charts with > 4 slices. Convert to bar chart or treemap.
- Glossy / 3D effects on data marks.

---

## Type rules on visuals

- **Section titles above a chart:** Anton uppercase, `0` tracking (default), 36–56px.
- **Axis labels:** Anton uppercase, 11–12px, tracking `0.2em`. Color `#000` or `#fff` depending on background.
- **Tick numbers / scale values:** Inter 500, 11–13px.
- **Big stats (CounterUp):** Anton, 120–200px, line-height 1.0, color depends on background. Pair with a small Inter 400 caption underneath at 14–18px.
- **Raw readouts / data tables / instrument values:** JetBrains Mono, 11–16px, weight 500 or 700.

---

## Chart.js drop-in skinning (Fly High)

```html
<canvas id="chart" width="800" height="420"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
Chart.defaults.font.family = "'Inter', 'Assistant', sans-serif";
Chart.defaults.color = '#1A1A1A';

new Chart(document.getElementById('chart'), {
  type: 'bar',
  data: {
    labels: ['Q1','Q2','Q3','Q4'],
    datasets: [
      { label: 'Last year', data: [120,135,140,150], backgroundColor: '#D4D6D6', borderRadius: 0, borderSkipped: false },
      { label: 'This year', data: [180,210,240,290], backgroundColor: '#5E17EB', borderRadius: 0, borderSkipped: false },
    ]
  },
  options: {
    plugins: {
      legend: {
        position: 'top', align: 'start',
        labels: {
          font: { family: "'Anton', sans-serif", size: 14 },
          color: '#000', boxWidth: 14, boxHeight: 14, padding: 18
        }
      },
      tooltip: { titleFont: { family: 'JetBrains Mono' }, bodyFont: { family: 'JetBrains Mono' } }
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { family: "'Anton', sans-serif", size: 12 }, color: '#000' }
      },
      y: {
        beginAtZero: true,
        grid: { color: 'rgba(0,0,0,0.06)', drawBorder: false },
        ticks: { font: { family: 'JetBrains Mono', size: 11 }, color: '#1A1A1A' }
      }
    }
  }
});
</script>
```

**To highlight one bar / point as hero:** swap that bar's `backgroundColor` to `#FFEC00`. Always pair the highlight with a labeled annotation pointing to it (`chartjs-plugin-annotation`).

---

## recharts override (React)

```tsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Q1', last: 120, current: 180 },
  { name: 'Q2', last: 135, current: 210 },
  { name: 'Q3', last: 140, current: 240 },
  { name: 'Q4', last: 150, current: 290 },
];

export function QuarterlyChart() {
  return (
    <ResponsiveContainer width="100%" height={420}>
      <BarChart data={data} margin={{ top: 24, right: 24, bottom: 24, left: 0 }}>
        <CartesianGrid stroke="rgba(0,0,0,0.06)" vertical={false} />
        <XAxis dataKey="name" axisLine={false} tickLine={false}
               tick={{ fontFamily: 'Anton, sans-serif', fontSize: 12, fill: '#000', letterSpacing: '0.2em' }} />
        <YAxis axisLine={false} tickLine={false}
               tick={{ fontFamily: 'JetBrains Mono', fontSize: 11, fill: '#1A1A1A' }} />
        <Tooltip contentStyle={{ fontFamily: 'JetBrains Mono', border: '1px solid #000', borderRadius: 0 }} />
        <Legend wrapperStyle={{ fontFamily: 'Anton, sans-serif', textTransform: 'uppercase' }} />
        <Bar dataKey="last" fill="#D4D6D6" radius={0} />
        <Bar dataKey="current" fill="#5E17EB" radius={0} />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

---

## The big-stat pattern (slide / hero / report cover)

When a single number IS the story, dedicate the surface to it. Combine `<CounterUp>` with an Anton headline and a small JetBrains-Mono caption.

```tsx
import { CounterUp } from './components/CounterUp';

<section style={{ background: '#F1F2F2', minHeight: '100vh', display: 'grid', placeItems: 'center', padding: 100 }}>
  <div style={{ textAlign: 'center' }}>
    <span style={{ fontFamily: 'JetBrains Mono', fontSize: 13, letterSpacing: '0.3em', color: '#5E17EB', fontWeight: 700 }}>
      AVERAGE WIN RATE · MAY 2026
    </span>
    <div style={{ marginTop: 32, fontFamily: 'Anton, sans-serif', fontSize: 240, lineHeight: 1, letterSpacing: '-0.01em', color: '#000' }}>
      <CounterUp to={94} />
      <span style={{ color: '#5E17EB' }}>%</span>
    </div>
    <p style={{ marginTop: 24, fontFamily: 'Inter, sans-serif', fontSize: 22, color: 'rgba(0,0,0,0.7)' }}>
      Up from <span style={{ color: '#5E17EB', fontWeight: 700 }}>71%</span> last quarter.
    </p>
  </div>
</section>
```

---

## Infographic patterns

### 1. The "before / after" split

Horizontal split, 50/50. Left half is the old state (grey + charcoal). Right half is the new state (purple + yellow accent). Anton label in the corner of each half.

### 2. The "from X to Y" arrow

A single big number, an Anton arrow → glyph at 0.6 the headline size, then the second number. Use yellow for the after-number, charcoal for the before-number.

### 3. The progress / journey arc

For "stages of a process" or "phases of a journey", use a 5–7 step horizontal bar with circular nodes. Current step in yellow, completed steps in purple, upcoming in charcoal-grey. Anton labels above each node.

### 4. The hierarchy / org diagram

Boxes are pure rectangles (radius 0). Lines are 1px charcoal. The "root" or "key" node gets the purple left-border treatment from the standard card pattern (`border-left: 4px solid #5E17EB`). Labels in Anton uppercase.

### 5. Isometric scene

For "how it works" diagrams. Use isometric projection (30° / 30° / 90°). Color in the brand palette only — purple as primary surface, yellow as accent or "active" highlight, charcoal for edges, grey-dark for shadows. Inline SVG so it scales infinitely.

### 6. Sankey / flow diagram

D3 sankey. All "flow" links default to purple at 25% opacity. The hero flow (the one the story is about) gets bumped to yellow at 80% opacity. Nodes are flat purple rectangles.

---

## What NOT to ship as a visual

- Generic Excel-default charts (Calibri labels, default colors, gridlines everywhere).
- Word-cloud "tag soup" — no information density.
- Stock infographics from FlatIcon / Freepik / etc.
- 3D effects on data.
- Glow / blur / drop-shadow on data marks.
- Multi-color rainbow palettes that don't encode anything meaningful.
- Pie charts that need a legend with > 5 entries.
- Donut charts with center text in a font other than Anton.
- Time series with mismatched scales on dual Y-axes.

---

## When to use which library

| Need | Tool |
|---|---|
| Quick bar / line / area chart in React | recharts |
| Quick bar / line / area chart in vanilla HTML | Chart.js |
| Bespoke interactive infographic | D3 + GSAP |
| Static infographic for slide / image / print | inline SVG (hand-built) |
| Dynamic dashboard with many panels | recharts + react-grid-layout |
| Sankey / sunburst / chord | D3 |
| Animated number counter | `<CounterUp>` (in `components/CounterUp.tsx`) |
| Big stat slide | Anton + `<CounterUp>` |
| Map / geo | Mapbox GL with a custom dark/light style — never default colors |
| Force-directed network | D3 + canvas (perf at > 200 nodes) |

---

## Self-check before shipping a visual

1. Palette is brand-only — no default chart colors leaked.
2. Hero data point is yellow (and labeled).
3. Type is in the system fonts — Anton headers, Inter body, JetBrains Mono readouts.
4. Gridlines are faint and uncoloured.
5. Axes have Anton uppercase labels with tracking.
6. The visual answers "what am I looking at?" in < 3 seconds.
7. If it's a stat, there's a `<CounterUp>` animating the number on view.
8. If it'll be screenshotted or shared, the brand watermark (`logo-rectangle-wordmark.png`) sits in the bottom-right corner.
