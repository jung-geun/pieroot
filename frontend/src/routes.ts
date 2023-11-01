import Home from "./pages/Home.svelte";
import Portfolio from "./pages/Portfolio/+page.svelte";
import FileUpload from "./pages/File_Upload/+page.svelte";
import Login from "./pages/Login/+page.svelte";
import Logout from "./pages/Login/+page.svelte";
import NotFound from "./pages/NotFound.svelte";

export default {
  "/": Home,
  "/portfolio": Portfolio,
  "/file_upload": FileUpload,
  "/login": Login,
  "/logout": Logout,
  "*": NotFound,
};
