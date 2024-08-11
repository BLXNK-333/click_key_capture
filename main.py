from src.config.recorder_config import load_config
from src.macros_recorder import MacrosRecorder


def main():
    config = load_config()
    macros_recorder = MacrosRecorder(config=config)


if __name__ == '__main__':
    main()