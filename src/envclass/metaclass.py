import os, re

from typing import get_type_hints


class MetaClass(type):
    _strict = True
    _prefix = None

    _env_file = None


    __env_repl = ''
    __read_only = False

    __TRUE_VALIDATOR = ('True', 'true', '1')
    __FALSE_VALIDATOR = ('False', 'false', '0')


    def __init__(cls, __name, __base, __dct):
        if cls._env_file is not None:
            cls.parse_env(cls._env_file)

        cls._init_attrs()


    def __setattr__(cls, name: str, value):
        if cls.__read_only and name != '_MetaClass__read_only':
            raise AttributeError('Attribute is Read-Only')
        return super().__setattr__(name, value)

    def __str__(cls):
        return cls.__env_repl.strip()


    def _init_attrs(cls):
        cls.__read_only = False
        hints = get_type_hints(cls)

        for label, attrib in hints.items():
            default = getattr(cls, label, None)

            [key, value] = cls.parse_attrib(
                label,
                attrib,
                default
            )

            cls.__env_repl += f'{key}={value!r}\n'
            setattr(cls, label, value)

        cls.__read_only = True

    def _get_env(cls, label: str, default_exists: bool):
        if not default_exists and cls._strict:
            return os.environ[label]

        return os.environ.get(label)


    def parse_env(cls, env_file: str):
        if os.path.isfile(env_file):
            with open(env_file, encoding='utf-8') as stream:
                env_content = stream.read()
                env_list = re.findall(
                    r'^([A-Za-z]\w*)=(\w*)',
                    env_content,
                    re.MULTILINE,
                )

                for name, value in env_list:
                    os.environ[name] = value

    def parse_label(cls, label: str):
        prefix = ''
        label = label.upper()

        if cls._prefix is not None:
            prefix = cls._prefix + '_'

        return prefix + label

    def parse_attrib(
            cls,
            label: str,
            attrib: type,
            default=None
        ):
        default_exists = default is not None
        upper_label = cls.parse_label(label)

        env_value = cls._get_env(
            upper_label,
            default_exists,
        )

        if env_value == '':
            return [upper_label, None]

        if attrib is bool:
            if env_value in cls.__TRUE_VALIDATOR:
                return [upper_label, True]
            elif env_value in cls.__FALSE_VALIDATOR:
                return [upper_label, False]

        if env_value is not None:
            value = attrib(env_value)
            return [upper_label, value]

        return [upper_label, default]
