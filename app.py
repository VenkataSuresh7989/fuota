from flask import Flask, render_template, request, jsonify
import os
import threading
import time
import requests

app = Flask(__name__)

# ----------------------------
# Utility Functions
# ----------------------------
def getXPRProgressMsg(sub):
    mapping = {
        "00": "Not active",
        "01": "Upgrade Failed",
        "02": "Upgrading...",
        "03": "Upgrade Failed",
        "04": "Upgrade image Ok",
        "05": "Restart Failed",
        "06": "Restart Pending"
    }
    return mapping.get(sub, "Unknown")

def hexaToBinary(resValue):
    resInfo = int(resValue, 16) if resValue else 0
    if resInfo & (0x01 << 0): return "Image Transmitted"
    if resInfo & (0x01 << 1): return "Success"
    if resInfo & (0x01 << 2): return "Upgrade Failed"
    if resInfo & (0x01 << 3): return "Upgrade Failed"
    return "Upgrade Failed"

def extractInt(response, startIdx, endIdx):
    sub_str = response[startIdx:endIdx]
    req_val = ''.join([c for c in sub_str if c.isdigit() or c == '-'])
    try:
        return int(req_val)
    except ValueError:
        return 0

# ----------------------------
# Routes
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_details', methods=['POST'])
def get_details():
    data = request.get_json()
    device_type = data.get('device_type')
    response = data.get('rx', "")

    devStatus = response[66:68] if len(response) >= 68 else "00"
    devPercent = int(response[68:70], 16) if len(response) >= 70 else 0
    devStatusMsg = getXPRProgressMsg(devStatus)
    status = ""

    if device_type == "129":  # Amplifier
        if devStatus == "06":
            dStatus = extractInt(response, 86, 88)
            status = hexaToBinary(hex(dStatus)[2:]) if dStatus != 0 else getXPRProgressMsg(devStatus)
        else:
            status = getXPRProgressMsg(devStatus)

    elif device_type == "128":  # Transponder
        if devStatus == "02":
            status = f"{getXPRProgressMsg(devStatus)} : {devPercent}%"
        elif devStatus != "00":
            status = getXPRProgressMsg(devStatus)
        else:
            status = "Success"

    return jsonify({
        "Device Status": devStatus,
        "Device Status Message": devStatusMsg,
        "Device Percentage": f"{devPercent}%",
        "Status": status
    })

# ----------------------------
# Keep-Alive Thread (Prevents Render Sleep)
# ----------------------------
def keep_alive():
    """Periodically ping the app to keep it alive on Render."""
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if not render_url:
        return  # Only run on Render

    while True:
        try:
            requests.get(render_url, timeout=5)
            print("🔁 Keep-alive ping sent.")
        except Exception as e:
            print(f"⚠️ Keep-alive failed: {e}")
        time.sleep(300)  # Ping every 5 minutes

# ----------------------------
# Main Runner (Local or Render)
# ----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"

    # Start keep-alive thread if on Render
    if os.getenv("RENDER"):
        threading.Thread(target=keep_alive, daemon=True).start()

    print(f"✅ Server running at http://localhost:{port}")
    app.run(host=host, port=port, debug=False)
