"""
Модель данных ml модели))).
"""

from typing import Dict, Any
from pydantic import BaseModel, field_validator, Field


class ModelSettings(BaseModel):
    """
    Класс для хранения настроек модели машинного обучения.

    Атрибуты:
        model_type_name (str): Тип модели машинного обучения.
            Допустимые типы:
            "LogisticRegression", "RandomForestClassifier", "DecisionTreeClassifier".
        params (Dict[str, Any]): Параметры для настройки модели.
            Должны соответствовать требованиям выбранного типа модели.

    Методы:
        check_model_type: Проверяет, что указанный тип модели находится в
        списке допустимых типов.
    """

    model_type_name: str
    params: Dict[str, Any]

    model_path: str = Field("models/models.pkl")

    @field_validator("model_type_name")
    def check_model_type(cls, v):
        allowed_models = [
            "LogisticRegression",
            "RandomForestClassifier",
            "DecisionTreeClassifier",
        ]
        if v not in allowed_models:
            raise ValueError(
                f"Недопустимый тип модели: {v}. Допустимые типы: {', '.join(allowed_models)}"
            )
        return v
