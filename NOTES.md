# AI Usage Note:
- Used Grok 3 for high-level guidance on implementation approach and code structure.
- Modified AI-provided code snippets to fit the specific requirements like flask routes & thread safety.
- Rejected overly complex suggestions (database usage) to adhere to in-memory storage requirement.

## Implementation Notes
- Built a Flask-based API with endpoints for health checks, URL shortening, redirection, and analytics.
- Used an in-memory dictionary (`URLStore` class) for storing URL mappings, ensuring simplicity and compliance with requirements.
- Implemented thread safety using `threading.Lock` to handle concurrent access to the store.
- Generated 6-character alphanumeric short codes using `random.choices` for simplicity and uniqueness with retry logic for collisions.
- Validated URLs with a regex to ensure they start with http:// or https://.
- Wrote 7 pytest tests to cover all critical paths like health check, valid/invalid URL shortening, valid/invalid redirects, valid/invalid stats.