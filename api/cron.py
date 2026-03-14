import json
from datetime import datetime
from os import environ, getenv
from pathlib import Path
from tempfile import NamedTemporaryFile
from zoneinfo import ZoneInfo

from src.job import run
from src.templates import build_summary
from src.utils import log as log_utils

CRON_TIMEZONE = getenv("APP_TIMEZONE", "Asia/Shanghai")
CRON_SECRET = getenv("CRON_SECRET")


def build_response(start_response, status: str, payload: dict[str, object], *, headers: list[tuple[str, str]] | None = None):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    response_headers = [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body)))]
    if headers:
        response_headers.extend(headers)
    start_response(status, response_headers)
    return [body]


def build_html_response(start_response, status: str, html: str, *, headers: list[tuple[str, str]] | None = None):
    body = html.encode("utf-8")
    response_headers = [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))]
    if headers:
        response_headers.extend(headers)
    start_response(status, response_headers)
    return [body]


def wants_html(environ) -> bool:
    accept = environ.get("HTTP_ACCEPT", "")
    content_type = environ.get("CONTENT_TYPE", "")
    return "html" in accept.lower() or "html" in content_type.lower()


def serialize_result(result):
    if result is None:
        return None
    if hasattr(result, "model_dump"):
        return result.model_dump()
    return result.dict()


def run_with_build_summary_context(now: datetime):
    previous_mode = environ.get("ANNIVERSARY_NOTIFY_MODE")
    environ["ANNIVERSARY_NOTIFY_MODE"] = "vercel-cron"
    with NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".md", delete=False) as tmp:
        summary_path = Path(tmp.name)

    previous_summary_path = log_utils.GITHUB_STEP_SUMMARY
    log_utils.GITHUB_STEP_SUMMARY = str(summary_path)

    try:
        result = run(now=now)
        if result is None:
            log_utils.log_messages("")
            log_utils.log_messages("build check: no reminders in the current cron window")

        summary = summary_path.read_text(encoding="utf-8") or "No build summary available."
    finally:
        log_utils.GITHUB_STEP_SUMMARY = previous_summary_path
        summary_path.unlink(missing_ok=True)
        if previous_mode is None:
            environ.pop("ANNIVERSARY_NOTIFY_MODE", None)
        else:
            environ["ANNIVERSARY_NOTIFY_MODE"] = previous_mode

    return result, {"logs": f"Generated at {now.isoformat(sep=' ', timespec='seconds')} ({CRON_TIMEZONE})\n\n{summary}"}


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    if method != "GET":
        return build_response(start_response, "405 Method Not Allowed", {"error": "method_not_allowed"}, headers=[("Allow", "GET")])

    if CRON_SECRET and environ.get("HTTP_AUTHORIZATION") != f"Bearer {CRON_SECRET}":
        return build_response(start_response, "401 Unauthorized", {"error": "unauthorized"})

    now = datetime.now(ZoneInfo(CRON_TIMEZONE)).replace(tzinfo=None)
    result, build_summary_context = run_with_build_summary_context(now)
    if wants_html(environ):
        return build_html_response(start_response, "200 OK", build_summary.render(build_summary_context))

    return build_response(
        start_response,
        "200 OK",
        {
            "ok": True,
            "mode": "vercel-cron",
            "timezone": CRON_TIMEZONE,
            "now": now.isoformat(timespec="seconds"),
            **build_summary_context,
            "result": serialize_result(result),
        },
    )
