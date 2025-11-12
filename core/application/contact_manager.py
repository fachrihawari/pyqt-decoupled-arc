from typing import Optional, Callable
from core.domain.contact import Contact
from core.domain.events import CONTACT_CREATED, CONTACT_DELETED
from core.event_bus.event_bus import EventBus
from core.repository.contact_repository import ContactRepository
from core.infrastructure.in_memory_contact_repository import InMemoryContactRepository
from .use_cases import CreateContactUseCase, GetAllContactsUseCase, DeleteContactUseCase

class ContactManager:
    def __init__(self, repo: ContactRepository, event_bus: EventBus):
        self.repo = repo
        self.event_bus = event_bus
        self.create_uc = CreateContactUseCase(repo, event_bus)
        self.list_uc = GetAllContactsUseCase(repo)
        self.delete_uc = DeleteContactUseCase(repo, event_bus)

    def seed_data(self):
        """Optional: Seed with initial data for testing/demo purposes."""
        self.create_contact(name="Alice Smith", email="alice@example.com", phone="+1-555-0100")
        self.create_contact(name="Bob Johnson", email="bob@example.com", phone="+1-555-0101")

    @classmethod
    def create(cls) -> 'ContactManager':
        """Factory method: Creates a manager with in-memory repo and event bus."""
        repo = InMemoryContactRepository()
        event_bus = EventBus()

        return cls(repo, event_bus)

    def create_contact(self, name: str, email: str, phone: str = "") -> Contact:
        result = self.create_uc.execute(name, email, phone)
        self.event_bus.publish(CONTACT_CREATED, {"contact": result})
        return result

    def get_all_contacts(self) -> list[Contact]:
        return self.list_uc.execute()

    def delete_contact(self, contact_id: str) -> bool:
        result = self.delete_uc.execute(contact_id)
        if result:
            self.event_bus.publish(CONTACT_DELETED, {"contact_id": contact_id})
        return result

    def subscribe_to_events(self, event_name: str, callback: Callable) -> Optional[Callable]:
        """Subscribe to domain events (for complex state)."""
        self.event_bus.subscribe(event_name, callback)