from datetime import datetime
from sys import argv

from src.job import run

if __name__ == "__main__":
    try:
        run(now=datetime.strptime(argv[-1], "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None))
    except ValueError:
        run(now=datetime.now())
