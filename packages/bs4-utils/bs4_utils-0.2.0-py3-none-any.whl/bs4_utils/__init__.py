from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from functools import cached_property

from bs4 import BeautifulSoup, Tag

if sys.version_info >= (3, 11):
    from typing import Self


class ListItem(ABC):
    def __init__(self, tag: Tag, parent: ListItem | None = None) -> None:
        self.__tag = tag
        self.__parent = parent

    @property
    def parent(self) -> ListItem | None:
        return self.__parent

    @property
    def tag(self) -> Tag:
        return self.__tag

    @cached_property
    def children(self) -> list[ListItem]:
        return self.init_children()

    @cached_property
    def text(self) -> str:
        return self.init_text()

    @abstractmethod
    def init_children(self) -> list[ListItem]:
        pass

    @abstractmethod
    def init_text(self) -> str:
        pass

    @cached_property
    def depth(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    @cached_property
    def height(self) -> int:
        if not self.children:
            return 0
        return 1 + max(child.height for child in self.children)


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

    @cached_property
    def height(self) -> int:
        return max(item.height for item in self.items)

    def save(
        self,
        filename: str,
        indent: int = 2,
        max_depth: int | None = None,
    ) -> None:
        def _get_text(node: ListItem, depth: int) -> str:
            text = " " * depth * indent + node.text
            if node.children and (max_depth is None or depth < max_depth):
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
