# routes/device_routes.py
from flask import Blueprint, request, jsonify
from utils.helpers import getXPRProgressMsg, hexaToBinary, extractInt, swVersionConversion, getStatusMappings

device_bp = Blueprint("device_bp", __name__)

@device_bp.route('/get_details', methods=['POST'])
def get_details():
    data = request.get_json()
    device_type = data.get('device_type')
    response = data.get('rx', "")

    devStatus = response[66:68] if len(response) >= 68 else "00"
    devPercent = int(response[68:70], 16) if len(response) >= 70 else 0
    devStatusMsg = getXPRProgressMsg(devStatus)
    status = ""

    # Firmware version logic
    typeRanges = {"128": {"start": 57, "end": 58}, "129": {"start": 60, "end": 61}}
    fw_version = "--.--"
    if device_type in typeRanges and len(response) > typeRanges[device_type]["end"] * 2:
        bytes_list = [response[i:i+2] for i in range(0, len(response), 2)]
        r = typeRanges[device_type]
        s = bytes_list[r["start"]:r["end"] + 1]
        if len(s) == 2:
            fw_version = swVersionConversion(s[0] + s[1])

    # Device status logic
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

# 🔹 API to send all status options to UI
@device_bp.route('/status_options', methods=['GET'])
def status_options():
    return jsonify(getStatusMappings())
