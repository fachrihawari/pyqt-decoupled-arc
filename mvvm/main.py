"""
Main entry point for the imperative PyQt6 client with MVVM architecture.

Architecture:
- Model: Core business logic (completely separated, UI-agnostic)
- View: Pure UI components (views/)
- ViewModel: Presentation logic and state management (viewmodels/)

The core module is completely decoupled and can be used by any client.
"""
import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import QApplication
from core.application.contact_manager import ContactManager
from viewmodels.contact_list_viewmodel import ContactListViewModel
from views.contact_list_view import ContactListView


def main():
    """
    Application entry point.
    Sets up MVVM architecture with clean separation.
    """
    # Initialize Qt Application
    app = QApplication(sys.argv)
    
    # Model Layer: Initialize core business logic (UI-agnostic)
    contact_manager = ContactManager.create()
    contact_manager.seed_data()  # Add some initial data
    
    # ViewModel Layer: Create presentation logic layer
    viewmodel = ContactListViewModel(contact_manager)
    
    # View Layer: Create UI component
    view = ContactListView(viewmodel)
    view.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
