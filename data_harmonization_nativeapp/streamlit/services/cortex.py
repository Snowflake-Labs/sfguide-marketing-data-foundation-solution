import json
import streamlit as st
import services.permissions as privileges


def get_mapping_query(src_columns_promt: str, target_columns_promt: str):
    user_prompt = f"'Give me a recomentation to map the next set of source columns {src_columns_promt} \
        with the next set of taget columns {target_columns_promt}'"

    system_prompt = "'You are gonna receive two sets of columns a source and a target, they are not ordered and can have diferent sizes. Also, add the similarity between each individual column mapping that goes from 0 to 1. Do not reply using a complete sentence, and only give the answer in JSON format like the next one: {\"mappings\": [{\"source\": \"column name\",\"target\": \"column name\",\"similarity\": x}]}'"

    cortex_query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE(\n\t'llama2-70b-chat',\n\t[\n\t\t{{'role': 'system', 'content': {system_prompt}}},\n\t\t{{ 'role': 'user', 'content': {user_prompt}}}\n\t],\n\t{{ 'temperature': 0, 'top_p': 0 }}) as response;"

    return cortex_query


def generate_transform_function_sample(function_name: str, in_type: str, out_type: str, language: str):
    user_prompt = f"'Give me a function named {function_name} with one input argument of type {in_type} \
        that returns a value of type {out_type} in the coding language {language}'"

    system_prompt = "'Do not reply using a complete sentence, and only give the answer in JSON format like the next one: {{\"code\": \"generated code\", \"comments\": any other text\"}}'"

    cortex_query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE(\n\t'llama2-70b-chat',\n\t[\n\t\t{{'role': 'system', 'content': {system_prompt}}},\n\t\t{{ 'role': 'user', 'content': {user_prompt}}}\n\t],\n\t{{ 'temperature': 0, 'top_p': 0 }}) as response;"

    return cortex_query


@st.cache_data(show_spinner='Fetching cortex recomendation...',)
def query_cortex_cache(_sp_session, cortex_query: str):
    has_privilege = privileges.request_account_privileges([privileges.SNOWFLAKEDB])
    if not has_privilege: return ''
    response = _sp_session.sql(cortex_query).collect()
    return response[0].as_dict()['RESPONSE'] if len(response) > 0 else ''


# Extract the response message from a cortext response
def get_response_message(json_response: str):
    try:
        return json.loads(json_response)['choices'][0]['messages']
    except:
        return None # TODO
