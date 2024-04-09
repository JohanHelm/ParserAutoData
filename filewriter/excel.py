from pathlib import Path
import xlsxwriter

from domain.models.dromru import DromGenerationEntity
from domain.models.dvadvornikaru import DvaDvornikaDataNorm
from .params import DvornikiNormParams, DromNormParams


class ExcelWriter:
    def __init__(self, fullfilepath: Path,
                 excel_params: [DromNormParams, DvornikiNormParams]) -> None:
        self.workbook = xlsxwriter.Workbook(fullfilepath)
        self.worksheet = self.workbook.add_worksheet(excel_params.worksheet_name)
        self.bold = self.workbook.add_format(
            {"bold": True, "font_name": "Times New Roman", "font_size": 13}
        )
        self.cell_format = self.workbook.add_format(
            {"font_name": "Times New Roman", "font_size": 13}
        )
        self.worksheet.write_row(0, 0, excel_params.worksheet_header, self.bold)
        self.row = 1

    def write_not_merged_data(self, computed_generation: DromGenerationEntity):
        for entity in computed_generation.entites:
            if not entity.merged_whith_dvorniki:
                write_data = list(computed_generation.model_dump().values())[:-1]
                write_data.extend(entity.model_dump().values())
                self.worksheet.write_row(self.row, 0, write_data, self.cell_format)
                self.worksheet.autofit()
                self.row += 1

    def write_data_row(self, some_data: [DvaDvornikaDataNorm, DromGenerationEntity]):
        self.worksheet.write_row(self.row, 0, some_data.model_dump().values(), self.cell_format)
        self.worksheet.autofit()
        self.row += 1
