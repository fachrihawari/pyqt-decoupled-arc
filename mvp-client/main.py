"""
Main entry point for MVP (Model-View-Presenter) client.

MVP Pattern:
- Model: Business logic (Core module - UI-agnostic)
- View: Passive UI that only displays data (implements View contract)
- Presenter: Mediator that handles ALL logic (implements Presenter contract)

Key Difference from MVVM:
- MVVM: View observes ViewModel (pull model)
- MVP: Presenter pushes data to View (push model)
- MVP: View is more passive (dumber)
- MVP: Easier to unit test (View is just an interface)
"""
import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import QApplication

from core.application.contact_manager import ContactManager
from presenter import ContactListPresenter
from view import ContactListView


def main():
    """
    Initialize MVP architecture and run the application.
    
    MVP Flow:
    1. Create Model (Core business logic)
    2. Create Presenter (with Model dependency)
    3. Create View (with Presenter dependency)
    4. View attaches itself to Presenter
    5. Presenter loads initial data and tells View to display it
    """
    # Qt Application
    app = QApplication(sys.argv)
    
    # Model: Core business logic (UI-agnostic)
    contact_manager = ContactManager.create()
    contact_manager.seed_data()
    
    # Presenter: Handles all logic
    presenter = ContactListPresenter(contact_manager)
    
    # View: Passive UI (implements View contract)
    view = ContactListView(presenter)
    view.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
