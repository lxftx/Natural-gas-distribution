from rest_framework import serializers


class CalculateSerializer(serializers.Serializer):
    """
    Сериализатор для расчета оптимального распределения природного газа между доменными печами.
    Валидирует входные данные и проверяет согласованность размеров массивов.
    """

    # Основные параметры цеха
    C_k = serializers.FloatField(
        min_value=0,
        help_text="Стоимость кокса, руб/(кг кокса)"
    )
    C_pg = serializers.FloatField(
        min_value=0,
        help_text="Стоимость природного газа, руб/(м3 ПГ)"
    )
    V_pg_total = serializers.FloatField(
        min_value=0,
        help_text="Лимит расхода природного газа по цеху, м3/ч"
    )
    K_total = serializers.FloatField(
        min_value=0,
        help_text="Запасы кокса по цеху, т/ч"
    )
    P_total = serializers.FloatField(
        min_value=0,
        help_text="Требуемая производительность по чугуну, т/ч"
    )
    N = serializers.IntegerField(
        min_value=1,
        max_value=20,
        help_text="Количество печей (1-20)"
    )

    # Параметры по печам (все списки должны иметь длину N)
    V_pg_0 = serializers.ListField(
        child=serializers.FloatField(min_value=0),
        help_text="Базовый расход ПГ по печам, м3/ч"
    )
    V_pg_min = serializers.ListField(
        child=serializers.FloatField(min_value=0),
        help_text="Минимальный расход ПГ по печам, м3/ч"
    )
    V_pg_max = serializers.ListField(
        child=serializers.FloatField(min_value=0),
        help_text="Максимальный расход ПГ по печам, м3/ч"
    )
    K_0 = serializers.ListField(
        child=serializers.FloatField(min_value=0),
        help_text="Базовый расход кокса по печам, т/ч"
    )
    e = serializers.ListField(
        child=serializers.FloatField(min_value=0),
        help_text="Эквивалент замены кокса, кг/(м3 ПГ)"
    )
    P_0 = serializers.ListField(
        child=serializers.FloatField(min_value=0),
        help_text="Базовая производительность по печам, т/ч"
    )
    S_0 = serializers.ListField(
        child=serializers.FloatField(min_value=0, max_value=1),
        help_text="Базовое содержание серы, %"
    )
    S_min = serializers.ListField(
        child=serializers.FloatField(min_value=0, max_value=1),
        help_text="Минимально допустимое содержание серы, %"
    )
    S_max = serializers.ListField(
        child=serializers.FloatField(min_value=0, max_value=1),
        help_text="Максимально допустимое содержание серы, %"
    )
    delta_P_pg = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Влияние ПГ на производство, т/(м3/ч)"
    )
    delta_P_k = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Влияние кокса на производство, т/(кг/ч)"
    )
    delta_S_pg = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Влияние ПГ на серу, %/(м3/ч)"
    )
    delta_S_k = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Влияние кокса на серу, %/(кг/ч)"
    )
    delta_S_p = serializers.ListField(
        child=serializers.FloatField(),
        help_text="Влияние производительности на серу, %/(т/ч)"
    )

    def validate(self, data):
        n = data['N']
        list_fields = [
            'V_pg_0', 'V_pg_min', 'V_pg_max', 'K_0', 'e',
            'P_0', 'S_0', 'S_min', 'S_max',
            'delta_P_pg', 'delta_P_k',
            'delta_S_pg', 'delta_S_k', 'delta_S_p'
        ]

        # Проверка длины массивов
        for field in list_fields:
            if len(data[field]) != n:
                raise serializers.ValidationError(
                    f"Поле {field} должно содержать ровно {n} значений (по числу печей)"
                )

        # Проверка минимальных/максимальных значений ПГ
        for i in range(n):
            if data['V_pg_min'][i] > data['V_pg_max'][i]:
                raise serializers.ValidationError(
                    f"Минимальный расход ПГ не может превышать максимальный (печь {i + 1})"
                )

            if not (data['V_pg_min'][i] <= data['V_pg_0'][i] <= data['V_pg_max'][i]):
                raise serializers.ValidationError(
                    f"Базовый расход ПГ для печи {i + 1} выходит за допустимые границы"
                )

        # Проверка содержания серы
        for i in range(n):
            if data['S_min'][i] > data['S_max'][i]:
                raise serializers.ValidationError(
                    f"Минимальное содержание серы не может превышать максимальное (печь {i + 1})"
                )

            if not (data['S_min'][i] <= data['S_0'][i] <= data['S_max'][i]):
                raise serializers.ValidationError(
                    f"Базовое содержание серы для печи {i + 1} выходит за допустимые границы"
                )

        return data
    
class CalculatedSerializer(serializers.Serializer):
    """
    Сериализатор для рассчитанных оптимальных значений.
    """

    objective = serializers.FloatField(
        min_value = 0,
        help_text = "Целевая функция руб/ч"
    )
    gas_distribution = serializers.ListField(
        child=serializers.FloatField(
            min_value = 0
        ),
        help_text="Распределение ПГ (м3/ч)"
    )
    total_gas_consumption = serializers.FloatField(
        min_value = 0,
        help_text = "Общий расход ПГ м3/ч"
    )
    total_coke_consumption = serializers.FloatField(
        min_value = 0,
        help_text = "Общий расход кокса т/ч"
    )
    total_iron_production = serializers.FloatField(
        min_value = 0,
        help_text = "Общее производство чугуна т/ч"
    )
    sulfur_content = serializers.ListField(
        child=serializers.FloatField(
            min_value = 0
        ),
        help_text="одержание серы (%)"
    )
    status = serializers.CharField(
        min_length=1,
        help_text="Статус"
    )