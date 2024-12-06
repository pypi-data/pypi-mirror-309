from typing import Iterator, Tuple
from .base import BaseStorage, T


class InMemoryStorage(BaseStorage):
    def __init__(self, dataloader):
        self.storage = {}
        super().__init__(dataloader=dataloader)

    def set(self, key: str, value: T):
        self.storage[key] = value

    def get(self, key: str) -> T:
        return self.storage[key]

    def delete(self, key: str):
        del self.storage[key]

    def clear(self):
        self.storage.clear()

    def keys(self) -> Iterator[str]:
        return self.storage.keys()

    def values(self) -> Iterator[T]:
        return self.storage.values()

    def items(self) -> Iterator[Tuple[str, T]]:
        return self.storage.items()

    def __contains__(self, key: str):
        return key in self.storage

    def __len__(self):
        return len(self.storage)
