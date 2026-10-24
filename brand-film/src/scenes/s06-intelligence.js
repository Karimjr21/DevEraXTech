import * as THREE from 'three';
import { ease, inv, lerp, prog, rng, smooth } from '../lib/util.js';
import { portalMesh } from '../lib/portal.js';
import { motes } from '../lib/motes.js';
import { drawTitle, scrim } from '../lib/text.js';

// SCENE 06 · 00:16–00:20 · Built to think bigger.
// Integration as architecture: illuminated strands weave through an arcade of the
// portal frames first seen in Scene 02, trading signals at relay beads, converging on
// one machined hub. Wide-to-close sweep, ending in macro on the hub.

const LEN = 24;
const centre = (s) => new THREE.Vector3(1.2 * Math.sin(s * Math.PI * 0.9), 1.6, -s * LEN);

function frameAt(s) {
  const p = centre(s);
  const tg = centre(s + 0.001).sub(p).normalize();
  const up = new THREE.Vector3(0, 1, 0);
  const n = new THREE.Vector3().crossVectors(up, tg).normalize();
  return { p, tg, n, up };
}

export default function (ctx) {
  const r = rng(6606);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  scene.environment = ctx.env.strips;
  scene.fog = new THREE.Fog(0x000000, 7, 26);
  const camera = new THREE.PerspectiveCamera(32, ctx.aspect, 0.005, 80);

  // Arcade of portal frames in dark brushed metal.
  const frameMat = new THREE.MeshPhysicalMaterial({ color: 0x5a5f66, metalness: 1, roughness: 0.3, envMapIntensity: 1.1, anisotropy: 0.6 });
  const PORTALS = [];
  for (let k = 1; k <= 7; k++) {
    const s = k / 7.6;
    const m = portalMesh(frameMat, 200, 20);
    m.userData.shape({ a: 1.15, b: 1.5, n: 5.5, m: 7, rN: 0.06, rZ: 0.16, wobble: 0, t: 0 });
    const f = frameAt(s);
    m.position.copy(f.p);
    m.lookAt(f.p.clone().add(f.tg));
    scene.add(m);
    PORTALS.push(s);
  }

  // Strands.
  const hub = centre(1.02);
  const strandMats = [];
  const beads = [];
  // four disciplined bundles; strands inside a bundle braid gently around its core
  const bundles = [0, 1, 2, 3].map((b) => ({ A: 0.45 + 0.35 * r(), B: 0.55 + 0.5 * r(), w1: 1.6 + 1.6 * r(), w2: 1.3 + 1.8 * r(), p1: b * 1.57 + r(), p2: b * 2.2 + r() }));
  for (let j = 0; j < 44; j++) {
    const bd = bundles[j % 4];
    const ja = r() * 6.28, jr = 0.04 + 0.09 * r(), jw = 5 + 4 * r();
    const A = bd.A, B = bd.B, w1 = bd.w1, w2 = bd.w2, p1 = bd.p1, p2 = bd.p2;
    const pts = [];
    for (let i = 0; i <= 80; i++) {
      const s = -0.05 + (i / 80) * 1.07;
      const f = frameAt(Math.min(s, 1.0));
      const conv = 1 - smooth(0.74, 1.0, s);
      const ox = (A * Math.cos(w1 * s + p1) + jr * Math.cos(jw * s + ja)) * conv, oy = (B * Math.sin(w2 * s + p2) + jr * Math.sin(jw * s + ja)) * conv;
      const pt = f.p.clone().addScaledVector(f.n, ox).addScaledVector(f.up, oy);
      if (s > 1.0) pt.lerp(hub, smooth(1.0, 1.02, s));
      pts.push(pt);
    }
    const curve = new THREE.CatmullRomCurve3(pts);
    const geo = new THREE.TubeGeometry(curve, 360, 0.0042 + 0.002 * r(), 5, false);
    const mat = new THREE.ShaderMaterial({
      uniforms: { uT: { value: 0 }, uSeed: { value: r() }, uSpeed: { value: 0.45 + 0.6 * r() }, uLift: { value: 0 } },
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, fog: false,
      vertexShader: /* glsl */ `varying float vU; varying float vD; void main(){ vU = uv.x; vec4 mv = modelViewMatrix * vec4(position,1.0); vD = -mv.z; gl_Position = projectionMatrix * mv; }`,
      fragmentShader: /* glsl */ `
        uniform float uT, uSeed, uSpeed, uLift; varying float vU; varying float vD;
        void main(){
          float ph = fract(vU * 3.0 - uT * uSpeed + uSeed);
          float ph2 = fract(vU * 5.0 - uT * uSpeed * 0.7 + uSeed * 3.7);
          float p = exp(-pow((ph - 0.5) * 30.0, 2.0)) + 0.6 * exp(-pow((ph2 - 0.5) * 40.0, 2.0));
          float base = 0.12 + uLift;
          float fog = smoothstep(26.0, 6.0, vD);
          vec3 c = vec3(0.86, 0.9, 0.95) * (base + 2.2 * p) * fog * (1.0 - 0.75 * smoothstep(0.9, 1.0, vU));
          gl_FragColor = vec4(c, 1.0);
        }`,
    });
    strandMats.push(mat);
    const mesh = new THREE.Mesh(geo, mat);
    mesh.frustumCulled = false;
    scene.add(mesh);
    // relay beads where a strand crosses a portal plane
    PORTALS.forEach((s, k) => { if ((j + k) % 3 === 0) beads.push(curve.getPointAt(Math.min(1, (s + 0.05) / 1.07))); });
  }
  const beadMat = new THREE.MeshPhysicalMaterial({ color: 0xe9ecef, metalness: 1, roughness: 0.08, envMapIntensity: 1.6 });
  const beadMesh = new THREE.InstancedMesh(new THREE.SphereGeometry(0.018, 16, 12), beadMat, beads.length);
  const M = new THREE.Matrix4();
  beads.forEach((b, i) => beadMesh.setMatrixAt(i, M.makeTranslation(b.x, b.y, b.z)));
  scene.add(beadMesh);

  // Machined hub where every strand converges.
  const prof = [];
  const P = (x, y) => prof.push(new THREE.Vector2(x, y));
  P(0, -0.32); P(0.11, -0.32); P(0.12, -0.31); P(0.12, -0.2); P(0.1, -0.19); P(0.1, -0.17); P(0.13, -0.16); P(0.13, 0.02);
  P(0.105, 0.03); P(0.105, 0.06); P(0.135, 0.07); P(0.135, 0.2); P(0.12, 0.215); P(0.06, 0.22); P(0.05, 0.26); P(0, 0.26);
  const hubMesh = new THREE.Mesh(new THREE.LatheGeometry(prof, 96), new THREE.MeshPhysicalMaterial({ color: 0xc9ced5, metalness: 1, roughness: 0.2, envMapIntensity: 1.4, anisotropy: 0.8 }));
  const hf = frameAt(1.0);
  hubMesh.position.copy(hub).addScaledVector(hf.tg, 0.28);
  hubMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, -1, 0), hf.tg);
  scene.add(hubMesh);

  const dust = motes({ count: 2600, box: [8, 6, 30], center: [0.6, 1.8, -11], seed: 66, H: ctx.H, brightness: 0.35 });
  scene.add(dust);

  // Camera rail: inside the bundle → wide overview → lateral sweep → macro on the hub.
  const camKeys = [
    centre(0.0).add(new THREE.Vector3(0.5, 0.35, 1.3)),
    centre(0.1).add(new THREE.Vector3(2.6, 3.0, 2.6)),
    centre(0.45).add(new THREE.Vector3(-2.6, 1.6, 0)),
    centre(0.86).add(new THREE.Vector3(1.0, 0.35, 0.6)),
    hub.clone().addScaledVector(hf.tg, 0.28).add(new THREE.Vector3(0.5, 0.14, 0.55)),
  ];
  const lookKeys = [centre(0.2), centre(0.45), centre(0.75), centre(0.97), hubMesh.position.clone()];
  const camCurve = new THREE.CatmullRomCurve3(camKeys, false, 'centripetal');
  const lookCurve = new THREE.CatmullRomCurve3(lookKeys, false, 'centripetal');

  function update(t) {
    strandMats.forEach((m) => { m.uniforms.uT.value = t; m.uniforms.uLift.value = 0.12 * (1 - smooth(16.0, 16.6, t)); });
    dust.userData.tick(t);
    const u = prog(16.0, 20.0, t, (x) => ease.inOutSine(x) * 0.75 + x * 0.25);
    camera.position.copy(camCurve.getPoint(u));
    camera.lookAt(lookCurve.getPoint(Math.min(1, u + 0.02)));
    camera.updateMatrixWorld();
    return { scene, camera, exposure: 1.0, bloom: [0.5, 0.5, 0.75] };
  }

  function overlay(g, t, alpha) {
    g.globalAlpha = alpha;
    scrim(g, ctx.W, ctx.H, smooth(16.3, 16.7, t) * (1 - smooth(19.2, 19.5, t)), 1400, 380);
    drawTitle(g, ctx.W, t, { lines: ['BUILT TO', 'THINK BIGGER.'], start: 16.45, end: 19.4, y: 1380, size: 64 });
    g.globalAlpha = 1;
  }

  return { start: 16, end: 20, xIn: 0.35, update, overlay };
}
