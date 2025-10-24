# utils/helpers.py

# XPR Progress Mapping
XPR_PROGRESS_MAPPING = {
    "00": "Success (or) Not active",
    "01": "Upgrade Failed (or) Upgrade initialized but image transport not started",
    "02": "Upgrading... (or) On Going",
    "03": "Upgrade Failed (or) Upgrade image BAD",
    "04": "Upgrade image Ok",
    "05": "Restart Failed",
    "06": "Restart Pending"
}

# Hex Binary Mapping
HEX_BINARY_MAPPING = {
    0: "None",
    1: "Image Transmitted",
    2: "Success",
    4: "Upgrade Failed",
    8: "Upgrade Failed"
}

def getXPRProgressMsg(code):
    return XPR_PROGRESS_MAPPING.get(code, "Unknown")

def hexaToBinary(hex_val):
    try:
        value = int(hex_val, 16)
        for mask, msg in HEX_BINARY_MAPPING.items():
            if value & mask:
                return msg
        return "Upgrade Failed"
    except:
        return "Upgrade Failed"

def extractInt(response, startIdx, endIdx):
    sub_str = response[startIdx:endIdx]
    req_val = ''.join([c for c in sub_str if c.isdigit() or c == '-'])
    try:
        return int(req_val)
    except:
        return 0

def swVersionConversion(hexVal, isReverse=False):
    try:
        preHex = hexVal[:2]
        nexHex = hexVal[2:]
        val1 = int(preHex, 16) if preHex else 0
        val2 = int(nexHex, 16) if nexHex else 0
        data = f"{val2}.{val1}" if isReverse else f"{val1}.{val2}"
        return "--.--" if data == "0.0" else data
    except:
        return hexVal

# 🔹 Return all mappings for UI display
def getStatusMappings():
    return {"XPR Progress": XPR_PROGRESS_MAPPING, "Hex Binary": HEX_BINARY_MAPPING}
