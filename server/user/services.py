from typing import Optional

from django.conf import settings
from django.http import HttpRequest, HttpResponse


class CookieServices:
    """
    Сервис для работы с refresh-токеном в HTTP cookies.
    """

    COOKIE_NAME = "refresh_token"

    def get(self, request: HttpRequest) -> Optional[str]:
        """Получить refresh-токен из cookies запроса."""
        return request.COOKIES.get(self.COOKIE_NAME)

    def set(self, response: HttpResponse, refresh_token: str) -> None:
        """Установить refresh-токен в cookies ответа."""
        response.set_cookie(
            key=self.COOKIE_NAME,
            value=refresh_token,
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],  # Обычно настройки JWT хранятся так
            httponly=True,  # Защита от XSS
            secure=not settings.DEBUG,  # В разработке может не быть HTTPS
            samesite='Lax' if settings.DEBUG else 'Strict',  # Баланс между безопасностью и удобством
            path='/api/user/',  # Ограничиваем путь, где доступен токен
            domain=settings.SESSION_COOKIE_DOMAIN if hasattr(settings, 'SESSION_COOKIE_DOMAIN') else None,
        )

    def delete(self, response: HttpResponse) -> None:
        """Удалить refresh-токен из cookies (для выхода из системы)."""
        response.delete_cookie(
            key=self.COOKIE_NAME,
            path='/api/auth/',
            domain=settings.SESSION_COOKIE_DOMAIN if hasattr(settings, 'SESSION_COOKIE_DOMAIN') else None,
        )