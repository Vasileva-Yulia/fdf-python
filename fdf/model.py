"""Точка и карта высот."""

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int
    color: str | None = None  # "#RRGGBB" или None


class Map:
    """Прямоугольная сетка точек. rows[y][x] — точка с координатами (x, y)."""

    def __init__(self, rows: list[list[Point]]) -> None:
        if not rows or not rows[0]:
            raise ValueError("карта не может быть пустой")
        if any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("строки карты разной длины")
        self._rows = rows

    @property
    def width(self) -> int:
        return len(self._rows[0])

    @property
    def height(self) -> int:
        return len(self._rows)

    @property
    def z_min(self) -> int:
        return min(p.z for p in self)

    @property
    def z_max(self) -> int:
        return max(p.z for p in self)

    def point(self, x: int, y: int) -> Point:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"точка ({x}, {y}) за пределами карты")
        return self._rows[y][x]

    def neighbors(self, x: int, y: int) -> list[Point]:
        """Соседи справа и снизу: так каждое ребро встречается один раз."""
        result = []
        if x + 1 < self.width:
            result.append(self.point(x + 1, y))
        if y + 1 < self.height:
            result.append(self.point(x, y + 1))
        return result

    def edges(self) -> Iterator[tuple[Point, Point]]:
        for p in self:
            for q in self.neighbors(p.x, p.y):
                yield p, q

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self) -> Iterator[Point]:
        for row in self._rows:
            yield from row

    def __repr__(self) -> str:
        return f"Map({self.width}x{self.height})"
