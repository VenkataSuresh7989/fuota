from flask import Flask, render_template
from routes.device_routes import device_bp
import threading
import os
import time
import requests

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(device_bp)


@app.route('/')
def index():
    return render_template('index.html')


# 🔹 Keep-Alive Thread (for Render hosting)
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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"
    if os.getenv("RENDER"):
        threading.Thread(target=keep_alive, daemon=True).start()
    print(f"✅ Server running at http://localhost:{port}")
    app.run(host=host, port=port, debug=False)
