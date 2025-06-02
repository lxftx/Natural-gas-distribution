from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class Calculate(models.Model):
    """
    Модель для хранения входных данных.
    """

    C_k = models.FloatField(verbose_name="Стоимость кокса, руб/(кг кокса)")
    C_pg = models.FloatField(verbose_name="Стоимость природного газа, руб/(м3 ПГ)")
    V_pg_total = models.FloatField(verbose_name="Лимит расхода природного газа по цеху, м3/ч")
    K_total = models.FloatField(verbose_name="Запасы кокса по цеху, т/ч")
    P_total = models.FloatField(verbose_name="Требуемая производительность по чугуну, т/ч")
    N = models.IntegerField(verbose_name="Количество печей (1-20)")
    V_pg_0 = ArrayField(
        verbose_name="Базовый расход ПГ по печам, м3/ч",
        base_field=models.FloatField()
    )
    V_pg_min = ArrayField(
        verbose_name="Минимальный расход ПГ по печам, м3/ч",
        base_field=models.FloatField()
    )
    V_pg_max = ArrayField(
        verbose_name="Максимальный расход ПГ по печам, м3/ч",
        base_field=models.FloatField()
    )
    K_0 = ArrayField(
        verbose_name="Базовый расход кокса по печам, т/ч",
        base_field=models.FloatField()
    )
    e = ArrayField(
        verbose_name="Эквивалент замены кокса, кг/(м3 ПГ)",
        base_field=models.FloatField()
    )
    P_0 = ArrayField(
        verbose_name="Базовая производительность по печам, т/ч",
        base_field=models.FloatField()
    )
    S_0 = ArrayField(
        verbose_name="Базовое содержание серы, %",
        base_field=models.FloatField()
    )
    S_min = ArrayField(
        verbose_name="Минимально допустимое содержание серы, %",
        base_field=models.FloatField()
    )
    S_max = ArrayField(
        verbose_name="Максимально допустимое содержание серы, %",
        base_field=models.FloatField()
    )
    delta_P_pg = ArrayField(
        verbose_name="Влияние ПГ на производство, т/(м3/ч)",
        base_field=models.FloatField()
    )
    delta_P_k = ArrayField(
        verbose_name="Влияние кокса на производство, т/(кг/ч)",
        base_field=models.FloatField()
    )
    delta_S_pg = ArrayField(
        verbose_name="Влияние ПГ на серу, %/(м3/ч)",
        base_field=models.FloatField()
    )
    delta_S_k = ArrayField(
        verbose_name="Влияние кокса на серу, %/(кг/ч)",
        base_field=models.FloatField()
    )
    delta_S_p = ArrayField(
        verbose_name="Влияние производительности на серу, %/(т/ч)",
        base_field=models.FloatField()
    )

    def __str__(self):
        return f"Входные данные №{self.pk}."
    
class History(models.Model):
    """
    Модель для хранения истории расчетов.
    """

    created_at = models.DateTimeField(verbose_name="Дата и время создания расчета", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата и время последнего обновления", auto_now=True)
    calculate = models.ForeignKey(to=Calculate, on_delete=models.CASCADE, verbose_name="Входные данные", related_name="calculate")
    objective = models.FloatField(verbose_name = "Целевая функция руб/ч")
    gas_distribution = ArrayField(
        verbose_name="Распределение ПГ (м3/ч)",
        base_field=models.FloatField(),
        help_text="Распределение ПГ (м3/ч)"
    )
    total_gas_consumption = models.FloatField(verbose_name="Общий расход ПГ м3/ч")
    total_coke_consumption = models.FloatField(verbose_name="Общий расход кокса т/ч")
    total_iron_production = models.FloatField(verbose_name="Общее производство чугуна т/ч")
    sulfur_content = ArrayField(
        verbose_name="Содержание серы (%)",
        base_field=models.FloatField(),
        help_text="Содержание серы (%)"
    )
    status = models.CharField(verbose_name="Статус")

    def __str__(self):
        return f"История №{self.pk}."