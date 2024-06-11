from globals import APPLICATION
from utils.model_helpers import execute_sql_query

unit_numbers_dict = {
    "Seconds" : 60,
    "Minutes" : 60,
    "Hours" : 24,
    "Days" : 30
}

def get_model_tables(sp_session, model_schema):
    get_tables_query = f"SELECT TABLE_NAME FROM {APPLICATION}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{model_schema}'"
    query_result = execute_sql_query(sp_session, get_tables_query)
    tables_list = [value["TABLE_NAME"] for value in query_result]
    return tables_list

def get_model_table_df(sp_session, model_schema, table_fullname):
    get_table_columms_query = f"""
        SELECT COLUMN_NAME AS "Column name", DATA_TYPE AS "Type" 
        FROM {APPLICATION}.INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = '{model_schema}' AND TABLE_NAME = '{table_fullname}';
    """
    df = execute_sql_query(sp_session, get_table_columms_query)
    return df

def calculate_table_height(rows_quantity):
    single_row_height = 35
    header_row_height = 38
    full_table_height = header_row_height + single_row_height * rows_quantity
    return full_table_height