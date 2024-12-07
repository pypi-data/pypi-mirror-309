from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cached_property
from typing import Callable, Iterable, Self

from bs4 import BeautifulSoup, Tag


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

    def depth_first_traverse(
        self,
        max_depth: int | None = None,
    ) -> Iterable[ListItem]:
        if max_depth is not None and self.depth > max_depth:
            return
        yield self
        for child in self.children:
            yield from child.depth_first_traverse(max_depth=max_depth)

    def breadth_first_traverse(
        self,
        max_depth: int | None = None,
    ) -> Iterable[ListItem]:
        current_level: list[ListItem] = [self]
        next_level: list[ListItem] = []
        while current_level:
            if max_depth is not None and current_level[0].depth > max_depth:
                return
            for item in current_level:
                yield item
                next_level.extend(item.children)
            current_level = next_level
            next_level = []


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

    def depth_first_traverse(
        self,
        max_depth: int | None = None,
    ) -> Iterable[ListItem]:
        for item in self.items:
            yield from item.depth_first_traverse(max_depth=max_depth)

    def breadth_first_traverse(self) -> Iterable[ListItem]:
        current_level: list[ListItem] = self.items
        next_level: list[ListItem] = []
        while current_level:
            for item in current_level:
                yield item
                next_level.extend(item.children)
            current_level = next_level
            next_level = []

    def save(
        self,
        filename: str,
        indent: int = 2,
        max_depth: int | None = None,
        item_formatter: Callable[[ListItem], str] | None = None,
    ) -> None:
        text = ""
        for item in self.depth_first_traverse(max_depth=max_depth):
            if item_formatter:
                text += item_formatter(item)
                if not text.endswith("\n"):
                    text += "\n"
            else:
                text += f'{" " * item.depth * indent}{item.text}\n'
        with open(filename, "w") as f:
            f.write(text)

    @classmethod
    def from_file(cls, filename: str) -> Self:
        with open(filename, "r") as file:
            return cls(BeautifulSoup(file, "html.parser"))
