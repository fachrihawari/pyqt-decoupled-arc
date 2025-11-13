"""
View - UI component that renders based on state and emits intents.
Pure view that only displays state and sends user actions as intents.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QMessageBox,
    QStackedWidget, QLineEdit, QFormLayout
)
from PyQt6.QtCore import Qt

from state import ContactState, ViewState
from intent import (
    LoadContacts, AddContact, DeleteContact, 
    NavigateToAdd, NavigateToList, RefreshContacts
)
from store import ContactStore


class ContactListPage(QWidget):
    """Contact list view - displays contacts and emits intents."""
    
    def __init__(self, store: ContactStore):
        super().__init__()
        self.store = store
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Contact List (MVI Pattern)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Contact")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        add_btn.clicked.connect(lambda: self.store.dispatch(NavigateToAdd()))
        button_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #5a6268; }
        """)
        refresh_btn.clicked.connect(lambda: self.store.dispatch(RefreshContacts()))
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def render(self, state: ContactState):
        """Render the view based on state (pure rendering)."""
        contacts = state.contacts
        self.table.setRowCount(len(contacts))
        
        for row, contact in enumerate(contacts):
            # ID (truncated)
            self.table.setItem(row, 0, QTableWidgetItem(contact['id'][:8] + '...'))
            
            # Name
            self.table.setItem(row, 1, QTableWidgetItem(contact['name']))
            
            # Email
            self.table.setItem(row, 2, QTableWidgetItem(contact['email']))
            
            # Phone
            self.table.setItem(row, 3, QTableWidgetItem(contact['phone']))
            
            # Delete button
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover { background-color: #c82333; }
            """)
            contact_id = contact['id']
            delete_btn.clicked.connect(
                lambda checked, cid=contact_id: self._on_delete_clicked(cid)
            )
            self.table.setCellWidget(row, 4, delete_btn)
    
    def _on_delete_clicked(self, contact_id: str):
        """Handle delete button click - emits intent."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this contact?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.store.dispatch(DeleteContact(contact_id=contact_id))


class ContactAddPage(QWidget):
    """Add contact view - form for adding new contacts."""
    
    def __init__(self, store: ContactStore):
        super().__init__()
        self.store = store
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Add New Contact")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        save_btn.clicked.connect(self._on_save_clicked)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #5a6268; }
        """)
        cancel_btn.clicked.connect(lambda: self.store.dispatch(NavigateToList()))
        button_layout.addWidget(cancel_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def render(self, state: ContactState):
        """Render the view based on state."""
        # Clear form if state says so
        if not state.form_name and not state.form_email:
            self.name_input.clear()
            self.email_input.clear()
            self.phone_input.clear()
    
    def _on_save_clicked(self):
        """Handle save button click - emits intent."""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        
        if not name or not email:
            QMessageBox.warning(self, "Invalid Input", "Name and Email are required!")
            return
        
        # Emit intent to add contact
        self.store.dispatch(AddContact(name=name, email=email, phone=phone))


class ContactView(QWidget):
    """
    Main view container - coordinates between list and add pages.
    Subscribes to store and renders based on state.
    """
    
    def __init__(self, store: ContactStore):
        super().__init__()
        self.store = store
        
        # Subscribe to state changes
        self.store.state_changed.connect(self.render)
        
        # Setup UI
        self._setup_ui()
        
        # Load initial data
        self.store.dispatch(LoadContacts())
    
    def _setup_ui(self):
        """Setup the main UI with stacked pages."""
        self.setWindowTitle("Contact Manager - MVI Pattern")
        self.setGeometry(100, 100, 900, 600)
        
        layout = QVBoxLayout()
        
        # Stacked widget for navigation
        self.stacked_widget = QStackedWidget()
        
        # Create pages
        self.list_page = ContactListPage(self.store)
        self.add_page = ContactAddPage(self.store)
        
        self.stacked_widget.addWidget(self.list_page)  # Index 0
        self.stacked_widget.addWidget(self.add_page)   # Index 1
        
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
    
    def render(self, state: ContactState):
        """
        Main render function - called whenever state changes.
        This is the single source of truth for UI updates.
        """
        # Navigate to correct page
        if state.current_view == ViewState.LIST:
            self.stacked_widget.setCurrentIndex(0)
            self.list_page.render(state)
        elif state.current_view == ViewState.ADD:
            self.stacked_widget.setCurrentIndex(1)
            self.add_page.render(state)
        
        # Show error if present
        if state.error_message:
            QMessageBox.critical(self, "Error", state.error_message)
