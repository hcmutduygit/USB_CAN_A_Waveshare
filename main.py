from waveshare_can import WaveshareCAN

if __name__ == "__main__":
    with WaveshareCAN(port='/dev/ttyUSB0', baudrate=2000000) as can_dev:
        can_dev.send(0x35E, "HELLO")
        # can_dev.send(0x005, [0x01, 0x02, 0x03])
        # can_dev.send(0x003, b"\x11\x22\x33\x44\x55")