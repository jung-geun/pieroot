<script context="module" lang="ts">
  import { token_refresh } from "$src/lib/ts/token";
  import { toast } from "@zerodevx/svelte-toast";

  export const updateError = (detail: string) => {
    if (detail == "Unauthorized") {
      token_refresh();
    } else if (detail != "") {
      toast.push(detail, {
        theme: {
          "--toastBackground": "#ff0000",
          "--toastProgressBackground": "#ff0000",
        },
      });
      setTimeout(() => {
        updateError("");
      }, 1000);
    }
  };
</script>
