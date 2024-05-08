import traceback
from typing import Any, Dict, Optional

from rest_framework.response import Response
from rest_framework.views import exception_handler

from utils.response_service import ResponseService


def app_exception_handler(exc: Exception, context: Any) -> Optional[Response]:
    # Сначала вызываем стандартный обработчик DRF, чтобы получить Response
    response = exception_handler(exc, context)

    # Если стандартный обработчик возвращает None, значит, это исключение не обрабатывается DRF
    if response is None:
        if isinstance(exc, AppBaseException):  # Наше кастомное исключение
            return ResponseService.failure(
                str(exc), exc.code, exc.context, status=exc.http_status
            )

        # Получаем информацию о трассировке
        tb = traceback.extract_tb(exc.__traceback__)
        # Берем последнюю запись в трассировке (где произошла ошибка)
        last_trace = tb[-1]
        filename = last_trace.filename
        line_no = last_trace.lineno

        print(f"Internal Error: {exc}, File: {filename}, Line: {line_no}")

        # Для всех необработанных исключений возвращаем HTTP 500
        internal_exc = InternalErrorException()
        return ResponseService.failure(
            internal_exc.message,
            internal_exc.code,
            internal_exc.context,
            status=internal_exc.http_status,
        )
    return response


class AppBaseException(Exception):
    def __init__(
        self,
        message: str,
        code: int,
        http_status: Optional[int] = 500,
        context: Optional[Dict] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.http_status = http_status
        self.context = context or {}


class InternalErrorException(AppBaseException):
    def __init__(
        self, message="InternalError", code=6000, http_status=500, context=None
    ):
        super().__init__(message, code, http_status, context)


class DataNotFoundException(AppBaseException):
    def __init__(
        self, message="DataNotFound", code=6001, http_status=404, context=None
    ):
        super().__init__(message, code, http_status, context)
