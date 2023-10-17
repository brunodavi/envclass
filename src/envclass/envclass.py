import os

from re import findall


class EnvClass:
    _strict = True
    _class_as_prefix = False

    _prefix = None
    _joiner = '_'

    _load_env = True


    def __init__(
            self,
            env_file: str = '.env',
        ):

        if self._load_env:
            self.parse_env(env_file)

        self._init_attrs()

    def _init_attrs(self):
        attributes = self.__annotations__
        attributes_items = attributes.items()

        for label, attrib in attributes_items:
            self._label = label
            self._attrib = attrib

            setattr(
                self,
                label,
                self._read_only_attribute
            )

    def _get_env(self, label: str, default_exists: bool):
        if not default_exists and self._strict:
            return os.environ[label]

        return os.environ.get(label)

    def _get_attribute(self):
        default = getattr(self, self._label, None)

        return self.parse_attrib(
            self._label,
            self._attrib,
            default,
        )

    def parse_env(self, env_file: str):
        if os.path.isfile(env_file):
            with open(env_file, encoding='utf-8') as stream:
                for line in stream:
                    try:
                        [(name, value)] = findall(r'^([A-Za-z]\w+)=(\w*)', line)
                        os.environ[name] = value
                    except ValueError:
                        continue
                return True
        return False

    def parse_label(self, label: str):
        prefix = ''
        joiner = self._joiner
        label = label.upper()

        if self._class_as_prefix:
            cls_name = type(self).__name__

            words = findall(r'[A-Z][a-z-0-9]+', cls_name)

            if len(words) > 1:
                prefix = joiner.join(words).upper()
            else:
                prefix = cls_name.upper()

            prefix += joiner

        if self._prefix is not None:
            prefix = self._prefix + joiner

        return prefix + label

    def parse_attrib(
            self,
            label: str,
            attrib: type,
            default=None
        ):
        default_exists = default is not None
        upper_label = self.parse_label(label)

        env_value = self._get_env(
            upper_label,
            default_exists,
        )

        if env_value == '':
            return None

        if attrib is bool:
            if env_value in 'True true 1'.split():
                return True
            elif env_value in 'False false 0'.split():
                return False

        if env_value is not None:
            value = attrib(env_value)

            return value

        return default

    _read_only_attribute = property(_get_attribute)
