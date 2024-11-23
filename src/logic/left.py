from ..utils.log import log_messages


def need_notify(name: str, total_seconds: int | float):
    hours = int(total_seconds / 3600)
    log_messages(f"- coming in {round(total_seconds / 86400):>5} days: {name}")
    return hours in (0, 1, 2, 8, 24, 24 * 2, 24 * 3, 24 * 4, 24 * 6, 24 * 8, 24 * 10, 24 * 14)
