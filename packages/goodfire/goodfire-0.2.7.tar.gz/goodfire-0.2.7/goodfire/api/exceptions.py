class GoodfireBaseException(Exception):
    pass


class RateLimitException(GoodfireBaseException):
    pass


class InvalidRequestException(GoodfireBaseException):
    pass


class ForbiddenException(GoodfireBaseException):
    pass


class NotFoundException(GoodfireBaseException):
    pass


class UnauthorizedException(GoodfireBaseException):
    pass


class ServerErrorException(GoodfireBaseException):
    pass


class RequestFailedException(GoodfireBaseException):
    pass


class InsufficientFundsException(GoodfireBaseException):
    pass


def check_status_code(status_code: int, respone_text: str):
    if status_code == 400:
        raise InvalidRequestException(respone_text).with_traceback(None)
    elif status_code == 401:
        raise UnauthorizedException(respone_text).with_traceback(None)
    elif status_code == 402:
        raise InsufficientFundsException(respone_text).with_traceback(None)
    elif status_code == 403:
        raise ForbiddenException(respone_text).with_traceback(None)
    elif status_code == 404:
        raise NotFoundException(respone_text).with_traceback(None)
    elif status_code == 429:
        raise RateLimitException(respone_text).with_traceback(None)
    elif status_code == 500:
        raise ServerErrorException("Server error").with_traceback(None)
    elif status_code > 400:
        raise RequestFailedException(respone_text).with_traceback(None)
