import * as THREE from 'three';
import { rng } from './util.js';

// Suspended metallic vapour: the same particle material appears in every scene so the
// whole film reads as one continuous physical universe.
export function motes({ count = 3000, box = [8, 8, 8], center = [0, 0, 0], seed = 7, size = 1.6, brightness = 0.5, H = 1920, drift = 0.04 }) {
  const r = rng(seed);
  const p = new Float32Array(count * 3), s = new Float32Array(count);
  for (let i = 0; i < count; i++) {
    p[i * 3] = center[0] + (r() - 0.5) * box[0];
    p[i * 3 + 1] = center[1] + (r() - 0.5) * box[1];
    p[i * 3 + 2] = center[2] + (r() - 0.5) * box[2];
    s[i] = r();
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(p, 3));
  g.setAttribute('aSeed', new THREE.BufferAttribute(s, 1));
  g.boundingSphere = new THREE.Sphere(new THREE.Vector3(...center), 100);
  const mat = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uPx: { value: H / 1920 }, uSize: { value: size }, uB: { value: brightness }, uDrift: { value: drift } },
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: /* glsl */ `
      attribute float aSeed; uniform float uT, uPx, uSize, uDrift; varying float vA;
      void main(){
        vec3 p = position;
        float s = aSeed * 6.2831;
        p += uDrift * vec3(sin(uT * 0.31 + s * 3.0), sin(uT * 0.23 + s * 5.0) + uT * 0.35, cos(uT * 0.27 + s * 7.0));
        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        gl_Position = projectionMatrix * mv;
        float d = -mv.z;
        vA = (0.35 + 0.65 * pow(0.5 + 0.5 * sin(uT * (0.7 + aSeed * 2.3) + s * 11.0), 4.0)) * smoothstep(0.15, 0.8, d) * smoothstep(30.0, 6.0, d);
        gl_PointSize = uPx * uSize * (0.6 + aSeed) * clamp(3.0 / d, 0.3, 4.0);
      }`,
    fragmentShader: /* glsl */ `
      uniform float uB; varying float vA;
      void main(){ float f = smoothstep(0.5, 0.0, length(gl_PointCoord - 0.5)); gl_FragColor = vec4(vec3(0.86, 0.89, 0.93) * vA * f * uB, 1.0); }`,
  });
  const pts = new THREE.Points(g, mat);
  pts.frustumCulled = false;
  pts.userData.tick = (t) => { mat.uniforms.uT.value = t; };
  return pts;
}

// Polished dark floor plus clip planes for mirrored "reflection" geometry: true planar
// reflections without the cost of re-rendering the scene.
export function darkFloor({ size = 60, color = 0x07080a, opacity = 0.82, roughness = 0.22, map = null, envI = 0.25 }) {
  const m = new THREE.MeshPhysicalMaterial({
    color, roughness, metalness: 0.9, clearcoat: 0.35, clearcoatRoughness: 0.12, transparent: true, opacity, map, envMapIntensity: envI,
  });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(size, size), m);
  floor.rotation.x = -Math.PI / 2;
  return floor;
}

export const ABOVE = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
export const BELOW = new THREE.Plane(new THREE.Vector3(0, -1, 0), 0);

// Mirror a mesh/group under the y=0 floor; the clone keeps live references to the source.
export function mirrorOf(obj, dim = 0.45) {
  const m = obj.clone(true);
  m.scale.y *= -1;
  m.traverse((o) => {
    if (o.isMesh) {
      o.material = (Array.isArray(o.material) ? o.material : [o.material]).map((mt) => {
        const c = mt.clone();
        c.clippingPlanes = [BELOW];
        if (c.color) c.color.multiplyScalar(dim);
        if (c.emissive) c.emissiveIntensity *= dim;
        if (c.envMapIntensity !== undefined) c.envMapIntensity *= dim;
        return c;
      });
      if (o.material.length === 1) o.material = o.material[0];
    }
  });
  return m;
}

// Copy animated transforms (and opacity) from a source tree onto its mirrored clone.
export function syncMirror(src, dst) {
  const a = [], b = [];
  src.traverse((o) => a.push(o));
  dst.traverse((o) => b.push(o));
  for (let i = 1; i < a.length; i++) {
    b[i].position.copy(a[i].position);
    b[i].quaternion.copy(a[i].quaternion);
    b[i].scale.copy(a[i].scale);
    b[i].visible = a[i].visible;
    if (a[i].isMesh && !Array.isArray(a[i].material) && a[i].material.transparent) b[i].material.opacity = a[i].material.opacity * 0.5;
  }
  dst.position.set(src.position.x, -src.position.y, src.position.z);
  dst.rotation.set(-src.rotation.x, src.rotation.y, -src.rotation.z);
}
