// Usage: import fastapi from "$lib/api";
import { access_token, test_url } from "$stores/store";
import qs from "qs";
import { get } from "svelte/store";

const fastapi = async (
  operation: string, // get, post, put, delete
  url: string, // /api/xxx
  params: any, // { "name": "John", "age": 30 }
  success_callback: any, // (json) => { ... }
  failure_callback: any // (json) => { ... }
) => {
  let method = operation;
  let content_type = "application/json";
  let body = JSON.stringify(params);

  let _url = test_url + url;

  if (method === "get") {
    if (params && Object.keys(params).length > 0) {
      _url += "?" + new URLSearchParams(params);
    }
    body = null;
  }

  if (method === "delete") {
    if (params && Object.keys(params).length > 0) {
      _url += "?" + new URLSearchParams(params);
    }
    body = null;
  }

  if (method === "post"){
    body = params;
  }

  if (method === "patch"){
    if (params && Object.keys(params).length > 0) {
      _url += "?" + new URLSearchParams(params);
    }
    body = null;
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
    },
  };

  if (method === "file_upload") {
    options["method"] = "post";
    options["headers"] = {
      Authorization: "Bearer " + get(access_token),
    };
    body = params;
  }

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
        } else {
          if (failure_callback) {
            failure_callback(json);
          } else {
            alert(JSON.stringify(json));
          }
        }
      })
      .catch((error) => {
        alert(JSON.stringify(error));
      });
  });
};

export default fastapi;
