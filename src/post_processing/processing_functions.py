from typing import List, Set
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


def remove_unpaired_up_events(events: List[AnyEvent]):
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
            if len(event) >= 4 and isinstance(event[3], (str, int)):
                button = event[3]
                _key = "click_" + str(button)
                if _type == "click_down":
                    cleaned_events.append(event)
                    pressed.add(_key)
                elif _key in pressed:
                    cleaned_events.append(event)
                    pressed.remove(_key)

    return cleaned_events, pressed


def remove_unpaired_down_events(events: List[AnyEvent], pressed: Set[str]):
    if not pressed:
        return events

    cleaned_events = []
    untracked = {"move", "scroll"}

    for event in reversed(events):
        _type = event[0]

        if _type in untracked:
            cleaned_events.append(event)
            continue

        if _type.startswith("key"):
            button = event[1]
            if _type == "key_press" and button in pressed:
                pressed.remove(button)
            else:
                cleaned_events.append(event)
        else:
            if len(event) >= 4 and isinstance(event[3], (str, int)):
                button = event[3]
                _key = f"click_{button}"
                if _type == "click_down" and _key in pressed:
                    pressed.remove(_key)
                else:
                    cleaned_events.append(event)

    return cleaned_events[::-1]


def cleanup_unpaired_events(events: List[AnyEvent]):
    """
    Удаляет из трека события нажатий и отпусканий клавиш клавиатуры или кликов мыши,
    которые не имеют пары. Например, если клавиша была нажата, но не отжата до
    конца макроса, или наоборот.
    """
    return remove_unpaired_down_events(*remove_unpaired_up_events(events))


def insert_hot_corner_activate(events: List[AnyEvent]):
    """
    Обрабатывает последовательность событий, добавляя активацию горячего
    угла при перемещении мыши в координаты (0, 0) и изменяя время задержки
    следующего события.
    """
    is_active = False
    result = []
    debt = 0.0

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
                convert_time_to_delays(events)
                )
            )
