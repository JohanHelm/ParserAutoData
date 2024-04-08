from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag, NavigableString
from loguru import logger
from requests import Response

from domain.models.dvadvornikaru import DvaDvornikaData, MarkData, ModelData, DvaDvornikaBrand, DvaDvornikaModelRaw

PARSE_MODE = "lxml"
BLOCK_A_P_TEXT: tuple[str, ...] = (
    "Бескаркасные щетки стеклоочистителя",
    "Гибридные щетки стеклоочистителя",
    "Каркасные щетки стеклоочистителя в чехле",
    "Оригинальные щетки стеклоочистителя",
    "Задние щетки стеклоочистителя",
    "Полезное",
)
MODEL_LINK_SW = "https://www.2dvornika.ru"


class BsParser:
    def __init__(self, parse_mode):
        self.parse_mode = parse_mode

    def parse_main_page(self,
        start_page_data: Response,
    ) -> list[DvaDvornikaBrand]:
        soup = BeautifulSoup(start_page_data.text, PARSE_MODE)
        marks = []
        article_id_main: Tag | NavigableString | None = soup.find("article", id="main")
        if article_id_main:
            mark_data: ResultSet = article_id_main.find_all("a")
            for data in mark_data:
                try:
                    mark_href_tag: str | None = data.get("href")
                    mark_p_tag: Tag | None = data.find("p")

                    if (mark_p_tag is not None) and (mark_href_tag is not None):
                        mark_name_raw: str = mark_p_tag.getText().strip()
                        mark_name = " ".join(mark_name_raw.split()).lower()

                        # Здесь ты пропускаешь итерацию если mark_name in BLOCK_A_P_TEXT?
                        # мусорные данные попадают
                        if mark_name_raw in BLOCK_A_P_TEXT:
                            logger.error("Попали в игнорируемый список")
                            continue
                        mark_link: str = mark_href_tag
                        model = DvaDvornikaBrand(brand_name=mark_name, link=mark_link)
                        marks.append(model)
                except AttributeError:
                    print(f"Error with {data}")
        return marks

    def parse_mark_page(self, mark_page_data: Response, brand: DvaDvornikaBrand):
        soup = BeautifulSoup(mark_page_data.text, PARSE_MODE)
        article_id_main: Tag | NavigableString | None = soup.find("article", id="main")
        models = []
        if article_id_main:
            model_data: ResultSet = article_id_main.find_all("a")
            for data in model_data:
                try:
                    mark_href_tag: str | None = data.get("href")
                    mark_b_tag: Tag | None = data.find("b")
                    mark_span_tag: Tag | None = data.find("span")
                    if (mark_b_tag is not None) and (mark_span_tag is not None):
                        model_name_raw: str = mark_b_tag.getText().strip()
                        model_name = " ".join(model_name_raw.split()).lower()
                        model_desc_raw: str = mark_span_tag.getText().strip()
                        model_desc = " ".join(model_desc_raw.split()).lower()
                        model_link: str = mark_href_tag
                        if not model_link.startswith(MODEL_LINK_SW):
                            model_link = MODEL_LINK_SW + model_link
                        model = DvaDvornikaModelRaw(
                            brand_name=brand.brand_name,
                            car_model_name=model_name,
                            link=model_link,
                            raw_data=model_desc
                        )
                        models.append(model)
                except AttributeError:
                    print(f"Error with {data}")
        return models

    def parse_model_brush_data(self, brush_page_html):
        soup = BeautifulSoup(brush_page_html.text, PARSE_MODE)
        article_id_main: Tag | NavigableString | None = soup.find("article", id="main")
        if article_id_main:
            data = article_id_main.find("small")
            lines = [line.strip() for line in data.get_text().splitlines() if len(line.strip()) > 0]
            res = "\n".join(lines)
            model_raw_data_brush = res
        else:
            model_raw_data_brush = "No data found"
        return model_raw_data_brush
