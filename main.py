import logging.config
import argparse
import sys
import coloredlogs

from src.config.logging_config import logging_config
from src import (
    load_config,
    record_macro,
    play_macro,
    Help,
    interactive_selection
)


class CustomArgumentParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        print(Help.HELP_MSG)

    def format_usage(self):
        return Help.USAGE_MSG


def parse_args():
    parser = CustomArgumentParser(
        add_help=False  # Отключаем автоматическое добавление -h/--help
    )

    parser.add_argument('-r', '--record', action='store_true')
    parser.add_argument('-k', '--keyboard', action='store_true')
    parser.add_argument('-m', '--mouse', action='store_true')
    parser.add_argument('-p', '--play', action='store_true')
    parser.add_argument('-d', '--delay', type=int, default=None)
    parser.add_argument('macro', nargs='?', default=None)
    parser.add_argument('-h', '--help', action='store_true')

    return parser.parse_args()


def main():
    logging.config.dictConfig(logging_config)
    coloredlogs.install(
        level='DEBUG', fmt=logging_config['formatters']['default']['format'])

    args = parse_args()
    app_config = load_config()

    if args.help:
        print(Help.HELP_MSG)
        sys.exit(0)

    try:
        if args.record:
            rec_mouse = args.mouse or not args.keyboard
            rec_keyboard = args.keyboard or not args.mouse
            record_macro(
                config=app_config, rec_mouse=rec_mouse, rec_keyboard=rec_keyboard)
        elif args.play:
            delay = args.delay
            macro_path = args.macro  # Если макрос не указан, он будет None
            if macro_path is None:
                macro_path = interactive_selection(
                    app_config.paths.macros_directory, ".txt"
                )
            if macro_path:
                play_macro(config=app_config, macro_path=macro_path, delay=delay)
        else:
            logging.error("You must specify a flag first, either -r for "
                          "recording or -p for playback.")
            sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
