import { readonly, writable, readable } from "svelte/store";

const persist_storage = (key: any, initValue: any) => {
  const storedValueStr = localStorage.getItem(key);
  const store = writable(
    storedValueStr != null ? JSON.parse(storedValueStr) : initValue
  );
  store.subscribe((val) => {
    localStorage.setItem(key, JSON.stringify(val));
  });
  return store;
};

const isDev = process.env.NODE_ENV === "development";

export const domain = readonly(
  readable(isDev ? "https://127.0.0.1:8000" : window.location.origin)
);
export const access_token = persist_storage("access_token", "");
export const username = persist_storage("username", "");
export const is_login = persist_storage("is_login", false);
