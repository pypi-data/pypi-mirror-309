"""
Мсодуль для тренировки модели.
"""

from pathlib import Path
import pickle

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from loguru import logger
import typer
from artem_mlops_misis.config_loader.loader import load_config


def train_decision_tree(
    x_train: pd.DataFrame, y_train: pd.DataFrame, **params
) -> DecisionTreeClassifier:
    """
    Тренирует модель дерева решений.

    Параметры:
    x_train (pd.DataFrame): Обучающие данные.
    y_train (pd.DataFrame): Значение таргета для обучения.
    **params: Словарь гиперпараметров модели.

    Возвращает:
    model: Обученная модель дерева решений.
    """
    logger.info(f"Старт обучения. Параметры: {params}")
    model = DecisionTreeClassifier(**params)
    model.fit(x_train, y_train)

    return model


def train_logistic_regression(
    x_train: pd.DataFrame, y_train: pd.DataFrame, **params
) -> LogisticRegression:
    """
    Тренирует модель логистической регрессии.

    Параметры:
    x_train (pd.DataFrame): Обучающие данные.
    y_train (pd.DataFrame): Значение таргета для обучения.
    **params: Словарь гиперпараметров модели.

    Возвращает:
    model: Обученная модель логистической регрессии.
    """
    logger.info(f"Старт обучения. Параметры: {params}")

    model = LogisticRegression(**params)
    model.fit(x_train, y_train)

    return model


def train_random_forest(
    x_train: pd.DataFrame, y_train: pd.DataFrame, **params
) -> RandomForestClassifier:
    """
    Тренирует модель случайного леса.

    Параметры:
    x_train (pd.DataFrame): Обучающие данные.
    y_train (pd.DataFrame): Значение таргета для обучения.
    **params: Словарь гиперпараметров модели.

    Возвращает:
    model: Обученная модель случайного леса.
    """
    logger.info(f"Старт обучения. Параметры: {params}")

    model = RandomForestClassifier(**params)
    model.fit(x_train, y_train)

    return model


app = typer.Typer()


@app.command()
def main(config_path: Path = Path(__file__).parent.parent.parent / "params.yaml") -> None:
    config = load_config(config_path)

    x_train = pd.read_csv(config.data.x_train_path)
    y_train = pd.read_csv(config.data.y_train_path)

    logger.info(f"Тренировка модели {config.model.model_type_name}")
    if config.model.model_type_name == "LogisticRegression":
        model = train_logistic_regression(x_train, y_train, **config.model.params)
    elif config.model.model_type_name == "RandomForestClassifier":
        model = train_random_forest(x_train, y_train, **config.model.params)
    elif config.model.model_type_name == "DecisionTreeClassifier":
        model = train_decision_tree(x_train, y_train, **config.model.params)
    else:
        logger.error("Недопустимая модель.")
        return 0

    with open(config.model.model_path, "wb") as file:
        pickle.dump(model, file)
        logger.info(f"Модель сохранена: {config.model.model_path}")


if __name__ == "__main__":
    app()
