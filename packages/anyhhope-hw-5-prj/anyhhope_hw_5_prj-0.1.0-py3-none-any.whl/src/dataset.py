import os
from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from src.config_utils import Params, project_root, read_params_from_yaml

app = typer.Typer()


def create_dataset(params: Params) -> pd.DataFrame:
    X, y = make_classification(
        n_samples=params.make_dataset.n_samples,
        n_features=params.make_dataset.n_features,
        n_informative=params.make_dataset.n_informative,
        n_redundant=params.make_dataset.n_redundant,
        n_classes=params.make_dataset.n_classes,
        shuffle=params.make_dataset.shuffle,
        random_state=params.random_state,
    )

    df = pd.DataFrame(X, columns=[f"col_{i+1}" for i in range(X.shape[1])])
    df[params.make_dataset.target_column_name] = y
    return df


@app.command()
def main(
    params_path: Path,
):
    """
    Make dataset for classification task
    """
    params = read_params_from_yaml(params_path)

    logger.info("Creating dataset...")
    df = create_dataset(params)
    logger.success(f"Dataset of shape {df.shape} is created")

    save_path = project_root / params.make_dataset.full_data_path
    df.to_csv(save_path, index=False)
    logger.info(f"Full dataset is saved to {save_path}")

    train_df, test_df = train_test_split(
        df,
        test_size=params.make_dataset.test_data_size,
        random_state=params.random_state,
    )

    save_path = project_root / params.make_dataset.train_data_path
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    train_df.to_csv(project_root / params.make_dataset.train_data_path, index=False)
    logger.info(f"Train dataset of shape {train_df.shape} is saved to {save_path}")

    save_path = project_root / params.make_dataset.test_data_path
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    test_df.to_csv(save_path, index=False)
    logger.info(f"Train dataset of shape {test_df.shape} is saved to {save_path}")


if __name__ == "__main__":
    app()
