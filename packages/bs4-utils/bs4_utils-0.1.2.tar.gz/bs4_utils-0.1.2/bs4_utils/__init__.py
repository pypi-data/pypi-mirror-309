from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from functools import cached_property

from bs4 import BeautifulSoup, Tag

if sys.version_info >= (3, 11):
    from typing import Self


class ListItem(ABC):
    text: str
    children: list[ListItem]

    def __init__(self, li: Tag) -> None:
        self.text = self.init_text(li)
        self.children = self.init_children(li)

    @classmethod
    @abstractmethod
    def init_children(cls, li: Tag) -> list[ListItem]:
        pass

    @classmethod
    @abstractmethod
    def init_text(cls, li: Tag) -> str:
        pass


class UnorderedList(ABC):
    soup: BeautifulSoup

    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    @property
    @abstractmethod
    def list_item_class(self) -> type[ListItem]:
        pass

    @abstractmethod
    def get_root_ul(self) -> Tag:
        pass

    @cached_property
    def items(self) -> list[ListItem]:
        return [
            self.list_item_class(li)
            for li in self.get_root_ul().find_all("li", recursive=False)
        ]

    def save(
        self,
        filename: str,
        indent: int = 2,
    ) -> None:
        def _get_text(node: ListItem, depth: int) -> str:
            text = " " * depth * indent + node.text
            if node.children:
                return f"{text}\n" + "\n".join(
                    [_get_text(child, depth + 1) for child in node.children]
                )
            return text

        text: str = "\n".join([_get_text(root, 0) for root in self.items])
        with open(filename, "w") as f:
            f.write(text)

    if sys.version_info >= (3, 11):

        @classmethod
        def from_file(cls, filename: str) -> Self:
            with open(filename, "r") as file:
                return cls(BeautifulSoup(file, "html.parser"))
    else:

        @classmethod
        def from_file(cls, filename: str) -> UnorderedList:
            with open(filename, "r") as file:
                return cls(BeautifulSoup(file, "html.parser"))
