/** YUV.AI "Fly High" design system — Tailwind preset
 *
 *  // tailwind.config.js
 *  module.exports = {
 *    presets: [require('./tokens/tailwind.config.js')],
 *    content: ['./src/**\/*.{ts,tsx,html}'],
 *  };
 */

module.exports = {
  theme: {
    extend: {
      colors: {
        // Brand
        purple:       '#5E17EB',
        'purple-dark':'#3D0DA8',
        yellow:       '#FFEC00',
        // Surfaces
        grey:         '#F1F2F2',
        'grey-dark':  '#D4D6D6',
        bone:         '#FAFAF7',
        // Keep black/white explicit so we never default to Tailwind's slate/zinc
        black:        '#000000',
        white:        '#FFFFFF',
      },
      fontFamily: {
        display: ['Anton', 'Rubik', 'sans-serif'],
        body:    ['Inter', 'Assistant', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"SF Mono"', 'ui-monospace', 'Menlo', 'monospace'],
      },
      letterSpacing: {
        tightest: '-0.04em',
        tighter:  '-0.03em',
        wide:     '0.04em',
        wider:    '0.20em',
        widest:   '0.32em',
      },
      borderRadius: {
        // Yuval system uses 0 or 999px — nothing in between
        none: '0',
        pill: '9999px',
      },
      boxShadow: {
        card:   '0 8px 24px rgba(0,0,0,0.05)',
        'card-hover': '0 16px 40px rgba(0,0,0,0.08)',
        // No coloured shadows. No blue-black.
      },
      maxWidth: {
        content: '1440px',
      },
    },
  },
  plugins: [],
};
