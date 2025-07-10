# USB CAN A Waveshare

Python library for communicating with Waveshare USB CAN A module through serial interface.

## 📋 Description

This project provides a simple interface for sending CAN frames through Waveshare USB CAN A module. The module converts CAN signals to USB serial communication, allowing computers to communicate with CAN bus networks easily.

## 🔧 System Requirements

- Python 3.6+
- `pyserial` module 
- USB CAN A Waveshare module
- Operating System: Windows, Linux, macOS

## 📦 Installation

1. Clone repository or download files:
```bash
git clone <repository-url>
cd USB_CAN_A_Waveshare
```

2. Install required libraries:
```bash
pip install pyserial
```

## 🚀 Usage

### Basic Example

```python
from waveshare_can import WaveshareCAN

# Using with context manager (recommended)
with WaveshareCAN(port='/dev/ttyUSB0', baudrate=2000000) as can_dev:
    # Send text string
    can_dev.send(0x35E, "HELLO")
    
    # Send list of bytes
    can_dev.send(0x005, [0x01, 0x02, 0x03])
    
    # Send binary data
    can_dev.send(0x003, b"\x11\x22\x33\x44\x55")
```

### Manual Usage

```python
from waveshare_can import WaveshareCAN

# Create instance
can_dev = WaveshareCAN(port='/dev/ttyUSB0', baudrate=2000000)

# Open connection
can_dev.open()

# Send data
can_dev.send(0x123, "DATA")

# Close connection
can_dev.close()
```

## 📡 CAN Frame Protocol

Module uses the following frame format:

```
| AA | C8 | IDL | IDH | DATA[0-7] | 55 |
```

- `AA C8`: Header
- `IDL`: CAN ID Low byte
- `IDH`: CAN ID High byte  
- `DATA[0-7]`: 8 bytes of data (padded with 0x00 if < 8 bytes)
- `55`: Footer

## 🤝 Contributing

All contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a Pull Request

## 📄 License

Free

## 📞 Contact

- **Author**: [Duy]
- **Email**: [duy.duongfebruary@gmail.com]
- **Project**: Reception Robot - HCMUT

---

*This project is part of the Reception Robot system at HCMUT.*
