from datetime import datetime
from typing import Callable


Strategy = Callable[[datetime], int | float | None]


strategies: list[Strategy] = []


register = strategies.append
