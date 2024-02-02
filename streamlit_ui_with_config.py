import sys
from pathlib import Path

import streamlit as st
from knowledge_net.chat.chat_event import MessageEvent
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase
import importlib.util


def exists_module(module_name: str) -> bool:
    """Checks if a module exists."""
    return importlib.util.find_spec(module_name) is not None


def get_openai_key() -> str:
    """Looks for the OpenAI API key in its possible locations."""

    if exists_module('credentials'):
        from credentials import openai_api_key
        return openai_api_key
    elif 'openai_api_key' in st.secrets:
        return st.secrets['openai_api_key']
    else:
        raise ValueError("No OpenAI API key found")


def get_configuration_directory() -> Path:
    """Gets the configuration directory as parameter or in st.secrets."""

    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    elif 'configuration_directory' in st.secrets:
        return Path(st.secrets['configuration_directory'])
    else:
        raise ValueError("No configuration directory specified")


st.title("Ask me anything...")

# Initialize chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatHistory()

if "kb" not in st.session_state:
    Knowledgebase.keys["openai_api_key"] = get_openai_key()
    Knowledgebase.instantiate_public(get_configuration_directory())
    st.session_state.kb = Knowledgebase.single_public_instance()

for message in st.session_state.chat_history.get_messages():
    with st.chat_message(message.role):
        st.markdown(message.message_text)

if prompt := st.chat_input("What do you want to learn about?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append(MessageEvent(message_text=prompt))
    response = st.session_state.kb.reply(st.session_state.chat_history)
    for message in response.get_messages():
        with st.chat_message(message.role):
            st.markdown(message.message_text)
    if response.returned_error():
        called, error = response.get_error()
        with st.chat_message("assistant"):
            st.markdown(f"Knowledge base {called} error: \"{error}\"")
    st.session_state.chat_history.extend(response)
