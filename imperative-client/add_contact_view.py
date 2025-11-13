"""
Add Contact View for Imperative Pattern.

A simple dialog for adding new contacts with form validation.
"""
import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt

class AddContactView(QDialog):
    """
    Dialog view for adding a new contact.
    
    Imperative Pattern:
    - Direct form handling
    - Simple validation
    - Callback-based communication with parent
    """
    
    def __init__(self, parent=None, manager=None):
        super().__init__(parent)
        
        self.manager = manager
        self.on_contact_added = None  # Callback function

        self._ready = False
        
        # Setup UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the dialog UI."""
        self.setWindowTitle("Add New Contact")
        self.setModal(True)
        self.setFixedSize(450, 250)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Add New Contact")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            margin: 10px;
            color: #333;
        """)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter contact name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                
                height: 30px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addRow("Name:", self.name_input)
        
        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setStyleSheet("""
            QLineEdit {
                
                height: 30px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addRow("Email:", self.email_input)
        
        # Phone input
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setStyleSheet("""
            QLineEdit {
                
                height: 30px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addRow("Phone:", self.phone_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = self._create_buttons()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set focus to name input
        self.name_input.setFocus()
    
    def _create_buttons(self):
        """Create action buttons."""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # Cancel button
        cancel_button = QPushButton("❌ Cancel")
        cancel_button.setFixedSize(120, 40)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        cancel_button.clicked.connect(self._on_cancel_clicked)
        layout.addWidget(cancel_button)
        
        # Save button
        save_button = QPushButton("💾 Save")
        save_button.setFixedSize(120, 40)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
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
        save_button.clicked.connect(self._on_save_clicked)
        layout.addWidget(save_button)
        
        return layout
    
    def _validate_inputs(self):
        """
        Validate form inputs.
        Returns (is_valid, error_message)
        """
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        
        # Validate name
        if not name:
            return False, "Name is required"
        
        if len(name) < 2:
            return False, "Name must be at least 2 characters"
        
        # Validate email
        if not email:
            return False, "Email is required"
        
        if '@' not in email or '.' not in email:
            return False, "Please enter a valid email address"
        
        # Phone is optional but validate if provided
        if phone and len(phone) < 5:
            return False, "Phone number must be at least 5 characters"
        
        return True, None
    
    def _on_save_clicked(self):
        """Handle save button click with validation."""
        # Validate inputs
        is_valid, error_message = self._validate_inputs()
        
        if not is_valid:
            # Use contract method
            self.show_error(f"Validation Error: {error_message}")
            return
        
        # Get form data using contract method
        form_data = self.get_form_data()
        name = form_data['name']
        email = form_data['email']
        phone = form_data['phone']
        
        # Create contact through manager
        if self.manager:
            try:
                self.manager.create_contact(name, email, phone)
                
                # Use contract method
                self.show_success(f"Contact '{name}' has been added successfully!")
                
                # Call callback if provided
                if self.on_contact_added:
                    self.on_contact_added()
                
                # Use contract method
                self.close()
                
            except Exception as e:
                # Use contract method
                self.show_error(f"Failed to add contact: {str(e)}")
        else:
            # Use contract method
            self.show_error("No contact manager available")
    
    def _on_cancel_clicked(self):
        """Handle cancel button click."""
        # Clear form
        self._clear_form()
        
        # Close dialog
        self.reject()
    
    def _clear_form(self):
        """Clear all form inputs."""
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
    
    # ===== Contract Implementation =====
    
    def get_form_data(self):
        """Get current form data as a dictionary (Contract method)."""
        return {
            'name': self.name_input.text().strip(),
            'email': self.email_input.text().strip(),
            'phone': self.phone_input.text().strip()
        }
    
    def show_error(self, message: str):
        """Show an error message (Contract method)."""
        QMessageBox.critical(
            self,
            "Error",
            message,
            QMessageBox.StandardButton.Ok
        )
    
    def show_success(self, message: str):
        """Show a success message (Contract method)."""
        QMessageBox.information(
            self,
            "Success",
            message,
            QMessageBox.StandardButton.Ok
        )
    
    def close(self):
        """Close the dialog (Contract method)."""
        self.accept()
