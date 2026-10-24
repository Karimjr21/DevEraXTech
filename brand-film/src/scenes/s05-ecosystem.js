import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { clamp, ease, inv, lerp, prog, smooth, TAU } from '../lib/util.js';
import { canvas } from '../lib/surfaces.js';
import { drawPhoneApp, drawPhoneStore, drawDashboard } from '../lib/ui.js';
import { motes } from '../lib/motes.js';
import { drawTitle, scrim } from '../lib/text.js';
import { PHONE_OUTLINE } from './s04-engineering.js';

// SCENE 05 · 00:12–00:16 · Beyond the screen.
// The traced outline becomes a titanium phone. It turns once, its screen moving from a
// concept app to a concept store, rolls into landscape as a dashboard, and we push into
// the dashboard's integrations map until its lines become light.

const PW = 0.75, PH = 1.55, PD = 0.072, PR = 0.1;
const START_DIST = PHONE_OUTLINE.dist * (PW / PHONE_OUTLINE.w);
// graph centre in landscape dashboard space (see drawDashboard layout)
const GRAPH_N = [0.8, 0.575];

export default function (ctx) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  scene.environment = ctx.env.strips;
  const camera = new THREE.PerspectiveCamera(30, ctx.aspect, 0.01, 60);

  const phone = new THREE.Group();
  scene.add(phone);
  const ti = new THREE.MeshPhysicalMaterial({ color: 0xb9bec5, metalness: 1, roughness: 0.3, envMapIntensity: 1.25, anisotropy: 0.7, clearcoat: 0.25 });
  const body = new THREE.Mesh(new RoundedBoxGeometry(PW, PH, PD, 8, PR), ti);
  phone.add(body);

  // Display: a rounded-corner canvas, then a cover glass that carries studio reflections.
  const SCW = 720, SCH = Math.round(720 * (PH - 0.05) / (PW - 0.05));
  const scr = canvas(SCW, SCH), sg = scr.getContext('2d');
  const dash = canvas(SCH, SCW), dg = dash.getContext('2d');
  const store = canvas(SCW, SCH), stg = store.getContext('2d');
  const scrTex = new THREE.CanvasTexture(scr);
  scrTex.colorSpace = THREE.SRGBColorSpace; scrTex.anisotropy = 8;
  const shape = new THREE.Shape();
  {
    const w = PW - 0.05, h = PH - 0.05, r = PR - 0.03;
    shape.moveTo(-w / 2 + r, -h / 2); shape.lineTo(w / 2 - r, -h / 2); shape.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r);
    shape.lineTo(w / 2, h / 2 - r); shape.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2); shape.lineTo(-w / 2 + r, h / 2);
    shape.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r); shape.lineTo(-w / 2, -h / 2 + r); shape.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2);
  }
  const scrGeo = new THREE.ShapeGeometry(shape, 12);
  {
    const uv = scrGeo.attributes.uv, p = scrGeo.attributes.position;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, p.getX(i) / (PW - 0.05) + 0.5, p.getY(i) / (PH - 0.05) + 0.5);
  }
  const screenMat = new THREE.MeshBasicMaterial({ map: scrTex, toneMapped: false });
  const screen = new THREE.Mesh(scrGeo, screenMat);
  screen.position.z = PD / 2 + 0.0008;
  phone.add(screen);
  const coverMat = new THREE.MeshPhysicalMaterial({ color: 0x000000, roughness: 0.02, metalness: 0, clearcoat: 1, transparent: true, opacity: 0.22, envMapIntensity: 1.4, depthWrite: false });
  const cover = new THREE.Mesh(scrGeo, coverMat);
  cover.position.z = PD / 2 + 0.0016;
  phone.add(cover);
  // Back: a single machined lens ring, deliberately generic.
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.012, 16, 48), new THREE.MeshPhysicalMaterial({ color: 0xe9ecef, metalness: 1, roughness: 0.12 }));
  ring.position.set(0, PH / 2 - 0.2, -PD / 2 - 0.004);
  const lens = new THREE.Mesh(new THREE.CircleGeometry(0.066, 40), new THREE.MeshPhysicalMaterial({ color: 0x050607, roughness: 0.02, clearcoat: 1 }));
  lens.position.set(0, PH / 2 - 0.2, -PD / 2 - 0.0045);
  lens.rotation.y = Math.PI;
  phone.add(ring, lens);

  // Edge light: the outline signal from Scene 04 lingers on the frame and fades out.
  const edge = new THREE.Mesh(
    new THREE.TorusGeometry(1, 0.003, 4, 4),
    new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, toneMapped: false })
  );
  edge.visible = false;

  const dust = motes({ count: 1500, box: [6, 6, 6], center: [0, 0, -1], seed: 55, H: ctx.H, brightness: 0.35 });
  scene.add(dust);
  const key = new THREE.DirectionalLight(0xffffff, 0.8); key.position.set(-2, 3, 3);
  scene.add(key);

  let lastKey = '';
  function paintScreen(t) {
    // screen sequence: off → app → (hidden swap during the turn) store → dashboard
    let k;
    if (t < 12.25) k = 'off';
    else if (t < 13.45) k = 'app';
    else if (t < 14.35) k = 'store';
    else k = 'dash';
    const q = Math.round(t * 60);
    const keyNow = `${k}:${q}`;
    if (keyNow === lastKey) return;
    lastKey = keyNow;
    sg.save();
    if (k === 'off') { sg.fillStyle = '#020203'; sg.fillRect(0, 0, SCW, SCH); }
    else if (k === 'app') drawPhoneApp(sg, SCW, SCH, t, inv(12.25, 13.0, t));
    else if (k === 'store') drawPhoneStore(sg, SCW, SCH, t, inv(13.45, 14.05, t));
    else {
      drawDashboard(dg, SCH, SCW, t, inv(14.2, 14.9, t), smooth(15.15, 15.85, t));
      sg.save();
      sg.translate(SCW, 0); sg.rotate(Math.PI / 2);
      sg.drawImage(dash, 0, 0);
      sg.restore();
      // the store dissolves into the dashboard rather than cutting through black
      const xf = 1 - smooth(14.35, 14.7, t);
      if (xf > 0) {
        drawPhoneStore(stg, SCW, SCH, t, 1);
        sg.globalAlpha = xf; sg.drawImage(store, 0, 0); sg.globalAlpha = 1;
      }
    }
    sg.restore();
    // power-on: the display wakes with a soft rise
    if (k === 'app' && t < 12.6) { sg.fillStyle = `rgba(0,0,0,${1 - inv(12.25, 12.6, t)})`; sg.fillRect(0, 0, SCW, SCH); }
    scrTex.needsUpdate = true;
  }

  const graphLocal = () => {
    // landscape (gx, gy) → portrait canvas (SCW - gy*SCW, gx*SCH) → screen local
    const cx = SCW - GRAPH_N[1] * SCW, cy = GRAPH_N[0] * SCH;
    return new THREE.Vector3((cx / SCW - 0.5) * (PW - 0.05), (0.5 - cy / SCH) * (PH - 0.05), PD / 2);
  };

  function update(t) {
    paintScreen(t);
    dust.userData.tick(t);
    // Body materialises from the traced outline.
    const mat = smooth(12.0, 12.45, t);
    ti.opacity = mat; ti.transparent = mat < 1;
    body.visible = mat > 0.001;

    // Device motion: yaw swing, one full turn (store swap hidden at the back), roll to landscape.
    const swing = -0.42 * prog(12.2, 13.0, t, ease.inOutCubic);
    const turn = TAU * prog(12.95, 13.95, t, ease.inOutQuart);
    const settle = 0.42 * prog(13.6, 14.3, t, ease.inOutCubic);
    const roll = (Math.PI / 2) * prog(14.25, 14.95, t, ease.inOutQuart);
    const tilt = 0.12 * Math.sin(prog(12.2, 14.9, t) * Math.PI);
    phone.rotation.set(tilt, swing + turn + settle - 0.1 * smooth(14.3, 15.0, t), roll, 'YXZ');
    phone.position.y = 0.03 * Math.sin((t - 12) * 1.3);
    phone.updateMatrixWorld();

    // Camera: continuous slow orbit while closing distance, then a push into the integrations map.
    const phi = lerp(0, 0.38, prog(12.0, 15.0, t, ease.inOutSine));
    const R = lerp(START_DIST, 3.9, prog(12.1, 15.0, t, ease.inOutCubic));
    const pos = new THREE.Vector3(Math.sin(phi) * R, 0.12 * Math.sin(phi * 2), Math.cos(phi) * R);
    const look = new THREE.Vector3(0, 0, 0);
    const push = prog(15.0, 16.35, t, ease.inOutCubic);
    if (push > 0) {
      const gw = phone.localToWorld(graphLocal());
      const nrm = new THREE.Vector3(0, 0, 1).applyQuaternion(phone.quaternion);
      pos.lerp(gw.clone().addScaledVector(nrm, 0.42), push);
      look.lerp(gw, smooth(15.0, 15.4, t));
    }
    camera.position.copy(pos);
    camera.lookAt(look);
    camera.updateMatrixWorld();
    return { scene, camera, exposure: 1.0, bloom: [0.3 + 0.45 * smooth(15.4, 16.0, t), 0.6, 0.8 - 0.12 * smooth(15.4, 16, t)] };
  }

  function overlay(g, t, alpha) {
    g.globalAlpha = alpha;
    scrim(g, ctx.W, ctx.H, smooth(12.3, 12.7, t) * (1 - smooth(14.9, 15.2, t)), 360, 360);
    drawTitle(g, ctx.W, t, { lines: ['BEYOND', 'THE SCREEN.'], start: 12.4, end: 15.1, y: 330, size: 62 });
    g.globalAlpha = 1;
  }

  return { start: 12, end: 16, xIn: 0.25, update, overlay };
}
