import Home from "./pages/Home.svelte";
import Portfolio from "./pages/Portfolio/+page.svelte";
import File from "./pages/File/+page.svelte";
import Gallery from "./pages/Gallery/+page.svelte";
import Login from "./pages/Login/+page.svelte";
import Logout from "./pages/Login/+page.svelte";
import NotFound from "./pages/NotFound.svelte";

export default {
  "/": Home,
  "/portfolio": Portfolio,
  "/file": File,
  "/gallery": Gallery,
  "/login": Login,
  "/logout": Logout,
  "*": NotFound,
};
