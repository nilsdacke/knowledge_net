import http.server
from typing import Any

from knowledge_net.chat.chat_history import ChatHistory


class NodeHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Handles incoming HTTP requests for the HTTP communication shell.

    To run a knowledge base HTTP server, use the script http_server.py.
    """

    TALK_TO_HOST = "localhost"
    TALK_TO_PORT = 8001

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, world!")


class CommShellHTTP:
    @staticmethod
    def reply(chat_history: ChatHistory, protocol_details: Any) -> ChatHistory:
        raise NotImplementedError()
