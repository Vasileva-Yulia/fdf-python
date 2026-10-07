from pathlib import Path

import pytest

from fdf.errors import MapFormatError
from fdf.parser import parse_map, parse_text, parse_value

MAPS = Path(__file__).parent.parent / "maps"
MAP_10_2 = MAPS / "10-2.fdf"


def test_map_10_2_size() -> None:
    m = parse_map(MAP_10_2)
    assert (m.width, m.height) == (10, 10)
    assert (m.z_min, m.z_max) == (-1, 1)


@pytest.mark.parametrize(("x", "y", "z"), [(0, 0, 1), (3, 0, -1), (9, 2, 1), (0, 9, 0)])
def test_map_10_2_points(x: int, y: int, z: int) -> None:
    assert parse_map(MAP_10_2).point(x, y).z == z


def test_map_10_2_coordinates_match_file() -> None:
    lines = MAP_10_2.read_text().splitlines()
    for p in parse_map(MAP_10_2):
        assert p.z == int(lines[p.y].split()[p.x])


@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("7", (7, None)),
        ("-3", (-3, None)),
        ("2,0xFF8800", (2, "#FF8800")),
        ("1,0xff", (1, "#0000FF")),
    ],
)
def test_parse_value(token: str, expected: tuple[int, str | None]) -> None:
    assert parse_value(token) == expected


@pytest.mark.parametrize("token", ["x", "1.5", "+5", "5,", "5,FF0000", "5,0x1234567"])
def test_parse_value_invalid(token: str) -> None:
    with pytest.raises(ValueError):
        parse_value(token)


def test_empty_file() -> None:
    with pytest.raises(MapFormatError, match="файл пуст"):
        parse_map(MAPS / "bad" / "empty.fdf")


def test_not_a_number() -> None:
    with pytest.raises(MapFormatError, match="строка 2, колонка 3: 'x' — не целое число"):
        parse_map(MAPS / "bad" / "not_number.fdf")


def test_uneven_rows() -> None:
    with pytest.raises(MapFormatError, match="строка 2, колонка 3"):
        parse_map(MAPS / "bad" / "uneven.fdf")


def test_bad_color() -> None:
    with pytest.raises(MapFormatError, match="строка 2, колонка 2"):
        parse_map(MAPS / "bad" / "bad_color.fdf")


def test_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        parse_map(MAPS / "nope.fdf")


def test_trailing_empty_lines() -> None:
    assert parse_text("1 2\n3 4\n\n\n").height == 2


def test_empty_line_inside() -> None:
    with pytest.raises(MapFormatError, match="строка 2"):
        parse_text("1 2\n\n3 4\n")


def test_binary_file(tmp_path: Path) -> None:
    path = tmp_path / "bin.fdf"
    path.write_bytes(b"1 2\n3 \xff\n")
    with pytest.raises(MapFormatError, match="строка 2, колонка 3"):
        parse_map(path)
