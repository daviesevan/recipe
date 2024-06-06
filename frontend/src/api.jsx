import axios from "axios";

const baseURL = import.meta.env.VITE_BASE_URL;

const api = axios.create({
  baseURL,
});
const refreshapi = axios.create({
  baseURL,
});

api.interceptors.request.use(
  (config) => {
    // Get access token from the localStorage
    const token = localStorage.getItem("access_token");
    // Add the access token to the request headers if it exists
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

refreshapi.interceptors.request.use(
  (config) => {
    // Get refresh token from the localStorage
    const token = localStorage.getItem("refresh_token");
    // Add the refresh token to the request header
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
export { refreshapi };
