export const Arc: React.FC<{
  logoColor1: string;
  logoColor2: string;
}> = ({ logoColor1, logoColor2 }) => {
  const height = 600;
  const width = 300;

  return (
    <svg
      width={height}
      height={height}
      viewBox={`0 0 ${height} ${height}`}
      style={{
        position: "absolute",
      }}
    >
      <defs>
        <linearGradient
          id={`gradient-${logoColor1}-${logoColor2}`}
          x1="0"
          y1="0"
          x2="1"
          y2="1"
        >
          <stop offset="0" stopColor={logoColor1} />
          <stop offset="1" stopColor={logoColor2} />
        </linearGradient>
      </defs>
      <ellipse
        cx={height / 2}
        cy={height / 2}
        rx={width / 2}
        ry={height / 2.5}
        stroke={`url(#gradient-${logoColor1}-${logoColor2})`}
        strokeWidth={20}
        fill="none"
      />
    </svg>
  );
};
