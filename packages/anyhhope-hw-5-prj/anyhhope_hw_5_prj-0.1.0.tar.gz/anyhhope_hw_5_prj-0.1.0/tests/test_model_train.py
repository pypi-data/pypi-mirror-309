from datetime import datetime
from pathlib import Path

from src.config_utils import Params, read_params_from_yaml
from src.dataset import create_dataset
from src.modeling.train import choose_model_and_load, form_save_folders, split_x_y

project_root = Path(__file__).resolve().parent.parent


def load_model():
    """Test the main function creates the datasets."""
    yaml_file = "tests/test_params.yaml"
    params: Params = read_params_from_yaml(project_root / yaml_file)

    model = choose_model_and_load(params)
    assert model


def test_split_x_y():
    """
    Test spliting df on features and target columns
    """
    yaml_file = "tests/test_params.yaml"
    params: Params = read_params_from_yaml(project_root / yaml_file)

    df = create_dataset(params)
    x, y = split_x_y(df, params.make_dataset.target_column_name)

    assert y.shape[0] == 100
    assert len(y.shape) == 1
    assert x.shape[0] == 100
    assert x.shape[1] == 20


def test_form_save_folder():
    """
    Test froming save folder
    """
    yaml_file = "tests/test_params.yaml"
    params: Params = read_params_from_yaml(project_root / yaml_file)

    date_str = datetime.now().strftime("%d.%m_%H:%M:%S")
    model_path = form_save_folders(date_str, params, params.models_path, "model.pkl")

    assert date_str in str(model_path)
