import { interpolate, useCurrentFrame } from "remotion";

export const Subtitle: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        fontFamily: "SF Pro Text, Helvetica, Arial, sans-serif",
        fontSize: 40,
        textAlign: "center",
        position: "absolute",
        bottom: 140,
        width: "100%",
        opacity,
      }}
    >
      Edit <code style={codeStyle}>src/HelloWorld.tsx</code> and save to reload.
    </div>
  );
};

const codeStyle: React.CSSProperties = {
  color: "black",
  padding: "4px 8px",
  borderRadius: 4,
  backgroundColor: "#EEEEEE",
  fontFamily: "SF Mono, Menlo, monospace",
};
