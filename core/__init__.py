"""Core package for Contact Management (UI-agnostic).

Expose commonly used classes at package level for convenience.
"""
from .event_bus.event_bus import EventBus
from .domain.contact import Contact
from .domain.events import CONTACT_CREATED, CONTACT_DELETED
from .repository.contact_repository import ContactRepository
from .infrastructure.in_memory_contact_repository import InMemoryContactRepository
from .application.use_cases import (
    CreateContactUseCase,
    GetAllContactsUseCase,
    DeleteContactUseCase,
)

__all__ = [
    "EventBus",
    "Contact",
    "CONTACT_CREATED",
    "CONTACT_DELETED",
    "ContactRepository",
    "InMemoryContactRepository",
    "CreateContactUseCase",
    "GetAllContactsUseCase",
    "DeleteContactUseCase",
]
