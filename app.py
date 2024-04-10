from time import perf_counter
from loguru import logger

from domain.dataproviders.drom import CarsModelsManager
from domain.dataproviders.dvadvornikaru import WindshieldWiperManager
from utils.mark_duration import duration
from settings import output_filepath


class MainAppManager:
    def __init__(self, start_passenger_drom: bool, start_freight_drom: bool, start_dvorniki: bool):
        self.start_passenger_drom = start_passenger_drom
        self.start_freight_drom = start_freight_drom
        self.start_dvorniki = start_dvorniki

    def start_main_app(self):
        if self.start_passenger_drom:
            passenger_cars_models_manager = CarsModelsManager(
                output_filepath=output_filepath,
                main_url="https://www.drom.ru",
                section="/catalog/",
                parse_mode="lxml",
                vehicle_type="passenger",
            )
            start = perf_counter()
            passenger_cars_models_manager.execute()
            end = perf_counter()
            logger.info(
                f"Full time spent collecting data from https://www.drom.ru/catalog/ is {duration(start, end)}")

        if self.start_freight_drom:
            freight_cars_models_manager = CarsModelsManager(
                output_filepath=output_filepath,
                main_url="https://www.drom.ru",
                section="/catalog/lcv/",
                parse_mode="lxml",
                vehicle_type="freight",
            )
            start = perf_counter()
            freight_cars_models_manager.execute()
            end = perf_counter()
            logger.info(
                f"Full time spent collecting data from https://www.drom.ru/catalog/lcv/ is {duration(start, end)}")

        if self.start_dvorniki:
            wwm = WindshieldWiperManager(
                parse_mode="lxml",
                output_filepath=output_filepath,
                main_url="https://www.2dvornika.ru/")
            start = perf_counter()
            wwm.execute()
            end = perf_counter()
            logger.info(f"Full time spent collecting data from https://www.2dvornika.ru/ is {duration(start, end)}")
