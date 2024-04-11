from pathlib import Path
import pickle
from datetime import date

from settings import output_filepath



def create_results_tables_dir() -> Path:
    directory_name = output_filepath.joinpath(f"results/tables/{date.today()}")
    new_directory = Path(directory_name)
    new_directory.mkdir(exist_ok=True, parents=True)
    return new_directory

def create_pickle_dir() -> Path:
    directory_name = output_filepath.joinpath("pickles")
    new_directory = Path(directory_name)
    new_directory.mkdir(exist_ok=True)
    return new_directory


def unpickle(filename, data_path=output_filepath):
    fullfilepath = data_path.joinpath(f"pickles/{filename}")
    with open(fullfilepath, "rb") as file:
        data = pickle.load(file)
    return data
