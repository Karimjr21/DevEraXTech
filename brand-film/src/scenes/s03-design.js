import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { ease, inv, lerp, prog, smooth, snap } from '../lib/util.js';
import { canvas } from '../lib/surfaces.js';
import { SITE_MODULES, drawSiteModule } from '../lib/ui.js';
import { motes, darkFloor, mirrorOf, syncMirror } from '../lib/motes.js';
import { drawTitle, scrim } from '../lib/text.js';

// SCENE 03 · 00:06–00:09 · Not just designed.
// An original concept website assembles itself on a smoked-glass slab inside an
// architecture of glass fins. Every module travels on one axis and lands on the grid.

// Module entrance: offset it travels from, and the landing window. Landings drive the audio clicks.
export const S03_LANDINGS = [6.5, 6.72, 6.96, 7.16, 7.34, 7.44, 7.54];
const FROM = [
  [0, 0.9, 0], [-2.4, 0, 0], [0, 0, 1.6], [2.4, 0, 0], [0, -1.2, 0], [0, -1.2, 0], [0, -1.2, 0],
];

export default function (ctx) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  scene.environment = ctx.env.strips;
  scene.fog = new THREE.Fog(0x000000, 10, 26);
  const camera = new THREE.PerspectiveCamera(30, ctx.aspect, 0.02, 80);

  const C = new THREE.Vector3(0, 2.25, 0);
  const site = new THREE.Group();
  site.position.copy(C);
  scene.add(site);

  const glass = new THREE.Mesh(
    new RoundedBoxGeometry(2.04, 3.42, 0.07, 4, 0.05),
    new THREE.MeshPhysicalMaterial({ color: 0x0a0c0f, roughness: 0.04, metalness: 0.1, clearcoat: 1, clearcoatRoughness: 0.02, envMapIntensity: 1.6, transparent: true, opacity: 0.92 })
  );
  glass.position.z = -0.05;
  site.add(glass);

  const PXU = 600;
  const mods = SITE_MODULES.map((m, i) => {
    const c = canvas(Math.round(m.w * PXU), Math.round(m.h * PXU));
    drawSiteModule(m.id, c.getContext('2d'), c.width, c.height);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(m.w, m.h), new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false, depthWrite: false }));
    mesh.position.set(m.x, m.y, 0.01 + i * 0.004);
    site.add(mesh);
    return { m, mesh, home: mesh.position.clone() };
  });

  // Alignment hairlines that flash as each module lands on the grid.
  const hair = mods.map(({ m }) => {
    const h = new THREE.Mesh(new THREE.PlaneGeometry(2.3, 0.004), new THREE.MeshBasicMaterial({ color: 0xe9ecef, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false }));
    h.position.set(0, m.y + m.h / 2, 0.03);
    site.add(h);
    return h;
  });

  const mirror = mirrorOf(site, 0.35);
  scene.add(mirror);

  // Glass architecture: two colonnades of fins and a ceiling grid, receding into fog.
  const finMat = new THREE.MeshPhysicalMaterial({ color: 0x9aa3ad, roughness: 0.03, metalness: 0, transparent: true, opacity: 0.2, envMapIntensity: 4.5, clearcoat: 1, side: THREE.DoubleSide, depthWrite: false });
  const finGeo = new THREE.BoxGeometry(0.04, 9, 1.3);
  const mullGeo = new THREE.BoxGeometry(0.025, 9, 0.025);
  const beamMatEarly = new THREE.MeshPhysicalMaterial({ color: 0xb9bec5, metalness: 1, roughness: 0.18, envMapIntensity: 1.4 });
  for (let s = -1; s <= 1; s += 2) {
    for (let i = 0; i < 9; i++) {
      const f = new THREE.Mesh(finGeo, finMat);
      f.position.set(s * (2.5 + (i % 2) * 0.12), 4.5, 3 - i * 2.1);
      f.rotation.y = s * 0.35;
      scene.add(f);
      const mu = new THREE.Mesh(mullGeo, beamMatEarly);
      mu.position.copy(f.position).add(new THREE.Vector3(Math.sin(s * 0.35) * 0.65, 0, Math.cos(s * 0.35) * 0.65));
      scene.add(mu);
    }
  }
  const beamGeo = new THREE.BoxGeometry(6, 0.035, 0.035);
  const beamMat = new THREE.MeshPhysicalMaterial({ color: 0xb9bec5, metalness: 1, roughness: 0.2, envMapIntensity: 1.2 });
  for (let i = 0; i < 9; i++) {
    const b = new THREE.Mesh(beamGeo, beamMat);
    b.position.set(0, 6.2, 3 - i * 2.1);
    scene.add(b);
  }
  scene.add(darkFloor({ opacity: 0.8, envI: 0.05 }));
  const dust = motes({ count: 2200, box: [7, 7, 16], center: [0, 3, -3], seed: 33, H: ctx.H, brightness: 0.4 });
  scene.add(dust);

  function update(t) {
    mods.forEach(({ mesh, home }, i) => {
      const land = S03_LANDINGS[i];
      const p = snap(land - 0.42, land, t, 0.0);
      const o = FROM[i];
      mesh.position.set(home.x + o[0] * (1 - p), home.y + o[1] * (1 - p), home.z + o[2] * (1 - p));
      mesh.material.opacity = smooth(land - 0.42, land - 0.2, t);
      const fl = Math.exp(-Math.max(0, t - land) * 7) * (t >= land ? 1 : 0);
      hair[i].material.opacity = 0.55 * fl;
    });
    syncMirror(site, mirror);
    dust.userData.tick(t + 6);

    const d = prog(6.0, 8.55, t, ease.inOutSine);
    const pos = new THREE.Vector3(lerp(0.75, -0.12, d), lerp(1.75, 2.2, d), lerp(10.4, 6.6, d));
    const look = new THREE.Vector3(0, lerp(1.85, 2.2, d), 0);
    const thru = prog(8.45, 9.02, t, ease.inQuart);
    pos.lerp(new THREE.Vector3(0, 2.32, -0.5), thru);
    look.z -= thru * 2;
    camera.position.copy(pos);
    camera.lookAt(look);
    camera.updateMatrixWorld();
    return { scene, camera, exposure: 1.0, bloom: [0.25, 0.5, 0.86] };
  }

  function overlay(g, t, alpha) {
    g.globalAlpha = alpha;
    scrim(g, ctx.W, ctx.H, smooth(6.2, 6.6, t) * (1 - smooth(8.4, 8.7, t)), 1420, 380);
    drawTitle(g, ctx.W, t, { lines: ['NOT JUST', 'DESIGNED.'], start: 6.3, end: 8.6, y: 1400, size: 66 });
    g.globalAlpha = 1;
  }

  return { start: 6, end: 9, xIn: 0.25, update, overlay };
}
