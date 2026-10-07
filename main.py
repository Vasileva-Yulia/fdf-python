"""Запуск: python main.py <файл.fdf>"""

import sys

from fdf.errors import FdfError
from fdf.parser import parse_map


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

    # TODO: окно в feature/render
    print(f"{path}: {fdf_map.width}x{fdf_map.height}, высоты {fdf_map.z_min}..{fdf_map.z_max}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
