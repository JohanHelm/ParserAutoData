from pydantic import BaseModel


class DromNormParams(BaseModel):
    worksheet_name: str = "drom_norm_data"
    worksheet_header: tuple[str, ...] = (
        "vehicle_type",
        "brand_name",
        "link",
        "model_name",
        "market",
        "generation",
        "restyling",
        "start_date",
        "end_date",
        "body_model_primary",
        "body_model_secondary",
        "body_type",
        "previous_scan_date",
        "current_scan_date",
        "photo_link",
        "status",
        "old_brand",
        "old_model",
        "old_market",
        "old_generation",
        "old_restyling",
        "old_start_date",
        "old_end_date",
        "old_body_model_primary",
        "old_body_model_secondary",
        "old_body_type",
    )


class DromMergedMarketsParams(BaseModel):
    worksheet_name: str = "drom_merged_data"
    worksheet_header: tuple[str, ...] = (
        "original_vehicle_type",
        "original_brand_name",
        "original_model",
        "original_generation",
        "min_entites_start",
        "max_entites_end",
        "original_body_type",
        "original_restyling",
        "computed_start_date",
        "computed_end_date",
        "merged_body_model_primary",
        "merged_body_model_secondary",
    )


class DvornikiNormParams(BaseModel):
    worksheet_name: str = "dvorniki_norm_data"
    worksheet_header: tuple[str, ...] = (
        "brand_name",
        "model_name",
        "start_date",
        "end_date",
        "body_type",
        "body_model",
        "generation",
        "restyling",
        "attach_type",
        "size_1",
        "size_2",
        "size_back",
        "washer",
        "heater",
        "info",
        "previous_scan_date",
        "current_scan_date",
        "link",
        "status",
        "old_brand",
        "old_model",
        "old_start_date",
        "old_end_date",
        "old_body_type",
        "old_body_model",
        "old_generation",
        "old_restyling",
        "old_attach_type",
        "old_size_1",
        "old_size_2",
        "old_size_back",
        "old_washer",
        "old_heater",
        "old_info",
    )


class ResultParams(BaseModel):
    worksheet_name: str = "joined_drom_dvorniki_data"
    worksheet_header: tuple[str, ...] = (
        "vehicle_type",
        "brand_name",
        "model_name",
        "market",
        "generation",
        "restyling",
        "start_date",
        "end_date",
        "body_model_primary",
        "body_model_secondary",
        "body_type",
        "attach_type",
        "left_brush_size",
        "right_brush_size",
        "size_back",
        "washer",
        "heater",
        "info",
    )
