import streamlit as st
import pandas as pd

from typing import List, Literal

class Message:    
    def __init__(self,
        role: Literal["system", "assistant", "user"],
        result: str = None,
        error: str = None,
        content: dict = None,
        text: str = None,
        sql: str = None,
        suggestions: List[str] = None,
    ):
        self.role = role
        self.content = Content(text, sql, suggestions) if content is None else Content(**content)
        self.result = result
        self.error = error

    def __str__(self):
        return str({
            'role': self.role,
            'content': str(self.content),
            'result': self.result,
            'error': self.error
        })
    
    def as_dict(self) -> dict:
        obj = {}
        obj['role'] = self.role
        obj['content'] = self.content.as_dict()
        if self.result: obj['result'] = self.result
        if self.error: obj['error'] = self.error
        return obj

    def get_result_df(self) -> 'DataFrame':
        return pd.read_json(self.result)


class Content:
    def __init__(self,
        text: str = None,
        sql: str = None,
        suggestions: List[str] = None
    ):
        self.text = text
        self.sql = sql
        self.suggestions = suggestions

    def __str__(self):
        return str({
            "text": self.text,
            "sql": self.sql 
        })

    def as_dict(self) -> dict:
        obj = {}
        if self.text: obj['text'] = self.text
        if self.sql: obj['sql'] = self.sql
        if self.suggestions: obj['suggestions'] = self.suggestions
        return obj


# TODO move to a better place
def json_parse_list(messages: List[Message]) -> str:
    import jsonpickle
    message_list = list(map(lambda m: m.as_dict(), messages))
    return jsonpickle.encode(message_list)