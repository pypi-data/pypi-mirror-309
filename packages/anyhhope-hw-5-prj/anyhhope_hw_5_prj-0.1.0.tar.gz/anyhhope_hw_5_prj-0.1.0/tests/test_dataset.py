from pathlib import Path

from src.config_utils import Params, read_params_from_yaml
from src.dataset import create_dataset

project_root = Path(__file__).resolve().parent.parent


def test_main_creates_datasets():
    """Test the main function creates the datasets."""
    yaml_file = "tests/test_params.yaml"
    params: Params = read_params_from_yaml(project_root / yaml_file)

    df = create_dataset(params)
    assert df.shape[0] == 100
