from pydantic import BaseModel, Field
from typing import Any
from datetime import date


class DromBrandEntity(BaseModel):
    vehicle_type: str = Field(default=None)
    brand_name: str = Field(default=None)
    link: str = Field(default=None)


class DromModelEntity(DromBrandEntity):
    car_model_name: str = Field(default=None)
    link: str = Field(default=None)


class DromRawGenerationsEntity(DromModelEntity):
    raw_markets_group: Any = Field(default=None)


class DromGenerationEntity(DromModelEntity):
    market: str = Field(default=None)
    generation: int = Field(default=None)
    restyling: int = Field(default=None)
    start_date: int = Field(default=None)
    end_date: int = Field(default=None)
    body_model_primary: str = Field(default=None)
    body_model_secondary: str = Field(default=None)
    body_type: str = Field(default=None)
    previous_scan_date: date = Field(default=None)
    current_scan_date: date = Field(default=date.today())
    photo_link: str = Field(default=None)
    status: str = Field(default=None)
    old_brand: str = Field(default=None)
    old_model: str = Field(default=None)
    old_market: str = Field(default=None)
    old_generation: int = Field(default=None)
    old_restyling: int = Field(default=None)
    old_start_date: int = Field(default=None)
    old_end_date: int = Field(default=None)
    old_body_model_primary: str = Field(default=None)
    old_body_model_secondary: str = Field(default=None)
    old_body_type: str = Field(default=None)



