import json
from datetime import datetime
from os import getenv
from zoneinfo import ZoneInfo

from src.job import run

CRON_TIMEZONE = getenv("APP_TIMEZONE", "Asia/Shanghai")
CRON_SECRET = getenv("CRON_SECRET")


def build_response(start_response, status: str, payload: dict[str, str], *, headers: list[tuple[str, str]] | None = None):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    response_headers = [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body)))]
    if headers:
        response_headers.extend(headers)
    start_response(status, response_headers)
    return [body]


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    if method != "GET":
        return build_response(start_response, "405 Method Not Allowed", {"error": "method_not_allowed"}, headers=[("Allow", "GET")])

    if CRON_SECRET and environ.get("HTTP_AUTHORIZATION") != f"Bearer {CRON_SECRET}":
        return build_response(start_response, "401 Unauthorized", {"error": "unauthorized"})

    now = datetime.now(ZoneInfo(CRON_TIMEZONE)).replace(tzinfo=None)
    environ["ANNIVERSARY_NOTIFY_MODE"] = "vercel-cron"
    run(now=now)

    return build_response(
        start_response,
        "200 OK",
        {"ok": "true", "mode": "vercel-cron", "timezone": CRON_TIMEZONE, "now": now.isoformat(timespec="seconds")},
    )
