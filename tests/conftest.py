import pytest
from pathlib import Path
import pickle

from utils.pickle_checker import unpickle


@pytest.fixture
def raw_freight_citroen_berlingo():
    data = unpickle(filename="freight_raw_drom_data.pickle")
    filtered_brands = filter(lambda x: x.brand_name == "Citroen", data)
    filtered_models = filter(lambda x: x.car_model_name == "Berlingo", filtered_brands)
    return next(filtered_models)
