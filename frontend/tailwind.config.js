/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");
export default {
  content: ["./index.html", "./src/**/*.{js,ts,svelte,tsx,jsx}"],
  theme: {
    extend: {
      colors: {
        lightsteelblue: "#F0F8FF",
        steelblue: "#B0C4DE",
      },
    },
  },
  darkmode: "class",
  plugins: [
    plugin(function ({ addBase, config }) {
      addBase({
        h1: { fontSize: config("theme.fontSize.2xl") },
        h2: { fontSize: config("theme.fontSize.xl") },
        h3: { fontSize: config("theme.fontSize.lg") },
        h4: { fontSize: config("theme.fontSize.base") },
        h5: { fontSize: config("theme.fontSize.sm") },
        h6: { fontSize: config("theme.fontSize.xs") },
      });
    }),
  ],
};
