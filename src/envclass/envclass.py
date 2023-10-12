from typing import IO


from os import getenv, environ
from dotenv import load_dotenv


class EnvClass:
    def __init__(
            self,
            env_file: str | None = None,
            stream: IO[str] | None = None,
            verbose: bool = False,
            override: bool = False,
            interpolate: bool = True,
            encoding: str | None = "utf-8"
        ):

        load_dotenv(
            env_file,
            stream,
            verbose,
            override,
            interpolate,
            encoding
        )

        self.__parse_attributes()


    def __parse_attributes(self):
        cls = self.__class__
        proxy_types = vars(cls)
        attributes = proxy_types['__annotations__']
        attributes_items = attributes.items()


        for label, attrib in attributes_items:
            self._label = label
            self._attrib = attrib

            setattr(
                self,
                label,
                self.__read_only_atributte
            )

    def parse_attrib(
            self,
            label: str,
            attrib: type,
            default=None
        ):
        breakpoint()
        return attrib(getenv(label.upper()) or default)

    def get_attribute(self):
        default = getattr(self, self._label, '')

        return self.parse_attrib(
            self._label,
            self._attrib,
            default,
        )

    __read_only_atributte = property(get_attribute)
