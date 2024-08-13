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
            if _type == "click_down":
                pressed.add(button)
            else:
                if button in pressed:
                    cleaned_events.append(event)
                    pressed.remove(button)

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
            if _type == "click_up":
                unpressed.add(button)
            else:
                if button in unpressed:
                    cleaned_events.append(events[i])
                    unpressed.remove(button)

    cleaned_events.reverse()
    return cleaned_events


def _cleanup_unpaired_events(events: List[AnyEvent]):
    """
    Удаляет из трека события нажатий и отпусканий клавиш клавиатуры или кликов мыши,
    которые не имеют пары. Например, если клавиша была нажата, но не отжата до
    конца макроса, или наоборот.
    """
    return _remove_unpaired_down_events(
        _remove_unpaired_up_events(events)
    )


def _stack_time_keyboard(events: List[AnyEvent]):
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


def post_process_input_events(events: List[AnyEvent]) -> List[AnyEvent]:
    """
    Функция выполняет пост обработку событий записанных с устройств ввода.
    1. Конвертируем время в задержки.
    2. Складываем задержки одинаковых соседних событий.
    3. Удаляем не парные события [нажатия, отжатия].
    :param events: Записанный макрос.
    :return: (List[KeyboardEvent]) Обработанный макрос.
    """

    return _cleanup_unpaired_events(
        _stack_time_keyboard(convert_time_to_delays(events))
    )


if __name__ == '__main__':
    _events_ = [('key_release', 'Key.ctrl', 1723564444.5224304),
                ('key_release', 'Key.space', 1723564444.5229015),
                ('key_press', "'z'", 1723564446.9984815),
                ('key_press', "'a'", 1723564447.10984),
                ('key_release', "'z'", 1723564447.136293),
                ('key_release', "'a'", 1723564447.2326026),
                ('key_press', "'l'", 1723564447.3530116),
                ('key_release', "'l'", 1723564447.4889426),
                ('key_press', "'u'", 1723564448.6351593),
                ('key_release', "'u'", 1723564448.7363021),
                ('key_press', "'p'", 1723564449.0572848),
                ('key_release', "'p'", 1723564449.1579237),
                ('key_press', "'a'", 1723564449.2428613),
                ('key_release', "'a'", 1723564449.343996),
                ('key_press', 'Key.ctrl', 1723564450.602112)]

    pprint.pprint(post_process_input_events(_events_))
