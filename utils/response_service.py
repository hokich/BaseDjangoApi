from typing import Any, Dict, Optional

from rest_framework.response import Response


class ResponseService:
    @staticmethod
    def success(data: Any, status: int = 200) -> Response:
        """Формирует успешный ответ"""
        return Response({"success": True, "data": data}, status=status)

    @staticmethod
    def failure(
        message: str,
        code: int,
        context: Optional[Dict] = None,
        status: int = 400,
    ) -> Response:
        """Формирует ответ с ошибкой"""
        return Response(
            {
                "success": False,
                "error": {
                    "message": message,
                    "code": code,
                    "context": context or {},
                },
            },
            status=status,
        )
