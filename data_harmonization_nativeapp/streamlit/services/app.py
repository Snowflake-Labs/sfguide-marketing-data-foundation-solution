import os
import json
from utils.model_helpers import connect_to_snowflake

class Application:
    _instance = None

    def __new__(class_, *args, **kwargs):
        # singleton definition
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        app = _get_app_config()
        self.app_name = app['nativeapp_name']


def _get_app_config() -> dict:
    return _get_local_app_config() if _is_local() else _get_cloud_app_config()


def _get_cloud_app_config() -> dict:
    sp_session = connect_to_snowflake()
    app_name = sp_session.sql('select current_database()').first()[0]
    return { 'nativeapp_name': app_name }


def _get_local_app_config() -> dict:
    app_file = _get_local_app_file_abspath()
    with open(app_file) as app_f:
        return json.load(app_f)


def _get_local_app_file_abspath() -> str:
    file_rpath = '../../../app_config.json'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), file_rpath))


# Returns if the current session is running in local machine
def _is_local():
    conn_file_abspath = _get_local_app_file_abspath()
    return os.path.isfile(conn_file_abspath)
