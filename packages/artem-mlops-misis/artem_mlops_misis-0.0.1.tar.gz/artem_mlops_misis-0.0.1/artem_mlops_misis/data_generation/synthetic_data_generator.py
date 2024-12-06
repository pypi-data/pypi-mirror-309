"""
Модуль генерации данных.
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from loguru import logger
import typer
from pathlib import Path

from artem_mlops_misis.config_loader.loader import load_config


def generate_synthetic_data(
    n_samples: int = 1000,
    n_features: int = 10,
    n_informative: int = 5,
    n_classes: int = 2,
    random_state: int = 42,
):
    """
    Генерирует синтетические данные для классификации или регрессии.

    Параметры:
    n_samples (int): Количество примеров.
    n_features (int): Количество признаков.
    n_informative (int): Количество информативных признаков.
    n_classes (int): Количество классов (только для классификации).
    random_state (int): Начальное состояние генератора случайных чисел.

    Возвращает:
    X, y: Матрица объектов-признаков и вектор целевых переменных.
    """
    np.random.seed(random_state)

    x, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_classes=n_classes,
        random_state=random_state,
    )
    logger.debug(f"Размер сгенерированных данных X:{x.shape} y:{y.shape}")
    return pd.DataFrame(x), y


app = typer.Typer()


@app.command()
def main(
    config_path: Path = Path(__file__).parent.parent.parent / "params.yaml",
) -> None:
    logger.info("Считывание конфига")
    config = load_config(config_path)

    logger.info("Генерация Данных")
    x, y = generate_synthetic_data(
        n_samples=config.data.n_samples,
        n_features=config.data.n_features,
        n_informative=config.data.n_informative,
        n_classes=config.data.n_classes,
    )
    x.to_csv(config.data.raw_x_path, index=False)
    y.to_csv(config.data.y_path, index=False)


if __name__ == "__main__":
    app()
