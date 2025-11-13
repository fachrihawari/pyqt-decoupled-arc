"""
Store - Central state container in the MVI pattern.
Manages state and processes intents through the reducer.
"""
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Callable
from state import ContactState
from intent import Intent
from reducer import ContactReducer


class ContactStore(QObject):
    """
    Store manages the application state.
    
    MVI Flow:
    1. View emits Intent
    2. Store receives Intent
    3. Store passes (current_state, intent) to Reducer
    4. Reducer returns new_state
    5. Store updates state and emits signal
    6. View receives new state and re-renders
    """
    
    # Signal emitted whenever state changes
    state_changed = pyqtSignal(ContactState)
    
    def __init__(self, reducer: ContactReducer, initial_state: ContactState = None):
        super().__init__()
        self._reducer = reducer
        self._state = initial_state or ContactState()
        
        # Middleware functions (optional, for logging/debugging)
        self._middleware = []
    
    @property
    def state(self) -> ContactState:
        """Get current state (read-only)."""
        return self._state
    
    def dispatch(self, intent: Intent):
        """
        Dispatch an intent to update state.
        
        This is the only way to change state in MVI.
        """
        # Run middleware (for logging, debugging, analytics)
        for middleware in self._middleware:
            middleware(self._state, intent)
        
        # Get new state from reducer
        new_state = self._reducer.reduce(self._state, intent)
        
        # Update state if it changed
        if new_state is not self._state:
            old_state = self._state
            self._state = new_state
            
            # Log state transition (helpful for debugging)
            self._log_transition(old_state, intent, new_state)
            
            # Notify views
            self.state_changed.emit(self._state)
    
    def add_middleware(self, middleware: Callable):
        """Add middleware function for side effects."""
        self._middleware.append(middleware)
    
    def _log_transition(self, old_state: ContactState, intent: Intent, new_state: ContactState):
        """Log state transitions (useful for debugging)."""
        print(f"[MVI] Intent: {intent.__class__.__name__}")
        print(f"      Contacts: {len(old_state.contacts)} → {len(new_state.contacts)}")
        print(f"      View: {old_state.current_view.value} → {new_state.current_view.value}")
        if new_state.error_message:
            print(f"      Error: {new_state.error_message}")
