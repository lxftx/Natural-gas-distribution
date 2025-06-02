import axios from "axios";
import type { FurnaceData, HistoryDataPost } from "@/pages/Solver/components/types.ts";

const apiUrl = import.meta.env.VITE_API_URL;

const API = axios.create({
  baseURL: apiUrl, // Базовый URL
  timeout: 5000, // Таймаут запроса
});

export default {
    // Метод для расчета
    calculate(data: FurnaceData) {
        return API.post("calculate/", data);
    },
    // Метод для входных данных
    defaultInputValues() {
      return API.get("default/")
    },
    // Метод для получения истории
    getHistory() {
      return API.get("history/")
    },
    // Метод для добавления истории
    addHistory(data: HistoryDataPost) {
      return API.post("history/", data);
    },
    // Метод для удаления истории
    deleteHistory(id: number) {
      return API.delete(`history/${id}/`)
    }
}