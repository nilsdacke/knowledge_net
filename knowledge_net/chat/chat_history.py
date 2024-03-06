import copy
import json
from datetime import datetime, timedelta
from typing import Optional, Any, Tuple
import pytz
from knowledge_net.chat.chat_event import ChatEvent, EventType, CallEvent, ReturnEvent,  DEFAULT_TIME_ZONE, SummaryType


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

    def is_empty(self) -> bool:
        return not self._history

    def has_messages(self) -> bool:
        return len(self.get_messages()) > 0

    def has_summary(self, summary_type=SummaryType.standalone_question):
        last_event = self.get_last_event()
        return last_event and last_event.event_type == EventType.summary and last_event.summary_type == summary_type

    def get_last_event(self) -> ChatEvent:
        return self._history[-1] if not self.is_empty() else None

    def get_messages(self, include_hidden: bool = False) -> list[ChatEvent]:
        """Returns the message events."""
        return [e for e in self._history if e.event_type == EventType.message and (include_hidden or not e.hidden)]

    def get_last_question(self) -> Optional[str]:
        if self.has_summary(SummaryType.standalone_question):
            return self.get_last_event().summary_text
        else:
            messages = self.get_messages()
            return messages[-1].message_text if messages else None

    def append(self, event: ChatEvent):
        """Appends an event to the end of the chat history."""
        self._history.append(event)

    def extend(self, other: "ChatHistory"):
        """Appends another chat history to self."""
        self._history.extend(other._history)

    def with_call_event(self, caller: str = "user", called: str = "", time_out_limit: timedelta = 0) -> "ChatHistory":
        """Adds a call event and returns self.

        Should be called right before calling another knowledge base. This is done automatically in the method
        :code:`Knowledgebase.reply`.
        """
        self.append(CallEvent(caller=caller,
                              called=called,
                              timestamp=datetime.now(tz=pytz.timezone(DEFAULT_TIME_ZONE)),
                              time_out_limit=time_out_limit))
        return self

    def with_return_event(self, input_chat_history: "ChatHistory", error: Optional[str] = "") -> "ChatHistory":
        """Adds a return event and returns self.

        Should be called when returning from a call to your knowledge base. This is done automatically in the method
        :code:`Knowledgebase.reply`.
        """
        self.append(self.return_event_from_chat_history(input_chat_history, error))
        return self

    @staticmethod
    def return_event_from_chat_history(input_chat_history: "ChatHistory", error: Optional[str] = "") -> ReturnEvent:
        """Creates a return event matching the call event at the end of the input chat history."""
        last_event = input_chat_history._history[-1]
        if last_event.event_type != EventType.call:
            raise ValueError("The input chat history should end with a call event")

        return ReturnEvent(caller=last_event.caller, called=last_event.called, error=error)

    @staticmethod
    def error(input_chat_history: "ChatHistory", error: Optional[str] = "") -> "ChatHistory":
        """Creates a chat history with a return event with an error message."""
        return ChatHistory().with_return_event(input_chat_history=input_chat_history, error=error)

    def returned_error(self):
        """Returns true if the last event is a return event with an error."""
        return self._history and self._history[-1].event_type == EventType.ret and self._history[-1].error

    def get_error(self) -> Tuple[str, str]:
        """Reports the called knowledge base name and the error if an error was returned.

        Check :code:`returned_error` before calling this.
        """
        assert self._history and self._history[-1].event_type == EventType.ret
        return self._history[-1].called, self._history[-1].error

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

    def __str__(self):
        """Returns a user-friendly string representation."""
        return self.as_json()

    def __repr__(self):
        """Returns a developer friendly string representation."""
        return self.as_json()
