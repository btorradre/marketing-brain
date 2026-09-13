import { TICK_RATE, type Tick } from './types.js';

export { TICK_RATE };

export function secondsToTicks(seconds: number): Tick {
  return Math.round(seconds * TICK_RATE);
}

export function ticksToSeconds(ticks: Tick): number {
  return ticks / TICK_RATE;
}

export function msToTicks(ms: number): Tick {
  return Math.round((ms * TICK_RATE) / 1000);
}

export function ticksToMs(ticks: Tick): number {
  return (ticks * 1000) / TICK_RATE;
}

/** Ticks for `frames` whole frames at `fps`. Exact for every fps that divides TICK_RATE. */
export function framesToTicks(frames: number, fps: number): Tick {
  return Math.round((frames * TICK_RATE) / fps);
}

/** Zero-based frame index containing `ticks` at `fps`. */
export function ticksToFrame(ticks: Tick, fps: number): number {
  return Math.floor((ticks * fps) / TICK_RATE);
}

/** Snap a tick to the start of its frame. */
export function snapToFrame(ticks: Tick, fps: number): Tick {
  return framesToTicks(ticksToFrame(ticks, fps), fps);
}

/** True when one frame at `fps` is a whole number of ticks. */
export function isFrameExact(fps: number): boolean {
  return Number.isInteger(TICK_RATE / fps);
}

/** Timecode string HH:MM:SS:FF for display. */
export function toTimecode(ticks: Tick, fps: number): string {
  const totalFrames = ticksToFrame(ticks, fps);
  const f = totalFrames % fps;
  const totalSeconds = Math.floor(totalFrames / fps);
  const s = totalSeconds % 60;
  const m = Math.floor(totalSeconds / 60) % 60;
  const h = Math.floor(totalSeconds / 3600);
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${pad(h)}:${pad(m)}:${pad(s)}:${pad(f)}`;
}
