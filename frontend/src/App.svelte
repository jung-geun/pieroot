<script lang="ts">
  import Router from "svelte-spa-router";
  import Head from "./components/Head.svelte";
  import Header from "./components/Header.svelte";
  import routes from "./routes";
  import Footer from "./components/Footer.svelte";
</script>

<Head />

<Header />

<Router {routes} />

<Footer />
