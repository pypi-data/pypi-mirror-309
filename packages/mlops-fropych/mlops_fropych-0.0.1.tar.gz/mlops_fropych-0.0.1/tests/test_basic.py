from pathlib import Path

import pandas as pd
import pytest
from sklearn.pipeline import Pipeline
from mlops.train import split_data, train_model, evaluate_model
from mlops.dataset import generate_data
from mlops.config import DataGeneratorConfig, TrainConfig, DataPreprocessConfig


@pytest.fixture
def data_generator_config():
    return DataGeneratorConfig(
        n_samples=100, n_features=10, n_informative=5, n_redundant=2, n_classes=2, save_path="data.csv"
    )


@pytest.fixture
def train_config():
    return TrainConfig(
        model={"_target_": "sklearn.ensemble.RandomForestClassifier"},
        data_preprocess_config=DataPreprocessConfig(
            scaler={"_target_": "sklearn.preprocessing.MinMaxScaler"},
        ),
        test_size=0.2,
    )


def test_generate_data(data_generator_config: DataGeneratorConfig):
    generate_data(data_generator_config)
    assert Path(data_generator_config.save_path).exists()


def test_split_data(data_generator_config: DataGeneratorConfig, train_config: TrainConfig):
    generate_data(data_generator_config)
    
    data = pd.read_csv(data_generator_config.save_path)
    X = data.drop(columns="target").values
    y = data["target"].values
    
    X_train, X_test, y_train, y_test = split_data(X, y, train_config)
    assert len(X_train) == int(data_generator_config.n_samples * (1 - train_config.test_size))
    assert len(X_test) == int(data_generator_config.n_samples * train_config.test_size)


def test_train_model(data_generator_config: DataGeneratorConfig, train_config: TrainConfig):
    generate_data(data_generator_config)
    
    data = pd.read_csv(data_generator_config.save_path)
    X = data.drop(columns="target").values
    y = data["target"].values
    
    X_train, _, y_train, _ = split_data(X, y, train_config)
    pipeline = train_model(X_train, y_train, train_config)
    assert isinstance(pipeline, Pipeline)
    assert "classifier" in pipeline.named_steps


def test_evaluate_model(data_generator_config: DataGeneratorConfig, train_config: TrainConfig):
    generate_data(data_generator_config)
    
    data = pd.read_csv(data_generator_config.save_path)
    X = data.drop(columns="target").values
    y = data["target"].values
    
    X_train, X_test, y_train, y_test = split_data(X, y, train_config)
    pipeline = train_model(X_train, y_train, train_config)
    accuracy = evaluate_model(pipeline, X_test, y_test)['Accuracy']
    assert 0.0 <= accuracy <= 1.0
