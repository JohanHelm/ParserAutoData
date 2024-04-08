from pathlib import Path
import pickle

WORKDIR: Path = Path(__file__).resolve().parent
output_filepath = WORKDIR.joinpath("out")
filename = f"joined_drom_data.pickle"

def unpickle_drom(filename, data_path):
    fullfilepath = data_path.joinpath(filename)
    with open(fullfilepath, "rb") as file:
        data = pickle.load(file)
    return data

data = unpickle_drom(filename, output_filepath)
print(type(data[0]))
print(data[0])
