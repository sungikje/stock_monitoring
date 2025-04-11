import axios from "axios";

const api = axios.create({
  baseURL: "https://stock-monitoring.com", // 공통 prefix
  withCredentials: true, // 필요 시 쿠키 등 포함
});

// 요청 인터셉터
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
