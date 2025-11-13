"""
Presenter for Contact List in MVP pattern.

The Presenter:
- Handles ALL business logic and user interactions
- Communicates with Model (Core) to get/manipulate data
- Tells View what to display (View is passive)
- Is UI-agnostic (can be unit tested without UI)
"""
import sys
sys.path.insert(0, '../')

from typing import Optional
from contracts import ContactListContract
from core.application.contact_manager import ContactManager
from core.serializers import contacts_to_dict_list, contact_to_dict


class ContactListPresenter(ContactListContract.Presenter):
    """
    Presenter handles all logic for Contact List feature.
    
    MVP Flow:
    1. View captures user action (e.g., button click)
    2. View calls Presenter method (e.g., on_add_contact_clicked)
    3. Presenter performs business logic with Model
    4. Presenter tells View what to display (e.g., view.show_contacts())
    """
    
    def __init__(self, contact_manager: ContactManager):
        self._manager = contact_manager
        self._view: Optional[ContactListContract.View] = None
        self._contacts = []
    
    def attach_view(self, view: ContactListContract.View):
        """Attach View and load initial data."""
        self._view = view
        self.load_contacts()
    
    def detach_view(self):
        """Detach View (cleanup)."""
        self._view = None
    
    def load_contacts(self):
        """Load contacts from Model and tell View to display them."""
        if not self._view:
            return
        
        try:
            # Show loading state
            self._view.show_loading()
            
            # Get data from Model (Core)
            domain_contacts = self._manager.get_all_contacts()
            self._contacts = contacts_to_dict_list(domain_contacts)
            
            # Tell View to display data
            self._view.hide_loading()
            self._view.show_contacts(self._contacts)
        except Exception as e:
            self._view.hide_loading()
            self._view.show_error(f"Failed to load contacts: {str(e)}")
    
    def on_add_contact_clicked(self):
        """Handle add contact button - just open dialog (View handles UI)."""
        # In MVP, Presenter doesn't manipulate UI directly
        # View will handle showing the dialog
        pass
    
    def on_delete_contact_clicked(self, contact_id: str):
        """Handle delete contact."""
        if not self._view:
            return
        
        try:
            # Perform business logic with Model
            self._manager.delete_contact(contact_id)
            
            # Update local cache
            self._contacts = [c for c in self._contacts if c['id'] != contact_id]
            
            # Tell View to update display
            self._view.show_contacts(self._contacts)
            self._view.show_success_message("Contact deleted successfully!")
        except Exception as e:
            self._view.show_error(f"Failed to delete contact: {str(e)}")
    
    def on_save_contact_clicked(self, name: str, email: str, phone: str):
        """Handle save contact from dialog."""
        if not self._view:
            return
        
        # Validation (Presenter's responsibility)
        if not name or not name.strip():
            self._view.show_error("Name is required")
            return
        
        if not email or not email.strip():
            self._view.show_error("Email is required")
            return
        
        if '@' not in email:
            self._view.show_error("Invalid email format")
            return
        
        try:
            # Perform business logic with Model
            new_contact = self._manager.create_contact(
                name=name.strip(),
                email=email.strip(),
                phone=phone.strip()
            )
            
            # Update local cache
            new_contact_dict = contact_to_dict(new_contact)
            self._contacts.append(new_contact_dict)
            
            # Tell View what to do
            self._view.show_contacts(self._contacts)
            self._view.show_success_message(f"Contact '{name}' added successfully!")
            self._view.close_add_dialog()
            self._view.clear_add_dialog_form()
        except Exception as e:
            self._view.show_error(f"Failed to add contact: {str(e)}")
    
    def on_refresh_clicked(self):
        """Handle refresh button."""
        self.load_contacts()
