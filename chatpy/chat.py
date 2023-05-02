import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple
import openai

Message = Dict[str, str]
Messages = List[Dict[str, str]]
ConversationTurn = List[Message]
ConversationHistory = List[ConversationTurn]


def create_message(role: str, content: str) -> Message:
    return {"role": role, "content": content.strip()}


class Chat:
    """A class to interact with Open AI's Chat GPT model.

    Attributes:
        api_key: The Open AI API key.
        model: The name of the model.
        temperature: The temperature of the model.
        system: The context system of the chat.
        conversation_history: This conversation history.
        context_window_size: The window size to use, i.e. number of conversation turns.
    References:
        https://platform.openai.com/docs/guides/chat/introduction
        https://github.com/openai/openai-cookbook/blob/main/techniques_to_improve_reliability.md
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float,
        system: str = "",
        conversation_history: ConversationHistory = [],
        context_window_size: int = 2,
    ):
        self.api_key = str(api_key)
        self.model = str(model)
        self.temperature = float(temperature)
        self._system_message = {}
        self.system = system
        self.conversation_history = conversation_history
        self.context_window_size = context_window_size

    # TODO (ajrl) make this a print() method, __str__ should have colours.
    def __str__(self):
        white_color = "\033[0m"
        green_color = "\033[92m"
        red_color = "\033[31m"
        user_color = "\033[95m"
        bot_color = "\033[96m"
        system_color = "\033[93m"
        code_color = "\033[92m"
        separator = "-" * 80 + "\n"
        messages = []
        system_content = self._system_message["content"]
        messages.append(
            f"{green_color}[{0}]{white_color} {system_color}system{white_color}: {system_content}"
        )
        number_of_conversation_turns = len(self.conversation_history)
        for index, conversation_turn in enumerate(self.conversation_history):
            i = index + 1
            user_active_color = red_color
            bot_active_color = red_color
            if i >= number_of_conversation_turns - self.context_window_size:
                user_active_color = green_color
                if i != number_of_conversation_turns:
                    bot_active_color = green_color
            user_content = conversation_turn[0]["content"]
            bot_content = conversation_turn[1]["content"]
            for language in ("python", "bash", "html", "css", "js"):
                bot_content = bot_content.replace(
                    f"```{language}", f"```{language}{code_color}"
                )
                bot_content = bot_content.replace("```\n", f"```{white_color}\n")
            messages.append(
                f"{user_active_color}[{i}]{white_color} {user_color}user{white_color}: {user_content}"
            )
            messages.append(
                f"{bot_active_color}[{i}]{white_color} {bot_color}bot{white_color}: {bot_content}"
            )
        return separator + "\n".join(messages) + "\n" + separator.strip()

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str):
        self._api_key = api_key
        openai.api_key = self.api_key

    @property
    def system(self) -> str:
        return self._system

    @system.setter
    def system(self, system: str):
        self._system = system
        if system:
            self.conversation_history = []  # reset!
            self._system_message = create_message(role="system", content=self.system)

    def _get_context_messages(self) -> Messages:
        messages = [self._system_message] + list(
            sum(self.conversation_history[-self.context_window_size :], [])
        )
        return messages

    # TODO (ajrl): Need to handle when there's an error.
    def _get_bot_answer(self, context_messages: Messages) -> Message:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=self.temperature,
                messages=context_messages,
            )
            bot_answer = response.choices[0].message.content
        except Exception as e:
            raise e
        else:
            return create_message(role="assistant", content=bot_answer)

    def ask(self, question: str):
        # Before we ask, get the context messages
        context_messages = self._get_context_messages()
        user_question = create_message(role="user", content=question)
        context_messages.append(user_question)
        bot_answer = self._get_bot_answer(context_messages)
        if bot_answer:
            conversation_turn = [user_question, bot_answer]
            self.conversation_history.append(conversation_turn)
        return bot_answer

    # TODO (ajrl) This is I/O territory.

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "api_key": self.api_key,
            "model": self.model,
            "temperature": self.temperature,
            "system": self.system,
            "conversation_history": self.conversation_history,
            "context_window_size": self.context_window_size,
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> cls:
        chat = cls(**data)
        return chat

    def to_json(self, filepath: Optional[str] = None) -> Optional[str]:
        data = self.to_dict()
        data = json.dumps(data)
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            return data

    @classmethod
    def from_json(cls, data: str) -> cls:
        chat = cls.from_dict(json.loads(data))
        return chat

    @classmethod
    def read_json(cls, filepath: str) -> cls:
        with open(filepath) as f:
            data = json.load(f)
        chat = cls.from_json(data)
        return chat

    @classmethod
    def from_filepath(cls, filepath: str, *args, **kwargs) -> cls:
        if os.path.isfile(filepath):
            chat = cls.read_json(filepath=filepath)
        else:
            chat = cls(*args, **kwargs)
        return chat
