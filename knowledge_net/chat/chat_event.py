from enum import Enum
from datetime import datetime
import pytz
from pydantic import BaseModel


DEFAULT_TIME_ZONE = 'GMT'


class EventType(str, Enum):
    """Enum of event types in the chat history."""

    message = 'message'
    summary = 'summary'
    call = 'call'
    ret = 'return'


class Role(str, Enum):
    """Enum of roles assigned to chat messages."""

    system = 'system'
    user = 'user'
    assistant = 'assistant'


class SummaryType(str, Enum):
    """Enum of summary types."""

    standalone_question = "standalone-question"


class ChatEvent(BaseModel):
    """Base class of chat history events."""

    event_type: EventType = EventType.message

    def to_dict(self):
        """Represents the instance as a dictionary."""

        # Work with both Pydantic version 1 and 2 since ChromaDb requires v1
        if hasattr(self, "model_dump"):
            # Use model_dump() for Pydantic version 2
            return self.model_dump()
        else:
            # Use dict() for Pydantic version 1
            return self.dict()

    @staticmethod
    def from_dict(d: dict) -> "ChatEvent":
        assert 'event_type' in d, "Event type ('event_type') required"
        event_class = event_classes[d['event_type']]
        return event_class.parse_obj(d)


class MessageEvent(ChatEvent):
    """Chat history event representing a message."""

    originator: str = "user"
    role: Role = Role.user
    message_text: str
    hidden: bool = False


class SummaryEvent(ChatEvent):
    """Chat history event providing a summary of preceding conversation."""

    originator: str = "user"
    role: Role = Role.assistant
    summary_type: SummaryType = SummaryType.standalone_question
    summary_text: str
    hidden: bool = False


class CallEvent(ChatEvent):
    """Chat history event recorded when a knowledge base calls another."""

    event_type: EventType = EventType.call
    caller: str = "user"
    called: str
    time_stamp: str = datetime.now(tz=pytz.timezone(DEFAULT_TIME_ZONE)).isoformat()
    time_out_seconds: int = 0


class ReturnEvent(ChatEvent):
    """Chat history event recorded when a call from a knowledge base to another returns."""

    event_type: EventType = EventType.ret
    caller: str = ""
    called: str
    time_stamp: str = datetime.now(tz=pytz.timezone(DEFAULT_TIME_ZONE)).isoformat()
    error: str = ""


"""Dictionary providing the ChatEvent subclasses corresponding to strings."""
event_classes: dict[str, type] = {
    'message': MessageEvent,
    'summary': SummaryEvent,
    'call': CallEvent,
    'return': ReturnEvent
}
