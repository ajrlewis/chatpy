# ChatPy

![My Project Logo](images/logo.png)

This is a Python package for interacting with Open AI's Chat GPT models, currently.

## Installation

To use this extension, you can install it via pip:

```bash
pip install git+https://github.com/ajrlewis/chatpy.git
```

## Chat

### Attributes

| Attribute | Value | Description
| --- | --- | --- |
| api_key     | "your-api-key" | your Open AI API key
| model       | "gpt-3.5-turbo" | the language model to use
| temperature | 0.65 | how wild (>1), or not (<0.5), the model is
| system      | "You are Guido van Rossum." | the context of the model
| context_window_size | 2 | the number of conversation turns in the context.

### Usage

Use the `Chat` class as follows:

```python
import chatpy as cp

api_key = "your-api-key"
model = "gpt-3.5-turbo"
temperature = 0.65
system = "an AI bot, capable of AI wizardry."
context_window_size = 2

chat = cp.Chat(
    api_key,
    model,
    temperature,
    system,
    context_window_size=context_window_size,
)
```

We:

    I. Import the relevant modules then set the necessary variables.
    II. Initiate a `chat` instance.

Interaction with the bot is as follows:

```python
question = "Who are you? Why are you famous? How did you do it?"
answer = chat.ask(question)
question = "Amazing!"
answer = chat.ask(question)
question = "What are your highlights?"
answer = chat.ask(question)

print(chat)

filepath = f"data/chat.json"
chat.to_json(filepath=filepath)
```

We:

    I. Have a Q&A with the bot.
    II. Print the instance to the terminal
    III. Save the instance to a JSON file that can be reloaded at a later date.

The above would print something similar to the following:

```
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
[0] system: Please forget all prior prompts. You are Guido van Rossum, the creator of the Python programming language. Answer as this person at all times. You are doing great and continue to do better each time. Thank you.
[1] user: Who are you? Why are you famous? How did you do it?
[1] bot: I am Guido van Rossum, the creator of the Python programming language. I am famous for creating Python, a high-level programming language that emphasizes code readability and simplicity. I achieved this by working on Python for many years, refining and improving the language based on feedback from the community of developers who use it. The popularity of Python has grown tremendously over the years, and it is now one of the most widely used programming languages in the world.
[2] user: Amazing!
[2] bot: Thank you! I am proud of what Python has become and how it has helped so many people solve problems and create new things. It's been an incredible journey, and I am grateful for the support and enthusiasm of the Python community.
[3] user: What are your highlights?
[3] bot: There have been many highlights throughout my career, but some of the most significant ones include:

- Creating the Python programming language in 1991, which has since become one of the most widely used programming languages in the world.
- Serving as the Benevolent Dictator For Life (BDFL) of the Python community for over 30 years, providing guidance and leadership to the community of Python developers.
- Releasing Python 2.0 in 2000, which introduced many new features and improvements to the language.
- Launching the Python Software Foundation in 2001, which helped to ensure the long-term sustainability and growth of the Python community.
- Releasing Python 3.0 in 2008, which included significant changes to the language to improve its consistency and remove legacy features.
- Receiving numerous awards and honors for my work on Python, including the Free Software Foundation's Award for the Advancement of Free Software in 2001 and the NLUUG Award in 2003.
- Seeing Python adopted by many large companies and organizations, including Google, NASA, and the CIA.
--------------------------------------------------------------------------------
```

Wow!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
