from __future__ import annotations
from typing import Iterable
from ..domain.contact import Contact
from ..domain.events import CONTACT_CREATED, CONTACT_DELETED
from ..repository.contact_repository import ContactRepository
from ..event_bus.event_bus import EventBus


class CreateContactUseCase:
    def __init__(self, repo: ContactRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def execute(self, name: str, email: str, phone: str) -> Contact:
        contact = Contact(name=name, email=email, phone=phone)
        saved = self._repo.save(contact)
        # publish event
        self._bus.publish(CONTACT_CREATED, {"contact": saved})
        return saved


class GetAllContactsUseCase:
    def __init__(self, repo: ContactRepository) -> None:
        self._repo = repo

    def execute(self) -> Iterable[Contact]:
        return list(self._repo.get_all())


class DeleteContactUseCase:
    def __init__(self, repo: ContactRepository, bus: EventBus) -> None:
        self._repo = repo
        self._bus = bus

    def execute(self, id: str) -> None:
        self._repo.delete(id)
        self._bus.publish(CONTACT_DELETED, {"id": id})
