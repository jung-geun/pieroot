import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import { mdsvex } from "mdsvex";
import path from "path";

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  extensions: [".svelte", ".svx"],
  preprocess: [
    vitePreprocess(),
    mdsvex({
      extensions: [".svx"],
    }),
  ],
  kit: {
    vite: {
      resolve: {
        alias: {
          $components: path.resolve("./src/components"),
          $lib: path.resolve("./src/lib"),
        },
      },
    },
  },
};
