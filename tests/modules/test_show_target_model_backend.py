import data_harmonization_nativeapp.streamlit.modules_backend.show_target_model_backend as backend
from data_harmonization_nativeapp.streamlit.utils.model_helpers import APPLICATION
from unittest.mock import MagicMock

model_path = "data_harmonization_nativeapp.streamlit.modules_backend.show_target_model_backend"
model_schema = "CAMPAIGN_INTELLIGENCE_COMBINED"

def test_get_model_table_df(mocker):
    # Given
    model_table = "DIM_ACCOUNT"
    get_table_columms_query = f"""
        SELECT COLUMN_NAME AS "Column name", DATA_TYPE AS "Type" 
        FROM {APPLICATION}.INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = '{model_schema}' AND TABLE_NAME = '{model_table}';
    """
    model_table_df = [
        {
            'Column name' : 'ID', 
            'Type'        : 'INTEGER'
        }, 
        {
            'Column name' : 'Key', 
            'Type'        : 'TEXT'
        }
    ]

    # When
    mock_session = MagicMock()
    mock_object_execute_sql_query = mocker.patch(f"{model_path}.execute_sql_query", return_value = model_table_df)
    get_model_table_df_result = backend.get_model_table_df(mock_session, model_schema, model_table)

    # Then
    mock_object_execute_sql_query.assert_called_with(mock_session, get_table_columms_query)
    assert get_model_table_df_result == model_table_df

def test_get_model_tables(mocker):
    # Given
    model_tables = [
        { 
            "TABLE_NAME" : "DIM_ACCOUNT" 
        }, 
        { 
            "TABLE_NAME" : "DIM_KEYWORD" 
        }
    ]
    table_list = ["DIM_ACCOUNT", "DIM_KEYWORD" ]
    get_model_tables_query = f"SELECT TABLE_NAME FROM {APPLICATION}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{model_schema}'"

    # When
    mock_session = MagicMock()
    mock_object_execute_sql_query = mocker.patch(f"{model_path}.execute_sql_query", return_value = model_tables)
    get_model_tables_result = backend.get_model_tables(mock_session, model_schema)

    # Then
    mock_object_execute_sql_query.assert_called_with(mock_session, get_model_tables_query)
    assert get_model_tables_result == table_list

def test_calculate_table_height():
    # Given
    rows_quantity = 10

    # When
    get_calculate_table_height = backend.calculate_table_height(rows_quantity)

    # Then
    assert get_calculate_table_height == 388
