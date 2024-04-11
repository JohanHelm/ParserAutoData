import pickle
from parser.dromru.html_parser import DromSoupParser
from pathlib import Path
from tqdm import tqdm


from loguru import logger

from domain.models.dromru import (
    DromBrandEntity,
    DromGenerationEntity,
    DromModelEntity,
    DromRawGenerationsEntity,
)
from downloader.retry import RetryManager
from filewriter.excel import ExcelWriter
from filewriter.params import DromNormParams
from normalizer.drom_norm import normalize_drom_raw_data
from utils.dirs_files_checker import create_results_tables_dir, create_pickle_dir


class CarsModelsManager:
    def __init__(
        self,
        output_filepath: Path,
        main_url: str,
        section: str,
        parse_mode: str,
        vehicle_type: str,
    ) -> None:
        self.drom_catalog_url = f"{main_url}{section}"
        self.parser: DromSoupParser = DromSoupParser(parse_mode)
        self.output_filepath = output_filepath
        self.drom_model: DromModelEntity = DromModelEntity()
        self.drom_brand: DromBrandEntity = DromBrandEntity()

        self.retry_manager: RetryManager = RetryManager()
        self.raw_drom_data: list[DromRawGenerationsEntity] = []
        self.drom_data: list[DromGenerationEntity] = []
        self.vehicle_type = vehicle_type

    def process_all_brands(self) -> None:
        brands_iterator = self.parser.get_and_parse_brands_page(
            url=self.drom_catalog_url, vehicle_type=self.vehicle_type
        )
        for brand in brands_iterator:
            self.drom_brand = brand
            self.process_one_brand()
            logger.info(f"{self.drom_brand.brand_name} is saved")

    def process_one_brand(self) -> None:
        models_iterator = self.parser.get_and_parse_models_page(self.drom_brand)
        models_amount = 0
        for model in models_iterator:
            self.drom_model = model
            self.process_one_model()
            models_amount += 1
        logger.info(f"Brand {self.drom_brand.brand_name} got {models_amount} models.")

    def process_one_model(self) -> None:
        drom_raw_generations_entity = self.parser.get_and_parse_markets_page(self.drom_model)
        if drom_raw_generations_entity:
            self.raw_drom_data.append(drom_raw_generations_entity)

    def pickle_raw_drom(self):
        new_directory = create_pickle_dir()
        filename = f"{self.vehicle_type}_raw_drom_data.pickle"
        fullfilepath = new_directory.joinpath(filename)
        with open(fullfilepath, "wb") as file:
            pickle.dump(self.raw_drom_data, file)
            logger.info(f"save binary file {fullfilepath}")

    def unpickle_raw_drom(self):
        filename = f"{self.vehicle_type}_raw_drom_data.pickle"
        fullfilepath = self.output_filepath.joinpath(f"pickles/{filename}")
        if Path.exists(fullfilepath):
            with open(fullfilepath, "rb") as file:
                logger.info(f"open binary file {fullfilepath}")
                self.raw_drom_data = pickle.load(file)

    def pickle_norm_drom(self):
        new_directory = create_pickle_dir()
        filename = f"{self.vehicle_type}_norm_drom_data.pickle"
        fullfilepath = new_directory.joinpath(filename)
        with open(fullfilepath, "wb") as file:
            pickle.dump(self.drom_data, file)
            logger.info(f"save binary file {fullfilepath}")

    def unpickle_norm_drom(self):
        filename = f"{self.vehicle_type}_norm_drom_data.pickle"
        fullfilepath = self.output_filepath.joinpath(f"pickles/{filename}")
        if Path.exists(fullfilepath):
            with open(fullfilepath, "rb") as file:
                self.drom_data = pickle.load(file)
        logger.info(f"open binary file {fullfilepath}")

    def norm_drom_brands(self):
        brands = set()
        for entry in self.drom_data:
            brands.add(entry.brand_name)
        return sorted(brands)

    def norm_drom_models(self, brand_name: str):
        models = set()
        filtered_by_brand = filter(lambda x: x.brand_name == brand_name, self.drom_data)
        for entry in filtered_by_brand:
            models.add(entry.car_model_name)
        return sorted(models)

    def normalize_markets_data(self):
        while self.raw_drom_data:
            drom_raw_generations_entity = self.raw_drom_data.pop(0)
            markets_group = self.parser.get_markets_group_out_of_drom_raw_model(drom_raw_generations_entity)
            generations_iterator = normalize_drom_raw_data(drom_raw_generations_entity, markets_group)
            generations_amount = 0
            for generation in generations_iterator:
                # self.drom_data.append(generation)
                self.compare_new_with_old(generation)
                generations_amount += 1
            logger.info(
                f"Brand {drom_raw_generations_entity.brand_name}, model {drom_raw_generations_entity.car_model_name} "
                f"got {generations_amount} generations"
            )
        logger.info(
            f"All raw {self.vehicle_type} from {self.drom_catalog_url} normalized"
        )

    def save_normalized_data_to_excel(self):
        new_directory = create_results_tables_dir()
        filename = f"{self.vehicle_type}_norm_drom_data.xlsx"
        fullfilepath = new_directory.joinpath(filename)
        writer: ExcelWriter = ExcelWriter(fullfilepath, DromNormParams())

        logger.info(
            f"Started to write excel with {self.vehicle_type} from {self.drom_catalog_url}"
        )
        # tqdm_params = {
        #     'desc': 'Write to excel',
        #     'total': len(self.drom_data),
        #     'miniters': 1,
        #     'unit': 'generation',
        #     'unit_scale': True, }
        # for generation in tqdm(self.drom_data, **tqdm_params):
        for generation in self.drom_data:
            writer.write_data_row(generation)
        writer.workbook.close()
        logger.info(
            f"Finished to write excel with {self.vehicle_type} from {self.drom_catalog_url}"
        )

    def compare_new_with_old(self, new_car_data: DromGenerationEntity):
        old_cars_data = tuple(filter(lambda x: x.photo_link == new_car_data.photo_link, self.drom_data))
        len_cars_items = len(old_cars_data)
        if len_cars_items > 1:
            print('Somehow there is more then one instance for one car')
        elif len_cars_items == 0:
            new_car_data.status = "новый"
            self.drom_data.append(new_car_data)
        elif len_cars_items == 1:
            if tuple(old_cars_data[0].model_dump().values())[:12] == tuple(new_car_data.model_dump().values())[:12]:
                old_cars_data[0].status = "старый"
                if not old_cars_data[0].previous_scan_date and old_cars_data[0].current_scan_date:
                    old_cars_data[0].previous_scan_date = old_cars_data[0].current_scan_date
                    old_cars_data[0].current_scan_date = None
            else:
                position = self.drom_data.index(old_cars_data[0])

                new_car_data.status = "изменён"
                new_car_data.old_brand = old_cars_data[0].brand_name
                new_car_data.old_model = old_cars_data[0].car_model_name
                new_car_data.old_market = old_cars_data[0].market
                new_car_data.old_generation = old_cars_data[0].generation
                new_car_data.old_restyling = old_cars_data[0].restyling
                new_car_data.old_start_date = old_cars_data[0].start_date
                new_car_data.old_end_date = old_cars_data[0].end_date
                new_car_data.old_body_model_primary = old_cars_data[0].body_model_primary
                new_car_data.old_body_model_secondary = old_cars_data[0].body_model_secondary
                new_car_data.old_body_type = old_cars_data[0].body_type

                self.drom_data[position] = new_car_data

    def execute(self):
        self.process_all_brands()
        self.pickle_raw_drom()
        self.unpickle_raw_drom()
        self.unpickle_norm_drom()
        self.normalize_markets_data()
        self.pickle_norm_drom()
        self.unpickle_norm_drom()
        self.save_normalized_data_to_excel()

