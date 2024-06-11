import json
import streamlit as st


# Extracts a list of key-value pair of the column_name with column_type from a DataFrame.Row
def get_column_name_with_type(rows):
    result = []
    for row in rows:
        col_name = row['column_name']
        col_type = json.loads(row['data_type'])['type']
        result.append({'col': col_name, 'type': col_type})
    return result
