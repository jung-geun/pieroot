import Home from "./pages/Home.svelte";
import NotFound from "./pages/NotFound.svelte";
import { wrap } from "svelte-spa-router/wrap";

export default {
  "/": Home,
  "/portfolio": wrap({
    asyncComponent: () => import("./pages/Portfolio/+page.svelte"),
  }),
  "/file": wrap({
    asyncComponent: () => import("./pages/File/+page.svelte"),
  }),
  "/gallery": wrap({
    asyncComponent: () => import("./pages/Gallery/+page.svelte"),
  }),
  "/login": wrap({
    asyncComponent: () => import("./pages/Login/+page.svelte"),
  }),
  "/logout": wrap({
    asyncComponent: () => import("./pages/Login/+page.svelte"),
  }),
  "*": NotFound,
};
