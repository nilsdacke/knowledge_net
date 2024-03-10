from typing import Sequence, Optional, List, Any

from langchain.schema import BaseMessage, AIMessage, SystemMessage
from langchain_community.llms import DeepInfra
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.runnables import RunnableConfig


class MixtralFormatter:
    """Creates a prompt formatted for the Mixtral instruction model.

    The format is described here:
        https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1
        https://deepinfra.com/mistralai/Mixtral-8x7B-Instruct-v0.1/api
    """

    @staticmethod
    def format_input(input: LanguageModelInput) -> str:
        # We assume that the input is a message sequence
        messages: Sequence[BaseMessage] = input

        # Little state machine handles system messages and non-standard cases like
        # multiple consecutive user messages
        strings = []
        done_sentence = done_instruction = True
        for m in messages[:-1]:
            message_string, done_sentence, done_instruction = MixtralFormatter.format_message(m, done_sentence,
                                                                                              done_instruction)
            strings.append(message_string)
        strings.append(MixtralFormatter.format_last_message(messages[-1]))
        return ''.join(strings)

    @staticmethod
    def format_message(message: BaseMessage, done_sentence: bool, done_instruction: bool) -> tuple[str, bool, bool]:
        """Formats messages depending on their type."""

        message_string = ""
        if done_sentence:
            message_string += "<s> "
            done_sentence = False
        if type(message) is AIMessage:
            message_string += f"{message.content}</s> "
            done_sentence = True
        elif type(message) is SystemMessage:
            message_string += f"[INST] <<SYS>>\n{message.content}\n<<SYS>>\n\n"
            done_instruction = False
        else:  # HumanMessage
            if done_instruction:
                message_string += "[INST] "
            done_instruction = True
            message_string += f"{message.content} [/INST] "
        return message_string, done_sentence, done_instruction

    @staticmethod
    def format_last_message(message: BaseMessage) -> str:
        return f"[INST] {message.content} [/INST] "


class DeepInfraMixtralLLM(DeepInfra):
    """DeepInfra LLM with the Mixtral instruction formatting."""

    def __init__(self):
        model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        super().__init__(model_id=model_id)

    def invoke(self,
               input: LanguageModelInput,
               config: Optional[RunnableConfig] = None,
               *,
               stop: Optional[List[str]] = None,
               **kwargs: Any
               ):
        """Invokes model with the Mixtral instruction formatting."""
        prompt = MixtralFormatter.format_input(input)
        return super().invoke(prompt, config=config, stop=stop, **kwargs)
