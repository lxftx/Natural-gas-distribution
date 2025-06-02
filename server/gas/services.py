from typing import Dict, List

from ortools.linear_solver import pywraplp

from server.settings import ERROR_LOGGER


class GasDistributionService:
    """
    Сервис для оптимизации распределения природного газа между доменными печами
    с использованием линейного программирования (Google OR-Tools).
    """

    C_p = 1.0  # Условно-постоянный коэффициент

    @classmethod
    def calculate_distribution(cls, data: Dict) -> Dict:
        """
        Основной метод расчета оптимального распределения.
        """
        try:
            # Инициализация решателя
            solver = cls._init_solver()
            N = data["N"]

            # Создание переменных решения
            V_pg = cls._create_decision_variables(solver, data, N)

            # Настройка целевой функции
            cls._setup_objective_function(solver, data, V_pg, N)

            # Добавление ограничений
            cls._add_constraints(solver, data, V_pg, N)

            # Решение задачи
            if not solver.Solve() == pywraplp.Solver.OPTIMAL:
                raise ValueError("Оптимальное решение не найдено. Проверьте ограничения.")

            # Формирование результатов
            return cls._prepare_results(data, V_pg, N, solver.Objective().Value())

        except Exception as e:
            ERROR_LOGGER.error(f"Ошибка расчета распределения: {str(e)}")
            raise ValueError(f"Ошибка при расчете: {str(e)}")

    @staticmethod
    def _init_solver():
        """Инициализация решателя SCIP"""
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            raise ValueError("Не удалось инициализировать решатель SCIP")
        return solver

    @staticmethod
    def _create_decision_variables(solver, data: Dict, N: int) -> List:
        """Создание переменных решения для каждой печи"""
        return [
            solver.NumVar(
                float(data["V_pg_min"][i]),
                float(data["V_pg_max"][i]),
                f"V_pg_{i}"
            ) for i in range(N)
        ]

    @classmethod
    def _setup_objective_function(cls, solver, data: Dict, V_pg: List, N: int):
        """Настройка целевой функции для максимизации эффективности"""
        objective = solver.Objective()
        for i in range(N):
            # Расчет коэффициента для целевой функции
            term1 = 0.5 * (data["e"][i] * data["C_k"] - data["C_pg"])
            term2 = 0.5 * cls.C_p * (data["delta_P_pg"][i] - data["e"][i] * data["delta_P_k"][i])
            objective.SetCoefficient(V_pg[i], term1 + term2)
        objective.SetMaximization()

    @classmethod
    def _add_constraints(cls, solver, data: Dict, V_pg: List, N: int):
        """Добавление всех ограничений в модель"""
        # 1. Ограничение по общему расходу ПГ
        cls._add_gas_constraint(solver, data, V_pg, N)

        # 2. Ограничение по расходу кокса
        cls._add_coke_constraint(solver, data, V_pg, N)

        # 3. Ограничение по производству чугуна
        cls._add_production_constraint(solver, data, V_pg, N)

        # 4. Ограничения по содержанию серы
        cls._add_sulfur_constraints(solver, data, V_pg, N)

    @staticmethod
    def _add_gas_constraint(solver, data: Dict, V_pg: List, N: int):
        """Ограничение по общему расходу природного газа"""
        constraint = solver.Constraint(0, float(data["V_pg_total"]))
        for i in range(N):
            constraint.SetCoefficient(V_pg[i], 1)

    @staticmethod
    def _add_coke_constraint(solver, data: Dict, V_pg: List, N: int):
        """Ограничение по общему расходу кокса"""
        constraint = solver.Constraint(-solver.infinity(), float(data["K_total"]))
        sum_K_0 = sum(data["K_0"])
        sum_V_pg_0_e = sum(data["V_pg_0"][i] * data["e"][i] * 0.001 for i in range(N))

        for i in range(N):
            constraint.SetCoefficient(V_pg[i], -0.001 * data["e"][i])

        constraint.SetUb(data["K_total"] - sum_K_0 + sum_V_pg_0_e)

    @staticmethod
    def _add_production_constraint(solver, data: Dict, V_pg: List, N: int):
        """Ограничение по минимальному производству чугуна"""
        constraint = solver.Constraint(float(data["P_total"]), solver.infinity())
        sum_P_0 = sum(data["P_0"])
        sum_V_pg_0_coeff = sum(
            data["V_pg_0"][i] * (data["delta_P_pg"][i] - data["e"][i] * data["delta_P_k"][i])
            for i in range(N)
        )

        for i in range(N):
            coeff = data["delta_P_pg"][i] - data["e"][i] * data["delta_P_k"][i]
            constraint.SetCoefficient(V_pg[i], coeff)

        constraint.SetLb(data["P_total"] - sum_P_0 + sum_V_pg_0_coeff)

    @staticmethod
    def _add_sulfur_constraints(solver, data: Dict, V_pg: List, N: int):
        """Ограничения по содержанию серы в чугуне"""
        for i in range(N):
            coeff = (
                    data["delta_S_pg"][i] - data["e"][i] * data["delta_S_k"][i] +
                    (data["delta_P_pg"][i] - data["e"][i] * data["delta_P_k"][i]) * data["delta_S_p"][i]
            )

            if abs(coeff) < 1e-10:  # Практически нулевой коэффициент
                continue

            # Вычисление границ
            delta_min = (data["S_min"][i] - data["S_0"][i]) / coeff
            delta_max = (data["S_max"][i] - data["S_0"][i]) / coeff

            # Установка границ с учетом базового значения
            lower = data["V_pg_0"][i] + min(delta_min, delta_max)
            upper = data["V_pg_0"][i] + max(delta_min, delta_max)

            # Обновление границ переменной
            V_pg[i].SetLb(max(float(data["V_pg_min"][i]), lower))
            V_pg[i].SetUb(min(float(data["V_pg_max"][i]), upper))

    @staticmethod
    def _prepare_results(data: Dict, V_pg: List, N: int, objective_value: float) -> Dict:
        """Подготовка итоговых результатов расчета"""
        gas_values = [V_pg[i].solution_value() for i in range(N)]

        return {
            "objective": round(objective_value, 2),
            "gas_distribution": [round(v, 2) for v in gas_values],
            "total_gas_consumption": round(sum(gas_values), 2),
            "total_coke_consumption": round(sum(
                data["K_0"][i] + 0.001 * (data["V_pg_0"][i] - gas_values[i]) * data["e"][i]
                for i in range(N)
            ), 2),
            "total_iron_production": round(sum(
                (gas_values[i] - data["V_pg_0"][i]) * data["delta_P_pg"][i] -
                data["e"][i] * (gas_values[i] - data["V_pg_0"][i]) * data["delta_P_k"][i] +
                data["P_0"][i]
                for i in range(N)
            ), 2),
            "sulfur_content": [
                round(data["S_0"][i] + (gas_values[i] - data["V_pg_0"][i]) *
                      (data["delta_S_pg"][i] - data["e"][i] * data["delta_S_k"][i]), 6)
                for i in range(N)
            ],
            "status": "OPTIMAL"
        }

class MainParameters:
    """
    Класс для получения основных параметров.
    """

    @staticmethod
    def values() -> Dict[str, float]:
        return dict(
            C_k=1.8,  # руб/кг
            C_pg=0.6,  # руб/м3
            V_pg_total=120000,  # м3/ч
            K_total=520,  # т/ч
            P_total=1100,  # т/ч
            C_p=1
        )
    
class BasicFurnaceParameters:
    """
    Класс для получения базовых параметров печей.
    """

    @staticmethod
    def values(N: int) -> Dict[str, List[float]]:
        return dict(
            V_pg_0=[15000, 17000, 11000, 13000, 12000, 15000, 17000, 14000],
            V_pg_min=[10000] * N,
            V_pg_max=[20000] * N,
            K_0=[64.25, 66.76, 56.08, 49.78, 62.92, 60.02, 81.68, 69.7],
            e=[0.59, 0.53, 0.85, 0.59, 0.75, 0.79, 0.87, 0.77],
            P_0=[146.4, 136.4, 134.30, 122.3, 138.2, 138.8, 191.4, 151.6]
        )

class SulfurParameters:
    """
    Класс для получения параметров серы.
    """

    @staticmethod
    def values(N: int) -> Dict[str, List[float]]:
        return dict(
            S_0=[0.015, 0.014, 0.013, 0.014, 0.017, 0.016, 0.013, 0.014],
            S_min=[0.000] * N,
            S_max=[0.025] * N
        )
    
class InfluenceCoefficients:
    """
    Класс для получения коэффициентов влияния.
    """

    @staticmethod
    def values(N: int) -> Dict[str, List[float]]:
        return dict(
            delta_P_pg=[-0.0007295, -0.0006695, 0.00, -0.00072373, -0.0007724, -0.0006872, -0.0007284, -0.0007305],
            delta_P_k=[-0.002970, -0.002970, -0.002928, -0.002897, -0.002970, -0.002970, -0.003316, -0.00356],
            delta_S_pg=[-0.0000034, -0.0000034, -0.0000035, -0.0000033, -0.0000034, -0.0000034, -0.0000034, -0.0000034],
            delta_S_k=[-0.0000030, -0.0000029, -0.0000032, -0.0000029, -0.0000031, -0.0000028, -0.0000030, -0.0000031],
            delta_S_p=[0] * N
        )

class DefaultInputValues:
    """
    Сервис для получения заготовленных входных данных
    """

    N = 8

    @classmethod
    def get_default_values(cls):
        return dict(
            N=cls.N,
            **MainParameters.values(),
            **BasicFurnaceParameters.values(cls.N),
            **SulfurParameters.values(cls.N),
            **InfluenceCoefficients.values(cls.N)
        )