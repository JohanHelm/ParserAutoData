import re

from domain.models.dvadvornikaru import AdditionalModelData, BrushModelData, DvaDvornikaModelRaw, DvaDvornikaDataNorm
from .proper_names import ProperNames
# from normalizer.proper_names import ProperNames


def year_extractor(data):
    p = re.compile(r"(?P<year_start>\d{4})-(?P<year_end>\d{4}).")
    m = p.search(data)
    if m is not None:
        res = m.groupdict()
        return int(res.get("year_start")), int(res.get("year_end"))
    else:
        return 0, 0


def body_type_extractor(data):
    for body_type_key, body_type_value in ProperNames.BODY_TYPES.value.items():
        if body_type_key.lower() in data.lower():
            return ProperNames.BODY_TYPES.value[body_type_key]
    return data


def restyling_num_extractor(data):
    if ProperNames.IS_RESTYLING.value in data:
        p = re.compile(r"((?P<idx>\d?)\sрестайлинг|рестайлинг)")
        m = p.search(data)
        if m is not None:
            res = m.groupdict()
            if res.get("idx"):
                return int(res.get("idx"))
    else:
        return 0


def restyling_extractor(data):
    if ProperNames.IS_RESTYLING.value in data:
        return True
    else:
        return False


def generation_extractor(data):
    p = re.compile(r".((?P<s1>\d{1})|(?P<s2>\d{1})-(?P<s3>\d{1}))\s(поколение|пок.)")
    m = p.search(data)
    if m is not None:
        res = m.groupdict()
        if res.get("s1"):
            return (int(res.get("s1")), 1)
        else:
            return (int(res.get("s2")), int(res.get("s3")))
    else:
        return 1, 1


def codes_extractor(data):
    p = re.compile(r"\[(?P<codes>.*?)\]")
    m = p.search(data)
    if m is not None:
        res = m.groupdict()
        if res.get("codes"):
            return res.get("codes")
    return "No data"


def brush_attach_type_extractor_line(data):
    lines = data.splitlines()
    for line in lines:
        if "тип крепления" in line.lower():
            res = line.split("-", 1)
            raw_str = res[-1]
            for attach_type in ProperNames.BRUSH_ATTACH_TYPES.value.keys():
                if attach_type in raw_str:
                    return ProperNames.BRUSH_ATTACH_TYPES.value[attach_type]
    return "No data"


def info_extractor(data):
    lines = data.splitlines()
    for line in lines:
        if "информация о дворниках" in line.lower():
            return line
    return "No data"


def brush_attach_type_extractor(data):
    for attach_type in ProperNames.BRUSH_ATTACH_TYPES.value:
        if attach_type in data:
            return attach_type


def brush_front_size_extractor(data):
    p = re.compile(r".*(?P<left>\d{3})\sмм\sи\s(?P<right>\d{3}).*")
    m = p.search(data)
    if m is not None:
        res = m.groupdict()
        return (int(res.get("left")), int(res.get("right")))
    else:
        return (0, 0)


def one_front_brush_extractor(data):
    p = re.compile(r".*(?P<left>\d{3})\sмм.*")
    m = p.search(data)
    if m is not None:
        res = m.groupdict()
        return int(res.get("left"))
    else:
        return 0


def brush_back_extractor(data):
    p = re.compile(r"задняя\s(?P<back>\d{3})\sмм")
    m = p.search(data)
    if m is not None:
        res = m.groupdict()
        return int(res.get("back"))
    else:
        return 0


def nozzles_extractor(data):
    return "форсунк" in data.lower()


def washer_extractor(data):
    return "омыват" in data.lower()


def heater_extractor(data):
    return "подогре" in data.lower()


def extract_data(data) -> AdditionalModelData:
    sales_start_year, sales_end_year = year_extractor(data)
    body_type: str = body_type_extractor(data)
    restyling: bool = restyling_extractor(data)
    restyling_num: int = restyling_num_extractor(data)
    first_gen, last_gen = generation_extractor(data)
    codes = codes_extractor(data)
    additional_data = AdditionalModelData(
        sales_start_year=sales_start_year,
        sales_end_year=sales_end_year,
        body_type=body_type,
        restyling=restyling,
        restyling_num=restyling_num,
        first_generation=first_gen,
        last_generation=last_gen,
        codes=codes,
    )
    return additional_data


def extract_brush_data(data) -> BrushModelData:
    brush_attach_type = brush_attach_type_extractor_line(data)
    (left, right) = brush_front_size_extractor(data)
    if (left, right) == (0, 0):
        left = one_front_brush_extractor(data)
    back = brush_back_extractor(data)
    nozzles = nozzles_extractor(data)
    washer = washer_extractor(data)
    heater = heater_extractor(data)
    info = info_extractor(data)
    brush_model = BrushModelData(
        attach_type=brush_attach_type,
        left_brush_size=left,
        right_brush_size=right,
        back_brush_size=back,
        nozzles=nozzles,
        washer=washer,
        heater=heater,
        info=info,
    )
    return brush_model

def normalize_brand(raw_data_item: DvaDvornikaModelRaw) -> str:
    raw_brand_name = raw_data_item.brand_name.lower().strip()
    proper_brand_names = ProperNames.BRANDS.value
    brand_name = proper_brand_names.get(raw_brand_name, raw_brand_name)
    return brand_name


# def normalize_model(raw_data_item: DvaDvornikaModelRaw) -> str:
#     norm_brand_name = normalize_brand(raw_data_item)
#     raw_model_name = raw_data_item.car_model_name.lower().strip()
#
#     car_model_name = raw_model_name
#     return car_model_name

def normalize_bad_models(partially_norm: DvaDvornikaDataNorm) -> str:
    brand = partially_norm.norm_brand_name
    bad_name = partially_norm.norm_model_name
    brand_models_dict = ProperNames.MODELS.value.get(brand, {})
    good_name = brand_models_dict.get(bad_name, bad_name)
    partially_norm.norm_model_name = good_name


def normalize_raw_dvorniki_data(raw_data_item: DvaDvornikaModelRaw) -> DvaDvornikaDataNorm:
    trim_data = " ".join(raw_data_item.raw_data.split())
    additional_data: AdditionalModelData = extract_data(trim_data)
    brush_model: BrushModelData = extract_brush_data(raw_data_item.raw_data_brush)
    normalized_dvorniki = DvaDvornikaDataNorm(
        norm_brand_name=normalize_brand(raw_data_item),
        norm_model_name=raw_data_item.car_model_name.lower().strip(),
        start_date=additional_data.sales_start_year,
        end_date=additional_data.sales_end_year,
        body_type=additional_data.body_type,
        body_model=additional_data.codes,
        generation=additional_data.first_generation,
        restyling=additional_data.restyling,
        attach_type=brush_model.attach_type,
        size_1=brush_model.right_brush_size,
        size2=brush_model.left_brush_size,
        size_back=brush_model.back_brush_size,
        washer=brush_model.washer or brush_model.nozzles,
        heater=brush_model.heater,
        info=brush_model.info,
        link=raw_data_item.link
    )
    return normalized_dvorniki
