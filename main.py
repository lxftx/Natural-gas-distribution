from ortools.linear_solver import pywraplp


def optimize_gas_distribution():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None

    # Цеховые параметры (из варианта 1)
    C_k = 1.8  # руб/кг
    C_pg = 0.6  # руб/м3
    V_pg_total = 120000  # м3/ч
    K_total = 520  # т/ч
    P_total = 1100  # т/ч
    C_p = 1

    N = 8  # Количество печей

    # Данные по печам
    V_pg_0 = [15000, 17000, 11000, 13000, 12000, 15000, 17000, 14000]
    V_pg_min = [10000] * N
    V_pg_max = [20000] * N
    K_0 = [64.25, 66.76, 56.08, 49.78, 62.92, 60.02, 81.68, 69.7]
    e = [0.59, 0.53, 0.85, 0.59, 0.75, 0.79, 0.87, 0.77]
    P_0 = [146.4, 136.4, 134.30, 122.3, 138.2, 138.8, 191.4, 151.6]
    S_0 = [0.015, 0.014, 0.013, 0.014, 0.017, 0.016, 0.013, 0.014]
    S_min = [0.000] * N
    S_max = [0.025] * N
    delta_P_pg = [-0.0007295, -0.0006695, 0.00, -0.00072373, -0.0007724, -0.0006872, -0.0007284, -0.0007305]
    delta_P_k = [-0.002970, -0.002970, -0.002928, -0.002897, -0.002970, -0.002970, -0.003316, -0.00356]
    delta_S_pg = [-0.0000034, -0.0000034, -0.0000035, -0.0000033, -0.0000034, -0.0000034, -0.0000034, -0.0000034]
    delta_S_k = [-0.0000030, -0.0000029, -0.0000032, -0.0000029, -0.0000031, -0.0000028, -0.0000030, -0.0000031]
    delta_S_p = [0] * N

    # Переменные
    V_pg = [solver.NumVar(V_pg_min[i], V_pg_max[i], f'V_pg_{i + 1}') for i in range(N)]

    # Целевая функция
    objective = solver.Objective()
    for i in range(N):
        coeff = 0.5 * (e[i] * C_k - C_pg) + 0.5 * C_p * (delta_P_pg[i] - e[i] * delta_P_k[i])
        objective.SetCoefficient(V_pg[i], coeff)
    objective.SetMaximization()

    # Ограничения

    # 1. По общему расходу ПГ
    constraint_gas = solver.Constraint(0, V_pg_total)
    for i in range(N):
        constraint_gas.SetCoefficient(V_pg[i], 1)

    # 2. По расходу кокса (в тоннах)
    constraint_coke = solver.Constraint(-solver.infinity(), K_total)
    for i in range(N):
        constraint_coke.SetCoefficient(V_pg[i], -0.001 * e[i])  # переводим кг в тонны

    # Свободный член для кокса
    sum_K_0 = sum(K_0)
    sum_V_pg_0_e = sum(V_pg_0[i] * e[i] * 0.001 for i in range(N))
    constraint_coke.SetUb(K_total - sum_K_0 + sum_V_pg_0_e)

    # 3. По производству чугуна
    constraint_iron = solver.Constraint(P_total, solver.infinity())
    for i in range(N):
        coeff = delta_P_pg[i] - e[i] * delta_P_k[i]
        constraint_iron.SetCoefficient(V_pg[i], coeff)

    # Свободный член для чугуна
    sum_P_0 = sum(P_0)
    sum_V_pg_0_coeff = sum(V_pg_0[i] * (delta_P_pg[i] - e[i] * delta_P_k[i]) for i in range(N))
    constraint_iron.SetLb(P_total - sum_P_0 + sum_V_pg_0_coeff)

    # 4. Ограничения по сере (упрощенный вариант)
    for i in range(N):
        coeff = (delta_S_pg[i]- e[i] * delta_S_k[i] + (delta_P_pg[i] - e[i] * delta_P_k[i]) * delta_S_p[i])
        if coeff != 0:
            lower = (S_min[i] - S_0[i]) / coeff + V_pg_0[i]
            upper = (S_max[i] - S_0[i]) / coeff + V_pg_0[i]
            V_pg[i].SetLb(max(float(V_pg_min[i]), min(lower, upper)))
            V_pg[i].SetUb(min(float(V_pg_max[i]), max(lower, upper)))

    # Решение
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        gas_values = [V_pg[i].solution_value() for i in range(N)]
        coke_total = sum(K_0[i] + 0.001 * (V_pg_0[i] - gas_values[i]) * e[i] for i in range(N))
        production_total = sum(
            (gas_values[i] - V_pg_0[i]) * delta_P_pg[i] -
            e[i] * (gas_values[i] - V_pg_0[i]) * delta_P_k[i] +
            P_0[i]
            for i in range(N)
        )
        sulfur = [
            S_0[i] + (gas_values[i] - V_pg_0[i]) * (delta_S_pg[i] - e[i] * delta_S_k[i])
            for i in range(N)
        ]

        print("✅ Оптимальное решение найдено!")
        print(f"Целевая функция: {objective.Value():.2f} руб/ч\n")
        print("Распределение ПГ (м3/ч):")
        for i in range(N):
            print(f"  Печь {i + 1}: {gas_values[i]:.2f} (было {V_pg_0[i]})")

        print(f"\nОбщий расход ПГ: {sum(gas_values):.2f} м3/ч (лимит: {V_pg_total})")
        print(f"Общий расход кокса: {coke_total:.2f} т/ч (лимит: {K_total})")
        print(f"Общее производство чугуна: {production_total:.2f} т/ч (требуется: {P_total})\n")
        print("Содержание серы (%):")
        for i in range(N):
            print(f"  Печь {i + 1}: {sulfur[i]:.6f} (допуск: {S_min[i]} - {S_max[i]})")
    else:
        print("❌ Оптимальное решение не найдено. Возможные причины:")
        print("- Несовместные ограничения")
        print("- Ошибка в коэффициентах (проверьте delta_P_pg и delta_P_k)")
        print("\nДля диагностики можно уменьшить P_total и проверить решение")


# Запуск
optimize_gas_distribution()