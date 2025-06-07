from gas.models import Calculate, History
from rest_framework import serializers


class CalculateBaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели Calculate (Входных данных).
    Сериализатор для расчета оптимального распределения природного газа между доменными печами.
    """
    
    class Meta:
        model = Calculate
        fields = []
        extra_kwargs = {
            "C_k": {
                "min_value": 0,
                "help_text": "Стоимость кокса, руб/(кг кокса)",
            },
            "C_pg": {
                "min_value": 0,
                "help_text": "Стоимость природного газа, руб/(м3 ПГ)",
            },
            "V_pg_total": {
                "min_value": 0,
                "help_text": "Лимит расхода природного газа по цеху, м3/ч",
            },
            "K_total": {
                "min_value": 0,
                "help_text": "Запасы кокса по цеху, т/ч",
            },
            "P_total": {
                "min_value": 0,
                "help_text": "Требуемая производительность по чугуну, т/ч",
            },
            "N": {
                "min_value": 1,
                "max_value": 20,
                "help_text": "Количество печей (1-20)"
            },
            "V_pg_0": {
                "min_length": 1,
                "help_text": "Базовый расход ПГ по печам, м3/ч"
            },
            "V_pg_min": {
                "min_length": 1,
                "help_text": "Минимальный расход ПГ по печам, м3/ч",
            },
            "V_pg_max": {
                "min_length": 1,
                "help_text": "Максимальный расход ПГ по печам, м3/ч",
            },
            "K_0": {
                "min_length": 1,
                "help_text": "Базовый расход кокса по печам, т/ч",
            },
            "e": {
                "min_length": 1,
                "help_text": "Эквивалент замены кокса, кг/(м3 ПГ)",
            },
            "P_0": {
                "min_length": 1,
                "help_text": "Базовая производительность по печам, т/ч",
            },
            "S_0": {
                "min_length": 1,
                "help_text": "Базовое содержание серы, %",
            },
            "S_min": {
                "min_length": 1,
                "help_text": "Минимально допустимое содержание серы, %",
            },
            "S_max": {
                "min_length": 1,
                "help_text": "Максимально допустимое содержание серы, %",
            },
            "delta_P_pg": {
                "min_length": 1,                
                "help_text": "Влияние ПГ на производство, т/(м3/ч)",
            },
            "delta_P_k": {
                "min_length": 1,
                "help_text": "Влияние кокса на производство, т/(кг/ч)",
            },
            "delta_S_pg": {
                "min_length": 1,
                "help_text": "Влияние ПГ на серу, %/(м3/ч)",
            },
            "delta_S_k": {
                "min_length": 1,
                "help_text": "Влияние кокса на серу, %/(кг/ч)",
            },
            "delta_S_p": {
                "min_length": 1,
                "help_text": "Влияние производительности на серу, %/(т/ч)",
            },
        }

    def validate(self, data):
        n = data["N"]
        list_fields = [
            "V_pg_0", "V_pg_min", "V_pg_max", "K_0", "e",
            "P_0", "S_0", "S_min", "S_max",
            "delta_P_pg", "delta_P_k",
            "delta_S_pg", "delta_S_k", "delta_S_p"
        ]

        # Проверка длины массивов
        for field in list_fields:
            if len(data[field]) != n:
                raise serializers.ValidationError(
                    f"Поле {field} должно содержать ровно {n} значений (по числу печей)"
                )

        # Проверка минимальных/максимальных значений ПГ
        for i in range(n):
            if data["V_pg_min"][i] > data["V_pg_max"][i]:
                raise serializers.ValidationError(
                    f"Минимальный расход ПГ не может превышать максимальный (печь {i + 1})"
                )

            if not (data["V_pg_min"][i] <= data["V_pg_0"][i] <= data["V_pg_max"][i]):
                raise serializers.ValidationError(
                    f"Базовый расход ПГ для печи {i + 1} выходит за допустимые границы"
                )

        # Проверка содержания серы
        for i in range(n):
            if data["S_min"][i] > data["S_max"][i]:
                raise serializers.ValidationError(
                    f"Минимальное содержание серы не может превышать максимальное (печь {i + 1})"
                )

            if not (data["S_min"][i] <= data["S_0"][i] <= data["S_max"][i]):
                raise serializers.ValidationError(
                    f"Базовое содержание серы для печи {i + 1} выходит за допустимые границы"
                )

        return data

class CalculateShortSerializer(CalculateBaseSerializer):
    """
    Сериализатор модели Calculate для вывода в списках.
    """

    class Meta(CalculateBaseSerializer.Meta):
        fields = CalculateBaseSerializer.Meta.fields + ["C_k", "C_pg", "V_pg_total", "K_total", "P_total", "N"]

class CalculateCreateSerializer(CalculateBaseSerializer):
    """
    Сериализатор модели Calculate для создания.
    Валидирует входные данные и проверяет согласованность размеров массивов.
    """

    class Meta(CalculateBaseSerializer.Meta):
        fields = CalculateBaseSerializer.Meta.fields + ["C_k", "C_pg", "V_pg_total", "K_total", "P_total", "N", "V_pg_0", 
                                                        "V_pg_min", "V_pg_max", "K_0", "e", "P_0", "S_0", "S_min", "S_max", 
                                                        "delta_P_pg", "delta_P_k", "delta_S_pg", "delta_S_k", "delta_S_p"]

class HistoryBaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели History.
    Сериализатор для хранения оптимального расчета распределения природного газа между доменными печами
    """

    class Meta:
        model = History
        fields = []
        extra_kwargs = {
            "objective": {
                "min_value": 0,
                "help_text": "Целевая функция руб/ч",
            },
            "gas_distribution": {
                "min_length": 1,
                "help_text": "Распределение ПГ (м3/ч)",
            },
            "total_gas_consumption": {
                "min_value": 0,
                "help_text": "Общий расход ПГ м3/ч",
            },
            "total_coke_consumption": {
                "min_value": 0,
                "help_text": "Общий расход кокса т/ч",
            },
            "total_iron_production": {
                "min_value": 0,
                "help_text": "Общее производство чугуна т/ч",
            },
            "sulfur_content": {
                "min_length": 1,
                "help_text": "Cодержание серы (%)",
            },
            "status": {
                "min_length": 1,
                "help_text": "Статус",
            },
        }
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        calculate_data = validated_data.pop("calculate")
        calculate_instance = Calculate.objects.create(**calculate_data)

        history_instance = History.objects.create(
            calculate=calculate_instance,
            user=self.context["request"].user,
            **validated_data
        )

        return history_instance

class HistoryListSerializer(HistoryBaseSerializer):
    """
    Сериализатор модели History для вывода списка расчетов.
    """

    calculate = CalculateShortSerializer()

    class Meta(HistoryBaseSerializer.Meta):
        fields = HistoryBaseSerializer.Meta.fields + ["id", "created_at", "objective", "gas_distribution", "total_gas_consumption", "total_coke_consumption", "total_iron_production", "sulfur_content", "status", "calculate"]

class HistoryDetailSerializer(HistoryBaseSerializer):
    """
    Сериализатор модели History для детального просмотра расчетов.
    """

    class Meta(HistoryBaseSerializer.Meta):
        fields = HistoryBaseSerializer.Meta.fields + ["objective", "gas_distribution", "total_gas_consumption", "total_coke_consumption", "total_iron_production", "sulfur_content", "status"]

class HistoryCreateSerializer(HistoryBaseSerializer):
    """
    Сериализатор модели History для создания расчета.
    Автоматически привязывает расчет к текущему пользователю.
    """

    calculate = CalculateCreateSerializer()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(HistoryBaseSerializer.Meta):
        fields = HistoryBaseSerializer.Meta.fields + ["id", "created_at", "calculate", "objective", "gas_distribution", "total_gas_consumption", "total_coke_consumption",
                  "total_iron_production", "sulfur_content", "status", "user"]
