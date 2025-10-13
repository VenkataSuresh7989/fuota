from flask import Flask, render_template, request, jsonify
import socket
import webbrowser

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
# Main Runner (Local Network)
# ----------------------------
if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    port = 5000
    url = f"http://{local_ip}:{port}"

    print(f"\n✅ App running at: {url}")
    webbrowser.open(url)
    app.run(host=local_ip, port=port, debug=True)
