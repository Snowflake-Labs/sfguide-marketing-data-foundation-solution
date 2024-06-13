import streamlit as st
from snowflake.snowpark.exceptions import SnowparkSQLException
from abc import ABC, abstractmethod
from typing import List
from llm.message import Message
from services.i18n import Translator
from snowflake.snowpark.functions import col


def stringify_timestamps(df):
    return df.select(*[
        col(c).cast("string").alias(c) if t == "timestamp" else col(c).alias(c)
        for c, t in df.dtypes
    ])


class LLM(ABC):
    context_file: str = None
    

    @abstractmethod
    def chat_complete(self, chat_history: List[Message]) -> Message:
        pass
    

    def process_sql(self, context: Message) -> Message:
        message = Message(role='assistant')
        try:
            sql = context.content.sql
            result = self.sp_session.sql(sql.replace(";",""))
            result = stringify_timestamps(result).to_pandas()
            message.result = result.to_json(date_format='iso')
            if len(result) > 0:
                data_summary = self.analyse_sql_result(context=context, result=message.result)
                message.content.text = data_summary
        except SnowparkSQLException as e:
            t = Translator().translate
            st.write(e)
            message.error = f"{t('ChatBotSqlError')}\n\n`{e.message}`"
        return message


    def analyse_sql_result(self, context: Message, result: str) -> str:
        pass


    def set_context_file(self, file_name: str) -> None:
        self.context_file = file_name


    def get_system_prompt(self, context_file: str) -> str:
        return None
    
    def _trim_context(self, chat_history: List[Message], last_n: int) -> List[Message]:
        system_prompt = chat_history[0] if chat_history[0].role == 'system' else []
        last_n_messages = [system_prompt] + chat_history[1:][-last_n:] if system_prompt else chat_history[-last_n:]
        return last_n_messages


    def _ignore_errors(self, chat_history: List[Message]) -> List[Message]:
        chat_history_filtered = list(filter(lambda m: m.error is None, chat_history))
        return chat_history_filtered
    