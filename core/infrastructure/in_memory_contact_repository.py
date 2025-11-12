from __future__ import annotations
from threading import RLock
from typing import Dict, List, Optional
from ..domain.contact import Contact
from ..repository.contact_repository import ContactRepository


class InMemoryContactRepository(ContactRepository):
    """Simple thread-safe in-memory repository for Contacts. Suitable for testing/prototyping."""

    def __init__(self) -> None:
        self._store: Dict[str, Contact] = {}
        self._lock = RLock()

    def get_by_id(self, id: str) -> Optional[Contact]:
        with self._lock:
            contact = self._store.get(id)
            # return a shallow copy to avoid accidental external mutation
            return Contact(**contact.__dict__) if contact is not None else None

    def get_all(self) -> List[Contact]:
        with self._lock:
            return [Contact(**c.__dict__) for c in self._store.values()]

    def save(self, contact: Contact) -> Contact:
        with self._lock:
            # store a copy to keep repository as single source of truth
            stored = Contact(**contact.__dict__)
            self._store[stored.id] = stored
            return Contact(**stored.__dict__)

    def delete(self, id: str) -> None:
        with self._lock:
            if id in self._store:
                del self._store[id]
