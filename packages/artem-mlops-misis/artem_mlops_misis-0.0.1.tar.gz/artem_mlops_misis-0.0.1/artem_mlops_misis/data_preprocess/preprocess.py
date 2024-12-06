"""
Модуль предобработки данных.
"""

from pathlib import Path

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import typer
from loguru import logger

from artem_mlops_misis.config_loader.loader import load_config


def preprocess_data(
    x: pd.DataFrame,
    numerical_cols: list | None = None,
    categorical_cols: list | None = None,
) -> pd.DataFrame:
    """
    Выполняет предобработку данных, включая обработку пропусков,
    масштабирование числовых признаков
    и кодирование категориальных признаков.

    Параметры:
    x (pd.DataFrame): Матрица объектов-признаков.
    numerical_cols (list): Список названий числовых столбцов.
    categorical_cols (list): Список названий категориальных столбцов.
    target_col (str): Название столбца с целевой переменной.

    Возвращает:
    x_preprocessed (pd.DataFrame): Предобработанная матрица объектов-признаков.
    """
    imputer = SimpleImputer(strategy="most_frequent")
    x_imputed = pd.DataFrame(imputer.fit_transform(x), columns=x.columns)

    if numerical_cols:
        scaler = StandardScaler()
        x_numeric = x_imputed[numerical_cols]
        x_numeric_scaled = pd.DataFrame(scaler.fit_transform(x_numeric), columns=numerical_cols)
        if categorical_cols:
            x_preprocessed = pd.concat([x_numeric_scaled, x_imputed[categorical_cols]], axis=1)
        else:
            x_preprocessed = x_numeric_scaled
    else:
        x_preprocessed = x_imputed

    if categorical_cols:
        encoder = OneHotEncoder()
        x_cat = x_preprocessed[categorical_cols]
        x_cat_encoded = pd.DataFrame(
            encoder.fit_transform(x_cat).toarray(),
            columns=encoder.get_feature_names_out(),
        )
        x_preprocessed = pd.concat(
            [x_preprocessed.drop(categorical_cols, axis=1), x_cat_encoded],
            axis=1,
        )

    return x_preprocessed


app = typer.Typer()


@app.command()
def main(
    config_path: Path = Path(__file__).parent.parent.parent / "params.yaml",
) -> None:
    logger.info("Считывание конфига")
    config = load_config(config_path)

    x = pd.read_csv(config.data.raw_x_path)

    logger.info("Предобработка данных.")
    categorical_cols = x.select_dtypes(include=["object", "category"]).columns.tolist()
    numerical_cols = x.select_dtypes(include=["number"]).columns.tolist()
    x = preprocess_data(
        x=x,
        numerical_cols=numerical_cols,
        categorical_cols=categorical_cols,
    )

    x.to_csv(config.data.preproc_x, index=False)


if __name__ == "__main__":
    app()
