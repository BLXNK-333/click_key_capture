import pprint
from typing import List
from src.event_handlers.events import AnyEvent


def convert_time_to_delays(events: List[AnyEvent]):
    """
    Заменяет временную метку события на задержку относительно
    времени наступления предыдущего события.
    """
    if not events:
        return []

    converted = []

    for current, next_event in zip(events, events[1:]):
        *data, cur_time = current
        next_time = next_event[-1]
        delay = next_time - cur_time
        converted.append((*data, delay))

    return converted


def _remove_unpaired_up_events(events: List[AnyEvent]):
    cleaned_events = []
    untracked = {"move", "scroll"}
    pressed = set()

    for event in events:
        _type = event[0]
        if _type in untracked:
            cleaned_events.append(event)
            continue

        if _type.startswith("key"):
            button = event[1]
            if _type == "key_press":
                cleaned_events.append(event)
                pressed.add(button)
            elif _type == "key_release" and button in pressed:
                cleaned_events.append(event)
                pressed.remove(button)
        else:
            button = event[3]
            _key = "click" + button
            if _type == "click_down":
                cleaned_events.append(event)
                pressed.add(_key)
            else:
                if _key in pressed:
                    cleaned_events.append(event)
                    pressed.remove(_key)

    return cleaned_events


def _remove_unpaired_down_events(events: List[AnyEvent]):
    cleaned_events = []
    untracked = {"move", "scroll"}
    unpressed = set()

    for i in range(len(events) - 1, -1, -1):
        _type = events[i][0]
        if _type in untracked:
            cleaned_events.append(events[i])
            continue

        if _type.startswith("key"):
            button = events[i][1]
            if _type == "key_release":
                cleaned_events.append(events[i])
                unpressed.add(button)
            elif _type == "key_press" and button in unpressed:
                cleaned_events.append(events[i])
                unpressed.remove(button)
        else:
            button = events[i][3]
            _key = "click" + button
            if _type == "click_up":
                cleaned_events.append(events[i])
                unpressed.add(_key)
            else:
                if _key in unpressed:
                    cleaned_events.append(events[i])
                    unpressed.remove(_key)

    cleaned_events.reverse()
    return cleaned_events


def cleanup_unpaired_events(events: List[AnyEvent]):
    """
    Удаляет из трека события нажатий и отпусканий клавиш клавиатуры или кликов мыши,
    которые не имеют пары. Например, если клавиша была нажата, но не отжата до
    конца макроса, или наоборот.
    """
    return _remove_unpaired_down_events(
        _remove_unpaired_up_events(events)
    )


def stack_time_keyboard(events: List[AnyEvent]):
    """
    Складывает время задержек для последовательных нажатий или отпусканий
    одной и той же клавиши.
    """
    if not events:
        return []

    stacked_events = []

    empty_field = ("", "", 0.0)
    events.append(empty_field)
    prev_event, prev_key, stacked_delay = empty_field

    for i in range(len(events)):
        event_type = events[i][0]
        if event_type.startswith("key"):
            cur_event, cur_key, delay = events[i]
            if cur_key == prev_key and cur_event == prev_event:
                stacked_delay += delay
                continue

        if event_type.startswith("key"):
            if prev_key:
                stacked_events.append((prev_event, prev_key, stacked_delay))
            prev_event, prev_key, stacked_delay = events[i]
        else:
            if prev_key:
                stacked_events.append((prev_event, prev_key, stacked_delay))
            stacked_events.append(events[i])
            prev_event, prev_key, stacked_delay = empty_field
    if stacked_events[-1] == empty_field:
        stacked_events.pop()
    return stacked_events


def insert_hot_corner_activate(events: List[AnyEvent]):
    """
    Обрабатывает последовательность событий, добавляя активацию горячего
    угла при перемещении мыши в координаты (0, 0) и изменяя время задержки
    следующего события.
    """
    is_active = False
    result = []
    n, debt = len(events), 0.0

    for event in events:
        action = event[0]

        if action == "move":
            x, y = event[1], event[2]

            if not x and not y:
                if not is_active:
                    is_active = True
                    debt = 0.001
                    result.extend([
                        event,
                        ("key_press", "Key.cmd", 0.0005),
                        ("key_release", "Key.cmd", 0.0005)
                    ])
                    continue
        if debt:
            *data, delay = event
            new_delay = round(delay - debt, 10)
            event = (*data, new_delay)
            debt = 0.0
            is_active = False

        result.append(event)

    return result


def post_process_input_events(events: List[AnyEvent]) -> List[AnyEvent]:
    """
    Функция выполняет постобработку событий, записанных с устройств ввода.
    1. Конвертирует время в задержки.
    2. Складывает задержки одинаковых соседних событий.
    3. Удаляет не парные события (нажатия и отжатия).
    4. Добавляет активацию горячего угла при перемещении мыши в координаты (0, 0).

    :param events: Записанный макрос.
    :return: Обработанный макрос.
    """
    return insert_hot_corner_activate(
        cleanup_unpaired_events(
            stack_time_keyboard(
                convert_time_to_delays(events)
            )
        )
    )


if __name__ == '__main__':

    # from src.file_io.file_io import read_macro
    #
    # filename = "zalupa"
    # compare = "2024-08-16_14-23-11_683"
    #
    # def get_macro(_file_name: str):
    #     macro_path = (f"/home/blxnk/PycharmProjects/click_key_capture/"
    #                   f"macros/{_file_name}.txt")
    #     return read_macro(macro_path)
    #
    # target_macro = get_macro(filename)
    # compare_macro = get_macro(compare)
    #
    # target_macro = insert_hot_corner_activate(target_macro)

    # for t, c in zip(target_macro, compare_macro):
    #     print(t == c, t, c)

    events = [
        ("move", 0, 0, 0.01),
        ("click", "left", 0.01),
        ("move", 0, 0, 0.02),
        ("move", 0, 0, 0.03)
    ]

    pprint.pprint(insert_hot_corner_activate(events))
