def render(markdown: str) -> str:
    from mistune import html

    print(html(markdown))

    return html(markdown)  # type: ignore
