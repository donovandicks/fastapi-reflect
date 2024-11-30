from abc import ABC
from typing import Generic, Sequence, TypeVar

from pydantic import UUID4

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    def list(self) -> Sequence[T]: ...
    def get(self, id: UUID4) -> T | None: ...
    def create(self, obj: T) -> T: ...
    def delete(self, id: UUID4) -> None: ...