# TODO
#  1. Дописать main.py
#  2. Удалить принты, добавить логирование вместо них, если надо.
#  3. Удалить закомментированные ненужные участки кода.
#  4. Переписать test_remove_unpaired_up_events.py, прошлая логика не актуальна.

import logging.config
import argparse
import sys
import coloredlogs
from src.config.logging_config import logging_config
from src import record_macro, play_macro, help_message


class CustomArgumentParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        print(help_message)


def parse_args():
    parser = CustomArgumentParser(
        add_help=False  # Отключаем автоматическое добавление -h/--help
    )

    parser.add_argument('-r', '--record', action='store_true')
    parser.add_argument('-k', '--keyboard', action='store_true')
    parser.add_argument('-m', '--mouse', action='store_true')
    parser.add_argument('-p', '--play', nargs='?', const=True, metavar='DELAY')
    parser.add_argument('macro', nargs='?', default=None)
    parser.add_argument('-h', '--help', action='store_true')

    return parser.parse_args()


def main():
    logging.config.dictConfig(logging_config)
    coloredlogs.install(level='DEBUG', fmt=logging_config['formatters']['default']['format'])

    args = parse_args()

    if args.help:
        print(help_message)
        sys.exit(0)

    if args.record:
        rec_mouse = args.mouse or not args.keyboard
        rec_keyboard = args.keyboard or not args.mouse
        record_macro(rec_mouse=rec_mouse, rec_keyboard=rec_keyboard)
    elif args.play:
        delay = args.play if isinstance(args.play, int) else None
        macro_path = args.macro
        play_macro(macro_path, delay)
    else:
        print("Ошибка: Необходимо указать либо -r для записи, либо -p для воспроизведения.")
        sys.exit(1)


if __name__ == '__main__':
    main()

