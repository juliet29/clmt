# save in an entered path.. can do stuff about creating a new directory later..
from pathlib import Path
import polars as pl


def save_dataframe(path_to_directory: Path, file_name: str, df: pl.DataFrame):
    assert path_to_directory.is_dir(), f"{path_to_directory} needs to be a directory!"
    assert path_to_directory.exists()
    save_path = path_to_directory / file_name
    df.write_csv(save_path)
    print(f"Saved data to {save_path}")
    return df


def read_csv(path: Path, file_name: str | None = None):
    if file_name:
        _path = path / file_name
    else:
        _path = path
    assert _path.exists(), f"{_path} does not exist!"
   
    return pl.read_csv(_path)
