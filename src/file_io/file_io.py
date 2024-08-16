import os.path
import csv
from typing import List, Union

from src.event_handlers.events import MouseEvent, KeyboardEvent


def write_macro(
        filename: str,
        data: List[Union[MouseEvent, KeyboardEvent]],
        path: str,
):
    # Изменяем расширение на .json
    filename = os.path.join(path, f"{filename}.txt")

    # Записываем данные в файл с использованием json.dump
    with open(filename, "w") as file:
        for line in data:
            file.write(f'{",".join([f'"{elem}"' for elem in line])}\n')


def read_macro(file_path: str):
    result = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for line in reader:
            action, *data = line

            if action == "move":
                x, y, delay = data
                result.append((action, int(x), int(y), float(delay)))

            elif action in {"click_down", "click_up"}:
                x, y, button, delay = data
                result.append(
                    (action, int(x), int(y), button, float(delay)))

            elif action == "scroll":
                x, y, dx, dy = map(int, data[:4])
                delay = float(data[4])
                result.append((action, x, y, dx, dy, delay))

            else:
                # Предполагается, что сюда попадут оставшиеся
                # {"key_press", "key_release"}
                button, delay = data
                result.append((action, button, float(delay)))

    return result
