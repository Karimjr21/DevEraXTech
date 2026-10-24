import { inv, smooth } from '../lib/util.js';
import { drawTitle, FONT } from '../lib/text.js';
import { brandStage } from './s09-reveal.js';

// SCENE 10 · 00:33–00:36 · The memory anchor.
// The mark holds; the line and the address arrive beneath it; a single silver
// reflection crosses the mark. The core then resolves the frame into Scene 01's first
// frame so the film loops seamlessly.

export const SHEEN = [34.0, 35.05];

export default function (ctx) {
  const st = brandStage(ctx);
  function overlay(g, t, alpha) {
    // final resolve: the mark lets go into pure obsidian, the state the loop returns from
    alpha *= 1 - smooth(35.3, 35.88, t);
    g.globalAlpha = alpha;
    st.drawLogo(g, alpha, t >= SHEEN[0] && t <= SHEEN[1] ? inv(SHEEN[0], SHEEN[1], t) : -1);
    st.drawWordmark(g, 1, alpha);
    g.globalAlpha = alpha;
    drawTitle(g, ctx.W, t, {
      lines: ['ENGINEERED EXCELLENCE.'], start: 33.1, end: 40, y: 1250, size: 34, family: FONT.medium,
      tracking: 0.34, cx: 540, shadow: 0, inDur: 0.7,
    });
    drawTitle(g, ctx.W, t, {
      lines: ['deveraxtech.com'], start: 33.5, end: 40, y: 1325, size: 30, family: FONT.regular,
      tracking: 0.12, cx: 540, shadow: 0, color: '141,147,155', inDur: 0.7,
    });
    g.globalAlpha = 1;
  }
  return { start: 33, end: 36.5, update: st.update, overlay };
}
