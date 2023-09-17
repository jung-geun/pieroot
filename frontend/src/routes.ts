import Home from "./pages/Home.svelte";
import Portfolio from "./pages/portfolio.svelte";
import NotFound from "./pages/NotFound.svelte";

export default {
  "/": Home,
  "/portfolio": Portfolio,
  "*": NotFound,
};