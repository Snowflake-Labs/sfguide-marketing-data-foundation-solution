import streamlit as st
from services.i18n import Translator

t = Translator().translate


def custom_spinner():
    st.markdown("""
    <style>
    div.stSpinner > div {
        text-align:center;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
  }
    div[data-testid="PageTabs"]{
                    display: none;
    } 
    </style>""", 
    
    unsafe_allow_html=True)
    return st.spinner(f"{t('BuildinModels')}")