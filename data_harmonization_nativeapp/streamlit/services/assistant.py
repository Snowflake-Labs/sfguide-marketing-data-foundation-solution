import json
import streamlit as st
import snowflake.connector

from globals import *
from uuid import uuid4
from snowflake.snowpark.functions import col
from snowflake.snowpark.table import Table
from typing import List
from dtos.assistant import Assistant
from llm.message import Message, json_parse_list
from enums.llm import LLM

def getUser():
    user = st.experimental_user
    return user.user_name if 'user_name' in user else user.email


def get_assistants_names(sp_session) -> List[Assistant]:
    user = getUser()
    dataframe = assistant_table(sp_session).select(col(ASSISTANT_TABLE_ID_COL), col(ASSISTANT_TABLE_NAME_COL), col(ASSISTANT_TABLE_TYPE_COL)).where(col(ASSISTANT_TABLE_USER_COL) == user).collect()
    assistants = list(map(lambda row: Assistant(id=row[0], name=row[1], type=row[2]), dataframe))
    return assistants


def assistant_table(sp_session) -> Table:
    return sp_session.table([LLM_SCHEMA, ASSISTANT_TABLE])


def add_assistant(sp_session, name: str, type: LLM) -> str:
    cols = assistant_table(sp_session).columns
    id = f'assistant-{uuid4()}'
    user = getUser()
    df = sp_session.create_dataframe([[id, name, None, user, type.value, None]], schema=cols)
    df.write.mode('append').save_as_table(table_name=[LLM_SCHEMA, ASSISTANT_TABLE])
    return id

def delete_assistant(sp_session, name: str) -> None:
    table = assistant_table(sp_session)
    table.delete(table[ASSISTANT_TABLE_ID_COL] == name ),

def rename_assistant(sp_session, id: str, new_name: str) -> None:
    table = assistant_table(sp_session)
    table.update(
        { ASSISTANT_TABLE_NAME_COL: new_name },
        table[ASSISTANT_TABLE_ID_COL] == id)


def update_chat(sp_session, id: str, new_chat: List[Message]) -> None:
    new_chat = json_parse_list(new_chat)
    table = assistant_table(sp_session)
    table.update(
        { ASSISTANT_TABLE_CHAT_COL: new_chat },
        table[ASSISTANT_TABLE_ID_COL] == id)


def update_sys_prompt(sp_session, id: str, sys_prompt: str) -> None:
    table = assistant_table(sp_session)
    table.update(
        { ASSISTANT_TABLE_SYS_PROMPT_COL: sys_prompt },
        table[ASSISTANT_TABLE_ID_COL] == id)


def get_messages(sp_session,  id: str) -> List[Message]:
    messages = assistant_table(sp_session)\
        .select(col(ASSISTANT_TABLE_CHAT_COL))\
        .where(col(ASSISTANT_TABLE_ID_COL) == id)\
        .first()[0]
    if not messages: return []
    obj = json.loads(messages)
    return list(map(lambda m: Message(**m), obj))