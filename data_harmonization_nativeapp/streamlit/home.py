import streamlit as st
st.set_page_config(
    page_title="Snowflake Marketing Cloud",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://quickstarts.snowflake.com/', # TODO REPLACE FOR the actual documentation link
        'Report a bug': "https://community.snowflake.com/s/forum", 
        'About': """## Snowflake Martketing Data Cloud.
        Version 1.0.0
Solution Innovation Team
          """
    }
)
import modules
import components

from enums.pages import Pages
from utils.resources import SnowflakeIcon
from utils.assets import get_asset_path


def render_page():
    # Page state switch
    if 'page_info' not in st.session_state: 
        st.session_state['page_info'] = {}
        modules.switch_page(Pages.HomePage)    
    page = st.session_state['page_info']['page']
    if page == Pages.SelectSourceModelPage:
        modules.select_source_model_page()
    elif page == Pages.AddPlatformAnalyticsModelPage:
        modules.add_platform_analytics_model_page()
    elif page == Pages.DataQualityPage:
        modules.data_quality_page()
    elif page == Pages.DataExplorer:
        modules.data_explorer_page()
    elif page == Pages.AIAssistant:
        modules.chat_assistant_page()
    else:
        home_page()


def home_page():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image(SnowflakeIcon(), width= 420)

    home_file = get_asset_path('./home.md')
    with open(home_file) as content:
        st.markdown(content.read())


def openPage(page: str):
    modules.switch_page(page)


def main():
    components.side_navigation_bar_component(openPage)
    render_page()

if __name__ == '__main__':
    main()
