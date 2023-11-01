<script lang="ts">
  import { access_token, is_login, username } from "$stores/store";
  import { link, location, push } from "svelte-spa-router";
  let showMenu = true;

  function showMenuClick() {
    showMenu = !showMenu;
  }
  $: if ($location == "/file_upload") {
    if ($is_login == false || $access_token == "" || $username == "") {
      is_login.set(false);
      access_token.set("");
      username.set("");
      push("/login");
    }
  }
  $: if ($location == "/logout") {
    if ($is_login == false) {
      push("/login");
    } else {
      access_token.set("");
      username.set("");
      is_login.set(false);
      push("/login");
    }
  }
</script>

<nav class="bg-gray-400 dark:bg-gray-800 rounded-t-lg">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="flex h-16 items-center justify-between">
      <div class="flex items-center">
        <div class="flex-shrink-0 font-bold text-lg">
          <a href="/" use:link>
            <p>PieRoot</p>
          </a>
        </div>
        <div class="hidden md:block">
          <div class="ml-10 flex items-baseline space-x-4">
            <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
            {#if $location === "/"}
              <a
                href="/"
                use:link
                class="bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
                >Home</a
              >
            {:else}
              <a
                href="/"
                use:link
                class="text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
                >Home</a
              >
            {/if}

            {#if $location === "/portfolio"}
              <a
                href="/portfolio"
                use:link
                class="bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
                >Portfolio</a
              >
            {:else}
              <a
                href="/portfolio"
                use:link
                class="text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
                >Portfolio</a
              >
            {/if}

            {#if $is_login == false}
              {#if $location === "/login"}
                <a
                  href="/login"
                  use:link
                  class="bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
                  >Login</a
                >
              {:else}
                <a
                  href="/login"
                  use:link
                  class="text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
                  >Login</a
                >
              {/if}
            {/if}

            {#if $is_login}
              {#if $location == "/file_upload"}
                <a
                  href="/file_upload"
                  use:link
                  class="bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
                  >File Upload</a
                >
              {:else}
                <a
                  href="/file_upload"
                  use:link
                  class="text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
                >
                  File Upload
                </a>
              {/if}

              <a
                href="/logout"
                use:link
                class="text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
              >
                Logout
              </a>
            {/if}
          </div>
        </div>
      </div>

      <div class="mr-2 flex md:hidden">
        <!-- Mobile menu button -->
        <button
          type="button"
          class="relative inline-flex items-center justify-center rounded-md bg-gray-800 p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
          on:click={showMenuClick}
        >
          <span class="absolute -inset-0.5" />
          <span class="sr-only">Open main menu</span>
          <!-- Menu open: "hidden", Menu closed: "block" -->
          <svg
            class="block h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
            />
          </svg>
          <!-- Menu open: "block", Menu closed: "hidden" -->
          <svg
            class="hidden h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Mobile menu, show/hide based on menu state. -->
  <div class="md:hidden" id="mobile-menu">
    <div
      class="space-y-1 px-2 pb-3 pt-2 sm:px-3 {showMenu ? 'visible' : 'hidden'}"
    >
      <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
      {#if $location === "/"}
        <a
          href="/"
          use:link
          class="bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
          >Home</a
        >
      {:else}
        <a
          href="/"
          use:link
          class="text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"
          >Home</a
        >
      {/if}

      {#if $location === "/portfolio"}
        <a
          href="/portfolio"
          use:link
          class="bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
          >Portfolio</a
        >
      {:else}
        <a
          href="/portfolio"
          use:link
          class="text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"
          >Portfolio</a
        >
      {/if}

      {#if $is_login == false}
        {#if $location === "/login"}
          <a
            href="/login"
            use:link
            class="bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
            >Login</a
          >
        {:else}
          <a
            href="/login"
            use:link
            class="text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"
            >Login</a
          >
        {/if}
      {/if}

      {#if $is_login}
        {#if $location == "/file_upload"}
          <a
            href="/file_upload"
            use:link
            class="bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
            >File Upload</a
          >
        {:else}
          <a
            href="/file_upload"
            use:link
            class="text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"
          >
            File Upload
          </a>
        {/if}
        <a
          href="/logout"
          use:link
          class="text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"
        >
          Logout
        </a>
      {/if}
    </div>
  </div>
</nav>
<div class="bg-white rounded-b-lg shadow-2xl">
  <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
    <h1 class="text-3xl font-bold tracking-tight text-gray-900">
      {#if $location === "/"}
        Home
      {:else}
        {$location
          .replace(/\b[a-z]/g, (char) => char.toUpperCase())
          .split("/")
          .join(" ")}
      {/if}
    </h1>
  </div>
</div>
