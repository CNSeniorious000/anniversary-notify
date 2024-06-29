from functools import cache
from pathlib import Path
from typing import Literal


from tomllib import loads


def parse_pyproject() -> dict[Literal["project"], dict[Literal["authors"], list[dict[Literal["name", "email"], str]]]]:
    return loads((Path.cwd() / "pyproject.toml").read_text())


@cache
def get_name_and_email():
    author = parse_pyproject()["project"]["authors"][0]
    return author["name"], author["email"]


def get_default_signature():
    name, email = get_name_and_email()
    return f"{name} <{email}>"
