from pathlib import Path
from time import perf_counter

from domain.dataproviders.drom import CarsModelsManager
from domain.dataproviders.dvadvornikaru import WindshieldWiperManager
from domain.datatransformers.main_merge2 import ScenarioWorker
from domain.datatransformers.join_drom_data import JoinerDromData
# from domain.datatransformers.merge_markets import DromMarketsMerger
from utils.logging_settings import configure_logger, init_logger
from utils.mark_duration import duration
from utils.models_names_handler import handle_model_names

WORKDIR: Path = Path(__file__).resolve().parent
output_filepath = WORKDIR.joinpath("out")
log_dirpath: Path = WORKDIR.joinpath("logs")

START_DROM = True
JOIN_DROM_FREIGHT_PASSENGER = False
START_PROCESS_2DVORNIKA = False
START_DATATRANSFORMERS = False

START_MODELS_NAMES_HANDLER = False
# MERGE_MARKETS = False


def main():
    logger = init_logger()
    configure_logger(logger, file_path=log_dirpath.joinpath("logfile.log"), rotation=10)
    if START_DROM:
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
        logger.info(f"Full time spent collecting data from https://www.drom.ru/catalog/ is {duration(start, end)}")

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
        logger.info(f"Full time spent collecting data from https://www.drom.ru/catalog/lcv/ is {duration(start, end)}")

    if JOIN_DROM_FREIGHT_PASSENGER:
        jdd = JoinerDromData(output_filepath)
        jdd.execute()

    if START_PROCESS_2DVORNIKA:
        wwm = WindshieldWiperManager(
            parse_mode="lxml",
            output_filepath=output_filepath,
            main_url="https://www.2dvornika.ru/")
        wwm.execute()

    if START_DATATRANSFORMERS:
        sw = ScenarioWorker(data_path=output_filepath)
        sw.execute()
        # sw.training()

    if START_MODELS_NAMES_HANDLER:
        passenger_cmm = CarsModelsManager(
            output_filepath=output_filepath,
            main_url="https://www.drom.ru",
            section="/catalog/",
            parse_mode="lxml",
            vehicle_type="passenger",
        )

        freight_cmm = CarsModelsManager(
            output_filepath=output_filepath,
            main_url="https://www.drom.ru",
            section="/catalog/lcv/",
            parse_mode="lxml",
            vehicle_type="freight",
        )

        wwm = WindshieldWiperManager(
            parse_mode="lxml",
            output_filepath=output_filepath,
            main_url="https://www.2dvornika.ru/"
        )
        handle_model_names(passenger_cmm, freight_cmm, wwm)

    # if MERGE_MARKETS:
    #     dmm = DromMarketsMerger(output_filepath)
    #     dmm.execute()


if __name__ == "__main__":
    main()


# drom sequence
# 1. split raw data production
# 2. split data normalization
# 3. join freight and passenger drom data
# 4. merge markets on joined drom data
# 5. merge on scenarios
