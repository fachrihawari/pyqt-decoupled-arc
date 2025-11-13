"""
Main entry point for the Imperative Pattern Contact Manager.

This demonstrates the imperative approach where:
- View directly manipulates UI elements
- Event callbacks trigger direct UI updates
- Simple, straightforward control flow
"""
import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import QApplication
from core.application.contact_manager import ContactManager

# from contact_list_view import ContactListView
from contact_grid_view import ContactGridView


if __name__ == "__main__":
    app = QApplication(sys.argv)

    manager = ContactManager.create()
    manager.seed_data()

    # Create and show the view
    # window = ContactListView(manager)
    window = ContactGridView(manager)
    window.show()
    
    sys.exit(app.exec())