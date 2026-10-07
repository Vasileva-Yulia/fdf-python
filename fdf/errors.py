"""Исключения программы."""


class FdfError(Exception):
    """Базовая ошибка FdF."""


class MapFormatError(FdfError):
    """Ошибка в формате файла карты."""

    def __init__(self, line: int, column: int, message: str) -> None:
        super().__init__(f"строка {line}, колонка {column}: {message}")
        self.line = line
        self.column = column
