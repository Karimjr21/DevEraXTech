import * as THREE from 'three';
import { clamp, ease, inv, lerp, rng, smooth } from '../lib/util.js';
import { canvas } from '../lib/surfaces.js';
import { motes } from '../lib/motes.js';

// SCENE 09 · 00:28–00:33 · The brand reveal.
// Tiny metallic fragments aggregate onto the exact pixels of the official DevEraXTech
// mark, then hand over to the untouched logo artwork, composited 1:1. The wordmark is
// typeset, never generated. Scene 10 reuses this stage so the composition never jumps.

export const LOGO = { cx: 540, cy: 800, w: 600 }; // 1080-space layout of the official mark
export const LOCK = 30.3;    // particles hand over to the artwork here (sonic logo note 1)
export const WORD_IN = 30.55;

let stage = null;

export function brandStage(ctx) {
  if (stage) return stage;
  const { W, H } = ctx;
  const k = W / 1080;
  const crop = ctx.logoCrop;
  const lw = LOGO.w, lh = (LOGO.w * crop.h) / crop.w;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, ctx.aspect, 0.05, 60);
  const D = 5;
  camera.position.set(0, 0, D);
  camera.lookAt(0, 0, 0);
  camera.updateMatrixWorld();
  const viewH = 2 * D * Math.tan(THREE.MathUtils.degToRad(15));
  const toWorld = (px, py) => new THREE.Vector3(((px - 540) / 1920) * viewH * (1080 / W) * (W / 1080), ((960 - py) / 1920) * viewH, 0);

  // Obsidian backdrop: a restrained radial lift behind the mark.
  const bg = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({
    depthWrite: false, depthTest: false, toneMapped: false,
    uniforms: { uA: { value: 1 } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.999, 1.0); }',
    fragmentShader: `uniform float uA; varying vec2 vUv;
      void main(){ vec2 q = vUv - vec2(0.5, 0.56); q.x *= ${(W / H).toFixed(4)};
        float r = length(q);
        vec3 c = mix(vec3(0.019, 0.021, 0.026), vec3(0.0026, 0.0029, 0.0036), smoothstep(0.0, 0.62, r));
        gl_FragColor = vec4(c * uA, 1.0); }`,
  }));
  bg.renderOrder = -10;
  bg.frustumCulled = false;
  scene.add(bg);

  // Sample the official artwork's own pixels: positions and colours.
  const SW = Math.round(lw), SH = Math.round(lh);
  const sc = canvas(SW, SH), sg = sc.getContext('2d', { willReadFrequently: true });
  sg.drawImage(ctx.logo, crop.x, crop.y, crop.w, crop.h, 0, 0, SW, SH);
  const img = sg.getImageData(0, 0, SW, SH).data;
  const r = rng(9909);
  const tgt = [], col = [], start = [], arr = [], seed = [];
  const step = 2;
  for (let y = 0; y < SH; y += step) {
    for (let x = 0; x < SW; x += step) {
      const i = (y * SW + x) * 4;
      if (img[i + 3] < 110) continue;
      const px = LOGO.cx - lw / 2 + x + 0.5, py = LOGO.cy - lh / 2 + y + 0.5;
      const w = toWorld(px, py);
      tgt.push(w.x, w.y, 0);
      col.push(...[img[i], img[i + 1], img[i + 2]].map((v) => Math.pow(v / 255, 2.2)));
      const th = r() * Math.PI * 2, ph = Math.acos(2 * r() - 1), rad = 1.4 + 3.2 * Math.pow(r(), 0.7);
      start.push(Math.cos(th) * Math.sin(ph) * rad * 0.8, Math.sin(th) * Math.sin(ph) * rad, Math.cos(ph) * rad * 0.6 - 0.5);
      arr.push(29.05 + 1.1 * (x / SW) * 0.8 + 0.25 * r());
      seed.push(r());
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(tgt, 3));
  g.setAttribute('aColor', new THREE.Float32BufferAttribute(col, 3));
  g.setAttribute('aStart', new THREE.Float32BufferAttribute(start, 3));
  g.setAttribute('aArr', new THREE.Float32BufferAttribute(arr, 1));
  g.setAttribute('aSeed', new THREE.Float32BufferAttribute(seed, 1));
  const pmat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending, toneMapped: false,
    uniforms: { uT: { value: 0 }, uPx: { value: k * step * 1.05 }, uFade: { value: 1 } },
    vertexShader: /* glsl */ `
      attribute vec3 aColor; attribute vec3 aStart; attribute float aArr; attribute float aSeed;
      uniform float uT, uPx; varying vec3 vC; varying float vA;
      void main(){
        float dur = 1.35;
        float p = clamp((uT - (aArr - dur)) / dur, 0.0, 1.0);
        float e = 1.0 - pow(1.0 - p, 3.0);
        vec3 off = aStart - position;
        float th = (1.0 - e) * 2.4 * (aSeed > 0.5 ? 1.0 : -1.0);
        float c = cos(th), s = sin(th);
        off.xy = mat2(c, -s, s, c) * off.xy;
        // before departure the fragments hang in the air as slow metallic vapour
        float idle = 1.0 - step(0.0001, p);
        vec3 drift = 0.06 * vec3(sin(uT * 0.7 + aSeed * 40.0), cos(uT * 0.6 + aSeed * 30.0), 0.0) * (1.0 - e);
        vec3 pos = position + off * (1.0 - e) + drift;
        vec4 mv = modelViewMatrix * vec4(pos, 1.0);
        gl_Position = projectionMatrix * mv;
        float depth = clamp(5.0 / -mv.z, 0.4, 3.0);
        gl_PointSize = uPx * mix(1.6, 1.0, e) * depth;
        vec3 silver = vec3(0.72, 0.77, 0.83);
        vC = mix(silver, aColor, smoothstep(0.55, 1.0, e));
        float glint = 0.55 + 0.45 * pow(0.5 + 0.5 * sin(uT * 9.0 + aSeed * 60.0), 8.0);
        vA = mix(0.22 * glint, 1.0, smoothstep(0.2, 1.0, e)) * (idle > 0.5 ? 0.35 : 1.0);
      }`,
    fragmentShader: /* glsl */ `
      uniform float uFade; varying vec3 vC; varying float vA;
      void main(){ float d = length(gl_PointCoord - 0.5); float f = smoothstep(0.5, 0.18, d);
        gl_FragColor = vec4(vC * vA * f * uFade * 1.75, 1.0); }`,
  });
  const pts = new THREE.Points(g, pmat);
  pts.frustumCulled = false;
  scene.add(pts);

  const vapour = motes({ count: 1600, box: [5, 8, 4], center: [0, 0, -1], seed: 99, H, brightness: 0.28, size: 1.3 });
  scene.add(vapour);

  // 2D layers: the official mark (untouched artwork), its sheen, and the typeset wordmark.
  const logoLayer = canvas(Math.round(lw * k), Math.round(lh * k));
  logoLayer.getContext('2d').drawImage(ctx.logo, crop.x, crop.y, crop.w, crop.h, 0, 0, logoLayer.width, logoLayer.height);
  const sheen = canvas(logoLayer.width, logoLayer.height);

  function drawLogo(c2d, alpha, sheenT = -1) {
    if (alpha <= 0) return;
    const x = (LOGO.cx - lw / 2) * k, y = (LOGO.cy - lh / 2) * k;
    c2d.save();
    c2d.globalAlpha = alpha;
    c2d.drawImage(logoLayer, x, y);
    if (sheenT >= 0 && sheenT <= 1) {
      // one delicate silver reflection crossing the mark, masked by the mark itself
      const s = sheen.getContext('2d');
      s.globalCompositeOperation = 'source-over';
      s.clearRect(0, 0, sheen.width, sheen.height);
      s.drawImage(logoLayer, 0, 0);
      s.globalCompositeOperation = 'source-in';
      const bx = lerp(-0.45, 1.45, ease.inOutSine(sheenT)) * sheen.width;
      const gr = s.createLinearGradient(bx - sheen.width * 0.13, 0, bx + sheen.width * 0.13, sheen.height * 0.35);
      gr.addColorStop(0, 'rgba(233,236,239,0)');
      gr.addColorStop(0.5, 'rgba(240,243,246,0.5)');
      gr.addColorStop(1, 'rgba(233,236,239,0)');
      s.fillStyle = gr;
      s.fillRect(0, 0, sheen.width, sheen.height);
      c2d.globalCompositeOperation = 'screen';
      c2d.drawImage(sheen, x, y);
      c2d.globalCompositeOperation = 'source-over';
    }
    c2d.restore();
  }

  function drawWordmark(c2d, reveal, alpha = 1) {
    if (reveal <= 0 || alpha <= 0) return;
    const px = 104 * k;
    c2d.save();
    c2d.font = `${px}px "InterDisplay SemiBold"`;
    c2d.letterSpacing = `${0.01 * px}px`;
    c2d.textAlign = 'center';
    const text = 'DevEraXTech';
    const w = c2d.measureText(text).width;
    const cx = 540 * k + (0.01 * px) / 2, by = 1140 * k;
    const gr = c2d.createLinearGradient(cx - w / 2, by - px, cx + w / 2, by);
    gr.addColorStop(0, '#a8842a'); gr.addColorStop(0.3, '#d4af37'); gr.addColorStop(0.5, '#f5d573');
    gr.addColorStop(0.7, '#d4af37'); gr.addColorStop(1, '#b8912a');
    // reveal opens from the centre outward, like the mark settling into place
    const e = ease.outQuart(reveal);
    c2d.beginPath();
    c2d.rect(cx - (w / 2 + 20 * k) * e, by - px * 1.1, (w + 40 * k) * e, px * 1.5);
    c2d.clip();
    c2d.globalAlpha = alpha * Math.min(1, reveal * 2);
    c2d.fillStyle = gr;
    c2d.fillText(text, cx, by);
    c2d.restore();
  }

  function update(t) {
    pmat.uniforms.uT.value = t;
    pmat.uniforms.uFade.value = 1 - smooth(LOCK - 0.05, LOCK + 0.35, t);
    pts.visible = pmat.uniforms.uFade.value > 0.001;
    vapour.userData.tick(t);
    return { scene, camera, exposure: 1.0, bloom: [0.22, 0.4, 0.9], vignette: 0.38 };
  }

  stage = { update, drawLogo, drawWordmark };
  return stage;
}

export default function (ctx) {
  const st = brandStage(ctx);
  function overlay(g, t, alpha) {
    g.globalAlpha = alpha;
    st.drawLogo(g, alpha * smooth(LOCK - 0.05, LOCK + 0.3, t));
    st.drawWordmark(g, inv(WORD_IN, WORD_IN + 0.7, t), alpha);
    g.globalAlpha = 1;
  }
  return { start: 28, end: 33, xIn: 0.25, update: st.update, overlay };
}
