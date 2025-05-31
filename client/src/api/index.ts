import axios from "axios";
import type {FurnaceData} from "@/pages/Solver/components/types.ts";

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Базовый URL
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
    }
}