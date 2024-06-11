import pytest
from data_harmonization_nativeapp.streamlit.utils.model_helpers import APPLICATION
from streamlit.testing.v1 import AppTest
from unittest.mock import MagicMock

@pytest.mark.skip(reason="As deployment model page will be changing, it is not worth to update this test until final page was accepted.")
def test_model_deployment_page(mocker):

    model_path = "data_harmonization_nativeapp.streamlit.modules.model_deployment"
    connector_name = "Fivetran Facebook Ads"
    schema_name = "facebook_ads"

    mock_session = MagicMock() 
    mock_get_session = mocker.patch(f"{model_path}.connect_to_snowflake", return_value = mock_session)
    mock_get_provider_connector = mocker.patch(f"{model_path}.get_provider_connector", return_value = connector_name)
    mock_update_current_schema = mocker.patch(f"{model_path}.update_current_schema", return_value = schema_name)
    mock_validate_schema_grants = mocker.patch(f"{model_path}.validate_schema_grants", return_value = True)
    
    at = AppTest.from_function(call_model_deployment_page).run()

    mock_get_session.assert_called()
    mock_get_provider_connector.assert_called_with(mock_session, APPLICATION)
    mock_update_current_schema.assert_called()
    mock_validate_schema_grants.assert_called_with(mock_session, APPLICATION, schema_name)

    assert at.title[0].value == "Deploy Snowflake's Campaign Intelligence Models"
    assert at.subheader[0].value == "Select your preferred connector"
    assert at.subheader[1].value == "Lets upload the information using the selected connector"
    assert at.button[0].label == "Fivetran Facebook Ads"
    assert at.subheader[2].value == "Give the application reading grants to the generated table"
    assert at.code[0].value == f"GRANT SELECT ON ALL TABLES IN SCHEMA facebook_ads TO APPLICATION {APPLICATION};"
    assert at.button[1].label == "Check"
    at.button[1].click().run()
    assert at.success[0].value == "Grants for facebook_ads schema were applied successfully."

    assert not at.exception

def call_model_deployment_page():
    import data_harmonization_nativeapp.streamlit.modules.model_deployment as model_deployment
    model_deployment.model_deployment_page()