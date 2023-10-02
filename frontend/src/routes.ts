import Home from "./pages/Home.svelte";
import Portfolio from "./pages/Portfolio/+page.svelte";
import FileUpload from "./pages/File_Upload/+page.svelte";
import Upload from "./pages/File_Upload/+page.server.svelte";
import NotFound from "./pages/NotFound.svelte";

export default {
  "/": Home,
  "/portfolio": Portfolio,
  "/file_upload": FileUpload,
  "/file_upload/:files": Upload,
  "*": NotFound,
};
