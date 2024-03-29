from pathlib import Path
from typing import Optional, Any

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain_core.language_models import BaseLanguageModel

from knowledge_net.langchain.conversions import Conversions
from knowledge_net.langchain.document_group_transform import DocumentGroupTransform
from knowledge_net.langchain.rag_prompts import COMBINE_DOCUMENTS_CHAT_PROMPT
from knowledge_net.langchain.transform_combine_chain import TransformCombineDocumentsChain
from knowledge_net.experimental.database.database import Database
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.chat.chat_model import ChatModel


class LangchainRAGChain(ChatModel):
    LLM_DEFAULT_MODEL = "gpt-3.5-turbo"

    def __init__(self,
                 database_location: Path,
                 source_descriptions: dict[str, dict[str, dict[str, str]]],
                 openai_api_key: str,
                 llm: BaseLanguageModel):
        self.chain = LangchainRAGChain.conversational_chain(database_location, openai_api_key=openai_api_key,
                                                            llm=llm, source_descriptions=source_descriptions)

    def __call__(self, chat_history: ChatHistory, originator: str) -> ChatHistory:
        langchain_question = Conversions.chat_history_to_langchain_question(chat_history)
        langchain_response = self.chain.invoke(langchain_question)
        return Conversions.chat_history_from_langchain_response(langchain_response, originator=originator)

    @staticmethod
    def conversational_chain(database_location: Path,
                             openai_api_key: str,
                             llm: BaseLanguageModel,
                             source_descriptions: Optional[dict[str, Any]] = None) -> BaseConversationalRetrievalChain:
        """Instantiates a conversational retrieval chain."""

        database = Database(database_location, openai_api_key=openai_api_key).load()
        retriever = database.as_retriever()
        chain = ConversationalRetrievalChain.from_llm(
            llm,
            retriever=retriever,
            memory=None,
            verbose=True
        )
        document_transform = DocumentGroupTransform(key='source', descriptions=source_descriptions)
        chain.combine_docs_chain \
            = TransformCombineDocumentsChain(document_transform=document_transform,
                                             combine_documents_chain=chain.combine_docs_chain)

        # We assume stuff chain and chat language model
        chain.combine_docs_chain.combine_documents_chain.llm_chain.prompt = COMBINE_DOCUMENTS_CHAT_PROMPT

        return chain
