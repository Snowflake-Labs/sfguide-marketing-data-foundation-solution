import streamlit as st
from snowflake.snowpark import dataframe as df

STARTED = 'started'
SUSPENDED = 'suspended'
TASK_COLUMNS_SELECT = ['"name"', '"id"', '"schedule"', '"database_name"', '"schema_name"', '"created_on"', '"definition"']


@st.cache_data(
    ttl=3600, # clears cache after one hour
    show_spinner='Fetching suspended tasks...')
def get_suspended_tasks(_sp_session):
    return _sp_session.sql('SHOW TASKS').select(TASK_COLUMNS_SELECT).where(df.col('"state"') == SUSPENDED).collect()


@st.cache_data(
    ttl=3600, # clears cache after one hour
    show_spinner='Fetching active tasks...')
def get_active_tasks(_sp_session):
    return _sp_session.sql('SHOW TASKS').select(TASK_COLUMNS_SELECT).where(df.col('"state"') == STARTED).collect()


@st.cache_data(
    ttl=3600, # clears cache after one hour
    show_spinner='Fetching tasks...')
def get_all_tasks_names(_sp_session):
    return _sp_session.sql('SHOW TASKS').select(['"name"', '"state"']).collect()


@st.cache_data(
    ttl=3600, # clears cache after one hour
    show_spinner='Fetching store procedures...')
def get_callable_procedures(_sp_session):
    # TODO review catalog_name where clause
    return _sp_session.sql('SHOW PROCEDURES').select('"name"').where(df.col('"catalog_name"') == 'DATA_HARMONIZATION').collect()


def clear_tasks_cache():
    get_active_tasks.clear()
    get_suspended_tasks.clear()
    get_all_tasks_names.clear()


def create_task_query(task_name: str, procedure_name: str, cron: str) -> str:
    query = f"CREATE OR REPLACE TASK {task_name}\n\
        SCHEDULE = 'USING CRON {cron} UTC'\n\
        AS CALL {procedure_name}();"
    return query


def try_create_task(sp_session, task_query: str):
    try:
        request = sp_session.sql(task_query).collect()
        return request[0]['status']
    except:
        # TODO return a more user frendly error
        return 'Error: something went wrong while creating the task'


def set_task_state(sp_session, task_name: str):
    state = 'RESUME' if st.session_state.task_state else 'SUSPEND'
    task_query = f"ALTER TASK IF EXISTS {task_name} {state}"
    result = sp_session.sql(task_query).collect()
    clear_tasks_cache()


def is_task_started(state: str) -> bool:
    return state == STARTED
