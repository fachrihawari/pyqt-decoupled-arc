"""
View for Contact List in MVP pattern.

The View:
- Is PASSIVE (dumb) - only displays data
- Delegates ALL logic to Presenter
- Implements the View interface from contracts
- Handles UI events but immediately delegates to Presenter
"""
import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem, 
    QMessageBox, QDialog, QLabel, QLineEdit, QFormLayout,
    QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from typing import List

from contracts import ContactListContract


class ContactListView(QMainWindow, ContactListContract.View):
    """
    Passive View that implements the View contract.
    
    MVP Principles:
    1. View is DUMB - no business logic
    2. View delegates ALL user actions to Presenter
    3. Presenter tells View what to display
    4. View and Presenter communicate through interface (contract)
    """
    
    def __init__(self, presenter: ContactListContract.Presenter):
        super().__init__()
        self._presenter = presenter
        self._add_dialog = None
        
        # Setup UI
        self._init_ui()
        
        # Attach View to Presenter
        self._presenter.attach_view(self)
    
    def _init_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle("Contact Manager - MVP Pattern")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Contact Manager (MVP)")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("➕ Add Contact")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_button.clicked.connect(self._on_add_clicked)
        
        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.refresh_button.clicked.connect(self._on_refresh_clicked)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Email", "Phone", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
        """)
        
        layout.addWidget(self.table)
    
    # ===== View Interface Implementation =====
    # These methods are called by the Presenter
    
    def show_contacts(self, contacts: List[dict]):
        """Display contacts in table - called by Presenter."""
        self.table.setRowCount(0)
        
        for contact in contacts:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Name
            self.table.setItem(row, 0, QTableWidgetItem(contact['name']))
            
            # Email
            self.table.setItem(row, 1, QTableWidgetItem(contact['email']))
            
            # Phone
            self.table.setItem(row, 2, QTableWidgetItem(contact.get('phone', '')))
            
            # Delete button
            delete_button = QPushButton("🗑️ Delete")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    padding: 5px 15px;
                    border: none;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            # Delegate to Presenter when clicked
            delete_button.clicked.connect(
                lambda checked, cid=contact['id']: self._on_delete_clicked(cid)
            )
            self.table.setCellWidget(row, 3, delete_button)
    
    def show_error(self, message: str):
        """Show error message - called by Presenter."""
        QMessageBox.critical(self, "Error", message)
    
    def show_loading(self):
        """Show loading state - called by Presenter."""
        self.setEnabled(False)
        self.setWindowTitle("Contact Manager - MVP Pattern (Loading...)")
    
    def hide_loading(self):
        """Hide loading state - called by Presenter."""
        self.setEnabled(True)
        self.setWindowTitle("Contact Manager - MVP Pattern")
    
    def show_success_message(self, message: str):
        """Show success message - called by Presenter."""
        QMessageBox.information(self, "Success", message)
    
    def close_add_dialog(self):
        """Close add dialog - called by Presenter."""
        if self._add_dialog:
            self._add_dialog.close()
    
    def clear_add_dialog_form(self):
        """Clear form fields - called by Presenter."""
        if self._add_dialog:
            self._add_dialog.name_input.clear()
            self._add_dialog.email_input.clear()
            self._add_dialog.phone_input.clear()
    
    # ===== UI Event Handlers =====
    # These capture user actions and delegate to Presenter
    
    def _on_add_clicked(self):
        """User clicked Add button - delegate to Presenter."""
        self._presenter.on_add_contact_clicked()
        # View handles showing dialog (UI concern)
        self._show_add_dialog()
    
    def _on_delete_clicked(self, contact_id: str):
        """User clicked Delete button - delegate to Presenter."""
        # View handles confirmation dialog (UI concern)
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this contact?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Delegate actual deletion to Presenter
            self._presenter.on_delete_contact_clicked(contact_id)
    
    def _on_refresh_clicked(self):
        """User clicked Refresh button - delegate to Presenter."""
        self._presenter.on_refresh_clicked()
    
    def _show_add_dialog(self):
        """Show add contact dialog - UI concern."""
        self._add_dialog = AddContactDialog(self, self._presenter)
        self._add_dialog.exec()
    
    def closeEvent(self, event):
        """Cleanup when window closes."""
        self._presenter.detach_view()
        event.accept()


class AddContactDialog(QDialog):
    """Dialog for adding a new contact."""
    
    def __init__(self, parent, presenter: ContactListContract.Presenter):
        super().__init__(parent)
        self._presenter = presenter
        
        self.setWindowTitle("Add Contact")
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        # Layout
        layout = QFormLayout(self)
        
        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone (optional)")
        
        layout.addRow("Name:", self.name_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Phone:", self.phone_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("💾 Save")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
            }
        """)
        save_button.clicked.connect(self._on_save_clicked)
        
        cancel_button = QPushButton("❌ Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
            }
        """)
        cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addRow(button_layout)
    
    def _on_save_clicked(self):
        """User clicked Save - delegate to Presenter."""
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        
        # Delegate ALL logic to Presenter
        self._presenter.on_save_contact_clicked(name, email, phone)
