// Usage: import fastapi from "$lib/api";
import { access_token, domain } from "$stores/store";
import qs from "qs";
import { get } from "svelte/store";

const FastAPI = async (
  operation: string, // get, post, put, delete
  url: string, // /api/xxx
  params: any, // { "name": "John", "age": 30 }
  success_callback: Function, // (json) => { ... }
  failure_callback: Function // (json) => { ... }
) => {
  let method = operation;
  let content_type: string | null = "application/json";
  let body: string | null = JSON.stringify(params);

  let _url = get(domain) + url;

  if (operation === "get") {
    if (params && Object.keys(params).length > 0) {
      _url += "?" + new URLSearchParams(params);
    }
    body = null;
  } else if (operation === "delete") {
    if (params && Object.keys(params).length > 0) {
      _url += "?" + new URLSearchParams(params);
    }
    body = null;
  } else if (operation === "put") {
    if (params && Object.keys(params).length > 0) {
      _url += "?" + new URLSearchParams(params);
    }
    body = null;
  } else if (operation === "post") {
    content_type = "application/json";
    body = JSON.stringify(params);
  }

  if (operation === "login") {
    method = "post";
    content_type = "application/x-www-form-urlencoded";
    body = qs.stringify(params);
  }

  let options = {
    method: method,
    headers: {
      "Content-Type": content_type,
      Authorization: "Bearer " + get(access_token),
    } as any,
    body: body,
  };

  if (method !== "get" && method !== "delete") {
    options["body"] = body;
  }

  await fetch(_url, options).then((response) => {
    response
      .json()
      .then((json) => {
        if (response.status >= 200 && response.status < 300) {
          // 200 ~ 299
          if (success_callback) {
            success_callback(json);
          }
        }
        // 400 ~ 499
        else {
          if (failure_callback) {
            failure_callback(json);
          } else {
            alert(JSON.stringify(json));
          }
        }
      })
      .catch((error) => {
        if (failure_callback) {
          failure_callback(error);
        } else {
          alert(JSON.stringify(error));
        }
      });
  });
};

export default FastAPI;
