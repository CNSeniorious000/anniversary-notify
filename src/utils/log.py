from functools import wraps
from os import getenv
from pathlib import Path

from promplate import Template
from promplate.llm.base import Complete
from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape

from .markdown import render

GITHUB_STEP_SUMMARY = getenv("GITHUB_STEP_SUMMARY")

console = Console()


def append_log(content: str):
    if GITHUB_STEP_SUMMARY:
        with Path(GITHUB_STEP_SUMMARY).open("a", encoding="utf-8") as f:
            f.write(content)


def log_messages(*messages: str, style: str | None = None):
    console.print(*map(escape, messages), style=style)
    append_log(" ".join(messages) + "\n")


def print_markdown(markdown: str):
    print("\n")
    console.print(Markdown(markdown))
    print()

    append_log(f"\n\n{markdown}\n")


messages_template = Template.read(f"{__file__}/../messages.j2")
response_template = Template.read(f"{__file__}/../response.j2")


def _log_prompt(prompt: str):
    append_log(f"<details>{render(messages_template.render({"prompt": prompt}))}</details>\n\n")


def _log_response(response: str):
    append_log(response_template.render({"response": response}))


def log_completion(func: Complete):
    @wraps(func)
    def wrapper(prompt: str, **config):
        _log_prompt(prompt)
        response = func(prompt, **config)
        _log_response(response)
        return response

    return wrapper
