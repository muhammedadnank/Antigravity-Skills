import React from 'react';

/**
 * Cockpit compass dial. Decorative — use sparingly on hero / divider slides.
 *
 *   <CompassDial size={220} heading={287} />
 */
export const CompassDial: React.FC<{
  size?: number;
  heading?: number;
  bg?: string;
  ring?: string;
  needle?: string;
  text?: string;
}> = ({
  size = 240,
  heading = 287,
  bg = 'rgba(0,0,0,0.4)',
  ring = '#FFEC00',
  needle = '#FFEC00',
  text = '#FFFFFF',
}) => (
  <svg viewBox="0 0 200 200" width={size} height={size}>
    <circle cx="100" cy="100" r="96" fill={bg} stroke={ring} strokeWidth="2" />
    <circle cx="100" cy="100" r="76" fill="none" stroke={ring} strokeWidth="1" opacity="0.5" />
    {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map((a) => (
      <line
        key={a}
        x1="100"
        y1="10"
        x2="100"
        y2={a % 90 === 0 ? '24' : '18'}
        stroke={ring}
        strokeWidth={a % 90 === 0 ? 2 : 1}
        transform={`rotate(${a} 100 100)`}
      />
    ))}
    {[
      ['N', 0],
      ['E', 90],
      ['S', 180],
      ['W', 270],
    ].map(([letter, ang]) => {
      const rad = ((ang as number) - 90) * (Math.PI / 180);
      return (
        <text
          key={letter as string}
          x={100 + 78 * Math.cos(rad)}
          y={100 + 78 * Math.sin(rad) + 5}
          fill={text}
          fontSize="14"
          fontFamily="Inter, sans-serif"
          fontWeight="700"
          textAnchor="middle"
        >
          {letter}
        </text>
      );
    })}
    <g
      style={{
        transformOrigin: '100px 100px',
        animation: 'yuv-needleSweep 6s ease-in-out infinite',
      }}
    >
      <polygon
        points="100,30 92,108 100,100 108,108"
        fill={needle}
        transform={`rotate(${heading} 100 100)`}
      />
    </g>
    <circle cx="100" cy="100" r="6" fill={ring} />
    <text
      x="100"
      y="160"
      fill={text}
      fontSize="13"
      fontFamily='"JetBrains Mono", monospace'
      letterSpacing="0.2em"
      textAnchor="middle"
    >
      HDG {heading}°
    </text>
  </svg>
);
