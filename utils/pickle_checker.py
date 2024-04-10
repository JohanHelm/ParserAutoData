from pathlib import Path
import pickle

WORKDIR: Path = Path(__file__).resolve().parent.parent
output_filepath = WORKDIR.joinpath("out")
# filename = f"freight_raw_drom_data.pickle"
filename = "dvorniki_raw_data.pickle"


def unpickle(filename=filename, data_path=output_filepath):
    fullfilepath = data_path.joinpath(filename)
    with open(fullfilepath, "rb") as file:
        data = pickle.load(file)
    return data

data = unpickle(filename, output_filepath)
# print(type(data[0]))
print(data[0])
filtered_brands = filter(lambda x: x.brand_name == "ac", data)
filtered_models = filter(lambda x: x.car_model_name == "ace", filtered_brands)
# print(len(tuple(filtered_models)))

raw_data_item = next(filtered_models)
trim_data = " ".join(raw_data_item.raw_data.split())
print(trim_data)

