import React from 'react';

/**
 * Vertical purple accent bar — sits to the left of content-slide headlines.
 * The single most consistent brand mark in the YUV.AI design system.
 *
 *   <div style={{ display: 'flex', alignItems: 'center' }}>
 *     <PurpleBar height={96} />
 *     <h2>The flight plan.</h2>
 *   </div>
 */
export const PurpleBar: React.FC<{
  height?: number;
  width?: number;
  offset?: number;
  color?: string;
}> = ({ height = 96, width = 8, offset = 0, color = '#5E17EB' }) => (
  <span
    aria-hidden
    style={{
      display: 'inline-block',
      width,
      height,
      background: color,
      marginRight: 28,
      transform: `translateY(${offset}px)`,
      verticalAlign: 'middle',
      flexShrink: 0,
    }}
  />
);
