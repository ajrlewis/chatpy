from __future__ import annotations
import json
import sys
import re
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
    ):
        self.api_key = str(api_key)
        self.model = str(model)
        self.temperature = float(temperature)
        self._system_message = {}
        self.system = system
        self.conversation_history = conversation_history

    def __str__(self):
        user_color = "\033[95m"
        bot_color = "\033[96m"
        system_color = "\033[93m"
        code_color = "\033[92m"
        white_color = "\033[0m"
        separator = "-" * 80 + "\n"
        messages = []
        system_content = self._system_message["content"]
        messages.append(f"[{0}] {system_color}system{white_color}: {system_content}")
        for index, conversation_turn in enumerate(self.conversation_history):
            user_content = conversation_turn[0]["content"]
            bot_content = conversation_turn[1]["content"]
            for language in ("python", "bash", "html", "css", "js"):
                bot_content = bot_content.replace(
                    f"```{language}", f"```{language}{code_color}"
                )
                bot_content = bot_content.replace("```\n", f"```{white_color}\n")
            messages.append(
                f"[{index + 1}] {user_color}user{white_color}: {user_content}"
            )
            messages.append(f"[{index + 1}] {bot_color}bot{white_color}: {bot_content}")
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
            self.conversation_history = []  # reset the context
            self._system_message = create_message(role="system", content=self.system)

    # TODO (ajrl): Need to flatten conversation history.
    def _get_context_messages(self, window_size: int) -> Messages:
        messages = [self._system_message] + list(
            sum(self.conversation_history[-window_size:], [])
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
            return create_message(role="assistant", content=f"{e}")
        else:
            return create_message(role="assistant", content=bot_answer)

    def ask(self, question: str, window_size: int = 2):
        context_messages = self._get_context_messages(window_size=window_size)
        user_question = create_message(role="user", content=question)
        context_messages.append(user_question)
        bot_answer = self._get_bot_answer(context_messages)
        if bot_answer:
            conversation_turn = (user_question, bot_answer)
            self.conversation_history.append(conversation_turn)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "api_key": self.api_key,
            "model": self.model,
            "temperature": self.temperature,
            "system": self.system,
            "conversation_history": self.conversation_history,
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Chat:
        chat = Chat(
            api_key=data["api_key"],
            model=data["model"],
            temperature=data["temperature"],
            system=data["system"],
            conversation_history=data["conversation_history"],
        )
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
    def from_json(cls, data: str) -> Chat:
        chat = Chat.from_dict(json.loads(data))
        return chat

    @classmethod
    def read_json(cls, filepath: str) -> Chat:
        with open(filepath) as f:
            data = json.load(f)
        chat = Chat.from_json(data)
        return chat
