import * as THREE from 'three';
import { clamp, ease, inv, lerp, prog, rng, smooth, TAU } from '../lib/util.js';
import { canvas, drawGenericSite } from '../lib/surfaces.js';
import { drawTitle, scrim } from '../lib/text.js';

// SCENE 01 · 00:00–00:03 · The pattern interrupt.
// A generic flat website frozen in a crystal slab. Cracks run out from an impact
// point along the exact lines the slab will later break on, then a shock wave
// shatters it. One fragment stays, turns once in the light, and we fly into it.

const SW = 1.5, SH = 2.6667, T = 0.08;
const P = new THREE.Vector2(0.12, 0.35); // impact point in slab space

// Variant timing: the shock alt hits almost at once; the curiosity alt holds the mystery longer.
const TIMING = {
  main: { shock: 1.0, crack0: 0.0, text0: 0.2 },
  shock: { shock: 0.32, crack0: 0.0, text0: 0.5 },
  curiosity: { shock: 1.9, crack0: 0.6, text0: 1.0 },
};

const SHARD_GLSL_HEAD = /* glsl */ `
  attribute vec3 aCenter; attribute vec3 aVel; attribute vec3 aAxis; attribute float aSpin; attribute float aDelay;
  uniform float uT;
  mat3 rotAxis(vec3 a, float g){ float s = sin(g), c = cos(g), oc = 1.0 - c;
    return mat3(oc*a.x*a.x + c, oc*a.x*a.y + a.z*s, oc*a.z*a.x - a.y*s,
                oc*a.x*a.y - a.z*s, oc*a.y*a.y + c, oc*a.y*a.z + a.x*s,
                oc*a.z*a.x + a.y*s, oc*a.y*a.z - a.x*s, oc*a.z*a.z + c); }
`;

function shardMaterial(params, uniforms, displaced = true) {
  const m = new THREE.MeshPhysicalMaterial(params);
  if (!displaced) return m;
  m.onBeforeCompile = (sh) => {
    sh.uniforms.uT = uniforms.uT;
    sh.vertexShader = SHARD_GLSL_HEAD + sh.vertexShader
      .replace('#include <beginnormal_vertex>', /* glsl */ `
        float te = max(0.0, uT - aDelay);
        // high-speed acquisition feel: a violent first instant that settles into slow motion
        float tw = 0.12 * (1.0 - exp(-te * 9.0)) + 0.07 * te;
        mat3 R = rotAxis(normalize(aAxis), aSpin * tw);
        vec3 objectNormal = R * normal;
        #ifdef USE_TANGENT
          vec3 objectTangent = vec3(tangent.xyz);
        #endif`)
      .replace('#include <begin_vertex>', /* glsl */ `
        vec3 transformed = R * (position - aCenter) + aCenter + aVel * tw + vec3(0.0, -0.025, 0.0) * te * te;`);
  };
  return m;
}

// Polar fracture net around the impact point: radial and concentric cracks, the way tempered glass fails.
function buildFracture(r) {
  const RINGS = 24, SPOKES = 30;
  const pts = [];
  const radius = (k) => 0.03 * Math.pow(1.215, k);
  const hx = SW / 2, hy = SH / 2;
  for (let k = 0; k < RINGS; k++) {
    const row = [];
    for (let j = 0; j < SPOKES; j++) {
      const th = ((j + (r() - 0.5) * 0.55) / SPOKES) * TAU + k * 0.07;
      const rr = radius(k) * (1 + (r() - 0.5) * 0.22);
      row.push(new THREE.Vector2(clamp(P.x + Math.cos(th) * rr, -hx, hx), clamp(P.y + Math.sin(th) * rr, -hy, hy)));
    }
    pts.push(row);
  }
  const cells = []; // {tris:[[a,b,c],...], k, j}
  for (let j = 0; j < SPOKES; j++) {
    const j2 = (j + 1) % SPOKES;
    cells.push({ k: -1, j, tris: [[P.clone(), pts[0][j], pts[0][j2]]] });
    for (let k = 0; k < RINGS - 1; k++) {
      const a = pts[k][j], b = pts[k + 1][j], c = pts[k + 1][j2], d = pts[k][j2];
      const tris = r() < 0.5 ? [[a, b, c], [a, c, d]] : [[a, b, d], [b, c, d]];
      cells.push({ k, j, tris });
    }
  }
  // Subdivide into finer shards (jittered midpoints), discarding slivers clamped off the slab.
  const area = (a, b, c) => Math.abs((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) / 2;
  const mid = (a, b) => new THREE.Vector2().lerpVectors(a, b, 0.5 + (r() - 0.5) * 0.3);
  const out = [];
  for (const cell of cells) {
    for (const [a, b, c] of cell.tris) {
      if (area(a, b, c) < 2e-6) continue;
      const fine = area(a, b, c) > 0.0016;
      const list = fine
        ? (() => { const ab = mid(a, b), bc = mid(b, c), ca = mid(c, a); return [[a, ab, ca], [ab, b, bc], [ca, bc, c], [ab, bc, ca]]; })()
        : [[a, b, c]];
      for (const t of list) if (area(...t) > 1e-6) out.push({ tri: t, k: cell.k, j: cell.j });
    }
  }
  return out;
}

function prismGeometry(shards, origin, attrs) {
  const face = { pos: [], nor: [], uv: [], c: [], v: [], ax: [], sp: [], dl: [] };
  const side = { pos: [], nor: [], uv: [], c: [], v: [], ax: [], sp: [], dl: [] };
  const uvOf = (p) => [p.x / SW + 0.5, p.y / SH + 0.5];
  const push = (G, p, n, uv, s) => {
    G.pos.push(p[0] - origin.x, p[1] - origin.y, p[2] - origin.z); G.nor.push(...n); G.uv.push(...uv);
    G.c.push(s.center.x - origin.x, s.center.y - origin.y, s.center.z - origin.z);
    G.v.push(...s.vel); G.ax.push(...s.axis); G.sp.push(s.spin); G.dl.push(s.delay);
  };
  for (const s of shards) {
    const [a, b, c] = s.tri;
    const z = T / 2;
    // front (+z) and back (-z) faces; winding fixed so normals face outward
    const ccw = (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0;
    const [p, q, w] = ccw ? [a, b, c] : [a, c, b];
    for (const v of [p, q, w]) push(face, [v.x, v.y, z], [0, 0, 1], uvOf(v), s);
    for (const v of [p, w, q]) push(face, [v.x, v.y, -z], [0, 0, -1], uvOf(v), s);
    const ring = [p, q, w];
    for (let i = 0; i < 3; i++) {
      const v0 = ring[i], v1 = ring[(i + 1) % 3];
      const n = new THREE.Vector3(v1.y - v0.y, -(v1.x - v0.x), 0).normalize();
      const quad = [[v0.x, v0.y, -z], [v1.x, v1.y, -z], [v1.x, v1.y, z], [v0.x, v0.y, -z], [v1.x, v1.y, z], [v0.x, v0.y, z]];
      for (const qv of quad) push(side, qv, [n.x, n.y, n.z], uvOf(new THREE.Vector2(qv[0], qv[1])), s);
    }
  }
  const make = (G) => {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(G.pos, 3));
    g.setAttribute('normal', new THREE.Float32BufferAttribute(G.nor, 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute(G.uv, 2));
    if (attrs) {
      g.setAttribute('aCenter', new THREE.Float32BufferAttribute(G.c, 3));
      g.setAttribute('aVel', new THREE.Float32BufferAttribute(G.v, 3));
      g.setAttribute('aAxis', new THREE.Float32BufferAttribute(G.ax, 3));
      g.setAttribute('aSpin', new THREE.Float32BufferAttribute(G.sp, 1));
      g.setAttribute('aDelay', new THREE.Float32BufferAttribute(G.dl, 1));
    }
    g.computeBoundingSphere();
    g.boundingSphere.radius = 50; // shards travel far from their rest pose; never cull
    return g;
  };
  return { face: make(face), side: make(side) };
}

export default function (ctx) {
  const tm = TIMING[ctx.variant] || TIMING.main;
  const r = rng(1101);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  scene.environment = ctx.env.strips;
  scene.environmentIntensity = 0.9;

  const camera = new THREE.PerspectiveCamera(20, ctx.aspect, 0.004, 60); // ~100 mm on a vertical frame

  // Website texture, with cracks painted along the true fracture lines.
  const TW = 1350, TH = 2400;
  const site = canvas(TW, TH), sg = site.getContext('2d');
  const base = canvas(TW, TH);
  drawGenericSite(base.getContext('2d'), TW, TH);
  const siteTex = new THREE.CanvasTexture(site);
  siteTex.colorSpace = THREE.SRGBColorSpace;
  siteTex.anisotropy = 8;

  const shards = buildFracture(r);
  // Hero fragment: a small cluster of cells just right of the impact, kept whole.
  const isHero = (s) => s.k >= 11 && s.k <= 12 && (s.j === 4 || s.j === 5);
  const heroShards = [], flyShards = [];
  for (const s of shards) {
    const [a, b, c] = s.tri;
    const cx = (a.x + b.x + c.x) / 3, cy = (a.y + b.y + c.y) / 3;
    s.center = new THREE.Vector3(cx, cy, 0);
    const d = Math.hypot(cx - P.x, cy - P.y);
    const dir = new THREE.Vector2(cx - P.x, cy - P.y).normalize();
    const sp = (0.25 + 1.3 * Math.exp(-d * 1.8)) * (0.6 + 0.8 * r());
    s.vel = [dir.x * sp + (r() - 0.5) * 0.12, dir.y * sp + (r() - 0.5) * 0.12, (0.12 + 0.9 * r()) * Math.exp(-d * 0.8)];
    s.axis = [r() - 0.5, r() - 0.5, r() - 0.5];
    s.spin = (r() < 0.5 ? -1 : 1) * (4 + 22 * r());
    s.delay = d / 3.2;
    (isHero(s) ? heroShards : flyShards).push(s);
  }

  const uniforms = { uT: { value: -10 } };
  const faceMat = shardMaterial({
    color: 0x6a6e74, map: siteTex, emissive: 0xffffff, emissiveMap: siteTex, emissiveIntensity: 0.2,
    roughness: 0.06, metalness: 0.0, clearcoat: 1, clearcoatRoughness: 0.02, ior: 1.6, specularIntensity: 1,
    envMapIntensity: 1.2,
  }, uniforms);
  const sideMat = shardMaterial({
    color: 0x0c0e11, roughness: 0.02, metalness: 0.0, clearcoat: 1, ior: 1.9, specularIntensity: 1, envMapIntensity: 2.2,
  }, uniforms);
  const zero = new THREE.Vector3();
  // Everything lives on a rig turned slightly off-axis so the slab's thickness and edges read.
  const rig = new THREE.Group();
  rig.rotation.set(0.08, -0.32, 0.02);
  scene.add(rig);
  const fly = prismGeometry(flyShards, zero, true);
  const flyGroup = new THREE.Group();
  flyGroup.add(new THREE.Mesh(fly.face, faceMat), new THREE.Mesh(fly.side, sideMat));
  rig.add(flyGroup);

  // The intact crystal slab, shown until the instant of the shock (identical outline and UVs).
  const staticFace = new THREE.MeshPhysicalMaterial({ ...faceMat.parameters });
  ['color', 'map', 'emissive', 'emissiveMap', 'emissiveIntensity', 'roughness', 'metalness', 'clearcoat', 'clearcoatRoughness', 'ior', 'specularIntensity', 'envMapIntensity']
    .forEach((k) => { staticFace[k] = faceMat[k]; });
  const staticSide = new THREE.MeshPhysicalMaterial();
  ['color', 'roughness', 'metalness', 'clearcoat', 'ior', 'specularIntensity', 'envMapIntensity'].forEach((k) => { staticSide[k] = sideMat[k]; });
  const slab = new THREE.Mesh(new THREE.BoxGeometry(SW, SH, T), [staticSide, staticSide, staticSide, staticSide, staticFace, staticFace]);
  rig.add(slab);

  // Hero fragment as its own rigid object.
  const heroC = new THREE.Vector3();
  heroShards.forEach((s) => heroC.add(s.center));
  heroC.divideScalar(heroShards.length);
  const heroGeo = prismGeometry(heroShards, heroC, false);
  const heroFaceMat = new THREE.MeshPhysicalMaterial({
    color: 0x6a6e74, map: siteTex, emissive: 0xffffff, emissiveMap: siteTex, emissiveIntensity: 0.2,
    roughness: 0.05, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.01, envMapIntensity: 1.2,
  });
  const heroSideMat = sideMat.clone(); heroSideMat.onBeforeCompile = () => {};
  const hero = new THREE.Group();
  hero.add(new THREE.Mesh(heroGeo.face, heroFaceMat), new THREE.Mesh(heroGeo.side, heroSideMat));
  rig.add(hero);

  // Glass dust: tiny particles thrown off along the shock front.
  const N = 6000;
  const dp = new Float32Array(N * 3), dv = new Float32Array(N * 3), dd = new Float32Array(N), ds = new Float32Array(N);
  for (let i = 0; i < N; i++) {
    const s = flyShards[(r() * flyShards.length) | 0];
    const [a, b] = s.tri;
    const u = r();
    dp[i * 3] = lerp(a.x, b.x, u); dp[i * 3 + 1] = lerp(a.y, b.y, u); dp[i * 3 + 2] = (r() - 0.5) * T;
    const d = Math.hypot(dp[i * 3] - P.x, dp[i * 3 + 1] - P.y);
    const dir = new THREE.Vector2(dp[i * 3] - P.x, dp[i * 3 + 1] - P.y).normalize();
    const sp = (1 + 4 * r()) * Math.exp(-d * 1.2);
    dv[i * 3] = dir.x * sp + (r() - 0.5) * 0.6; dv[i * 3 + 1] = dir.y * sp + (r() - 0.5) * 0.6; dv[i * 3 + 2] = (0.3 + 3.2 * r()) * Math.exp(-d);
    dd[i] = d / 3.2; ds[i] = r();
  }
  const dustGeo = new THREE.BufferGeometry();
  dustGeo.setAttribute('position', new THREE.BufferAttribute(dp, 3));
  dustGeo.setAttribute('aVel', new THREE.BufferAttribute(dv, 3));
  dustGeo.setAttribute('aDelay', new THREE.BufferAttribute(dd, 1));
  dustGeo.setAttribute('aSeed', new THREE.BufferAttribute(ds, 1));
  dustGeo.boundingSphere = new THREE.Sphere(zero, 50);
  const dustMat = new THREE.ShaderMaterial({
    uniforms: { uT: uniforms.uT, uPx: { value: ctx.H / 1920 } },
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: /* glsl */ `
      attribute vec3 aVel; attribute float aDelay; attribute float aSeed; uniform float uT, uPx; varying float vA;
      void main(){
        float te = max(0.0, uT - aDelay);
        float tw = 0.16 * (1.0 - exp(-te * 9.0)) + 0.09 * te;
        vec3 p = position + aVel * tw;
        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        gl_Position = projectionMatrix * mv;
        float on = step(0.0001, uT - aDelay);
        // facets catch the light as they tumble: a deterministic per-particle glint
        float glint = pow(0.5 + 0.5 * sin(aSeed * 91.0 + te * (8.0 + aSeed * 22.0)), 6.0);
        vA = on * (0.25 + 0.95 * glint) * exp(-te * 0.25);
        gl_PointSize = uPx * (1.4 + 2.6 * aSeed) * (2.2 / max(0.2, -mv.z));
      }`,
    fragmentShader: /* glsl */ `
      varying float vA;
      void main(){ vec2 c = gl_PointCoord - 0.5; float f = smoothstep(0.5, 0.0, length(c)); gl_FragColor = vec4(vec3(0.93, 0.95, 0.97) * vA * f, 1.0); }`,
  });
  const dust = new THREE.Points(dustGeo, dustMat);
  rig.add(dust);

  // Shock alt opening: a polished titanium slug is fired through the slab.
  const slug = new THREE.Mesh(new THREE.SphereGeometry(0.07, 48, 32), new THREE.MeshPhysicalMaterial({ color: 0xd0d5dc, metalness: 1, roughness: 0.12, clearcoat: 0.5 }));
  slug.visible = false;
  const slugDir = new THREE.Vector3(-0.12, 0.05, -1).normalize();
  rig.add(slug);

  // Minimal white edge light.
  const key = new THREE.DirectionalLight(0xffffff, 0.7); key.position.set(-2, 3, 1.5);
  const rim = new THREE.DirectionalLight(0xe9ecef, 0.9); rim.position.set(1.5, 2, -3);
  scene.add(key, rim);

  // Crack network = every shard edge, revealed outward from the impact.
  const edges = [];
  const seen = new Set();
  const heroUse = new Map();
  const kp = (p) => `${p.x.toFixed(4)},${p.y.toFixed(4)}`;
  for (const s of heroShards) for (let i = 0; i < 3; i++) {
    const k = [kp(s.tri[i]), kp(s.tri[(i + 1) % 3])].sort().join('|');
    heroUse.set(k, (heroUse.get(k) || 0) + 1);
  }
  const key2 = (p) => `${p.x.toFixed(4)},${p.y.toFixed(4)}`;
  for (const s of shards) {
    const t3 = s.tri;
    for (let i = 0; i < 3; i++) {
      const a = t3[i], b = t3[(i + 1) % 3];
      const k = [key2(a), key2(b)].sort().join('|');
      if (seen.has(k)) continue;
      seen.add(k);
      if ((heroUse.get(k) || 0) > 1) continue;
      const m = new THREE.Vector2().addVectors(a, b).multiplyScalar(0.5);
      edges.push({ a, b, d: m.distanceTo(P), hero: isHero(s) });
    }
  }
  const toPx = (p) => [(p.x / SW + 0.5) * TW, (0.5 - p.y / SH) * TH];
  let lastCrack = -1;
  function paintCracks(R) {
    const q = Math.round(R * 400) / 400;
    if (q === lastCrack) return;
    lastCrack = q;
    sg.drawImage(base, 0, 0);
    sg.lineCap = 'round';
    for (const pass of [[6, 0.10], [1.6, 0.85]]) {
      sg.lineWidth = pass[0];
      sg.strokeStyle = `rgba(250,252,255,${pass[1]})`;
      sg.beginPath();
      for (const e of edges) {
        if (e.d > q) continue;
        const [ax, ay] = toPx(e.a), [bx, by] = toPx(e.b);
        sg.moveTo(ax, ay); sg.lineTo(bx, by);
      }
      sg.stroke();
    }
    siteTex.needsUpdate = true;
  }

  const heroQ = new THREE.Vector3(0.16, 0.3, 1.0);
  const tmpE = new THREE.Euler();
  const W = (v) => { rig.updateMatrixWorld(); return rig.localToWorld(v.clone()); };
  const Pw = () => W(new THREE.Vector3(P.x, P.y, 0));

  function update(t) {
    const ts = tm.shock;
    const broken = t >= ts;
    slab.visible = !broken;
    flyGroup.visible = broken;
    // cracks race outward and accelerate into the shock
    const crackR = t < tm.crack0 ? 0 : 0.05 + 1.2 * Math.pow(inv(tm.crack0, ts, t), 2.4);
    paintCracks(broken ? 3 : crackR);
    uniforms.uT.value = t - ts;
    if (ctx.variant === 'shock') {
      slug.visible = t > ts - 0.3 && t < ts + 0.6;
      slug.position.set(P.x, P.y, 0).addScaledVector(slugDir, (t - ts) * 11);
    }
    const die = smooth(ts, ts + 0.9, t);
    faceMat.emissiveIntensity = 0.2 * (1 - 0.75 * die);
    faceMat.color.setHex(0x6a6e74).multiplyScalar(1 - 0.6 * die);

    // Hero fragment: detaches, glides to the centre of frame and turns once through the light.
    const h0 = ts + 0.1, h1 = Math.max(2.4, h0 + 0.5);
    const hp = prog(h0, h1, t, ease.inOutCubic);
    hero.position.lerpVectors(heroC, heroQ, hp);
    const turn = prog(h0, 2.7, t, ease.inOutQuart);
    tmpE.set(0.3 * Math.sin(turn * Math.PI), TAU * turn + 0.32 * hp, -0.1 * Math.sin(turn * Math.PI));
    hero.quaternion.setFromEuler(tmpE);
    const mirror = smooth(2.0, 2.85, t);
    heroFaceMat.emissiveIntensity = 0.2 * (1 - 0.85 * mirror);
    heroFaceMat.metalness = 0.95 * mirror;
    heroFaceMat.roughness = 0.05 - 0.04 * mirror;
    scene.environmentRotation.set(0, -0.9 + 1.4 * smooth(2.0, 3.0, t), 0);

    // Camera: aggressive push-in on the impact, a slow-motion drift through the debris,
    // then a committed dive into the surviving fragment.
    const pos = new THREE.Vector3(), look = new THREE.Vector3();
    const pw = Pw();
    if (ctx.variant === 'curiosity') {
      // opens on an abstract glint travelling along the slab's edge, then pulls back until the website reads
      const pull = prog(0, 1.3, t, ease.inOutCubic);
      const edge = W(new THREE.Vector3(SW / 2, 0.55, 0));
      pos.lerpVectors(edge.clone().add(new THREE.Vector3(0.18, 0.06, 0.32)), new THREE.Vector3(1.3, -0.5, 9.5), pull);
      look.lerpVectors(edge, new THREE.Vector3(0.02, 0.08, 0), pull);
      const push = prog(1.3, ts, t, ease.inQuart);
      pos.lerp(new THREE.Vector3(0.55, 0.2, 3.3), push);
      look.lerp(pw, push);
    } else {
      const push = prog(0, ts, t, ctx.variant === 'shock' ? ease.outCubic : ease.inCubic);
      pos.set(lerp(1.3, 0.55, push), lerp(-0.55, 0.2, push), lerp(10.5, 3.3, push));
      look.lerpVectors(new THREE.Vector3(0.02, 0.06, 0), pw, push);
    }
    const drift = prog(ts, 2.1, t, ease.outCubic);
    const hw = W(hero.position);
    pos.lerp(new THREE.Vector3(0.45, 0.3, 2.85), drift);
    look.lerp(hw, smooth(ts + 0.05, 1.9, t));
    const dive = prog(2.05, 3.0, t, ease.inExpo);
    const normalW = new THREE.Vector3(0, 0, 1).applyQuaternion(hero.quaternion).applyQuaternion(rig.quaternion);
    pos.lerp(hw.clone().addScaledVector(normalW, 0.01), dive);
    camera.position.copy(pos);
    camera.lookAt(look);
    camera.updateMatrixWorld();

    return {
      scene, camera,
      exposure: 1.0 + 0.9 * smooth(2.7, 3.0, t),
      bloom: [0.26 + 0.6 * smooth(2.6, 3.0, t), 0.5, 0.88 - 0.1 * smooth(2.6, 3.0, t)],
      grain: 0.02,
    };
  }

  function overlay(g, t, alpha) {
    g.globalAlpha = alpha;
    scrim(g, ctx.W, ctx.H, smooth(tm.text0 - 0.2, tm.text0 + 0.3, t) * (1 - smooth(2.5, 2.8, t)), 1180);
    drawTitle(g, ctx.W, t, {
      lines: ['THE INTERNET', 'DOESN’T NEED', 'ANOTHER WEBSITE.'],
      start: tm.text0, end: 2.72, y: 1230, size: 60,
    });
    g.globalAlpha = 1;
  }

  return { start: 0, end: 3, update, overlay };
}
