import streamlit as st
import streamlit.components.v1 as components

from components.mappings.mapping_table import MappingTable
from components.mappings.collapsible_sidebar import CollapsibleSideBar
from dtos.mapping_model import MappingModel
from services.i18n import Translator


t = Translator().translate


def custom_mapping_component(model: MappingModel):
    mapping_table = MappingTable(key='custom_mapping_table', data=model.mappings)
    source_schema = CollapsibleSideBar(
        label=t('CustomMapSourceSchemaHeader'), 
        key='source_schema_side_bar',
        orientation='left', 
        data=model.source_tables,
        mappings=[i[0].lower() for i in model.mappings])
    target_schema = CollapsibleSideBar(
        label=t('CustomMapTargetSchemaHeader'), 
        key='target_schema_side_bar',
        orientation='right', 
        data=model.target_tables,
        mappings=[i[1].lower() for i in model.mappings])

    components.html(f'''
    <div class="custom_mapping_container">
        {_render_stylesheet()}
        {source_schema.render()}
        {mapping_table.render()}
        {target_schema.render()}
    </div>
    ''', height=800)


def _render_stylesheet() -> str:
    return f'''
    <style>
        .custom_mapping_container {{
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            justify-content: space-between;
            gap: 24px;

            font-family: sans-serif;
            color: #262730;
        }}
    </style>
    '''
