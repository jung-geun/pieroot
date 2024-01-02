<script lang="ts">
  import { domain } from "$src/stores/store";
  import { get } from "svelte/store";

  // @ts-ignore
  import Content from "./markdown.md";
  // @ts-ignore
</script>

<main>
  <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 whitespace-normal">
    <div
      class="bg-slate-500 dark:bg-gray-500 rounded-lg shadow-lg px-5 py-6 sm:px-6 md:px-8 mb-6 grid grid-rows-2"
    >
      <div class="">
        <p class="text-white mx-4">파일 다운로드</p>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4">
        <a
          href="{get(domain)}/file/public/cv.pdf"
          class="bg-gray-800 text-white block rounded-md px-3 py-2 text-base font-medium hover:bg-gray-700 hover:text-white mx-1"
          >CV</a
        >
        <a
          href="{get(domain)}/file/public/이력서.pdf"
          class="bg-gray-800 text-white block rounded-md px-3 py-2 text-base font-medium hover:bg-gray-700 hover:text-white mx-1"
          >이력서</a
        >
      </div>
    </div>
    <Content />
  </div>
</main>
