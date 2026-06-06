import React from 'react';

/**
 * Hand-drawn SVG yellow underline. Sits under ONE specific word for emphasis.
 *
 *   <span style={{ position: 'relative', display: 'inline-block' }}>
 *     <span style={{ position: 'relative', zIndex: 2 }}>explode.</span>
 *     <YellowUnderline width={210}
 *       style={{ position: 'absolute', left: -4, bottom: -16, zIndex: 1 }} />
 *   </span>
 *
 * Sizing: width should match the underlined word's rendered width.
 * Don't float decoratively — it should always anchor a specific word.
 */
export const YellowUnderline: React.FC<{
  width?: number;
  color?: string;
  strokeWidth?: number;
  style?: React.CSSProperties;
}> = ({ width = 360, color = '#FFEC00', strokeWidth = 10, style }) => (
  <svg
    viewBox="0 0 360 24"
    width={width}
    height={(24 * width) / 360}
    style={style}
    aria-hidden
  >
    <path
      d="M 8 16 C 70 6, 140 22, 200 12 S 320 4, 352 14"
      stroke={color}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      fill="none"
    />
  </svg>
);
