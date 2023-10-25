const int stepPin = 6; //6
const int dirPin = 4; //4
const int stepPin2 = 5; //5
const int dirPin2 = 2; //2
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
      stepv(1);
    } else if (vCommand == 'D') {
      digitalWrite(dirPin2, LOW);
      stepv(-1);
    }
  }
}


long long hswT = 0;
boolean hstate = 0;
void steph() {
  const int n =5 * 1000;
  if (hswT < (micros() - n)) {
    hstate ^= 1;
    hswT = micros();

  }
  digitalWrite(stepPin, hstate);
}
long long vswT = 0;
boolean vstate = 0;
int total = 0;
void stepv(int dir) {
  delay(1);
  return;
  if (abs(dir) > 2) {
    return;
  }

  const int n = 100 * 1000;
  if (vswT < (micros() - n)) {
    vstate ^= 1;
    vswT = micros();

  }
  digitalWrite(stepPin2, vstate);
    total += dir; // assume 2deg / step
}
