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
