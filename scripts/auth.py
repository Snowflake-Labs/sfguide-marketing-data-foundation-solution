import os
import json
from snowflake.snowpark.session import Session

def authenticate(conn_file_name: str = None, is_local_installation: bool = False) -> Session:

    if is_local_installation:
        conn_obj = get_conn_obj(conn_file_name)
    else:
        try:

            conn_obj = {
                "user" : os.environ["DATAOPS_SNOWFLAKE_USER"],
                "password" : os.environ["DATAOPS_SNOWFLAKE_PASSWORD"],
                "account" : os.environ["DATAOPS_SNOWFLAKE_ACCOUNT"],
                "database" : f"{os.environ['DATAOPS_DATABASE']}_MARKETING_FOUNDATION",
                "solution_prefix" : os.environ["DATAOPS_CATALOG_SOLUTION_PREFIX"],
                "warehouse" : f"{os.environ['DATAOPS_CATALOG_SOLUTION_PREFIX']}_BUILD_WH"
                }
        except KeyError:
            raise Exception("Could not find one or more required environment variables")
            
    print(f'Warehouse selected: {conn_obj["warehouse"]}')

    sp_session = Session.builder.configs(conn_obj).create()
    sp_session.use_warehouse(conn_obj["warehouse"])
    session_query = 'select current_account(), current_warehouse(), current_role(), current_database(), current_schema()'
    print(sp_session.sql(session_query).first())


        
    return sp_session


def get_conn_obj(conn_file_name: str) -> dict:
    with open(conn_file_name) as conn_f:
        return json.load(conn_f)


