import json
import os
import pickle
from datetime import datetime
from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

from src.config_utils import ModelType, Params, project_root, read_params_from_yaml

app = typer.Typer()


def choose_model_and_load(params: Params):
    """
    Load model by model_type
    """
    if params.train_params.model_type == ModelType.LOGISTIC_REGRESSION:
        model = LogisticRegression(
            multi_class=params.train_params.logistic_regression.multi_class,
            solver=params.train_params.logistic_regression.solver,
            max_iter=params.train_params.logistic_regression.max_iter,
            random_state=params.random_state,
        )
    elif params.train_params.model_type == ModelType.RANDOM_FOREST:
        model = RandomForestClassifier(
            n_estimators=params.train_params.random_forest.n_estimators,
            max_depth=params.train_params.random_forest.max_depth,
            random_state=params.random_state,
        )
    elif params.train_params.model_type == ModelType.DECISION_TREE:
        model = DecisionTreeClassifier(
            criterion=params.train_params.decision_tree.criterion,
            max_depth=params.train_params.decision_tree.max_depth,
            random_state=params.random_state,
        )
    return model


def split_x_y(
    df: pd.DataFrame, target_column_name: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split on fetures column and targer
    """
    y = df[target_column_name]
    x = df.drop(target_column_name, axis=1)
    return x, y


def form_save_folders(date_str: str, params: Params, orig_path: str, filename: str):
    """
    Form correct output folder with different folders for models
    """
    folder = project_root / orig_path / str(params.train_params.model_type.value)
    os.makedirs(folder, exist_ok=True)
    model_filename = filename.split(".")[0] + f"_{date_str}." + filename.split(".")[1]
    return folder / model_filename


@app.command()
def main(
    params_path: Path,
):
    """
    Train model for multiclassification task
    """
    params = read_params_from_yaml(params_path)

    df_train = pd.read_csv(project_root / params.make_dataset.train_data_path)
    df_test = pd.read_csv(project_root / params.make_dataset.test_data_path)

    x_train, y_train = split_x_y(df_train, params.make_dataset.target_column_name)
    x_test, y_test = split_x_y(df_test, params.make_dataset.target_column_name)
    logger.info("Data is loaded")

    model = choose_model_and_load(params)
    logger.info(f"Model {model} is initialized")

    model.fit(x_train, y_train)
    logger.success("Finished training")

    date_str = datetime.now().strftime("%d.%m_%H:%M:%S")

    model_path = form_save_folders(date_str, params, params.models_path, "model.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    logger.info(f"Model is saved to {project_root / params.models_path}")

    y_pred = model.predict(x_test)

    report = classification_report(y_test, y_pred, output_dict=True)

    report_path = form_save_folders(
        date_str, params, params.report_path, "classification_report.json"
    )
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as json_file:
        json.dump(report, json_file, indent=4)


if __name__ == "__main__":
    app()
