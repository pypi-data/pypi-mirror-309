"""
Модуль для загрузки конфига.
"""

from pathlib import Path
import yaml

from pydantic import BaseModel
from loguru import logger

from artem_mlops_misis.config_loader.models.data import DataSettings
from artem_mlops_misis.config_loader.models.general import GeneralSettings
from artem_mlops_misis.config_loader.models.metrics import MetricsSettings
from artem_mlops_misis.config_loader.models.ml_models import ModelSettings


class Config(BaseModel):
    """
    general - общая информация.
    data - настройки данных.
    model - настройки модели.
    metric - метрики для оценки.
    """

    general: GeneralSettings
    data: DataSettings
    model: ModelSettings
    metric: MetricsSettings


def load_config(config_path: str) -> Config:
    """
    Загружает конфигурацию из YAML-файла и возвращает объект Config.
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден.")

    try:
        with open(config_file, "r") as f:
            config_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Ошибка при загрузке конфигурационного файла: {e}")
    logger.debug(config_data)
    return Config(**config_data)
