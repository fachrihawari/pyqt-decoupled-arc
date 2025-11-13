"""
Example: How to use the global ContactManager in any component.

This demonstrates three patterns:
1. Using the full hook with contacts state (use_contact_manager)
2. Using only the manager (use_contact_manager_only)
3. Accessing the manager in child components
"""
from edifice import component, View, Label, Button
from contexts.contact_manager import use_contact_manager, use_contact_manager_only


@component
def ContactStats(self):
    """
    Example component that uses the global manager to show statistics.
    This component can be placed anywhere in your app tree.
    """
    # Option 1: Get manager + contacts state (if you need to display contacts)
    manager, contacts, _ = use_contact_manager()
    
    total_contacts = len(contacts)
    
    with View():
        Label(f"Total Contacts: {total_contacts}")


@component
def QuickAddButton(self):
    """
    Example component that only needs the manager to perform actions.
    No need for contacts state here.
    """
    # Option 2: Get only the manager (lighter, no state subscription)
    manager = use_contact_manager_only()
    
    def add_test_contact():
        manager.create_contact(
            name="Test User",
            email=f"test{len(manager.get_all_contacts())}@example.com",
            phone="+1-555-9999"
        )
    
    with View():
        Button("Quick Add Test Contact", on_click=add_test_contact)


@component
def ContactActionsPanel(self, contact_id: str):
    """
    Example of a child component that can access the manager.
    """
    manager = use_contact_manager_only()
    
    def delete_this_contact():
        manager.delete_contact(contact_id)
    
    with View():
        Button("Delete", on_click=delete_this_contact)
        # You can add more actions here: edit, archive, etc.


# Usage example in your app:
# @component
# def SomePage(self):
#     with View():
#         ContactStats()  # Shows total contacts
#         QuickAddButton()  # Adds contacts without props drilling
#         # ... rest of your page
