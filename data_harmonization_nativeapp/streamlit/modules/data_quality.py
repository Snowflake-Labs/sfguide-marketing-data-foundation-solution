import streamlit as st
import components

from components.error_handler import errorHandling
from services.i18n import Translator
import webbrowser
import uuid

from modules_backend.data_quality_backend import notebook_urls

t = Translator().translate

@errorHandling
def data_quality_page():
    components.title(t('DataQuality'))

    
    notebook_container(t('DataQualityStarter'),t("DataQualityStarterDesc"),notebook_urls()[1])
    notebook_container(t('DataQualityStarter2'),t('DataQualityStarter2Desc'), notebook_urls()[2])
    notebook_container(t('DataQualityStarter3'),t('DataQualityStarter3Desc'), notebook_urls()[3])

    
def notebook_container(id, description, notebook):
    style = "display: flex; gap: 16px;"
    with components.container(key = f"selector_container_1", customStyle=style):
        components.text_medium(id)
        description_col,middle,button_col = st.columns([0.9,0.1,0.2])
        with description_col:
            components.text_medium(description)
        with button_col:
           st.markdown(f'[{t("OpenButton")}]({notebook})')