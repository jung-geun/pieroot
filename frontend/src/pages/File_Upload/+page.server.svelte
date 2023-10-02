<script context="module">
  import { writable } from "svelte/store";

  export let files = writable([]);

  export const getHello = async () => {
    const apiURL = "/api/hello";
    const res = await fetch(apiURL);
    let response = await res.json();

    if (res.ok) {
      console.log("response", response);
    } else {
      console.log("error", response);
    }
  };
</script>
