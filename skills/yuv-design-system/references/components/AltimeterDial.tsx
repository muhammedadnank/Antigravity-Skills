import React from 'react';

/**
 * Cockpit altimeter dial. Companion to CompassDial — same visual language.
 *
 *   <AltimeterDial size={220} alt={35400} />
 */
export const AltimeterDial: React.FC<{
  size?: number;
  alt?: number;
  bg?: string;
  ring?: string;
  needle?: string;
  text?: string;
}> = ({
  size = 240,
  alt = 35000,
  bg = 'rgba(0,0,0,0.4)',
  ring = '#FFEC00',
  needle = '#FFEC00',
  text = '#FFFFFF',
}) => {
  const rotation = ((alt % 1000) / 1000) * 360;
  return (
    <svg viewBox="0 0 200 200" width={size} height={size}>
      <circle cx="100" cy="100" r="96" fill={bg} stroke={ring} strokeWidth="2" />
      {Array.from({ length: 10 }, (_, i) => i * 36).map((a) => (
        <line
          key={a}
          x1="100"
          y1="10"
          x2="100"
          y2="22"
          stroke={ring}
          strokeWidth="1.5"
          transform={`rotate(${a} 100 100)`}
        />
      ))}
      {Array.from({ length: 10 }, (_, i) => i * 36).map((a, i) => {
        const rad = (a - 90) * (Math.PI / 180);
        return (
          <text
            key={i}
            x={100 + 78 * Math.cos(rad)}
            y={100 + 78 * Math.sin(rad) + 5}
            fill={text}
            fontSize="13"
            fontFamily='"JetBrains Mono", monospace'
            fontWeight="600"
            textAnchor="middle"
          >
            {i}
          </text>
        );
      })}
      <polygon
        points="100,28 95,100 100,108 105,100"
        fill={needle}
        transform={`rotate(${rotation} 100 100)`}
        style={{ transition: 'transform 2s ease-out' }}
      />
      <circle cx="100" cy="100" r="6" fill={ring} />
      <text
        x="100"
        y="160"
        fill={text}
        fontSize="13"
        fontFamily='"JetBrains Mono", monospace'
        letterSpacing="0.18em"
        textAnchor="middle"
      >
        ALT {alt.toLocaleString()}
      </text>
    </svg>
  );
};
