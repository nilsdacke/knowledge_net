"""Test functions.

Use them as smoke tests, to examine the output, or to step through the code.
"""

import os
from pathlib import Path

from langchain_openai import ChatOpenAI

from credentials import openai_api_key, deepinfra_api_token
from knowledge_net.chat.chat_history import ChatHistory
from knowledge_net.langchain.deep_infra_mixtral import DeepInfraMixtralLLM
from knowledge_net.langchain.rag_knowledgebase import LangchainRAGKnowledgebase


def chat_with_knowledgebase() -> str:
    kb_name = "galton"
    display_name = "Francis Galton"
    database_location = Path("db/galton")
    source_descriptions_file = Path("examples/meta/victorian-science-sources.json")

    os.environ["DEEPINFRA_API_TOKEN"] = deepinfra_api_token

    # llm_default_model = "gpt-3.5-turbo"
    # llm = ChatOpenAI(model_name=llm_default_model, temperature=0, openai_api_key=openai_api_key)
    llm = DeepInfraMixtralLLM()
    knowledgebase = LangchainRAGKnowledgebase(database_location=database_location,
                                              source_descriptions_file=source_descriptions_file,
                                              identifier=kb_name,
                                              openai_api_key=openai_api_key,
                                              llm=llm,
                                              display_name=display_name)
    return knowledgebase.reply(ChatHistory.from_str("Tell me about Africa")).get_last_message_text()
