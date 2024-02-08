from importlib import import_module
from typing import Any, Tuple, Optional

from knowledge_net.chat.chat_history import ChatHistory


class CommShell:
    """
    All-static class serving as an interface to the communication shell.

    The class dispatches requests based on the protocol used.
    """

    @staticmethod
    def reply(kb_name: str, chat_history: ChatHistory, protocol: str, protocol_details: Any, timeout: int = None) -> \
            Tuple[ChatHistory, Optional[str]]:
        """Calls the reply method on the class implementing the protocol.

        We rely on the convention that modules are called :code:`comm_shell_<protocol_name>`,
        for example :code:`comm_shell_http` and classes :code:`CommShell<Protocol_name>`, for example
        :code:`CommShellHttp`. The class should have a static :code:`reply` method.
        """

        module_name = "knowledge_net.comm_shell.comm_shell_" + protocol.lower()
        module = import_module(module_name)
        class_name = "CommShell" + protocol.capitalize()
        c = getattr(module, class_name)
        reply_method = getattr(c, "reply")
        return reply_method(kb_name, chat_history, protocol_details)
