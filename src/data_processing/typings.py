"""This module contains custom types from structural type hints."""
# Standard library imports
import typing 

class FileLike(typing.Protocol):
    def __fspath__(self) -> str:
        ...


