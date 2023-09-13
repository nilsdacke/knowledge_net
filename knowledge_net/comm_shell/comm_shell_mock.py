import random
from typing import Any, Tuple, Optional

from knowledge_net.chat.chat_event import Role, MessageEvent
from knowledge_net.chat.chat_history import ChatHistory


class CommShellMock:
    @staticmethod
    def reply(kb_name: str, chat_history: ChatHistory, protocol_details: Any) -> Tuple[ChatHistory, Optional[str]]:
        message = random.choice(
            [
                "Early to bed and early to rise, makes a man healthy, wealthy and wise.",
                "A penny saved is a penny earned.",
                "We are the ones we have been waiting for.",
                "May the force be with you.",
                "Bad times, hard times – this is what people keep saying; but let us live well "
                "and times shall be good. We are the times. Such as we are, such are the times."
            ]
        )
        return ChatHistory([MessageEvent(originator=kb_name,
                                         role=Role.assistant,
                                         message_text=message)]), None
