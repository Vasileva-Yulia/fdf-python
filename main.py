"""Запуск: python main.py <файл.fdf>"""

import sys

from fdf.errors import FdfError
from fdf.model import Map
from fdf.parser import parse_map


def show_window(fdf_map: Map, title: str) -> None:
    # импорт здесь, а не наверху: тесты main.py не должны тянуть за собой pygame
    from fdf.app import App

    App(fdf_map, title).run()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Использование: python main.py <файл.fdf>", file=sys.stderr)
        return 2

    path = argv[1]
    try:
        fdf_map = parse_map(path)
    except FdfError as e:
        print(f"Ошибка в карте {path}: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Не удалось открыть {path}: {e.strerror}", file=sys.stderr)
        return 1

    show_window(fdf_map, path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
