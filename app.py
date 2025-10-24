# app.py
from flask import Flask, render_template
import os
import threading
import time
import requests
from routes.device_routes import device_bp

app = Flask(__name__)
app.register_blueprint(device_bp)

# ----------------------------
# Keep-Alive (Optional for Render)
# ----------------------------
def keep_alive():
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if not render_url:
        return
    while True:
        try:
            requests.get(render_url, timeout=5)
            print("🔁 Keep-alive ping sent.")
        except Exception as e:
            print(f"⚠️ Keep-alive failed: {e}")
        time.sleep(300)

# ----------------------------
# Main Route
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ----------------------------
# Main Runner
# ----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"
    if os.getenv("RENDER"):
        threading.Thread(target=keep_alive, daemon=True).start()
    print(f"✅ Server running at http://localhost:{port}")
    app.run(host=host, port=port, debug=False)
