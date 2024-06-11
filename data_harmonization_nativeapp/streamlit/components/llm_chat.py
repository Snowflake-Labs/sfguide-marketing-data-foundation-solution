import components
import streamlit as st
from enums.llm import LLM
from llm.message import Message
from services.i18n import Translator
from typing import List
from utils.resources import get_de_assistan_icon


t = Translator().translate


def chat_component(llm, messages: List[Message], assistant_type: LLM, system_prompt: str = None, on_update = None):
    _init(messages, system_prompt)
    _render_messages(get_messages(), assistant_type)
        
    if user_input := st.chat_input(t("ChatQuestionLabel")):
        _process_input_message(llm, prompt=user_input, on_update=on_update, assistant_type = assistant_type)

    if 'active_suggestion' in st.session_state:
        selected_suggestion = st.session_state.active_suggestion
        _process_input_message(llm, prompt=selected_suggestion, on_update=on_update, assistant_type = assistant_type)
        del st.session_state.active_suggestion
    
    if is_show_help := len(get_messages()) <= 2:
        _render_help_message(llm, on_update, assistant_type = assistant_type)


def add_message(message: Message, render: bool = False, assistant_type: LLM = None) -> None:
    st.session_state.messages.append(message)
    message_index = len(st.session_state.messages)
    if render: _render_message(message, assistant_type, message_index)


def get_messages() -> List[Message]:
    return st.session_state.messages if 'messages' in st.session_state else []


def clear_messages() -> None:
    if 'messages' in st.session_state:
        del st.session_state.messages


def _init(messages: List[Message], system_prompt: str) -> None:
    if messages: st.session_state.messages = messages
    if "messages" in st.session_state: return

    st.session_state.messages = []

    if system_prompt is not None:
        system_message = Message(role='system', text=system_prompt)
        add_message(system_message)

    welcome_message = Message(role='assistant', text=t("TextChatBotWelcome"))
    add_message(welcome_message)


def _render_messages(messages: List[Message], assistant_type: LLM):
    message: Message
    for message_index, message in enumerate(messages):
        if message.role != 'system':
            _render_message(message, assistant_type, message_index)


def _render_message(message: Message, assistant_type: LLM, message_index: int) -> None:
    image = get_de_assistan_icon() if assistant_type == LLM.DataEngineering.value and message.role == 'assistant' else None
    with st.chat_message(message.role, avatar=image):
        if message.result is not None:
            st.dataframe(message.get_result_df())
        if message.content.text is not None:
            components.text_small(message.content.text)
        if message.content.sql is not None:
            st.code(message.content.sql, language='sql')
        if message.content.suggestions is not None:
            _render_suggestions(message.content.suggestions, message_index)
        if message.error is not None:
            st.error(message.error)


def _render_suggestions(suggestions: List[str], message_index: int) -> None:
    with st.expander("Suggestions", expanded=True):
        suggestion: str
        for i, suggestion in enumerate(suggestions):
            key = f'suggestion_{i}_{message_index}'
            components.button(suggestion, key=key, on_click=_set_active_suggestion, kwargs={'suggestion': suggestion})


def _render_help_message(llm, on_update, assistant_type: LLM):
    placeholder = st.empty()
    if placeholder.button(t('ChatSuggestion'), key='help_suggestion'):
        placeholder.empty()
        _process_input_message(llm, prompt=t('ChatSuggestion'), assistant_type=assistant_type, on_update=on_update)


def _process_input_message(llm, prompt: str, assistant_type: LLM, on_update = None) -> None:
    add_message(Message(role='user', text=prompt), render=True)
    with st.spinner("Generating response..."):
        on_update({ "llm": llm, "messages": get_messages() }, assistant_type)


def _set_active_suggestion(suggestion: str) -> None:
    st.session_state.active_suggestion = suggestion
