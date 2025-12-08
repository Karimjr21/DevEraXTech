import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import { useEffect, useRef, useState } from 'react';

function RotatingLogo() {
  const meshRef = useRef();
  const { size } = useThree();
  // Responsive scale based on viewport width
  const scale = Math.max(0.6, Math.min(1.0, size.width / 1400));
  useFrame(({ clock }) => {
    if (meshRef.current) meshRef.current.rotation.y = clock.getElapsedTime() * 0.2;
  });
  const material = new THREE.MeshPhysicalMaterial({
    color: '#d4af37',
    metalness: 1,
    roughness: 0.15,
    clearcoat: 1,
    clearcoatRoughness: 0.05,
    envMapIntensity: 1.2,
    emissive: '#d4af37',
    emissiveIntensity: 0.3
  });
  return (
    <mesh ref={meshRef} material={material} scale={scale}>
      <torusKnotGeometry args={[2.2, 0.7, 220, 64]} />
    </mesh>
  );
}

function CinematicCamera() {
  const { camera } = useThree();
  const tRef = useRef(0);
  useFrame((state, delta) => {
    tRef.current += delta * 0.05;
    const r = 10;
    camera.position.x = Math.sin(tRef.current) * r * 0.4;
    camera.position.z = 10 + Math.cos(tRef.current * 0.7) * 1.2;
    camera.position.y = Math.sin(tRef.current * 0.6) * 0.6;
    camera.lookAt(0, 0, 0);
  });
  return null;
}

function Particles() {
  const pointsRef = useRef();
  const count = 320;
  const positions = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const r = 12 * Math.random();
    const theta = 2 * Math.PI * Math.random();
    const phi = Math.acos(2 * Math.random() - 1);
    positions[3 * i] = r * Math.sin(phi) * Math.cos(theta);
    positions[3 * i + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[3 * i + 2] = r * Math.cos(phi);
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const material = new THREE.PointsMaterial({ color: '#d4af37', size: 0.12 });
  useFrame(({ clock }) => {
    if (pointsRef.current) pointsRef.current.rotation.y = clock.getElapsedTime() * 0.05;
  });
  return <points ref={pointsRef} args={[geometry, material]} />;
}

function hasWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(
      window.WebGLRenderingContext &&
      (c.getContext('webgl') || c.getContext('experimental-webgl'))
    );
  } catch {
    return false;
  }
}

export default function Logo3D() {
  if (typeof window !== 'undefined' && !hasWebGL()) return null;
  return (
    <div className="fixed inset-0 pointer-events-none z-0">
      <Canvas camera={{ position: [0, 0, 10], fov: 50 }} gl={{ alpha: true, antialias: true }} style={{ background: 'transparent' }}>
        <CinematicCamera />
        <ambientLight intensity={0.8} />
        <directionalLight position={[5, 5, 5]} intensity={1.6} />
        <pointLight position={[-5, -3, 4]} intensity={0.8} />
        <RotatingLogo />
        <Particles />
        <OrbitControls enablePan={false} enableZoom={false} autoRotate autoRotateSpeed={0.2} />
      </Canvas>
    </div>
  );
}
