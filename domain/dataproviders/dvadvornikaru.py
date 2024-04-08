import pickle
from pathlib import Path

from loguru import logger
from requests import Response
from tqdm import tqdm

from domain.models.dvadvornikaru import DvaDvornikaBrand, DvaDvornikaModelRaw, DvaDvornikaDataNorm
from downloader.httpdownloader import RequestsDownloader
from downloader.params import RequestManagerParams
from normalizer.dvadvornikaru import normalize_raw_dvorniki_data, normalize_bad_models
from parser.twodvornikaru.htmlparser import BsParser
from filewriter.excel import ExcelWriter
from filewriter.params import DvornikiNormParams


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
        tqdm_params = {
            'desc': 'Get brands',
            'total': len(self.dvorniki_brands_list),
            'miniters': 1,
            'unit': 'brand',
            'unit_scale': True, }
        for brand in tqdm(self.dvorniki_brands_list, **tqdm_params):
            # for brand in self.dvorniki_brands_list:
            mark_page_html: Response | None = self.loader.safe_get(url=brand.link, params=RequestManagerParams())
            models = self.parser.parse_mark_page(mark_page_html, brand)

            self.dvorniki_models_list_raw.extend(models)
            logger.info(f"Add {brand.brand_name}")
        self.process_auto_mark_brush_data()

    def process_auto_mark_brush_data(self):
        tqdm_params = {
            'desc': 'Get models',
            'total': len(self.dvorniki_models_list_raw),
            'miniters': 1,
            'unit': 'model',
            'unit_scale': True, }
        for model in tqdm(self.dvorniki_models_list_raw, **tqdm_params):
        # for model in self.dvorniki_models_list_raw:
            logger.info(f"proceed model brush data for {model.brand_name} {model.car_model_name}")
            brush_page_html: Response | None = self.loader.safe_get(url=model.link, params=RequestManagerParams())
            brush_data = self.parser.parse_model_brush_data(brush_page_html)
            model.raw_data_brush = brush_data

    def pickle_raw_dvorniki(self):
        filename = f"dvorniki_raw_data.pickle"
        fullfilepath = self.output_filepath.joinpath(filename)
        with open(fullfilepath, "wb") as file:
            pickle.dump(self.dvorniki_models_list_raw, file)
            logger.info(f"save binary file {fullfilepath}")

    def unpickle_raw_dvorniki(self):
        filename = f"dvorniki_raw_data.pickle"
        fullfilepath = self.output_filepath.joinpath(filename)
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
            if tuple(old_brush_data[0].model_dump().values())[:-3] == tuple(new_brush_data.model_dump().values())[:-3]:
                old_brush_data[0].status = "старый"
            else:
                position = self.dvorniki_data_norm_list.index(old_brush_data[0])
                new_brush_data.status = "изменён"
                self.dvorniki_data_norm_list[position] = new_brush_data

    def normalize_models(self):
        for partially_norm in self.dvorniki_data_norm_list:
            normalize_bad_models(partially_norm)

    def split_model_by_slash(self):
        for model in self.dvorniki_data_norm_list:
            splitted_model_names = tuple(filter(None, model.norm_model_name.split("/")))
            if len(splitted_model_names) > 1:
                for name in splitted_model_names:
                    name = name.strip()
                    split_model = model.__deepcopy__()
                    split_model.norm_model_name = name
                    self.dvorniki_data_norm_list.append(split_model)

    def delete_models_with_slash(self):
        models_without_slash = filter(lambda x: "/" not in x.norm_model_name, self.dvorniki_data_norm_list)
        self.dvorniki_data_norm_list = sorted(models_without_slash, key=lambda x: x.norm_brand_name)

    def pickle_norm_dvorniki(self):
        filename = f"dvorniki_norm_data.pickle"
        fullfilepath = self.output_filepath.joinpath(filename)
        with open(fullfilepath, "wb") as file:
            pickle.dump(self.dvorniki_data_norm_list, file)
            logger.info(f"save binary file {fullfilepath}")

    def unpickle_norm_dvorniki(self):
        filename = f"dvorniki_norm_data.pickle"
        fullfilepath = self.output_filepath.joinpath(filename)
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

    # @staticmethod
    # def static_load_binary(path):
    #     file_path = path
    #     with open(file_path, "rb") as handle:
    #         logger.info(f"open binary file {file_path}")
    #         data = handle.read()
    #         data = pickle.loads(data)
    #         return data

    def save_excel(self):
        logger.info("start saving data in excel")
        filename = f"dvorniki_norm_data.xlsx"
        fullfilepath = self.output_filepath.joinpath(filename)
        writer = ExcelWriter(fullfilepath, DvornikiNormParams())
        tqdm_params = {
            'desc': 'Write to excel',
            'total': len(self.dvorniki_data_norm_list),
            'miniters': 1,
            'unit': 'dvorniki_data',
            'unit_scale': True, }
        for dvorniki_data_norm in tqdm(self.dvorniki_data_norm_list, **tqdm_params):
            writer.write_data_row(dvorniki_data_norm)
        writer.workbook.close()
        logger.info(f"saved data in excel file {fullfilepath}")

    def execute(self):
        # self.process_main_data()
        # self.pickle_raw_dvorniki()
        self.unpickle_raw_dvorniki()
        self.unpickle_norm_dvorniki()
        self.normalize_raw_dvorniki()
        # self.split_model_by_slash()
        # self.delete_models_with_slash()
        self.normalize_models()
        self.pickle_norm_dvorniki()
        print(len(self.dvorniki_data_norm_list))
        # self.unpickle_norm_dvorniki()
        self.save_excel()
