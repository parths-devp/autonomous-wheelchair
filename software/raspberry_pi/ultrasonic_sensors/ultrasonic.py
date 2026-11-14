
import RPi.GPIO as GPIO
import time
import json
import os


frontTrig, frontEcho = 17, 27
rightTrig, rightEcho = 22, 5
leftTrig, leftEcho = 23, 24

DATA_FILE = "/dev/shm/ultrasonic_distances.json"

obstacleDistance = 15.0
numberOfReadings = 10

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for trig, echo in [
    (frontTrig, frontEcho),
    (rightTrig, rightEcho),
    (leftTrig, leftEcho)
]:
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trig, GPIO.LOW)


def getDistance(trigPin, echoPin):

    GPIO.output(trigPin, GPIO.LOW)
    time.sleep(0.000002)

    GPIO.output(trigPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigPin, GPIO.LOW)

    startTime = time.monotonic()

    while GPIO.input(echoPin) == GPIO.LOW:
        if time.monotonic() - startTime > 0.03:
            return -1

    pulseStart = time.monotonic()

    while GPIO.input(echoPin) == GPIO.HIGH:
        if time.monotonic() - pulseStart > 0.03:
            return -1

    pulseEnd = time.monotonic()

    return (pulseEnd - pulseStart) * 34300 / 2.0


def getAverageDistance(trigPin, echoPin):

    total = 0
    validCount = 0

    for _ in range(numberOfReadings):

        distance = getDistance(trigPin, echoPin)

        if distance > 0:
            total += distance
            validCount += 1

        time.sleep(0.05)

    if validCount == 0:
        return -1

    return total / validCount


def saveReadings(front, right, left):

    data = {
        "front_cm": round(front, 1),
        "right_cm": round(right, 1),
        "left_cm": round(left, 1),
        "timestamp": time.time()
    }

    temp_file = DATA_FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(data, f)

    os.replace(temp_file, DATA_FILE)


try:

    print("3-Sensor Ultrasonic Monitor Started")
    print("Writing readings to:", DATA_FILE)

    while True:

        

        frontDistance = getAverageDistance(
            frontTrig, frontEcho
        )
        time.sleep(0.06)

        rightDistance = getAverageDistance(
            rightTrig, rightEcho
        )
        time.sleep(0.06)

        leftDistance = getAverageDistance(
            leftTrig, leftEcho
        )

        saveReadings(
            frontDistance,
            rightDistance,
            leftDistance
        )

        print(
            f"FRONT: {frontDistance:.1f} cm | "
            f"RIGHT: {rightDistance:.1f} cm | "
            f"LEFT: {leftDistance:.1f} cm"
        )

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping sensors...")

finally:
    GPIO.cleanup()

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    print("GPIO cleaned up.")
