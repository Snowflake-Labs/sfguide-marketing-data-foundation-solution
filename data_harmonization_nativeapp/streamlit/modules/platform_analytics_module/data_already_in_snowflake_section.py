import components

from components.mappings.customize_mappings import clear_selected_model
from modules_backend.add_platform_analytics_model_backend import *
from snowflake.snowpark.functions import col, lit

def data_already_in_snowflake_section():
    section_header(translate("LinkDataAlreadyInSnowflake"))
    database_col, schema_col, connector_col = st.columns(3)
    with database_col:
        databases = sp_session.sql('SHOW DATABASES').select(QUOTED_NAME_KEY).where(col(QUOTED_NAME_KEY)!=lit(APPLICATION)).collect()
        selected_database = st.selectbox(translate('SelectorDatabase'), databases)
    with schema_col:
        try:
            schemas = sp_session.sql(f'SHOW SCHEMAS IN {selected_database}').select(QUOTED_NAME_KEY).where(col(QUOTED_NAME_KEY)!=lit(INFORMATION_SCHEMA)).collect()
            selected_schema = st.selectbox(translate('SelectorSchema'), schemas)
        except:
            selected_schema = st.selectbox(translate('SelectorSchema'), [])
    with connector_col:
        provider_id = page_parameters()[PROVIDER_INFO_PARAM_KEY][ID_KEY]
        connectors_info = get_connectors_list(provider_id)
        connectors_names = [value for sublist in connectors_info for value in sublist[1::2]]
        selected_connector = st.selectbox(translate('ConnectorUsed'), connectors_names)
    create_dont_see_your_data_expander()
    display_grants_action_section(selected_database, selected_schema, selected_connector)

def create_dont_see_your_data_expander():
    with st.expander(translate("DontSeeYourData")):
        components.text_small(translate("RunFollowingCommand"))
        st.code(language='sql', body = get_needed_grants())
        refresh = components.button(translate("ReloadData"))
        if refresh:
            st.experimental_rerun()

def display_grants_action_section(selected_database, selected_schema, selected_connector):
    if GRANTED_TABLES_KEY not in page_parameters() or not page_parameters()[GRANTED_TABLES_KEY]:
        validate_grants_section(selected_database, selected_schema)
    else:
        store_user_selections(selected_database, selected_schema, selected_connector)
        display_granted_tables_section()

def validate_grants_section(selected_database, selected_schema):
    if ERROR_MESSAGE_KEY in page_parameters():
        st.error(f":x: {page_parameters()[ERROR_MESSAGE_KEY]}")
        del page_parameters()[ERROR_MESSAGE_KEY]
    back_button_col, next_button_col, _ = st.columns([1, 1, 15])
    with back_button_col:
        go_back = components.button(translate("BackButton"))
        if go_back:
            back_component_settings(substep2_bold = True)
    with next_button_col:
        continue_button = components.button(translate("ConnectButton"), key="ConnectButton", type="primary")
    if continue_button:
        with st.spinner(f"{translate('LoadingMessage')}..."):
            granted_tables = get_granted_tables(selected_database, selected_schema)
            if len(granted_tables) > 0:
                non_change_tracking_tables = verify_change_tracking(selected_database, selected_schema)
                if non_change_tracking_tables:
                    commands = get_chage_tracking_commands(selected_database, selected_schema, non_change_tracking_tables)
                    st.error(f":x: {translate('ChangeTrackingNotEnabled')} [{translate('LearnMore')}]({CHANGE_TRACKING_DOCUMENTATION})")
                    st.code(language='sql', body = commands)
                else:
                    page_parameters()[GRANTED_TABLES_KEY] = granted_tables
                    st.experimental_rerun()
            else:
                page_parameters()[ERROR_MESSAGE_KEY] = translate('NotConnected')
                st.experimental_rerun()

def display_granted_tables_section():
    st.success(f":white_check_mark: {translate('SuccessfullyConnected')}")
    components.text_medium_bold(translate("TablesFound"))
    st.dataframe({translate("TableName") : page_parameters()[GRANTED_TABLES_KEY]}, hide_index = True, use_container_width=True)
    with components.key_container('JumpToCustomizeMappings'):
        back_button_col, next_button_col, _ = st.columns([1, 1, 15])
    with back_button_col:
        go_back = components.button(translate("BackButton"))
        if go_back:
            page_parameters()[GRANTED_TABLES_KEY] = None
            back_component_settings(substep2_bold = True)
    with next_button_col:
        clicked = components.button(translate("ContinueButton"), key="ContinueButton", type="primary", on_click = tab_jump_settings)
        if clicked:
            insert_user_settings()
            clear_selected_model()
            tab_change()

def tab_jump_settings(): 
    page_parameters()[SUBSTEPS_PARAM_KEY] = None
    