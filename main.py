from datetime import datetime
from importlib import import_module
from sys import argv

from src.job import run

if __name__ == "__main__":
    import_module("src.strategies")
    try:
        run(now=datetime.strptime(argv[-1], "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None))
    except ValueError:
        run(now=datetime.now())
