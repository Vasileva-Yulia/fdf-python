from pathlib import Path

import pytest

from fdf.model import Point
from fdf.parser import parse_map, parse_text
from fdf.projection import Camera

MAPS = Path(__file__).parent.parent / "maps"


def test_origin_goes_to_origin() -> None:
    assert Camera().project(Point(0, 0, 0)) == pytest.approx((0, 0))


def test_height_goes_up() -> None:
    _, y = Camera().project(Point(0, 0, 1))
    assert y < 0


def test_z_scale_zero_ignores_height() -> None:
    cam = Camera(z_scale=0)
    assert cam.project(Point(2, 3, 100)) == pytest.approx(cam.project(Point(2, 3, 0)))


@pytest.mark.parametrize(("width", "height"), [(800, 600), (300, 900), (1920, 1080)])
def test_fit_keeps_map_inside_window(width: int, height: int) -> None:
    m = parse_map(MAPS / "10-2.fdf")
    cam = Camera()
    cam.fit(m, width, height)
    for p in m:
        x, y = cam.project(p)
        assert 0 <= x <= width
        assert 0 <= y <= height


def test_fit_centers_flat_map() -> None:
    # плоская квадратная карта — ромб, симметричный относительно середины окна
    m = parse_text("0 0 0\n0 0 0\n0 0 0\n")
    cam = Camera()
    cam.fit(m, 800, 600)
    top_x, _ = cam.project(m.point(0, 0))
    bottom_x, _ = cam.project(m.point(2, 2))
    left_x, _ = cam.project(m.point(0, 2))
    right_x, _ = cam.project(m.point(2, 0))
    assert top_x == pytest.approx(400)
    assert bottom_x == pytest.approx(400)
    assert 400 - left_x == pytest.approx(right_x - 400)


def test_fit_single_point() -> None:
    m = parse_text("5")
    cam = Camera()
    cam.fit(m, 800, 600)
    assert cam.project(m.point(0, 0)) == pytest.approx((400, 300))
