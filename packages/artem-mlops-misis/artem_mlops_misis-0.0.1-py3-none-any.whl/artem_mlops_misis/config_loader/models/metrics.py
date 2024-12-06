"""
Модель данных для метрик.
"""

from typing import List
from pydantic import BaseModel, field_validator, Field


class MetricsSettings(BaseModel):
    """
    Класс для хранения настроек метрик, используемых для оценки моделей.

    Атрибуты:
        metrics (List[str]): Список метрик для оценки производительности модели.
            Допустимые метрики: "accuracy_score", "f1_score".

    Методы:
        check_metric: Проверяет, что все указанные метрики находятся в списке допустимых метрик.
            Если метрика недопустима, выбрасывает ValueError с соответствующим сообщением.

    """

    metrics: List[str]
    metrics_path: str = Field("references/metrics.json")

    @field_validator("metrics")
    def check_metric(cls, v: list):
        allowed_metrics = ["accuracy_score", "f1_score"]
        for value in v:
            if value not in allowed_metrics:
                raise ValueError(
                    f"Недопустимая метрика: {v}. Допустимые метрики: {', '.join(allowed_metrics)}"
                )
        return v
