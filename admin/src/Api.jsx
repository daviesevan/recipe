import axios from "axios";

const baseURL = import.meta.env.VITE_BASE_URL;

const api = axios.create({
  baseURL,
});

const refreshapi = axios.create({
  baseURL,
});

// Request interceptor for API calls
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


// Request interceptor for refresh token
refreshapi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("refresh_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Function to handle employee signup
const signupEmployee = async (fullname, email, password) => {
  try {
    const response = await api.post("/admin/signup", {
      fullname,
      email,
      password
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || "An error occurred during signup");
    } else {
      throw error;
    }
  }
};

// Function to handle admin login
const loginAdmin = async (email, password) => {
  try {
    const response = await api.post("/admin/login", {
      email,
      password
    });
    const { access_token, refresh_token } = response.data;
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || "An error occurred during login");
    } else {
      throw error;
    }
  }
};

export { api, refreshapi, signupEmployee, loginAdmin };