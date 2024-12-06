"""
Модель данных для синтетических данных.
"""

from pydantic import BaseModel, Field


class DataSettings(BaseModel):
    """
    Класс для настройки параметров генерации данных для тестирования и обучения моделей.

    Атрибуты:
        test_size (float):
            Доля данных, отводимая для тестирования. Должна быть в диапазоне (0, 0.6).
        random_state (int):
            Состояние генератора случайных чисел для воспроизводимости результатов.
        n_samples (int):
            Общее количество образцов (строк) данных, которые будут сгенерированы.
        n_features (int):
            Общее количество признаков (столбцов) в сгенерированных данных.
        n_informative (int):
            Количество информативных признаков,
            которые будут использоваться для генерации целевой переменной.
        n_classes (int):
            Количество классов для целевой переменной (для задач классификации).
    """

    raw_x_path: str = Field("data/raw/x.csv")
    y_path: str = Field("data/raw/y.csv")
    preproc_x: str = Field("data/processed/x.csv")

    x_train_path: str = Field("data/interim/x_train.csv")
    x_test_path: str = Field("data/interim/x_test.csv")
    y_train_path: str = Field("data/interim/y_train.csv")
    y_test_path: str = Field("data/interim/y_test.csv")

    y_pred: str = Field("data/interim/y_pred.csv")

    test_size: float = Field(default=0.2, gt=0, lt=0.6)
    random_state: int = Field(default=42)
    n_samples: int = Field(default=1000)
    n_features: int = Field(default=10)
    n_informative: int = Field(default=5)
    n_classes: int = Field(default=3)
