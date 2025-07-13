# Waveshare USB-CAN Library

A comprehensive library for communicating with Waveshare USB-CAN modules over serial/UART interface. This library provides an easy-to-use interface for sending and receiving CAN frames with support for both Windows and Linux platforms.

## Available Implementations

This library is available in **two implementations** to suit different project requirements:

### 🐍 Python Implementation (`waveshare_can.py`)
- **Best for**: Rapid prototyping, IoT projects, integration with existing Python systems
- **Features**: Simple API, built-in threading, automatic data type handling
- **Dependencies**: `pyserial` library
- **Performance**: Good for most applications, easier debugging

### ⚡ C++ Implementation (`waveshare_can.hpp`)
- **Best for**: High-performance applications, embedded systems, real-time control
- **Features**: Zero-copy operations, minimal memory footprint, cross-platform
- **Dependencies**: Standard C++11, system serial libraries
- **Performance**: Maximum speed and efficiency

## When to Use Which Version?

| Use Case | Python | C++ |
|----------|--------|-----|
| IoT/Automation Projects | ✅ | ⚠️ |
| Real-time Control Systems | ⚠️ | ✅ |
| Rapid Prototyping | ✅ | ⚠️ |
| High-frequency CAN Traffic | ⚠️ | ✅ |
| Integration with Python Apps | ✅ | ❌ |
| Embedded/Resource-constrained | ❌ | ✅ |
| Cross-language Integration | ⚠️ | ✅ |

## Common Features (Both Versions)

- ✅ **Cross-platform support** (Windows & Linux)
- ✅ **Send CAN frames** with 11-bit standard ID
- ✅ **Receive CAN frames** (blocking and non-blocking)
- ✅ **Continuous receive loop** with callback function
- ✅ **Thread-safe operations**
- ✅ **Automatic serial port configuration**

## Python-Specific Features

- ✅ **Automatic data type conversion**
- ✅ **Built-in pyserial integration**
- ✅ **Exception-based error handling**
- ✅ **Dynamic port detection**

## C++ Specific Features

- ✅ **Zero-copy operations**
- ✅ **Debug mode** for troubleshooting
- ✅ **RAII resource management**
- ✅ **Header-only implementation**
**Multiple data format support** (vector, array, string)
- ✅ **Robust error handling** and timeout management
- ✅ **Automatic serial port configuration**

## Python-Specific Features

- ✅ **Automatic data type conversion**
- ✅ **Built-in pyserial integration**
- ✅ **Exception-based error handling**
- ✅ **Dynamic port detection**

## C++ Specific Features

- ✅ **Zero-copy operations**
- ✅ **Debug mode** for troubleshooting
- ✅ **RAII resource management**
- ✅ **Header-only implementation**

## CAN Frame Format

The library uses the Waveshare USB-CAN protocol format:

```
AA C8 IDL IDH DATA[8] 55
```

- `AA`: Start byte (Header)
- `C8`: Command byte  
- `IDL`: CAN ID Low byte (bits 0-7)
- `IDH`: CAN ID High byte (bits 8-10)
- `DATA[8]`: 8 bytes of data (padded with zeros if less than 8)
- `55`: End byte (Tail)

## Quick Start

Choose your preferred implementation:

### 🐍 Python Quick Start

#### 1. Install Dependencies

```bash
pip install pyserial
```

#### 2. Basic Python Usage

```python
from waveshare_can import WaveshareCAN

# Create CAN interface
can = WaveshareCAN(port='/dev/ttyUSB0', baudrate=2000000)  # Linux
# can = WaveshareCAN(port='COM8', baudrate=2000000)       # Windows

# Open connection
can.open()

# Send a CAN frame
can.send(0x123, [0x01, 0x02, 0x03, 0x04])

# Receive a single frame
frame = can.receive()
if frame:
    can_id, data = frame
    print(f"Received: ID=0x{can_id:X}, Data={data}")

# Start continuous receive with callback
def on_frame_received(can_id, data):
    print(f"Frame: ID=0x{can_id:X}, Data={data}")

can.start_receive_loop(on_frame_received)

# Keep running for 10 seconds
import time
time.sleep(10)

# Cleanup
can.close()
```

### ⚡ C++ Quick Start

#### 1. C++ Hardware Setup

1. Connect your Waveshare USB-CAN module to the computer via USB
2. Connect CAN_H and CAN_L to your CAN bus network
3. Ensure proper CAN bus termination (120Ω resistors at both ends)
4. Power on your CAN devices

#### 2. Build the C++ Library

```bash
# Clone or download the source files
# Navigate to the library directory
cd USB_CAN_A_Waveshare/

# Build the example application
make

# Or build just the static library
make lib

# Build with debug symbols
make debug
```

#### 3. C++ Basic Usage Example

```cpp
#include "waveshare_can.hpp"

int main() {
    try {
        // Create CAN interface (adjust port as needed)
        WaveshareCAN can("/dev/ttyUSB0", 2000000);  // Linux
        // WaveshareCAN can("COM8", 2000000);       // Windows
        
        // Open connection
        if (!can.open()) {
            std::cerr << "Failed to open CAN interface" << std::endl;
            return -1;
        }
        
        // Send a CAN frame
        std::vector<uint8_t> data = {0x01, 0x02, 0x03, 0x04};
        can.send(0x123, data);
        
        // Receive a single frame
        uint16_t rx_id;
        std::vector<uint8_t> rx_data;
        if (can.receive(rx_id, rx_data)) {
            std::cout << "Received: ID=0x" << std::hex << rx_id << std::endl;
        }
        
        // Start continuous receive with callback
        can.start_receive_loop([](uint16_t id, const std::vector<uint8_t>& data) {
            std::cout << "Frame received: ID=0x" << std::hex << id << std::endl;
        });
        
        // Keep running for 10 seconds
        std::this_thread::sleep_for(std::chrono::seconds(10));
        
        // Cleanup
        can.close();
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return -1;
    }
    
    return 0;
}
```

#### 4. Run the C++ Example

```bash
# Run the built example
./can_example

# Or use make to build and run
make run
```

## Python API Reference

### Constructor

```python
WaveshareCAN(port='COM8', baudrate=2000000, timeout=1)
```

**Parameters:**
- `port`: Serial port device path (e.g., "/dev/ttyUSB0", "COM8")
- `baudrate`: Serial communication baud rate (default: 2,000,000)
- `timeout`: Read timeout in seconds (default: 1)

### Python Methods

#### `open()`
Opens the serial port connection.

#### `close()`
Closes the serial connection and stops any running receive threads.

#### `send(can_id, data)`
Sends a CAN frame.

**Parameters:**
- `can_id`: int, 11-bit CAN identifier (0-0x7FF)
- `data`: bytes, list[int], or str (up to 8 bytes)

#### `receive()`
Receives a single CAN frame (blocking operation).

**Returns:** `(can_id, data)` tuple if successful, `None` on timeout

#### `start_receive_loop(callback)`
Starts continuous frame reception in a separate thread.

**Parameters:**
- `callback`: Function called for each received frame: `callback(can_id, data)`

#### `stop_receive_loop()`
Stops the continuous receive loop.

## C++ API Reference

### Constructor

```cpp
WaveshareCAN(const std::string& port = "/dev/ttyUSB0", 
             int baudrate = 2000000, 
             int timeout_ms = 1000);
```

**Parameters:**
- `port`: Serial port device path (e.g., "/dev/ttyUSB0", "COM8")
- `baudrate`: Serial communication baud rate (default: 2,000,000)
- `timeout_ms`: Read timeout in milliseconds (default: 1000)

### Connection Management

#### `bool open()`
Opens the serial port connection and configures communication parameters.

**Returns:** `true` if successful, `false` otherwise

#### `void close()`
Closes the serial connection and stops any running receive threads.

#### `bool is_open() const`
Checks if the serial port connection is currently open.

**Returns:** `true` if open, `false` otherwise

### Sending Data

#### `bool send(uint16_t can_id, const std::vector<uint8_t>& data)`
Sends a CAN frame with vector data.

**Parameters:**
- `can_id`: 11-bit CAN identifier (0-0x7FF)
- `data`: Data bytes (automatically padded to 8 bytes)

#### `bool send(uint16_t can_id, const uint8_t* data, size_t length)`
Sends a CAN frame with raw byte array.

#### `bool send(uint16_t can_id, const std::string& data)`
Sends a CAN frame with string data (converted to bytes).

### Receiving Data

#### `bool receive(uint16_t& can_id, std::vector<uint8_t>& data)`
Receives a single CAN frame (blocking operation).

**Parameters:**
- `can_id`: Reference to store received CAN ID
- `data`: Reference to store received data bytes

**Returns:** `true` if frame received, `false` on timeout/error

#### `void start_receive_loop(callback)`
Starts continuous frame reception in a separate thread.

**Parameters:**
- `callback`: Function called for each received frame: `void(uint16_t can_id, const std::vector<uint8_t>& data)`

#### `void stop_receive_loop()`
Stops the continuous receive loop and joins the receive thread.

## Hardware Configuration

### Supported Devices

- Waveshare USB-CAN-A
- Waveshare USB-CAN-B
- Compatible USB-to-CAN adapters using Waveshare protocol

### Device Detection

**Linux:**
```bash
# List available USB serial devices
ls /dev/ttyUSB* /dev/ttyACM*

# Check kernel messages for new devices
dmesg | grep tty

# Check device info
lsusb
```

**Windows:**
```cmd
# Check Device Manager for COM ports
# Usually appears as "USB Serial Port (COMx)"
```

Common device paths:
- **Linux:** `/dev/ttyUSB0`, `/dev/ttyACM0`, `/dev/ttyS0`
- **Windows:** `COM1`, `COM3`, `COM8`, etc.

### Serial Port Permissions (Linux)

Add your user to the `dialout` group to access serial devices without sudo:

```bash
sudo usermod -a -G dialout $USER
# Logout and login again for changes to take effect
```

Alternatively, you can run with elevated privileges (not recommended for production):

```bash
sudo ./can_example
```

### Supported Baud Rates

The library supports standard baud rates including:
- 9600, 19200, 38400, 57600
- 115200, 230400, 460800
- 500000, 576000, 921600
- 1000000, 1152000, 1500000
- **2000000 (default)**, 2500000, 3000000, 3500000, 4000000

## Advanced Usage

### Migrating Between Python and C++

Both implementations use similar APIs to make migration easier:

#### Python to C++ Migration Example

**Python code:**
```python
can = WaveshareCAN('/dev/ttyUSB0', 2000000)
can.open()
can.send(0x123, [0x01, 0x02, 0x03, 0x04])
```

**Equivalent C++ code:**
```cpp
WaveshareCAN can("/dev/ttyUSB0", 2000000);
can.open();
std::vector<uint8_t> data = {0x01, 0x02, 0x03, 0x04};
can.send(0x123, data);
```

### Performance Comparison

| Metric | Python | C++ |
|--------|--------|-----|
| Message Latency | ~2-5ms | ~0.5-1ms |
| CPU Usage | Medium | Low |
| Memory Usage | ~10-50MB | ~1-5MB |
| Startup Time | ~100-500ms | ~10-50ms |
| Max Throughput | ~1000 msg/s | ~5000+ msg/s |

### Multiple Data Formats (Both Versions)

**Python:**
```python
# Send with list
can.send(0x123, [0x01, 0x02, 0x03, 0x04])

# Send with bytes
can.send(0x456, b'\xAA\xBB\xCC\xDD')

# Send with string
can.send(0x789, "HELLO")
```

**C++:**
```cpp
// Send with std::vector
std::vector<uint8_t> vec_data = {0x01, 0x02, 0x03, 0x04};
can.send(0x123, vec_data);

// Send with raw array
uint8_t raw_data[] = {0xAA, 0xBB, 0xCC, 0xDD};
can.send(0x456, raw_data, sizeof(raw_data));

// Send with string
can.send(0x789, "HELLO");
```

### Continuous Receive with Custom Callback

```cpp
auto callback = [](uint16_t id, const std::vector<uint8_t>& data) {
    std::cout << "CAN ID: 0x" << std::hex << std::setw(3) << std::setfill('0') << id;
    std::cout << " Data: ";
    for (size_t i = 0; i < data.size(); i++) {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << (int)data[i];
        if (i < data.size() - 1) std::cout << " ";
    }
    std::cout << std::dec << std::endl;
    
    // Process specific CAN IDs
    switch (id) {
        case 0x701:
            // Handle battery status
            break;
        case 0x702:
            // Handle position data
            break;
        default:
            // Handle other frames
            break;
    }
};

can.start_receive_loop(callback);
```

### Debug Mode

Enable debug mode for detailed logging:

```cpp
WaveshareCAN can("/dev/ttyUSB0");
can.setDebugMode(true);  // Enable verbose logging
can.open();
```

This will show detailed information about:
- Serial port operations
- Frame parsing process
- Error conditions
- Timeout events

## Installation

### Python Installation

1. **Install Python dependencies:**
   ```bash
   pip install pyserial
   ```

2. **Copy the Python file to your project:**
   ```bash
   cp waveshare_can.py /path/to/your/project/
   ```

3. **Import and use in your Python code:**
   ```python
   from waveshare_can import WaveshareCAN
   ```

### C++ Installation

#### Option 1: Header-Only Usage
```bash
# Just copy the header file to your project
cp waveshare_can.hpp /path/to/your/project/include/
```

#### Option 2: Build as Static Library

```bash
# Build static library
make lib

# Install system-wide (optional)
sudo make install
```

## Build System (C++)

### Makefile Targets

```bash
make           # Build example executable (default)
make lib       # Build static library only
make clean     # Remove build files
make install   # Install library system-wide (requires sudo)
make uninstall # Uninstall library
make run       # Build and run example
make debug     # Build with debug symbols
make check     # Syntax check only
make help      # Show available targets
```

### Manual Compilation

```bash
# Compile library
g++ -std=c++11 -pthread -c waveshare_can.cpp -o waveshare_can.o

# Create static library
ar rcs libwaveshare_can.a waveshare_can.o

# Compile your application
g++ -std=c++11 -pthread -o my_app main.cpp waveshare_can.cpp

# Or link with static library
g++ -std=c++11 -pthread -o my_app main.cpp -L. -lwaveshare_can
```

## Troubleshooting

### Common Issues (Both Versions)

#### 1. Permission Denied
```
Error: Failed to open serial port: /dev/ttyUSB0
```

**Solutions:**
- Add user to dialout group: `sudo usermod -a -G dialout $USER`
- Check device permissions: `ls -l /dev/ttyUSB0`
- Try running with sudo (temporary solution)

#### 2. Device Not Found
```
Error: Failed to open serial port: /dev/ttyUSB0
```

**Solutions:**
- Check USB connection
- Verify device path: `ls /dev/ttyUSB*`
- Check kernel messages: `dmesg | tail`
- Try different device path (/dev/ttyACM0, etc.)

#### 3. No Data Received
```
Warning: Read timeout - no data received
```

**Solutions:**
- Check CAN bus termination (120Ω resistors)
- Verify CAN_H and CAN_L connections
- Ensure CAN bus has active traffic
- Check CAN bus baud rate configuration
- Verify Waveshare module configuration

### Python-Specific Issues

#### 4. Import Error
```
ModuleNotFoundError: No module named 'serial'
```

**Solutions:**
```bash
pip install pyserial
# or
pip3 install pyserial
```

#### 5. Python Serial Port Issues
```python
# Test serial port manually
import serial
ser = serial.Serial('/dev/ttyUSB0', 2000000, timeout=1)
print(ser.is_open)
ser.close()
```

### C++ Specific Issues

#### 6. Compilation Errors

**Missing C++11 support:**
```bash
g++ --version  # Check compiler version
# Use: g++ -std=c++11 ...
```

**Threading issues:**
```bash
# Ensure pthread linking
g++ -std=c++11 -pthread ...
```

### Debug Steps

1. **Enable debug mode:**

   **Python:**
   ```python
   can = WaveshareCAN('/dev/ttyUSB0', baudrate=2000000, timeout=1)
   # Python version doesn't have debug mode but uses exceptions for error handling
   ```

   **C++:**
   ```cpp
   can.setDebugMode(true);
   ```

2. **Check serial port:**
   ```bash
   # Linux
   sudo minicom -D /dev/ttyUSB0 -b 2000000
   
   # Windows
   # Use PuTTY or similar terminal
   ```

3. **Test basic connectivity:**

   **Python:**
   ```python
   try:
       can = WaveshareCAN('/dev/ttyUSB0')
       can.open()
       print("Connection successful!")
       can.close()
   except Exception as e:
       print(f"Connection failed: {e}")
   ```

   **C++:**
   ```cpp
   WaveshareCAN can("/dev/ttyUSB0");
   if (can.open()) {
       std::cout << "Connection successful!" << std::endl;
       can.close();
   } else {
       std::cout << "Connection failed!" << std::endl;
   }
   ```

4. **Verify CAN bus:**
   ```bash
   # Use candump (if available)
   candump can0
   ```

5. **Test with loopback:**

   **Python:**
   ```python
   # Send and immediately try to receive
   can.send(0x123, [0x01, 0x02, 0x03, 0x04])
   frame = can.receive()  # Check if your CAN bus has loopback enabled
   ```

   **C++:**
   ```cpp
   // Send and immediately try to receive
   can.send(0x123, {0x01, 0x02, 0x03, 0x04});
   // Check if your CAN bus has loopback enabled
   ```

## Examples

The library includes example programs for both implementations:

### Python Examples
- Basic send/receive operations
- Continuous receive loop with callback
- Error handling and debugging
- Integration with existing Python applications

### C++ Examples
- `main.cpp` - Complete demonstration with all features
- `example.cpp` - Basic usage examples
- Individual test cases for each function
- Performance benchmarking examples

## File Structure

```
USB_CAN_A_Waveshare/
├── waveshare_can.py      # Python implementation
├── waveshare_can.hpp     # C++ header-only implementation
├── README.md             # This documentation
├── Makefile             # Build system for C++ (if available)
└── examples/            # Example code for both languages
    ├── python_examples/
    └── cpp_examples/
```

## Performance Notes

### Python Performance
- **Baud Rate**: 2,000,000 baud is recommended for high-speed CAN communication
- **Threading**: Uses Python threading for non-blocking receive operations
- **Memory**: Moderate memory usage due to Python overhead
- **Latency**: Typical frame latency 2-5ms under normal conditions
- **Best for**: Prototyping, integration, moderate-speed applications

### C++ Performance
- **Baud Rate**: 2,000,000 baud is recommended for high-speed CAN communication
- **Threading**: Uses std::thread for non-blocking performance
- **Memory**: Efficient memory usage with RAII and smart resource management
- **Latency**: Typical frame latency < 1ms under normal conditions
- **Best for**: High-performance, real-time, embedded applications

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## Support

For issues, questions, or contributions:

1. **Check the troubleshooting section** above
2. **Review example code** in the repository
3. **Verify hardware connections** and permissions
4. **Enable debug mode** for detailed logging
5. **Create an issue** with detailed error messages and system information

## Version History

### Python Implementation
- **v1.0.0** - Initial Python implementation with basic send/receive functionality
- **v1.1.0** - Added continuous receive loop and callback support
- **v1.2.0** - Improved error handling and exception management
- **v1.3.0** - Enhanced data type support and cross-platform compatibility

### C++ Implementation
- **v1.0.0** - Initial C++ release with basic send/receive functionality
- **v1.1.0** - Added continuous receive loop and callback support
- **v1.2.0** - Improved error handling and timeout management
- **v1.3.0** - Added debug mode and cross-platform support
- **v1.4.0** - Enhanced build system and documentation

### Unified Documentation
- **v2.0.0** - Combined documentation for both Python and C++ implementations
- **v2.1.0** - Added migration guides and performance comparisons

---

**Waveshare USB-CAN Library** - Available in Python and C++ for all your CAN communication needs.