import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from hydra import compose, initialize
from hydra.core.config_store import ConfigStore
from hydra.utils import instantiate
from omegaconf import OmegaConf


def load_config(config_path: str):
    initialize(version_base="1.3", config_path=os.path.relpath(config_path, os.path.dirname(__file__)), job_name="test_app")
    cfg = compose(config_name="base_airflow",)
    OmegaConf.resolve(cfg)
    cfg: PipelineConfig = instantiate(cfg, _recursive_=True)
    return cfg

class ScalerType(str, Enum):
    NONE = "None"
    STANDARD = "StandardScaler"
    MINMAX = "MinMaxScaler"


def range_validation_from_metadata(obj):
    for field_name, field_def in obj.__dataclass_fields__.items():
        value = getattr(obj, field_name)
        min_value = field_def.metadata.get("min_value")
        max_value = field_def.metadata.get("max_value")
        if min_value is not None and value < min_value:
            raise ValueError(f"{field_name} must be at least {min_value}, got {value}")
        if max_value is not None and value > max_value:
            raise ValueError(f"{field_name} must be at most {max_value}, got {value}")


@dataclass
class DataGeneratorConfig:
    n_samples: int = field(default=1000, metadata={"min_value": 1})
    n_features: int = field(default=20, metadata={"min_value": 1})
    n_informative: int = field(default=2, metadata={"min_value": 0})
    n_redundant: int = field(default=2, metadata={"min_value": 0})
    n_classes: int = field(default=2, metadata={"min_value": 2})
    random_state: int = 42
    save_path: str = "../data/raw/data.csv"

    def __post_init__(self):
        range_validation_from_metadata(self)


@dataclass
class DataPreprocessConfig:
    scaler: Optional[Dict[str, Any]] = field(
        default_factory=lambda: {"_target_": "sklearn.preprocessing.MinMaxScaler"}
    )


@dataclass
class TrainConfig:
    model: Optional[Dict[str, Any]] = field(
        default_factory=lambda: {"_target_": "sklearn.ensemble.RandomForestClassifier"}
    )

    data_preprocess_config: DataPreprocessConfig = DataPreprocessConfig()
    test_size: float = field(default=0.2, metadata={"min_value": 0.0, "max_value": 1.0})

    def __post_init__(self):
        if "_target_" not in self.model:
            raise ValueError("The 'model' dictionary must contain a '_target_' key.")

        range_validation_from_metadata(self)


@dataclass
class PipelineConfig:
    train_config: TrainConfig = TrainConfig()
    data_generator_config: DataGeneratorConfig = DataGeneratorConfig()
    save_path: str = "models/base/model_pipeline.pkl"
    metrics_path: str = "models/base/metrics.yaml"
    random_state: int = 42
    
    batch_predict_new_data_path: Optional[str] = None
    batch_predict_output_path: Optional[str] = None


cs = ConfigStore.instance()
cs.store(name="pipeline_config", node=PipelineConfig)
