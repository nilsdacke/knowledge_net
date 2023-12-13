from typing import Tuple, Optional

from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.knowledgebase.knowledgebase import Knowledgebase
from knowledge_net.chat.chat_event import SummaryType

from knowledge_net.experimental.summarization.chat_summarizer import ChatSummarizer
from knowledge_net.experimental.routing_knowledgebase.matchable_texts import MatchableTexts


class RoutingKnowledgebase(Knowledgebase):
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
        self.chat_summarizer.add_summary_if_missing(chat_history, originator=self.identifier,
                                                    summary_type=SummaryType.standalone_question)
        question = chat_history.get_last_question()

        names = self.knowledgebase_descriptions.baseline_or_better(query=question, k=4)
        relevant_knowledgebases = [self._connected_knowledgebases[n] for n in names]
        replies = [kb.reply(chat_history) for kb in relevant_knowledgebases]

        message_text_lists = [[m.message_text for m in r.get_messages()] for r in replies]
        concatenated = ['\n\n'.join(text_list) for text_list in message_text_lists]
        display_names = [kb.display_name for kb in relevant_knowledgebases]
        prefixed = [f"From **{name}**:\n\n{m}" for name, m in zip(display_names, concatenated)]
        message = self.message('\n\n'.join(prefixed))

        return ChatHistory([message]), None

    def set_connected_knowledgebases(self, knowledgebases: dict[str, Knowledgebase]):
        super().set_connected_knowledgebases(knowledgebases)
        d = {identifier: kb.description for identifier, kb in self._connected_knowledgebases.items()}
        self.knowledgebase_descriptions = MatchableTexts(d, self.openai_api_key)

