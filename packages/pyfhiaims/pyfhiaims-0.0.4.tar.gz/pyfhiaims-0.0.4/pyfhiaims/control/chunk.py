"""A class representing a chunk of control.in file"""

from dataclasses import dataclass
from inspect import isclass
from typing import Sequence

from monty.json import MSONable


@dataclass(kw_only=True)
class AimsControlChunk(MSONable):
    keywords: tuple[str] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        keywords = []
        if not cls.keywords:
            for field in cls.__annotations__.values():
                if isclass(field) and issubclass(field, AimsControlChunk):
                    keywords += list(field.keywords)
            cls.keywords = tuple(keywords)

    @classmethod
    def from_strings(cls, config_str: Sequence[str]) -> "AimsControlChunk":
        raise NotImplementedError

    def to_string(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.to_string()
