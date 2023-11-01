import { svelte } from "@sveltejs/vite-plugin-svelte";
import path from "path";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  resolve: {
    alias: {
      $src: path.resolve("./src"),
      $lib: path.resolve("./src/lib"),
      $components: path.resolve("./src/components"),
      $stores: path.resolve("./src/stores"),
      $assets: path.resolve("./src/assets"),
    },
  },
});
