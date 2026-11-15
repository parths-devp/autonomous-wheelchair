import time

import serial


SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200


def main():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as connection:
        time.sleep(2)
        connection.reset_input_buffer()
        print("Commands: F = forward, B = backward, S = stop, Q = quit")

        while True:
            command = input("Command: ").strip().upper()

            if command == "Q":
                connection.write(b"S")
                connection.flush()
                break

            if command in {"F", "B", "S"}:
                connection.write(command.encode("ascii"))
                connection.flush()
                print("Sent:", command)
            else:
                print("Enter F, B, S, or Q.")


if __name__ == "__main__":
    main()
