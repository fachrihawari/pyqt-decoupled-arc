"""
View for Contact List
Pure UI component that displays contacts and handles user interactions.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QTableWidget, QTableWidgetItem, QPushButton,
                              QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt


class ContactListView(QWidget):
    """
    View component for displaying and managing contacts.
    Follows MVVM pattern - only handles UI rendering and user interactions.
    """
    
    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        
        # Connect ViewModel signals to View slots
        self.viewmodel.contacts_changed.connect(self._on_contacts_changed)
        self.viewmodel.error_occurred.connect(self._on_error)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Contact Management - MVVM")
        self.setGeometry(100, 100, 800, 500)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Contact Management (MVVM Pattern)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        # Table
        self.table = self._create_table()
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = self._create_buttons()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _create_table(self):
        """Create and configure the contacts table."""
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "Actions"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        return table
    
    def _create_buttons(self):
        """Create action buttons."""
        layout = QHBoxLayout()
        
        # Add Random Contact button
        add_btn = QPushButton("➕ Add Random Contact")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_btn.clicked.connect(self._on_add_random_clicked)
        layout.addWidget(add_btn)
        
        # Add Custom Contact button
        add_custom_btn = QPushButton("📝 Add Custom Contact")
        add_custom_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        add_custom_btn.clicked.connect(self._on_add_custom_clicked)
        layout.addWidget(add_custom_btn)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        refresh_btn.clicked.connect(self._on_refresh_clicked)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        return layout
    
    def _on_contacts_changed(self, contacts):
        """Update the table when contacts change (triggered by ViewModel signal)."""
        self.table.setRowCount(len(contacts))
        
        for row, contact in enumerate(contacts):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(contact['id'][:8] + '...'))
            
            # Name
            self.table.setItem(row, 1, QTableWidgetItem(contact['name']))
            
            # Email
            self.table.setItem(row, 2, QTableWidgetItem(contact['email']))
            
            # Phone
            self.table.setItem(row, 3, QTableWidgetItem(contact['phone']))
            
            # Delete button in the Actions column
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            delete_btn.clicked.connect(
                lambda checked, cid=contact['id']: self._on_delete_clicked(cid)
            )
            self.table.setCellWidget(row, 4, delete_btn)
    
    def _on_add_random_clicked(self):
        """Handle add random contact button click."""
        import random
        import string
        
        name = ''.join(random.choices(string.ascii_uppercase, k=5))
        email = f"{name.lower()}@example.com"
        phone = f"+1-555-{random.randint(1000, 9999)}"
        
        # Call ViewModel method (separation of concerns)
        self.viewmodel.add_contact(name, email, phone)
    
    def _on_add_custom_clicked(self):
        """Handle add custom contact button click."""
        # Import here to avoid circular dependencies
        from PyQt6.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Contact")
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        name_input = QLineEdit()
        email_input = QLineEdit()
        phone_input = QLineEdit()
        
        layout.addRow("Name:", name_input)
        layout.addRow("Email:", email_input)
        layout.addRow("Phone:", phone_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = name_input.text().strip()
            email = email_input.text().strip()
            phone = phone_input.text().strip()
            
            if name and email:
                self.viewmodel.add_contact(name, email, phone)
            else:
                QMessageBox.warning(self, "Invalid Input", "Name and Email are required!")
    
    def _on_delete_clicked(self, contact_id):
        """Handle delete contact button click."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this contact?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.viewmodel.delete_contact(contact_id)
    
    def _on_refresh_clicked(self):
        """Handle refresh button click."""
        self.viewmodel.refresh_contacts()
    
    def _on_error(self, error_message):
        """Handle error from ViewModel."""
        QMessageBox.critical(self, "Error", error_message)
