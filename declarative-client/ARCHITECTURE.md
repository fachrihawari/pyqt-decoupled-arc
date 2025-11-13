# Declarative UI + Clean Architecture

## Do You Need MVVM?

**No, traditional MVVM is not needed** with Edifice's declarative/reactive approach. Here's why:

### Traditional MVVM Components:
- **Model**: Domain entities and business logic
- **View**: UI presentation (QML, widgets)
- **ViewModel**: State management, UI logic, commands, data binding

### With Edifice (React-like) Architecture:

```
┌─────────────────────────────────────────────────────┐
│                  Edifice Component                   │
│  ┌──────────────────────────────────────────────┐  │
│  │    Component State (use_state hooks)         │  │ ← Replaces ViewModel
│  │    - Local UI state                          │  │
│  │    - Event handlers                          │  │
│  │    - Reactive rendering                      │  │
│  └──────────────────────────────────────────────┘  │
│                        │                            │
│                        ↓                            │
│  ┌──────────────────────────────────────────────┐  │
│  │     Declarative View (JSX-like syntax)       │  │
│  │    - Automatic updates when state changes    │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        │
                        ↓ (adapter functions)
┌─────────────────────────────────────────────────────┐
│            Core Business Logic Layer                 │
│  ┌──────────────────────────────────────────────┐  │
│  │  ContactManager (Facade/Application Service) │  │
│  │    ├─ Use Cases                              │  │
│  │    ├─ Domain Models                          │  │
│  │    ├─ Repository                             │  │
│  │    └─ Event Bus                              │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
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

Already well-designed with:
- Domain models (`Contact`)
- Use cases (create, read, delete)
- Repository pattern
- Event bus for reactive updates

**Responsibilities**:
- Business rules
- Data persistence
- Domain events

### Layer 2: Adapter Functions 🆕
**Location**: `main.py` functions

Simple functions that translate between UI and core:

```python
def add_contact(contact_dict):
    """Adapter: UI dict → Core use case"""
    manager.create_contact(
        name=contact_dict['name'],
        email=contact_dict['email'],
        phone=contact_dict['phone']
    )

def contact_to_dict(contact):
    """Adapter: Core domain → UI dict"""
    return {
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'phone': contact.phone
    }
```

**Responsibilities**:
- Data transformation
- Calling use cases
- Event subscription

### Layer 3: Edifice Components 🎨
**Location**: `pages/` components

Declarative UI components with hooks:

```python
@component
def ContactList(self, contacts, navigate, on_delete):
    # Renders UI based on props
    # Handles user interactions
    # No business logic
```

**Responsibilities**:
- Render UI declaratively
- Handle user interactions
- Display data (no business logic)

## Benefits of This Approach:

### ✅ **Simpler Than MVVM**
- No ViewModel boilerplate
- No signal/slot complexity
- Direct state management with hooks

### ✅ **Reactive & Declarative**
- UI updates automatically when state changes
- Easy to reason about data flow
- Component composition is natural

### ✅ **Clean Separation**
- Core module is UI-agnostic
- Easy to test business logic independently
- Can swap UI frameworks without touching core

### ✅ **Event-Driven Updates**
- Core publishes domain events
- UI subscribes and reacts automatically
- Multiple UIs can listen to same events

## When to Use Additional Patterns:

### Use a separate "Service" layer if:
- You have complex cross-cutting concerns
- Multiple components need same business operations
- You want more abstraction from core

### Use Context/State Management library if:
- Deep component trees need shared state
- Prop drilling becomes painful
- Global state is needed (user auth, theme, etc.)

### Keep it simple if:
- App is small/medium sized (like this one)
- State flows naturally through components
- Direct adapter functions work well

## Example Flow:

```
User clicks "Add Contact"
        ↓
ContactAdd component calls on_save(dict)
        ↓
add_contact adapter function
        ↓
manager.create_contact() use case
        ↓
Domain event published: CONTACT_CREATED
        ↓
Event handler refreshes contacts
        ↓
set_contacts() updates state
        ↓
ContactList re-renders automatically ✨
```

## Testing Strategy:

### Core Layer (Unit Tests)
- Test use cases independently
- Mock repositories
- Verify domain events

### Adapter Functions (Integration Tests)
- Test data transformations
- Verify correct use case calls
- Check event subscriptions

### Components (Component Tests)
- Test rendering with different props
- Test user interactions
- Snapshot testing for UI

## Conclusion:

**You don't need MVVM** because:
1. Edifice components handle what ViewModels do (state + logic)
2. Your core is already well-architected
3. Simple adapter functions bridge the gap
4. Result: Less code, easier maintenance, clearer data flow

This is similar to how React apps work with backend APIs - you don't need ViewModels, just smart components and service functions.
