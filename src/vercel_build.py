from datetime import datetime
from os import environ, getenv
from pathlib import Path
from zoneinfo import ZoneInfo

from .templates import build_summary

APP_TIMEZONE = getenv("APP_TIMEZONE", "Asia/Shanghai")
PUBLIC_DIR = Path("public")
SUMMARY_PATH = PUBLIC_DIR / "_build_summary.md"
INDEX_PATH = PUBLIC_DIR / "index.html"


def main():
    PUBLIC_DIR.mkdir(exist_ok=True)
    SUMMARY_PATH.write_text("", encoding="utf-8")
    environ["GITHUB_STEP_SUMMARY"] = str(SUMMARY_PATH)
    environ["ANNIVERSARY_NOTIFY_MODE"] = "vercel-cron"

    from .job import run
    from .utils.log import log_messages

    now = datetime.now(ZoneInfo(APP_TIMEZONE)).replace(tzinfo=None)
    result = run(now=now)

    if result is None:
        log_messages("")
        log_messages("build check: no reminders in the current cron window")

    summary = SUMMARY_PATH.read_text(encoding="utf-8") or "No build summary available."
    INDEX_PATH.write_text(
        build_summary.render({"logs": f"Generated at {now.isoformat(sep=' ', timespec='seconds')} ({APP_TIMEZONE})\n\n{summary}"}),
        encoding="utf-8",
    )
    SUMMARY_PATH.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
