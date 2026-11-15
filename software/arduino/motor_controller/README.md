# Arduino motor controller

Firmware: `motor_controller.ino`

The sketch receives single-character serial commands and generates STEP pulses for a TB6600 driver.

## Pin assignments

| Arduino Uno | TB6600 terminal |
|---|---|
| D2 | PUL+ |
| D3 | DIR+ |
| GND | PUL- and DIR- |

ENA is left disconnected in the current wiring. The TB6600 uses a separate 12 V supply. Confirm the driver's input wiring and current/microstep settings against its actual documentation.

## Serial protocol

- Baud rate: 115200
- `F`: forward
- `B`: backward
- `S`: stop

The current sketch uses an 800 microsecond STEP interval and a 5 microsecond STEP pulse. Direction is set HIGH for forward and LOW for backward. If the physical direction is reversed, verify the motor wiring and direction convention with the wheels raised before changing the code.

## Upload and test

1. Open `motor_controller.ino` in Arduino IDE.
2. Select Arduino Uno and the correct serial port.
3. Upload the sketch.
4. Keep the drive wheels raised or mechanically disengaged.
5. Run `software/raspberry_pi/motor_control/motor_test.py` from the Raspberry Pi.
6. Test F, B, and S separately and verify the physical emergency stop.

The firmware and Pi serial utility are integration-stage code. Recheck timing, direction, driver current, and stop response on the actual hardware.