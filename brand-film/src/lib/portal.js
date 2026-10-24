import * as THREE from 'three';

// A superellipse "portal" swept with a superellipse cross-section. All shape parameters
// are continuous, so the same mesh can morph from a liquid blob into machined architecture.
const sgnPow = (v, e) => Math.sign(v) * Math.pow(Math.abs(v), e);

export function portalMesh(material, U = 320, V = 40) {
  const pos = new Float32Array(U * V * 3);
  const idx = [];
  for (let i = 0; i < U; i++) {
    for (let j = 0; j < V; j++) {
      const a = i * V + j, b = ((i + 1) % U) * V + j, c = ((i + 1) % U) * V + ((j + 1) % V), d = i * V + ((j + 1) % V);
      idx.push(a, b, d, b, c, d);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setIndex(idx);
  const mesh = new THREE.Mesh(g, material);
  mesh.frustumCulled = false;

  // p: { a, b, n, rN, rZ, m, wobble, t }
  mesh.userData.shape = (p) => {
    const P = (th) => [p.a * sgnPow(Math.cos(th), 2 / p.n), p.b * sgnPow(Math.sin(th), 2 / p.n)];
    let k = 0;
    for (let i = 0; i < U; i++) {
      const th = (i / U) * Math.PI * 2;
      const [x0, y0] = P(th);
      const [x1, y1] = P(th + 1e-3);
      let tx = x1 - x0, ty = y1 - y0;
      const tl = Math.hypot(tx, ty) || 1;
      tx /= tl; ty /= tl;
      const nx = ty, ny = -tx; // outward normal in the portal plane
      for (let j = 0; j < V; j++) {
        const ph = (j / V) * Math.PI * 2;
        const cu = sgnPow(Math.cos(ph), 2 / p.m), su = sgnPow(Math.sin(ph), 2 / p.m);
        let X = x0 + nx * cu * p.rN, Y = y0 + ny * cu * p.rN, Z = su * p.rZ;
        if (p.wobble > 0) {
          // layered travelling ripples: liquid metal still finding its form
          const w = p.wobble * (Math.sin(3.1 * X + 2.3 * p.t + 1.7 * Z) + 0.7 * Math.sin(4.3 * Y - 1.9 * p.t + 0.5)
            + 0.5 * Math.sin(5.7 * Z + 2.9 * p.t + 2.0 * X) + 0.35 * Math.sin(9.1 * (X + Y) - 3.3 * p.t));
          const ox = nx * cu, oy = ny * cu, oz = su;
          const ol = Math.hypot(ox, oy, oz) || 1;
          X += (ox / ol) * w; Y += (oy / ol) * w; Z += (oz / ol) * w;
        }
        pos[k++] = X; pos[k++] = Y; pos[k++] = Z;
      }
    }
    g.attributes.position.needsUpdate = true;
    g.computeVertexNormals();
  };
  return mesh;
}
