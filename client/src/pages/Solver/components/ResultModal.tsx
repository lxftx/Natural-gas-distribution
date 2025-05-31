import type {ModalProps} from "./types.ts";

export const ResultModal = ({ data, onClose }: ModalProps) => {
  const isError = "error" in data;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">
              {isError ? "Ошибка расчета" : "Результаты расчета"}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          {isError ? (
            <div className="bg-red-100 border border-red-300 text-red-700 p-4 rounded">
              <p>{data.error}</p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-50 p-4 rounded">
                  <h3 className="font-semibold mb-2">Общие показатели</h3>
                  <p>
                    Статус: <span className="font-medium">{data.status}</span>
                  </p>
                  <p>
                    Целевая функция:{" "}
                    <span className="font-medium">
                      {data.objective.toFixed(2)}
                    </span>
                  </p>
                </div>

                <div className="bg-gray-50 p-4 rounded">
                  <h3 className="font-semibold mb-2">Суммарные значения</h3>
                  <p>
                    Расход кокса:{" "}
                    <span className="font-medium">
                      {data.total_coke_consumption.toFixed(2)} т/ч
                    </span>
                  </p>
                  <p>
                    Расход газа:{" "}
                    <span className="font-medium">
                      {data.total_gas_consumption.toFixed(2)} м³/ч
                    </span>
                  </p>
                  <p>
                    Производство чугуна:{" "}
                    <span className="font-medium">
                      {data.total_iron_production.toFixed(2)} т/ч
                    </span>
                  </p>
                </div>
              </div>

              <div className="bg-gray-50 p-4 rounded">
                <h3 className="font-semibold mb-2">
                  Распределение газа по печам
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                  {data.gas_distribution.map((value, index) => (
                    <div key={index} className="bg-white p-3 rounded shadow">
                      <p className="font-medium">Печь {index + 1}</p>
                      <p>Газ: {value.toFixed(2)} м³/ч</p>
                      <p>
                        Сера:{" "}
                        {data.sulfur_content[index]?.toFixed(2) ?? "N/A"}%
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          <div className="flex justify-end pt-4">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
