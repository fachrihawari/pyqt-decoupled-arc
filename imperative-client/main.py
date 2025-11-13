import sys
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

    def _refresh_table(self):
        """Refresh the existing table with updated contacts."""
        contacts = self.manager.get_all_contacts()
        self.table.setRowCount(len(contacts))
        for row, contact in enumerate(contacts):
            self.table.setItem(row, 0, QTableWidgetItem(contact.id))
            self.table.setItem(row, 1, QTableWidgetItem(contact.name))
            self.table.setItem(row, 2, QTableWidgetItem(contact.email))
            self.table.setItem(row, 3, QTableWidgetItem(contact.phone))

    def _render_add_button(self):
        def add_random_contact():
            name = ''.join(random.choices(string.ascii_uppercase, k=5))
            email = f"{name.lower()}@example.com"
            phone = f"+1-555-{random.randint(1000,9999)}"
            self.manager.create_contact(name, email, phone)
            # add_layout = QVBoxLayout()
            # add_layout.addWidget(QLabel("Add Random Contact Clicked"))
            # self.setLayout(add_layout)

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
        self._refresh_table()  # Initial population of the table

        # Render add random contact button
        add_button = self._render_add_button()
        layout.addWidget(add_button)

        # Set main layout
        self.setLayout(layout)


        # Set listeners for data changes
        self.manager.subscribe_to_events(CONTACT_CREATED, lambda data: self._refresh_table())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactApp()
    window.show()
    sys.exit(app.exec())