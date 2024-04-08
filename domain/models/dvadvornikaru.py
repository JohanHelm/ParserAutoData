from typing import List, Optional, Any
from pydantic import BaseModel, RootModel, Field

# TODO удалить от сюда
class BrushModelData(BaseModel):
    attach_type: Optional[str] = None
    left_brush_size: Optional[int] = None
    right_brush_size: Optional[int] = None
    back_brush_size: Optional[int] = None
    nozzles: Optional[bool] = None
    washer: Optional[bool] = None
    heater: Optional[bool] = None
    info: Optional[str] = None


class AdditionalModelData(BaseModel):
    sales_start_year: Optional[int] = None
    sales_end_year: Optional[int] = None
    body_type: Optional[str] = None
    restyling: Optional[bool] = None
    restyling_num: Optional[int] = None
    first_generation: Optional[int] = None
    last_generation: Optional[int] = None
    codes: Optional[str] = None


class ModelData(BaseModel):
    name: Optional[str] = None
    link: Optional[str] = None
    raw_data: Optional[str] = None
    raw_data_brush: Optional[str] = None
    parsed_raw_data: Optional[AdditionalModelData] = None
    parsed_raw_data_brush: Optional[BrushModelData] = None
    status: Optional[str] = None


class MarkData(BaseModel):
    name: Optional[str] = None
    link: Optional[str] = None
    models: Optional[List[ModelData]] = []


class DvaDvornikaData(RootModel):
    root: List[MarkData] = []


class DvaDvornikaFlatModel(BaseModel):
    mark_name: Optional[str] = None
    car_model_name: Optional[str] = None
    sales_start_year: Optional[int] = None
    sales_end_year: Optional[int] = None
    body_type: Optional[str] = None
    restyling: Optional[bool] = None
    restyling_num: Optional[int] = None
    first_generation: Optional[int] = None
    last_generation: Optional[int] = None
    codes: Optional[str] = None
    attach_type: Optional[str] = None
    left_brush_size: Optional[int] = None
    right_brush_size: Optional[int] = None
    back_brush_size: Optional[int] = None
    nozzles: Optional[bool] = None
    washer: Optional[bool] = None
    heater: Optional[bool] = None
    info: Optional[str] = None


class DvaDvornikaFlatData(RootModel):
    root: List[DvaDvornikaFlatModel] = []
# TODO до сюда

class DvaDvornikaBrand(BaseModel):
    brand_name: str = Field(default=None)
    link: str = Field(default=None)


class DvaDvornikaModelRaw(DvaDvornikaBrand):
    car_model_name: str = Field(default=None)
    raw_data: str = Field(default=None)
    raw_data_brush: str = Field(default=None)

class DvaDvornikaDataNorm(BaseModel):
    norm_brand_name: str = Field(default=None)
    norm_model_name: str = Field(default=None)
    start_date: int
    end_date: int
    body_type: str
    body_model: str
    generation: int = Field(default=1)
    restyling: int = Field(default=0)
    attach_type: str = Field(default=None)
    size_1: int
    size2: int
    size_back: int = Field(default=0)
    washer: bool = Field(default=False)
    heater: bool = Field(default=False)
    info: str = Field(default=None)
    previous_scan_date: date = Field(default=None)
    current_scan_date: date = Field(default=date.today())
    link: str = Field(default=None)
    status: str = Field(default=None)
