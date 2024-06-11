import streamlit as st
import components
import components.llm_chat as chat
import services.copilot as copilot
import modules as pages

from enums.pages import Pages
from utils.resources import get_de_assistan_icon, get_cm_assistan_icon
from utils.model_helpers import center_components
from modules.pages import get_page_params, switch_page
from globals import *
from uuid import uuid4
from enums.llm import LLM as llm_type
from llm.llm_base import LLM
from services.session import session
from services.i18n import Translator
from services.copilot import CortexCopilot
from services.cortex_complete import CortexComplete
from services.assistant import update_chat, update_sys_prompt, get_messages
from components.sf_object_selector import ObjectSelector
from services.assistant import get_assistants_names, add_assistant, delete_assistant, rename_assistant
from dtos.assistant import Assistant
from services.permissions import request_account_privileges, SNOWFLAKEDB
from datetime import datetime
from typing import List


t = Translator().translate


@st.cache_resource
def connect_to_snowflake():
    return session()


sp_session = connect_to_snowflake()


def _clear_assistants() -> None:
    if 'assistants_names' in st.session_state:
        del st.session_state.assistants_names

def _create_assistant(sp_session, type: llm_type) -> None:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    assistant_name = f"{MDEA_KEY if type == llm_type.DataEngineering else MCMA_KEY} {dt_string}"
    with st.spinner(t('WaitAddAssistant')):
        add_assistant(sp_session, assistant_name, type)
        st.session_state[SELECTED_CHAT_KEY] = None
        chat.clear_messages()
        _clear_assistants()


def chat_selector(assistants: List[Assistant]):
      selected = st.selectbox(t('AssistantsExpander'), label_visibility='collapsed', index= len(assistants) - 1,options = assistants, format_func=lambda x: x.name, placeholder=t('AssistantPlaceholder'))
      st.session_state[SELECTED_CHAT_KEY] = selected
      chat.clear_messages()


def chat_assistant_page():
    components.title(t('AIAssistant'))
    st.write("")
    
    request_account_privileges([SNOWFLAKEDB])
    if ASSISTANT_PAGE_KEY not in get_page_params() or get_page_params()[ASSISTANT_PAGE_KEY] == ADD_ASSISTANT_PAGE_KEY:
        add_assistant_page()
    elif get_page_params()[ASSISTANT_PAGE_KEY] == SELECT_ASSISTANT_PAGE_KEY:
        select_assistant_page()
    

def add_assistant_page():
    sub_title_col, _ = st.columns(2)
    if SELECTED_CHAT_KEY not in st.session_state:
        st.session_state[SELECTED_CHAT_KEY] = None
    if EDITING_ASSISTANT_KEY not in st.session_state:
        st.session_state[EDITING_ASSISTANT_KEY] = False 
    assistant_collection = get_assistants_names(sp_session)
    assistant_count = len(assistant_collection)
    
    is_not_selected_chat = SELECTED_CHAT_KEY not in st.session_state or st.session_state[SELECTED_CHAT_KEY] is None
    if (is_not_selected_chat) and assistant_count > 0:
        st.session_state[SELECTED_CHAT_KEY] = assistant_collection[assistant_count-1] # If none is selected. Select the last option

    is_editing = st.session_state[EDITING_ASSISTANT_KEY]
    cols_distribution = [4, 2, 4, 3]

    assistant = st.session_state[SELECTED_CHAT_KEY]

    if not assistant:
        assist_col, _, _, _ = st.columns(cols_distribution)
        with assist_col:
            components.text_small(t('AssistantsExpander'))

        assist_col, _, _, action_col = st.columns(cols_distribution)
        with assist_col:
            chat_selector(assistant_collection)
        with action_col:
            _render_new_assistant_btn()
        return

    llm = _init_llm(sp_session, assistant.type)

    with sub_title_col:
        subtitle = t('MarketingDataEngineeringAssistant') if assistant.type == llm_type.DataEngineering.value else t('MarketingCampaignManagementAssistant')
        components.subtitle(subtitle)

    # Headers section
    assist_col, _, model_col, _ = st.columns(cols_distribution)
    with assist_col:
        if not is_editing:
            components.text_small(t('AssistantsExpander'))
        else:
            components.text_small(t('RenameAssistant'))
    with model_col:
        components.text_small(t('SelectDataModel'))

    # Controls section
    assist_col, edit_col, model_col, action_col = st.columns(cols_distribution)
    if not is_editing:
        with assist_col:
            chat_selector(assistant_collection)
        with edit_col:
            chat_editing_controls(sp_session, st.session_state[SELECTED_CHAT_KEY])
    else:
        rename_assistant_form(sp_session, assistant, assist_col, edit_col)

    with model_col:
            _render_semantic_context_selector(sp_session, llm)
    with action_col:
        _render_new_assistant_btn()

    st.divider()
    assistant_tab(sp_session, assistant, llm)


def select_assistant_page():
    center_components()
    assistant_selection_container(DATA_ENGINEERING_ASSISTANT_KEY, 
                                    get_de_assistan_icon(),
                                    t('MarketingDataEngineeringAssistant'),
                                    t('MarketingDataEngineeringAssistantDescription'),
                                    llm_type.DataEngineering)   
    assistant_selection_container(CAMPAIGN_MANAGEMENT_ASSISTANT_KEY, 
                                    get_cm_assistan_icon(),
                                    t('MarketingCampaignManagementAssistant'),
                                    t('MarketingCampaignManagementAssistantDescription'),
                                    llm_type.CortexCopilot)
    clicked = components.button(t("BackButton"))
    if clicked:
        switch_page(Pages.AIAssistant, params = { ASSISTANT_PAGE_KEY : ADD_ASSISTANT_PAGE_KEY })

def assistant_selection_container(key: str, image: str, title: str, description: str, type: llm_type):
    with components.container(key = key):
        col1, col2 = st.columns([10, 2])
        with col1:
            sub_col1, sub_col2, _ = col1.columns([2, 15, 20])
            with sub_col1:
                st.image(image)
            with sub_col2:
                components.text_medium_bold(title)
            components.text_small(description)
        with col2:
            clicked = col2.button(t('SelectAssistant'), key = key, type='primary')
            if clicked:
                _create_assistant(sp_session, type) 
                switch_page(Pages.AIAssistant, params = { ASSISTANT_PAGE_KEY : ADD_ASSISTANT_PAGE_KEY })

def rename_assistant_form(sp_session, assistant: Assistant, input_col, action_col):
    with input_col:
        newName = st.text_input(t('RenameAssistant'), placeholder=t('RenameAssistant'), label_visibility='collapsed')
        if(newName):
            assistant.name = newName
            rename_assistant(sp_session, assistant.id, newName)
            st.session_state[SELECTED_CHAT_KEY] = assistant
            st.session_state[EDITING_ASSISTANT_KEY] = False
            st.experimental_rerun()
    with action_col:
        if components.button(t('Cancel')):
            st.session_state[EDITING_ASSISTANT_KEY] = False
            st.experimental_rerun()

def chat_editing_controls(sp_session, assistant: Assistant):
    rename_col, delete_col = st.columns(2)
    with rename_col:
        if (components.button(t('Rename'), help=f"{t('RenameAssistant')}", key=f'edit-assistant{assistant.id}')):
            st.session_state[EDITING_ASSISTANT_KEY] = True
            st.experimental_rerun()
    with delete_col:
        if(components.button(t('Delete'), help=f"{t('DeleteAssistant')}", key=f'delete-assistant{assistant.id}')):
            delete_assistant(sp_session, assistant.id)
            st.session_state[SELECTED_CHAT_KEY] = None
            st.session_state[EDITING_ASSISTANT_KEY] = False
            assistant = None
            st.experimental_rerun()


def assistant_tab(sp_session, assistant: Assistant, llm: LLM):
    system_prompt = llm.get_system_prompt(llm.context_file)
    # TODO this sql query is called on every streamlit refresh
    if system_prompt: update_sys_prompt(sp_session, assistant.id, system_prompt)
    messages = get_messages(sp_session, assistant.id)
    chat.chat_component(llm, messages, assistant.type, system_prompt=system_prompt, on_update=_send_messages, )


def _send_messages(response: dict, assistant_type) -> None:
    llm: LLM = response["llm"]
    chat_history = response["messages"]
    message = llm.chat_complete(chat_history)
    chat.add_message(message, render=True, assistant_type = assistant_type)
    
    if message.content.sql is not None:
        message = llm.process_sql(message)
        chat.add_message(message, render=True, assistant_type = assistant_type)
    
    # Update assistant chat in the table
    sp_session = connect_to_snowflake()
    assistant_id =  st.session_state[SELECTED_CHAT_KEY].id
    update_chat(sp_session, assistant_id, chat.get_messages())


def _init_llm(sp_session, type: str) -> LLM:
    if type == llm_type.CortexCopilot.value:
        return CortexCopilot(sp_session) # TODO refactor
    else:
        return CortexComplete(sp_session)


def _render_new_assistant_btn() -> None:
    if components.button(t('NewAssistant'), type='primary'):
        switch_page(Pages.AIAssistant, params = { ASSISTANT_PAGE_KEY : SELECT_ASSISTANT_PAGE_KEY })


def _render_semantic_context_selector(sp_session, llm: LLM):
    query = f'LIST @{APPLICATION}.{LLM_SCHEMA}.{LLM_SEMANTIC_MODEL_STAGE}'
    model_selected = ObjectSelector(
            sp_session,
            key='data_model_select',
            label=t('SelectorDataModel'),
            query=query,
            on_change=chat.clear_messages,
            label_visibility="collapsed").render()
    if not model_selected: return
    file_name = model_selected.replace(f'{LLM_SEMANTIC_MODEL_STAGE.lower()}/', '')
    llm.set_context_file(file_name)
