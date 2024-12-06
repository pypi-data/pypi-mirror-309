from pathlib import Path

import typer
import pandas as pd
from loguru import logger
from sklearn.model_selection import train_test_split


from artem_mlops_misis.config_loader.loader import load_config

app = typer.Typer()


@app.command()
def main(config_path: Path = Path(__file__).parent.parent / "params.yaml") -> None:
    config = load_config(config_path)

    x = pd.read_csv(config.data.preproc_x)
    y = pd.read_csv(config.data.y_path)

    logger.info("Разбиение на тренировочную и тестовую выборки.")
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config.data.test_size, random_state=config.data.random_state
    )

    x_train.to_csv(config.data.x_train_path, index=False)
    x_test.to_csv(config.data.x_test_path, index=False)
    y_train.to_csv(config.data.y_train_path, index=False)
    y_test.to_csv(config.data.y_test_path, index=False)


if __name__ == "__main__":
    app()
