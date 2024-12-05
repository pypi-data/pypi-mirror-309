import os
import pickle
from pathlib import Path

import pandas as pd
import typer
from loguru import logger

from src.config_utils import Params, project_root, read_params_from_yaml

app = typer.Typer()


def get_latest_model_path(model_dir: Path) -> Path:
    """
    Get the path of the latest model file in the directory.
    """
    model_files = list(model_dir.glob("model_*.pkl"))
    if not model_files:
        raise FileNotFoundError(f"No model files found in {model_dir}")

    latest_model = max(model_files, key=os.path.getmtime)
    return latest_model


def load_latest_model(params: Params):
    """
    Load the most recent trained model based on model_type from the saved path.
    """
    model_dir = (
        project_root / params.models_path / str(params.train_params.model_type.value)
    )

    if not model_dir.exists():
        raise FileNotFoundError(f"Model directory {model_dir} not found")

    latest_model_path = get_latest_model_path(model_dir)

    with open(latest_model_path, "rb") as f:
        model = pickle.load(f)
        print(type(model))

    return model, latest_model_path


@app.command()
def main(
    params_path: Path,
    new_data_path: Path,
):
    """
    Load the latest trained model and run inference on new data from the CSV file.
    """
    params = read_params_from_yaml(params_path)

    new_data = pd.read_csv(new_data_path)
    logger.info(f"New data from {new_data_path} is loaded")

    model, model_path = load_latest_model(params)
    logger.info(f"Latest model {model} loaded from {model_path}")

    x_new = new_data.drop(
        columns=[params.make_dataset.target_column_name], errors="ignore"
    )

    predictions = model.predict(x_new)
    logger.success(f"Prediction completed for {len(predictions)} samples")

    predictions_path = project_root / params.predictions_path / "predictions_latest.csv"
    os.makedirs(os.path.dirname(predictions_path), exist_ok=True)

    result_df = new_data.copy()
    result_df["predictions"] = predictions
    result_df.to_csv(predictions_path, index=False)
    logger.info(f"Predictions saved to {predictions_path}")


if __name__ == "__main__":
    app()
