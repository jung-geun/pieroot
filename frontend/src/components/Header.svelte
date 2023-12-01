<script lang="ts">
  import { is_login } from "$stores/store";
  import { link, location } from "svelte-spa-router";
  let showMenu = false;

  function showMenuClick() {
    showMenu = !showMenu;
  }
</script>

<nav class="bg-gray-400 dark:bg-gray-800 rounded-t-lg">
  <div class="mx-auto px-4 md:px-6 lg:px-8">
    <div class="h-16 flex items-center justify-between">
      <a href="/" use:link class="flex-shrink-0 font-bold text-lg p-3.5">
        <p>PieRoot</p>
      </a>

      <!-- Mobile menu button -->
      <div class="m-2 flex">
        <button
          type="button"
          class="relative inline-flex items-center justify-center rounded-md bg-gray-800 p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800 md:hidden"
          on:click={showMenuClick}
        >
          <!-- Menu open: "hidden", Menu closed: "block" -->
          <svg
            class="h-6 w-6 {showMenu ? 'hidden' : 'block'}"
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
            class="h-6 w-6 {showMenu ? 'block' : 'hidden'}"
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

      <div class="items-baseline space-x-4 mx-auto hidden md:flex">
        <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
        <a
          href="/"
          use:link
          class="
              {$location === '/'
            ? 'bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium'
            : 'text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium'}"
          >Home
        </a>

        <a
          href="/portfolio"
          use:link
          class={$location === "/portfolio"
            ? "bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
            : "text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"}
          >Portfolio
        </a>

        <a
          href="/gallery"
          use:link
          class={$location === "/gallery"
            ? "bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
            : "text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"}
          >Gallery
        </a>

        {#if $is_login == false}
          <a
            href="/login"
            use:link
            class={$location === "/login"
              ? "bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
              : "text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"}
            >Login
          </a>
        {:else}
          <a
            href="/file"
            use:link
            class={$location === "/file"
              ? "bg-gray-600 dark:bg-gray-700 text-white dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"
              : "text-slate-50 dark:text-gray-300 hover:bg-gray-600 hover:text-white hover:dark:text-slate-50 rounded-md px-3 py-2 text-sm font-medium"}
            >File
          </a>

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

    <!-- Mobile menu, show/hide based on menu state. -->
    <div class="md:hidden" id="mobile-menu">
      <div
        class="space-y-1 px-2 pb-3 pt-2 sm:px-3 {showMenu
          ? 'visible'
          : 'hidden'}"
      >
        <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->

        <a
          href="/"
          use:link
          class={$location === "/"
            ? "bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
            : "text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"}
          >Home
        </a>

        <a
          href="/portfolio"
          use:link
          class={$location === "/portfolio"
            ? "bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
            : "text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"}
          >Portfolio
        </a>

        <a
          href="/gallery"
          use:link
          class={$location === "/gallery"
            ? "bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
            : "text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"}
          >Gallery
        </a>

        {#if $is_login == false}
          <a
            href="/login"
            use:link
            class={$location === "/login"
              ? "bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
              : "text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"}
            >Login
          </a>
        {:else}
          <a
            href="/file"
            use:link
            class={$location === "/file"
              ? "bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium"
              : "text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium"}
            >File
          </a>

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
  </div>
</nav>
<div class="bg-white rounded-b-lg shadow-2xl">
  <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
    <h1 class="text-3xl font-bold tracking-tight text-gray-900 px-3">
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
