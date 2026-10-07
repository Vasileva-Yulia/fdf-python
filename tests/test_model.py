import pytest

from fdf.model import Map, Point


def grid(width: int, height: int) -> Map:
    return Map([[Point(x, y, x + y) for x in range(width)] for y in range(height)])


def test_len() -> None:
    assert len(grid(4, 3)) == 12


def test_iteration_order() -> None:
    coords = [(p.x, p.y) for p in grid(2, 2)]
    assert coords == [(0, 0), (1, 0), (0, 1), (1, 1)]


def test_neighbors_top_left_corner() -> None:
    m = grid(3, 3)
    assert m.neighbors(0, 0) == [m.point(1, 0), m.point(0, 1)]


def test_neighbors_bottom_right_corner() -> None:
    assert grid(3, 3).neighbors(2, 2) == []


def test_each_edge_once() -> None:
    # 3 ребра в каждой из 3 строк + 4 * 2 вертикальных
    assert len(list(grid(4, 3).edges())) == 3 * 3 + 4 * 2


def test_point_out_of_range() -> None:
    with pytest.raises(IndexError):
        grid(3, 3).point(3, 0)


def test_not_rectangular() -> None:
    with pytest.raises(ValueError):
        Map([[Point(0, 0, 0), Point(1, 0, 0)], [Point(0, 1, 0)]])
