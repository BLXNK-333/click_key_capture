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
    toggle_recording: str
    exit_the_program: str
    switch_layout: str


@dataclass
class Settings:
    delay: float
    mouse_record: True
    keyboard_record: True
    delay_before_playback: int


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
            toggle_recording=recorder_settings["hot_keys"]["toggle_recording"],
            exit_the_program=recorder_settings["hot_keys"]["exit_the_program"],
            switch_layout=recorder_settings["hot_keys"]["switch_layout"]
        ),
        settings=Settings(
            mouse_record=recorder_settings["settings"]["mouse_record"],
            keyboard_record=recorder_settings["settings"]["keyboard_record"],
            delay=recorder_settings["settings"]["delay"],
            delay_before_playback=recorder_settings["settings"]["delay_before_playback"]
        )
    )
