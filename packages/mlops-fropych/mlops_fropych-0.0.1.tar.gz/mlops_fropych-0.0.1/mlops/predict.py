from pathlib import Path

import joblib
import numpy as np
from loguru import logger
from sklearn.pipeline import Pipeline


def load_pipeline(path: str) -> Pipeline:
    path = Path(path)
    logger.info("Loading pipeline from {}", path.absolute())
    pipeline = joblib.load(path)
    return pipeline

def make_prediction(pipeline: Pipeline, X_new: np.ndarray) -> np.ndarray:
    logger.info("Making predictions")
    predictions = pipeline.predict(X_new)
    return predictions