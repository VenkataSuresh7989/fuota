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

# 🔹 SW Version Conversion
def swVersionConversion(hexVal, isReverse=False):
    try:
        preHex = hexVal[:2]
        nexHex = hexVal[2:]
        val1 = int(preHex, 16) if preHex else 0
        val2 = int(nexHex, 16) if nexHex else 0
        data = f"{val2}.{val1}" if isReverse else f"{val1}.{val2}"
        if data == "0.0":
            data = "--.--"
        return data
    except Exception as e:
        print("Error during SW version conversion:", e)
        return hexVal

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

    # 🔹 Firmware version logic
    typeRanges = {
        "128": {"start": 57, "end": 58},
        "129": {"start": 60, "end": 61}
    }
    fw_version = "--.--"
    if device_type in typeRanges and len(response) > typeRanges[device_type]["end"] * 2:
        bytes_list = [response[i:i+2] for i in range(0, len(response), 2)]
        range_ = typeRanges[device_type]
        slice_ = bytes_list[range_["start"]:range_["end"] + 1]
        if len(slice_) == 2:
            joined = slice_[0] + slice_[1]
            fw_version = swVersionConversion(joined, isReverse=False)

    # 🔹 Device status logic
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
        "Firmware Version": fw_version,
        "Status": status
    })

# ----------------------------
# Keep-Alive Thread (Render)
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
# Main Runner
# ----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"
    if os.getenv("RENDER"):
        threading.Thread(target=keep_alive, daemon=True).start()
    print(f"✅ Server running at http://localhost:{port}")
    app.run(host=host, port=port, debug=False)
