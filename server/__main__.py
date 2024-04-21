from server.tasks import worker

import sys


def main() -> int:
    worker.start()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        worker.stop()
