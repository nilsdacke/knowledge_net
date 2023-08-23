from typing import Any, Optional

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.comm_shell.comm_shell import CommShell


class Knowledgebase:
    def __init__(self,
                 preferred_protocol: str = "http",
                 protocol_details: Optional[dict[str, Any]] = None):
        self.preferred_protocol = preferred_protocol
        self._protocol_details = protocol_details or {'mock': None}

    def get_details_for_protocol(self, protocol: str) -> Any:
        assert protocol in self._protocol_details, f"No details for protocol {protocol}"
        return self._protocol_details[protocol]

    def reply(self, chat_history: ChatHistory, protocol: Optional[str] = None):
        protocol = protocol or self.preferred_protocol
        return CommShell.reply(protocol,
                               self.get_details_for_protocol(self.preferred_protocol),
                               chat_history)
