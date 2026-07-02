import { AbsoluteFill } from "remotion";
import { Arc } from "./Arc";

export const Atom: React.FC<{
  logoColor1: string;
  logoColor2: string;
  scale: number;
  rotation: number;
}> = ({ scale, rotation, logoColor1, logoColor2 }) => {
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        transform: `scale(${scale}) rotate(${rotation}rad)`,
      }}
    >
      <Arc logoColor1={logoColor1} logoColor2={logoColor2} />
    </AbsoluteFill>
  );
};
