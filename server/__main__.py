from core.config import config
from db.db import db
from workers.handler import handler as workers_handlers

import sys
import logging


def __init__():
    if config.debug:
        logging.basicConfig(level=logging.INFO)


def main() -> int:
    workers_handlers.start()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        workers_handlers.stop()
