import pandas as pd
import streamlit as st


def data_mapper_table(data: dict, src_cols_types: list, target_cols_types: list, functions: list):
    get_type = lambda li, col: next((x['type'] for x in li if x['col'] == col), None)
    src_cols = list(map(lambda x: f"{x['source']} ({get_type(src_cols_types, x['source'])})", data))
    target_cols = list(map(lambda x: f"{x['target']} ({get_type(target_cols_types, x['target'])})", data))
    similarity_cols = list(map(lambda x: x['similarity'] if 'similarity' in x else 0, data))
    data_template = lambda src, target, s: {
        'selected': True, 
        'source': src,
        'transform': '',
        'target':  target,
        'similarity': s }
    data = list(map(data_template, src_cols, target_cols, similarity_cols))

    df = pd.DataFrame(data)

    columns_template = {
        'selected': st.column_config.CheckboxColumn(
            '',
            width='small'
        ),
        'source': st.column_config.SelectboxColumn(
            'Source column',
            options = src_cols,
            required = True,
        ),
        'transform': st.column_config.SelectboxColumn(
            'Transform function',
            options = functions
        ),
        'target': st.column_config.SelectboxColumn(
            'Target column',
            options = target_cols,
            required = True,
        ),
        'similarity': st.column_config.ProgressColumn(
            'Similarity',
            width='small',
            format='%f',
            min_value=0,
            max_value=1
        )
    }

    data_editor = st.data_editor(df,
        hide_index=True, 
        use_container_width=True, 
        column_config=columns_template)

    return data_editor
