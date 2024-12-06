from pathlib import Path

import numpy as np
import typer
from loguru import logger
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from misiss_mlops.entities.params import read_pipeline_params

app = typer.Typer()


def save_data(save_path, x_train, x_test, y_train, y_test):

    save_path.mkdir(parents=True, exist_ok=True)
    np.save(save_path / "x_train.npy", x_train)
    np.save(save_path / "x_test.npy", x_test)
    np.save(save_path / "y_train.npy", y_train)
    np.save(save_path / "y_test.npy", y_test)
    logger.info(f"data is saved in {save_path}")


@app.command()
def generate_data(params_path: str):
    params = read_pipeline_params(params_path)
    x, y = make_classification(
        n_samples=params.data_params.n_samples,
        n_features=params.data_params.n_features,
        random_state=params.random_state,
    )
    logger.info("Data generation completed successfully.")
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=params.data_params.test_size, random_state=params.random_state
    )
    processed_data_path = Path(params.data_params.data_dir)
    save_data(processed_data_path, x_train, x_test, y_train, y_test)
    logger.info(f"Split data into train ({x_train.shape}) and test ({x_test.shape})")

    return x_train, x_test, y_train, y_test


if __name__ == "__main__":
    app()
