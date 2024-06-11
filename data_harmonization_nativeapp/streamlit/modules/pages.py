import streamlit as st
from enums.pages import Pages


def switch_page(page : Pages, params : dict = {}) -> None:
    st.session_state.page_info = { 'page': page, 'params': params }
    st.experimental_rerun() # TODO will deprecate in future Streamlit version


def get_current_page() -> Pages:
    return st.session_state.page_info['page'] if 'page_info' in st.session_state else Pages.HomePage


def get_page_params() -> dict:
    return st.session_state.page_info['params'] if 'page_info' in st.session_state else {}
