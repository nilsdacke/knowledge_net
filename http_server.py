import socketserver
from knowledge_net.comm_shell.comm_shell_http import NodeHTTPHandler


PORT = 8000

with socketserver.TCPServer(("", PORT), NodeHTTPHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
