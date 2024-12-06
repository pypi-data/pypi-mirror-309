"""
Модуль для оценки модели.
"""

import json
import pickle
from pathlib import Path

import typer
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from loguru import logger

from artem_mlops_misis.config_loader.loader import load_config


def get_pred(model, x_test: pd.DataFrame) -> pd.DataFrame:
    """
    Получение предиктов модели.

    :param model: Обученная модель
    :param y_test: Тестовая выборка
    :return: Список предсказанных меток классов
    """
    y_pred = model.predict(x_test)

    return pd.DataFrame(y_pred)


def evaluate_model(y_true, y_pred):
    """
    Оценивает модель по различным метрикам.

    :param y_true: Список истинных меток классов
    :param y_pred: Список предсказанных меток классов
    :return: Словарь с метриками оценки
    """
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="weighted")

    metrics = {
        "Accuracy": accuracy,
        "F1 Score": f1,
    }

    return metrics


app = typer.Typer()


@app.command()
def main(
    config_path: Path = Path(__file__).parent.parent.parent / "random_forest_pipline.yaml",
) -> None:
    config = load_config(config_path)

    x_test = pd.read_csv(config.data.x_test_path)
    y_test = pd.read_csv(config.data.y_test_path)

    with open(config.model.model_path, "rb") as file:
        model = pickle.load(file)

    logger.info("Оценка модели")
    y_pred = get_pred(model=model, x_test=x_test)
    scores = evaluate_model(y_true=y_test, y_pred=y_pred)
    logger.info(f"Результаты {scores}")

    with open(config.metric.metrics_path, "w") as json_file:
        json.dump(scores, json_file)

    y_pred.to_csv(config.data.y_pred, index=False)


if __name__ == "__main__":
    app()
