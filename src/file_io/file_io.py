import os.path
import csv
from typing import List, Union

from ..event_handlers.events import MouseEvent, KeyboardEvent, Action


def write_macro(
        filename: str,
        data: List[Union[MouseEvent, KeyboardEvent]],
        path: str,
):
    # Изменяем расширение на .txt
    filename = os.path.join(path, f"{filename}.txt")

    # Записываем данные в файл с использованием json.dump
    with open(filename, "w") as file:
        for line in data:
            file.write(f'{",".join([f'"{elem}"' for elem in line])}\n')
        print(f"File '{filename}' has been saved successfully.\n")


def read_macro(file_path: str):
    result = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for line in reader:
            action, *data = line

            if action == Action.MOVE:
                x, y, delay = data
                result.append((action, int(x), int(y), float(delay)))

            elif action in {Action.CLICK_DOWN, Action.CLICK_UP}:
                x, y, button, delay = data
                result.append(
                    (action, int(x), int(y), button, float(delay)))

            elif action == Action.SCROLL:
                x, y, dx, dy = map(int, data[:4])
                delay = float(data[4])
                result.append((action, x, y, dx, dy, delay))

            else:
                # Предполагается, что сюда попадут оставшиеся
                # {"key_press", "key_release"}
                button, delay = data
                result.append((action, button, float(delay)))

    return result
