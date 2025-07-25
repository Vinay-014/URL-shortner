from flask import Flask, jsonify, request, redirect, abort
from app.models import url_store
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Shorten a long URL and return a short code."""
    data = request.get_json()
    long_url = data.get('url') if data else None
    if not long_url or not is_valid_url(long_url):
        return jsonify({"error": "Invalid or missing URL"}), 400
    
    attempts = 10  # Limit retry attempts to avoid infinite loops
    while attempts > 0:
        short_code = generate_short_code()
        if url_store.add(short_code, long_url):
            short_url = f"http://localhost:5000/{short_code}"
            return jsonify({"short_code": short_code, "short_url": short_url}), 201
        attempts -= 1
    
    return jsonify({"error": "Failed to generate unique short code"}), 500

@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect to the original URL and increment click count."""
    entry = url_store.get(short_code)
    if not entry:
        abort(404)
    url_store.increment_clicks(short_code)
    return redirect(entry["url"])

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """Return analytics for a short code."""
    entry = url_store.get(short_code)
    if not entry:
        abort(404)
    return jsonify({
        "url": entry["url"],
        "clicks": entry["clicks"],
        "created_at": entry["created_at"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)