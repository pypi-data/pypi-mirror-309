import pathlib
from importlib import resources
import pandas as pd


def get_instances_metadata_path() -> pathlib.Path:
    """Get the path to the instances metadata CSV file."""
    return resources.files("miplib_benchmark") / "data" / "instances.csv"

def load_instances_metadata() -> pd.DataFrame:
    """Load the instances metadata as a pandas DataFrame."""
    path = get_instances_metadata_path()
    df = pd.read_csv(path)
    return df

def get_all_instance_names() -> list[str]:
    """Get all instance names."""
    metadata = load_instances_metadata()
    return metadata["InstanceInst."].tolist()
