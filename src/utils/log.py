from functools import wraps
from os import getenv
from pathlib import Path

from promplate.llm.base import Complete
from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape

from ..templates import messages, response
from .markdown import render

GITHUB_STEP_SUMMARY = getenv("GITHUB_STEP_SUMMARY")

console = Console()


def append_log(content: str):
    if GITHUB_STEP_SUMMARY:
        with Path(GITHUB_STEP_SUMMARY).open("a", encoding="utf-8") as f:
            f.write(content)


def log_messages(*items: str, style: str | None = None):
    strings = tuple(map(str, items))
    console.print(*map(escape, strings), style=style)
    append_log(" ".join(strings) + "\n")


def print_markdown(markdown: str):
    print("\n")
    console.print(Markdown(markdown))
    print()

    append_log(f"\n\n{markdown}\n")


def log_completion(func: Complete):
    @wraps(func)
    def wrapper(prompt: str, **config):
        append_log(f"<details>{render(messages.render({"prompt": prompt}))}</details>\n\n")
        completion = func(prompt, **config)
        append_log(response.render({"response": completion}))
        return completion

    return wrapper
