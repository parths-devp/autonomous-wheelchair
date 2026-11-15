import json
import time
from pathlib import Path

import serial


SENSOR_FILE = Path("/dev/shm/ultrasonic_distances.json")
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

STOP_DISTANCE_CM = 15.0
CLEAR_DISTANCE_CM = 25.0
SENSOR_TIMEOUT_SECONDS = 5.0
LOOP_INTERVAL_SECONDS = 0.1


def read_front_distance():
    try:
        with SENSOR_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        timestamp = float(data["timestamp"])
        distance = float(data["front_cm"])

        if time.time() - timestamp > SENSOR_TIMEOUT_SECONDS:
            return None

        if distance <= 0:
            return None

        return distance
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None


def send_command(connection, command, current_command):
    if command != current_command:
        connection.write(command.encode("ascii"))
        connection.flush()
        print("Motor command:", command)
        return command

    return current_command


def main():
    current_command = "S"

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as connection:
        time.sleep(2)
        connection.reset_input_buffer()
        connection.write(b"S")
        connection.flush()
        print("Obstacle motor controller started.")

        while True:
            distance = read_front_distance()

            if distance is None:
                current_command = send_command(connection, "S", current_command)
                print("Front sensor data invalid or stale. Motor stopped.")
            elif distance <= STOP_DISTANCE_CM:
                current_command = send_command(connection, "S", current_command)
                print(f"Obstacle at {distance:.1f} cm. Motor stopped.")
            elif distance >= CLEAR_DISTANCE_CM:
                current_command = send_command(connection, "F", current_command)
                print(f"Path clear at {distance:.1f} cm. Forward enabled.")
            else:
                print(f"Maintaining current state at {distance:.1f} cm.")

            if current_command in {"F", "B"}:
                connection.write(b"H")
                connection.flush()

            time.sleep(LOOP_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping motor controller.")
