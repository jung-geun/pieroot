<script>
  // import { file_upload } from "./+page.server.svelte";
  import { getHello } from "./+page.server.svelte";
  // import { user_check } from "../../components/Header.svelte";

  // if (!user_check) {
    // window.location.href = "/";
  // }
</script>

<div class="bg-white rounded-b-lg shadow-2xl">
  <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
    <h1 class="text-3xl font-bold tracking-tight text-gray-900">file upload</h1>
  </div>
</div>

<main>
  <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 whitespace-normal">
    <form
      action="/api/file/upload"
      method="post"
      enctype="multipart/form-data"
    >
      <div>
        <input
          type="file"
          name="files"
          class="file:mr-4 file:py-2 file:px-4
        file:rounded-full file:border-0
        file:text-sm file:font-semibold
        file:bg-violet-50 file:text-violet-700
        hover:file:bg-violet-100 file:border-solid"
          multiple
        />
      </div>
      <button type="submit">submit</button>
    </form>
    <button type="button" on:click={getHello}> hello test</button>
  </div>
</main>
