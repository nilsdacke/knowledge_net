import socketserver
import warnings
from typing import Any, Tuple, Optional
import http.server
import requests
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase


class NodeHTTPHandler(http.server.BaseHTTPRequestHandler):
    """Handles incoming HTTP requests for the HTTP communication shell.

    To run a knowledge base HTTP server, use the script http_server.py.

    Requests are post requests, where the data part is json and has the properties:
    "knowledgebase": name of the knowledge base to talk to
    "history": chat history

    The response has the same format as the "history" and contains the
    continuation of the chat.
    """

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            knowledgebase, chat_history, error = Knowledgebase.kb_and_history_from_json(post_data.decode('utf-8'))
        except ValueError:
            self.respond_bad_request('POST')
            return

        if error:
            continuation = ChatHistory.error(chat_history, error).as_json()
        else:
            continuation = knowledgebase.reply(chat_history).as_json()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', str(len(continuation)))
        self.end_headers()

        self.wfile.write(continuation.encode('utf-8'))

    def do_GET(self):
        self.respond_bad_request('GET')

    def respond_bad_request(self, request_type: str = 'GET'):
        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("Bad Request", "utf-8"))
        warnings.warn(f"Bad {request_type} request from {self.client_address}")


class CommShellHttp:
    """Handles replies over HTTP."""

    @staticmethod
    def reply(kb_name: str, chat_history: ChatHistory, protocol_details: Any, timeout: int = None) \
            -> Tuple[ChatHistory, Optional[str]]:
        if 'url' not in protocol_details:
            raise ValueError("Missing required 'url' in protocol details")
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        json_data = Knowledgebase.kb_and_history_as_dict(kb_name, chat_history)
        response = requests.post(url=protocol_details['url'], json=json_data, headers=headers, timeout=timeout)
        return ChatHistory.from_json(response.content.decode('utf-8')), None


class Server:
    """Runs a Knowledge Net HTTP server."""

    DEFAULT_PORT = 8000

    @staticmethod
    def serve(port: int = None):
        port = port or Server.DEFAULT_PORT
        with socketserver.TCPServer(("", port), NodeHTTPHandler) as httpd:
            print("Serving at port", port)
            httpd.serve_forever()
