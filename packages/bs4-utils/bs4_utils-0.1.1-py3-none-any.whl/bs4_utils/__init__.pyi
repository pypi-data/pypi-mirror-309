import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, Tag
from functools import cached_property as cached_property

class ListItem(ABC, metaclass=abc.ABCMeta):
    text: Incomplete
    children: Incomplete
    def __init__(self, li: Tag) -> None: ...
    @classmethod
    @abstractmethod
    def init_children(cls, li: Tag) -> list[ListItem]: ...
    @classmethod
    @abstractmethod
    def init_text(cls, li: Tag) -> str: ...

class UnorderedList(ABC, metaclass=abc.ABCMeta):
    soup: Incomplete
    def __init__(self, soup: BeautifulSoup) -> None: ...
    @property
    @abstractmethod
    def list_item_class(self) -> type[ListItem]: ...
    @abstractmethod
    def get_root_ul(self) -> Tag: ...
    @cached_property
    def items(self) -> list[ListItem]: ...
    def save(self, filename: str) -> None: ...
    @classmethod
    def from_file(cls, filename: str) -> UnorderedList: ...
