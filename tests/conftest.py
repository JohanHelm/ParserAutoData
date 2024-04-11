import pytest

from utils.dirs_files_checker import unpickle


@pytest.fixture
def raw_freight_citroen_berlingo():
    data = unpickle(filename="freight_raw_drom_data.pickle")
    filtered_brands = filter(lambda x: x.brand_name == "Citroen", data)
    filtered_models = filter(lambda x: x.car_model_name == "Berlingo", filtered_brands)
    return next(filtered_models)


@pytest.fixture
def raw_dvorniki_ac_ace():
    data = unpickle(filename="dvorniki_raw_data.pickle")
    filtered_brands = filter(lambda x: x.brand_name == "ac", data)
    filtered_models = filter(lambda x: x.car_model_name == "ace", filtered_brands)
    return next(filtered_models)


@pytest.fixture
def get_trim_data(raw_dvorniki_ac_ace):
    trim_data = " ".join(raw_dvorniki_ac_ace.raw_data.split())
    return trim_data
