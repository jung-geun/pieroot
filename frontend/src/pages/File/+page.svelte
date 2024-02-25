<script lang="ts">
  import { token_get } from "$lib/ts/token";
  import { updateError } from "$src/components/Error.svelte";
  import FastAPI from "$src/lib/ts/api";
  import { access_token, domain, is_login, username } from "$stores/store";
  import { toast } from "@zerodevx/svelte-toast";
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";
  import { get } from "svelte/store";

  let files: FileList | null = null;
  let input: HTMLInputElement;
  let file_list: any[] = [];
  let currentPage = 1;
  let next_flag = false;
  let prev_flag = false;
  let page_size = 10;
  let sort: string = "asc";
  let sortBy: string = "name";
  let search: string = "";
  let file_count: number = 0;

  onMount(() => {
    if (
      get(is_login) === false ||
      get(access_token) === "" ||
      get(username) === ""
    ) {
      push("/logout");
    } else {
      token_get();
      get_file_list();
    }
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

  const sort_prev = () => {
    currentPage--;
    get_file_list();
  };
  const sort_next = () => {
    currentPage++;
    get_file_list();
  };

  const get_file_list = async () => {
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

    FastAPI(
      "get",
      "/file/list",
      params,
      (json: any) => {
        file_list = json.file_list;
        file_count = json.file_count;
        next_flag = currentPage * page_size >= file_count;
        prev_flag = currentPage <= 1;
      },
      (json_error: any) => {
        updateError(json_error.detail);
      }
    );
  };

  const ShortLivedToken = async () => {
    return new Promise((resolve, reject) => {
      FastAPI(
        "post",
        "/users/token/short-lived",
        {},
        (json: any) => {
          resolve(json.access_token);
        },
        (json_error: any) => {
          updateError(json_error.detail);
          reject(json_error.detail);
        }
      );
    });
  };

  const file_upload_check = (files: FileList | null) => {
    if (files && files.length > 10) {
      toast.push("파일은 한번에 10개까지만 업로드 가능합니다.", {
        theme: {
          "--toastBackground": "#f87171",
          "--toastProgressBackground": "#ef4444",
        },
      });
      return false;
    }
    return true;
  };

  const file_upload = async (files: FileList | null, event: any) => {
    event.preventDefault();

    if (!files || files.length == 0) {
      toast.push("파일을 선택해주세요.", {
        theme: {
          "--toastBackground": "#f87171",
          "--toastProgressBackground": "#ef4444",
        },
      });
      return;
    }

    if (file_upload_check(files) == false) {
      files = null;
      input.value = "";
      return;
    }

    const chunk_size = 1024 * 1024;
    const progress_group = document.getElementById("progress_group");
    progress_group?.classList.remove("hidden");

    let fileListArray = Array.from(files);

    try {
      const short_lived_token_promise = await ShortLivedToken();

      const socket_url =
        "wss://" +
        get(domain).split("//")[1] +
        "/file/ws/upload/" +
        short_lived_token_promise;

      for (let i = 0; i < fileListArray.length; i++) {
        const file = fileListArray[i];
        let chunk_offset = 0;
        const file_size = file.size;
        const file_name = file.name;

        const socket = new WebSocket(socket_url);

        const progress_label_div = document.createElement("div");
        const progress_label_h3 = document.createElement("h3");
        const progress_label_span = document.createElement("span");

        progress_label_div.className = "md-2 flex justify-between items-center";

        progress_label_h3.className =
          "text-sm font-semibold text-gray-800 dark:text-white";
        progress_label_h3.innerHTML = file_name;

        progress_label_span.className = "text-sm text-gray-800 dark:text-white";

        progress_label_div.appendChild(progress_label_h3);
        progress_label_div.appendChild(progress_label_span);

        const progress_format = document.createElement("div");
        const progress_bar = document.createElement("div");

        progress_format.className =
          "flex w-full h-2 bg-gray-200 rounded-full overflow-hidden dark:bg-gray-700";

        progress_bar.className =
          "flex flex-col justify-center rounded-full overflow-hidden bg-green-500 text-xs text-white text-center whitespace-nowrap transition duration-500 dark:bg-blue-500";

        progress_bar.style.width = "0%";

        progress_format.appendChild(progress_bar);

        progress_group?.appendChild(progress_label_div);
        progress_group?.appendChild(progress_format);

        socket.onmessage = (event) => {
          let json_data = JSON.parse(event.data);

          if (json_data.cmd == "update" && json_data.detail != "error") {
            let progress_size = json_data.detail.split("len ")[1];
            let percent = Math.round((progress_size / file_size) * 100);
            progress_bar.style.width = percent + "%";
            progress_label_span.innerHTML = percent + "%";
          }

          if (json_data.cmd == "EOF") {
            if (json_data.detail == "success") {
              toast.push(file_name + " 파일 업로드에 성공했습니다.", {
                theme: {
                  "--toastBackground": "#34d399",
                  "--toastProgressBackground": "#059669",
                },
              });
            } else if (json_data.detail == "fail") {
              toast.push(file_name + " 파일 업로드에 실패했습니다.", {
                theme: {
                  "--toastBackground": "#f87171",
                  "--toastProgressBackground": "#ef4444",
                },
              });
            }
            setTimeout(() => {
              progress_bar.remove();
              progress_format.remove();

              progress_label_span.remove();
              progress_label_h3.remove();

              progress_label_div?.remove();
            }, 2000);
          }

          if (json_data.cmd == "error") {
            progress_bar.classList.add("bg-red-500");
            progress_label_span.innerHTML = "error";
            toast.push(file_name + "파일 업로드에 실패했습니다.", {
              theme: {
                "--toastBackground": "#f87171",
                "--toastProgressBackground": "#ef4444",
              },
            });
            socket.close();
          }
        };

        socket.onopen = () => {
          let s_data = {
            cmd: "start",
            detail: {
              name: file.name,
              size: file.size,
              chunk_size: chunk_size,
            },
          };

          socket.send(JSON.stringify(s_data));

          while (chunk_offset < file.size) {
            const chuck = file.slice(chunk_offset, chunk_offset + chunk_size);
            socket.send(chuck);
            // byte 단위로 전송
            chunk_offset += chunk_size;
          }

          const textEncoder = new TextEncoder();
          const EOF = textEncoder.encode("EOF");
          socket.send(EOF);
        };

        socket.onclose = () => {
          fileListArray.splice(i, 1);
          get_file_list();
        };

        socket.onerror = () => {
          progress_bar.classList.add("bg-red-500");
          progress_label_span.innerHTML = "error";
          updateError("파일 업로드에 실패했습니다.");
          socket.close();
        };
      }
      files = null;
      input.value = "";
    } catch (e: any) {
      updateError(e);
    }
  };

  const file_download = async (file_name: string, event: any) => {
    event.preventDefault();
    let params = { file_name: file_name };
    let _url = get(domain) + "/file/download?" + new URLSearchParams(params);
    let option = {
      method: "get",
      headers: {
        Authorization: "Bearer " + get(access_token),
      },
      body: null,
    };
    await fetch(_url, option).then(async (response) => {
      if (response.status == 200) {
        const blob = await response.blob();
        let fileUrl = window.URL.createObjectURL(blob);
        let a = document.createElement("a");

        a.style.display = "none";
        a.href = fileUrl;
        a.download = file_name;

        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(a.href);
        document.body.removeChild(a);
      } else {
        response.json().then((json) => {
          updateError(json.detail);
        });
      }
    });
  };

  const file_delete = (file_name: string) => {
    let _url = "/file/delete";
    let param = { file_name: file_name };

    FastAPI(
      "delete",
      _url,
      param,
      (json: any) => {
        toast.push(file_name + " 파일이 삭제되었습니다.", {
          theme: {
            "--toastBackground": "#34d399",
            "--toastProgressBackground": "#059669",
          },
        });
        file_count--;
        get_file_list();
      },
      (json_error: any) => {
        updateError(json_error.detail);
      }
    );
  };

  const handleSearch = () => {
    currentPage = 1;
    get_file_list();
  };

  let timeoutId = setTimeout(() => {}, 0);

  const handleInputChange = () => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(handleSearch, 1000);
  };

  const sort_select_name = () => {
    sort = sort == "asc" ? "desc" : "asc";
    sortBy = "name";
    get_file_list();
  };

  const sort_select_size = () => {
    sort = sort == "asc" ? "desc" : "asc";
    sortBy = "size";
    get_file_list();
  };
</script>

<main>
  <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 grid place-items-center">
    <div id="progress_group" class="w-1/2 md:w-2/3 hidden"></div>
    <br />
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
        accept="audio/*,video/*,image/*,text/*,application/*"
        multiple
        bind:files
        bind:this={input}
        on:change={() => {
          if (!file_upload_check(files)) {
            files = null;
            input.value = "";
          }
        }}
      />
      <button
        type="submit"
        class="px-5 py-2 relative rounded group overflow-hidden font-medium bg-white text-violet-700 inline-block"
        disabled={!files || files.length == 0}
        on:click={(event) => {
          file_upload(files, event);
        }}
      >
        <span
          class="absolute top-0 left-0 flex w-full h-0 mb-0 transition-all duration-200 ease-out transform translate-y-0 bg-violet-700 group-hover:h-full opacity-90"
        />
        <span class="relative group-hover:text-white">Submit</span>
      </button>
    </form>
    <br />
    <div class="whitespace-normal w-6/7 md:w-11/12">
      <table class="table-auto w-full">
        <thead>
          <tr
            class="border border-solid border-sky-50
        rounded-md py-0.3 px-2 grid grid-cols-5 gap-15
        bg-slate-400 dark:bg-slate-600"
          >
            <th
              class="col-span-4 md:col-span-3 text-ellipsis cursor-pointer text-left hover:bg-slate-500 w-104 hover:border-solid hover:border-sky-50 rounded-md py-0.3 px-2"
              on:click={sort_select_name}
            >
              파일 이름 <span>
                {#if sortBy == "name"}{#if sort == "asc"}▲{:else}▼{/if}{/if}
              </span>
            </th>
            <th
              class="text-right cursor-pointer hover:bg-slate-500 w-104 hover:border-solid hover:border-sky-50 rounded-md py-0.3 px-2"
              on:click={sort_select_size}
            >
              크기
              <span>
                {#if sortBy == "size"}{#if sort == "asc"}▲{:else}▼{/if}{/if}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          {#await file_list}
            <tr>리스트를 불러오는 중 입니다...</tr>
          {:then file_list}
            {#each file_list as info, key}
              <tr
                class="hover:bg-slate-600 w-104 hover:border-solid hover:border-sky-50 rounded-md py-0.3 px-2 grid grid-cols-5 gap-15"
              >
                <td
                  class="col-span-4 md:col-span-3 hover:text-white hover:underline ml-0"
                >
                  <button
                    class="w-full text-left truncate"
                    on:click={(event) => {
                      file_download(info["name"], event);
                    }}
                  >
                    {info["name"]}
                  </button>
                </td>
                <td class="text-right truncate">
                  <p>{info["size"]}</p>
                </td>
                <td
                  class=" hover:bg-slate-500 rounded-md py-0.3 px-2 mx-auto hidden md:block"
                >
                  <button
                    on:click={() => {
                      if (confirm(info["name"] + " 파일을 삭제하시겠습니까?")) {
                        file_delete(info["name"]);
                      }
                    }}
                  >
                    제거
                  </button>
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
            bind:value={search}
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
          disabled={prev_flag}
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
        <span class="dark:text-indigo-100 text-gray-800">
          {(currentPage - 1) * page_size + 1} - {(currentPage - 1) * page_size +
            file_list.length} of
          {file_count} files
        </span>
        <button
          class="rounded-md px-3.5 py-1 m-1 overflow-hidden relative group cursor-pointer border-2 font-medium border-indigo-600 text-indigo-600 bg-slate-300"
          on:click={sort_next}
          disabled={next_flag}
        >
          <span
            class="absolute w-64 h-0 transition-all duration-300 origin-center rotate-45 -translate-x-20 bg-indigo-600 top-1/2 group-hover:h-64 group-hover:-translate-y-32 ease"
            aria-disabled="true"
          />
          <span
            class="relative text-indigo-600 transition duration-300 group-hover:text-white ease"
          >
            Next
          </span>
        </button>
      </div>
    </div>
  </div>
</main>
