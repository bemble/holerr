from server.tasks import worker
from server.api import server

import sys


def main() -> int:
    worker.start()
    server.start()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        worker.stop()
