import { z } from "zod";
import {
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  spring,
  AbsoluteFill,
} from "remotion";
import { Atom } from "./Atom";
import { zColor } from "@remotion/zod-types";

export const myCompSchema2 = z.object({
  logoColor1: zColor(),
  logoColor2: zColor(),
});

export const Logo: React.FC<z.infer<typeof myCompSchema2>> = ({
  logoColor1,
  logoColor2,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const development = spring({
    frame,
    fps,
    config: {
      damping: 100,
      stiffness: 10,
      mass: 0.5,
    },
  });

  const rotationDevelopment = spring({
    frame,
    fps,
    config: {
      damping: 100,
      mass: 0.5,
    },
  });

  const scale = interpolate(development, [0, 1], [0.8, 1]);

  const rotation = interpolate(rotationDevelopment, [0, 1], [0, Math.PI]);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
        }}
      >
        <Atom
          scale={1}
          rotation={rotation + Math.PI * 0.5}
          logoColor1={logoColor1}
          logoColor2={logoColor2}
        />
        <Atom
          scale={1}
          rotation={rotation + Math.PI * (1 / 3) + Math.PI * 0.5}
          logoColor1={logoColor1}
          logoColor2={logoColor2}
        />
        <Atom
          scale={1}
          rotation={rotation + Math.PI * (2 / 3) + Math.PI * 0.5}
          logoColor1={logoColor1}
          logoColor2={logoColor2}
        />
      </div>
    </AbsoluteFill>
  );
};
