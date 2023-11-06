<script lang="ts">
  import Error from "$components/Error.svelte";
  import fastapi from "$lib/api";
  import { test_url } from "$stores/store";
  import { Circle3 } from "svelte-loading-spinners";
  import { push } from "svelte-spa-router";
  let loading = false;
  let error = { detail: "" };
  let files: FileList | any[], input: HTMLInputElement;
  let file_list: any[] = [];

  async function get_file_list() {
    fastapi(
      "file_list",
      "/api/file/list",
      {},
      (json: any) => {
        file_list = json.file_list;
      },
      (json_error: any) => {
        error = json_error;
      }
    );
  }

  function file_upload(event: any) {
    event.preventDefault();
    loading = true;

    let url = "/api/file/upload";
    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    fastapi(
      "file_upload",
      url,
      formData,
      (json: any) => {
        loading = false;
        console.log(json.detail);
        error = { detail: json.detail };
      },
      (json_error: any) => {
        loading = false;
        console.log(json_error);
        error = json_error;
      }
    );
  }

  $: if (error.detail != "") {
    setTimeout(() => {
      error.detail = "";
      input.value = "";
      files = [];
      get_file_list();
    }, 5000);
  }
</script>

<main>
  <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 grid place-items-center">
    <Error {error} />
    <br />
    {#if loading == true}
      <!-- popup -->
      <div class="fixed inset-0 flex items-center justify-center">
        <div class="absolute inset-0 bg-gray-500 opacity-75" />
        <div class="z-10 bg-white rounded-lg p-4">
          <div class="flex justify-center">
            <Circle3 size="60" unit="px" duration="2s" />
          </div>
        </div>
      </div>
    {/if}
    <form method="post" enctype="multipart/form-data" class="auto-rows-auto grid  grid-cols-5">
      <input
        type="file"
        id="file_input"
        class="file:mr-4 file:py-2 file:px-4
        file:rounded-full file:border-0
        file:text-sm file:font-semibold
        file:bg-violet-50 file:text-violet-700
        hover:file:bg-violet-100 file:border-solid col-span-4"
        multiple
        bind:files
        bind:this={input}
      />

      <button
        type="submit"
        class="border-solid border-2 border-black rounded-md px-4 py-2
        hover:bg-gray-100 hover:border-gray-300 hover:text-black hover:shadow-md
        "
        disabled={!files || files.length == 0 || loading}
        on:click={file_upload}>submit</button
      >
    </form>
    <br />
    <div class="whitespace-normal">
      <ul role="list">
        {#await get_file_list()}
          <li>리스트를 불러오는 중 입니다...</li>
        {:then}
          {#each file_list as info, key}
            <li
              class="border-none hover:bg-slate-600 w-104 hover:border-solid hover:border-sky-50 rounded-md py-0.3 px-2 grid grid-cols-4 gap-15"
            >
              <a
                href="{test_url}/api/file/download/{info['name']}"
                class="col-span-3 text-ellipsis overflow-hidden"
                >{info["name"]}</a
              >
              <p class="text-right">{info["size"]}</p>
              <button>삭제</button>
            </li>
          {/each}
        {:catch error}
          <li>파일을 불러오는데 실패했습니다</li>
        {/await}
      </ul>
    </div>
  </div>
</main>
