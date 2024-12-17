from typing import Iterator

from bs4 import BeautifulSoup
from loguru import logger
from requests import Response

from domain.models.dromru import DromBrandEntity, DromRawGenerationsEntity, DromModelEntity
from downloader.httpdownloader import RequestsDownloader
from downloader.params import RequestManagerParams
from downloader.retry import RetryManager


class MarketsGroupError(Exception):
    pass


class DromSoupParser:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode
        self.loader: RequestsDownloader = RequestsDownloader(params=RequestManagerParams())
        self.retry_manager: RetryManager = RetryManager()
        self.retry_error = self.retry_manager.retry_error

    def get_and_parse_brands_page(self, url: str, vehicle_type: str) -> Iterator[DromBrandEntity]:
        try:
            for attempt in self.retry_manager.make_retry():
                with attempt:
                    brands_page: Response | None = self.loader.safe_get(url, params=RequestManagerParams())
                    soup = BeautifulSoup(brands_page.text, self.parse_mode)
                    # auto_vendor_table = soup.find(
                    #     'div', attrs={"class": 'css-18clw5c ehmqafe0', "data-ftid": "component_cars-list"})
                    auto_vendor_table = soup.find(
                        'a', attrs={"class": 'css-1q66we5 e4ojbx42', "data-ftid": "component_cars-list-item_hidden-link"})
                    if not auto_vendor_table:
                        logger.info(f"got empty main page")
                    row_brands = auto_vendor_table.find_all("a")
        except self.retry_error:
            logger.warning(f"out of retries with attempts to get correct main page")
        else:
            for brand in row_brands:
                name = brand.text
                href = brand.attrs.get("href")
                brand_data: DromBrandEntity = DromBrandEntity(vehicle_type=vehicle_type,
                                                              brand_name=name,
                                                              link=href, )
                yield brand_data

    def get_and_parse_models_page(self, drom_brand: DromBrandEntity) -> Iterator[DromModelEntity]:
        try:
            for attempt in self.retry_manager.make_retry():
                with attempt:
                    brand_models_page: Response | None = self.loader.safe_get(url=drom_brand.link,
                                                                              params=RequestManagerParams())
                    soup = BeautifulSoup(brand_models_page.text, self.parse_mode)
                    brand_models_table = soup.find(
                        'div', attrs={"class": 'css-18clw5c ehmqafe0', "data-ftid": "component_cars-list"})
                    if not brand_models_table:
                        logger.info(f"got empty {drom_brand.brand_name}")
                    row_models_list = brand_models_table.find_all('a')
        except self.retry_error:
            logger.warning(f"out of retries to find models in brand {drom_brand.brand_name}")
        else:
            for row_model in row_models_list:
                model = row_model.text
                model_href = row_model.attrs.get("href")
                model_data: DromModelEntity = DromModelEntity(vehicle_type=drom_brand.vehicle_type,
                                                              brand_name=drom_brand.brand_name,
                                                              car_model_name=model,
                                                              link=model_href, )
                yield model_data

    def get_and_parse_markets_page(self, drom_model: DromModelEntity) -> DromRawGenerationsEntity | None:
        try:
            for attempt in self.retry_manager.make_retry():
                with attempt:
                    model_markets_page: Response | None = self.loader.safe_get(url=drom_model.link,
                                                                               params=RequestManagerParams())
                    soup = BeautifulSoup(model_markets_page.text, self.parse_mode)
                    markets_group = soup.find_all('div', "css-pyemnz e1ei9t6a4")
                    if not markets_group:
                        logger.warning(
                            f"not found data {drom_model.brand_name} {drom_model.car_model_name} in this attempt")
                        raise MarketsGroupError()
        except MarketsGroupError:
            logger.warning(f"out of retries to find generations in brand {drom_model.brand_name} "
                           f"for model {drom_model.car_model_name}")
        else:
            return DromRawGenerationsEntity(vehicle_type=drom_model.vehicle_type,
                                            brand_name=drom_model.brand_name,
                                            car_model_name=drom_model.car_model_name,
                                            link=drom_model.link,
                                            raw_markets_group=model_markets_page.text)

    def get_markets_group_out_of_drom_raw_model(self, drom_raw_generations_entity: DromRawGenerationsEntity):
        model_markets_page_text = drom_raw_generations_entity.raw_markets_group
        soup = BeautifulSoup(model_markets_page_text, self.parse_mode)
        markets_group = soup.find_all('div', "css-pyemnz e1ei9t6a4")
        return markets_group
