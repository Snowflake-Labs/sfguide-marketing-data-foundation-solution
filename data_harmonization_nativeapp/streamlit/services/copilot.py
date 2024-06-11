import json
import pandas as pd
import requests
import streamlit as st
import time

from globals import *
from snowflake.snowpark import Session
from services.session import connection, is_local, is_docker
from llm.llm_base import LLM
from llm.message import Message
from typing import List
from requests.exceptions import HTTPError


class CortexCopilot(LLM):
    def __init__(self, sp_session):
        self.sp_session = sp_session
        self.use_cloud_udf = True

    
    def chat_complete(self, chat_history: List[Message]) -> Message:
        last_message: Message = chat_history[-1]
        try:
            response = self._send_message(self.sp_session, last_message.content.text, self.context_file)
            last_message = response["messages"][-1]["content"]
            return self._get_message(last_message)
        except HTTPError as e:
            return Message(role='assistant', error=e.response.text)
        except Exception as e:
            return Message(role='assistant', error=str(e))


    def _send_message(self, sp_session, prompt: str, file: str) -> dict:
        if not self.use_cloud_udf and (is_docker() or is_local()):
            return self._send_message_local(sp_session, prompt, file)
        else:
            return self._send_message_cloud(sp_session, prompt, file)


    def _send_message_cloud(self, sp_session, prompt: str, file: str) -> dict:
        file_path = f'{APPLICATION}.{LLM_SCHEMA}.{LLM_SEMANTIC_MODEL_STAGE}'
        response = sp_session.call(f'{APPLICATION}.{LLM_SCHEMA}.GET_CHAT_RESPONSE', prompt, file, file_path)
        response = json.loads(response)

        if response['status'] >= 400: 
            raise Exception(response)
        
        content = json.loads(response['content'])
        return content


    def _send_message_local(self, conn, prompt: str, file: str) -> dict:
        local = connection()
        """Calls the REST API and returns the response."""
        request_body = {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
            "modelPath": file,
        }
        max_retries = 10
        for retry in range(max_retries):
            
            resp = requests.post(
                (
                    f"https://{API}/api/v2/databases/{APPLICATION}/"
                    f"schemas/{LLM_SCHEMA}/copilots/{LLM_SEMANTIC_MODEL_STAGE}/chats/-/messages"
                ),
                json=request_body,
                headers={
                    "Authorization": f'Snowflake Token="{local.rest.token}"',
                    "Content-Type": "application/json",
                },
            )
            if resp.status_code < 400:
                return resp.json()
            time.sleep(1)
        resp.raise_for_status()


    def _get_message(self, content: list) -> Message:
        message = Message(role='assistant')
        for item in content:
            if item["type"] == "text":
                message.content.text = item["text"]
            elif item["type"] == "suggestions":
                message.content.suggestions = item["suggestions"]
            elif item["type"] == "sql":
                message.content.sql = item["statement"]
            else:
                # TODO handle unexpected cases
                pass
        return message
