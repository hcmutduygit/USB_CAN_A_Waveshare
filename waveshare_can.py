import serial

class WaveshareCAN:
    def __init__(self, port='COM8', baudrate=2000000, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        """Open serial port"""
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        print(f"🔌 Opened {self.port} @ {self.baudrate} baud")

    def close(self):
        """Đóng cổng serial"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 Closed serial port")

    def send(self, can_id, data):
        """
        Send 1 CAN frame
        :param can_id: int, CAN ID (11 bit standard)
        :param data: bytes or list[int] max 8 bytes
        """
        if not self.ser or not self.ser.is_open:
            raise Exception("Serial port hasn't opend! Call open() first.")

        if isinstance(data, str):
            data = data.encode('ascii')
        elif isinstance(data, list):
            data = bytes(data)
        elif isinstance(data, bytes) or isinstance(data, bytearray):
            pass
        else:
            raise TypeError("data must be bytes, bytearray, list[int] or str")

        if len(data) > 8:
            data = data[:8]
        elif len(data) < 8:
            data = data + bytes([0] * (8 - len(data)))

        frame = bytearray()
        frame.append(0xAA)
        frame.append(0xC8)
        frame.append(can_id & 0xFF)          # IDL 
        frame.append((can_id >> 8) & 0xFF)   # IDH

        frame.extend(data)
        frame.append(0x55)

        self.ser.write(frame)
        print(f"✅ Sent: ID=0x{can_id:03X}, Data={data.hex(' ')}")

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

