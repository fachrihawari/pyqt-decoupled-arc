import sys
from edifice import App, Window, component, use_state, use_effect
from PyQt6.QtWidgets import QApplication
from pages.contact_list import ContactList
from pages.contact_add import ContactAdd

# Import core business logic
sys.path.insert(0, '../')
from core.application.contact_manager import ContactManager
from core.domain.events import CONTACT_CREATED, CONTACT_DELETED
from core.serializers import contact_to_dict, contacts_to_dict_list

@component
def MyApp(self):
  # route: 'list' or 'add'
  route, set_route = use_state("list")
  contacts, set_contacts = use_state([])
  
  # Initialize ContactManager (singleton pattern for the app lifecycle)
  manager, set_manager = use_state(None)
  
  # Initialize manager on mount
  def init_manager():
    print("ContactManager initialized.")

    contact_manager = ContactManager.create()
    contact_manager.seed_data()  # Optional: Add initial data
    set_manager(contact_manager)

    # Load initial contacts
    all_contacts = contact_manager.get_all_contacts()
    set_contacts(contacts_to_dict_list(all_contacts))
    
    # Subscribe to domain events for reactive updates
    def on_contact_created(payload):
      # Optimized: Add new contact to state without re-fetching
      new_contact = payload['contact']
      set_contacts(lambda current: current + [contact_to_dict(new_contact)])
    
    def on_contact_deleted(payload):
      # Optimized: Remove contact from state without re-fetching
      deleted_id = payload['id']
      set_contacts(lambda current: [c for c in current if c['id'] != deleted_id])
    
    unsubscribe_created = contact_manager.subscribe_to_events(CONTACT_CREATED, on_contact_created)
    unsubscribe_deleted = contact_manager.subscribe_to_events(CONTACT_DELETED, on_contact_deleted)

    def cleanup_handler():
      unsubscribe_created()
      unsubscribe_deleted()

    return cleanup_handler
  
  use_effect(init_manager, [])  # Run once on mount

  def navigate(r):
    set_route(r)

  def add_contact(contact_dict):
    """Adapter: Convert UI dict to domain use case call"""
    if manager:
      try:
        # Call the core business logic
        manager.create_contact(
          name=contact_dict.get('name', ''),
          email=contact_dict.get('email', ''),
          phone=contact_dict.get('phone', '')
        )
        # Events will trigger automatic UI update
      except Exception as e:
        print(f"Error creating contact: {e}")

  def delete_contact(contact_id):
    """Adapter: Delete contact through core"""
    if manager:
      try:
        manager.delete_contact(contact_id)
        # Events will trigger automatic UI update
      except Exception as e:
        print(f"Error deleting contact: {e}")

  with Window(title="Contact Manager"):
    # Render the selected page
    if route == "list":
      ContactList(contacts=contacts, navigate=navigate, on_delete=delete_contact)
    elif route == "add":
      ContactAdd(on_save=add_contact, navigate=navigate)


if __name__ == "__main__":
  app = QApplication(sys.argv)

  App(
    root_element=MyApp(),
    create_application=False,
    qapplication=app,
  ).start()