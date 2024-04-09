from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


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
    start_date: int = Field(default=None)
    end_date: int = Field(default=None)
    body_type: str = Field(default=None)
    body_model: str = Field(default=None)
    generation: int = Field(default=1)
    restyling: int = Field(default=0)
    attach_type: str = Field(default=None)
    size_1: int = Field(default=None)
    size2: int = Field(default=None)
    size_back: int = Field(default=0)
    washer: bool = Field(default=False)
    heater: bool = Field(default=False)
    info: str = Field(default=None)
    previous_scan_date: date = Field(default=None)
    current_scan_date: date = Field(default=date.today())
    link: str = Field(default=None)
    status: str = Field(default=None)
    old_brand: str = Field(default=None)
    old_model: str = Field(default=None)
    old_start_date: int = Field(default=None)
    old_end_date: int = Field(default=None)
    old_body_type: str = Field(default=None)
    old_body_model: str = Field(default=None)
    old_generation: int = Field(default=None)
    old_restyling: int = Field(default=None)
    old_attach_type: str = Field(default=None)
    old_size_1: int = Field(default=None)
    old_size2: int = Field(default=None)
    old_size_back: int = Field(default=None)
    old_washer: bool = Field(default=False)
    old_heater: bool = Field(default=False)
    old_info: str = Field(default=None)
