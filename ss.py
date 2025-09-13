

bool buttonPressed = false;
bool buttonHandled = false;

void setup() {
  pinMode(25, OUTPUT);
  pinMode(26, OUTPUT);
  pinMode(27, OUTPUT);
  pinMode(14, INPUT_PULLUP);
  
  digitalWrite(redPin, LOW);
  digitalWrite(yellowPin, LOW);
  digitalWrite(greenPin, LOW);
}

void loop() {
  digitalWrite(redPin, HIGH);
  
  for (int i = 0; i < 70; i++) {
    delay(100);
    checkButton();
    if (buttonPressed) {
      digitalWrite(25, LOW);
      handleButtonPress();
      return;
    }
  }
  
  digitalWrite(25, LOW);
  digitalWrite(26, HIGH);
  
  for (int i = 0; i < 30; i++) {
    delay(100);
    checkButton();
    if (buttonPressed) {
      digitalWrite(26, LOW);
      handleButtonPress();
      return;
    }
  }
  
  digitalWrite(26, LOW);
  
  for (int i = 0; i < 3; i++) {
    digitalWrite(26, HIGH);
    delay(500);
    digitalWrite(26, LOW);
    delay(500);
    
    checkButton();
    if (buttonPressed) {
      handleButtonPress();
      return;
    }
  }
  
  digitalWrite(27, HIGH);
  
  for (int i = 0; i < 70; i++) {
    delay(100);
    checkButton();
    if (buttonPressed) {
      digitalWrite(27, LOW);
      handleButtonPress();
      return;
    }
  }
  
  digitalWrite(27, LOW);
}

void checkButton() {
  if (digitalRead() == LOW && !buttonHandled) {
    buttonPressed = true;
    buttonHandled = true;
  }
  
  if (digitalRead() == HIGH) {
    buttonHandled = false;
  }
}

void handleButtonPress() {
  digitalWrite(25, LOW);
  digitalWrite(27, LOW);
  
  for (int i = 0; i < 3; i++) {
    digitalWrite(26, HIGH);
    delay(500);
    digitalWrite(26, LOW);
    delay(500);
  }
  
  digitalWrite(27, HIGH);
  delay(7000);
  digitalWrite(27, LOW);
  
  buttonPressed = false;
}