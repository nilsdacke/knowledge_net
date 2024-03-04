from abc import ABC, abstractmethod

from knowledge_net.chat.chat_history import ChatHistory


class ChatModel(ABC):
    """Abstract interface for chat models."""

    @abstractmethod
    def __call__(self, chat_history: ChatHistory, originator: str) -> ChatHistory:
        """Calls the model and returns the chat continuation."""
        pass
