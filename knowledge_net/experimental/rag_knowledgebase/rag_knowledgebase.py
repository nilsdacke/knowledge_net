import json
from pathlib import Path
from typing import Tuple, Optional

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase
from knowledge_net.experimental.rag_chain.chain_factory import ChainFactory


class RAGKnowledgebase(Knowledgebase):
    """Knowledgebase based on retrieval from a vector database."""

    def __init__(self,
                 database_location: Path,
                 source_descriptions_file: Path,
                 identifier: str,
                 openai_api_key: str,
                 display_name: Optional[str] = None,
                 description: str = None):
        super().__init__(identifier=identifier, display_name=display_name, description=description)
        source_descriptions = self.get_source_descriptions(source_descriptions_file)
        self.chain = ChainFactory.conversational_chain(database_location, openai_api_key=openai_api_key,
                                                       source_descriptions=source_descriptions)

    def _reply_local(self, chat_history: ChatHistory) -> Tuple[ChatHistory, Optional[str]]:
        langchain_question = chat_history.to_langchain_question()
        langchain_response = self.chain(langchain_question)
        return ChatHistory.from_langchain_response(langchain_response, originator=self.identifier), None

    @staticmethod
    def get_source_descriptions(source_descriptions_file: Path) -> dict[str, dict[str, dict[str, str]]]:
        with open(source_descriptions_file, 'r') as f:
            descriptions = json.load(f)
        descriptions = {'source': descriptions}
        return descriptions
