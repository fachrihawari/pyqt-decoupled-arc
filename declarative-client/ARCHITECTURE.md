# Declarative UI + Clean Architecture + Global State Management

## Do You Need MVVM?

**No, traditional MVVM is not needed** with Edifice's declarative/reactive approach. Here's why:

### Traditional MVVM Components:
- **Model**: Domain entities and business logic
- **View**: UI presentation (QML, widgets)
- **ViewModel**: State management, UI logic, commands, data binding

### With Edifice (React-like) Architecture + Global State:

```
┌────────────────────────────────────────────────────┐
│         Global Context (contact_manager_context)   │
│  ┌──────────────────────────────────────────────┐  │
│  │   Singleton ContactManager                   │  │ ← Global State
│  │   + Event Subscriptions                      │  │
│  │   + Reactive Updates                         │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
                        ↑
                        │ (hooks: use_contact_manager)
                        │
┌─────────────────────────────────────────────────────┐
│            Self-Contained Components                │
│  ┌───────────────────────────────────────────────┐  │
│  │  ContactList Component                        │  │
│  │    - Accesses global manager                  │  │ ← Replaces ViewModel
│  │    - Gets contacts state                      │  │
│  │    - Handles own business logic               │  │
│  │    - Renders declaratively                    │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │  ContactAdd Component                         │  │
│  │    - Accesses global manager                  │  │
│  │    - Manages form state                       │  │
│  │    - Calls use cases directly                 │  │
│  │    - No prop drilling needed                  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        │
                        ↓ (direct use case calls)
┌────────────────────────────────────────────────────┐
│            Core Business Logic Layer               │
│  ┌──────────────────────────────────────────────┐  │
│  │  ContactManager (Facade/Application Service) │  │
│  │    ├─ Use Cases                              │  │
│  │    ├─ Domain Models                          │  │
│  │    ├─ Repository                             │  │
│  │    ├─ Event Bus                              │  │
│  │    └─ Serializers (domain → UI dicts)        │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

## Key Differences from MVVM:

### 1. **State Management**
- **MVVM**: ViewModel holds observable properties
- **Edifice**: Component hooks (`use_state`) manage state directly
- **Result**: No need for separate ViewModel class

### 2. **Data Binding**
- **MVVM**: Two-way binding via signals/slots or property binding
- **Edifice**: One-way data flow with explicit state updates
- **Result**: Simpler, more predictable updates

### 3. **Separation of Concerns**
- **MVVM**: View ↔ ViewModel ↔ Model
- **Edifice**: Component (View + Logic) ↔ Adapter ↔ Core
- **Result**: Fewer layers, less boilerplate

## Architecture Layers:

### Layer 1: Core (Business Logic) ✅
**Location**: `core/` module

Well-designed with:
- Domain models (`Contact`)
- Use cases (create, read, delete)
- Repository pattern
- Event bus for reactive updates
- **Serializers** (`serializers.py`) for domain → UI transformation

**Responsibilities**:
- Business rules
- Data persistence
- Domain events
- Data transformation (domain objects → dicts)

### Layer 2: Global State Management �
**Location**: `contact_manager_context.py`

Provides hooks for accessing global ContactManager:

```python
# Hook 1: Full access (manager + contacts state)
manager, contacts = use_contact_manager()

# Hook 2: Lightweight (manager only, no state)
manager = use_contact_manager_only()
```

**Features**:
- Singleton ContactManager instance
- Automatic event subscription and cleanup
- Reactive state updates via domain events
- No prop drilling needed

**Responsibilities**:
- Initialize ContactManager singleton
- Subscribe to domain events
- Manage contacts state synchronization
- Provide hooks for components

### Layer 3: Self-Contained Components 🎨
**Location**: `pages/` components

Components now handle their own business logic:

```python
@component
def ContactList(self, navigate):
    # Access global state directly
    manager, contacts = use_contact_manager()
    
    def delete_contact(contact_id):
        # Call core business logic directly
        manager.delete_contact(contact_id)
        # Events trigger automatic UI update
    
    # Render UI declaratively
```

```python
@component
def ContactAdd(self, navigate):
    # Access global manager
    manager = use_contact_manager_only()
    
    def save():
        # Call core business logic directly
        manager.create_contact(name, email, phone)
        navigate("list")
    
    # Render form UI
```

**Responsibilities**:
- Access global manager via hooks
- Handle user interactions
- Call use cases directly
- Manage local form/UI state
- Render UI declaratively

### Layer 4: Router (App Shell) 📱
**Location**: `main.py`

Minimal routing logic only:

```python
@component
def MyApp(self):
    route, set_route = use_state("list")
    
    def navigate(r):
        set_route(r)
    
    # Simple page routing - components are self-contained
    if route == "list":
        ContactList(navigate=navigate)
    elif route == "add":
        ContactAdd(navigate=navigate)
```

**Responsibilities**:
- Handle page routing only
- No business logic
- No prop drilling

## Benefits of This Approach:

### ✅ **No MVVM Boilerplate**
- No ViewModel classes needed
- No signal/slot complexity
- Direct state management with hooks
- Components handle their own logic

### ✅ **No Prop Drilling**
- Global state accessible anywhere
- Components are self-contained
- Add components without modifying parents
- Clean component API (minimal props)

### ✅ **Reactive & Declarative**
- UI updates automatically when state changes
- Easy to reason about data flow
- Component composition is natural
- One-way data flow from core → UI

### ✅ **Clean Separation**
- Core module is 100% UI-agnostic
- Easy to test business logic independently
- Can swap UI frameworks without touching core
- Serializers in core ensure consistent data transformation

### ✅ **Event-Driven Updates**
- Core publishes domain events once per action
- UI subscribes and reacts automatically
- Multiple UIs can listen to same events
- Optimized state updates (no re-fetching)

### ✅ **Scalability**
- Easy to add new components
- Easy to add new features
- Components can be dropped anywhere in tree
- Global state prevents coupling

## Current Pattern: Global State with Custom Hooks ✅

This app uses **custom hooks pattern** (similar to React Context):

### ✅ **Already Implemented:**
- Global singleton ContactManager
- Custom hooks (`use_contact_manager`, `use_contact_manager_only`)
- Event-driven reactive updates
- Self-contained components
- No prop drilling

### When to Add More Patterns:

**Use a centralized state management library (like Redux/Zustand) if:**
- You need time-travel debugging
- Complex state with many interdependencies
- Need middleware for logging/persistence
- Team prefers structured state mutations

**Use separate "Service" classes if:**
- Multiple complex business workflows
- Need additional abstraction layer
- Want more testable mocks
- Building for multiple client types (web + desktop)

**Current approach is perfect if:**
- ✅ App is small to medium sized (like this one)
- ✅ Global state is straightforward (contacts list)
- ✅ Core module handles business logic well
- ✅ Custom hooks provide enough abstraction

## Example Flow (Updated):

```
User clicks "Save" in ContactAdd
        ↓
ContactAdd.save() handler
        ↓
manager.create_contact(name, email, phone)  ← Direct call
        ↓
CreateContactUseCase.execute()
        ↓
Contact saved to repository
        ↓
Domain event published: CONTACT_CREATED (once!)
        ↓
Global context event handler triggered
        ↓
set_contacts(lambda: current + [new_contact])  ← Optimized update
        ↓
ContactList re-renders automatically ✨
        ↓
ContactAdd navigates to "list"
```

**Key improvements:**
- ✅ No intermediate adapter functions
- ✅ Components call manager directly
- ✅ Events published once (fixed duplicate issue)
- ✅ State updated optimally (no re-fetching)
- ✅ Serializers in core handle transformations

## Testing Strategy:

### Core Layer (Unit Tests)
- Test use cases independently
- Mock repositories
- Verify domain events published correctly
- Test serializers (domain → dict conversion)

### Global Context (Integration Tests)
- Test hook initialization
- Verify event subscriptions work
- Test state updates on events
- Test cleanup on unmount

### Components (Component Tests)
- Test rendering with mock manager
- Test user interactions (clicks, form input)
- Verify use case calls
- Snapshot testing for UI

### E2E Tests
- Full user flows (add → list → delete)
- Verify UI updates automatically
- Test navigation between pages

## Project Structure (Updated):

```
declarative-client/
├── contact_manager_context.py  # 🌐 Global state hooks
├── main.py                      # 📱 Router only (15 lines!)
├── pages/
│   ├── contact_list.py         # 🎨 Self-contained list component
│   └── contact_add.py          # 🎨 Self-contained form component
├── examples_usage.py           # 📚 Hook usage examples
└── requirements.txt

../core/                         # 🏗️ Business logic (UI-agnostic)
├── serializers.py              # 🔄 Domain → UI transformations
├── application/
│   ├── contact_manager.py      # Facade/service
│   └── use_cases.py            # Business operations
├── domain/
│   ├── contact.py              # Entities
│   └── events.py               # Domain events
├── repository/
│   └── contact_repository.py   # Data access
└── event_bus/
    └── event_bus.py            # Pub/sub system
```

## Conclusion:

**You don't need MVVM** because:
1. ✅ **Global hooks replace ViewModel layer** - `use_contact_manager()` provides everything
2. ✅ **Components are self-contained** - Each handles its own logic (no prop drilling)
3. ✅ **Core is UI-agnostic** - Well-architected with use cases, events, serializers
4. ✅ **Event-driven reactivity** - Automatic UI updates via domain events
5. ✅ **Less boilerplate** - ~50 lines removed from main.py

**Result**: Less code, easier maintenance, clearer data flow, better scalability.

This is the **modern React/Edifice pattern** - similar to how React apps work with global state (Context/Zustand) and backend APIs. You don't need ViewModels, just:
- Smart self-contained components
- Global state via custom hooks
- Clean core business logic
- Event-driven updates
