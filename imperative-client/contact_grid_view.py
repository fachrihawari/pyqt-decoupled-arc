"""
View for Contact Grid in Imperative Pattern.

The View in imperative pattern with grid layout:
- Displays contacts as cards in a grid
- Directly manipulates UI elements
- Uses direct method calls to update state
- Manager subscribes to events and directly updates the view
- Simple and straightforward approach
"""
import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
import random
import string

from core.application.contact_manager import CONTACT_CREATED
from add_contact_view import AddContactView


class ContactCard(QFrame):
    """
    A card widget to display a single contact's information.
    """
    
    def __init__(self, contact, parent=None):
        super().__init__(parent)
        self.contact = contact
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the card UI."""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            ContactCard {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
            }
            ContactCard:hover {
                border: 1px solid #2196F3;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # ID Label
        id_label = QLabel(f"ID: {str(self.contact.id)[:8]}...")
        id_label.setStyleSheet("color: #999; font-size: 11px;")
        id_label.setToolTip(str(self.contact.id))
        layout.addWidget(id_label)
        
        # Name Label
        name_label = QLabel(self.contact.name)
        name_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #333;
        """)
        layout.addWidget(name_label)
        
        # Email Label
        email_label = QLabel(f"📧 {self.contact.email}")
        email_label.setStyleSheet("color: #555; font-size: 13px;")
        email_label.setWordWrap(True)
        layout.addWidget(email_label)
        
        # Phone Label
        phone_label = QLabel(f"📱 {self.contact.phone}")
        phone_label.setStyleSheet("color: #555; font-size: 13px;")
        layout.addWidget(phone_label)
        
        layout.addStretch()
        self.setLayout(layout)


class ContactGridView(QWidget):
    """
    Imperative View that displays contacts in a grid layout.
    
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
      
        # Store reference to the grid layout
        self.grid_layout = None
        self.cards = []  # Store contact cards
        
        # Setup UI
        self._init_ui()
        
        # Subscribe to events - Manager will call our methods directly
        self.manager.subscribe_to_events(CONTACT_CREATED, self._on_contact_created)
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Window settings
        self.setWindowTitle("Contact Management - Grid View (Imperative)")
        self.setGeometry(100, 100, 1000, 600)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = self._create_title()
        layout.addWidget(title)
        
        # Scroll area for grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f5f5;
            }
        """)
        
        # Container widget for grid
        container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        container.setLayout(self.grid_layout)
        
        scroll_area.setWidget(container)
        layout.addWidget(scroll_area)
        
        # Load initial data
        self._load_contacts()
        
        # Buttons
        button_layout = self._create_buttons()
        layout.addLayout(button_layout)
        
        # Set layout
        self.setLayout(layout)
    
    def _create_title(self):
        """Create and style the title label."""
        title = QLabel("Contact Management (Grid View - Imperative)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            margin: 15px;
            color: #333;
        """)
        return title
    
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
        """Load all contacts from manager and populate the grid."""
        contacts = self.manager.get_all_contacts()
        for contact in contacts:
            self.add_contact_card(contact)
    
    # ===== Contract Implementation =====
    
    def add_contact_card(self, contact):
        """
        Add a single contact card to the grid (Contract method).
        This is direct UI manipulation - imperative style.
        """
        # Create contact card
        card = ContactCard(contact)
        self.cards.append(card)
        
        # Calculate position in grid (3 columns)
        num_cards = len(self.cards)
        row = (num_cards - 1) // 3
        col = (num_cards - 1) % 3
        
        # Add to grid
        self.grid_layout.addWidget(card, row, col)
    
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
        
        # Use contract method to add card
        self.add_contact_card(contact)