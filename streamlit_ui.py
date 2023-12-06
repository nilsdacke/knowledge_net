import sys
import streamlit as st
from knowledge_net.chat.chat_event import MessageEvent
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase

st.title("Welcome to the KnowledgeNet")

# Initialize chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatHistory()

if "kb" not in st.session_state:
    Knowledgebase.clear_public_knowledgebases()
    kb_name = sys.argv[1]
    url = sys.argv[2]
    st.session_state.kb = Knowledgebase(identifier=kb_name,
                                        protocol='http',
                                        protocol_details={'http': {'url': url}})

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
