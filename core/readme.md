
# Core — Contact Management (UI-agnostic)

This `core` package implements a UI-agnostic domain and application layer for a
Contact Management application following Clean Architecture / DDD principles.

It is intended to be reused by multiple clients (PyQt, CLI, web backends, etc.)
and purposely contains no UI or framework-specific code.

Key responsibilities
- Domain: Contact entity and domain event names
- Application: Use cases (Create, List, Delete) which orchestrate repository and publish events
- Infrastructure: Repository interfaces and an in-memory implementation for testing/prototyping
- Event bus: Lightweight, thread-safe pub/sub for domain events

Package layout

core/
├── __init__.py — convenience exports
├── _run_example.py — small runnable demo (create + list)
├── event_bus/
│   ├── __init__.py
│   └── event_bus.py — EventBus class
├── domain/
│   ├── __init__.py
│   ├── contact.py — Contact dataclass
│   └── events.py — event name constants
├── repository/
│   ├── __init__.py
│   └── contact_repository.py — repository interface (abstract)
├── infrastructure/
│   ├── __init__.py
│   └── in_memory_contact_repository.py — simple in-memory repo
└── application/
		├── __init__.py
		└── use_cases.py — Create/GetAll/Delete use cases

Highlights

- EventBus: `EventBus.subscribe(event_name, callback)` returns an `unsubscribe()`
	function. Use `EventBus.publish(event_name, payload)` to notify subscribers.
- The `Contact` entity is a simple `dataclass` with `id`, `name`, `email`, `phone`.
- `ContactRepository` is an abstract interface. The in-memory repository is
	`InMemoryContactRepository` (thread-safe) — useful for tests and prototyping.
- Use cases:
	- `CreateContactUseCase(repo, bus)` — creates a Contact, saves via repository,
		and publishes the `ContactCreated` event with payload `{"contact": contact}`.
	- `GetAllContactsUseCase(repo)` — returns an iterable of contacts.
	- `DeleteContactUseCase(repo, bus)` — deletes and publishes `ContactDeleted`.

Quickstart (from project root)

Run the small example which demonstrates subscribing to `ContactCreated` and
creating/listing contacts:

```bash
python3 -m core._run_example
```

Example usage (in code)

```python
from core.event_bus.event_bus import EventBus
from core.infrastructure.in_memory_contact_repository import InMemoryContactRepository
from core.application.use_cases import CreateContactUseCase, GetAllContactsUseCase

bus = EventBus()
repo = InMemoryContactRepository()

def on_created(payload):
		contact = payload.get("contact")
		print("Contact created:", contact)

unsubscribe = bus.subscribe("ContactCreated", on_created)

create_uc = CreateContactUseCase(repo, bus)
list_uc = GetAllContactsUseCase(repo)

create_uc.execute("Alice", "alice@example.com", "+1-555-0100")
print(list(list_uc.execute()))

unsubscribe()
```

Extending for production

- Implement a persistent repository that conforms to `ContactRepository` (e.g.
	SQLite, Postgres). Keep the same interface so the application layer stays
	unchanged.
- Add domain validations (value objects for Email, Phone) and surface errors
	via use case responses or exceptions.
- Add unit tests for EventBus, repository implementations and use cases.

License & attribution

This module is intentionally minimal and framework-free so it can be embedded
in different UI clients. Feel free to adapt and extend for your projects.
