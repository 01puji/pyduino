# include <Servo.h>
Servo myServo;
String str = "";

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
  Serial.println("5자리 숫자 입력하세요: ");
}

void loop() {
  if(Serial.available() > 0){
    str = Serial.readStringUntil('\n');

    if(str.length() == 5){
      String coffee = str.substring(1, 2);
      String cola = str.substring(2, 5);

      Serial.print("입력한 숫자 = ");
      Serial.println(str);

      int degree_angle = cola.toInt();
      int currentAngle = myServo.read();

      if (coffee == "0") {
        Serial.println("[motor rotation = left]");
        int targetAngle = currentAngle + degree_angle;
        targetAngle = constrain(targetAngle, 0, 180);
        myServo.write(targetAngle);
      } else if (coffee == "1") {
        Serial.println("[motor rotation = right]");
        int targetAngle = currentAngle - degree_angle;
        targetAngle = constrain(targetAngle, 0, 180);
        myServo.write(targetAngle);
      }

delay(2000);

for(int i = 0; i <= degree_angle; i++){
  Serial.print(i);
  Serial.println("도 회전");
  delay(10);
}
delay(1000);
    }else {
      Serial.println("입력한 숫자가 올바르지 않습니다. 5자리 숫자를 입력하세요.");
    }
 }
}
