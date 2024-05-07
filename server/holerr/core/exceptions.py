class NotFoundException(Exception):
    """custom exception class for not found item"""


class AlreadyExistsException(Exception):
    """custom exception class for already existing item"""


class HttpRequestException(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(f"{message} (status code: {str(status_code)})")
        self.status_code = status_code
