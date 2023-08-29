import random
from typing import Any

from knowledge_net.chat.chat_event import Role, MessageEvent
from knowledge_net.chat.chat_history import ChatHistory


class CommShellMock:
    @staticmethod
    def reply(kb_name: str, chat_history: ChatHistory, protocol_details: Any) -> ChatHistory:
        message = random.choice(
            [
                "Early to bed and early to rise, makes a man healthy, wealthy and wise.",
                "A penny saved is a penny earned.",
                "We are the ones we have been waiting for.",
                "May the force be with you."
            ]
        )
        return ChatHistory([MessageEvent(originator="computer",
                                         role=Role.assistant,
                                         message_text=message)])
