import components

from modules_backend.add_platform_analytics_model_backend import *
from utils.model_helpers import center_components

def select_connector_section(provider_id):
    section_header(translate("SelectConnector"))
    page_parameters()[LAST_STATE_KEY] = LINK_TO_YOUR_DATA_STATE_KEY
    connectors_list = get_connectors_dictionaries(provider_id)
    generate_connector_columns(connectors_list)
    go_back = components.button(translate("BackButton"))
    if go_back:
        back_component_settings()

def generate_connector_columns(connectors_list):
    num_groups = (len(connectors_list) + 2) // 3
    grouped_connectors_list = [connectors_list[i*3:i*3+3] + [None]*(3-len(connectors_list[i*3:i*3+3])) for i in range(num_groups)]
    for connectors_group in grouped_connectors_list:
        col1, col2, col3 = st.columns(3)
        generate_column_connector(col1, connectors_group[0])
        generate_column_connector(col2, connectors_group[1])
        generate_column_connector(col3, connectors_group[2])

def generate_column_connector(column, connector):
    if connector:
        with column:
            generate_connector_selector_container(connector)

def generate_connector_selector_container(connector_info):
    center_components()
    provider_info = page_parameters()[PROVIDER_INFO_PARAM_KEY]
    connector_id = connector_info[ID_KEY]
    connector_name = connector_info[NAME_KEY]
    with components.container(key = f"selector_container{connector_id}"):
        image_col, text_col, button_col = st.columns([1,3,1])
        with image_col:
            image_col.image(connector_info[IMAGE_KEY])
        with text_col:
            text_col.write(connector_name)
        with button_col:
            clicked = components.button(translate("AddButton"), key=f"Add-{connector_id}")
            if clicked:
                set_connector_page_parameters(provider_info, connector_id, connector_name)
                set_page_substeps(bold2 = True)
                update_page_state(CONNECTOR_SETUP_STATE_KEY)