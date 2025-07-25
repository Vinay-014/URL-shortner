from threading import Lock
from datetime import datetime

class URLStore:
    """In-memory store for URL mappings with thread-safe operations."""
    def __init__(self):
        self._store = {}  # {short_code: {"url": str, "clicks": int, "created_at": str}}
        self._lock = Lock()

    def add(self, short_code, long_url):
        """Add a new URL mapping."""
        with self._lock:
            if short_code in self._store:
                return False
            self._store[short_code] = {
                "url": long_url,
                "clicks": 0,
                "created_at": datetime.utcnow().isoformat()
            }
            return True

    def get(self, short_code):
        """Retrieve URL mapping by short code."""
        with self._lock:
            return self._store.get(short_code)

    def increment_clicks(self, short_code):
        """Increment click count for a short code."""
        with self._lock:
            if short_code in self._store:
                self._store[short_code]["clicks"] += 1
                return True
            return False

# Global store instance
url_store = URLStore()