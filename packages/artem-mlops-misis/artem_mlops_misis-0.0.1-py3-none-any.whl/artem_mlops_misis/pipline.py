"""
Главный модуль обучения.
"""

from pathlib import Path
import time
import pickle

from sklearn.model_selection import train_test_split
from loguru import logger
import typer


from artem_mlops_misis.data_generation.synthetic_data_generator import generate_synthetic_data
from artem_mlops_misis.config_loader.loader import load_config
from artem_mlops_misis.model_performance.train import (
    train_decision_tree,
    train_logistic_regression,
    train_random_forest,
)
from artem_mlops_misis.evaluation.eval import evaluate_model, get_pred
from artem_mlops_misis.data_preprocess.preprocess import preprocess_data

app = typer.Typer()


@app.command()
def main(config_path: Path = Path(__file__).parent.parent / "random_forest_pipline.yaml") -> None:
    """Глаыная функция обучекния."""
    logger.info("Считывание конфига")
    config = load_config(config_path)

    logger.info("Генерация Данных")
    x, y = generate_synthetic_data(
        n_samples=config.data.n_samples,
        n_features=config.data.n_features,
        n_informative=config.data.n_informative,
        n_classes=config.data.n_classes,
    )

    logger.info("Предобработка данных.")
    categorical_cols = x.select_dtypes(include=["object", "category"]).columns.tolist()
    numerical_cols = x.select_dtypes(include=["number"]).columns.tolist()
    x = preprocess_data(
        x=x,
        numerical_cols=numerical_cols,
        categorical_cols=categorical_cols,
    )

    logger.info("Разбиение на тренировочную и тестовую выборки.")
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config.data.test_size, random_state=config.data.random_state
    )

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

    logger.info("Оценка модели")
    y_pred = get_pred(model=model, x_test=x_test)
    scores = evaluate_model(y_true=y_test, y_pred=y_pred)
    logger.info(f"Результаты {scores}")

    logger.info("Сохранение результатов")
    model_path = (
        Path(__file__).parent.parent
        / "models"
        / f"{config.model.model_type_name}{time.time().as_integer_ratio()[0]}.pkl"
    )
    with open(model_path, "wb") as file:
        pickle.dump(model, file)
        logger.info(f"Модель сохранена: {model_path}")
    return 0


if __name__ == "__main__":
    app()
