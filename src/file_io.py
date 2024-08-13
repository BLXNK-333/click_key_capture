import os.path
from typing import List, Union

from .event_handlers.events import MouseEvent, KeyboardEvent


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
            file.write(f"{','.join(map(str, line))}\n")


def read_macro(file_path: str):
    result = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.rstrip().split(",")
            input_device, action, *data = line

            if input_device == "mouse":
                if action == "move":
                    x, y, duration = data
                    result.append((input_device, action, int(x), int(y), float(duration)))

                elif action in {"click_down", "click_up"}:
                    x, y, button, duration = data
                    result.append(
                        (input_device, action, int(x), int(y), button, float(duration)))

                elif action == "scroll":
                    x, y, dx, dy = map(int, data[:4])
                    duration = float(data[4])
                    result.append((input_device, action, x, y, dx, dy, duration))

            else:
                # Предполагается, что сюда попадут оставшиеся
                # {"key_press", "key_release"}
                button, duration = data
                result.append((input_device, action, button, float(duration)))

    return result
