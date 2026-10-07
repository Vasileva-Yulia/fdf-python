"""Чтение файлов карт .fdf."""

import re
from pathlib import Path

from fdf.errors import MapFormatError
from fdf.model import Map, Point

# [0-9] вместо \d: \d пропускает и не-ASCII цифры, а int() принял бы ещё "+5" и "1_000"
HEIGHT_RE = re.compile(r"-?[0-9]+")
COLOR_RE = re.compile(r"0x([0-9a-f]{1,6})", re.IGNORECASE)


def parse_value(token: str) -> tuple[int, str | None]:
    """'7' -> (7, None), '1,0xff' -> (1, '#0000FF')."""
    height, comma, color = token.partition(",")
    if not HEIGHT_RE.fullmatch(height):
        raise ValueError(f"{height!r} — не целое число")
    if not comma:
        return int(height), None
    match = COLOR_RE.fullmatch(color)
    if match is None:
        raise ValueError(f"{color!r} — некорректный цвет")
    return int(height), "#" + match.group(1).upper().rjust(6, "0")


def parse_text(text: str) -> Map:
    lines = text.rstrip().splitlines()  # пустые строки в конце не считаются
    if not lines:
        raise MapFormatError(1, 1, "файл пуст")

    rows: list[list[Point]] = []
    for y, line in enumerate(lines):
        tokens = line.split()
        if not tokens:
            raise MapFormatError(y + 1, 1, "пустая строка")
        if rows and len(tokens) != len(rows[0]):
            width = len(rows[0])
            raise MapFormatError(
                y + 1,
                min(len(tokens), width) + 1,
                f"ожидалось значений: {width}, найдено: {len(tokens)}",
            )
        row = []
        for x, token in enumerate(tokens):
            try:
                z, color = parse_value(token)
            except ValueError as e:
                raise MapFormatError(y + 1, x + 1, str(e)) from e
            row.append(Point(x, y, z, color))
        rows.append(row)
    return Map(rows)


def parse_map(path: str | Path) -> Map:
    """Прочитать карту из файла. OSError (нет файла и т.п.) не перехватывается."""
    data = Path(path).read_bytes()
    try:
        text = data.decode("utf-8-sig")  # -sig: пропускает BOM от Блокнота
    except UnicodeDecodeError as e:
        line = data.count(b"\n", 0, e.start) + 1
        column = e.start - data.rfind(b"\n", 0, e.start)
        raise MapFormatError(line, column, "файл не в кодировке UTF-8") from e
    return parse_text(text)
