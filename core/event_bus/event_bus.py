from __future__ import annotations
import threading
from collections import defaultdict
from typing import Callable, Any, Dict, List

Callback = Callable[[Any], None]


class EventBus:
    """
    Lightweight, thread-safe publish/subscribe event bus.

    Usage:
        bus = EventBus()
        def on_created(payload): ...
        bus.subscribe("ContactCreated", on_created)
        bus.publish("ContactCreated", {"contact": contact})
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._subscribers: Dict[str, List[Callback]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callback) -> Callable[[], None]:
        """
        Subscribe to an event. Returns an unsubscribe function.

        event_name: string identifier for event (e.g. "ContactCreated")
        callback: callable that accepts a single payload argument
        """
        with self._lock:
            self._subscribers[event_name].append(callback)

        def _unsubscribe() -> None:
            with self._lock:
                try:
                    self._subscribers[event_name].remove(callback)
                except ValueError:
                    pass

        return _unsubscribe

    def publish(self, event_name: str, payload: Any = None) -> None:
        """
        Publish an event to all subscribers. Exceptions in subscribers are caught
        and do not stop delivery to other subscribers.
        """
        with self._lock:
            subscribers = list(self._subscribers.get(event_name, []))

        for callback in subscribers:
            try:
                callback(payload)
            except Exception:
                # In core library we avoid logging dependencies; clients can subscribe
                # and handle their own logging. Swallow exceptions to not break other subscribers.
                pass
