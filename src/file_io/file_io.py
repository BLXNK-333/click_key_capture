import logging
import os.path
import csv
from typing import List, Union, Optional

from ..event_handlers.events import MouseEvent, KeyboardEvent, AnyEvent, Action


def write_macro(
        filename: str,
        data: List[Union[MouseEvent, KeyboardEvent]],
        path: str,
):
    """
    Эта функция записывает макрос в файл. Вызывается в отдельном процессе,
    а логики возврата чего-либо в основной процесс не написано.
    """
    # Изменяем расширение на .txt
    if not os.path.exists(path):
        os.makedirs(path)

    filename = os.path.join(path, f"{filename}.txt")

    # Записываем данные в файл с использованием json.dump
    with open(filename, "w") as file:
        for line in data:
            file.write(f'{",".join([f'"{elem}"' for elem in line])}\n')
        print(f"\nFile '{filename}' has been saved successfully.\n")


def read_macro(file_path: str) -> Optional[List[AnyEvent]]:
    """
    Функция читает файл txt с записанным макросом и переводит его
    в список с tuples, где tuple это какое-либо событие с устройств ввода.
    Если файл прочитать не удалось, тогда возвращает None.

    :param file_path: (str) Путь до файла.
    :return: Optional[List[AnyEvent]] Список с событиями или ничего.
    """
    result = []
    # Странно, но logger пришлось объявить здесь, потому что функция
    # не видит его в глобальной зоне видимости, а класс создавать пока
    # нет смысла.
    logger = logging.getLogger(__name__)
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            for line_number, line in enumerate(reader, 1):
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

    except ValueError as e:
        logger.error(f"Error reading file on line {line_number}: {e}")
        return None
