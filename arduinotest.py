import serial, time

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)  # let Arduino reset

# Send test commands
for msg in ["HELLO", "PING", "XYZ"]:
    ser.write((msg + "\n").encode())
    reply = ser.readline().decode().strip()
    print(f"Sent: {msg}  |  Received: {reply}")
    time.sleep(0.5)

ser.close()
