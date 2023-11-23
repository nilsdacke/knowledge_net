from typing import Callable, List, Any, Tuple, Optional
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.schema import Document


class TransformCombineDocumentsChain(BaseCombineDocumentsChain):
    """Extends the combine documents chain with a step that transforms the list of input documents.

    For example, it can be used to group and annotate documents according to source or other metadata.
    """

    document_transform: Callable[[list[Document]], list[Document]]
    combine_documents_chain: BaseCombineDocumentsChain

    @property
    def input_keys(self) -> List[str]:
        return self.combine_documents_chain.input_keys

    @property
    def output_keys(self) -> List[str]:
        return self.combine_documents_chain.output_keys

    def prompt_length(self, docs: List[Document], **kwargs: Any) -> Optional[int]:
        return self.combine_documents_chain.prompt_length(docs, **kwargs)

    def combine_docs(self, docs: List[Document], **kwargs: Any) -> Tuple[str, dict]:
        docs = self.document_transform(docs)
        return self.combine_documents_chain.combine_docs(docs, **kwargs)

    async def acombine_docs(self, docs: List[Document], **kwargs: Any) -> Tuple[str, dict]:
        docs = self.document_transform(docs)
        return await self.combine_documents_chain.acombine_docs(docs, **kwargs)

    @property
    def _chain_type(self) -> str:
        return self.combine_documents_chain._chain_type

