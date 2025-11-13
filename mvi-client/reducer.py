"""
Reducer - Pure function that transforms state based on intents.
This is the heart of MVI - predictable state transitions.
"""
import sys
sys.path.insert(0, '../')

from state import ContactState, ViewState, LoadingState
from intent import (
    Intent, LoadContacts, AddContact, DeleteContact, 
    RefreshContacts, NavigateToAdd, NavigateToList
)
from core.application.contact_manager import ContactManager
from core.serializers import contacts_to_dict_list, contact_to_dict


class ContactReducer:
    """
    Pure reducer that takes current state + intent and produces new state.
    
    Principles:
    1. Pure function (no side effects)
    2. Synchronous (side effects handled separately)
    3. Predictable (same input = same output)
    4. Testable (easy to unit test)
    """
    
    def __init__(self, contact_manager: ContactManager):
        self._manager = contact_manager
    
    def reduce(self, state: ContactState, intent: Intent) -> ContactState:
        """
        Main reducer function.
        Takes current state and intent, returns new state.
        """
        # Navigation intents
        if isinstance(intent, NavigateToList):
            return state.copy_with(
                current_view=ViewState.LIST,
                form_name="",
                form_email="",
                form_phone=""
            )
        
        elif isinstance(intent, NavigateToAdd):
            return state.copy_with(current_view=ViewState.ADD)
        
        # Data intents
        elif isinstance(intent, LoadContacts):
            return self._load_contacts(state)
        
        elif isinstance(intent, RefreshContacts):
            return self._load_contacts(state)
        
        elif isinstance(intent, AddContact):
            return self._add_contact(state, intent)
        
        elif isinstance(intent, DeleteContact):
            return self._delete_contact(state, intent)
        
        # Unknown intent - return unchanged state
        return state
    
    def _load_contacts(self, state: ContactState) -> ContactState:
        """Load contacts from core."""
        try:
            domain_contacts = self._manager.get_all_contacts()
            contacts = contacts_to_dict_list(domain_contacts)
            return state.copy_with(
                contacts=contacts,
                loading_state=LoadingState.SUCCESS,
                error_message=None
            )
        except Exception as e:
            return state.copy_with(
                loading_state=LoadingState.ERROR,
                error_message=f"Failed to load contacts: {str(e)}"
            )
    
    def _add_contact(self, state: ContactState, intent: AddContact) -> ContactState:
        """Add a new contact."""
        try:
            # Call core business logic
            new_contact = self._manager.create_contact(
                name=intent.name,
                email=intent.email,
                phone=intent.phone
            )
            
            # Create new state with updated contacts list
            new_contact_dict = contact_to_dict(new_contact)
            updated_contacts = state.contacts + [new_contact_dict]
            
            return state.copy_with(
                contacts=updated_contacts,
                current_view=ViewState.LIST,
                loading_state=LoadingState.SUCCESS,
                error_message=None,
                # Clear form
                form_name="",
                form_email="",
                form_phone=""
            )
        except Exception as e:
            return state.copy_with(
                loading_state=LoadingState.ERROR,
                error_message=f"Failed to add contact: {str(e)}"
            )
    
    def _delete_contact(self, state: ContactState, intent: DeleteContact) -> ContactState:
        """Delete a contact."""
        try:
            # Call core business logic
            self._manager.delete_contact(intent.contact_id)
            
            # Create new state with contact removed
            updated_contacts = [
                c for c in state.contacts 
                if c['id'] != intent.contact_id
            ]
            
            return state.copy_with(
                contacts=updated_contacts,
                loading_state=LoadingState.SUCCESS,
                error_message=None
            )
        except Exception as e:
            return state.copy_with(
                loading_state=LoadingState.ERROR,
                error_message=f"Failed to delete contact: {str(e)}"
            )
