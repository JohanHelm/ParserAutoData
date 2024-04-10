from pathlib import Path
import pickle

WORKDIR: Path = Path(__file__).resolve().parent.parent
output_filepath = WORKDIR.joinpath("out")
filename = f"freight_raw_drom_data.pickle"


def unpickle(filename=filename, data_path=output_filepath):
    fullfilepath = data_path.joinpath(filename)
    with open(fullfilepath, "rb") as file:
        data = pickle.load(file)
    return data

data = unpickle(filename, output_filepath)
print(type(data[0]))
print(data[0])

