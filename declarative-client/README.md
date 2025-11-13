# Contact Manager - Declarative UI + Clean Architecture

A contact management application demonstrating **Edifice's declarative/reactive UI** integrated with **Clean Architecture** principles. This shows how modern React-like patterns can work with domain-driven design without needing traditional MVVM.

## Features

- 📋 **Contact List**: View all your contacts in a styled card layout
- ➕ **Add Contact**: Form to add new contacts with name, email, and phone
- 🗑️ **Delete Contact**: Remove contacts with a single click
- 🎨 **Modern UI**: Clean, professional styling with proper spacing and colors
- ⚡ **Reactive**: State-driven UI updates automatically when contacts change
- 🧭 **Navigation**: Simple page routing between list and add views
- 🏗️ **Clean Architecture**: UI decoupled from core business logic
- 📡 **Event-Driven**: Domain events trigger automatic UI updates

## Project Structure

```
declarative-client/
├── main.py                 # App entry point, core integration, routing
├── pages/
│   ├── contact_list.py    # Contact list page component
│   └── contact_add.py     # Add contact form component
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── ARCHITECTURE.md       # Detailed architecture explanation

../core/                   # Shared business logic module
├── application/
│   ├── contact_manager.py  # Application service facade
│   └── use_cases.py        # Business use cases
├── domain/
│   ├── contact.py          # Domain entities
│   └── events.py           # Domain events
├── repository/
│   └── contact_repository.py  # Repository interface
└── event_bus/
    └── event_bus.py        # Pub/sub event system
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

1. Click "➕ Add New Contact" button
2. Fill in the name (required), email (required), and phone number (optional)
3. Click "Save" to add the contact
4. The app navigates back to the contact list automatically
5. Domain event triggers and UI updates reactively

### Viewing Contacts

- The contact list shows all saved contacts in card format
- Each card displays the contact's name, email, and phone number
- If no contacts exist, a helpful message is displayed
- Click "➕ Add New Contact" button at the bottom to add your first contact

### Deleting a Contact

1. Find the contact in the list
2. Click the "🗑️ Delete" button on the contact card
3. Contact is removed via core business logic
4. UI updates automatically through domain events

## Architecture

This app demonstrates **Clean Architecture with Declarative UI** - **NO traditional MVVM needed**! 

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed explanation of why MVVM is unnecessary with Edifice.

### Three-Layer Architecture

1. **Core Layer** (`../core/`)
   - Domain models and business rules
   - Use cases (application logic)
   - Repository pattern for data access
   - Event bus for reactive updates
   - **100% UI-agnostic**

2. **Adapter Layer** (`main.py` functions)
   - Simple functions bridging UI ↔ Core
   - Data transformation (domain models ↔ UI dicts)
   - Event subscription setup
   - **Thin integration layer**

3. **UI Layer** (Edifice components)
   - Declarative components with `@component`
   - State management via `use_state()` hooks
   - Reactive rendering (automatic updates)
   - **Replaces ViewModel functionality**

### Key Concepts

- **No ViewModel Classes**: Edifice components manage state directly with hooks
- **Event-Driven Updates**: Domain events automatically refresh UI
- **One-Way Data Flow**: Props down, events up
- **Separation**: Core can be tested/reused independently
- **Simplicity**: Fewer layers than traditional MVVM

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
