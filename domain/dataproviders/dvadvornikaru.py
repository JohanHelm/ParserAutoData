import pickle
from pathlib import Path
from loguru import logger
from requests import Response

from domain.models.dvadvornikaru import DvaDvornikaBrand, DvaDvornikaModelRaw, DvaDvornikaDataNorm
from downloader.httpdownloader import RequestsDownloader
from downloader.params import RequestManagerParams
from normalizer.dvadvornikaru import normalize_raw_dvorniki_data, normalize_bad_models
from parser.twodvornikaru.htmlparser import BsParser
from filewriter.excel import ExcelWriter
from filewriter.params import DvornikiNormParams
from utils.dirs_files_checker import create_results_tables_dir, create_pickle_dir


class WindshieldWiperManager:
    def __init__(
            self,
            parse_mode: str,
            output_filepath: Path,
            main_url: str,
    ) -> None:
        self.loader: RequestsDownloader = RequestsDownloader(params=RequestManagerParams())
        self.parser: BsParser = BsParser(parse_mode)
        self.output_filepath = output_filepath
        self.main_url = main_url
        self.dvorniki_brands_list: list[DvaDvornikaBrand] = []
        self.dvorniki_models_list_raw: list[DvaDvornikaModelRaw] = []
        self.dvorniki_data_norm_list: list[DvaDvornikaDataNorm] = []
        logger.info("Init Windshield Wiper manager")

    def process_main_data(self) -> None:
        logger.info("proceed main page")
        main_page_html: Response | None = self.loader.safe_get(url=self.main_url, params=RequestManagerParams())
        self.dvorniki_brands_list = self.parser.parse_main_page(start_page_data=main_page_html)
        self.process_auto_mark_data()
        logger.info(f"{self.main_url} main page is saved")

    def process_auto_mark_data(self):
        logger.info(f"proceed models data for {self.main_url}")
        for brand in self.dvorniki_brands_list:
            mark_page_html: Response | None = self.loader.safe_get(url=brand.link, params=RequestManagerParams())
            models = self.parser.parse_mark_page(mark_page_html, brand)

            self.dvorniki_models_list_raw.extend(models)
            logger.info(f"Add {brand.brand_name}")
        self.process_auto_mark_brush_data()

    def process_auto_mark_brush_data(self):
        for model in self.dvorniki_models_list_raw:
            logger.info(f"proceed model brush data for {model.brand_name} {model.car_model_name}")
            brush_page_html: Response | None = self.loader.safe_get(url=model.link, params=RequestManagerParams())
            brush_data = self.parser.parse_model_brush_data(brush_page_html)
            model.raw_data_brush = brush_data

    def pickle_raw_dvorniki(self):
        new_directory = create_pickle_dir()
        filename = f"dvorniki_raw_data.pickle"
        fullfilepath = new_directory.joinpath(filename)
        with open(fullfilepath, "wb") as file:
            pickle.dump(self.dvorniki_models_list_raw, file)
            logger.info(f"save binary file {fullfilepath}")

    def unpickle_raw_dvorniki(self):
        filename = f"dvorniki_raw_data.pickle"
        fullfilepath = self.output_filepath.joinpath(f"pickles/{filename}")
        if Path.exists(fullfilepath):
            with open(fullfilepath, "rb") as file:
                logger.info(f"open binary file {fullfilepath}")
                self.dvorniki_models_list_raw = pickle.load(file)

    def normalize_raw_dvorniki(self):
        for raw_dvorniki_data in self.dvorniki_models_list_raw:
            self.compare_new_with_old(normalize_raw_dvorniki_data(raw_dvorniki_data))
            logger.info(
                f"normalize dvorniki data for {raw_dvorniki_data.brand_name} {raw_dvorniki_data.car_model_name}")

    def compare_new_with_old(self, new_brush_data: DvaDvornikaDataNorm = None):
        old_brush_data = tuple(filter(lambda x: x.link == new_brush_data.link, self.dvorniki_data_norm_list))
        len_brush_items = len(old_brush_data)
        if len_brush_items > 1:
            print('Somehow there is more then one instance for one car')
        elif len_brush_items == 0:
            new_brush_data.status = "новый"
            self.dvorniki_data_norm_list.append(new_brush_data)
        elif len_brush_items == 1:
            if tuple(old_brush_data[0].model_dump().values())[:15] == tuple(new_brush_data.model_dump().values())[:15]:
                old_brush_data[0].status = "старый"
                if not old_brush_data[0].previous_scan_date and old_brush_data[0].current_scan_date:
                    old_brush_data[0].previous_scan_date = old_brush_data[0].current_scan_date
                    old_brush_data[0].current_scan_date = None
            else:
                position = self.dvorniki_data_norm_list.index(old_brush_data[0])

                new_brush_data.status = "изменён"
                new_brush_data.old_brand = old_brush_data[0].norm_brand_name
                new_brush_data.old_model = old_brush_data[0].norm_model_name
                new_brush_data.old_start_date = old_brush_data[0].start_date
                new_brush_data.old_end_date = old_brush_data[0].end_date
                new_brush_data.old_body_type = old_brush_data[0].body_type
                new_brush_data.old_body_model = old_brush_data[0].body_model
                new_brush_data.old_generation = old_brush_data[0].generation
                new_brush_data.old_restyling = old_brush_data[0].restyling
                new_brush_data.old_attach_type = old_brush_data[0].attach_type
                new_brush_data.old_size_1 = old_brush_data[0].size_1
                new_brush_data.old_size2 = old_brush_data[0].size2
                new_brush_data.old_size_back = old_brush_data[0].size_back
                new_brush_data.old_washer = old_brush_data[0].washer
                new_brush_data.old_heater = old_brush_data[0].heater
                new_brush_data.old_info = old_brush_data[0].info

                self.dvorniki_data_norm_list[position] = new_brush_data

    def normalize_models(self):
        for partially_norm in self.dvorniki_data_norm_list:
            normalize_bad_models(partially_norm)

    def pickle_norm_dvorniki(self):
        new_directory = create_pickle_dir()
        filename = f"dvorniki_norm_data.pickle"
        fullfilepath = new_directory.joinpath(filename)
        with open(fullfilepath, "wb") as file:
            pickle.dump(self.dvorniki_data_norm_list, file)
            logger.info(f"save binary file {fullfilepath}")

    def unpickle_norm_dvorniki(self):
        filename = f"dvorniki_norm_data.pickle"
        fullfilepath = self.output_filepath.joinpath(f"pickles/{filename}")
        if Path.exists(fullfilepath):
            with open(fullfilepath, "rb") as file:
                logger.info(f"open binary file {fullfilepath}")
                self.dvorniki_data_norm_list = pickle.load(file)

    def norm_dvorniki_brands(self):
        brands = set()
        for entry in self.dvorniki_data_norm_list:
            brands.add(entry.norm_brand_name)
        return sorted(brands)

    def norm_dvorniki_models(self, brand_name: str):
        models = set()
        filtered_by_brand = filter(lambda x: x.norm_brand_name == brand_name, self.dvorniki_data_norm_list)
        for entry in filtered_by_brand:
            models.add(entry.norm_model_name)
        return sorted(models)

    def save_excel(self):
        logger.info("start saving data in excel")
        new_directory = create_results_tables_dir()
        filename = f"dvorniki_norm_data.xlsx"
        fullfilepath = new_directory.joinpath(filename)
        writer = ExcelWriter(fullfilepath, DvornikiNormParams())
        for dvorniki_data_norm in self.dvorniki_data_norm_list:
            writer.write_data_row(dvorniki_data_norm)
        writer.workbook.close()
        logger.info(f"saved data in excel file {fullfilepath}")

    def execute(self):
        self.process_main_data()
        self.pickle_raw_dvorniki()
        self.unpickle_raw_dvorniki()
        self.unpickle_norm_dvorniki()
        self.normalize_raw_dvorniki()
        self.normalize_models()
        self.pickle_norm_dvorniki()
        self.unpickle_norm_dvorniki()
        self.save_excel()
