import {type FormEvent, useState, useRef, useEffect} from 'react';
import API from '@/api';
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Loader2 } from "lucide-react"
import { ResultModal } from "../ResultModal.tsx";
import type { FurnaceData, ResultData, HistoryDataPost } from "../types.ts";

function Solver() {
  const [furnaceCount, setFurnaceCount] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ResultData | { error: string } | null>(null);
  const [normalized, setNormalized] = useState<FurnaceData | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const formRef = useRef<HTMLFormElement | null>(null);

  const [defaultData, setDefaultData] = useState<FurnaceData | null>(null);

  useEffect(() => {
    if (!defaultData) return;

    requestAnimationFrame(() => {
      if (!formRef.current) return;
      const form = formRef.current;

      const set = (name: string, value: number | string) => {
        const el = form.elements.namedItem(name) as HTMLInputElement | null;
        if (el) el.value = String(value);
      };

      // Примитивные
      set("C_k", defaultData.C_k);
      set("C_pg", defaultData.C_pg);
      set("V_pg_total", defaultData.V_pg_total);
      set("K_total", defaultData.K_total);
      set("P_total", defaultData.P_total);
      set("N", defaultData.N);

      // Массивы
      const setArray = (base: string, values: number[]) => {
        values.forEach((v, i) => set(`${base}_${i}`, v));
      };

      setArray("V_pg_0", defaultData.V_pg_0);
      setArray("V_pg_min", defaultData.V_pg_min);
      setArray("V_pg_max", defaultData.V_pg_max);
      setArray("K_0", defaultData.K_0);
      setArray("e", defaultData.e);
      setArray("P_0", defaultData.P_0);
      setArray("S_0", defaultData.S_0);
      setArray("S_min", defaultData.S_min);
      setArray("S_max", defaultData.S_max);
      setArray("delta_P_pg", defaultData.delta_P_pg);
      setArray("delta_P_k", defaultData.delta_P_k);
      setArray("delta_S_pg", defaultData.delta_S_pg);
      setArray("delta_S_k", defaultData.delta_S_k);
      setArray("delta_S_p", defaultData.delta_S_p);

      setDefaultData(null); // Сброс
    });
  }, [furnaceCount, defaultData]); // Ждём когда оба условия выполнены

  
  const handleFillDefaults = async () => {
  try {
      const response = await API.defaultInputValues();
      const data: FurnaceData = response.data;

      setFurnaceCount(data.N);
      setDefaultData(data); // Далее всё произойдёт в useEffect
    } catch (error) {
      console.error("Не удалось загрузить значения по умолчанию", error);
    }
  };

  const renderInputs = (name: string, label: string) => {
    return (
      <div className="space-y-2">
        <Label className="text-sm font-medium">{label}</Label>
        <div className="grid gap-2">
          {Array.from({ length: furnaceCount }, (_, i) => (
            <Input
              key={`${name}_${i}`}
              name={`${name}_${i}`}
              type="number"
              step="0.00000001"
              placeholder={`Печь ${i + 1}`}
              className="w-full"
              required
            />
          ))}
        </div>
      </div>
    )
  };

  const getNumberArray = (data: Record<string, any>, name: string): number[] => {
    return Array.from({ length: furnaceCount }, (_, i) => {
      const value = data[`${name}_${i}`]
      return value ? Number(value) : 0
    })
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const formData = new FormData(e.target as HTMLFormElement);
      const data = Object.fromEntries(formData);
      
      const normalizedData: FurnaceData = {
        C_k: Number(data.C_k),
        C_pg: Number(data.C_pg),
        V_pg_total: Number(data.V_pg_total),
        K_total: Number(data.K_total),
        P_total: Number(data.P_total),
        N: furnaceCount,
        V_pg_0: getNumberArray(data, "V_pg_0"),
        V_pg_min: getNumberArray(data, "V_pg_min"),
        V_pg_max: getNumberArray(data, "V_pg_max"),
        K_0: getNumberArray(data, "K_0"),
        e: getNumberArray(data, "e"),
        P_0: getNumberArray(data, "P_0"),
        S_0: getNumberArray(data, "S_0"),
        S_min: getNumberArray(data, "S_min"),
        S_max: getNumberArray(data, "S_max"),
        delta_P_pg: getNumberArray(data, "delta_P_pg"),
        delta_P_k: getNumberArray(data, "delta_P_k"),
        delta_S_pg: getNumberArray(data, "delta_S_pg"),
        delta_S_k: getNumberArray(data, "delta_S_k"),
        delta_S_p: getNumberArray(data, "delta_S_p"),
      }
      
      setNormalized(normalizedData);
      // Нормализация данных и отправка...
      const response = await API.calculate(normalizedData);
      setResult(response.data);

      setIsModalOpen(true);
    } catch (err: any) {
      setResult({ error: err.response?.data?.error || "Неизвестная ошибка" });
      setIsModalOpen(true);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (result && 'gas_distribution' in result && normalized) {
      const history: HistoryDataPost = {
        ...result,
        calculate: normalized
      };
      API.addHistory(history);
    }
  }, [result, normalized]);

  return (
    <div className="container mx-auto py-8">
    <form ref={formRef} onSubmit={handleSubmit} className="space-y-6">
        {/* Основные параметры */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Основные параметры</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="C_k">Стоимость кокса, руб/(кг кокса)</Label>
              <Input id="C_k" name="C_k" type="number" step="0.01" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="C_pg">Стоимость природного газа, руб/(м³ ПГ)</Label>
              <Input id="C_pg" name="C_pg" type="number" step="0.01" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="V_pg_total">Лимит расхода ПГ по цеху, м³/ч</Label>
              <Input id="V_pg_total" name="V_pg_total" type="number" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="K_total">Запасы кокса по цеху, т/ч</Label>
              <Input id="K_total" name="K_total" type="number" step="0.001" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="P_total">Требуемая производительность, т/ч</Label>
              <Input id="P_total" name="P_total" type="number" step="0.001" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="N">Количество печей</Label>
              <Input
                id="N"
                name="N"
                type="number"
                min="1"
                max="20"
                value={furnaceCount}
                onChange={(e) => setFurnaceCount(Math.max(1, Number(e.target.value) || 1))}
                required
              />
            </div>
          </CardContent>
        </Card>

        {/* Базовые параметры печей */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Базовые параметры печей</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {renderInputs("V_pg_0", "Базовый расход ПГ")}
            {renderInputs("V_pg_min", "Минимальный расход ПГ")}
            {renderInputs("V_pg_max", "Максимальный расход ПГ")}
            {renderInputs("K_0", "Базовый расход кокса")}
            {renderInputs("e", "Эквивалент замены кокса")}
            {renderInputs("P_0", "Базовая производительность")}
          </CardContent>
        </Card>

        {/* Параметры серы */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Параметры серы</CardTitle>
            <CardDescription>Параметры содержания серы в чугуне</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {renderInputs("S_0", "Базовое содержание серы")}
            {renderInputs("S_min", "Минимальное содержание серы")}
            {renderInputs("S_max", "Максимальное содержание серы")}
          </CardContent>
        </Card>

        {/* Коэффициенты влияния */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Коэффициенты влияния</CardTitle>
            <CardDescription>Коэффициенты влияния параметров на производство</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {renderInputs("delta_P_pg", "Влияние ПГ на производство")}
            {renderInputs("delta_P_k", "Влияние кокса на производство")}
            {renderInputs("delta_S_pg", "Влияние ПГ на серу")}
            {renderInputs("delta_S_k", "Влияние кокса на серу")}
            {renderInputs("delta_S_p", "Влияние производительности на серу")}
          </CardContent>
        </Card>

        <div className="flex flex-col sm:flex-row gap-4 mt-6">
            {/* Кнопка "Рассчитать" */}
            <Button
                type="submit"
                className="w-full text-lg py-6 bg-black text-white"
                disabled={isLoading}
            >
                {isLoading ? (
                <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Выполняется расчет...
                </>
                ) : (
                "Рассчитать"
                )}
            </Button>

            {/* Кнопка "Заполнить по умолчанию" */}
            <Button
                type="button"
                onClick={handleFillDefaults}
                className="w-full text-lg py-6 border border-gray-300 text-gray-800 hover:bg-gray-100"
                >
                Заполнить по умолчанию
            </Button>
        </div>
      </form>

      {isModalOpen && result && (
        <ResultModal 
          data={result}
          onClose={() => setIsModalOpen(false)}
        />
      )}
    </div>
  );
};

export default Solver