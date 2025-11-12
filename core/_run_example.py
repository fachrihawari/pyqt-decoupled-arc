"""Small runnable example demonstrating Create and List use cases and EventBus.

Run from repository root:
    python3 core/_run_example.py

This script is intentionally UI-agnostic. It shows how a ViewModel or other
consumer could subscribe to events and react to changes.
"""
from core.event_bus.event_bus import EventBus
from core.infrastructure.in_memory_contact_repository import InMemoryContactRepository
from core.application.use_cases import CreateContactUseCase, GetAllContactsUseCase


def main() -> None:
    bus = EventBus()
    repo = InMemoryContactRepository()

    # Example subscriber (e.g., a ViewModel) reacts to new contacts
    def on_contact_created(payload):
        contact = payload.get("contact")
        print(f"[Subscriber] New contact created: {contact.id} - {contact.name} ({contact.email})")

    unsubscribe = bus.subscribe("ContactCreated", on_contact_created)

    # Use cases
    create_uc = CreateContactUseCase(repo, bus)
    list_uc = GetAllContactsUseCase(repo)

    # Create a couple of contacts
    print("Creating contacts...")
    c1 = create_uc.execute("Alice", "alice@example.com", "+1-555-0100")
    c2 = create_uc.execute("Bob", "bob@example.com", "+1-555-0101")

    # List contacts
    print("Listing all contacts:")
    for c in list_uc.execute():
        print(f" - {c.id}: {c.name} | {c.email} | {c.phone}")

    # Clean up subscriber
    unsubscribe()


if __name__ == "__main__":
    main()
