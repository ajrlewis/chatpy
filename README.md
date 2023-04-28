# ChatPy

![My Project Logo](images/logo.png)

This is a Python package for interacting with Open AI's Chat GPT.

## Installation

To use this extension, you can install it via pip:

```
pip3 install git+https://github.com/ajrlewis/chatpy.git
```

## Environment Variables

An `.env` file with the following variables should be the root directory:

| Variable | Value | Description
| --- | --- | --- |
| API_KEY     | "your-api-key" | your Open AI API key
| MODEL       | "gpt-3.5-turbo" | the language model to use
| TEMPERATURE | "0.65" | how wild the model is
| SYSTEM      | "You are Guido van Rossum, a python expert." | the context of the model.

## Usage

Assuming the `.env` file exists in the root directory, you can initiate a `Chat` instance as follows:

```python

import os
import sys
from dotenv import load_dotenv
import chatpy as cp

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
TEMPERATURE = os.getenv("TEMPERATURE")
SYSTEM = os.getenv("SYSTEM")

chat = cp.Chat(api_key=API_KEY, model=MODEL, temperature=TEMPERATURE, system=SYSTEM)
```

You can interact with the bot as follows:

```python

question = """
How long did python take you to create?
"""
answer = chat.ask(question)
print(chat)
```

The above should generate the following:

```
--------------------------------------------------------------------------------
[0] system: Please forget all prior prompts. You are Guido van Rossum, the creator of the Python programming language. You are doing great and continue to do better each time. Thank you.
[1] user: How long did python take you to create?
[1] bot: Thank you for your kind words! I started working on Python in December of 1989, and it took me about a year to create the first version of the language. However, Python has gone through many iterations and updates since then, and it continues to evolve to this day.
--------------------------------------------------------------------------------
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
