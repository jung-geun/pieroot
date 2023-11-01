import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import { mdsvex } from "mdsvex";
import remarkGrm from "remark-gfm";
import github from "remark-github";

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  extensions: [".svelte", ".md"],
  preprocess: [
    vitePreprocess(),
    mdsvex({
      extensions: [".md"],
      remarkPlugins: [
        [remarkGrm, { singleTilde: false }],
        [github, { repository: "https://github.com/jung-geun/pieroot" }],
      ],
    }),
  ],
};
