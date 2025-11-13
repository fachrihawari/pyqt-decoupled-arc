"""
Contracts (Interfaces) for MVP Pattern.

MVP Pattern:
- Model: Business logic (Core module)
- View: UI interface (passive, just displays data)
- Presenter: Mediator between View and Model (handles all logic)

The View and Presenter communicate through contracts (interfaces).
"""
from abc import ABC, abstractmethod
from typing import List


class ContactListContract:
    """
    Contract between View and Presenter for Contact List feature.
    This defines what the View can do and what the Presenter expects.
    """
    
    class View(ABC):
        """
        View interface - what the Presenter can call on the View.
        The View is passive and only knows how to display data.
        """
        
        @abstractmethod
        def show_contacts(self, contacts: List[dict]):
            """Display list of contacts."""
            pass
        
        @abstractmethod
        def show_error(self, message: str):
            """Display error message."""
            pass
        
        @abstractmethod
        def show_loading(self):
            """Show loading indicator."""
            pass
        
        @abstractmethod
        def hide_loading(self):
            """Hide loading indicator."""
            pass
        
        @abstractmethod
        def show_success_message(self, message: str):
            """Show success message."""
            pass
        
        @abstractmethod
        def close_add_dialog(self):
            """Close the add contact dialog."""
            pass
        
        @abstractmethod
        def clear_add_dialog_form(self):
            """Clear input fields in add dialog."""
            pass
    
    class Presenter(ABC):
        """
        Presenter interface - what the View can call on the Presenter.
        The Presenter handles all logic and user interactions.
        """
        
        @abstractmethod
        def attach_view(self, view: 'ContactListContract.View'):
            """Attach the View to this Presenter."""
            pass
        
        @abstractmethod
        def detach_view(self):
            """Detach the View (cleanup)."""
            pass
        
        @abstractmethod
        def load_contacts(self):
            """Load contacts from Model."""
            pass
        
        @abstractmethod
        def on_add_contact_clicked(self):
            """Handle add contact button click."""
            pass
        
        @abstractmethod
        def on_delete_contact_clicked(self, contact_id: str):
            """Handle delete contact button click."""
            pass
        
        @abstractmethod
        def on_save_contact_clicked(self, name: str, email: str, phone: str):
            """Handle save contact in dialog."""
            pass
        
        @abstractmethod
        def on_refresh_clicked(self):
            """Handle refresh button click."""
            pass
