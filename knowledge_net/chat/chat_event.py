from enum import Enum
from datetime import datetime, timedelta
from pydantic import BaseModel


class EventType(str, Enum):
    """Enum of event types in the chat history."""

    message = 'message'
    call = 'call'
    ret = 'return'


class Role(str, Enum):
    """Enum of roles assigned to chat messages."""

    system = 'system'
    user = 'user'
    assistant = 'assistant'


class ChatEvent(BaseModel):
    """Base class of chat history events."""

    event_type: EventType = EventType.message

    def to_dict(self):
        return self.model_dump()

    @staticmethod
    def from_dict(d: dict) -> "ChatEvent":
        assert 'event_type' in d, "Event type ('event_type') required"
        event_class = event_classes[d['event_type']]
        return event_class.parse_obj(d)


class MessageEvent(ChatEvent):
    originator: str = "user"
    role: Role = Role.user
    message_text: str
    hidden: bool = False


class CallEvent(ChatEvent):
    event_type: EventType = EventType.call
    caller: str
    called: str
    time_stamp: datetime
    time_out_limit: timedelta


class ReturnEvent(ChatEvent):
    event_type: EventType = EventType.ret
    caller: str
    called: str
    time_stamp: datetime


event_classes: dict[str, type] = {
    'message': MessageEvent,
    'call': CallEvent,
    'ret': ReturnEvent
}
