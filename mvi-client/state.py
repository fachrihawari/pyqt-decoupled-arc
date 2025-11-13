"""
State - Immutable application state in the MVI pattern.
Represents the entire UI state at any point in time.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class ViewState(Enum):
    """Possible view states."""
    LIST = "list"
    ADD = "add"


class LoadingState(Enum):
    """Loading states for async operations."""
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"


@dataclass(frozen=True)
class ContactState:
    """
    Immutable application state.
    Every field is immutable to ensure predictable state transitions.
    """
    # Navigation
    current_view: ViewState = ViewState.LIST
    
    # Data
    contacts: List[dict] = field(default_factory=list)
    
    # Loading states
    loading_state: LoadingState = LoadingState.IDLE
    error_message: Optional[str] = None
    
    # Form state (for add contact)
    form_name: str = ""
    form_email: str = ""
    form_phone: str = ""
    
    def copy_with(self, **kwargs):
        """
        Create a new state with updated fields.
        This ensures immutability while allowing updates.
        """
        from dataclasses import replace
        return replace(self, **kwargs)
