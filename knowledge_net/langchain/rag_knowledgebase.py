import json
from pathlib import Path
from typing import Tuple, Optional

from langchain_core.language_models import BaseLanguageModel

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase
from knowledge_net.langchain.rag_chain import LangchainRAGChain


class LangchainRAGKnowledgebase(Knowledgebase):
    """Knowledgebase based on retrieval from a vector database."""

    def __init__(self,
                 database_location: Path,
                 source_descriptions_file: Path,
                 identifier: str,
                 openai_api_key: str,
                 llm: BaseLanguageModel,
                 display_name: Optional[str] = None,
                 description: str = None):
        super().__init__(identifier=identifier, display_name=display_name, description=description)
        source_descriptions = self.get_source_descriptions(source_descriptions_file)
        self.chain = LangchainRAGChain(database_location, openai_api_key=openai_api_key,
                                       source_descriptions=source_descriptions, llm=llm)

    def _reply(self, chat_history: ChatHistory) -> Tuple[ChatHistory, Optional[str]]:
        return self.chain(chat_history, originator=self.identifier), None

    @staticmethod
    def get_source_descriptions(source_descriptions_file: Path) -> dict[str, dict[str, dict[str, str]]]:
        with open(source_descriptions_file, 'r') as f:
            descriptions = json.load(f)
        descriptions = {'source': descriptions}
        return descriptions
