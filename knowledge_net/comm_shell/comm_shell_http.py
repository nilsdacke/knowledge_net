from typing import Any
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

        knowledgebase, chat_history = Knowledgebase.kb_and_history_from_json(post_data.decode('utf-8'))
        continuation = knowledgebase.reply(chat_history).as_json()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', str(len(continuation)))
        self.end_headers()

        self.wfile.write(continuation.encode('utf-8'))


class CommShellHttp:
    @staticmethod
    def reply(kb_name: str, chat_history: ChatHistory, protocol_details: Any) -> ChatHistory:
        if 'url' not in protocol_details:
            raise ValueError("Missing required 'url' in protocol details")
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        json_data = Knowledgebase.kb_and_history_as_dict(kb_name, chat_history)
        response = requests.post(url=protocol_details['url'], json=json_data, headers=headers)
        return ChatHistory.from_json(response.content.decode('utf-8'))
