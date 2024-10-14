import serial
import time

import serial.tools.list_ports
print("Available ports:")
for port in serial.tools.list_ports.comports():
    print(port.device)

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)

def send_command(command):
    arduino.reset_input_buffer()
    arduino.write(bytes(command + '\n', 'utf-8'))
    time.sleep(0.5)

def read_response():
    response = ""
    start_time = time.time()
    while True:
        if arduino.inWaiting() > 0:
            response_line = arduino.readline().decode('utf-8').rstrip()
            if response_line:
                response += response_line + "\n"
        if time.time() - start_time > 3:
            break
    return response.strip()

while True:
    user_input = input("Enter a 5-digit number: ")

    if len(user_input) == 5 and user_input.isdigit():
        send_command(user_input)

        time.sleep(0.5)
        response = read_response()

        if response:
            print("Arduino Response:\n", response)
        else:
            print("No Response from Arduino.")
    else:
        print("Please enter a 5-digit number.")
