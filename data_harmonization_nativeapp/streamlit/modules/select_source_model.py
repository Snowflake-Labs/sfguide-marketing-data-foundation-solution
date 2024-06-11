import streamlit as st
import components

from components.error_handler import errorHandling
from enums.pages import Pages
from modules.pages import switch_page
from modules_backend.select_source_model_backend import *
from services.i18n import Translator
from utils.model_helpers import center_components, connect_to_snowflake

t = Translator().translate
sp_session = connect_to_snowflake()

@errorHandling
def select_source_model_page():
    # Generate add new source section
    components.title(t("AddNewSource"))
    providers_info = get_providers_info(sp_session)
    generate_provider_columns(providers_info)

    # Generate existing sources section
    existing_sources_list = get_existing_sources_info(sp_session)
    if existing_sources_list:
        components.title(t("ExistingSources"))
        for source in existing_sources_list:
            generate_existing_source_container(source)

def generate_provider_columns(providers_list):
    num_groups = (len(providers_list) + 2) // 3
    grouped_providers_list = [providers_list[i*3:i*3+3] + [None]*(3-len(providers_list[i*3:i*3+3])) for i in range(num_groups)]
    for provider_group in grouped_providers_list:
        col1, col2, col3 = st.columns(3)
        fill_col_container(col1, provider_group[0])
        fill_col_container(col2, provider_group[1])
        fill_col_container(col3, provider_group[2])

def fill_col_container(col, provider):
    if provider:
        with col:
            generate_provider_selector_container(provider)

def generate_provider_selector_container(provider_info):
    center_components()
    provider_id = provider_info["ID"]
    disabled= provider_id in blocked_providers
    opacity = "opacity: 50%" if disabled else "opacity: 100%"
    with components.container(key = f"selector_container{provider_id}", customStyle=opacity):
        image_col, text_col, button_col = st.columns([1,3,1])       
        with image_col:
            image_col.image(provider_info["IMAGE"])
        with text_col:
            components.text_medium(provider_info['NAME'])
        with button_col:
            clicked = components.button(t("AddButton"), key=f"Add-{provider_id}", disabled=disabled)
            if clicked:
                switch_page(Pages.AddPlatformAnalyticsModelPage, {
                        PROVIDER_INFO_PARAM_KEY : provider_info,
                        LINK_TO_DATA_KEY        : LINK_TO_YOUR_DATA_STATE_KEY,
                        DATA_MODE_KEY           : ADD_MODE_KEY
                    })
                st.experimental_rerun()

def generate_existing_source_container(source):
    center_components()
    provider_name = source["PROVIDER_NAME"]
    connector_name = source["CONNECTOR_NAME"]
    provider_image = source["PROVIDER_IMAGE"]
    source_database = source['DATABASE_NAME']
    source_schema = source['SCHEMA_NAME']
    key = f"{provider_name}-{connector_name}-{source_database}-{source_schema}"
    with components.container(key = f"selector_container-{key}"):
        info_col, dates_col, provider_col, connector_col, button_col = st.columns([13,15,2,2,3])
        with info_col:
            components.text_medium_bold(f"{provider_name} + {connector_name}")
            components.text_small(f"{source_database}.{source_schema}", color=DARK_GRAY_1)
        with dates_col:
            components.text_small(f"{t('CreatedDate')}: {source[CREATED_DATE_KEY]}", color=DARK_GRAY_1)
        with provider_col:
            provider_col.image(provider_image)
        with connector_col:
            connector_col.image(source["CONNECTOR_IMAGE"])
        with button_col:
            clicked = components.button(t("EditButton"), key = f"Edit-{key}", type='primary')
            if clicked:
                provider_id = get_provider_id_by_name(sp_session, provider_name)
                provider_info = generate_provider_info_dict(provider_id, provider_name, provider_image)
                user_selections = { DATABASE_KEY : source_database, SCHEMA_KEY : source_schema, CONNECTOR_NAME_KEY : connector_name }
                switch_page(Pages.AddPlatformAnalyticsModelPage, {
                        PROVIDER_INFO_PARAM_KEY : provider_info,
                        LINK_TO_DATA_KEY        : LINK_TO_YOUR_DATA_STATE_KEY,
                        DATA_MODE_KEY           : EDIT_MODE_KEY,
                        USER_SELECTIONS_KEY     : user_selections
                    })