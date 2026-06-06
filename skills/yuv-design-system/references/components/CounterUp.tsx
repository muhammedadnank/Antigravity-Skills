import React from 'react';

/**
 * Animated number counter. Counts from 0 to `to` with ease-out cubic.
 *
 *   <CounterUp to={95} duration={1600} />
 *
 * Pairs nicely with a big Anton % sign for stat slides.
 */
export const CounterUp: React.FC<{
  to: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  style?: React.CSSProperties;
}> = ({ to, duration = 1400, prefix = '', suffix = '', style }) => {
  const [val, setVal] = React.useState(0);
  React.useEffect(() => {
    let raf = 0;
    const t0 = performance.now();
    const tick = (t: number) => {
      const elapsed = t - t0;
      const p = Math.min(1, elapsed / duration);
      const eased = 1 - Math.pow(1 - p, 3); // ease-out cubic
      setVal(Math.round(to * eased));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [to, duration]);
  return (
    <span style={style}>
      {prefix}
      {val}
      {suffix}
    </span>
  );
};
