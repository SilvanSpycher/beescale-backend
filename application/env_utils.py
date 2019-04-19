import io
import os
import secrets
import sys
from collections import abc
from pathlib import Path
from typing import Union

import dotenv
from colorama import Fore, Style
from dotenv import dotenv_values
from ruamel.yaml import YAML

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML_ENV_FILE = os.path.join(BASE_DIR, '.env.yaml')
DOTENV_FILE = os.path.join(BASE_DIR, '.env')

__all__ = ['load_yaml_env', 'Env']


class empty:  # noqa
    pass


class Env:
    # TODO: Extend with returning a miniEnv on non-existant key in case there is a sub-child lookup.
    #  In that case, miniEnv should respond with an empty dict

    def __init__(self, yaml_env_file: Union[str, dict] = YAML_ENV_FILE, parent=None):
        self.yaml_path = yaml_env_file
        self.parent = parent

        if isinstance(yaml_env_file, str):
            self.yaml = YAML().load(Path(self.yaml_path)) or YAML().load("Remote: true")
        else:
            self.yaml = yaml_env_file

    def __getattr__(self, item):
        return self.get(item)

    def get(self, key, default=empty):
        try:
            value = self.yaml[key]
            if value is not None:
                if isinstance(value, dict):
                    return Env(value, parent=self)
                return value
            raise KeyError(key)
        except KeyError as e:
            if default is not empty:

                # save value
                _dict = self.yaml
                segments = key.split('.')
                for segment in segments[:-1]:
                    _dict = _dict[segment]
                _dict[segments[-1]] = default

                return default

            raise e

    def get_password(self, key, length=12, default=None):
        if not default:
            default = _generate_password(length=length)
        return self.get(key, default)

    def get_root_instance(self):
        root = self
        while root.parent:
            root = root.parent
        return root

    def persist_to_dotenv(self):
        # If you ever need to export the env vars to a "classic" .env, call this method
        def dotter(mixed, key=None):
            dots = {}
            if isinstance(mixed, abc.Mapping):
                for (k, v) in mixed.items():
                    dots.update(dotter(mixed[k], '%s.%s' % (key, k) if key else k))
            elif key:
                dots[key] = mixed

            return dots

        DotEnv().save(dotter(self.yaml))

    def __str__(self):
        output = io.StringIO()
        YAML().dump(self.yaml, output)
        output.seek(0)
        return output.read()

    def persist(self):
        if self.parent is not None:
            print("Must call from parent instance!")
            return

        assert isinstance(self.yaml_path, str), 'Must have valid yaml_path'

        yaml = YAML()
        with open(self.yaml_path, 'w') as fp:
            yaml.dump(self.yaml, fp)


def load_yaml_env(yaml_env_file=YAML_ENV_FILE):
    try:
        return Env(yaml_env_file)
    except FileNotFoundError:
        print(
            f'{Fore.YELLOW}Local {Style.BRIGHT}.env.yaml{Style.NORMAL}{Fore.YELLOW} file not found. '
            f'Make sure you create one inside your project root directory at '
            f'{Style.BRIGHT}{BASE_DIR}{Style.NORMAL}{Fore.RESET}')
        sys.exit(1)


def find_key_value_path(d, key, value):
    for k, v in d.items():
        if isinstance(v, dict) and hasattr(dict.__getitem__):
            p = find_key_value_path(v, key, value)
            if p:
                return [k] + p
        elif k == key and v == value:
            return [k]


def find_key_path(d, key):
    for k, v in d.items():
        if isinstance(v, dict):
            p = find_key_path(v, key)
            if p:
                return [k] + p
        elif k == key:
            return [k]


class DotEnv:
    def __init__(self, env_file=DOTENV_FILE):
        self.env_file = env_file

    def set(self, key, value):
        open(self.env_file, 'a')
        dotenv.set_key(self.env_file, key, str(value) if value else "")

    def get(self, key, default=None):
        open(self.env_file, 'a')
        value = dotenv.get_key(self.env_file, key)
        if value is None and default is not None:
            dotenv.set_key(self.env_file, key, str(default) if default else "")
        return value

    def get_env_password(self, key, default=None, length=12):
        if default is None:
            default = _generate_password(length=length)
        return self.get(key, default)

    def key_exists(self, key):
        d = dotenv_values(self.env_file)
        return find_key_path(d, key) is not None

    def save(self, _dict: dict):
        for key, value in _dict.items():
            self.set(key, value)


def _generate_password(length=12, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"):
    return "".join([secrets.choice(charset) for _ in range(0, length)])
