import Home from "./pages/Home.svelte";
import Portfolio from "./pages/Portfolio/+page.svelte";
import NotFound from "./pages/NotFound.svelte";

export default {
  "/": Home,
  "/portfolio": Portfolio,
  "*": NotFound,
};