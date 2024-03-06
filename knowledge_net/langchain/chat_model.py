from langchain_core.language_models import BaseLanguageModel

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.chat.chat_model import ChatModel


class LangchainChatModel(ChatModel):
    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm

    def __call__(self, chat_history: ChatHistory, originator: str) -> ChatHistory:
        # TODO Convert to LanguageModelInput and from BaseMessage
        pass
