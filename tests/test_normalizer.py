import pytest
from datetime import date

from normalizer.proper_names import ProperNames
from normalizer.drom_norm import \
    normalize_generation_restyling, \
    normalize_brand, \
    normalize_model, \
    normalize_date, \
    normalize_body_model_primary



@pytest.mark.parametrize("item, key, expected_result",
                         [("BRANDS", "samand / iran khodro / ikco", "iran khodro"),
                          ("BRUSH_ATTACH_TYPES", "специальная кнопка GWB072", "специальное, кнопка"),
                          ("BODY_TYPES", "1971-1994 мыльница [968]", "седан"),
                          ("MODELS", "газ", {'зим': '12 зим'})])
def test_proper_names(item, key, expected_result):
    assert ProperNames._member_map_[item].value[key] == expected_result


@pytest.mark.parametrize("raw_generation_restyling, expected_result",
                         [("1 поколение", (1, 0)),
                          ("2 поколение, рестайлинг", (2, 1)),
                          ("3 поколение, 2-й рестайлинг", (3, 2))])
def test_normalize_generation_restyling(raw_generation_restyling, expected_result):
    assert normalize_generation_restyling(raw_generation_restyling) == expected_result


def test_normalize_brand(raw_freight_citroen_berlingo):
    assert normalize_brand(raw_freight_citroen_berlingo) == "citroen"

def test_normalize_model(raw_freight_citroen_berlingo):
    assert normalize_model(raw_freight_citroen_berlingo) == "berlingo"


@pytest.mark.parametrize("raw_date, expected_result",
                         [("10.1994", 1994),
                          ("01.2015", 2015),
                          ("н.в.", date.today().year)])
def test_normalize_date(raw_date, expected_result):
    assert normalize_date(raw_date) == expected_result


@pytest.mark.parametrize("car_text_block1, expected_result",
                         [("Audi e-tron", "no data"),
                          ("Audi SQ8 (4MN)", "4mn")])
def test_normalize_body_model_primary(car_text_block1, expected_result):
    assert normalize_body_model_primary(car_text_block1) == expected_result

