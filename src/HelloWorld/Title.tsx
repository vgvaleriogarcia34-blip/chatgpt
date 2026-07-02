import { interpolate, useCurrentFrame } from "remotion";

export const Title: React.FC<{
  titleText: string;
  titleColor: string;
}> = ({ titleText, titleColor }) => {
  const text = titleText.split(" ").map((t) => ` ${t} `);
  const frame = useCurrentFrame();

  return (
    <h1
      style={{
        fontFamily: "SF Pro Text, Helvetica, Arial, sans-serif",
        fontWeight: "bold",
        fontSize: 100,
        textAlign: "center",
        position: "absolute",
        bottom: 160,
        width: "100%",
      }}
    >
      {text.map((t, i) => {
        return (
          <span
            key={t}
            style={{
              color: titleColor,
              marginLeft: 10,
              marginRight: 10,
              transform: `scale(${interpolate(
                frame,
                [i * 5, i * 5 + 15],
                [0, 1],
                {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                },
              )})`,
              display: "inline-block",
            }}
          >
            {t}
          </span>
        );
      })}
    </h1>
  );
};
