import components

from modules_backend.add_platform_analytics_model_backend import *

def connector_setup_section():
    section_header(translate("ConnectorSetup"))
    page_parameters()[LAST_STATE_KEY] = SELECT_CONNECTOR_STATE_KEY
    content = page_parameters()[MD_CONTENT_PARAM_KEY]
    st.markdown(content)
    components.text_small(f"[{translate('LearnMore')}]({page_parameters()[CONNECTOR_URL_PARAM_KEY]})")
    back_button_col, next_button_col, _ = st.columns([1, 1, 15])
    with back_button_col:
        go_back = components.button(translate("BackButton"))
        if go_back:
            back_component_settings(substep1_bold = True)
    with next_button_col:
        continue_button = components.button(translate("ContinueButton"), key="ContinueButton", type="primary")
        if continue_button:
            page_parameters()[LAST_STATE_KEY] = CONNECTOR_SETUP_STATE_KEY
            set_page_substeps(bold3 = True)
            update_page_state(DATA_ALREADY_IN_SNOWFLAKE_STATE_KEY)
