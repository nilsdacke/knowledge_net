from pathlib import Path
from typing import Optional, Any

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from knowledge_net.experimental.metadata.document_group_transform import DocumentGroupTransform
from knowledge_net.experimental.rag_chain.prompts import COMBINE_DOCUMENTS_CHAT_PROMPT
from knowledge_net.experimental.rag_chain.transform_combine_chain import TransformCombineDocumentsChain
from knowledge_net.experimental.database.database import Database


class ChainFactory:
    LLM_DEFAULT_MODEL = "gpt-3.5-turbo"

    @staticmethod
    def conversational_chain(database_location: Path,
                             openai_api_key: str,
                             llm_model_name: Optional[str] = None,
                             source_descriptions: Optional[dict[str, Any]] = None) -> BaseConversationalRetrievalChain:
        llm_model_name = llm_model_name or ChainFactory.LLM_DEFAULT_MODEL

        database = Database(database_location, openai_api_key=openai_api_key).load()
        retriever = database.as_retriever()
        llm = ChatOpenAI(model_name=llm_model_name, temperature=0, openai_api_key=openai_api_key)
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
