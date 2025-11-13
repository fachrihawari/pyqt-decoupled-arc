"""
View for Contact List in Imperative Pattern.

The View in imperative pattern:
- Directly manipulates UI elements
- Uses direct method calls to update state
- Manager subscribes to events and directly updates the view
- Simple and straightforward approach
"""
import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QPushButton
)
from PyQt6.QtCore import Qt
import random
import string

from core.application.contact_manager import CONTACT_CREATED
from add_contact_view import AddContactView


class ContactListView(QWidget):
    """
    Imperative View that directly manipulates UI elements.
    
    Imperative Pattern Characteristics:
    1. Direct UI manipulation
    2. Manager subscribes to events and calls view methods directly
    3. Simple callbacks for user actions
    4. No complex state management or indirection
    """
    
    def __init__(self, manager):
        super().__init__()
        
        # Use provided manager or create a new one (dependency injection)
        self.manager = manager
      
        # Store reference to the table
        self.table = None
        
        # Setup UI
        self._init_ui()
        
        # Subscribe to events - Manager will call our methods directly
        self.manager.subscribe_to_events(CONTACT_CREATED, self._on_contact_created)
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Window settings
        self.setWindowTitle("Contact Management - Imperative Pattern")
        self.setGeometry(100, 100, 800, 500)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = self._create_title()
        layout.addWidget(title)
        
        # Table
        self.table = self._create_table()
        layout.addWidget(self.table)
        
        # Load initial data
        self._load_contacts()
        
        # Buttons
        button_layout = self._create_buttons()
        layout.addLayout(button_layout)
        
        # Set layout
        self.setLayout(layout)
    
    def _create_title(self):
        """Create and style the title label."""
        title = QLabel("Contact Management (Imperative)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            margin: 15px;
            color: #333;
        """)
        return title
    
    def _create_table(self):
        """Create and configure the contacts table."""
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 8px;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        return table
    
    def _create_buttons(self):
        """Create action buttons."""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Add Contact button
        add_contact_button = QPushButton("➕ Add Contact")
        add_contact_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        add_contact_button.clicked.connect(self._on_add_contact_clicked)
        layout.addWidget(add_contact_button)
        
        # Add Random Contact button
        add_random_button = QPushButton("🎲 Add Random Contact")
        add_random_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6bc2;
            }
        """)
        add_random_button.clicked.connect(self._on_add_random_clicked)
        layout.addWidget(add_random_button)
        
        layout.addStretch()
        return layout
    
    def _load_contacts(self):
        """Load all contacts from manager and populate the table."""
        contacts = self.manager.get_all_contacts()
        for contact in contacts:
            self.add_contact_row(contact)
    
    # ===== Contract Implementation =====
    
    def add_contact_row(self, contact):
        """
        Add a single contact row to the table (Contract method).
        This is direct UI manipulation - imperative style.
        """
        # Get next row position
        row_position = self.table.rowCount()
        self.table.setRowCount(row_position + 1)
        
        # Create and set items
        id_item = QTableWidgetItem(str(contact.id)[:8])
        id_item.setToolTip(str(contact.id))  # Show full ID on hover
        
        name_item = QTableWidgetItem(contact.name)
        email_item = QTableWidgetItem(contact.email)
        phone_item = QTableWidgetItem(contact.phone)
        
        # Set items in the table
        self.table.setItem(row_position, 0, id_item)
        self.table.setItem(row_position, 1, name_item)
        self.table.setItem(row_position, 2, email_item)
        self.table.setItem(row_position, 3, phone_item)
        
        # Optional: Center align ID column
        id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def show_add_contact_dialog(self):
        """Show the add contact dialog (Contract method)."""
        dialog = AddContactView(parent=self, manager=self.manager)
        dialog.exec()
    
    # ===== Private Helper Methods =====
    
    def _on_add_contact_clicked(self):
        """
        Handle add contact button click - opens dialog.
        Direct, imperative approach to handling user actions.
        """
        # Use contract method
        self.show_add_contact_dialog()
    
    def _on_add_random_clicked(self):
        """
        Handle add random contact button click - creates random contact.
        Useful for testing and demonstration.
        """
        # Generate random contact data
        name = ''.join(random.choices(string.ascii_uppercase, k=5))
        email = f"{name.lower()}@example.com"
        phone = f"+1-555-{random.randint(1000, 9999)}"
        
        # Create contact through manager
        # Manager will emit CONTACT_CREATED event
        # Which triggers _on_contact_created callback
        self.manager.create_contact(name, email, phone)
    
    def _on_contact_created(self, contact):
        """
        Event handler called when a contact is created.
        Manager calls this directly via event subscription.
        This is the imperative pattern - direct callback execution.
        """
        print(f"Contact created event received: {contact.name}")
        
        # Use contract method to add row
        self.add_contact_row(contact)
