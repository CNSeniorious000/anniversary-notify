from datetime import datetime
from typing import cast

from promplate import ChainContext
from promptools.extractors import extract_json
from pydantic import BaseModel
from tenacity import retry

from .logic import collect
from .templates import prompt
from .utils.llm import complete
from .utils.log import log_messages
from .utils.resend import send_md, to_email


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

    log_messages(context)

    res = cast("Response", prompt.invoke(context, complete).result)

    send_md(res.subject, res.body)
