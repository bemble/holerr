import axios from "axios";
import store from "../store";

let baseURL = (window as any).base_path;
if (baseURL === "/") {
  baseURL = "";
}
baseURL += "/api";

const httpApi = axios.create({
  baseURL,
  headers: { Accept: "application/json" },
});

httpApi.interceptors.request.use(
  (config) => {
    const apiKey = store.getState().appConfig.apiKey;
    if (apiKey && apiKey.length && !apiKey.startsWith("%holerr-api-key-")) {
      config.headers = config.headers || {};
      config.headers["X-Api-Key"] = apiKey;
    }
    return config;
  },
  (error) => error
);

export default httpApi;
