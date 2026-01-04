"use client";

import { MeshDistortMaterial, Icosahedron } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useRef } from "react";

export default function SceneShape() {
  const ref = useRef<any>(null);

  useFrame((_, delta) => {
    if (!ref.current) return;
    ref.current.rotation.x += delta * 0.2;
    ref.current.rotation.y += delta * 0.16;
  });

  return (
    <Icosahedron ref={ref} args={[2.4, 1]}>
      <MeshDistortMaterial
        color="#A4B4FF"
        speed={0.5}
        distort={0.25}
        roughness={0.2}
        metalness={0.35}
      />
    </Icosahedron>
  );
}
