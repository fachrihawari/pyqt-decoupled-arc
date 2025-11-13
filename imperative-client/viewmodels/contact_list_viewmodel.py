"""
ViewModel for Contact List
Handles business logic presentation and state management for the contact list view.
"""
import sys
sys.path.insert(0, '../../')

from PyQt6.QtCore import QObject, pyqtSignal
from core.application.contact_manager import ContactManager
from core.serializers import contacts_to_dict_list, contact_to_dict


class ContactListViewModel(QObject):
    """
    ViewModel for the contact list view.
    Acts as an intermediary between the View (UI) and the Model (Core).
    
    This implementation optimizes updates by directly manipulating state
    instead of re-fetching from the repository on every change.
    """
    
    # Signals to notify the view of changes
    contacts_changed = pyqtSignal(list)  # Emits list of contact dicts
    error_occurred = pyqtSignal(str)     # Emits error message
    
    def __init__(self, contact_manager: ContactManager):
        super().__init__()
        self._manager = contact_manager
        self._contacts = []
        
        # Load initial data
        self.refresh_contacts()
    
    @property
    def contacts(self):
        """Get the current list of contacts."""
        return self._contacts
    
    def refresh_contacts(self):
        """Refresh contacts from the core and notify view."""
        try:
            domain_contacts = self._manager.get_all_contacts()
            self._contacts = contacts_to_dict_list(domain_contacts)
            self.contacts_changed.emit(self._contacts)
        except Exception as e:
            self.error_occurred.emit(f"Failed to load contacts: {str(e)}")
    
    def add_contact(self, name: str, email: str, phone: str = ""):
        """
        Add a new contact.
        Optimized: Directly updates state without re-fetching.
        """
        try:
            # Call core business logic
            new_contact = self._manager.create_contact(name, email, phone)
            
            # Optimized: Add to local state without re-fetching
            new_contact_dict = contact_to_dict(new_contact)
            self._contacts.append(new_contact_dict)
            
            # Emit signal to update view
            self.contacts_changed.emit(self._contacts)
        except Exception as e:
            self.error_occurred.emit(f"Failed to add contact: {str(e)}")
    
    def delete_contact(self, contact_id: str):
        """
        Delete a contact by ID.
        Optimized: Directly updates state without re-fetching.
        """
        try:
            # Call core business logic
            self._manager.delete_contact(contact_id)
            
            # Optimized: Remove from local state without re-fetching
            self._contacts = [c for c in self._contacts if c['id'] != contact_id]
            
            # Emit signal to update view
            self.contacts_changed.emit(self._contacts)
        except Exception as e:
            self.error_occurred.emit(f"Failed to delete contact: {str(e)}")
