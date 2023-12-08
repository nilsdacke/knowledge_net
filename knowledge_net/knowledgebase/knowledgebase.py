import json
from importlib import import_module
from pathlib import Path
from typing import Any, Optional, Tuple
from knowledge_net.chat.chat_event import MessageEvent, Role
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.comm_shell.comm_shell import CommShell


class Knowledgebase:
    """
    Represents a knowledge base accessed remotely or locally.

    When a knowledge base is accessed over a communication protocol like HTTP, the communication shell
    is called to make the connection.

    Knowledge bases can also run locally, in the same process as the caller. To implement a local knowledge base,
    subclass :code:`Knowledgebase` and implement the :code:`_reply` method.
    """

    _public_knowledgebases: dict[str, "Knowledgebase"] = {}
    """List of knowledge bases exposed to the outside"""

    def __init__(self,
                 identifier: str,
                 display_name: Optional[str] = None,
                 description: str = None,
                 protocol: str = 'local',
                 protocol_details: Optional[dict[str, Any]] = None):
        self.identifier = identifier
        self.display_name = display_name or identifier
        self.description = description
        self.protocol = protocol
        self._protocol_details = protocol_details or {'mock': None}
        self._connected_knowledgebases = {}

    def reply(self, chat_history: ChatHistory, caller: str = "user", protocol: Optional[str] = None) -> ChatHistory:
        """Calls the knowledge base and returns the continuation of the chat history."""

        protocol = protocol or self.protocol
        chat_history.with_call_event(caller=caller, called=self.identifier)
        if protocol == 'local':
            continuation, error = self._reply(chat_history.copy())
        else:
            continuation, error = \
                CommShell.reply(self.identifier, chat_history, protocol, self.get_details_for_protocol(protocol))
        return continuation.with_return_event(chat_history, error=error or "")

    def _reply(self, chat_history: ChatHistory) -> Tuple[ChatHistory, Optional[str]]:
        """Override this to define the behavior of your knowledgebase."""
        raise NotImplementedError("Need to reimplement _reply to create a knowledgebase")

    @staticmethod
    def clear_public_knowledgebases():
        """Empties the list of public knowledgebases."""
        Knowledgebase._public_knowledgebases = {}

    def get_details_for_protocol(self, protocol: str) -> Any:
        """Returns the protocol details for the knowledgebase and a protocol."""

        assert protocol in self._protocol_details, f"No details for protocol {protocol}"
        return self._protocol_details[protocol]

    def message(self, message_text: str) -> MessageEvent:
        """Creates a message event."""
        return MessageEvent(originator=self.identifier, role=Role.assistant, message_text=message_text)

    @staticmethod
    def instantiate_public(directory: Path):
        """Instantiates and shares knowledgebases from json configuration files."""

        instances = Knowledgebase.instances_from_json(directory, "public.json")
        Knowledgebase.set_public_knowledgebases_from_list(instances)

    def make_connected_knowledgebases(self, directory: Path):
        """Instantiates the connected knowledgebases for this knowledgebase."""

        instances = Knowledgebase.instances_from_json(directory, self.identifier + ".json")
        self.set_connected_knowledgebases_from_list(instances)

    @staticmethod
    def set_public_knowledgebases(knowledgebases: dict[str, "Knowledgebase"]):
        Knowledgebase._public_knowledgebases = knowledgebases

    @staticmethod
    def set_public_knowledgebases_from_list(knowledgebases: list["Knowledgebase"]):
        as_dict = {e.identifier: e for e in knowledgebases}
        Knowledgebase.set_public_knowledgebases(as_dict)

    def share(self):
        """Makes the knowledgebase public."""
        Knowledgebase._public_knowledgebases[self.identifier] = self

    def set_connected_knowledgebases(self, knowledgebases: dict[str, "Knowledgebase"]):
        self._connected_knowledgebases = knowledgebases

    def set_connected_knowledgebases_from_list(self, knowledgebases: list["Knowledgebase"]):
        as_dict = {e.identifier: e for e in knowledgebases}
        self.set_connected_knowledgebases(as_dict)

    @staticmethod
    def instances_from_json(directory: Path, file_name: str) -> list["Knowledgebase"]:
        """Makes a list of knowledge bases from a json specification.

        We instantiate the knowledgebases in the file :code:`directory / file_name`.
        This works recursively in that a local knowledgebase can instantiate connected knowledgebases.
        Connected knowledgebases are found in :code:`directory`.

        In :code:`directory`, files are named according to the following convention:
        :code:`public.json` lists public knowledgebases
        :code:`<identifier>.json` lists connected knowledgebases for the knowledgebase named :code:`identifier`.
        """

        with open(directory / file_name) as f:
            dict_list = json.load(f)
        return [Knowledgebase.from_dict(d, directory) for d in dict_list]

    @staticmethod
    def from_dict(d: dict[str, Any], directory: Path) -> "Knowledgebase":
        """Creates a single knowledge base from a dictionary."""

        if d['protocol'] == 'local':
            return Knowledgebase._instantiate_local(d, directory)
        else:
            return Knowledgebase._instantiate_remote(d)

    @staticmethod
    def _instantiate_local(d: dict[str, Any], directory: Path) -> "Knowledgebase":
        """Creates a local knowledge base from a dictionary."""

        class_name = d['protocol_details']['class']
        module_name = d['protocol_details']['module']
        kwargs = d['protocol_details']['kwargs']
        module = import_module(module_name)
        c = getattr(module, class_name)
        standard_args = {
            'identifier': d['identifier'],
            'display_name': d['display_name'],
            'description': d['description']
        }
        knowledgebase = c(**standard_args, **kwargs)
        knowledgebase.make_connected_knowledgebases(directory)
        return knowledgebase

    @staticmethod
    def _instantiate_remote(d: dict[str, Any]) -> "Knowledgebase":
        """Creates a local remote knowledge base from a dictionary."""
        return Knowledgebase(**d)

    @staticmethod
    def kb_and_history_from_json(json_data: str) -> Tuple["Knowledgebase", ChatHistory, str]:
        """Returns Knowledgebase and ChatHistory objects from json data."""

        data_dict = json.loads(json_data)
        assert 'knowledgebase' in data_dict, "Knowledgebase key ('knowledgebase') required"
        assert 'chat_history' in data_dict, "Chat history key ('chat_history') required"

        kb_name = data_dict['knowledgebase']

        error: str = ""
        knowledgebase: Optional["Knowledgebase"] = None

        if Knowledgebase.has_public_knowledgebase(kb_name):
            knowledgebase = Knowledgebase.public_knowledgebase_by_name(kb_name)
        else:
            error = f"Knowledge base {kb_name} not found"
        chat_history: ChatHistory = ChatHistory.from_dict_list(data_dict['chat_history'])
        return knowledgebase, chat_history, error

    @staticmethod
    def kb_and_history_as_dict(kb_name: str, chat_history: ChatHistory) -> dict[str, Any]:
        """Creates a dictionary representation of the knowledge base name and the chat history."""
        return {'knowledgebase': kb_name, 'chat_history': chat_history.to_dict_list()}

    @staticmethod
    def kb_and_history_as_json(kb_name: str, chat_history: ChatHistory) -> str:
        """Creates a json representation of the knowledge base name and the chat history."""
        return json.dumps(Knowledgebase.kb_and_history_as_dict(kb_name, chat_history))

    @staticmethod
    def has_public_knowledgebase(kb_name: str) -> bool:
        """Returns true if the knowledge base is in the list of public knowledgebases."""
        return kb_name in Knowledgebase._public_knowledgebases

    @staticmethod
    def public_knowledgebase_by_name(kb_name: str) -> "Knowledgebase":
        """Returns a public knowledge base using its unique name."""

        if kb_name not in Knowledgebase._public_knowledgebases:
            raise ValueError(f"Knowledgebase {kb_name} not found")
        return Knowledgebase._public_knowledgebases[kb_name]

    @staticmethod
    def single_public_instance() -> "Knowledgebase":
        """Returns the only public knowledge base if there is just one."""

        n_knowledgebases = len(Knowledgebase._public_knowledgebases)
        assert n_knowledgebases == 1, f"Assumed single knowledge base, found {n_knowledgebases}"
        return next(iter(Knowledgebase._public_knowledgebases.values()))

