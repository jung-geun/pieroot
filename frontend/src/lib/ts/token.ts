import FastAPI from "$lib/ts/api";
import { updateError } from "$src/components/Error.svelte";
import { access_token, is_login, username } from "$stores/store";
import { toast } from "@zerodevx/svelte-toast";
import { push } from "svelte-spa-router";

export const token_login = async (
  login_username: string,
  login_password: string
) => {
  FastAPI(
    "login",
    "/users/token",
    {
      username: login_username,
      password: login_password,
    },
    (json: any) => {
      access_token.set(json.access_token);
      username.set(json.username);
      is_login.set(true);
      push("/");
    },
    (json_error: any) => {
      toast.push("아이디 또는 비밀번호가 틀렸습니다.", {
        theme: {
          "--toastBackground": "#ff0000",
          "--toastProgressBackground": "#ff0000",
        },
      });
      push("/logout");
    }
  );
};

export const token_get = async () => {
  FastAPI(
    "get",
    "/users/token",
    {},
    (json: any) => {
      username.set(json.username);
    },
    (json_error: any) => {
      updateError(json_error.detail);
    }
  );
};

export const token_delete = async () => {
  access_token.set("");
  username.set("");
  is_login.set(false);
  FastAPI(
    "delete",
    "/users/token",
    {},
    () => {},
    () => {}
  );
  toast.push("로그아웃 되었습니다.", {
    theme: {
      "--toastBackground": "#0000ff",
      "--toastProgressBackground": "#0000ff",
    },
  });
  push("/login");
};

export const token_refresh = async () => {
  FastAPI(
    "put",
    "/users/token",
    {},
    async (json: any) => {
      access_token.set(json.access_token);
      username.set(json.username);
      is_login.set(true);
      // 현재 페이지 새로고침
      await location.reload();
    },
    (json_error: any) => {
      push("/logout");
    }
  );
};
