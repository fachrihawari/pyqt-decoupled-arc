"""
Intent - User actions/intentions in the MVI pattern.
All possible user actions are defined here as immutable data classes.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Intent:
    """Base class for all user intents."""
    pass


@dataclass(frozen=True)
class LoadContacts(Intent):
    """Intent to load all contacts."""
    pass


@dataclass(frozen=True)
class AddContact(Intent):
    """Intent to add a new contact."""
    name: str
    email: str
    phone: str = ""


@dataclass(frozen=True)
class DeleteContact(Intent):
    """Intent to delete a contact."""
    contact_id: str


@dataclass(frozen=True)
class RefreshContacts(Intent):
    """Intent to refresh the contact list."""
    pass


@dataclass(frozen=True)
class NavigateToAdd(Intent):
    """Intent to navigate to add contact page."""
    pass


@dataclass(frozen=True)
class NavigateToList(Intent):
    """Intent to navigate to contact list page."""
    pass
