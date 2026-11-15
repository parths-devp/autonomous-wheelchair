const byte STEP_PIN = 2;
const byte DIR_PIN = 3;
const unsigned long STEP_INTERVAL_US = 800;
const unsigned long STEP_PULSE_US = 5;
const unsigned long COMMAND_TIMEOUT_US = 750000;

bool motorRunning = false;
bool stepIsHigh = false;
unsigned long lastStepRise = 0;
unsigned long stepRiseTime = 0;
unsigned long lastCommandTime = 0;

void stopMotor() {
  motorRunning = false;
  stepIsHigh = false;
  digitalWrite(STEP_PIN, LOW);
}

void setMotorDirection(bool forward) {
  stopMotor();
  digitalWrite(DIR_PIN, forward ? HIGH : LOW);
  lastStepRise = micros();
  lastCommandTime = lastStepRise;
  motorRunning = true;
}

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(STEP_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);
  Serial.begin(115200);
}

void loop() {
  while (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'F' || command == 'f') {
      setMotorDirection(true);
    } else if (command == 'B' || command == 'b') {
      setMotorDirection(false);
    } else if (command == 'S' || command == 's') {
      stopMotor();
    } else if (command == 'H' || command == 'h') {
      lastCommandTime = micros();
    }
  }

  unsigned long now = micros();

  if (motorRunning && now - lastCommandTime > COMMAND_TIMEOUT_US) {
    stopMotor();
  }

  if (!motorRunning) {
    return;
  }

  if (stepIsHigh && now - stepRiseTime >= STEP_PULSE_US) {
    digitalWrite(STEP_PIN, LOW);
    stepIsHigh = false;
  }

  if (!stepIsHigh && now - lastStepRise >= STEP_INTERVAL_US) {
    digitalWrite(STEP_PIN, HIGH);
    stepIsHigh = true;
    stepRiseTime = now;
    lastStepRise = now;
  }
}
