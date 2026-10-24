import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { buildStudioEnv } from './lib/env.js';
import { loadFonts } from './lib/text.js';
import { clamp } from './lib/util.js';

import s01 from './scenes/s01-interrupt.js';
import s02 from './scenes/s02-standard.js';
import s03 from './scenes/s03-design.js';
import s04 from './scenes/s04-engineering.js';
import s05 from './scenes/s05-ecosystem.js';
import s06 from './scenes/s06-intelligence.js';
import s07 from './scenes/s07-craft.js';
import s08 from './scenes/s08-values.js';
import s09 from './scenes/s09-reveal.js';
import s10 from './scenes/s10-anchor.js';

const params = new URLSearchParams(location.search);
const W = +(params.get('w') || 1080);
const H = +(params.get('h') || 1920);
const VARIANT = params.get('variant') || 'main'; // main | shock | curiosity

// Film grain, vignette and a hint of highlight roll-off, applied in display space.
const FinishShader = {
  uniforms: { tDiffuse: { value: null }, uFrame: { value: 0 }, uGrain: { value: 0.022 }, uVig: { value: 0.32 }, uRes: { value: new THREE.Vector2(W, H) } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform float uFrame, uGrain, uVig; uniform vec2 uRes; varying vec2 vUv;
    float h(vec2 p){ p = fract(p * vec2(443.897, 441.423)); p += dot(p, p.yx + 19.19); return fract((p.x + p.y) * p.x); }
    void main(){
      vec3 c = texture2D(tDiffuse, vUv).rgb;
      vec2 q = vUv - 0.5; q.x *= uRes.x / uRes.y;
      float v = smoothstep(0.95, 0.18, length(q));
      c *= mix(1.0 - uVig, 1.0, v);
      // luminance-weighted grain: strongest in mids, gentle in the blacks so they stay clean
      float l = dot(c, vec3(0.299, 0.587, 0.114));
      float g = (h(vUv * uRes + uFrame * 17.0) + h(vUv * uRes * 0.5 + uFrame * 3.1) - 1.0);
      c += g * uGrain * (0.25 + 0.75 * smoothstep(0.0, 0.5, l) * (1.0 - smoothstep(0.7, 1.0, l)));
      gl_FragColor = vec4(c, 1.0);
    }`,
};

export async function boot() {
  await loadFonts('/assets/fonts');
  const logoImg = new Image();
  logoImg.src = '/assets/brand/deveraxtech-logo.png';
  await logoImg.decode();

  const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.localClippingEnabled = true;

  const target = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, target);
  const renderPass = new RenderPass(new THREE.Scene(), new THREE.PerspectiveCamera());
  const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), 0.35, 0.55, 0.82);
  const finish = new ShaderPass(FinishShader);
  composer.addPass(renderPass);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());
  composer.addPass(finish);

  const comp = document.createElement('canvas');
  comp.width = W; comp.height = H;
  document.body.appendChild(comp);
  const c2d = comp.getContext('2d');

  const ctx = {
    THREE, renderer, W, H, aspect: W / H, variant: VARIANT,
    env: { strips: buildStudioEnv(renderer, 'strips'), soft: buildStudioEnv(renderer, 'soft'), chrome: buildStudioEnv(renderer, 'chrome') },
    logo: logoImg,
    logoCrop: { x: 284, y: 164, w: 970, h: 660 }, // transparent padding trimmed; artwork itself untouched
  };

  const scenes = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10].map((S) => S(ctx));

  // Render one scene's 3D plate into the composite canvas.
  // three.js only honours envMapIntensity for a material's own envMap, so bind the scene's
  // environment explicitly once; per-material reflection levels then behave as authored.
  const bound = new WeakSet();
  function bindEnv(scene) {
    if (bound.has(scene)) return;
    bound.add(scene);
    scene.traverse((o) => {
      if (!o.material) return;
      for (const m of Array.isArray(o.material) ? o.material : [o.material]) {
        if (m.isMeshStandardMaterial && !m.envMap && scene.environment) { m.envMap = scene.environment; m.needsUpdate = true; }
      }
    });
  }

  function plate(sc, t, alpha, frame) {
    const st = sc.update(t);
    bindEnv(st.scene);
    renderPass.scene = st.scene;
    renderPass.camera = st.camera;
    const b = st.bloom || [0.35, 0.55, 0.82];
    bloom.strength = b[0]; bloom.radius = b[1]; bloom.threshold = b[2];
    renderer.toneMappingExposure = st.exposure ?? 1.0;
    finish.uniforms.uFrame.value = frame;
    finish.uniforms.uGrain.value = st.grain ?? 0.022;
    finish.uniforms.uVig.value = st.vignette ?? 0.32;
    composer.render();
    c2d.globalAlpha = alpha;
    c2d.drawImage(renderer.domElement, 0, 0);
    c2d.globalAlpha = 1;
  }

  function active(t) {
    let i = scenes.findIndex((s) => t >= s.start && t < s.end);
    if (i < 0) i = t < scenes[0].start ? 0 : scenes.length - 1;
    return i;
  }

  // Frame is a pure function of t. Transitions blend the outgoing scene (evaluated
  // past its end) with the incoming one for the incoming scene's `xIn` seconds.
  window.renderFrame = (t, frame = Math.round(t * 60)) => {
    c2d.globalCompositeOperation = 'source-over';
    c2d.fillStyle = '#000';
    c2d.fillRect(0, 0, W, H);
    const i = active(t);
    const sc = scenes[i];
    const prev = scenes[i - 1];
    const xIn = sc.xIn || 0;
    if (prev && xIn > 0 && t < sc.start + xIn) {
      const a = clamp((t - sc.start) / xIn);
      plate(prev, t, 1, frame);
      plate(sc, t, a * a * (3 - 2 * a), frame);
      prev.overlay?.(c2d, t, 1 - a);
      sc.overlay?.(c2d, t, a);
    } else {
      plate(sc, t, 1, frame);
      sc.overlay?.(c2d, t, 1);
    }
    return comp;
  };

  window.__scenes = scenes;
  window.grabFrame = (t, type = 'image/png', q) => window.renderFrame(t).toDataURL(type, q);
  window.filmReady = true;
}

boot();
