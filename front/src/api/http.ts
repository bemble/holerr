import axios from "axios";

let baseURL = (window as any).base_path;
if (baseURL === "/") {
  baseURL = "";
}
baseURL += "/api";

const httpApi = axios.create({
  baseURL,
  headers: { Accept: "application/json" },
});

export default httpApi;
