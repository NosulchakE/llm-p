# app/core/errors.py
class AppError(Exception):
    """Базовое исключение приложения"""
    pass


class ConflictError(AppError):
    """Конфликт (email уже существует)"""
    pass


class UnauthorizedError(AppError):
    """Неавторизован (неверный пароль)"""
    pass


class ForbiddenError(AppError):
    """Запрещено (нет прав)"""
    pass


class NotFoundError(AppError):
    """Не найдено"""
    pass


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса"""
    pass
