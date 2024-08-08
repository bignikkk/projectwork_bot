class MissingTokenError(Exception):
    """Исключение при отсутствии токенов для доступа к серверу API."""

    pass


class IncorrectResponseCodeError(Exception):
    """Инициализирует объект исключения с заданными параметрами."""

    def __init__(self, code, reason, text):
        """Исключение для неверного кода ответа от сервера API."""
        self.code = code
        self.reason = reason
        self.text = text
        super().__init__(
            f'Неверный код ответа от сервера API: {code} ({reason}): {text}')
