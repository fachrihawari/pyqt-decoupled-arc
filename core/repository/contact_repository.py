from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, Optional
from ..domain.contact import Contact


class ContactRepository(ABC):
    """Repository interface for Contact persistence."""

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Contact]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Iterable[Contact]:
        raise NotImplementedError

    @abstractmethod
    def save(self, contact: Contact) -> Contact:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError
