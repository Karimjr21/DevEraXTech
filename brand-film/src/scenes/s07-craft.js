import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { ease, inv, lerp, prog, rng, smooth, snap } from '../lib/util.js';
import { motes } from '../lib/motes.js';
import { drawTitle, scrim } from '../lib/text.js';

// SCENE 07 · 00:20–00:24 · Every pixel. Every detail.
// Three macro details on rhythmic match cuts, each ending on a tactile "click":
// A titanium shaft seats in its collar · B a glass edge catches one moving light ·
// C an interface grid snaps into alignment, then opens out into the monolith hall.

export const S07_CLICKS = [20.74, 21.98, 23.2];
const CUT1 = 21.333, CUT2 = 22.667;

const titanium = () => new THREE.MeshPhysicalMaterial({ color: 0xc4c9d0, metalness: 1, roughness: 0.26, anisotropy: 0.85, anisotropyRotation: Math.PI / 2, envMapIntensity: 1.3, clearcoat: 0.15 });

function lathe(points, segs = 160) {
  return new THREE.LatheGeometry(points.map(([x, y]) => new THREE.Vector2(x, y)), segs);
}

export default function (ctx) {
  const r = rng(7707);

  // ---------- A: shaft seating in a collar
  const A = new THREE.Scene();
  A.background = new THREE.Color(0x000000);
  A.environment = ctx.env.strips;
  const camA = new THREE.PerspectiveCamera(22, ctx.aspect, 0.01, 20);
  const collar = new THREE.Mesh(lathe([
    [0.081, -0.13], [0.2, -0.13], [0.21, -0.12], [0.21, -0.05], [0.2, -0.045], [0.2, -0.035], [0.21, -0.03],
    [0.21, 0.12], [0.2, 0.13], [0.081, 0.13], [0.081, -0.13],
  ]), titanium());
  collar.rotation.z = Math.PI / 2;
  const shaftPts = [[0, -0.45], [0.06, -0.45], [0.078, -0.43]];
  for (let i = 0; i < 6; i++) { const y = -0.3 + i * 0.05; shaftPts.push([0.078, y - 0.012], [0.072, y - 0.008], [0.072, y + 0.008], [0.078, y + 0.012]); }
  shaftPts.push([0.078, 0.38], [0.068, 0.4], [0.068, 0.43], [0.04, 0.45], [0, 0.45]);
  const shaft = new THREE.Mesh(lathe(shaftPts), titanium());
  shaft.rotation.z = -Math.PI / 2;
  const groupA = new THREE.Group();
  groupA.add(collar, shaft);
  groupA.rotation.set(0.2, -0.55, 0.05);
  A.add(groupA);
  const keyA = new THREE.DirectionalLight(0xffffff, 1.6); keyA.position.set(-1, 2, 1.5); A.add(keyA);
  A.add(motes({ count: 600, box: [2, 2, 2], seed: 71, H: ctx.H, brightness: 0.3, size: 1.0 }));

  // ---------- B: a glass edge catching one moving light
  const B = new THREE.Scene();
  B.background = new THREE.Color(0x000000);
  B.environment = ctx.env.strips;
  const camB = new THREE.PerspectiveCamera(22, ctx.aspect, 0.01, 20);
  const glass = new THREE.Mesh(
    new RoundedBoxGeometry(1.4, 0.9, 0.24, 8, 0.045),
    new THREE.MeshPhysicalMaterial({ color: 0xf2f5f8, metalness: 0, roughness: 0.0, transmission: 1, thickness: 0.24, ior: 1.52, envMapIntensity: 1.6, specularIntensity: 1, clearcoat: 1, attenuationColor: new THREE.Color(0x9fb0c0), attenuationDistance: 1.2 })
  );
  glass.rotation.set(0.42, -0.62, 0.0);
  B.add(glass);
  // the grid of detail C, glimpsed through the glass: foreshadowing the next cut
  const behind = new THREE.GridHelper(4, 40, 0x2a2e33, 0x2a2e33);
  behind.rotation.x = Math.PI / 2; behind.position.z = -0.9;
  B.add(behind);
  const glint = new THREE.PointLight(0xffffff, 0, 3, 2);
  B.add(glint);

  // ---------- C: an interface grid snapping into alignment
  const C = new THREE.Scene();
  C.background = new THREE.Color(0x000000);
  C.environment = ctx.env.strips;
  C.fog = new THREE.Fog(0x000000, 3, 14);
  const camC = new THREE.PerspectiveCamera(26, ctx.aspect, 0.01, 40);
  const N = 41, CELL = 0.12, SPAN = (N - 1) * CELL;
  const barMat = new THREE.MeshPhysicalMaterial({ color: 0xd0d5dc, metalness: 1, roughness: 0.22, envMapIntensity: 1.4 });
  const bars = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), barMat, N * 2);
  const offs = [];
  for (let i = 0; i < N * 2; i++) {
    const d = Math.abs((i % N) - (N - 1) / 2) / ((N - 1) / 2);
    offs.push({ o: (r() - 0.5) * 0.09 * (1 - d * 0.5), a: (r() - 0.5) * 0.05, y: r() * 0.03 });
  }
  C.add(bars);
  const nodeMat = new THREE.MeshPhysicalMaterial({ color: 0xe9ecef, metalness: 1, roughness: 0.12 });
  const nodes = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.009, 0.009, 0.006, 16), nodeMat, N * N);
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), S = new THREE.Vector3(), E = new THREE.Euler();
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
    nodes.setMatrixAt(i * N + j, M.compose(V.set(-SPAN / 2 + i * CELL, 0.004, -SPAN / 2 + j * CELL), Q.identity(), S.set(1, 1, 1)));
  }
  C.add(nodes);
  const floorC = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshStandardMaterial({ color: 0x050607, metalness: 0.8, roughness: 0.35, envMapIntensity: 0.15 }));
  floorC.rotation.x = -Math.PI / 2; floorC.position.y = -0.006;
  C.add(floorC);

  function update(t) {
    if (t < CUT1) {
      // A — shaft decelerates into the bore and seats with a hair of settle
      const p = snap(20.0, S07_CLICKS[0], t, 0.0);
      shaft.position.x = lerp(-0.95, -0.39, p);
      const ring = Math.exp(-Math.max(0, t - S07_CLICKS[0]) * 18) * (t > S07_CLICKS[0] ? 1 : 0);
      shaft.position.x -= 0.0025 * Math.sin((t - S07_CLICKS[0]) * 80) * ring;
      const d = prog(20.0, CUT1, t, ease.inOutSine);
      camA.position.set(lerp(0.75, 0.62, d), lerp(0.36, 0.3, d), lerp(1.75, 1.5, d));
      camA.lookAt(lerp(-0.2, -0.12, d), 0, 0);
      camA.updateMatrixWorld();
      A.environmentRotation.y = 0.3 + 0.4 * d;
      return { scene: A, camera: camA, exposure: 1.05, bloom: [0.25, 0.4, 0.88] };
    }
    if (t < CUT2) {
      // B — one studio light travels the length of the chamfered edge
      const d = prog(CUT1, CUT2, t, ease.inOutSine);
      B.environmentRotation.set(0, lerp(-1.1, 1.3, prog(CUT1, CUT2, t, ease.inOutCubic)), 0);
      glint.position.set(lerp(-0.9, 0.9, prog(CUT1 + 0.1, CUT2, t, ease.inOutCubic)), 0.6, 0.5);
      glint.intensity = 0;
      camB.position.set(lerp(0.15, 0.05, d), lerp(0.55, 0.5, d), lerp(1.05, 0.95, d));
      camB.lookAt(0.02, 0.33, 0.08);
      camB.updateMatrixWorld();
      return { scene: B, camera: camB, exposure: 1.1, bloom: [0.32, 0.4, 0.85] };
    }
    // C — misaligned bars snap to the grid; then the grid opens into architecture
    const p = snap(S07_CLICKS[2] - 0.38, S07_CLICKS[2], t, 0.0);
    for (let i = 0; i < N * 2; i++) {
      const k = i % N, horiz = i < N;
      const o = offs[i];
      const off = o.o * (1 - p), ang = o.a * (1 - p), lift = o.y * (1 - p);
      const c = -SPAN / 2 + k * CELL + off;
      if (horiz) { V.set(0, lift, c); E.set(0, ang, 0); S.set(SPAN + 0.02, 0.006, 0.006); }
      else { V.set(c, lift, 0); E.set(0, ang, 0); S.set(0.006, 0.006, SPAN + 0.02); }
      bars.setMatrixAt(i, M.compose(V, Q.setFromEuler(E), S));
    }
    bars.instanceMatrix.needsUpdate = true;
    const lock = smooth(S07_CLICKS[2], S07_CLICKS[2] + 0.15, t);
    nodeMat.emissive.setScalar(0.6 * Math.exp(-Math.max(0, t - S07_CLICKS[2]) * 6) * lock);
    const open = prog(23.35, 24.15, t, ease.inOutCubic);
    camC.position.set(lerp(0.1, 0.0, open), lerp(1.55, 0.32, open), lerp(1.0, 2.6, open));
    camC.lookAt(0, 0, lerp(0.0, -3.0, open));
    camC.updateMatrixWorld();
    C.environmentRotation.y = lerp(-0.4, 0.5, prog(CUT2, 24, t));
    return { scene: C, camera: camC, exposure: 1.05, bloom: [0.28, 0.45, 0.86] };
  }

  function overlay(g, t, alpha) {
    g.globalAlpha = alpha;
    scrim(g, ctx.W, ctx.H, smooth(20.1, 20.4, t) * (1 - smooth(23.4, 23.7, t)), 1440, 420);
    drawTitle(g, ctx.W, t, { lines: ['EVERY PIXEL.', 'EVERY DETAIL.'], start: 20.25, end: 23.6, y: 1410, size: 64, stagger: 1.1 });
    g.globalAlpha = 1;
  }

  return { start: 20, end: 24, xIn: 0.25, update, overlay };
}
