import json
import pickle
import time
from pathlib import Path

import numpy as np
import sklearn.ensemble
import sklearn.metrics
import typer
from loguru import logger

from misiss_mlops.entities.params import read_pipeline_params

app = typer.Typer()


@app.command()
def predict(params_path: str):

    params = read_pipeline_params(params_path)
    load_path = Path(params.data_params.data_dir)
    x_test = np.load(load_path / "X_test.npy")
    y_test = np.load(load_path / "y_test.npy")

    model_path = Path(params.train_params.model_path) / params.train_params.model_file_name
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    logger.info(f"Model loaded from {model_path}")

    y_pred = model.predict(x_test)
    logger.info("Predictions made on the test set")

    metrics = {
        "accuracy": round(sklearn.metrics.accuracy_score(y_test, y_pred), 3),
        "f1_score": round(sklearn.metrics.f1_score(y_test, y_pred), 3),
        "precision": round(sklearn.metrics.precision_score(y_test, y_pred), 3),
        "recall": round(sklearn.metrics.recall_score(y_test, y_pred), 3),
    }
    logger.info(f"Metrics: {metrics}")

    metrics_path = Path(params.train_params.metrics_path)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    logger.info(f"Metrics saved to {metrics_path}")


if __name__ == "__main__":
    app()
