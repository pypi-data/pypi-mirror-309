import hydra
from hydra.utils import instantiate
from omegaconf import OmegaConf
import pandas as pd
from loguru import logger
from sklearn.datasets import make_classification

from mlops.config import DataGeneratorConfig


def generate_data(config: DataGeneratorConfig):
    logger.info("Generating data with configuration: {}", config)
    X, y = make_classification(
        n_samples=config.n_samples,
        n_features=config.n_features,
        n_informative=config.n_informative,
        n_redundant=config.n_redundant,
        n_classes=config.n_classes,
    )

    df = pd.DataFrame(X)
    df["target"] = y
    df.to_csv(config.save_path, index=False)
    logger.info("Data saved to {}", config.save_path)


@hydra.main(version_base=None, config_name="base", config_path="../configs")
def main(config: DataGeneratorConfig):
    logger.info(f"Starting data generation with configuration:\n{OmegaConf.to_yaml(config)}")
    config = instantiate(config.data_generator_config, _recursive_=True)
    generate_data(config)


if __name__ == "__main__":
    main()
