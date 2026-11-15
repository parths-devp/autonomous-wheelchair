import threading
import time

import serial


SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
HEARTBEAT_INTERVAL_SECONDS = 0.2


def main():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as connection:
        time.sleep(2)
        connection.reset_input_buffer()

        current_command = ["S"]
        command_lock = threading.Lock()
        stop_heartbeat = threading.Event()

        def heartbeat():
            while not stop_heartbeat.wait(HEARTBEAT_INTERVAL_SECONDS):
                with command_lock:
                    if current_command[0] in {"F", "B"}:
                        connection.write(b"H")
                        connection.flush()

        heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
        heartbeat_thread.start()

        print("Commands: F = forward, B = backward, S = stop, Q = quit")

        try:
            while True:
                command = input("Command: ").strip().upper()

                if command == "Q":
                    with command_lock:
                        connection.write(b"S")
                        connection.flush()
                        current_command[0] = "S"
                    break

                if command in {"F", "B", "S"}:
                    with command_lock:
                        connection.write(command.encode("ascii"))
                        connection.flush()
                        current_command[0] = command
                    print("Sent:", command)
                else:
                    print("Enter F, B, S, or Q.")

        finally:
            with command_lock:
                connection.write(b"S")
                connection.flush()
                current_command[0] = "S"

            stop_heartbeat.set()
            heartbeat_thread.join(timeout=1)


if __name__ == "__main__":
    main()
