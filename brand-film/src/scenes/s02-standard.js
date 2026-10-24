import * as THREE from 'three';
import { ease, lerp, prog, smooth } from '../lib/util.js';
import { portalMesh } from '../lib/portal.js';
import { motes, darkFloor, BELOW } from '../lib/motes.js';
import { drawTitle, scrim } from '../lib/text.js';

// SCENE 02 · 00:03–00:06 · The new standard.
// The surviving fragment liquefies into chrome and pulls itself into a machined portal.
// Clockwise orbit, then a dolly straight through the opening.

export default function (ctx) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  scene.environment = ctx.env.chrome;
  scene.fog = new THREE.Fog(0x000000, 12, 30);
  const camera = new THREE.PerspectiveCamera(32, ctx.aspect, 0.02, 80);

  const C = new THREE.Vector3(0, 1.42, 0);
  const chrome = new THREE.MeshPhysicalMaterial({ color: 0xe9ecef, metalness: 1, roughness: 0.035, envMapIntensity: 1.35, clearcoat: 0.6 });
  const portal = portalMesh(chrome);
  portal.position.copy(C);
  scene.add(portal);

  const mirrorMat = chrome.clone();
  mirrorMat.color.multiplyScalar(0.4);
  mirrorMat.envMapIntensity = 0.55;
  mirrorMat.clippingPlanes = [BELOW];
  const mirror = new THREE.Mesh(portal.geometry, mirrorMat);
  mirror.frustumCulled = false;
  mirror.scale.y = -1;
  mirror.position.set(C.x, -C.y, C.z);
  scene.add(mirror);

  scene.add(darkFloor({ opacity: 0.86, envI: 0.018 }));
  const dust = motes({ count: 2500, box: [14, 6, 18], center: [0, 2.2, -2], seed: 22, H: ctx.H, brightness: 0.45 });
  scene.add(dust);

  function update(t) {
    // Shape: liquid blob → rounded-square architectural frame.
    const f = prog(3.1, 5.2, t, ease.inOutSine);
    const f2 = prog(3.4, 5.6, t, ease.inOutQuart);
    portal.userData.shape({
      a: lerp(0.02, 0.98, f), b: lerp(0.02, 1.32, f),
      n: lerp(2, 5.5, f2), m: lerp(2, 7, f2),
      rN: lerp(0.52, 0.085, f), rZ: lerp(0.5, 0.2, f),
      wobble: 0.075 * (1 - smooth(3.2, 5.4, t)) + 0.02 * (1 - smooth(3.0, 3.4, t)),
      t,
    });
    dust.userData.tick(t);

    // Camera: tight on the chrome, pulls back into a clockwise orbit, then dollies through.
    const th = 0.95 * (1 - prog(3.0, 5.35, t, ease.inOutCubic));
    let R = lerp(1.25, 8.6, prog(3.0, 4.45, t, ease.outCubic));
    R = lerp(R, 6.8, prog(4.45, 5.35, t, ease.inOutCubic));
    const y = lerp(C.y, 0.95, prog(3.0, 4.2, t, ease.inOutCubic));
    const pos = new THREE.Vector3(C.x + Math.sin(th) * R, y, C.z + Math.cos(th) * R);
    const through = prog(5.35, 6.05, t, ease.inCubic);
    pos.lerp(new THREE.Vector3(0, C.y, -1.6), through);
    pos.y = lerp(pos.y, C.y, smooth(5.0, 5.6, t));
    camera.position.copy(pos);
    camera.lookAt(C.x, lerp(C.y, C.y + 0.1, smooth(3.4, 4.4, t)) * (1 - through) + C.y * through, C.z - 3 * through);
    camera.updateMatrixWorld();

    return { scene, camera, exposure: 1.05, bloom: [0.28, 0.5, 0.86] };
  }

  function overlay(g, t, alpha) {
    g.globalAlpha = alpha;
    scrim(g, ctx.W, ctx.H, smooth(3.2, 3.6, t) * (1 - smooth(5.4, 5.7, t)), 1350, 420);
    drawTitle(g, ctx.W, t, { lines: ['IT NEEDS A', 'NEW STANDARD.'], start: 3.3, end: 5.6, y: 1330, size: 64 });
    g.globalAlpha = 1;
  }

  return { start: 3, end: 6, xIn: 0.22, update, overlay };
}
