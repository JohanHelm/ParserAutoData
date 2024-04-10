import pytest

from normalizer.drom_norm import *
from normalizer.dvadvornikaru import *
from normalizer.proper_names import ProperNames


##  Tests for drom normalizer
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


##  Tests for dvorniki normalizer
def test_extract_data(raw_dvorniki_ac_ace, get_trim_data):
    assert extract_data(get_trim_data) == AdditionalModelData(
        sales_start_year=1996,
        sales_end_year=2005,
        body_type="седан",
        restyling=False,
        restyling_num=0,
        first_generation=1,
        last_generation=1,
        codes="No data",
    )


def test_extract_brush_data(raw_dvorniki_ac_ace):
    assert extract_brush_data(raw_dvorniki_ac_ace.raw_data_brush) == BrushModelData(
        attach_type="крючок",
        left_brush_size=500,
        right_brush_size=500,
        back_brush_size=0,
        nozzles=False,
        washer=False,
        heater=False,
        info="No data")


def test_year_extractor(get_trim_data):
    assert year_extractor(get_trim_data) == (1996, 2005)


def test_body_type_extractor(get_trim_data):
    assert body_type_extractor(get_trim_data) == "седан"


def test_restyling_num_extractor(get_trim_data):
    assert restyling_num_extractor(get_trim_data) == 0


def test_restyling_extractor(get_trim_data):
    assert not restyling_extractor(get_trim_data)


def test_generation_extractor(get_trim_data):
    assert generation_extractor(get_trim_data) == (1, 1)


def test_codes_extractor(get_trim_data):
    assert codes_extractor(get_trim_data) == "No data"


def test_brush_attach_type_extractor_line(raw_dvorniki_ac_ace):
    assert brush_attach_type_extractor_line(raw_dvorniki_ac_ace.raw_data_brush) == "крючок"


def test_info_extractor(raw_dvorniki_ac_ace):
    assert info_extractor(raw_dvorniki_ac_ace.raw_data_brush) == "No data"


def test_brush_front_size_extractor(raw_dvorniki_ac_ace):
    assert brush_front_size_extractor(raw_dvorniki_ac_ace.raw_data_brush) == (500, 500)


def test_brush_back_extractor(raw_dvorniki_ac_ace):
    assert brush_back_extractor(raw_dvorniki_ac_ace.raw_data_brush) == 0


def test_nozzles_extractor(raw_dvorniki_ac_ace):
    assert not nozzles_extractor(raw_dvorniki_ac_ace.raw_data_brush)


def test_washer_extractor(raw_dvorniki_ac_ace):
    assert not washer_extractor(raw_dvorniki_ac_ace.raw_data_brush)


def test_heater_extractor(raw_dvorniki_ac_ace):
    assert not heater_extractor(raw_dvorniki_ac_ace.raw_data_brush)
