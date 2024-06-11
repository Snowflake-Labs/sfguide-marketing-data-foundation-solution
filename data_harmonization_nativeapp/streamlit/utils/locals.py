import os
import json


# Returns if the current connection is using local credentials
def is_local():
    conn_file_abspath = get_local_conn_file_abspath()
    return os.path.isfile(conn_file_abspath)


def get_local_conn_file_abspath():
    # TODO change how the connection file is obtained
    conn_file_rpath = '../../../connection_config.json'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), conn_file_rpath))


def get_local_credentials():
    with open(get_local_conn_file_abspath()) as conn_f:
        return json.load(conn_f)
