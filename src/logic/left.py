from datetime import datetime, timedelta
from os import getenv

from ..utils.log import log_messages

LOCAL_REMINDER_HOURS = (0, 1, 2, 8, 24, 24 * 2, 24 * 3, 24 * 4, 24 * 6, 24 * 8, 24 * 10, 24 * 14)
VERCEL_CRON_REMINDER_HOURS = (24, 24 * 2, 24 * 3, 24 * 4, 24 * 6, 24 * 8, 24 * 10, 24 * 14)
VERCEL_CRON_WINDOW_HOURS = 24
VERCEL_CRON_MODE = "vercel-cron"


def need_notify(name: str, total_seconds: int | float, now: datetime):
    hours_left = total_seconds / 3600
    target = now + timedelta(seconds=total_seconds)
    log_messages(f"- {round(total_seconds / 86400):>5} days · {target:%Y-%m-%d %H:%M} · {name}")

    if getenv("ANNIVERSARY_NOTIFY_MODE") == VERCEL_CRON_MODE:
        # A daily cron run should catch thresholds crossed since the previous run.
        return any(threshold - VERCEL_CRON_WINDOW_HOURS < hours_left <= threshold for threshold in VERCEL_CRON_REMINDER_HOURS)

    return int(hours_left) in LOCAL_REMINDER_HOURS
