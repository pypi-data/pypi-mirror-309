from enum import IntEnum
from typing import Union


class StatusCode(IntEnum):
    OK = 0
    INVALID_ARGUMENT = 400
    UNAUTHENTICATED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    ABORTED = 409
    PRECONDITION_FAILED = 412
    OUT_OF_RANGE = 416
    ALREADY_EXISTS = 422
    RESOURCE_EXHAUSTED = 429
    CANCELLED = 499
    INTERNAL = 500
    UNIMPLEMENTED = 501
    UNAVAILABLE = 503
    DEADLINE_EXCEEDED = 504


class BaseException(Exception):
    def __init__(
        self,
        message: str = "",
        code: Union[int, StatusCode] = 500,
    ):
        super().__init__(message)
        self._message = message if isinstance(message, str) else str(message)
        self._code = code if isinstance(code, int) else int(code)

    @property
    def message(self) -> str:
        return self._message

    @property
    def code(self) -> int:
        return self._code

    def __str__(self):
        if self.code:
            return f"{super().__str__()} [{self.code}]"
        else:
            return super().__str__()


class InvalidArgumentException(BaseException):
    def __init__(
        self,
        message: str = "",
    ):
        super().__init__(message, 400)


class UnauthenticatedException(BaseException):
    def __init__(
        self,
        message: str = "",
    ):
        super().__init__(message, 401)


class ForbiddenException(BaseException):
    def __init__(
        self,
        message: str = "",
    ):
        super().__init__(message, 403)


class NotFoundException(BaseException):
    def __init__(
        self,
        message: str = "",
    ):
        super().__init__(message, 404)


class AbortedException(BaseException):
    def __init__(
        self,
        message: str = "",
    ):
        super().__init__(message, 409)


class InternalException(BaseException):
    def __init__(
        self,
        message: str = "",
    ):
        super().__init__(message, 500)


class UnimplementedException(BaseException):
    def __init__(
        self,
        message: str = "",
    ):
        super().__init__(message, 501)
