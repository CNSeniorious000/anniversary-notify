from functools import cache
from os import getenv

from promplate import Message
from tenacity import retry

from .log import log_completion


@cache
def get_generate():
    from promplate.llm.openai import ChatGenerate

    return ChatGenerate().bind(model=getenv("LLM_MODEL"))


@log_completion
@retry
def complete(prompt: str | list[Message]) -> str:
    result = ""
    for i in get_generate()(prompt):
        print(i, end="", flush=True)
        result += i
    print()

    return result
