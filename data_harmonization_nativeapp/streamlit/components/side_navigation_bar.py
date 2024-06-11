import streamlit as st
import components
import modules

from enums.pages import Pages
from globals import *
from utils.resources import SidebarLogo
from services.i18n import Translator
from utils.resources import SidebarLogo

def side_navigation_bar_component(callback):
    t = Translator().translate
    with st.sidebar:
        st.image(SidebarLogo())

        mappingIcon = 'icons/add_circle.svg'
        analyticsIcon = 'icons/insert_chart.svg'
        chatIcon = 'icons/chat.svg'
        checkBoxIcon = 'icons/check_box.svg'

        selecte_page = modules.pages.get_current_page()
        if _render_sidebar_button(f'{t("SideBarSelectSource")}', key='sidebar_maps', icon_name=mappingIcon, 
            is_active=selecte_page == Pages.SelectSourceModelPage):
            callback(Pages.SelectSourceModelPage)
        if _render_sidebar_button(f' {t("SideBarDataQuality")}', key='sidebar_quality', icon_name=checkBoxIcon, 
            is_active=selecte_page == Pages.DataQualityPage):
            callback(Pages.DataQualityPage)
        if _render_sidebar_button(f'{t("SideBarDataExplorer")}', key='sidebar_data_explorer', icon_name=analyticsIcon, 
            is_active=selecte_page == Pages.DataExplorer):
            callback(Pages.DataExplorer)
        if _render_sidebar_button(f'{t("AIAssistant")}', key='sidebar_ai_assistant', icon_name=chatIcon, 
            is_active=selecte_page == Pages.AIAssistant):
            callback(Pages.AIAssistant)
        generate_page_substeps()
        st.divider()
        st.caption(t("SideBarCaption"))


def _render_sidebar_button(text: str, key: str, icon_name: str, is_active: bool) -> bool:
    active_style = "background-color: #E6EAF1; p { font-weight: 600; }"

    style = f"""
        justify-content: flex-start;
        background-color: transparent;
        border: none;
        
        {active_style if is_active else ''}

        &:hover {{{active_style}}}
    """
    icon = components.Icon(icon_name, alignment='left')
    return components.button(text, styles=style, key=key, icon=icon, use_container_width=True)


def generate_page_substeps():
    if PAGE_INFO_KEY in st.session_state:
        page_params = st.session_state[PAGE_INFO_KEY][PARAMS_KEY]
        if SUBSTEPS_PARAM_KEY in page_params and page_params[SUBSTEPS_PARAM_KEY]:
            substeps_list = page_params[SUBSTEPS_PARAM_KEY]
            st.divider()
            for substep in substeps_list:
                text = substep[TEXT_KEY]
                is_bold = substep[IS_BOLD_KEY]
                if is_bold: components.text_medium_bold(text) 
                else: components.text_medium(text)
