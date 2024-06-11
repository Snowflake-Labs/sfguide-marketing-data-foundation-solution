from typing import List
from llm.message import Message
from enums.llm import LLM


class Assistant:
    def __init__(self, id: str, name: str, type: LLM, chat: List[Message] = None):
        self.id = id
        self.name = name
        self.chat = chat
        self.type = type
