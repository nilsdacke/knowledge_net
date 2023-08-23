from enum import Enum
from datetime import datetime, timedelta
from pydantic import BaseModel


class EventType(str, Enum):
    message = 'message'
    call = 'call'
    ret = 'return'


class Role(str, Enum):
    system = 'system'
    user = 'user'
    assistant = 'assistant'


class ChatEvent(BaseModel):
    event_type: EventType = EventType.message

    def to_dict(self):
        return self.model_dump()


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
