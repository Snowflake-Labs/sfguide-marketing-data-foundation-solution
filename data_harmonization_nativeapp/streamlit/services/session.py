import os
import snowflake.connector
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session


def get_login_token() -> str:
    if not is_token(): return ''
    with open('/snowflake/session/token', 'r') as f:
        return f.read()

def read_local_credentials():
    import json
    with open(get_local_conn_file_abspath()) as conn_f:
        return json.load(conn_f)

def connection() -> snowflake.connector.SnowflakeConnection:
    if is_local():
        session = read_local_credentials()
        creds = {
            'account': session['account'],
            'user': session['user'],
            'password': session['password'],
            'warehouse': session['warehouse'],
            'database': session['database'],
            'schema': session['schema'],
            'role': session['role'],
            'client_session_keep_alive': True
        }
    elif is_docker():
        creds = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'role': os.getenv('SNOWFLAKE_ROLE'),
            'client_session_keep_alive': True
        }
    else:
        creds = {
            'protocol': "https",
            'authenticator': "oauth",
            'host': os.getenv('SNOWFLAKE_HOST'),
            'port': os.getenv('SNOWFLAKE_PORT'),
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'token': get_login_token(),
            'client_session_keep_alive': True
        }

    snowflake.connector.paramstyle='numeric'
    connection = snowflake.connector.connect(**creds)
    return connection

def session() -> Session:
    try:
        return get_active_session()
    except Exception:
        pass
    return Session.builder.configs({"connection": connection()}).create()

def get_local_conn_file_abspath():
    conn_file_rpath = '../../../connection_config.json'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), conn_file_rpath))

# Returns if the current session is running in local machine
def is_local() -> bool:
    conn_file_abspath = get_local_conn_file_abspath()
    return os.path.isfile(conn_file_abspath)

def is_token() -> bool:
    return os.path.isfile("/snowflake/session/token")

def is_docker() -> bool:
    return os.getenv('CREDENTIALS_DOCKER') is not None
