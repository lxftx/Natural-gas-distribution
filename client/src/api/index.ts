import axios from "axios";
import type { FurnaceData, HistoryDataPost } from "@/pages/Solver/components/types.ts";
import { AuthError } from "@/lib/types"

const apiUrl = import.meta.env.VITE_API_URL;

const API = axios.create({
  baseURL: apiUrl, // Базовый URL
  timeout: 5000, // Таймаут запроса
});

API.interceptors.request.use(config => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.withCredentials = true;  // Важно для отправки cookies
  return config;
});

export default {
    // Метод для расчета
    async calculate(data: FurnaceData) {
        return await API.post("gas/calculate/", data);
    },
    // Метод для входных данных
    async defaultInputValues() {
      return await API.get("gas/default/")
    },
    // Метод для получения истории
    async getHistory() {
      return await API.get("gas/history/")
    },
    // Метод для добавления истории
    async addHistory(data: HistoryDataPost) {
      return await API.post("gas/history/", data);
    },
    // Метод для удаления истории
    async deleteHistory(id: number) {
      return await API.delete(`gas/history/?id=${id}`)
    },
    async infoUser() {
      return await API.get("/user/info/")
    },
    async loginUser(email: string, password: string): Promise<string> {
      try {
        const response = await API.post("user/login/", { email, password })
        return response.data.access
      } catch (error: any) {
        const message = error.response?.data?.error || "Ошибка авторизации"
        throw new AuthError(message, error.response?.status)
      }
    },
    async registerUser(first_name: string, last_name: string, email: string, password: string): Promise<string> {
      try {
        const response = await API.post("user/register/", {email, first_name, last_name, password})

        return response.data.access
      } catch (error: any) {
        const message = error.response?.data?.error || "Ошибка регистрации"
        throw new AuthError(message, error.response?.status)
      }
    },
    async refreshAccessToken(): Promise<string> {
      try {
        const response = await API.post("user/token/refresh/")

        return response.data.access
      } catch (error: any) {
        const message = error.response?.data?.error || "Не удалось обновить токен"
        throw new AuthError(message, error.response?.status)
      }
    },
    async logout() {
      try {
        await API.post("user/logout/")
      } catch (error: any) {
        const message = error.response?.data?.error || "Ошибка выхода из системы"
        throw new AuthError(message, error.response?.status)
      }
    }
}