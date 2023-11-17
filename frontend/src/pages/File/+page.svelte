<script lang="ts">
  import Error from "$components/Error.svelte";
  import fastapi from "$lib/ts/api";
  import { access_token, test_url } from "$stores/store";
  import { onMount } from "svelte";
  import { Circle3 } from "svelte-loading-spinners";
  import { push } from "svelte-spa-router";
  import { get } from "svelte/store";
  let loading = false;
  let error = { detail: "" };
  let files: FileList | any[], input: HTMLInputElement;
  let file_list: any[] = [];
  let currentPage = 1;
  let page_size = 10;
  let sort: string = "asc";
  let sortBy: string = "name";
  let file_count: number = 0;

  onMount(() => {
    get_file_list();
  });

  function sort_prev() {
    currentPage--;
    get_file_list();
  }
  function sort_next() {
    currentPage++;
    get_file_list();
  }

  async function get_file_list() {
    if (currentPage < 1) {
      currentPage = 1;
    }

    let start = (currentPage - 1) * page_size;
    let end = currentPage * page_size;

    let params = {
      start: start,
      end: end,
      sort: sort,
      order: sortBy,
    };

    fastapi(
      "get",
      "/file/list",
      params,
      (json: any) => {
        file_list = json.file_list;
        file_count = json.file_count;
      },
      (json_error: any) => {
        error = json_error;
      }
    );
  }

  function file_upload(event: any) {
    event.preventDefault();
    loading = true;
    let url = "/file/upload";
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
        get_file_list();
      },
      (json_error: any) => {
        loading = false;
        console.log(json_error);
        error = json_error;
      }
    );
  }

  function file_download(event: Event, file_name: string) {
    event.preventDefault();
    let url = test_url + "/file/download/" + file_name;
    let option = {
      method: "get",
      headers: {
        Authorization: "Bearer " + get(access_token),
      },
      body: null,
    };
    fetch(url, option).then((response) => {
      if (response.status == 200) {
        response.blob().then((blob) => {
          let fileUrl = window.URL.createObjectURL(blob);
          let a = document.createElement("a");

          a.href = fileUrl;
          a.download = file_name;
          console.log(file_name);

          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        });
      } else {
        error = { detail: "파일을 다운로드하는데 실패했습니다" };
      }
    });
  }

  function file_delete(file_name: string) {
    let delete_ = confirm(file_name + " 파일을 정말로 삭제하시겠습니까?");
    if (delete_ == true) {
      loading = true;
      let url = "/file/delete";
      let param = { file_name: file_name };

      fastapi(
        "delete",
        url,
        param,
        (json: any) => {
          loading = false;
          console.log(json.detail);
          error = { detail: json.detail };
          get_file_list();
        },
        (json_error: any) => {
          loading = false;
          console.log(json_error);
          error = json_error;
        }
      );
    }
  }

  $: if (error.detail === "Unauthorized") {
    push("/logout");
  } else if (error.detail != "") {
    setTimeout(() => {
      error.detail = "";
      input.value = "";
      files = [];
    }, 5000);
  }

  // $: console.log(loading);
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
    <form
      method="post"
      enctype="multipart/form-data"
      class="auto-rows-auto grid grid-cols-5"
    >
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
        class="px-5 py-2 relative rounded group overflow-hidden font-medium bg-white text-violet-700 inline-block"
        disabled={!files || files.length == 0 || loading}
        on:click={file_upload}
      >
        <span
          class="absolute top-0 left-0 flex w-full h-0 mb-0 transition-all duration-200 ease-out transform translate-y-0 bg-violet-700 group-hover:h-full opacity-90"
        />
        <span class="relative group-hover:text-white">Submit</span>
      </button>
    </form>
    <br />
    <div class="whitespace-normal">
      <ul role="list">
        {#await get_file_list()}
          <li>리스트를 불러오는 중 입니다...</li>
        {:then}
          {#each file_list as info, key}
            <li
              class="border-none hover:bg-slate-600 w-104 hover:border-solid hover:border-sky-50 rounded-md py-0.3 px-2 grid grid-cols-5 gap-15"
            >
              <a
                href="/#"
                class="col-span-3 text-ellipsis overflow-hidden"
                on:click={file_download(event, info["name"])}>{info["name"]}</a
              >
              <p class="text-right">{info["size"]}</p>
              <button
                class="border-collapse"
                on:click={file_delete(info["name"])}>제거</button
              >
            </li>
          {/each}
        {:catch error}
          <li>파일을 불러오는데 실패했습니다</li>
        {/await}
      </ul>
    </div>

    <div class="mt-4 flex justify-between items-center">
      <div>
        <button
          on:click={sort_prev}
          disabled={currentPage <= 1}
          class="rounded-md px-3.5 py-1 m-1 overflow-hidden relative group cursor-pointer border-2 font-medium border-indigo-600 text-indigo-600 bg-slate-300"
        >
          <span
            class="absolute w-64 h-0 transition-all duration-300 origin-center rotate-45 -translate-x-20 bg-indigo-600 top-1/2 group-hover:h-64 group-hover:-translate-y-32 ease"
          />
          <span
            class="relative text-indigo-600 transition duration-300 group-hover:text-white ease"
            >Prev</span
          >
        </button>
        <span class="text-indigo-100">
          {currentPage * page_size - page_size + 1} - {currentPage * page_size -
            page_size +
            file_list.length} of
          {file_count} files
        </span>
        <button
          class="rounded-md px-3.5 py-1 m-1 overflow-hidden relative group cursor-pointer border-2 font-medium border-indigo-600 text-indigo-600 bg-slate-300"
          on:click={sort_next}
          disabled={currentPage * page_size >= file_count}
        >
          <span
            class="absolute w-64 h-0 transition-all duration-300 origin-center rotate-45 -translate-x-20 bg-indigo-600 top-1/2 group-hover:h-64 group-hover:-translate-y-32 ease"
            aria-disabled="true"
          />
          <span
            class="relative text-indigo-600 transition duration-300 group-hover:text-white ease"
            >Next</span
          ></button
        >
      </div>
      <div>
        <label for="sort">Sort by:</label>
        <select
          id="sort"
          class="text-black border p-2 rounded border-black"
          bind:value={sortBy}
          on:change={get_file_list}
        >
          <option value="name">Name</option>
          <option value="size">Size</option>
          <!-- Add more sorting options if needed -->
        </select>
      </div>
    </div>
  </div>
</main>
