# MVI Client - Model-View-Intent Pattern

This client demonstrates the **MVI (Model-View-Intent)** pattern with PyQt6, featuring **unidirectional data flow** and **immutable state**.

## MVI Pattern Overview

```
┌─────────────────────────────────────────────────────────┐
│                   User Interaction                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    Intent (Action)                       │
│  • AddContact(name, email, phone)                       │
│  • DeleteContact(contact_id)                            │
│  • NavigateToAdd()                                      │
│  • LoadContacts()                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  Store.dispatch(intent)                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│         Reducer(current_state, intent) → new_state      │
│  • Pure function (no side effects)                      │
│  • Predictable (same input = same output)               │
│  • Testable                                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                New State (Immutable)                     │
│  • contacts: [...]                                      │
│  • current_view: LIST/ADD                               │
│  • loading_state: IDLE/LOADING/SUCCESS/ERROR            │
│  • error_message: Optional[str]                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│            Store emits state_changed signal              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│              View.render(new_state)                      │
│  • Pure rendering based on state                        │
│  • No business logic                                    │
│  • Declarative UI updates                               │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
mvi-client/
├── main.py          # Entry point
├── intent.py        # User action definitions (intents)
├── state.py         # Immutable application state
├── reducer.py       # Pure state transformation logic
├── store.py         # State container & dispatcher
├── view.py          # Pure UI rendering
└── README.md        # This file

../core/             # Shared business logic (UI-agnostic)
```

## Key Components

### 1. **Intent** (`intent.py`)
Immutable data classes representing user actions.

```python
@dataclass(frozen=True)
class AddContact(Intent):
    name: str
    email: str
    phone: str = ""

@dataclass(frozen=True)
class DeleteContact(Intent):
    contact_id: str
```

**Benefits:**
- Type-safe actions
- Easy to log and debug
- Serializable for time-travel debugging

### 2. **State** (`state.py`)
Immutable application state.

```python
@dataclass(frozen=True)
class ContactState:
    current_view: ViewState = ViewState.LIST
    contacts: List[dict] = field(default_factory=list)
    loading_state: LoadingState = LoadingState.IDLE
    error_message: Optional[str] = None
    
    def copy_with(self, **kwargs):
        return replace(self, **kwargs)
```

**Benefits:**
- Predictable (can't be modified unexpectedly)
- Easy to debug (full state history)
- Time-travel debugging possible
- Easy to test

### 3. **Reducer** (`reducer.py`)
Pure function that produces new state.

```python
class ContactReducer:
    def reduce(self, state: ContactState, intent: Intent) -> ContactState:
        if isinstance(intent, AddContact):
            return self._add_contact(state, intent)
        elif isinstance(intent, DeleteContact):
            return self._delete_contact(state, intent)
        return state
```

**Benefits:**
- Pure function (no side effects)
- Easy to test (input → output)
- Predictable behavior
- Can be optimized/memoized

### 4. **Store** (`store.py`)
Manages state and dispatches intents.

```python
class ContactStore(QObject):
    state_changed = pyqtSignal(ContactState)
    
    def dispatch(self, intent: Intent):
        new_state = self._reducer.reduce(self._state, intent)
        self._state = new_state
        self.state_changed.emit(self._state)
```

**Benefits:**
- Single source of truth
- Centralized state management
- Easy debugging (log all state transitions)
- Middleware support

### 5. **View** (`view.py`)
Pure UI that renders based on state.

```python
class ContactView(QWidget):
    def __init__(self, store: ContactStore):
        self.store = store
        self.store.state_changed.connect(self.render)
    
    def render(self, state: ContactState):
        # Pure rendering based on state
        if state.current_view == ViewState.LIST:
            self.list_page.render(state)
```

**Benefits:**
- Declarative rendering
- No business logic in view
- Easy to test (pass mock state)
- Predictable UI updates

## Running the Application

```bash
cd mvi-client
python main.py
```

## MVI vs MVVM vs Declarative

| Aspect | MVI | MVVM | Declarative (Edifice) |
|--------|-----|------|----------------------|
| **State** | Immutable, centralized | Observable properties | Component-local hooks |
| **Updates** | Unidirectional flow | Bidirectional binding | Reactive re-rendering |
| **Debugging** | Time-travel possible | Signal debugging | React DevTools |
| **Predictability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Boilerplate** | Medium | Medium | Low |
| **Learning Curve** | Redux-like | Qt patterns | React patterns |
| **Testing** | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## Key Benefits of MVI

### ✅ **1. Predictable State Management**
- Same input always produces same output
- No hidden state mutations
- Easy to reason about

### ✅ **2. Time-Travel Debugging**
- Can replay any sequence of intents
- Can inspect state at any point in time
- Can undo/redo actions

### ✅ **3. Testability**
```python
def test_add_contact():
    reducer = ContactReducer(mock_manager)
    initial_state = ContactState(contacts=[])
    intent = AddContact(name="Test", email="test@example.com")
    
    new_state = reducer.reduce(initial_state, intent)
    
    assert len(new_state.contacts) == 1
    assert new_state.contacts[0]['name'] == "Test"
```

### ✅ **4. Middleware Support**
```python
def logging_middleware(state, intent):
    print(f"[{datetime.now()}] {intent}")

def analytics_middleware(state, intent):
    send_to_analytics(intent)

store.add_middleware(logging_middleware)
store.add_middleware(analytics_middleware)
```

### ✅ **5. Persistence**
```python
# Save state to disk
with open('state.json', 'w') as f:
    json.dump(dataclasses.asdict(state), f)

# Restore state from disk
with open('state.json', 'r') as f:
    data = json.load(f)
    state = ContactState(**data)
```

## When to Use MVI

### ✅ **Use MVI when:**
- Need predictable state management
- Building complex UIs with lots of state
- Want time-travel debugging
- Need to replay user actions
- Building forms with validation
- Team familiar with Redux/Elm/Flux

### ❌ **Don't use MVI when:**
- Simple CRUD app (MVVM is enough)
- Team not familiar with functional programming
- Real-time high-frequency updates (overhead)
- Prefer less boilerplate (use Edifice/declarative)

## MVI for MRI Simulator

MVI is **excellent** for MRI Simulator because:

### ✅ **1. Complex State Machine**
```python
@dataclass(frozen=True)
class MRIState:
    scan_state: ScanState  # IDLE/PREPARING/SCANNING/PROCESSING
    parameters: ScanParameters  # TE, TR, FOV, etc.
    kspace_data: np.ndarray
    reconstructed_image: np.ndarray
    progress: float  # 0-100%
    artifacts: List[Artifact]
```

### ✅ **2. Reproducible Scans**
```python
# Record scan as sequence of intents
scan_recording = [
    SetParameter(param="TE", value=30),
    SetParameter(param="TR", value=500),
    StartScan(),
    # ... scan completes ...
]

# Replay exact same scan later
for intent in scan_recording:
    store.dispatch(intent)
```

### ✅ **3. Educational Mode**
- Step through scan process
- Show state at each step
- Time-travel debugging for teaching

### ✅ **4. Validation**
```python
def validate_parameters(state: MRIState, intent: Intent):
    if isinstance(intent, SetParameter):
        if intent.param == "TE" and intent.value > state.parameters.TR:
            raise ValueError("TE cannot exceed TR")
```

## Example: Time-Travel Debugging

```python
# Record all intents
intent_history = []

def recording_middleware(state, intent):
    intent_history.append((datetime.now(), intent))

store.add_middleware(recording_middleware)

# Later: replay from any point
def replay_from(index):
    initial_state = ContactState()
    current_state = initial_state
    
    for i in range(index):
        _, intent = intent_history[i]
        current_state = reducer.reduce(current_state, intent)
    
    return current_state
```

## Testing Example

```python
import pytest
from reducer import ContactReducer
from state import ContactState
from intent import AddContact, DeleteContact

def test_add_contact_increases_count():
    reducer = ContactReducer(mock_manager)
    state = ContactState(contacts=[])
    intent = AddContact(name="Test", email="test@example.com", phone="123")
    
    new_state = reducer.reduce(state, intent)
    
    assert len(new_state.contacts) == 1

def test_delete_contact_removes_from_list():
    reducer = ContactReducer(mock_manager)
    state = ContactState(contacts=[
        {'id': '1', 'name': 'Test', 'email': 'test@example.com', 'phone': '123'}
    ])
    intent = DeleteContact(contact_id='1')
    
    new_state = reducer.reduce(state, intent)
    
    assert len(new_state.contacts) == 0

def test_reducer_is_pure():
    reducer = ContactReducer(mock_manager)
    state = ContactState(contacts=[])
    intent = AddContact(name="Test", email="test@example.com")
    
    # Call reducer twice
    state1 = reducer.reduce(state, intent)
    state2 = reducer.reduce(state, intent)
    
    # Should produce same result
    assert state1 == state2
```

## Conclusion

**MVI Pattern is excellent for:**
- ✅ Predictable state management
- ✅ Time-travel debugging
- ✅ Complex state machines (perfect for MRI simulator!)
- ✅ Reproducible actions
- ✅ Easy testing

**Your core module remains UI-agnostic** - MVI is just another adapter pattern, like MVVM and Declarative approaches!
