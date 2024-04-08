from datetime import date, datetime
from typing import Iterator

from domain.models.dromru import DromGenerationEntity, DromRawGenerationsEntity
from .proper_names import ProperNames


def create_generation(car_model, drom_raw_model: DromRawGenerationsEntity, market) -> DromGenerationEntity:
    brand_name = normalize_brand(drom_raw_model)
    car_model_name = normalize_model(brand_name, drom_raw_model)
    car_data = car_model.find("a")
    short_car_href = car_data.attrs.get("href")
    car_text1 = car_data.find("span", attrs={"class": "e1adi9cz0",
                                             "data-ftid": "component_article_caption"}).text.split("\n")
    raw_start_date = car_text1[1].split(" - ")[0].strip()
    norm_start_date = normalize_date(raw_start_date)
    raw_end_date = car_text1[1].split(" - ")[1].strip()
    norm_end_date = normalize_date(raw_end_date)
    body_model_primary = normalize_body_model_primary(car_text1[0])
    car_text2_block = car_data.find("div", attrs={"data-ftid": "component_article_extended-info"})
    raw_generation_restyling = car_text2_block.find("div").text
    generation, restyling = normalize_generation_restyling(raw_generation_restyling)
    car_text2_2_block = [item.text for item in car_text2_block.find_all("div", "e1rlzkvp0")]
    body_model_secondary = car_text2_2_block[0].lower() if car_text2_2_block[0] else "no data"
    raw_body_type = car_text2_2_block[1].lower().strip() if car_text2_2_block[1] else "no data"
    proper_body_type = ProperNames.BODY_TYPES.value
    body_type = proper_body_type.get(raw_body_type, raw_body_type)

    generation_data = DromGenerationEntity(vehicle_type=drom_raw_model.vehicle_type,
                                           brand_name=brand_name,
                                           car_model_name=car_model_name,
                                           link=drom_raw_model.link,
                                           photo_link=f"{drom_raw_model.link}{short_car_href}/",
                                           market=market.lower().strip(),
                                           generation=generation,
                                           restyling=restyling,
                                           start_date=norm_start_date,
                                           end_date=norm_end_date,
                                           body_model_primary=body_model_primary,
                                           body_model_secondary=body_model_secondary,
                                           body_type=body_type)
    return generation_data


def normalize_brand(drom_raw_model: DromRawGenerationsEntity) -> str:
    raw_brand_name = drom_raw_model.brand_name.lower().strip()
    proper_brand_names = ProperNames.BRANDS.value
    brand_name = proper_brand_names.get(raw_brand_name, raw_brand_name)
    return brand_name

def normalize_model(brand_name: str, drom_raw_model: DromRawGenerationsEntity) -> str:
    raw_model_name = drom_raw_model.car_model_name.lower().strip()

    car_model_name = raw_model_name
    return car_model_name


def normalize_date(raw_date: str) -> int:
    pattern = "%m.%Y"
    if raw_date.isdigit():
        pattern = "%Y"
    try:
        result_date = datetime.strptime(raw_date, pattern).date()
    except ValueError:
        result_date = date.today()
    return result_date.year


def normalize_body_model_primary(raw_body_model_primary):
    body_model_primary = "no data"
    if "(" in raw_body_model_primary and ")" in raw_body_model_primary:
        body_model_primary = \
            raw_body_model_primary[raw_body_model_primary.find("("):raw_body_model_primary.find(")") + 1].strip('()')
    return body_model_primary.lower()


def normalize_generation_restyling(raw_generation_restyling: str) -> tuple[int, int]:
    if raw_generation_restyling:
        raw_generation_restyling = raw_generation_restyling.split(', ')
        if raw_generation_restyling[0]:
            generation = int(raw_generation_restyling[0].split()[0])
        else:
            generation = 1
        if len(raw_generation_restyling) > 1:
            raw_restyling = raw_generation_restyling[1]
            if raw_restyling and raw_restyling.isalpha():
                restyling = 1
            elif raw_restyling and not raw_restyling.isalpha():
                restyling = int(raw_restyling.split("-")[0])
        else:
            restyling = 0
    else:
        generation, restyling = 1, 0
    return generation, restyling


def normalize_drom_raw_data(drom_raw_model: DromRawGenerationsEntity, markets_group) -> Iterator[DromGenerationEntity]:
    for group in markets_group:
        market = group.find("div", "css-112idg0 e1ei9t6a3").get("id")
        market_models = group.find_all("div", attrs={"data-ga-stats-name": "generations_outlet_item"})
        for car_model in market_models:
            generation_data = create_generation(car_model, drom_raw_model, market)
            yield generation_data
