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
  let search: string = "";
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
    } else if (currentPage * page_size > file_count && file_count != 0) {
      currentPage = Math.ceil(file_count / page_size);
    }

    let start = (currentPage - 1) * page_size;
    let end = currentPage * page_size;

    let params = {
      start: start,
      end: end,
      sort: sort,
      order: sortBy,
      search: search,
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
    let count = 0;
    let lose = 0;
    for (let i = 0; i < files.length; i++) {
      let formData = new FormData();
      formData.append("files", files[i]);
      fastapi(
        "file_upload",
        url,
        formData,
        () => {
          count++;
          error = { detail: count + "개 중 " + lose + "개 업로드 실패" };
        },
        (json_error: any) => {
          lose++;
          count++;
          error = { detail: count + "개 중 " + lose + "개 업로드 실패" };
        }
      );
    }
    setTimeout(() => {
      loading = false;
      get_file_list();
    }, 5000);
  }

  function file_download(event: Event, file_name: string) {
    event.preventDefault();
    let params = { file_name: file_name };
    let url = test_url + "/file/download?" + new URLSearchParams(params);
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

          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        });
      } else {
        response.json().then((json) => {
          error = { detail: json.detail };
        });
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
          error = { detail: json.detail };
          get_file_list();
        },
        (json_error: any) => {
          loading = false;
          error = json_error;
        }
      );
    }
  }

  let searchQuery = "";

  function handleSearch() {
    currentPage = 1;
    search = searchQuery;
    get_file_list();
  }

  let timeoutId = setTimeout(() => {}, 0);

  function handleInputChange() {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(handleSearch, 1000);
  }

  onMount(() => {
    document.addEventListener("keydown", (event) => {
      if (event.key === "/") {
        event.preventDefault();
        const searchInput = document.getElementById("search-input");
        if (searchInput) {
          searchInput.focus();
        }
      }
    });
  });

  $: if (error.detail === "Unauthorized") {
    push("/logout");
  } else if (error.detail != "") {
    setTimeout(() => {
      error.detail = "";
      input.value = "";
      files = [];
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
    <div class="whitespace-normal w-3/4 md:w-5/6">
      <table class="table-auto w-full">
        <thead>
          <tr
            class="border border-solid border-sky-50
        rounded-md py-0.3 px-2 grid grid-cols-5 gap-15
        bg-slate-600"
          >
            <th
              class="col-span-3 text-ellipsis cursor-pointer text-left hover:bg-slate-500 w-104 hover:border-solid hover:border-sky-50 rounded-md py-0.3 px-2"
              on:click={() => {
                sort = sort == "asc" ? "desc" : "asc";
                sortBy = "name";
                get_file_list();
              }}
            >
              파일 이름 <span>
                {#if sortBy == "name"}{#if sort == "asc"}▲{:else}▼{/if}{/if}
              </span>
            </th>
            <th
              class="text-right cursor-pointer hover:bg-slate-500 w-104 hover:border-solid hover:border-sky-50 rounded-md py-0.3 px-2"
              on:click={() => {
                sort = sort == "asc" ? "desc" : "asc";
                sortBy = "size";
                get_file_list();
              }}
            >
              크기
              <span>
                {#if sortBy == "size"}{#if sort == "asc"}▲{:else}▼{/if}{/if}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          {#await get_file_list()}
            <tr>리스트를 불러오는 중 입니다...</tr>
          {:then}
            {#each file_list as info, key}
              <tr
                class="hover:bg-slate-600 w-104 hover:border-solid hover:border-sky-50 rounded-md py-0.3 px-2 grid grid-cols-5 gap-15"
              >
                <td
                  class="col-span-3 text-ellipsis overflow-hidden hover:text-white hover:underline ml-0 mr-auto"
                >
                  <a href="/#" on:click={file_download(event, info["name"])}
                    >{info["name"]}</a
                  >
                </td>
                <td class="text-right">
                  <p>{info["size"]}</p>
                </td>
                <td class=" hover:bg-slate-500 rounded-md py-0.3 px-2 mx-auto">
                  <button on:click={file_delete(info["name"])}>제거</button>
                </td>
              </tr>
            {/each}
          {:catch error}
            <tr>파일을 불러오는데 실패했습니다</tr>
          {/await}
        </tbody>
      </table>
      {#if file_list.length == 0}
        <div class="text-center">파일이 없습니다</div>
      {:else}
        <div class="mt-4 flex justify-end items-center">
          <input
            id="search-input"
            type="text"
            bind:value={searchQuery}
            placeholder="검색어를 입력하세요"
            class="px-4 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-black"
            on:input={handleInputChange}
          />
        </div>
      {/if}
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
          {(currentPage - 1) * page_size + 1} - {(currentPage - 1) * page_size +
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
    </div>
  </div>
</main>
