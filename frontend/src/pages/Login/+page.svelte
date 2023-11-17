<script lang="ts">
  import Error from "$components/Error.svelte";
  import fastapi from "$lib/ts/api";
  import { access_token, is_login, username } from "$stores/store";
  import { push } from "svelte-spa-router";

  let login_username = "";
  let login_password = "";
  let error = { detail: "" };

  function post_user(event: any) {
    event.preventDefault();
    if (login_username == "" || login_password == "") {
      error.detail = "아이디 또는 비밀번호를 입력해주세요.";
      if (login_username == "") {
        document.getElementById("username_input").focus();
      } else {
        document.getElementById("password_input").focus();
      }
      return;
    }
    let url = "/users/token";
    let params = {
      username: login_username,
      password: login_password,
    };
    fastapi(
      "login",
      url,
      params,
      (json: any) => {
        access_token.set(json.access_token);
        username.set(json.username);
        is_login.set(true);
        push("/");
      },
      (json_error: any) => {
        error = json_error;
      }
    );
  }
</script>

<main>
  <div class="mx-auto max-w-7xl py-4 sm:px-6 lg:px-8 whitespace-normal">
    <div class="flex flex-col items-center justify-center dark">
      <div
        class="w-full max-w-md bg-gray-300 dark:bg-gray-800 rounded-lg shadow-md p-6"
      >
        <h2 class="text-2xl font-bold dark:text-gray-200 mb-4">Login</h2>
        <Error {error} />
        <br />
        <form class="flex flex-col" method="post">
          <input
            placeholder="Email address"
            class="bg-gray-100 text-gray-700 border-0 rounded-md p-2 mb-4 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150"
            type="email"
            id="username_input"
            bind:value={login_username}
            required
            minlength="8"
            maxlength="50"
          />
          <input
            placeholder="Password"
            class="bg-gray-100 text-gray-700 border-0 rounded-md p-2 mb-4 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150"
            type="password"
            id="password_input"
            bind:value={login_password}
            required
            minlength="8"
            maxlength="20"
          />
          <button
            class="bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-bold py-2 px-4 rounded-md mt-4 hover:bg-indigo-600 hover:to-blue-600 transition ease-in-out duration-150"
            type="submit"
            on:click={post_user}>Login</button
          >
        </form>
      </div>
    </div>
  </div>
</main>
