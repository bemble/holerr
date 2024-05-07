import logging
import re

logging.basicConfig(level=logging.WARN)


class Log:
    _debug_regex: list[re.Pattern] = None

    @staticmethod
    def set_debug_regex(regexes: list[str]):
        Log._debug_regex = [re.compile(regex) for regex in regexes]
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
        for logger in loggers:
            logger.setLevel(logging.WARN)
            for regex in Log._debug_regex:
                if regex.match(logger.name):
                    logger.setLevel(logging.DEBUG)
                    break

    @staticmethod
    def get_logger(package_name: str) -> logging.Logger:
        name = f"holerr.{package_name}"
        logger = logging.getLogger(name)
        log_level = logging.INFO
        if Log._debug_regex:
            for regex in Log._debug_regex:
                if regex.match(name):
                    log_level = logging.DEBUG
                    break

        logger.setLevel(log_level)
        return logger
