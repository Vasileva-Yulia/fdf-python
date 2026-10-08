from pathlib import Path

import pytest

import main
from fdf.model import Map

MAPS = Path(__file__).parent.parent / "maps"


def test_no_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    assert main.main(["main.py"]) == 2
    assert "Использование" in capsys.readouterr().err


def test_missing_file(capsys: pytest.CaptureFixture[str]) -> None:
    assert main.main(["main.py", "nope.fdf"]) == 1
    assert "Не удалось открыть" in capsys.readouterr().err


def test_bad_map(capsys: pytest.CaptureFixture[str]) -> None:
    assert main.main(["main.py", str(MAPS / "bad" / "not_number.fdf")]) == 1
    assert "строка 2, колонка 3" in capsys.readouterr().err


def test_good_map_opens_window(monkeypatch: pytest.MonkeyPatch) -> None:
    shown: list[Map] = []
    monkeypatch.setattr(main, "show_window", lambda fdf_map, title: shown.append(fdf_map))

    assert main.main(["main.py", str(MAPS / "10-2.fdf")]) == 0
    assert len(shown) == 1
    assert shown[0].width == 10
