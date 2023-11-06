<script lang="ts">
  export let error: any = {};
</script>

<div class="whitespace-normal">
  {#if typeof error.detail === "string"}
    <ul>
      <li>{error.detail}</li>
    </ul>
  {:else}
    <ul>
      {#each Object.keys(error.detail) as key}
        <li>{error.detail[key]}</li>
      {/each}
    </ul>
  {/if}
</div>
