import streamlit as st
import globals as g
import components
import modules

from typing import List
from components.mappings.custom_mapping import custom_mapping_component
from components.mappings.target_model_selector import target_model_selector_component
from components.mappings.mapping_table import MappingTable
from dtos.mapping_model import MappingModel
from dtos.table_model import TableModel
from modules_backend.mappings_backend import generate_unified_model, generate_aggregated_model, generate_standardize_model, get_columns_info_schema
from dtos.dynamic_table import DynamicTableParams
from snowflake.snowpark.session import Session
from globals import *
from enums.pages import Pages
from utils.model_helpers import section_header
from modules.pages import get_page_params
from components.custom_spinner import custom_spinner
from services.i18n import Translator


# TODO import will be deleted when zamboni is added
from components.mappings.mock_mapping_model import MockTargetUnifiedModel, MockFacebookFivetran, MockLinkedInOmnata

t = Translator().translate


def customize_mappings_page(sp_session: Session):
    selected_model = _get_selected_model()

    if selected_model is None:
        default_model = MappingModel('CAMPAIGN_INTELLIGENCE_COMBINED', 'Unified Marketing Data Model')
        _render_target_models(models=[default_model])
    else:
        _get_model_info_schemas(sp_session, selected_model)
        _render_custom_mapping(model=selected_model)


def clear_selected_model() -> None:
    if SELECTED_MODEL_KEY in st.session_state:
        del st.session_state.selected_model


def _render_target_models(models: List[MappingModel]) -> None:
    section_header(t("CustomMapSelectTargetModelTitle"))
    for model in models:
        selected_model = _get_selected_model()
        is_selected =  selected_model is not None and selected_model.id == model.id 
        target_model_selector_component(
            model=model, 
            selected=is_selected, 
            on_select=_select_model_handler, 
            on_confirm=_continue_handler)


def _render_custom_mapping(model: MappingModel) -> None:
    components.button(t('CustomMapBackBtn'), on_click=clear_selected_model)
    components.subtitle(t('CustomMapCustomizedMappingsTitle'))
    _render_header(model)
    custom_mapping_component(model)
    apply = components.button(t('CustomMapApplyContinueBtn'), type='primary', on_click=_continue_handler, kwargs={'model': model})
    if apply:
        st.session_state[MODEL_INFORMATION_KEY] = { DATABASE_KEY : APPLICATION, SCHEMA_KEY : AGGREGATED_REPORTS_KEY }
        modules.switch_page(Pages.DataExplorer)


def _render_header(model: MappingModel) -> None:
    header_key = 'custom_mapping_header'
    container = components.key_container(header_key, class_name=header_key)
    src_db, trg_db = container.columns(2)
    with src_db:
        st.markdown(t('CustomMapSourceDBSchemaHeader').format(model.source_schema))
    with trg_db:
        st.markdown(t('CustomMapTargetDBSchemaHeader').format(model.target_schema))
    
    st.empty().markdown(f"""
    <style>
        .{header_key} > div:nth-child(2) {{
            text-align: end;
        }}
    </style>
    """, unsafe_allow_html=True)


def _select_model_handler(model: MappingModel, selected: bool) -> None:
    st.session_state.selected_model = model if not selected else None


def _continue_handler(model) -> None:
    with custom_spinner():
        generate_unified_model(DynamicTableParams( get_page_params()[USER_SELECTIONS_KEY][CONNECTOR_NAME_KEY].lower(), 
                                                get_page_params()[PROVIDER_INFO_PARAM_KEY][NAME_KEY].lower(),
                                                get_page_params()[USER_SELECTIONS_KEY][DATABASE_KEY], 
                                                get_page_params()[USER_SELECTIONS_KEY][SCHEMA_KEY]))
        generate_aggregated_model()
        generate_standardize_model(DynamicTableParams( get_page_params()[USER_SELECTIONS_KEY][CONNECTOR_NAME_KEY], 
                                                get_page_params()[PROVIDER_INFO_PARAM_KEY][NAME_KEY],
                                                get_page_params()[USER_SELECTIONS_KEY][DATABASE_KEY], 
                                                get_page_params()[USER_SELECTIONS_KEY][SCHEMA_KEY]))



def _get_selected_model() -> MappingModel:
    return st.session_state.selected_model if SELECTED_MODEL_KEY in st.session_state else None


def _get_model_info_schemas(sp_session, model: MappingModel) -> MappingModel:
    page_params = modules.pages.get_page_params()

    if (g.USER_SELECTIONS_KEY not in page_params): return model

    provider = page_params[g.PROVIDER_INFO_PARAM_KEY][g.NAME_KEY]
    connector = page_params[g.USER_SELECTIONS_KEY][g.CONNECTOR_NAME_KEY]

    source_params = page_params[g.USER_SELECTIONS_KEY]
    source_db = source_params[g.DATABASE_KEY]
    source_schema = source_params[g.SCHEMA_KEY]

    target_db = g.APPLICATION
    target_schema = g.UNIFIED_MODEL_SCHEMA

    model.source_schema = f'{source_db}.{source_schema}'
    model.target_schema = f'{target_db}.{target_schema}'
    
    source_columns = get_columns_info_schema(sp_session, source_db, source_schema)
    target_columns = MockTargetUnifiedModel
    
    for table in source_columns:
        model.add_source_column(table[g.TABLE_NAME_KEY], table[g.COLUMN_NAME_KEY])

    for table in target_columns:
        model.target_tables.append(TableModel(**table))

    model.mappings = _get_mappings(provider, connector)
    
    return model


def _get_mappings(provider: str, connector: str) -> List[List[str]]:
    mapping = []
    if provider == 'LinkedIn' and connector == 'Omnata':
        mapping = MockLinkedInOmnata
    elif provider == 'Facebook' and connector == 'Fivetran':
        mapping = MockFacebookFivetran
    return mapping
