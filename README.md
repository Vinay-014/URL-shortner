# URL-Shortener

## Overview
Built a simple URL shortening service similar to bit.ly or tinyurl. This work showcases my ability to design and implement a small but complete feature from scratch.

### Setup
```bash
# Clone/download this repository
# Navigate to the assignment directory
cd url-shortener

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m flask --app app.main run

# The API will be available at http://localhost:5000
# Run tests with: pytest
```

### What was Provided
- Basic Flask application structure
- Health check endpoints
- One example test
- Empty files for your implementation

### ToDo

1. **Shorten URL Endpoint**
   - `POST /api/shorten`
   - Accept a long URL in the request body
   - Return a short code (e.g., "abc123")
   - Store the mapping for later retrieval

2. **Redirect Endpoint**
   - `GET /<short_code>`
   - Redirect to the original URL
   - Return 404 if short code doesn't exist
   - Track each redirect (increment click count)

3. **Analytics Endpoint**
   - `GET /api/stats/<short_code>`
   - Return click count for the short code
   - Return creation timestamp
   - Return the original URL

### Technical Requirements

- URLs are validated before shortening
- Short codes consisting 6 characters in alphanumeric
- Handled concurrent requests properly
- Included basic error handling
- Written at least 5 tests covering core functionality

### Example API Usage

```bash
# Shorten a URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'

# Response: {"short_code": "$shortcode", "short_url": "http://localhost:5000/$shortcode"}

# Use the short URL (this redirects)
curl -L http://localhost:5000/$shortcode

# Get analytics
curl http://localhost:5000/api/stats/$shortcode

# Response: {"url": "https://www.example.com/very/long/url", "clicks": 5, "created_at": "2024-01-01T10:00:00"}
```
