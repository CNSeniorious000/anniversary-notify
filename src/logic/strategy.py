from collections.abc import Callable
from datetime import datetime

Strategy = Callable[[datetime], int | float | None]


strategies: list[Strategy] = []


register = strategies.append
