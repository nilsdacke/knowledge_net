from knowledge_net.comm_shell.comm_shell_http import Server
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase

PORT = 8001
_ = Knowledgebase(identifier='my_knowledgebase', preferred_protocol='mock')

Server.serve(port=PORT)
