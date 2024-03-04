from typing import Tuple, Optional

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase
from knowledge_net.chat.chat_event import SummaryType, MessageEvent

from knowledge_net.experimental.summarization.chat_summarizer import ChatSummarizer
from knowledge_net.experimental.routing_knowledgebase.matchable_texts import MatchableTexts


class RoutingKnowledgebase(Knowledgebase):
    """Knowledgebase that synthesizes the replies of connected knowledgebases.

    The knowledgebases to be consulted are selected based on the user's question."""

    def __init__(self,
                 identifier: str,
                 openai_api_key: str,
                 display_name: Optional[str] = None,
                 description: str = None):
        super().__init__(identifier, display_name, description)
        self.openai_api_key = openai_api_key
        self.chat_summarizer: ChatSummarizer = ChatSummarizer(openai_api_key=openai_api_key)
        self.knowledgebase_descriptions: Optional[MatchableTexts] = None

    def _reply(self, chat_history: ChatHistory) -> Tuple[ChatHistory, Optional[str]]:
        """Replies by aggregating the replies from selected knowledgebases."""
        query = self._prepare_routing_query(chat_history)
        relevant_knowledgebases = self._select_knowledgebases(query)
        replies = [kb.reply(chat_history) for kb in relevant_knowledgebases]
        message = self._combine_replies(relevant_knowledgebases, replies)
        return ChatHistory([message]), None

    def _prepare_routing_query(self, chat_history: ChatHistory) -> str:
        """Computes a query with which the relevant knowledgebases will be selected."""
        self.chat_summarizer.add_summary_if_missing(chat_history, originator=self.identifier,
                                                    summary_type=SummaryType.standalone_question)
        query = chat_history.get_last_question()
        assert query is not None
        return query

    def _select_knowledgebases(self, query: str) -> list[Knowledgebase]:
        """Picks relevant knowledgebases based on the query."""
        names = self.knowledgebase_descriptions.baseline_or_better(query=query, k=4)
        return [self._connected_knowledgebases[n] for n in names]

    def _combine_replies(self, knowledge_bases: list[Knowledgebase], replies: list[ChatHistory]) -> MessageEvent:
        """Produces a reply message from the replies of the connected knowledgebases.

        The message simply presents the reply from each knowledgebase under its display name. Example:

            From Old History:
            The king was very cruel...

            From Recent History:
            The president was very old...

        Override this method for more advanced aggregation or different formatting."""

        message_text_lists = [[m.message_text for m in r.get_messages()] for r in replies]
        concatenated = ['\n\n'.join(text_list) for text_list in message_text_lists]
        display_names = [kb.display_name for kb in knowledge_bases]
        prefixed = [f"From **{name}**:\n\n{m}" for name, m in zip(display_names, concatenated)]
        return self.message('\n\n'.join(prefixed))

    def set_connected_knowledgebases(self, knowledgebases: dict[str, Knowledgebase]):
        """Sets the connected knowledgebases and similarity-searchable knowledgebase descriptions."""
        super().set_connected_knowledgebases(knowledgebases)
        d = {identifier: kb.description for identifier, kb in self._connected_knowledgebases.items()}
        self.knowledgebase_descriptions = MatchableTexts(d, self.openai_api_key)
