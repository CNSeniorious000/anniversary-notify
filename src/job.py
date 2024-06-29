from datetime import datetime
from typing import cast
from promplate import Node, ChainContext
from promptools.extractors import extract_json
from pydantic import BaseModel
from tenacity import retry


from .utils.resend import send_md, to_email

from .utils.llm import complete

from .logic import collect

prompt = Node.read("src/prompt.j2")


class Response(BaseModel):
    subject: str
    body: str


@prompt.end_process
@retry
def parse(context: ChainContext):
    context.result = extract_json(context.result, expect=Response)


def run():
    results = collect()
    if not results:
        return

    context = {"results": results, "name": "Muspi Merol", "to": to_email, "now": datetime.today()}

    print(context)

    res = cast(Response, prompt.invoke(context, complete).result)

    send_md(res.subject, res.body)
