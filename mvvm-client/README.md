# Contact Manager - PyQt6 + Edifice

A simple contact management application built with PyQt6 and the Edifice framework, demonstrating reactive UI patterns with a clean, modern design.

## Features

- 📋 **Contact List**: View all your contacts in a styled card layout
- ➕ **Add Contact**: Form to add new contacts with name and phone
- 🎨 **Modern UI**: Clean, professional styling with proper spacing and colors
- ⚡ **Reactive**: State-driven UI updates automatically when contacts change
- 🧭 **Navigation**: Simple page routing between list and add views

## Project Structure

```
mvvm-client/
├── main.py                 # App entry point, routing, and state management
├── pages/
│   ├── contact_list.py    # Contact list page component
│   └── contact_add.py     # Add contact form component
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Requirements

- Python 3.8+
- PyQt6 6.5.2
- pyedifice 4.4.1

## Installation

1. **Create and activate a virtual environment** (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The application window will open with:
- A navigation bar at the top with two buttons
- The Contact List page (default view)
- Click "Add Contact" to add new contacts
- Click "Contact List" to return to the list view

## Usage

### Adding a Contact

1. Click "➕ Add Contact" in the navigation bar
2. Fill in the name (required) and phone number (optional)
3. Click "💾 Save Contact" to add the contact
4. The app will navigate back to the contact list automatically

### Viewing Contacts

- The contact list shows all saved contacts in card format
- Each card displays the contact's name and phone number
- If no contacts exist, a helpful message is displayed
- Click the green "➕ Add New Contact" button at the bottom to add your first contact

## Architecture

This app demonstrates the MVVM (Model-View-ViewModel) pattern using Edifice:

- **Model**: Simple dictionary-based contact data
- **View**: Declarative UI components in `pages/`
- **ViewModel**: State management and navigation logic in `main.py`

### Key Concepts

- **Components**: Reusable UI components decorated with `@component`
- **State Management**: Using `use_state()` hooks for reactive state
- **Declarative UI**: Context managers (`with VBoxView():`) for layout
- **Props**: Passing data and callbacks between components

## Styling

The app uses:
- Qt stylesheets for global theming (applied in `main.py`)
- Inline styles for component-specific customization
- HTML formatting in Labels for rich text (headings, colors, icons)

## Development

To modify the UI:
1. Edit components in `pages/contact_list.py` or `pages/contact_add.py`
2. Changes to state management go in `main.py`
3. The app will reflect changes on next run (no hot reload)

## License

This is a sample project for demonstration purposes.
