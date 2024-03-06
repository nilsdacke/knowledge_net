from textwrap import dedent
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain

from knowledge_net.chat.chat_event import SummaryEvent, SummaryType
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.langchain.conversions import Conversions


class ChatSummarizer:
    """Adds summary events to the chat history."""

    STANDALONE_QUESTION_TEMPLATE = dedent(
        """Given the following conversation and a follow up question, rephrase the follow up question to be """
        """a standalone question, in its original language.
        
        Chat history:
        {chat_history}
        Follow up question: {question}
        Standalone question:""")

    def __init__(self, openai_api_key: str):
        self.llm = OpenAI(openai_api_key=openai_api_key)
        standalone_question_prompt = PromptTemplate.from_template(ChatSummarizer.STANDALONE_QUESTION_TEMPLATE)
        self.standalone_question_chain = LLMChain(llm=self.llm, prompt=standalone_question_prompt)

    def make_standalone_question(self, chat_history: ChatHistory) -> str:
        langchain_question = Conversions.chat_history_to_langchain_question(chat_history)
        return self.standalone_question_chain(langchain_question)['text'].strip()

    def add_standalone_question(self, chat_history: ChatHistory, originator):
        chat_history.append(SummaryEvent(summary_type=SummaryType.standalone_question,
                                         summary_text=self.make_standalone_question(chat_history),
                                         originator=originator))

    def make_summary_of_type(self, chat_history: ChatHistory, summary_type=SummaryType.standalone_question) -> str:
        if summary_type == "standalone-question":
            return self.make_standalone_question(chat_history)
        raise ValueError(f"Unknown summary type {summary_type}")

    def add_summary_of_type(self, chat_history: ChatHistory, originator,
                            summary_type=SummaryType.standalone_question):
        chat_history.append(SummaryEvent(summary_type=summary_type,
                                         summary_text=self.make_summary_of_type(chat_history, summary_type),
                                         originator=originator))

    def add_summary_if_missing(self, chat_history: ChatHistory, originator,
                               summary_type=SummaryType.standalone_question):
        if chat_history.has_messages() and not chat_history.has_summary(summary_type):
            self.add_summary_of_type(chat_history, originator, summary_type)
