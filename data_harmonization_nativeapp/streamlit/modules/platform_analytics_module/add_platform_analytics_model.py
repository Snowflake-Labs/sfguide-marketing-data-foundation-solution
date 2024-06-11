import streamlit as st
import components

from components.mappings.customize_mappings import customize_mappings_page
from components.error_handler import errorHandling
from modules.platform_analytics_module.connector_setup_section import connector_setup_section
from modules.platform_analytics_module.data_already_in_snowflake_section import data_already_in_snowflake_section
from modules.platform_analytics_module.link_to_your_data_section import link_to_your_data_section
from modules.platform_analytics_module.select_connector_section import select_connector_section
from modules_backend.add_platform_analytics_model_backend import *
from utils.model_helpers import center_components

@errorHandling
def add_platform_analytics_model_page():
    center_components()
    provider_info = page_parameters()[PROVIDER_INFO_PARAM_KEY]
    title_col, image_col, _ = st.columns([4, 1, 12])
    with title_col:
        components.title(translate("AddPlatformAnalytics").format(provider_info[NAME_KEY]))
    image_col.image(provider_info[IMAGE_KEY])
    data_mode_key = page_parameters()[DATA_MODE_KEY]
    if data_mode_key == ADD_MODE_KEY:
        add_mode_section(provider_info)
    elif data_mode_key == EDIT_MODE_KEY:
        customize_mappings_page(sp_session)

def add_mode_section(provider_info):
    deactivate_non_selected_tab()
    with components.key_container('PageTabs'):
        link_data_tab, customize_mappings_tab = st.tabs([f"⒈ {translate('LinkDataInSnowflake')}", f"⒉ {translate('CustomizeMappings')}"])
    with link_data_tab:
         generate_link_data_tab_content(provider_info[ID_KEY])
    with customize_mappings_tab:
        customize_mappings_page(sp_session)

def generate_link_data_tab_content(provider_id):
    if page_parameters()[LINK_TO_DATA_KEY] == LINK_TO_YOUR_DATA_STATE_KEY:
        link_to_your_data_section()
    elif page_parameters()[LINK_TO_DATA_KEY] == SELECT_CONNECTOR_STATE_KEY:
        select_connector_section(provider_id)
    elif page_parameters()[LINK_TO_DATA_KEY] == CONNECTOR_SETUP_STATE_KEY:
        connector_setup_section()
    elif page_parameters()[LINK_TO_DATA_KEY] == DATA_ALREADY_IN_SNOWFLAKE_STATE_KEY:
        data_already_in_snowflake_section()