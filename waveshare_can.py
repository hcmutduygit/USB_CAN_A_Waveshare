import serial
import threading

class WaveshareCAN:
    """
    WaveshareCAN
    -------------
    A simple class to send and receive CAN frames via Waveshare USB-CAN module over UART.
    Supports:
        - Sending single frame
        - Receiving single frame
        - Continuous receive loop in a separate thread with callback
    """

    def __init__(self, port='COM8', baudrate=2000000, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self._rx_thread = None
        self._rx_running = False

    def open(self):
        """Open the serial port."""
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        print(f"🔌 Serial port opened: {self.port} @ {self.baudrate} baud")

    def close(self):
        """Stop the receive loop (if running) and close the serial port."""
        self._rx_running = False
        if self._rx_thread and self._rx_thread.is_alive():
            self._rx_thread.join()
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 Serial port closed")

    def send(self, can_id, data):
        """
        Send a CAN frame.

        :param can_id: int, CAN ID (11-bit standard)
        :param data: bytes | list[int] | str (up to 8 bytes)
        """
        if not self.ser or not self.ser.is_open:
            raise Exception("Serial port is not open. Call open() first.")

        if isinstance(data, str):
            data = data.encode('ascii')
        elif isinstance(data, list):
            data = bytes(data)
        elif isinstance(data, (bytes, bytearray)):
            pass
        else:
            raise TypeError("Data must be bytes, bytearray, list[int], or str")

        if len(data) > 8:
            data = data[:8]
        elif len(data) < 8:
            data += bytes([0] * (8 - len(data)))

        frame = bytearray()
        frame.append(0xAA)
        frame.append(0xC8)
        frame.append(can_id & 0xFF)          # IDL
        frame.append((can_id >> 8) & 0xFF)   # IDH
        frame.extend(data)
        frame.append(0x55)

        self.ser.write(frame)
        print(f"✅ Sent: ID=0x{can_id:03X} Data={data.hex(' ')}")

    def receive(self):
        """
        Receive one CAN frame.

        :return: tuple (can_id, data: bytes)
        """
        if not self.ser or not self.ser.is_open:
            raise Exception("Serial port is not open. Call open() first.")

        while True:
            b = self.ser.read(1)
            if not b:
                continue
            if b[0] == 0xAA:
                break

        cmd = self.ser.read(1)
        if not cmd or cmd[0] != 0xC8:
            raise ValueError("Invalid CMD byte")

        idl = self.ser.read(1)
        idh = self.ser.read(1)
        data = self.ser.read(8)
        tail = self.ser.read(1)

        if not tail or tail[0] != 0x55:
            raise ValueError("Invalid tail byte")

        can_id = idl[0] | (idh[0] << 8)

        print(f"📥 Received: ID=0x{can_id:03X} Data={data.hex(' ')}")
        return can_id, data

    def start_receive_loop(self, callback):
        """
        Start a separate thread to continuously receive CAN frames
        and call the given callback(can_id, data).

        :param callback: function(can_id, data)
        """
        if self._rx_thread and self._rx_thread.is_alive():
            print("🔄 Receive loop already running.")
            return

        self._rx_running = True
        self._rx_thread = threading.Thread(
            target=self._receive_worker,
            args=(callback,),
            daemon=True
        )
        self._rx_thread.start()
        print("🔄 Receive loop started (thread)")

    def _receive_worker(self, callback):
        """Worker thread that continuously receives frames and calls callback."""
        try:
            while self._rx_running:
                can_id, data = self.receive()
                callback(can_id, data)
        except Exception as e:
            print(f"❌ Error in receive loop: {e}")

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
