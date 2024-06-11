import streamlit as st
import components
import modules
from enums.pages import Pages
from services.i18n import Translator
from dtos.mapping_model import MappingModel
from globals import *

t = Translator().translate


def target_model_selector_component(
    model: MappingModel, 
    selected: bool = False, 
    on_select = None, 
    on_confirm = None
) -> None:
    with components.container(key=model.id):
        # TODO improve layout responsiveness
        label_col, btn_col = st.columns(2)
        with label_col:
            with components.stylable_container(f'{model.id}_label', css_styles="{ padding: 10px 0; }"):
                components.text_medium(model.name)
        with btn_col:
            _render_actions(model, selected, on_select, on_confirm)


def _render_actions(model: MappingModel, selected: bool, on_select, on_confirm):
    show_btn, apply_btn = st.columns(2)
    with show_btn:
        show_key=_get_show_btn_key(model.id)
        label = t('CustomMapHideCustomizedMappingsBtn') if selected else t('CustomMapShowCustomizedMappingsBtn')
        components.button(label, key=show_key, on_click=on_select, kwargs={'model': model, 'selected': selected})
    with apply_btn:
        apply_key=_get_apply_btn_key(model.id)
        apply = components.button(label=t('CustomMapApplyContinueBtn'), 
            key=apply_key,
            type='primary',
            on_click=on_confirm, 
            kwargs={'model': model})
        if apply:
            st.session_state[MODEL_INFORMATION_KEY] = { DATABASE_KEY : APPLICATION, SCHEMA_KEY : AGGREGATED_REPORTS_KEY }
            modules.switch_page(Pages.DataExplorer)
        

def _get_show_btn_key(model_id: str) -> str:
    return f'{model_id}_show_btn'


def _get_apply_btn_key(model_id: str) -> str:
    return f'{model_id}_apply_btn'
