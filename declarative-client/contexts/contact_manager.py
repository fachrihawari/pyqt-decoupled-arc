"""
Global ContactManager context for sharing across components.
This provides a singleton ContactManager instance accessible from any component.
"""
import sys
sys.path.insert(0, '../')

from edifice import use_state, use_effect
from core.application.contact_manager import ContactManager
from core.domain.events import CONTACT_CREATED, CONTACT_DELETED
from core.serializers import contact_to_dict, contacts_to_dict_list

# Global singleton instance
_manager_instance = None

def get_contact_manager():
    """Get or create the global ContactManager singleton."""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = ContactManager.create()
        _manager_instance.seed_data()  # Optional: Add initial data
    return _manager_instance


def use_contact_manager():
    """
    Hook to access the ContactManager and contacts state from any component.
    
    Returns:
        tuple: (manager, contacts, set_contacts)
    """
    manager = get_contact_manager()
    contacts, set_contacts = use_state([])
    
    def init_contacts():
        # Load initial contacts
        all_contacts = manager.get_all_contacts()
        set_contacts(contacts_to_dict_list(all_contacts))
        
        # Subscribe to domain events for reactive updates
        def on_contact_created(payload):
            new_contact = payload['contact']
            set_contacts(lambda current: current + [contact_to_dict(new_contact)])
        
        def on_contact_deleted(payload):
            deleted_id = payload['id']
            set_contacts(lambda current: [c for c in current if c['id'] != deleted_id])
        
        unsubscribe_created = manager.subscribe_to_events(CONTACT_CREATED, on_contact_created)
        unsubscribe_deleted = manager.subscribe_to_events(CONTACT_DELETED, on_contact_deleted)
        
        # Cleanup function
        def cleanup():
            unsubscribe_created()
            unsubscribe_deleted()
        
        return cleanup
    
    use_effect(init_contacts, [])
    
    return manager, contacts


def use_contact_manager_only():
    """
    Hook to access only the ContactManager (without contacts state).
    Useful for components that only need to call manager methods.
    
    Returns:
        ContactManager: The global ContactManager instance
    """
    return get_contact_manager()
