import json
import os
import time

from gpiozero import DigitalInputDevice, DigitalOutputDevice


FRONT_TRIG, FRONT_ECHO = 17, 27
RIGHT_TRIG, RIGHT_ECHO = 22, 5
LEFT_TRIG, LEFT_ECHO = 23, 24

DATA_FILE = "/dev/shm/ultrasonic_distances.json"
NUMBER_OF_READINGS = 10
ECHO_TIMEOUT = 0.03

sensors = {
    "front": (
        DigitalOutputDevice(FRONT_TRIG, initial_value=False),
        DigitalInputDevice(FRONT_ECHO, pull_up=False),
    ),
    "right": (
        DigitalOutputDevice(RIGHT_TRIG, initial_value=False),
        DigitalInputDevice(RIGHT_ECHO, pull_up=False),
    ),
    "left": (
        DigitalOutputDevice(LEFT_TRIG, initial_value=False),
        DigitalInputDevice(LEFT_ECHO, pull_up=False),
    ),
}


def get_distance(trigger, echo):
    trigger.off()
    time.sleep(0.000002)
    trigger.on()
    time.sleep(0.00001)
    trigger.off()

    if not echo.wait_for_active(timeout=ECHO_TIMEOUT):
        return -1.0

    pulse_start = time.perf_counter()

    if not echo.wait_for_inactive(timeout=ECHO_TIMEOUT):
        return -1.0

    pulse_end = time.perf_counter()
    return (pulse_end - pulse_start) * 34300.0 / 2.0


def get_average_distance(trigger, echo):
    readings = []

    for _ in range(NUMBER_OF_READINGS):
        distance = get_distance(trigger, echo)

        if distance > 0:
            readings.append(distance)

        time.sleep(0.05)

    if not readings:
        return -1.0

    return sum(readings) / len(readings)


def save_readings(front, right, left):
    data = {
        "front_cm": round(front, 1),
        "right_cm": round(right, 1),
        "left_cm": round(left, 1),
        "timestamp": time.time(),
    }

    temporary_file = DATA_FILE + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file)

    os.replace(temporary_file, DATA_FILE)


try:
    print("3-Sensor Ultrasonic Monitor Started")
    print("Writing readings to:", DATA_FILE)

    while True:
        front_distance = get_average_distance(*sensors["front"])
        time.sleep(0.06)

        right_distance = get_average_distance(*sensors["right"])
        time.sleep(0.06)

        left_distance = get_average_distance(*sensors["left"])

        save_readings(front_distance, right_distance, left_distance)

        print(
            f"FRONT: {front_distance:.1f} cm | "
            f"RIGHT: {right_distance:.1f} cm | "
            f"LEFT: {left_distance:.1f} cm"
        )

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping sensors...")

finally:
    for trigger, echo in sensors.values():
        trigger.close()
        echo.close()

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    print("Sensor devices closed.")
