from typing import Any

from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from knowledge_net.chat.chat_event import Role, MessageEvent
from knowledge_net.chat.chat_history import ChatHistory


class Conversions:
    """Utilities for converting between KnowledgeNet and Langchain data structures."""

    @staticmethod
    def chat_history_from_langchain_response(response: dict[str, Any], originator: str = "user") -> ChatHistory:
        """Creates an instance representing the chat history continuation from the answer returned by Langchain."""
        return ChatHistory([MessageEvent(role=Role.assistant, message_text=response['answer'], originator=originator)])

    @staticmethod
    def chat_history_to_langchain_question(chat_history: ChatHistory) -> dict[str, Any]:
        """Returns a dictionary that can be passed to a Langchain conversational chain."""
        langchain_messages = Conversions.chat_history_to_langchain_messages(chat_history)
        return {'question': langchain_messages[-1].content, 'chat_history': langchain_messages[:-1]}

    @staticmethod
    def chat_history_to_langchain_messages(chat_history: ChatHistory) -> list[BaseMessage]:
        """Returns the message history as Langchain message instances."""
        return [Conversions.message_event_to_langchain(m) for m in chat_history.get_messages()]

    @staticmethod
    def message_event_to_langchain(message_event: MessageEvent) -> BaseMessage:
        """Converts a message event to a Langchain message instance."""
        c = {Role.user: HumanMessage, Role.assistant: AIMessage, Role.system: SystemMessage}[message_event.role]
        return c(content=message_event.message_text)
