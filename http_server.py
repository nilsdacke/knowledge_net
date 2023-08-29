import socketserver
from knowledge_net.comm_shell.comm_shell_http import NodeHTTPHandler
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase

PORT = 8001
_ = Knowledgebase(name='my_knowledgebase', preferred_protocol='mock')

with socketserver.TCPServer(("", PORT), NodeHTTPHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
