from pathlib import Path

from src.config_utils import Params, read_params_from_yaml

project_root = Path(__file__).resolve().parent.parent


def test_read_params_from_yaml():
    """Test reading parameters from a YAML file."""
    yaml_file = "tests/test_params.yaml"
    params: Params = read_params_from_yaml(project_root / yaml_file)

    assert params.make_dataset.n_samples == 100
    assert params.make_dataset.n_features == 20
    assert params.make_dataset.n_informative == 10
    assert params.make_dataset.n_redundant == 5
    assert params.make_dataset.n_classes == 3
    assert params.make_dataset.shuffle is True
    assert params.make_dataset.target_column_name == "target"
    assert params.train_params.model_type.value == "logistic_regression"
    assert params.train_params.logistic_regression.multi_class == "multinomial"
    assert params.train_params.logistic_regression.solver == "lbfgs"
    assert params.train_params.logistic_regression.max_iter == 500
    assert params.report_path == "reports"
    assert params.models_path == "models"
    assert params.random_state == 14
