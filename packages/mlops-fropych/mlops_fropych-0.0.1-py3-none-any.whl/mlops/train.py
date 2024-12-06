from pathlib import Path
from typing import Dict, Tuple

import hydra
import joblib
import pandas as pd
import yaml
from hydra.utils import instantiate
from loguru import logger
from omegaconf import OmegaConf
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from mlops.config import PipelineConfig, TrainConfig


def split_data(X, y, config: TrainConfig) -> Tuple:
    logger.info("Splitting data with test size: {}", config.test_size)
    return train_test_split(X, y, test_size=config.test_size)


def train_model(X_train, y_train, config: TrainConfig) -> Pipeline:
    logger.info("Training model with configuration: {}", config.model)
    model = instantiate(config.model, _recursive_=False)

    steps = []
    if config.data_preprocess_config.scaler:
        scaler = instantiate(config.data_preprocess_config.scaler, _recursive_=False)
        steps.append(("scaler", scaler))
    steps.append(("classifier", model))

    pipeline = Pipeline(steps)
    pipeline.fit(X_train, y_train)
    return pipeline


def evaluate_model(pipeline: Pipeline, X_test, y_test) -> Dict[str, float]:
    logger.info("Evaluating model")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info("Model accuracy: {:.2f}", accuracy)
    return {"Accuracy": accuracy}


def save_pipeline(pipeline: Pipeline, config: PipelineConfig):
    path = Path(config.save_path)
    path.parent.mkdir(exist_ok=True, parents=True)

    logger.info("Saving pipeline to {}", path.absolute())
    joblib.dump(pipeline, path)


def save_metrics(metrics: Dict[str, float], metrics_path: str):
    metrics_path = Path(metrics_path)
    metrics_path.parent.mkdir(exist_ok=True, parents=True)

    logger.info("Saving metrics to {}", metrics_path.absolute())
    with open(metrics_path, "w") as file:
        yaml.dump(metrics, file)


@hydra.main(version_base=None, config_name="random_forest", config_path="../configs")
def main(config: PipelineConfig):
    logger.info(f"Starting pipeline with configuration:\n{OmegaConf.to_yaml(config)}")
    config = instantiate(config, _recursive_=True)

    data = pd.read_csv(config.data_generator_config.save_path)
    X = data.drop(columns="target").values
    y = data["target"].values

    X_train, X_test, y_train, y_test = split_data(X, y, config.train_config)
    pipeline = train_model(X_train, y_train, config.train_config)
    metrics = evaluate_model(pipeline, X_test, y_test)
    save_metrics(metrics, config.metrics_path)
    save_pipeline(pipeline, config)


if __name__ == "__main__":
    main()
