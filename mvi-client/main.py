"""
Main entry point for MVI (Model-View-Intent) client.

MVI Pattern:
- Model: Immutable application state
- View: Pure UI that renders state and emits intents
- Intent: User actions that trigger state changes

Flow:
User Action → Intent → Reducer → New State → View Updates
"""
import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import QApplication

from core.application.contact_manager import ContactManager
from state import ContactState
from reducer import ContactReducer
from store import ContactStore
from view import ContactView


def main():
    """
    Initialize MVI architecture and run the application.
    """
    # Qt Application
    app = QApplication(sys.argv)
    
    # Model Layer: Core business logic (UI-agnostic)
    contact_manager = ContactManager.create()
    contact_manager.seed_data()
    
    # MVI Setup
    initial_state = ContactState()
    reducer = ContactReducer(contact_manager)
    store = ContactStore(reducer, initial_state)
    
    # View: Subscribe to store and render based on state
    view = ContactView(store)
    view.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
