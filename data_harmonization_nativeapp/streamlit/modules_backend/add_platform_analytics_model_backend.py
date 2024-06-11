import ast
import streamlit as st
import streamlit.components.v1 as st_components
from datetime import datetime
from services.i18n import Translator
from utils.assets import get_asset_path
from utils.model_helpers import connect_to_snowflake, section_header
from utils.resources import get_fivetran_icon, get_omnata_icon
from globals import *
from snowflake.snowpark.functions import col
from snowflake.snowpark import dataframe
from utils.model_helpers import execute_sql_query

sp_session = connect_to_snowflake()
translate = Translator().translate
connector_images = {
    1 : get_fivetran_icon(),
    2 : get_omnata_icon()
}

def get_connectors_dictionaries(provider_id: int)-> list:
    connectors_result = get_connectors_list(provider_id)
    connectors_list = []
    for row in connectors_result:
        connector_info = generate_connector_dict(row[ID_KEY], row[NAME_KEY], connector_images[row[ID_KEY]])
        connectors_list.append(connector_info)
    return connectors_list

def get_connectors_list(provider_id):
    connector_providers = get_provider_connectors(provider_id)
    connector_id_options = connector_providers.select(col(CONNECTOR_ID_KEY))
    connector_result = sp_session.table([APPLICATION, CONFIGURATION_SCHEMA,CONNECTORS_TABLE])\
                                        .where(col(ID_KEY).isin(connector_id_options)).collect()
    return connector_result

def get_provider_connector_default_schema(provider_id, connector_id):
    connector_default_schema = get_provider_connectors(provider_id)\
            .filter(col(CONNECTOR_ID_KEY) == connector_id)\
            .filter(col(PROVIDER_ID_KEY) == provider_id)\
            .collect()[0][DEFAULT_SCHEMA_KEY]
    return connector_default_schema

def get_provider_connectors(provider_id: int)-> dataframe:
    return sp_session.table([APPLICATION, CONFIGURATION_SCHEMA,CONNECTOR_PROVIDERS_TABLE]).where(col(PROVIDER_ID_KEY)==provider_id)

def get_connector_provider_url(provider_id: int, connector_id: int)-> str:
    connector_url_result = sp_session.table([APPLICATION, CONFIGURATION_SCHEMA, CONNECTOR_PROVIDERS_TABLE])\
                                        .where((col(PROVIDER_ID_KEY)==provider_id)&\
                                               (col(CONNECTOR_ID_KEY)==connector_id))\
                                        .select(col(CONNECTOR_URL_KEY)).collect()
    return connector_url_result[0].__getitem__(CONNECTOR_URL_KEY)

def generate_connector_dict(connector_id: int, connector_name: str, image: str)-> dict:
    connector_info = {
        ID_KEY    : connector_id,
        NAME_KEY  : connector_name,
        IMAGE_KEY : image
    }
    return connector_info

def open_md(file_name):
    home_file = get_asset_path(file_name)
    with open(home_file) as content:
        file_content = content.read()
        return file_content

def page_parameters():
    return st.session_state[PAGE_INFO_KEY][PARAMS_KEY]

def set_page_substeps(bold1 = False, bold2 = False, bold3 = False):
    page_substeps = [
        {TEXT_KEY : f"1.1 {translate('SelectConnector')}", IS_BOLD_KEY : bold1}, 
        {TEXT_KEY : f"1.2 {translate('ConnectorSetup')}", IS_BOLD_KEY : bold2},
        {TEXT_KEY : f"1.3 {translate('LinkDataAlreadyInSnowflake')}", IS_BOLD_KEY :  bold3}
    ]
    st.session_state[PAGE_INFO_KEY][PARAMS_KEY][SUBSTEPS_PARAM_KEY] = page_substeps

def update_page_state(new_state):
    page_parameters()[LINK_TO_DATA_KEY] = new_state
    st.experimental_rerun()

def set_connector_page_parameters(provider_info, connector_id, connector_name):
    provider_name = provider_info[NAME_KEY]
    connector_link = get_connector_provider_url(provider_info[ID_KEY], connector_id)
    connector_md = open_md(f"connectors_md/{connector_name}{provider_name}.md")
    page_parameters()[MD_CONTENT_PARAM_KEY] = connector_md
    page_parameters()[CONNECTOR_URL_PARAM_KEY] = connector_link

def get_granted_tables(database, schema):
    check_command = f"SELECT {TABLE_NAME_KEY} FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{schema}';"
    granted_tables = sp_session.sql(check_command).collect()
    granted_tables_list = [row[0] for row in granted_tables]
    return granted_tables_list

def verify_change_tracking(database, schema):
    stored_procedure_fullname = f"{APPLICATION}.{USER_SETTINGS_SCHEMA}.{SHOW_TABLES_KEY}"
    non_change_tracking_tables = sp_session.call(stored_procedure_fullname, database, schema)
    return ast.literal_eval(non_change_tracking_tables)

def get_chage_tracking_commands(database, schema, non_change_tracking_tables):
    check_change_tracking = "ALTER TABLE {database}.{schema}.{table} SET CHANGE_TRACKING = TRUE;"
    command_list = [USE_ADMIN_ROLE_COMMAND]
    for table in non_change_tracking_tables:
        command = check_change_tracking.format(database = database, schema = schema, table = table)
        command_list.append(command)
    return NEW_LINE.join(command_list)

def back_component_settings(substep1_bold = False, substep2_bold = False, substep3_bold = False):
    back_state = page_parameters()[LAST_STATE_KEY]
    if back_state == LINK_TO_YOUR_DATA_STATE_KEY:
        st.session_state[PAGE_INFO_KEY][PARAMS_KEY][SUBSTEPS_PARAM_KEY] = None
    else:
        set_page_substeps(substep1_bold, substep2_bold, substep3_bold)
    update_page_state(back_state)

def get_needed_grants():
    needed_grants = f"""
        {USE_ADMIN_ROLE_COMMAND}
        GRANT USAGE ON DATABASE <DATABASE_NAME> TO APPLICATION {APPLICATION};
        GRANT USAGE ON SCHEMA <DATABASE_NAME>.<SCHEMA_NAME> TO APPLICATION {APPLICATION};
        GRANT SELECT ON ALL TABLES IN SCHEMA <DATABASE_NAME>.<SCHEMA_NAME> TO APPLICATION {APPLICATION};
    """
    return needed_grants

def store_user_selections(database, schema, connector):
    page_parameters()[USER_SELECTIONS_KEY] = {
        DATABASE_KEY       : database,
        SCHEMA_KEY         : schema,
        CONNECTOR_NAME_KEY : connector
    }

def get_connector_id_by_name(connector_name):
    connector_id_query = f"SELECT {ID_KEY} FROM {APPLICATION}.{CONFIGURATION_SCHEMA}.{CONNECTORS_TABLE} WHERE {NAME_KEY} = '{connector_name}'"
    connector_id_result = execute_sql_query(sp_session, connector_id_query)
    connector_id = connector_id_result[0][ID_KEY]
    return connector_id

def insert_user_settings():
    user_selections = page_parameters()[USER_SELECTIONS_KEY]
    provider_id = page_parameters()[PROVIDER_INFO_PARAM_KEY][ID_KEY]
    connector_id = get_connector_id_by_name(user_selections[CONNECTOR_NAME_KEY])
    insert_into_existing_sources = f"""
    INSERT INTO {APPLICATION}.{USER_SETTINGS_SCHEMA}.{EXISTING_SOURCES_TABLE} 
    SELECT {provider_id}, {connector_id}, '{user_selections[DATABASE_KEY]}', '{user_selections[SCHEMA_KEY]}', '{datetime.now()}'
    WHERE NOT EXISTS (
        SELECT 1 FROM {APPLICATION}.{USER_SETTINGS_SCHEMA}.{EXISTING_SOURCES_TABLE}
        WHERE PROVIDER_ID = {provider_id} AND CONNECTOR_ID = {connector_id} AND DATABASE = '{user_selections[DATABASE_KEY]}' AND SCHEMA = '{user_selections[SCHEMA_KEY]}'
    )
    """
    execute_sql_query(sp_session, insert_into_existing_sources)

def tab_change():
    st_components.html(f"""
    <script>
        frameElement.parentElement.style.display = 'none';
        window.parent.document.querySelector('div[role="tablist"]').children[1].click();
        frameElement.remove()
    </script>
    """, height=0)

def deactivate_non_selected_tab():
    st.markdown('''
    <style>
        div[role="tablist"] button[aria-selected="false"] {
            opacity: .6;
            pointer-events: none;
        }
    </style>
    ''', unsafe_allow_html=True)

def store_user_selections(database, schema, connector):
    page_parameters()[USER_SELECTIONS_KEY] = {
        DATABASE_KEY : database,
        SCHEMA_KEY : schema,
        CONNECTOR_NAME_KEY : connector
    }
