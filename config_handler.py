import os
from dataclasses import dataclass
from environs import Env


class NoValueException(Exception):
    def __str__(self):
        return 'Not variable in config'


path: str


@dataclass
class TgBot:
    some_token: str
    moneys: int
    admins: list[int]
    bool_value: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous


def load_env_config(cfg_path: str = None) -> Config:
    global path
    path = cfg_path
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            some_token=env.str("SOME_TOKEN"),
            moneys=env.int("MONEYS"),
            admins=list(map(int, env.list("ADMINS"))),
            bool_value=env.bool("BOOL_VALUE"),
        ),
        misc=Miscellaneous()
    )


def set_variable(variable: str, value):
    with open(path, 'r') as file:
        start_config = file.read()
    data = start_config
    try:
        data = data[data.index(variable):]
    except ValueError:
        raise NoValueException
    data = data[data.index('=')+1:]
    old_value = data[:data.index('\n')]
    start_config = start_config.replace(f'{variable}={old_value}', f'{variable}={str(value)}')
    with open(path, 'w') as file:
        file.write(start_config)

    # After set a variable you need to restart project,
    # because the library not load two times per session
