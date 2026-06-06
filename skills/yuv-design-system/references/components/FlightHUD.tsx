import React from 'react';

/**
 * Bottom flight-simulator HUD strip. Sits below every slide as a running
 * status bar — progress bar + flight phase + instrument readouts + counter.
 *
 *   <FlightHUD n={12} total={23} cite="The 7 Traps" tone="purple" />
 *
 * Values progress over the deck via flightStatus() — pre-flight → climb →
 * cruise → descent → landed.
 */

export type FlightTone = 'content' | 'purple';

type Phase = {
  phase: string;
  alt: number;
  spd: number;
  hdg: number;
  fuel: number;
};

/**
 * Default journey shape — pre-flight → climb → cruise → descent → landed
 * across N steps. Override by passing your own `status` prop.
 */
export function defaultFlightStatus(n: number, total = 23): Phase {
  // 23-step default. Adapt for shorter/longer decks by scaling.
  const phases: Array<[number, Phase]> = [
    [1,  { phase: 'PRE-FLIGHT', alt: 0,      spd: 0,   hdg: 287, fuel: 100 }],
    [2,  { phase: 'TAXI',       alt: 0,      spd: 28,  hdg: 287, fuel: 99 }],
    [3,  { phase: 'TAKEOFF',    alt: 850,    spd: 165, hdg: 290, fuel: 98 }],
    [5,  { phase: 'CLIMB',      alt: 9100,   spd: 280, hdg: 294, fuel: 95 }],
    [9,  { phase: 'CRUISE',     alt: 33800,  spd: 472, hdg: 302, fuel: 85 }],
    [12, { phase: 'CRUISE',     alt: 35400,  spd: 484, hdg: 308, fuel: 76 }],
    [15, { phase: 'CRUISE',     alt: 35400,  spd: 484, hdg: 308, fuel: 67 }],
    [19, { phase: 'CRUISE',     alt: 35400,  spd: 484, hdg: 308, fuel: 55 }],
    [20, { phase: 'DESCENT',    alt: 24600,  spd: 410, hdg: 312, fuel: 50 }],
    [21, { phase: 'DESCENT',    alt: 12400,  spd: 320, hdg: 314, fuel: 46 }],
    [22, { phase: 'FINAL',      alt: 2200,   spd: 180, hdg: 316, fuel: 43 }],
    [23, { phase: 'LANDED',     alt: 0,      spd: 0,   hdg: 0,   fuel: 41 }],
  ];
  // Find closest defined phase ≤ n
  let last = phases[0][1];
  for (const [num, p] of phases) {
    if (num <= n) last = p;
    else break;
  }
  return last;
}

export const FlightHUD: React.FC<{
  n: number;
  total?: number;
  cite?: string;
  tone?: FlightTone;
  status?: Phase;
  flightId?: string;
}> = ({ n, total = 23, cite, tone = 'content', status, flightId = 'FH-YUV-AI' }) => {
  const onPurple = tone === 'purple';
  const s = status ?? defaultFlightStatus(n, total);
  const pct = (n / total) * 100;

  const txt = onPurple ? '#FFFFFF' : '#000000';
  const dim = onPurple ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.55)';
  const accent = onPurple ? '#FFEC00' : '#5E17EB';
  const borderColor = onPurple ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.12)';
  const cellBg = onPurple ? 'rgba(255,255,255,0.06)' : '#FFFFFF';

  const Cell: React.FC<{ label: string; value: string; unit?: string }> = ({ label, value, unit }) => (
    <div
      style={{
        background: cellBg,
        border: `1px solid ${borderColor}`,
        padding: '6px 14px',
        minWidth: 92,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <span
        style={{
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: 9,
          color: dim,
          letterSpacing: '0.2em',
          fontWeight: 700,
        }}
      >
        {label}
      </span>
      <span
        style={{
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: 16,
          color: txt,
          fontWeight: 700,
          letterSpacing: '0.04em',
          marginTop: 2,
        }}
      >
        {value}
        {unit && <span style={{ fontSize: 10, color: dim, marginLeft: 4 }}>{unit}</span>}
      </span>
    </div>
  );

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 5,
      }}
    >
      {/* Progress bar */}
      <div
        style={{
          position: 'relative',
          height: 6,
          background: onPurple ? 'rgba(255,255,255,0.10)' : 'rgba(0,0,0,0.06)',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: '0 auto 0 0',
            width: `${pct}%`,
            background: 'linear-gradient(90deg, #5E17EB 0%, #FFEC00 100%)',
          }}
        />
      </div>
      {/* HUD strip */}
      <div
        style={{
          padding: '14px 100px 18px',
          background: onPurple ? 'rgba(0,0,0,0.20)' : 'rgba(255,255,255,0.65)',
          backdropFilter: 'blur(4px)',
          WebkitBackdropFilter: 'blur(4px)',
          borderTop: `1px solid ${borderColor}`,
          display: 'grid',
          gridTemplateColumns: '1fr auto 1fr',
          alignItems: 'center',
          gap: 24,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <span
            style={{
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: 11,
              color: accent,
              letterSpacing: '0.3em',
              fontWeight: 700,
              padding: '3px 10px',
              border: `1px solid ${accent}`,
            }}
          >
            ◉ {s.phase}
          </span>
          {cite && (
            <span
              style={{
                fontFamily: '"JetBrains Mono", monospace',
                fontSize: 11,
                color: dim,
                letterSpacing: '0.06em',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                maxWidth: 540,
              }}
            >
              {cite}
            </span>
          )}
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <Cell label="ALT" value={s.alt.toLocaleString()} unit="ft" />
          <Cell label="SPD" value={String(s.spd)} unit="kt" />
          <Cell label="HDG" value={s.hdg ? `${s.hdg}°` : '— —'} />
          <Cell label="FUEL" value={`${s.fuel}%`} />
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 12 }}>
          <span
            style={{
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: 11,
              color: dim,
              letterSpacing: '0.2em',
              fontWeight: 600,
            }}
          >
            FLIGHT {flightId}
          </span>
          <span
            style={{
              fontFamily: 'Anton, sans-serif',
              fontSize: 22,
              color: txt,
              letterSpacing: '0.02em',
            }}
          >
            {String(n).padStart(2, '0')}
            <span style={{ color: dim }}> / {total}</span>
          </span>
        </div>
      </div>
    </div>
  );
};
