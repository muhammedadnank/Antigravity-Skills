import React from 'react';

/**
 * Full-bleed background image with Ken-Burns pan + customisable overlay.
 *
 *   <HeroBg
 *     src={myImage}
 *     overlay={`linear-gradient(180deg, rgba(241,242,242,0.6), rgba(241,242,242,0.95))`}
 *   />
 *
 * The overlay is mandatory in practice — without it, headlines lose contrast.
 * Pair with a Ken-Burns CSS keyframe `yuv-kenBurns` (see keyframes.css).
 */
export const HeroBg: React.FC<{
  src: string;
  overlay?: string;
  reverse?: boolean;
  zIndex?: number;
}> = ({ src, overlay, reverse, zIndex = 0 }) => (
  <>
    <div
      aria-hidden
      style={{
        position: 'absolute',
        inset: 0,
        zIndex,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          position: 'absolute',
          inset: '-6%',
          backgroundImage: `url(${src})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          animation: `${reverse ? 'yuv-kenBurnsR' : 'yuv-kenBurns'} 22s ease-in-out infinite`,
          filter: 'saturate(1.05) contrast(1.04)',
        }}
      />
    </div>
    {overlay && (
      <div
        aria-hidden
        style={{
          position: 'absolute',
          inset: 0,
          zIndex: zIndex + 1,
          background: overlay,
          pointerEvents: 'none',
        }}
      />
    )}
  </>
);
