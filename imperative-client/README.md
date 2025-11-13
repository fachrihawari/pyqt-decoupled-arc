# Imperative Pattern - Contact Manager

This implementation demonstrates the **Imperative Pattern** for building PyQt6 applications.

## Pattern Overview

The imperative pattern is the most straightforward approach to UI programming:

- **Direct UI Manipulation**: Methods directly modify UI elements
- **Simple Event Handling**: Callbacks directly update the view
- **Minimal Abstraction**: No intermediate layers or complex state management
- **Procedural Flow**: Code executes in a clear, step-by-step manner

## Architecture

```
┌─────────────────────────────────────┐
│       ContactListView (Main)        │
│  (Direct UI Manipulation)           │
│                                     │
│  - Displays contact table           │
│  - Subscribes to manager events     │
│  - Directly updates table on events │
│  - Opens AddContactView dialog      │
└──────────┬──────────────────────────┘
           │
           │ Opens dialog
           ▼
┌─────────────────────────────────────┐
│        AddContactView (Dialog)      │
│  (Form Handling & Validation)       │
│                                     │
│  - Collects user input              │
│  - Validates form data              │
│  - Creates contact via manager      │
│  - Shows success/error messages     │
└──────────┬──────────────────────────┘
           │
           │ Direct method calls
           │ Event subscriptions
           ▼
┌─────────────────────────────────────┐
│        ContactManager (Core)        │
│                                     │
│  - Business logic                   │
│  - Emits CONTACT_CREATED events     │
│  - Manages contact data             │
└─────────────────────────────────────┘
```

## Key Characteristics

### 1. Direct UI Updates
```python
def _add_contact_row(self, contact):
    row_position = self.table.rowCount()
    self.table.setRowCount(row_position + 1)
    self.table.setItem(row_position, 0, QTableWidgetItem(str(contact.id)))
    # ... more direct UI manipulation
```

### 2. Dependency Injection Support
```python
def __init__(self, manager):
    # Manager is injected for testability
    self.manager = manager
```

### 3. Event Subscription
```python
self.manager.subscribe_to_events(CONTACT_CREATED, self._on_contact_created)
```

### 4. Simple Callbacks
```python
def _on_contact_created(self, contact):
    # Directly add row to table
    self._add_contact_row(contact)
```

### 5. Separate Dialog Views
```python
def _on_add_contact_clicked(self):
    # Create and show add contact dialog
    dialog = AddContactView(parent=self, manager=self.manager)
    dialog.exec()
```

### 6. Form Validation
```python
def _validate_inputs(self):
    # Direct validation in the dialog
    if not name:
        return False, "Name is required"
    return True, None
```

## Advantages

✅ **Simple and Easy to Understand**: Clear flow from event to UI update  
✅ **Less Code**: No additional abstraction layers (no presenter, no complex viewmodel)  
✅ **Quick Development**: Fast to implement for simple applications  
✅ **Debugging**: Easy to trace execution path  
✅ **Loose Coupling**: View depends only on core business logic through events  
✅ **Event-Driven**: Clean separation via event subscription pattern  
✅ **Efficient Updates**: Incremental updates only modify what changed (better performance than full refresh)  
✅ **Testable**: Supports dependency injection for easy mocking in tests  

## When to Use

Use the imperative pattern for:
- Simple applications with straightforward UI logic
- Prototypes and proof-of-concepts
- Small teams or solo projects
- When rapid development is prioritized over maintainability

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## File Structure

```
imperative-client/
├── main.py                  # Application entry point
├── contracts.py             # View contracts (interfaces)
├── contact_list_view.py     # Main contact list view
├── add_contact_view.py      # Add contact dialog view
├── requirements.txt         # PyQt6 dependencies
└── README.md                # This file
```

## Components

### Contracts (`contracts.py`)
- `ContactListViewContract`: Interface for contact list operations
- `AddContactViewContract`: Interface for add contact dialog operations
- Provides clear API boundaries and enables better testing

### ContactListView (`contact_list_view.py`)
- Implements `ContactListViewContract`
- Main window displaying the contact table
- Subscribes to `CONTACT_CREATED` events
- Incrementally adds rows when contacts are created
- Opens `AddContactView` dialog for adding contacts
- Provides "Add Random Contact" for testing

### AddContactView (`add_contact_view.py`)
- Implements `AddContactViewContract`
- Modal dialog for adding new contacts
- Contains form with name, email, and phone fields
- Validates user input before saving
- Creates contacts through the manager
- Shows success/error messages using contract methods

## Comparison with Other Patterns

| Pattern      | Complexity | Testability | Scalability | Coupling | Learning Curve |
|-------------|-----------|-------------|-------------|----------|----------------|
| Imperative  | Low       | Medium      | Medium      | Low      | Easy           |
| MVP         | Medium    | High        | High        | Very Low | Medium         |
| MVVM        | High      | High        | High        | Low      | Steep          |
| MVI         | High      | Very High   | Very High   | Very Low | Steep          |

**Key Differences:**
- **Imperative vs MVP**: MVP uses formal contracts/interfaces; Imperative is more direct with events
- **Imperative vs MVVM**: Imperative does incremental updates via events; MVVM does full state refresh via signals
- **UI Manipulation**: All patterns use direct PyQt6 API calls - this is not a distinguishing factor
- **Coupling**: All patterns use event-driven architecture with core, so coupling is low across the board
- **Testing**: All patterns support dependency injection for testability

## Example Flows

### Adding a Contact (Form)
1. User clicks "➕ Add Contact" button
2. `_on_add_contact_clicked()` opens `AddContactView` dialog
3. User fills in name, email, and phone fields
4. User clicks "💾 Save" button
5. Dialog validates input fields
6. If valid, `manager.create_contact()` is called
7. Manager emits `CONTACT_CREATED` event
8. `ContactListView._on_contact_created()` callback is triggered
9. `_add_contact_row()` directly adds new row to table
10. Dialog shows success message and closes
11. UI reflects the change immediately

### Adding a Random Contact (Testing)
1. User clicks "🎲 Add Random Contact" button
2. `_on_add_random_clicked()` generates random data
3. `manager.create_contact()` is called directly
4. Manager emits `CONTACT_CREATED` event
5. `_on_contact_created()` callback is triggered
6. `_add_contact_row()` directly updates the table
7. UI reflects the change immediately

This direct, imperative flow makes the pattern easy to understand and implement.
