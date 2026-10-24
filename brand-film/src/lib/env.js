import * as THREE from 'three';

// Automotive-style studio for reflections: a black cyclorama lit only by a few
// long, soft strip lights. Gives chrome and glass clean, intentional highlights
// instead of the busy box-room look of a stock environment.
export function buildStudioEnv(renderer, variant = 'strips') {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  const dome = new THREE.Mesh(
    new THREE.SphereGeometry(50, 32, 16),
    new THREE.MeshBasicMaterial({ color: 0x050607, side: THREE.BackSide })
  );
  scene.add(dome);

  const strip = (w, h, intensity, pos, look, tint = 0xffffff) => {
    const m = new THREE.Mesh(
      new THREE.PlaneGeometry(w, h),
      new THREE.MeshBasicMaterial({ color: new THREE.Color(tint).multiplyScalar(intensity), side: THREE.DoubleSide })
    );
    m.position.set(...pos);
    m.lookAt(...look);
    scene.add(m);
  };

  if (variant === 'strips') {
    strip(30, 1.2, 6, [0, 14, -2], [0, 0, 0]);          // long overhead strip
    strip(1.0, 22, 4, [-16, 2, 6], [0, 0, 0]);          // tall left key strip
    strip(0.7, 22, 2.6, [15, 2, 2], [0, 0, 0], 0xdfe6ee); // right fill strip, faintly cool
    strip(18, 0.6, 3, [0, 3, -18], [0, 0, 0]);          // rim strip behind subject
    strip(6, 6, 0.35, [0, -10, 10], [0, 0, 0], 0x8ea6bf); // low cool bounce
  } else if (variant === 'chrome') {
    // liquid-metal studio: a dim gradient sky, a horizon band and long strips, so chrome reads as chrome
    const sky = new THREE.Mesh(new THREE.SphereGeometry(45, 48, 24), new THREE.ShaderMaterial({
      side: THREE.BackSide,
      vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
      fragmentShader: 'varying vec3 vP; void main(){ float y = vP.y; vec3 c = mix(vec3(0.015), vec3(0.22,0.23,0.25), smoothstep(-0.1, 0.9, y)); c += vec3(0.9) * exp(-pow((y - 0.02) * 22.0, 2.0)) * 0.6; gl_FragColor = vec4(c, 1.0); }',
    }));
    scene.add(sky);
    strip(30, 1.6, 7, [0, 14, -2], [0, 0, 0]);
    strip(1.4, 22, 5, [-16, 2, 6], [0, 0, 0]);
    strip(1.0, 22, 3.5, [15, 2, 2], [0, 0, 0], 0xdfe6ee);
    strip(20, 0.8, 4, [0, 3, -18], [0, 0, 0]);
    strip(1.0, 16, 3, [6, 2, 16], [0, 0, 0]);
    strip(1.0, 16, 2.5, [-7, 2, 15], [0, 0, 0], 0xdfe6ee);
  } else if (variant === 'soft') {
    strip(24, 6, 2.2, [0, 14, 0], [0, 0, 0]);
    strip(2.5, 18, 2.4, [-14, 0, 8], [0, 0, 0]);
    strip(2.0, 18, 1.4, [14, 0, 4], [0, 0, 0], 0xdfe6ee);
    strip(18, 1.0, 2.0, [0, 2, -16], [0, 0, 0]);
  }

  const pmrem = new THREE.PMREMGenerator(renderer);
  const tex = pmrem.fromScene(scene, 0.02).texture;
  pmrem.dispose();
  return tex;
}
