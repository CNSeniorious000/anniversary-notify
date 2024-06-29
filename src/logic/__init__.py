from datetime import datetime
from .left import need_notify

from .strategy import strategies


def collect():
    now = datetime.now()

    results: list[tuple[str, float]] = []

    for strategy in strategies:
        if (seconds_left := strategy(now)) is not None and need_notify(seconds_left):
            results.append((strategy.__doc__ or strategy.__name__, seconds_left))

    return results
