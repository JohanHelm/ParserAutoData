from pathlib import Path
import pickle
from datetime import date
import os

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


def move_tables_files_to_smb_share():
    source_dir = output_filepath.joinpath("results/tables")
    dest_dir = Path("/home/user/results/tables")
    # dest_dir = output_filepath.joinpath("user_results/tables")
    inner_dirs = os.listdir(source_dir)
    for dir_file in inner_dirs:
        source_path = source_dir.joinpath(dir_file)
        dest_path = dest_dir.joinpath(dir_file)
        os.replace(source_path, dest_path)
        change_owner_recursive(dest_path)


def results_chown_chgrp(file_path):
    owner = 1000
    group = 1000
    os.chown(file_path, owner, group)

def change_owner_recursive(directory):
    owner = 1000
    group = 1000
    os.chown(directory, owner, group)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            os.chown(file_path, owner, group)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            change_owner_recursive(dir_path)
