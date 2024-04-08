from domain.dataproviders.drom import CarsModelsManager
from domain.dataproviders.dvadvornikaru import WindshieldWiperManager


def brands_in_both_sets(
        passenger_cmm: CarsModelsManager,
        freight_cmm: CarsModelsManager,
        wwm: WindshieldWiperManager
) -> list[str, ...]:
    """generate brands set present in both sources drom and dvorniki"""

    passenger_cmm.unpickle_norm_drom()
    drom_norm_passenger_brands = set(passenger_cmm.norm_drom_brands())

    freight_cmm.unpickle_norm_drom()
    drom_norm_freight_brands = set(freight_cmm.norm_drom_brands())
    common_drom_brands = drom_norm_freight_brands | drom_norm_passenger_brands

    wwm.unpickle_norm_dvorniki()
    dvorniki_norm_brands = set(wwm.norm_dvorniki_brands())
    common_brands_list = dvorniki_norm_brands & common_drom_brands

    return sorted(common_brands_list)


def models_for_brand(
        passenger_cmm: CarsModelsManager,
        freight_cmm: CarsModelsManager,
        wwm: WindshieldWiperManager,
        brand: str
) -> tuple[list[str, ...], list[str, ...]]:
    """generate models set for exact brand present in both sources drom and dvorniki
    returns tuple(drom common models for brand, dvorniki models for brand)"""
    passenger_cmm.unpickle_norm_drom()
    drom_passenger_models = set(passenger_cmm.norm_drom_models(brand))

    freight_cmm.unpickle_norm_drom()
    drom_freight_models = set(freight_cmm.norm_drom_models(brand))
    common_drom_models = drom_freight_models | drom_passenger_models

    wwm.unpickle_norm_dvorniki()
    dvorniki_models = set(wwm.norm_dvorniki_models(brand))
    drom_models_out = sorted(common_drom_models - dvorniki_models)
    dvorniki_models_out = sorted(dvorniki_models - common_drom_models)

    return drom_models_out, dvorniki_models_out


def handle_model_names(
        passenger_cmm: CarsModelsManager,
        freight_cmm: CarsModelsManager,
        wwm: WindshieldWiperManager):
    common_brands_list = brands_in_both_sets(passenger_cmm, freight_cmm, wwm)
    # limit = 3
    # brands_amount = 0
    with open('brands.txt', 'w', encoding='utf-8') as file:
        for brand in common_brands_list:
            drom_models_out, dvorniki_models_out = models_for_brand(passenger_cmm, freight_cmm, wwm, brand)
            file.write(f'{brand}\n')
            file.write(f'drom_models_out\n')
            file.write(str(drom_models_out))
            file.write("\n")
            file.write(f'dvorniki_models_out\n')
            file.write(str(dvorniki_models_out))
            file.write("\n\n")
            # brands_amount += 1
            # if limit == brands_amount:
            #     break
