<script lang="ts">
  import { updateError } from "$components/Error.svelte";
  import { token_delete, token_login } from "$lib/ts/token";
  import { onMount } from "svelte";
  import { location } from "svelte-spa-router";

  let login_username = "";
  let login_password = "";

  onMount(() => {
    if ($location == "/logout") {
      token_delete();
    }
    let username_input = document.getElementById("username_input");
    if (username_input) username_input.focus();
    else document;
  });

  function login_submit(event: any) {
    event.preventDefault();
    if (login_username == "" || login_password == "") {
      updateError("아이디 또는 비밀번호를 입력해주세요.");
      if (login_username == "") {
        let username_input = document.getElementById("username_input");
        if (username_input) username_input.focus();
      } else {
        let password_input = document.getElementById("password_input");
        if (password_input) password_input.focus();
      }
      return;
    }
    token_login(login_username, login_password);
  }
</script>

<main>
  <div class="mx-auto max-w-7xl py-4 sm:px-6 lg:px-8 whitespace-normal">
    <div class="flex flex-col items-center justify-center dark">
      <div
        class="w-full max-w-md bg-gray-300 dark:bg-gray-800 rounded-lg shadow-md p-6"
      >
        <h2 class="text-2xl font-bold dark:text-gray-200 mb-4">Login</h2>
        <!-- <Error {error} /> -->
        <br />
        <form class="flex flex-col" on:submit={login_submit}>
          <input
            placeholder="Email address"
            class="bg-gray-100 text-gray-700 border-0 rounded-md p-2 mb-4 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150"
            type="email"
            id="username_input"
            name="email"
            autocomplete="email"
            bind:value={login_username}
            minlength="8"
            maxlength="50"
            required
          />
          <input
            placeholder="Password"
            class="bg-gray-100 text-gray-700 border-0 rounded-md p-2 mb-4 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150"
            type="password"
            id="password_input"
            name="password"
            bind:value={login_password}
            minlength="8"
            maxlength="20"
            required
          />
          <button
            class="bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-bold py-2 px-4 rounded-md mt-4 hover:bg-indigo-600 hover:to-blue-600 transition ease-in-out duration-150"
            type="submit">Login</button
          >
        </form>
      </div>
    </div>
  </div>
</main>
