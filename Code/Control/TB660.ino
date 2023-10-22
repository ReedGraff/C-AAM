const int stepPin = 5;
const int dirPin = 2;
const int stepPin2 = 6;
const int dirPin2 = 4;
const int SHT_PIN = 10;
unsigned long shootPreviousTime = 0;
unsigned long currentTime = 0;
unsigned long hPreviousTime = 0;
unsigned long vPreviousTime = 0;
const int moveDuration = 200; // 200ms

char hCommand = ' '; // Initialize with a space
char vCommand = ' '; // Initialize with a space

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(SHT_PIN, OUTPUT);
  digitalWrite(SHT_PIN, HIGH);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming command

    if ( command == 'S') {
      digitalWrite(SHT_PIN, LOW);
      shootPreviousTime = millis();
    }
    if (command == 'R' || command == 'L') {
      hCommand = command; // Update the last command if it's 'R' or 'L'
      hPreviousTime = millis();
    }
    if (command == 'U' || command == 'D') {
      vCommand = command; // Update the last command if it's 'U' or 'D'
      vPreviousTime = millis();
    }

  }

  
  if (shootPreviousTime < ( millis() - moveDuration)) {
    digitalWrite(SHT_PIN, HIGH);
  }

  if (hPreviousTime >  (millis() - moveDuration)) {
    // Execute the last command
    if (hCommand == 'R') {
      digitalWrite(dirPin, HIGH); // Set the direction to move right
      steph();
    } else if (hCommand == 'L') {
      digitalWrite(dirPin, LOW); // Set the direction to move left
      steph();
    }
  }
  if (vPreviousTime >  (millis() - moveDuration)) {
    if (vCommand == 'U') {
      digitalWrite(dirPin2, HIGH);
      stepv();
    } else if (vCommand == 'D') {
      digitalWrite(dirPin2, LOW);
      stepv();
    }
  }
}

void steph() {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(8000);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(8000);
}
void stepv() {
  digitalWrite(stepPin2, HIGH);
  delayMicroseconds(8000);
  digitalWrite(stepPin2, LOW);
  delayMicroseconds(8000);
}
