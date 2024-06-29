from datetime import datetime, timedelta
from .logic.strategy import register


@register
def monthly_9th(now: datetime):
    if now.day < 10:
        delta = now - datetime(now.year, now.month, 9)
        return delta.total_seconds()


@register
def yearly_birthday(now: datetime):
    delta = now - datetime(now.year, 2, 9)
    return delta.total_seconds()


@register
def hundred_days_since_march_9th(now: datetime):
    start = datetime(2022, 4, 9)

    delta = (now - start).days

    next_delta = ((delta // 100) + 1) * 100

    return (start + timedelta(days=next_delta) - now).total_seconds()
