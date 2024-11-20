import serial
import time
import speech_recognition as sr
import re

import serial.tools.list_ports
print("Available ports:")
for port in serial.tools.list_ports.comports():
    print(port.device)
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)

recognizer = sr.Recognizer()

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

def process_voice_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
          audio = recognizer.listen(source)
          text = recognizer.recognize_google(audio, language="ko-KR")
          print(f"You said: {text}")

          if"왼쪽으로" in text:
            angle = extract_angle(text)
            if angle is not None:
              return f"10{angle:03}"
          elif "오른쪽으로" in text:
            angle = extract_angle(text)
            if angle is not None:
              return f"11{angle:03}"
          else:
            print("인식할 수 없는 명령입니다, 다시 시도하십시오.")
            return None
        except sr.UnknownValueError:
          print("인식할 수 없는 명령입니다, 다시 시도하십시오.。")
          return None
        except sr.RequestError as e:
          print(f"음성 인식 요청 오류：{e}")
        return None

def extract_angle(text):
    import re
    match = re.search(r"(\d+)도", text)
    if match:
        angle = int(match.group(1))
        if 0 <= angle <= 180:
            return angle
            print("잘못된 회전 각도입니다, 다시 시도하십시오.")
    print("유효 각도를 찾을 수 없습니다. 범위를 벗어났습니다（1-180）。")
    return None

print("1. 음성 모드")
print("2. 명령 모드")

while True:
  mode = input("모드를 선택해 주세요（1/2）：")
  if mode in ("1", "2"):
      print(f"모드 {mode}이(가) 선택되었습니다. 메인 루프에 들어갑니다：")
      break
  else:
      print("입력이 잘못되었습니다. 다시 선택하십시오.")

while True:
    print(f"현재 모드：{mode}")
    if mode == "1":
      command = process_voice_command()
      if command:
          print(f"인코딩된 명령：{command}")
          send_command(command)
          response = read_response()
          if response:
              print("Arduino Response:\n", response)
          else:
              print("No response from Arduino")
    elif mode == "2":
      user_input = input("명령어를 입력하십시오：")
      if len(user_input) == 5 and user_input.isdigit():
          send_command(user_input)
          response = read_response()
          if response:
              print("Arduino Response:\n", response)
          else:
              print("No response from Arduino")
      else:
          print("Please enter a 5-digit number.")
    else:
        print("Invalid mode. Please choose 1 or 2.")
