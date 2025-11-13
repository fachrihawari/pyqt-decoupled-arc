import sys
sys.path.insert(0, '../')

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from PyQt6.QtCore import Qt
import random
import string

# Import core logic
from core.application.contact_manager import ContactManager, CONTACT_CREATED

class ContactApp(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = ContactManager.create()  # No events for simplicity

        # Seed initial data
        self.manager.seed_data()

        self.table = None  # Store reference to the table

        self.render()

    def _render_title(self):
        title = QLabel("Contact Management")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        return title
    
    def _render_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        return table
    
    def _render_row(self, contact):
        # Set Row Count to accommodate new row if necessary
        next_row = self.table.rowCount()
        print(f"Adding row {next_row} for contact {contact}")
        self.table.setRowCount(next_row + 1)

        # Set items in the row
        self.table.setItem(next_row, 0, QTableWidgetItem(str(contact.id)))
        self.table.setItem(next_row, 1, QTableWidgetItem(contact.name))
        self.table.setItem(next_row, 2, QTableWidgetItem(contact.email))
        self.table.setItem(next_row, 3, QTableWidgetItem(contact.phone))

    def _render_add_button(self):
        def add_random_contact():
            name = ''.join(random.choices(string.ascii_uppercase, k=5))
            email = f"{name.lower()}@example.com"
            phone = f"+1-555-{random.randint(1000,9999)}"
            self.manager.create_contact(name, email, phone)

        button = QPushButton("Add Random Contact")
        button.clicked.connect(add_random_contact)

        return button

    def render(self):
        
        # Window settings
        self.setWindowTitle("Contact Management")
        self.setGeometry(100, 100, 600, 400)

        # Layout setup
        layout = QVBoxLayout()

        # Render title
        title = self._render_title()
        layout.addWidget(title)

        # Render table
        self.table = self._render_table()
        layout.addWidget(self.table)

        # Initial data population
        for contact in self.manager.get_all_contacts():
            self._render_row(contact)

        # Render add random contact button
        add_button = self._render_add_button()
        layout.addWidget(add_button)

        # Set main layout
        self.setLayout(layout)

        self.manager.subscribe_to_events(CONTACT_CREATED, self._render_row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactApp()
    window.show()
    sys.exit(app.exec())