from core.config import config

import sys
import logging


def init():
    if config.debug:
        logging.basicConfig(level=logging.INFO)
    print("coucou init")


def main() -> int:
    init()
    print("coucous")
    return 0


if __name__ == "__main__":
    sys.exit(main())
