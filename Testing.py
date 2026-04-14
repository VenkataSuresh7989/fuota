import serial.tools.list_ports


def list_com_ports():
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("No COM ports found")
        return

    print("Available COM Ports:")
    for port in ports:
        print(f"Device: {port.device}")
        print(f"Name: {port.name}")
        print(f"Description: {port.description}")
        print(f"HWID: {port.hwid}")
        print("-" * 30)


if __name__ == "__main__":
    list_com_ports()