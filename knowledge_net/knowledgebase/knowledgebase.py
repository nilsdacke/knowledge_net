import json
from typing import Any, Optional, Tuple

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.comm_shell.comm_shell import CommShell


class Knowledgebase:
    """
    Represents a knowledge base accessed remotely or locally.

    When a knowledge base is accessed over a communication protocol like HTTP, the communication shell
    is called to make the connection.

    Knowledge bases can also run locally, in the same process as the caller. To implement a local knowledge base,
    subclass :code:`Knowledgebase` and implement the :code:`_reply_local` method.
    """

    _directory: dict[str, "Knowledgebase"] = {}
    """Directory of the knowledge bases known to the running process
    
    The knowledge bases include the "main" knowledge base (local or remote) presented by your server or local UI,
    local knowledge bases running in the same process, and knowledge bases accessed remotely.    
    """

    def __init__(self,
                 name: str,
                 preferred_protocol: str = 'local',
                 protocol_details: Optional[dict[str, Any]] = None):
        self.name = name
        self.preferred_protocol = preferred_protocol
        self._protocol_details = protocol_details or {'mock': None}
        self._register()

    def reply(self, chat_history: ChatHistory, protocol: Optional[str] = None) -> ChatHistory:
        """Calls the knowledge base and returns the continuation of the chat history."""

        protocol = protocol or self.preferred_protocol
        if protocol == 'local':
            return self._reply_local(chat_history.copy())
        else:
            return CommShell.reply(self.name, chat_history, protocol, self.get_details_for_protocol(protocol))

    def _reply_local(self, chat_history: ChatHistory) -> ChatHistory:
        """Override this to create a knowledge base that runs locally in the same process as the caller."""
        raise NotImplementedError("Need to reimplement to run a local knowledgebase")

    def _register(self):
        """Enters the knowledge base into the local knowledge base directory."""

        if self.name in Knowledgebase._directory:
            raise ValueError("Knowledgebase name must be unique")
        Knowledgebase._directory[self.name] = self

    @staticmethod
    def clear_directory():
        Knowledgebase._directory = {}

    def get_details_for_protocol(self, protocol: str) -> Any:
        """Returns the protocol details for the knowledgebase and a protocol."""

        assert protocol in self._protocol_details, f"No details for protocol {protocol}"
        return self._protocol_details[protocol]

    @staticmethod
    def kb_and_history_from_json(json_data: str) -> Tuple["Knowledgebase", ChatHistory]:
        """Returns Knowledgebase and ChatHistory objects from json data."""

        data_dict = json.loads(json_data)
        assert 'knowledgebase' in data_dict, "Knowledgebase key ('knowledgebase') required"
        assert 'chat_history' in data_dict, "Chat history key ('chat_history') required"
        kb_name = data_dict['knowledgebase']
        knowledgebase: "Knowledgebase" = Knowledgebase.kb_by_name(kb_name)
        chat_history: ChatHistory = ChatHistory.from_dict_list(data_dict['chat_history'])
        return knowledgebase, chat_history

    @staticmethod
    def kb_and_history_as_dict(kb_name: str, chat_history: ChatHistory) -> dict[str, Any]:
        """Creates a dictionary representation of the knowledge base name and the chat history."""
        return {'knowledgebase': kb_name, 'chat_history': chat_history.to_dict_list()}

    @staticmethod
    def kb_and_history_as_json(kb_name: str, chat_history: ChatHistory) -> str:
        """Creates a json representation of the knowledge base name and the chat history."""
        return json.dumps(Knowledgebase.kb_and_history_as_dict(kb_name, chat_history))

    @staticmethod
    def kb_by_name(kb_name: str) -> "Knowledgebase":
        """Returns a knowledge base using its unique name."""

        if kb_name not in Knowledgebase._directory:
            raise ValueError(f"Knowledgebase {kb_name} not found")
        return Knowledgebase._directory[kb_name]
