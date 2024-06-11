import components

from enums.pages import Pages
from modules.pages import switch_page
from modules_backend.add_platform_analytics_model_backend import *
from utils.model_helpers import center_components
from utils.resources import get_cloud_upload_icon, get_database_icon

def link_to_your_data_section():
    section_header(translate("LinkToYourData"))
    page_parameters()[LAST_STATE_KEY] = LINK_TO_YOUR_DATA_STATE_KEY
    bring_data_col, link_data_col = st.columns(2)
    with bring_data_col:
        bring_data = generate_data_selection_container(get_cloud_upload_icon(), key_to_translate = "BringDataIntoSnowflake")
        if bring_data:
            set_page_substeps(bold1 = True)
            update_page_state(SELECT_CONNECTOR_STATE_KEY)
    with link_data_col:
        link_data = generate_data_selection_container(get_database_icon(), key_to_translate = "LinkDataAlreadyInSnowflake")
        if link_data:
            update_page_state(DATA_ALREADY_IN_SNOWFLAKE_STATE_KEY)
    should_go_back = components.button(translate("BackButton"), key="back")
    if should_go_back:
        switch_page(Pages.SelectSourceModelPage)


def generate_data_selection_container(container_image, key_to_translate):
    center_components()
    with components.container(key = key_to_translate):
        image_col, text_col, button_col = st.columns([1, 8, 2])
        image_col.image(container_image)
        with text_col:
            components.text_medium(translate(key_to_translate))
        with button_col:
            clicked = components.button(translate("SelectButton"), key=f'{key_to_translate}_btn')
        return clicked