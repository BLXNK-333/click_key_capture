from dataclasses import dataclass
from .recorder_settings import recorder_settings


@dataclass
class Paths:
    start_sound: str
    stop_sound: str
    exit_sound: str
    macros_directory: str


@dataclass
class HotKeys:
    start_record: str
    stop_record: str
    exit_the_program: str


@dataclass
class Settings:
    trim_idle: bool
    stack_time: bool
    duration: float


@dataclass
class Config:
    paths: Paths
    hot_keys: HotKeys
    settings: Settings


def load_config():
    return Config(
        paths=Paths(
            start_sound=recorder_settings["paths"]["start_sound"],
            stop_sound=recorder_settings["paths"]["stop_sound"],
            exit_sound=recorder_settings["paths"]["exit_sound"],
            macros_directory=recorder_settings["paths"]["macros_directory"]
        ),
        hot_keys=HotKeys(
            start_record=recorder_settings["hot_keys"]["start_record"],
            stop_record=recorder_settings["hot_keys"]["stop_record"],
            exit_the_program=recorder_settings["hot_keys"]["exit_the_program"]
        ),
        settings=Settings(
            trim_idle=recorder_settings["settings"]["trim_idle"],
            stack_time=recorder_settings["settings"]["stack_time"],
            duration=recorder_settings["settings"]["duration"]
        )
    )
