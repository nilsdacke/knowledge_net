from typing import Any, Optional

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.comm_shell.comm_shell import CommShell


class Knowledgebase:
    """
    Represents a knowledge base accessed remotely or locally.

    When a knowledge base is accessed over a communication protocol like HTTP, the communication shell
    is called to make the connection.

    Knowledge bases can also run locally, in the same process as the caller. To implement a local knowledge base,
    subclass `Knowledgebase` and implement the `_reply_local` method.
    """

    _directory: list["Knowledgebase"] = []
    """List of the knowledge bases known to the running process
    
    The knowledge bases include the "main" knowledge base (local or remote) presented by your server or local UI,
    local knowledge bases running in the same process, and knowledge bases accessed remotely.    
    """

    def __init__(self,
                 name: Optional[str] = None,
                 preferred_protocol: str = 'local',
                 protocol_details: Optional[dict[str, Any]] = None):
        self.name = name
        self.preferred_protocol = preferred_protocol
        self._protocol_details = protocol_details or {'mock': None}
        self.register()

    def reply(self, chat_history: ChatHistory, protocol: Optional[str] = None) -> ChatHistory:
        protocol = protocol or self.preferred_protocol
        if protocol == 'local':
            return self._reply_local(chat_history.copy())
        else:
            return CommShell.reply(chat_history, protocol, self.get_details_for_protocol(protocol))

    def _reply_local(self, chat_history: ChatHistory) -> ChatHistory:
        raise NotImplementedError("Need to reimplement to run a local knowledgebase")

    def register(self):
        Knowledgebase._directory.append(self)

    def get_details_for_protocol(self, protocol: str) -> Any:
        assert protocol in self._protocol_details, f"No details for protocol {protocol}"
        return self._protocol_details[protocol]
