import pickle
from pathlib import Path

import numpy as np
import typer
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from misiss_mlops.entities.params import read_pipeline_params

app = typer.Typer()


def choose_model(model_name: str, model_params: dict):
    if model_name == "logistic_regression":
        return LogisticRegression(penalty=model_params["penalty"])
    if model_name == "random_forest":
        return RandomForestClassifier(
            n_estimators=model_params["n_estimators"], max_depth=model_params["max_depth"]
        )
    if model_name == "decision_tree":
        return DecisionTreeClassifier(max_depth=model_params["max_depth"])
    return None

def save_model(model, model_path: Path):
    with open(model_path, "wb") as f:
        pickle.dump(model, f)


@app.command()
def train_model(params_path: str):

    params = read_pipeline_params(params_path)
    load_path = Path(params.data_params.data_dir)
    x_train = np.load(load_path / "X_train.npy")
    y_train = np.load(load_path / "y_train.npy")
    logger.info(f"Data loaded from {load_path}")
    model_params = params.train_params.classification_model_params
    model = choose_model(params.train_params.model_name, model_params)
    logger.info(f"model is selected - {params.train_params.model_name}")

    model.fit(x_train, y_train)
    logger.info("model is trained")

    model_path = Path(params.train_params.model_path) / params.train_params.model_file_name
    save_model(model, model_path)
    logger.info(f"Model saved to {model_path}")


if __name__ == "__main__":
    app()
