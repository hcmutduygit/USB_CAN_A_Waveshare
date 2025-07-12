import serial
import time
import struct

def read_serial_data(port='/dev/ttyUSB1', baudrate=2000000, timeout=1):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout
        )
        
        print(f"Đã kết nối với cổng {port} tại tốc độ {baudrate} baud")
        
        while True:
            if ser.in_waiting > 0:
                raw_data = ser.read(ser.in_waiting)
                print(f"Dữ liệu CAN (hex): {raw_data.hex()}")
                print(f"Topic: {raw_data.hex()[4:8]}")
            
            time.sleep(0.01)
            
    except serial.SerialException as e:
        print(f"Lỗi kết nối serial: {e}")
        print("Hãy kiểm tra cổng hoặc quyền truy cập (nhóm 'dialout').")
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình bởi người dùng")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Đã đóng cổng serial")


if __name__ == "__main__":
    read_serial_data(port='/dev/ttyUSB0', baudrate=2000000)