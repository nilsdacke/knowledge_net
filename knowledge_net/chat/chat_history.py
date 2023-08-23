import copy
from typing import List, Optional

from knowledge_net.chat.chat_event import ChatEvent, EventType, MessageEvent


class ChatHistory:
    """
    The chat history is the central data structure in the KnowledgeNet.

    It records the interactions between the user and a knowledge base and between knowledge bases.
    It can be seen as an extended version of the chat history of chat LLMs. Elements are events rather than
    messages to allow for a broader class of items. The additional features include:

    - Multiple parties (user and any number of knowledge bases) interacting
    - Timestamped events for calling and returning from knowledge bases

    Currently, messages are text only. Support for attachments of different types is planned.
    """

    def __init__(self, events: Optional[list[ChatEvent]] = None):
        self._history: list[ChatEvent] = events or []

    def copy(self) -> "ChatHistory":
        """Makes a copy for passing between knowledge bases."""
        return copy.deepcopy(self)

    def get_messages(self, include_hidden: bool = False) -> list[ChatEvent]:
        """Returns the message events."""
        return [e for e in self._history if e.event_type == EventType.message and (include_hidden or not e.hidden)]

    def append(self, event: ChatEvent):
        """Appends an event to the end of the chat history."""
        self._history.append(event)

    def extend(self, other: "ChatHistory"):
        """Appends another chat history to self."""
        self._history.extend(other._history)
