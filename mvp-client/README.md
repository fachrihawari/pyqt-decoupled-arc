# MVP Client - Model-View-Presenter Pattern

This client demonstrates the **MVP (Model-View-Presenter)** pattern with PyQt6, featuring **passive views** and **testable presenters**.

## MVP Pattern Overview

```
┌─────────────────────────────────────────────────────────┐
│                   User Interaction                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    View (Passive)                        │
│  • Captures events (button clicks, etc.)                │
│  • Immediately delegates to Presenter                   │
│  • NO business logic                                    │
│  • Implements View interface (contract)                 │
└────────────────────┬────────────────────────────────────┘
                     │ on_add_clicked()
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  Presenter (Smart)                       │
│  • Handles ALL business logic                           │
│  • Validates input                                      │
│  • Calls Model to get/save data                         │
│  • Tells View what to display                           │
│  • Implements Presenter interface (contract)            │
└────────────────────┬────────────────────────────────────┘
                     │ create_contact()
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    Model (Core)                          │
│  • Business rules and domain logic                      │
│  • Data persistence                                     │
│  • UI-agnostic                                          │
└────────────────────┬────────────────────────────────────┘
                     │ returns Contact
                     ↓
┌─────────────────────────────────────────────────────────┐
│                     Presenter                            │
│  • Transforms domain data to View data                  │
└────────────────────┬────────────────────────────────────┘
                     │ view.show_contacts(contacts)
                     ↓
┌─────────────────────────────────────────────────────────┐
│                View displays data                        │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
mvp-client/
├── main.py          # Entry point
├── contracts.py     # View and Presenter interfaces
├── presenter.py     # Presenter implementation (all logic)
├── view.py          # Passive View implementation (just UI)
└── README.md        # This file

../core/             # Shared business logic (UI-agnostic)
```

## Key Components

### 1. **Contracts** (`contracts.py`)
Defines interfaces for View and Presenter communication.

```python
class ContactListContract:
    class View(ABC):
        @abstractmethod
        def show_contacts(self, contacts: List[dict]):
            """Presenter calls this to tell View to display contacts."""
            pass
        
        @abstractmethod
        def show_error(self, message: str):
            """Presenter calls this to tell View to show error."""
            pass
    
    class Presenter(ABC):
        @abstractmethod
        def on_add_contact_clicked(self):
            """View calls this when user clicks Add button."""
            pass
        
        @abstractmethod
        def on_delete_contact_clicked(self, contact_id: str):
            """View calls this when user clicks Delete."""
            pass
```

**Benefits:**
- ✅ Clear contract between View and Presenter
- ✅ Easy to mock for testing
- ✅ View and Presenter are decoupled
- ✅ Can swap implementations

### 2. **Presenter** (`presenter.py`)
Handles ALL business logic and user interactions.

```python
class ContactListPresenter(ContactListContract.Presenter):
    def on_save_contact_clicked(self, name: str, email: str, phone: str):
        # Validation (Presenter's job)
        if not name:
            self._view.show_error("Name is required")
            return
        
        # Business logic with Model
        new_contact = self._manager.create_contact(name, email, phone)
        
        # Update cache
        self._contacts.append(contact_to_dict(new_contact))
        
        # Tell View what to display (push model)
        self._view.show_contacts(self._contacts)
        self._view.show_success_message("Contact added!")
        self._view.close_add_dialog()
```

**Benefits:**
- ✅ UI-agnostic (no PyQt imports!)
- ✅ Easy to unit test (mock View interface)
- ✅ All logic in one place
- ✅ No data binding needed

### 3. **View** (`view.py`)
Passive UI that only displays data.

```python
class ContactListView(QMainWindow, ContactListContract.View):
    def __init__(self, presenter: ContactListContract.Presenter):
        self._presenter = presenter
        self._presenter.attach_view(self)  # Register with Presenter
    
    # Implement View interface (called by Presenter)
    def show_contacts(self, contacts: List[dict]):
        """Presenter tells us to display contacts."""
        self.table.setRowCount(0)
        for contact in contacts:
            # Just display, no logic!
            ...
    
    # Delegate user actions to Presenter
    def _on_add_clicked(self):
        """User clicked button - delegate to Presenter."""
        self._presenter.on_add_contact_clicked()
        self._show_add_dialog()  # View handles UI concern
```

**Benefits:**
- ✅ Dumb View (easy to understand)
- ✅ No business logic in UI
- ✅ Easy to replace UI framework
- ✅ Clear separation of concerns

## Running the Application

```bash
cd mvp-client
python main.py
```

## MVP vs MVVM vs MVI

| Aspect | MVP | MVVM | MVI |
|--------|-----|------|-----|
| **View Intelligence** | Passive (dumb) | Semi-active | Reactive |
| **Communication** | Push (Presenter → View) | Pull (View observes ViewModel) | Unidirectional |
| **Contracts** | Explicit interfaces | Implicit (signals) | Intents + State |
| **Testing** | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Boilerplate** | Medium | Medium | High |
| **Android/iOS** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Data Binding** | Not needed | Uses signals | Not needed |

## Key MVP Principles

### ✅ **1. View is Passive (Dumb)**
```python
# ❌ BAD: View has logic
def on_save_clicked(self):
    if not self.name_input.text():
        self.show_error("Name required")  # View deciding rules!
        return

# ✅ GOOD: View just delegates
def on_save_clicked(self):
    self._presenter.on_save_contact_clicked(
        self.name_input.text(),
        self.email_input.text(),
        self.phone_input.text()
    )
    # Presenter handles validation and tells us what to do
```

### ✅ **2. Presenter is UI-Agnostic**
```python
# ✅ Presenter has no PyQt imports!
from contracts import ContactListContract  # Abstract interface
from core.application.contact_manager import ContactManager

class ContactListPresenter:
    def __init__(self, contact_manager: ContactManager):
        self._manager = contact_manager  # Only depends on Core
        self._view = None  # View is just an interface
```

### ✅ **3. Communication Through Contracts**
```python
# View → Presenter: Direct method calls
self._presenter.on_delete_contact_clicked(contact_id)

# Presenter → View: Through interface
self._view.show_contacts(contacts)
self._view.show_error(message)

# No signals, no observables, just simple method calls!
```

### ✅ **4. Easy to Test**
```python
def test_add_contact_validation():
    # Mock View
    mock_view = Mock(spec=ContactListContract.View)
    
    # Create Presenter with mock
    presenter = ContactListPresenter(mock_manager)
    presenter.attach_view(mock_view)
    
    # Test invalid input
    presenter.on_save_contact_clicked("", "test@test.com", "")
    
    # Verify Presenter called View.show_error()
    mock_view.show_error.assert_called_once_with("Name is required")

def test_add_contact_success():
    mock_view = Mock(spec=ContactListContract.View)
    presenter = ContactListPresenter(mock_manager)
    presenter.attach_view(mock_view)
    
    # Test valid input
    presenter.on_save_contact_clicked("John", "john@test.com", "123")
    
    # Verify Presenter told View to update
    mock_view.show_contacts.assert_called_once()
    mock_view.show_success_message.assert_called_once()
    mock_view.close_add_dialog.assert_called_once()
```

## MVP vs MVVM: Key Differences

### MVVM (Observer Pattern)
```python
# ViewModel emits signals
class ContactListViewModel(QObject):
    contacts_changed = pyqtSignal(list)
    
    def add_contact(self, ...):
        # ... do work ...
        self.contacts_changed.emit(self._contacts)  # Broadcast

# View observes ViewModel
class ContactListView:
    def __init__(self, viewmodel):
        viewmodel.contacts_changed.connect(self.update_table)  # Pull
```

**MVVM**: View pulls data when notified (observer pattern)

### MVP (Direct Communication)
```python
# Presenter calls View directly
class ContactListPresenter:
    def add_contact(self, ...):
        # ... do work ...
        self._view.show_contacts(self._contacts)  # Push directly

# View implements interface
class ContactListView(ContactListContract.View):
    def show_contacts(self, contacts):
        self.update_table(contacts)  # Direct call
```

**MVP**: Presenter pushes data to View (command pattern)

## When to Use MVP

### ✅ **Use MVP when:**
- Need maximum testability (can test Presenter without UI)
- Want passive, dumb Views (easier to understand)
- Building Android/iOS apps (MVP is popular there)
- Team prefers explicit contracts/interfaces
- Don't need data binding
- Want clear separation of concerns

### ❌ **Don't use MVP when:**
- Need two-way data binding (use MVVM)
- View has complex UI logic (MVP View must be passive)
- Building web apps (use MVI/Redux)
- Team unfamiliar with interfaces/contracts

## MVP for MRI Simulator

MVP is **good** for MRI Simulator because:

### ✅ **1. Testable Logic**
```python
class MRIScanPresenter(ScanContract.Presenter):
    def on_start_scan_clicked(self):
        # Validate parameters (testable without UI!)
        if not self._validate_scan_params():
            self._view.show_error("Invalid scan parameters")
            return
        
        # Start scan
        self._scan_engine.start_scan(self._params)
        
        # Tell View to update
        self._view.show_scanning_state()
        self._view.update_progress(0)
```

### ✅ **2. Complex Validation**
```python
def on_parameter_changed(self, param: str, value: float):
    # Complex validation logic in Presenter (testable!)
    if param == "TE" and value > self._params.TR:
        self._view.show_error("TE cannot exceed TR")
        self._view.reset_parameter(param, self._params.TE)
        return
    
    # Check physical constraints
    if not self._physics_engine.is_valid(param, value):
        self._view.show_warning(f"Parameter {param} may cause artifacts")
```

### ✅ **3. UI-Agnostic Logic**
```python
# Presenter can work with different UIs!
# - PyQt for desktop
# - Kivy for mobile
# - Web frontend
# Just implement the View contract!
```

## Testing Example

```python
import pytest
from unittest.mock import Mock
from presenter import ContactListPresenter
from contracts import ContactListContract

def test_delete_contact_success():
    # Arrange
    mock_manager = Mock()
    mock_view = Mock(spec=ContactListContract.View)
    
    presenter = ContactListPresenter(mock_manager)
    presenter.attach_view(mock_view)
    presenter._contacts = [
        {'id': '1', 'name': 'Test', 'email': 'test@test.com'}
    ]
    
    # Act
    presenter.on_delete_contact_clicked('1')
    
    # Assert
    mock_manager.delete_contact.assert_called_once_with('1')
    mock_view.show_contacts.assert_called_once()
    assert len(presenter._contacts) == 0

def test_add_contact_validation():
    mock_view = Mock(spec=ContactListContract.View)
    presenter = ContactListPresenter(Mock())
    presenter.attach_view(mock_view)
    
    # Test empty name
    presenter.on_save_contact_clicked("", "test@test.com", "")
    mock_view.show_error.assert_called_with("Name is required")
    
    # Test invalid email
    presenter.on_save_contact_clicked("John", "invalid-email", "")
    mock_view.show_error.assert_called_with("Invalid email format")
```

## Comparison Summary

| Pattern | Best For | Testability | Complexity |
|---------|----------|-------------|------------|
| **MVP** | Android/iOS, maximum testability | ⭐⭐⭐⭐⭐ | Medium |
| **MVVM** | Desktop apps, data binding | ⭐⭐⭐⭐ | Medium |
| **MVI** | Complex state, time-travel | ⭐⭐⭐⭐⭐ | High |
| **Declarative** | Modern UIs, rapid dev | ⭐⭐⭐⭐ | Low |

## Conclusion

**MVP Pattern is excellent for:**
- ✅ Maximum testability (Presenter is UI-agnostic)
- ✅ Passive Views (easy to understand)
- ✅ Explicit contracts (clear API)
- ✅ Android/iOS development

**Your core module remains UI-agnostic** - MVP is just another adapter pattern!

You now have **FOUR** complete implementations:
1. **Declarative** (Edifice) - React-like
2. **MVVM** - Qt signals/slots
3. **MVI** - Redux-like immutable state
4. **MVP** - Passive View with smart Presenter ✨
