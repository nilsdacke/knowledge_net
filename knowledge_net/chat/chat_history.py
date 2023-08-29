import copy
import json
from typing import Optional, Any

from knowledge_net.chat.chat_event import ChatEvent, EventType


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

    @staticmethod
    def from_dict_list(dict_list: list[dict[str, Any]]) -> "ChatHistory":
        """Creates an instance from a list of dictionaries representing events."""
        return ChatHistory([ChatEvent.from_dict(e) for e in dict_list])

    @staticmethod
    def from_json(json_data: str) -> "ChatHistory":
        """Creates an instance from a json string."""
        return ChatHistory.from_dict_list(json.loads(json_data))

    def as_json(self) -> str:
        """Returns this instance as a json string."""
        return json.dumps(self.to_dict_list())

    def to_dict_list(self) -> list[dict[str, Any]]:
        """Returns a list of dictionaries representing this instance."""
        return [e.to_dict() for e in self._history]
