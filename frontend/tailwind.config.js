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
  plugins: [
    plugin(function ({ addBase, config }) {
      addBase({
        h1: {
          fontSize: config("theme.fontSize.4xl"),
          fontWeight: config("theme.fontWeight.bold"),
        },
        h2: {
          fontSize: config("theme.fontSize.2xl"),
          fontWeight: config("theme.fontWeight.bold"),
        },
        h3: {
          fontSize: config("theme.fontSize.xl"),
          fontWeight: config("theme.fontWeight.bold"),
        },
        h4: { fontSize: config("theme.fontSize.lg") },
        h5: { fontSize: config("theme.fontSize.base") },
        h6: { fontSize: config("theme.fontSize.text-sm") },
      });
    }),
  ],
};
