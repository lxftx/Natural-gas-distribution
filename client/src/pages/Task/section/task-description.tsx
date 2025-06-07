"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Info, Target, Settings, Calculator } from "lucide-react"

function TaskDescription() {
  return (
    <div className="space-y-6">
      {/* Заголовок */}
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-2xl flex items-center justify-center gap-2">
            <Target className="h-6 w-6 text-blue-600" />
            Задача оптимизации доменного производства
          </CardTitle>
        </CardHeader>
      </Card>

      {/* Описание проблемы */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Info className="h-5 w-5 text-blue-600" />
            Постановка задачи
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-gray-700 leading-relaxed">
            В состав доменного цеха входит <strong>N печей</strong>, на каждой из которых осуществляется инжектирование
            природного газа (ПГ) с расходами V<sub>i</sub>
            <sup>пг</sup> (i = 1, …, N), м³/ч.
          </p>

          <p className="text-gray-700 leading-relaxed">
            Эффективность инжектируемого топлива оценивается <strong>эквивалентом замены кокса</strong> e<sub>i</sub>{" "}
            (кг/м³), физический смысл которого – это количество кокса, сэкономленного на i-й печи при вдувании 1 м³
            природного газа.
          </p>

          <Alert>
            <Target className="h-4 w-4" />
            <AlertDescription>
              <strong>Цель:</strong> Распределить подачу природного газа между печами доменного цеха таким образом,
              чтобы при существующих ограничениях была достигнута максимальная эффективность его использования в целом
              по цеху.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Исходные данные */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5 text-green-600" />
            Исходные данные
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <h4 className="font-semibold text-gray-800">Экономические параметры:</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Badge variant="outline">
                    С<sub>к</sub>
                  </Badge>{" "}
                  Стоимость кокса, руб/кг
                </li>
                <li>
                  <Badge variant="outline">
                    С<sub>пг</sub>
                  </Badge>{" "}
                  Стоимость природного газа, руб/м³
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-gray-800">Ограничения цеха:</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Badge variant="outline">
                    V<sub>пг</sub>
                  </Badge>{" "}
                  Лимит расхода ПГ по цеху, м³/ч
                </li>
                <li>
                  <Badge variant="outline">K</Badge> Запасы кокса по цеху, т/ч
                </li>
                <li>
                  <Badge variant="outline">П</Badge> Требуемая производительность по чугуну, т/ч
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-gray-800">Параметры печей:</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Badge variant="outline">
                    V<sub>i</sub>
                    <sup>пг min/max</sup>
                  </Badge>{" "}
                  Пределы расхода ПГ на печь
                </li>
                <li>
                  <Badge variant="outline">
                    e<sub>i</sub>
                  </Badge>{" "}
                  Эквивалент замены кокса, кг/м³
                </li>
                <li>
                  <Badge variant="outline">
                    П<sub>i</sub>
                  </Badge>{" "}
                  Производительность печи, т/ч
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-gray-800">Качественные показатели:</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Badge variant="outline">
                    [S]<sub>i min/max</sub>
                  </Badge>{" "}
                  Пределы содержания серы, %
                </li>
                <li>
                  <Badge variant="outline">δS/δПГ</Badge> Влияние ПГ на серу
                </li>
                <li>
                  <Badge variant="outline">δS/δК</Badge> Влияние кокса на серу
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Математическая модель */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calculator className="h-5 w-5 text-purple-600" />
            Математическая модель
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Целевая функция */}
          <div>
            <h4 className="font-semibold text-gray-800 mb-3">Целевая функция (максимизация эффективности):</h4>
            <div className="bg-gray-50 p-4 rounded-lg border">
              <div className="text-center text-lg font-mono">
                Э = Σ(i=1 to N) [e<sub>i</sub> × С<sub>к</sub> - С<sub>пг</sub> + С<sub>п</sub> × (δП/δПГ<sub>i</sub> -
                e<sub>i</sub> × δП/δК<sub>i</sub>)] × V<sub>i</sub>
                <sup>пг</sup>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                где С<sub>п</sub> = 1 руб/т чуг (условно постоянный коэффициент)
              </p>
            </div>
          </div>

          <Separator />

          {/* Ограничения */}
          <div className="space-y-4">
            <h4 className="font-semibold text-gray-800">Система ограничений:</h4>

            <div className="grid gap-4">
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <h5 className="font-medium text-blue-800 mb-2">1. По расходу природного газа в цехе:</h5>
                <div className="font-mono text-sm">
                  Σ(i=1 to N) V<sub>i</sub>
                  <sup>пг</sup> ≤ V<sub>пг</sub>
                </div>
              </div>

              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <h5 className="font-medium text-green-800 mb-2">2. По расходу кокса в цехе:</h5>
                <div className="font-mono text-sm">
                  Σ(i=1 to N) [K<sub>i</sub>
                  <sup>0</sup> - e<sub>i</sub> × (V<sub>i</sub>
                  <sup>пг</sup> - V<sub>i</sub>
                  <sup>пг0</sup>)] ≤ K
                </div>
              </div>

              <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                <h5 className="font-medium text-yellow-800 mb-2">3. По производству чугуна в цехе:</h5>
                <div className="font-mono text-sm">
                  Σ(i=1 to N) [П<sub>i</sub>
                  <sup>0</sup> + δП/δПГ<sub>i</sub> × (V<sub>i</sub>
                  <sup>пг</sup> - V<sub>i</sub>
                  <sup>пг0</sup>) + δП/δК<sub>i</sub> × (K<sub>i</sub> - K<sub>i</sub>
                  <sup>0</sup>)] ≥ П
                </div>
              </div>

              <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
                <h5 className="font-medium text-orange-800 mb-2">4. По расходу ПГ на каждую печь:</h5>
                <div className="font-mono text-sm">
                  V<sub>i</sub>
                  <sup>пг min</sup> ≤ V<sub>i</sub>
                  <sup>пг</sup> ≤ V<sub>i</sub>
                  <sup>пг max</sup>
                </div>
              </div>

              <div className="bg-red-50 p-4 rounded-lg border border-red-200">
                <h5 className="font-medium text-red-800 mb-2">5. По содержанию серы в чугуне:</h5>
                <div className="font-mono text-sm">
                  [S]<sub>i</sub>
                  <sup>min</sup> ≤ [S]<sub>i</sub>
                  <sup>0</sup> + δS/δПГ<sub>i</sub> × ΔV<sub>i</sub>
                  <sup>пг</sup> + δS/δК<sub>i</sub> × ΔK<sub>i</sub> + δS/δП<sub>i</sub> × ΔП<sub>i</sub> ≤ [S]
                  <sub>i</sub>
                  <sup>max</sup>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Метод решения */}
      <Card>
        <CardHeader>
          <CardTitle>Метод решения</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-gray-700">
            Данная задача представляет собой <strong>задачу линейного программирования</strong> с целевой функцией
            максимизации и системой линейных ограничений.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h5 className="font-semibold text-blue-800 mb-2">Особенности задачи:</h5>
              <ul className="text-sm space-y-1">
                <li>• Многомерная оптимизация</li>
                <li>• Линейные ограничения</li>
                <li>• Экономическая целевая функция</li>
                <li>• Технологические ограничения</li>
              </ul>
            </div>

            <div className="bg-green-50 p-4 rounded-lg">
              <h5 className="font-semibold text-green-800 mb-2">Методы решения:</h5>
              <ul className="text-sm space-y-1">
                <li>• Симплекс-метод</li>
                <li>• Метод внутренней точки</li>
                <li>• Двойственный симплекс-метод</li>
                <li>• Численные методы оптимизации</li>
              </ul>
            </div>
          </div>

          <Alert>
            <Calculator className="h-4 w-4" />
            <AlertDescription>
              Калькулятор решает данную задачу с использованием численных методов оптимизации, учитывая все
              представленные ограничения для получения оптимального распределения природного газа между печами.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    </div>
  )
}

export default TaskDescription