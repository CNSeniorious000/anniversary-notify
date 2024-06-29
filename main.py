from importlib import import_module
from src.job import run


if __name__ == "__main__":
    import_module("src.strategies")
    run()
