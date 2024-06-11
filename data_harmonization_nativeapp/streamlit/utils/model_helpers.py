import streamlit as st
import components

from services.session import session


@st.cache_data
def execute_sql_query(_sp_session, query):
    result = _sp_session.sql(query)
    return result.collect()  

@st.cache_resource
def connect_to_snowflake():
    return session()

def section_header(text):
    components.subtitle(text)

def center_components():
    style = """
            <style>
                [data-testid="stHorizontalBlock"] {
                    align-items: center;
                }
            </style>
            """
    st.markdown(style,unsafe_allow_html=True)