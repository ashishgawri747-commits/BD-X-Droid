import serial, time

# open UART connected to Arduino
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)   # wait for Arduino to reset

while True:
    angle = input("Enter servo angle (0-180): ")
    if not angle:
        break
    ser.write(f"ANGLE:{angle}\n".encode())
    print(f"Sent -> ANGLE:{angle}")
