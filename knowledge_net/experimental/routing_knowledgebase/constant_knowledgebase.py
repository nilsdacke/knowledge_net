from typing import Tuple, Optional

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase


class ConstantKnowledgebase(Knowledgebase):
    def __init__(self,
                 identifier: str,
                 display_name: Optional[str] = None,
                 description: str = None,
                 fixed_message: str = "Hello world"):
        super().__init__(identifier, display_name, description)
        self.fixed_message = fixed_message

    def _reply(self, chat_history: ChatHistory) -> Tuple[ChatHistory, Optional[str]]:
        return ChatHistory([self.message(self.fixed_message)]), None
