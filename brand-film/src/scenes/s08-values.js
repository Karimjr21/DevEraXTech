import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { ease, inv, lerp, prog, smooth } from '../lib/util.js';
import { canvas } from '../lib/surfaces.js';
import { motes, ABOVE, BELOW } from '../lib/motes.js';

// SCENE 08 · 00:24–00:28 · The brand values.
// Three black-glass monoliths rise from a polished floor whose seams continue the grid
// of Scene 07. Each carries one engraved statement. They converge into one structure,
// and the camera's move around it ends in its black face: an empty space.

export const S08_RISES = [24.0, 24.8, 25.6];
export const S08_CONVERGE = 27.0;
const WORDS = ['SECURE.', 'SCALABLE.', 'PIXEL-PERFECT.'];
const MW = 0.95, MH = 3.0, MD = 0.34;
const XS = [-1.2, 0, 1.2];

function engraving(word) {
  const c = canvas(1024, 256), g = c.getContext('2d');
  g.clearRect(0, 0, 1024, 256);
  g.textAlign = 'center'; g.textBaseline = 'middle';
  let px = 112;
  g.font = `${px}px "InterDisplay Medium"`;
  g.letterSpacing = `${px * 0.14}px`;
  const w = g.measureText(word).width;
  if (w > 900) { px *= 900 / w; g.font = `${px}px "InterDisplay Medium"`; g.letterSpacing = `${px * 0.14}px`; }
  const grad = g.createLinearGradient(0, 128 - px / 2, 0, 128 + px / 2);
  grad.addColorStop(0, '#e9ecef'); grad.addColorStop(0.55, '#b9bec5'); grad.addColorStop(1, '#8b9199');
  g.fillStyle = grad;
  g.fillText(word, 512 + (px * 0.14) / 2, 132);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 16;
  return tex;
}

function seamTexture() {
  const c = canvas(512, 512), g = c.getContext('2d');
  g.fillStyle = '#000000'; g.fillRect(0, 0, 512, 512);
  g.fillStyle = '#9aa0a8';
  g.fillRect(0, 0, 512, 3); g.fillRect(0, 0, 3, 512);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(200, 200);
  t.anisotropy = 16;
  return t;
}

export default function (ctx) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  scene.environment = ctx.env.strips;
  scene.fog = new THREE.Fog(0x050607, 8, 26);
  const camera = new THREE.PerspectiveCamera(30, ctx.aspect, 0.02, 80);

  const floor = new THREE.Mesh(new THREE.PlaneGeometry(48, 48), new THREE.MeshPhysicalMaterial({
    color: 0x0a0b0d, emissive: 0xffffff, emissiveMap: seamTexture(), emissiveIntensity: 0.45, metalness: 0.9, roughness: 0.28, clearcoat: 0.4, clearcoatRoughness: 0.1, envMapIntensity: 0.12, transparent: true, opacity: 0.84,
  }));
  floor.rotation.x = -Math.PI / 2;
  scene.add(floor);

  const glassMat = (clip, dim = 1) => new THREE.MeshPhysicalMaterial({
    color: new THREE.Color(0x08090b).multiplyScalar(dim), metalness: 0.25, roughness: 0.05, clearcoat: 1, clearcoatRoughness: 0.02,
    envMapIntensity: 1.6 * dim, specularIntensity: 1, clippingPlanes: [clip],
  });
  const textMat = (word, clip, dim = 1) => new THREE.MeshBasicMaterial({
    map: engraving(word), transparent: true, toneMapped: false, clippingPlanes: [clip], depthWrite: false,
    color: new THREE.Color(1, 1, 1).multiplyScalar(dim),
  });

  const monos = WORDS.map((w, i) => {
    const make = (clip, dim) => {
      const g = new THREE.Group();
      const body = new THREE.Mesh(new RoundedBoxGeometry(MW, MH, MD, 4, 0.018), glassMat(clip, dim));
      const plate = new THREE.Mesh(new THREE.PlaneGeometry(MW * 0.86, MW * 0.86 * 0.25), textMat(w, clip, dim));
      plate.position.set(0, 0.35, MD / 2 + 0.002);
      g.add(body, plate);
      return g;
    };
    const real = make(ABOVE, 1);
    const mirror = make(BELOW, 0.32);
    mirror.scale.y = -1;
    scene.add(real, mirror);
    return { real, mirror, i };
  });

  // Architectural volumetric light: soft vertical shafts behind the monoliths.
  const shaftMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { uA: { value: 0 } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'uniform float uA; varying vec2 vUv; void main(){ float x = 1.0 - abs(vUv.x - 0.5) * 2.0; float a = pow(x, 3.0) * smoothstep(0.0, 0.35, vUv.y) * (1.0 - vUv.y) * uA; gl_FragColor = vec4(vec3(0.75, 0.8, 0.86) * a, 1.0); }',
  });
  const shafts = [-2.6, 0, 2.6].map((x) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 9), shaftMat);
    m.position.set(x, 4.5, -3.2);
    scene.add(m);
    return m;
  });
  const backdrop = new THREE.Mesh(new THREE.PlaneGeometry(60, 20), new THREE.ShaderMaterial({
    depthWrite: false, fog: false,
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'varying vec2 vUv; void main(){ float y = vUv.y; float h = exp(-pow((y - 0.06) * 7.0, 2.0)); float x = 1.0 - abs(vUv.x - 0.5) * 1.4; vec3 c = vec3(0.09, 0.098, 0.113) * h * clamp(x, 0.0, 1.0); gl_FragColor = vec4(c, 1.0); }',
  }));
  backdrop.position.set(0, 1.2, -9);
  scene.add(backdrop);
  const dust = motes({ count: 2400, box: [9, 5, 9], center: [0, 2.3, -1], seed: 88, H: ctx.H, brightness: 0.38 });
  scene.add(dust);
  const rim = new THREE.DirectionalLight(0xe9ecef, 1.2); rim.position.set(-2, 4, -3);
  scene.add(rim);

  function update(t) {
    dust.userData.tick(t);
    shaftMat.uniforms.uA.value = 0.18 + 0.16 * smooth(24.0, 26.5, t);
    const conv = prog(26.2, S08_CONVERGE, t, ease.inOutQuart);
    monos.forEach(({ real, mirror, i }) => {
      const r0 = S08_RISES[i];
      const rise = prog(r0, r0 + 0.72, t, ease.outQuart);
      const y = lerp(-MH / 2 - 0.05, MH / 2, rise);
      const x = lerp(XS[i], (i - 1) * MW, conv);
      real.position.set(x, y, 0);
      mirror.position.set(x, -y, 0);
    });

    // Camera: low-angle lateral track across the rising monoliths, pull back for the
    // convergence, then a move around the structure until its black face fills frame.
    const track = prog(23.9, 26.2, t, ease.inOutSine);
    const pos = new THREE.Vector3(lerp(-1.6, 1.4, track), 0.55, 7.2);
    const look = new THREE.Vector3(lerp(-1.2, 1.2, track), 1.25, 0);
    const back = prog(26.1, 27.1, t, ease.inOutCubic);
    pos.lerp(new THREE.Vector3(0, 0.5, 8.6), back);
    look.lerp(new THREE.Vector3(0, 1.35, 0), back);
    // around and in: the structure's edge sweeps the frame until its black face is all we see
    const around = prog(27.15, 28.05, t, ease.inCubic);
    const ang = -0.55 * around;
    const R = lerp(8.6, 0.85, around);
    const F = new THREE.Vector3(-0.35, 2.6, MD / 2);
    pos.lerp(new THREE.Vector3(Math.sin(ang) * R, lerp(0.5, 2.6, around), Math.cos(ang) * R + MD / 2), smooth(27.15, 27.25, t));
    look.lerp(F, around);
    camera.position.copy(pos);
    camera.lookAt(look);
    camera.updateMatrixWorld();

    return { scene, camera, exposure: 1.0 + 0.15 * smooth(26.8, 27.2, t), bloom: [0.3, 0.55, 0.85] };
  }

  return { start: 24, end: 28, xIn: 0.3, update };
}
