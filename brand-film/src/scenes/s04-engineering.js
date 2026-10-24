import * as THREE from 'three';
import { ease, inv, lerp, prog, rng, smooth } from '../lib/util.js';
import { motes } from '../lib/motes.js';
import { drawTitle, scrim } from '../lib/text.js';

// SCENE 04 · 00:09–00:12 · Engineered.
// Beneath the interface: two strata of fine metallic traces, machined pads and vias,
// carrying light pulses. The camera tracks between them, then a single travelling
// signal draws the outline of a phone in the dark ahead.

const FLOOR = 0.52;
export const PHONE_OUTLINE = { w: 0.33, h: 0.68, dist: 2.2 }; // matched by Scene 05's opening framing

function roundedRectPath(w, h, r, n = 400) {
  const pts = [];
  // start at top centre, travel clockwise
  const segs = [];
  const hw = w / 2, hh = h / 2;
  const add = (p) => segs.push(p);
  add([0, hh]); add([hw - r, hh]);
  for (let i = 1; i <= 12; i++) { const a = Math.PI / 2 - (i / 12) * (Math.PI / 2); add([hw - r + Math.cos(a) * r, hh - r + Math.sin(a) * r]); }
  add([hw, -hh + r]);
  for (let i = 1; i <= 12; i++) { const a = -(i / 12) * (Math.PI / 2); add([hw - r + Math.cos(a) * r, -hh + r + Math.sin(a) * r]); }
  add([-hw + r, -hh]);
  for (let i = 1; i <= 12; i++) { const a = -Math.PI / 2 - (i / 12) * (Math.PI / 2); add([-hw + r + Math.cos(a) * r, -hh + r + Math.sin(a) * r]); }
  add([-hw, hh - r]);
  for (let i = 1; i <= 12; i++) { const a = Math.PI - (i / 12) * (Math.PI / 2); add([-hw + r + Math.cos(a) * r, hh - r + Math.sin(a) * r]); }
  add([0, hh]);
  // resample uniformly by arc length
  const L = [0];
  for (let i = 1; i < segs.length; i++) L.push(L[i - 1] + Math.hypot(segs[i][0] - segs[i - 1][0], segs[i][1] - segs[i - 1][1]));
  const total = L[L.length - 1];
  let j = 0;
  for (let k = 0; k <= n; k++) {
    const s = (k / n) * total;
    while (j < L.length - 2 && L[j + 1] < s) j++;
    const f = (s - L[j]) / (L[j + 1] - L[j] || 1);
    pts.push(new THREE.Vector3(lerp(segs[j][0], segs[j + 1][0], f), lerp(segs[j][1], segs[j + 1][1], f), 0));
  }
  return pts;
}

export default function (ctx) {
  const r = rng(4404);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  scene.environment = ctx.env.strips;
  scene.fog = new THREE.Fog(0x000000, 4, 15);
  const camera = new THREE.PerspectiveCamera(30, ctx.aspect, 0.01, 60);

  // Substrate boards.
  const boardMat = new THREE.MeshStandardMaterial({ color: 0x0b0c0f, metalness: 0.7, roughness: 0.42, envMapIntensity: 0.35 });
  for (const s of [-1, 1]) {
    const b = new THREE.Mesh(new THREE.PlaneGeometry(8, 40), boardMat);
    b.rotation.x = s * Math.PI / 2;
    b.position.set(0, -s * FLOOR - s * 0.004, -12);
    scene.add(b);
  }

  // Manhattan routes with 45° jogs on both strata.
  const routes = [];
  for (const side of [-1, 1]) {
    for (let i = 0; i < 230; i++) {
      let x = (Math.round((r() - 0.5) * 5.6 / 0.06) * 0.06);
      if (Math.abs(x) < 0.12) x += Math.sign(x || 1) * 0.12;
      let z = 4 - r() * 26;
      const pts = [new THREE.Vector3(x, side * FLOOR, z)];
      const legs = 1 + Math.floor(r() * 3);
      for (let k = 0; k < legs; k++) {
        z -= 0.6 + r() * 4.5;
        pts.push(new THREE.Vector3(x, side * FLOOR, z));
        if (k < legs - 1) {
          const jog = (r() < 0.5 ? -1 : 1) * (0.06 * (1 + Math.floor(r() * 5)));
          x += jog; z -= Math.abs(jog);
          pts.push(new THREE.Vector3(x, side * FLOOR, z));
        }
      }
      routes.push({ pts, side, speed: 1.2 + r() * 2.4, off: r() * 10, lit: r() < 0.55 });
    }
  }
  const segs = [];
  for (const ro of routes) for (let k = 1; k < ro.pts.length; k++) segs.push([ro.pts[k - 1], ro.pts[k]]);
  const traceMat = new THREE.MeshStandardMaterial({ color: 0xc9ced5, metalness: 1, roughness: 0.28, envMapIntensity: 1.3 });
  const traces = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), traceMat, segs.length);
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), S = new THREE.Vector3(), Pm = new THREE.Vector3();
  const Z = new THREE.Vector3(0, 0, 1);
  segs.forEach(([a, b], i) => {
    const d = new THREE.Vector3().subVectors(b, a);
    const len = d.length();
    Q.setFromUnitVectors(Z, d.clone().normalize());
    Pm.addVectors(a, b).multiplyScalar(0.5);
    S.set(0.011, 0.004, len + 0.011);
    traces.setMatrixAt(i, M.compose(Pm, Q, S));
  });
  scene.add(traces);

  // Machined pads at every route end, vias between strata.
  const padPts = [];
  for (const ro of routes) { padPts.push(ro.pts[0], ro.pts[ro.pts.length - 1]); }
  const padMat = new THREE.MeshStandardMaterial({ color: 0xe9ecef, metalness: 1, roughness: 0.18, envMapIntensity: 1.6 });
  const pads = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.024, 0.024, 0.008, 20), padMat, padPts.length);
  const I = new THREE.Quaternion();
  padPts.forEach((p, i) => pads.setMatrixAt(i, M.compose(p, I, new THREE.Vector3(1, 1, 1))));
  scene.add(pads);
  const viaPts = padPts.filter((p, i) => i % 9 === 0 && p.y > 0 && Math.abs(p.x) > 0.35);
  const vias = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.008, 0.008, FLOOR * 2, 10), traceMat, viaPts.length);
  viaPts.forEach((p, i) => vias.setMatrixAt(i, M.compose(new THREE.Vector3(p.x, 0, p.z), I, new THREE.Vector3(1, 1, 1))));
  scene.add(vias);

  // Light pulses travelling along lit routes.
  const lit = routes.filter((ro) => ro.lit);
  const pulseMat = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  pulseMat.color.setScalar(2.0);
  const pulses = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), pulseMat, lit.length);
  lit.forEach((ro) => {
    ro.len = [0];
    for (let k = 1; k < ro.pts.length; k++) ro.len.push(ro.len[k - 1] + ro.pts[k].distanceTo(ro.pts[k - 1]));
  });
  scene.add(pulses);

  // The phone outline drawn by one signal.
  const outlinePts = roundedRectPath(PHONE_OUTLINE.w, PHONE_OUTLINE.h, 0.044);
  const tube = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(outlinePts, false, 'centripetal'), 600, 0.0022, 6, false);
  const outlineMat = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, transparent: true });
  const outline = new THREE.Mesh(tube, outlineMat);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.006, 12, 8), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }));
  head.material.color.setScalar(4);
  const outlineGroup = new THREE.Group();
  outlineGroup.add(outline, head);
  scene.add(outlineGroup);
  const idxCount = tube.index.count;

  const dust = motes({ count: 1800, box: [3, 1, 24], center: [0, 0, -9], seed: 44, H: ctx.H, brightness: 0.35, size: 1.2 });
  scene.add(dust);

  const camZ = (t) => lerp(2.5, -13.2, prog(9.0, 11.35, t, (x) => ease.inOutCubic(x) * 0.8 + x * 0.2));

  function update(t) {
    const cz = camZ(t);
    const sway = Math.sin((t - 9) * 1.4) * 0.09 * (1 - smooth(10.8, 11.4, t));
    camera.position.set(sway, 0.02 * Math.sin((t - 9) * 2.1), cz);
    const look = new THREE.Vector3(sway * 0.4, 0, cz - 4);
    camera.lookAt(look);
    camera.updateMatrixWorld();

    // pulses
    lit.forEach((ro, i) => {
      const L = ro.len[ro.len.length - 1];
      const cyc = L + 2.5;
      const s = ((t * ro.speed + ro.off) % cyc);
      if (s > L) { pulses.setMatrixAt(i, M.makeScale(0, 0, 0)); return; }
      let k = 1;
      while (k < ro.len.length - 1 && ro.len[k] < s) k++;
      const f = (s - ro.len[k - 1]) / (ro.len[k] - ro.len[k - 1]);
      const a = ro.pts[k - 1], b = ro.pts[k];
      Pm.lerpVectors(a, b, f); Pm.y += ro.side * -0.003;
      Q.setFromUnitVectors(Z, new THREE.Vector3().subVectors(b, a).normalize());
      pulses.setMatrixAt(i, M.compose(Pm, Q, S.set(0.014, 0.006, 0.16)));
    });
    pulses.instanceMatrix.needsUpdate = true;
    dust.userData.tick(t);

    // outline sits ahead of where the camera comes to rest
    const endZ = camZ(12);
    outlineGroup.position.set(0, 0, endZ - PHONE_OUTLINE.dist);
    const draw = prog(10.95, 11.75, t, ease.inOutCubic);
    outline.geometry.setDrawRange(0, Math.floor((idxCount * draw) / 3) * 3);
    outline.visible = draw > 0;
    const hp = outlinePts[Math.min(outlinePts.length - 1, Math.floor(draw * (outlinePts.length - 1)))];
    head.position.copy(hp);
    head.visible = draw > 0 && draw < 1;
    outlineMat.opacity = 1;

    return { scene, camera, exposure: 1.0, bloom: [0.42, 0.45, 0.8] };
  }

  function overlay(g, t, alpha) {
    g.globalAlpha = alpha;
    drawTitle(g, ctx.W, t, { lines: ['ENGINEERED.'], start: 9.08, end: 10.95, y: 1000, size: 88, family: '"InterDisplay SemiBold"', tracking: 0.18, inDur: 0.4 });
    g.globalAlpha = 1;
  }

  return { start: 9, end: 12, xIn: 0.2, update, overlay };
}
