import data_harmonization_nativeapp.streamlit.modules_backend.model_deployment_backend as backend
from data_harmonization_nativeapp.streamlit.utils.model_helpers import APPLICATION
from unittest.mock import MagicMock

model_path = "data_harmonization_nativeapp.streamlit.modules_backend.model_deployment_backend"

provider_id = 1
provider_name = 'Facebook'

connector_id = 1
connector_name = 'Fivetran'
connector_schema = 'FACEBOOK_ADS'
connector_url = 'https://fivetran.com/dashboard/connectors'

providers_dict = { provider_name : provider_id }
connectors_dict = { connector_name : connector_id }
connector = [{ 'ID' : connector_id, 'NAME' : connector_name }]
connector_providers = [{ 
    'PROVIDER_ID'    : provider_id, 
    'CONNECTOR_ID'   : connector_id, 
    'DEFAULT_SCHEMA' : connector_schema, 
    'CONNECTOR_URL'  : connector_url 
}]

def test_get_providers_dict(mocker):
    mock_session = MagicMock()
    mock_object_execute_sql_query = mocker.patch(f"{model_path}.execute_sql_query", return_value = [{'ID' : 1, 'NAME' : provider_name}])
    providers_dict_result = backend.get_providers_dict(mock_session, APPLICATION)
    mock_object_execute_sql_query.assert_called_with(mock_session, f'SELECT * FROM {APPLICATION}.{backend.SCHEMA}.PROVIDERS')
    assert providers_dict_result == providers_dict

def test_get_connector_providers(mocker):
    mock_session = MagicMock()
    mock_object_execute_sql_query = mocker.patch(f"{model_path}.execute_sql_query", return_value = connector_providers)
    connector_providers_result = backend.get_connector_providers(mock_session, APPLICATION, provider_id)
    mock_object_execute_sql_query.assert_called_with(mock_session, f"SELECT * FROM {APPLICATION}.{backend.SCHEMA}.CONNECTOR_PROVIDERS WHERE PROVIDER_ID = '{provider_id}'")
    assert connector_providers_result == connector_providers

def test_get_connectors_dict(mocker):
    mock_session = MagicMock()
    mock_object_execute_sql_query = mocker.patch(f"{model_path}.execute_sql_query", return_value = connector)
    connectors_dict_result = backend.get_connectors_dict(mock_session, APPLICATION, connector_providers)
    mock_object_execute_sql_query.assert_called_with(mock_session, f"SELECT NAME FROM {APPLICATION}.{backend.SCHEMA}.CONNECTORS WHERE ID = '{connector_id}'")
    assert connectors_dict_result == connectors_dict

def test_get_connector_information():
    connector_information_result = backend.get_connector_information(connector_providers, provider_id, connectors_dict, connector_name)
    assert connector_information_result == (connector_schema, connector_url)

def test_update_current_schema():
    my_schema = "MySchema"
    current_schema_result = backend.update_current_schema(current_schema = my_schema, customized_schema = connector_schema)
    assert current_schema_result == connector_schema

def test_validate_schema_grants(mocker):
    mock_session = MagicMock()
    mock_execute_sql_query = mocker.patch(f"{model_path}.execute_sql_query", return_value = [{ "name" : f"DB.{connector_schema}.Table"}])
    has_grants_result = backend.validate_schema_grants(mock_session, APPLICATION, connector_schema)
    mock_execute_sql_query.assert_called_with(mock_session, f"SHOW GRANTS TO APPLICATION {APPLICATION};")
    assert has_grants_result == True