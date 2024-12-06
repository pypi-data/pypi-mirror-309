from __future__ import annotations
from typing import Tuple, TypeVar, Generic, Iterator, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from ..dataloader import DataLoader

T = TypeVar("T")


class BaseStorage(ABC, Generic[T]):
    def __init__(self, dataloader: DataLoader):
        self.dataloader = dataloader

    @abstractmethod
    def set(self, key: str, value: T) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> T:
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def keys(self) -> Iterator[str]:
        pass

    @abstractmethod
    def values(self) -> Iterator[T, None, None]:
        pass

    def items(self) -> Iterator[Tuple[str, T]]:
        for key in self.keys():
            yield key, self.get(key)

    def __contains__(self, key: str) -> bool:
        return key in list(self.keys())

    def __len__(self) -> int:
        return len(list(self.keys()))

    def __iter__(self) -> Iterator[Tuple[str, T]]:
        return self.values()

    def __getitem__(self, key: str) -> T:
        self.get(key)

    def __setitem__(self, key: str, value: T):
        self.set(key, value)

    def __delitem__(self, key: str):
        self.delete(key)
