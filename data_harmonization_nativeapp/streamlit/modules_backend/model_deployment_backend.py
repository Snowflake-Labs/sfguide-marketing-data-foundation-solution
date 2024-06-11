from utils.model_helpers import execute_sql_query
from globals import *


def get_providers_dict(sp_session, application):
    get_providers_query = f'SELECT * FROM {application}.{CONFIGURATION_SCHEMA}.PROVIDERS'
    providers = execute_sql_query(sp_session, get_providers_query)
    providers_dict = {row[NAME_KEY]: row[ID_KEY] for row in providers}
    return providers_dict

def get_connector_providers(sp_session, application, provider_id):
    get_connector_providers_query = f"SELECT * FROM {application}.{CONFIGURATION_SCHEMA}.CONNECTOR_PROVIDERS WHERE PROVIDER_ID = '{provider_id}'"
    connector_providers = execute_sql_query(sp_session, get_connector_providers_query)
    return connector_providers

def get_connectors_dict(sp_session, application, connector_providers):
    connector_id_options = [row[CONNECTOR_ID_KEY] for row in connector_providers]
    connectors_dict = {}
    for connector_id in connector_id_options:
        get_connector_name_query = f"SELECT NAME FROM {application}.{CONFIGURATION_SCHEMA}.CONNECTORS WHERE ID = '{connector_id}'"
        connector_info = execute_sql_query(sp_session, get_connector_name_query)[0]
        connectors_dict[connector_info[NAME_KEY]] = connector_id
    return connectors_dict

def get_connector_information(connector_providers, provider_id, connectors_dict, connector_name):
    connector_id = connectors_dict[connector_name]
    for source in connector_providers:
        if (source[PROVIDER_ID_KEY] == provider_id and source[CONNECTOR_ID_KEY] == connector_id):
            return source[DEFAULT_SCHEMA_KEY].upper(), source[CONNECTOR_URL_KEY]

def update_current_schema(current_schema, customized_schema):
    has_changed = customized_schema != current_schema
    current_schema = customized_schema if has_changed else current_schema
    return current_schema

def validate_schema_grants(sp_session, application, current_schema):
    check_command = f"SHOW GRANTS TO APPLICATION {application};"
    application_grants = execute_sql_query(sp_session, check_command)
    has_schema_grants = any(f".{current_schema}." in grant[NAME_KEY] for grant in application_grants)
    return has_schema_grants


