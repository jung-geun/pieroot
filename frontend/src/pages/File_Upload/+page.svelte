<script lang="ts">
  import Error from "$components/Error.svelte";
  import fastapi from "$lib/api";
  import { Circle3 } from "svelte-loading-spinners";
  import { push } from "svelte-spa-router";
  let loading = false;
  let error = { detail: "" };
  let files: FileList | any[], input: HTMLInputElement;
  let file_list: any[] = [];

  fastapi(
    "me",
    "/users/me",
    {},
    (json: any) => {
      if (json.detail == "Unauthenticated") {
        push("/login");
      }
    },
    (json_error: any) => {
      push("/login");
    }
  );

  async function get_file_list() {
    fastapi(
      "file_list",
      "/api/file/list",
      {},
      (json: any) => {
        file_list = json.file_list;
      },
      (json_error: any) => {
        file_list = ["리스트를 불러오는데 실패했습니다."];
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
        error = { detail: json.detail };
      },
      (json_error: any) => {
        loading = false;
        error = json_error;
      }
    );
  }

  $: if (error.detail != "") {
    setTimeout(() => {
      error.detail = "";
      input.value = "";
      files = [];
    }, 5000);
  }
</script>

<main>
  <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 whitespace-normal">
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
    <form method="post" enctype="multipart/form-data">
      <div>
        <input
          type="file"
          id="file_input"
          class="file:mr-4 file:py-2 file:px-4
        file:rounded-full file:border-0
        file:text-sm file:font-semibold
        file:bg-violet-50 file:text-violet-700
        hover:file:bg-violet-100 file:border-solid"
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
      </div>
    </form>
    <br />
    <div>
      <ul class="">
        {#await get_file_list()}
          <li>리스트를 불러오는 중 입니다...</li>
        {:then}
          {#each file_list as name, key}
            <li>- {name}</li>
          {/each}
        {:catch error}
          {error}
        {/await}
      </ul>
    </div>
  </div>
</main>
