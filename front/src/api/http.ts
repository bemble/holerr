import axios from "axios";

let baseURL = process.env.PUBLIC_URL;
if (baseURL === "/") {
  baseURL = "";
}
baseURL += "/api";

const httpApi = axios.create({
  baseURL
});

export default httpApi;
