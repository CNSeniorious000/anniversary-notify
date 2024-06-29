from functools import cache


@cache
def get_markdown():
    from mistune import create_markdown

    return create_markdown(escape=False)


def render(markdown: str) -> str:
    renderer = get_markdown()

    return renderer(markdown)
