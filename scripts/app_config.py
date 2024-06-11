import os
import json


def get_app_config(app_config_f: str = 'app_config.json', is_local_installation: bool = False) -> dict:
    with open(app_config_f) as app_f:
        app_config = json.load(app_f)
    
    if not is_local_installation:
        app_config["database"] = f"{os.environ['DATAOPS_DATABASE']}_MARKETING_FOUNDATION"
        app_config["warehouse"]= f"{os.environ['DATAOPS_CATALOG_SOLUTION_PREFIX']}_BUILD_WH"

    print(app_config)

    return app_config

