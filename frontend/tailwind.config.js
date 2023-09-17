/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,svelte,tsx,jsx}"],
  theme: {
    extend: {
      colors: {
        'lightsteelblue': '#F0F8FF',
        'steelblue': '#B0C4DE',
      }
    },
  },
  darkmode: "class",
  plugins: [],
};
