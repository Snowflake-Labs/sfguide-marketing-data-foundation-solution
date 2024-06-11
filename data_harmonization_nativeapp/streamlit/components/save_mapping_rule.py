import streamlit as st
from components.sf_object_selector import ObjectSelector
from utils.mapping_helpers import generate_mapping_rule


def save_mapping_rule_component(sp_session, src_table_name: str, target_table_name: str, data_mapper):
    col1, col2 = st.columns(2)
    with col1:
        mapping_name = st.text_input('Set a mapping rule name', placeholder='default_mapping_name', max_chars=20)
    with col2:
        language = st.selectbox('select output language', ('yaml', 'json'))
    map_rule = generate_mapping_rule(
        mapping_name, 
        src_table_name, 
        target_table_name, 
        data_mapper, 
        language)
    st.code(map_rule, language)


    col1, col2, col3 = st.columns(3)
    with col1:
        database = ObjectSelector(sp_session, 'Select a database', 'show databases', 'save-db').render()
    with col2:
        schema_query = f'show schemas in {database}'
        schema = ObjectSelector(sp_session, 'Select a schema', schema_query, 'save-schema').render()
    with col3:
        stage_query = f'show stages in {database}.{schema}'
        stage = ObjectSelector(sp_session, 'Select a stage', stage_query, 'save-stage').render()

    if st.button('Save mapping rule', type='primary') and mapping_name:
        return # TODO