"""Изометрическая проекция точек карты на плоскость окна."""

import math
from dataclasses import dataclass

from fdf.model import Map, Point


@dataclass
class Camera:
    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    z_scale: float = 1.0
    angle: float = math.radians(30)

    def project(self, p: Point) -> tuple[float, float]:
        """Координаты точки на экране. Ось Y экрана направлена вниз, поэтому z вычитаем."""
        x = (p.x - p.y) * math.cos(self.angle)
        y = (p.x + p.y) * math.sin(self.angle) - p.z * self.z_scale
        return x * self.scale + self.offset_x, y * self.scale + self.offset_y

    def fit(self, fdf_map: Map, width: int, height: int) -> None:
        """Подобрать масштаб и смещение, чтобы карта поместилась в окно по центру."""
        self.scale, self.offset_x, self.offset_y = 1.0, 0.0, 0.0
        points = [self.project(p) for p in fdf_map]
        min_x = min(x for x, _ in points)
        max_x = max(x for x, _ in points)
        min_y = min(y for _, y in points)
        max_y = max(y for _, y in points)

        # у карты из одной точки или линии рамка бывает нулевой — иначе деление на ноль
        scales = []
        if max_x > min_x:
            scales.append(width / (max_x - min_x))
        if max_y > min_y:
            scales.append(height / (max_y - min_y))
        self.scale = min(scales) * 0.9 if scales else 1.0

        self.offset_x = width / 2 - (min_x + max_x) / 2 * self.scale
        self.offset_y = height / 2 - (min_y + max_y) / 2 * self.scale
