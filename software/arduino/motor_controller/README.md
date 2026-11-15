# Arduino motor controller

Firmware: `motor_controller.ino`

The sketch receives serial commands and generates STEP pulses for a TB6600 driver.

## Pin assignments

| Arduino Uno | TB6600 terminal |
|---|---|
| D2 | PUL+ |
| D3 | DIR+ |
| GND | PUL- and DIR- |

ENA is disconnected in the current test wiring. The TB6600 uses a separate 12 V supply. Confirm the driver's input wiring, current setting, and microstep setting against its documentation.

## Serial protocol

- Baud rate: 115200
- `F`: forward
- `B`: backward
- `S`: stop
- `H`: heartbeat while motion is active

The current sketch uses an 800 microsecond STEP interval and a 5 microsecond STEP pulse. Direction is HIGH for forward and LOW for backward. If the physical direction is reversed, verify the motor wiring and direction convention with the wheels raised.

The Arduino stops the motor if no heartbeat is received for 750 ms while moving. The Pi motor-control scripts send a heartbeat every 200 ms during manual motion or every control-loop iteration during automatic operation.

## Upload and test

1. Open `motor_controller.ino` in Arduino IDE.
2. Select Arduino Uno and the correct serial port.
3. Upload the sketch.
4. Keep the drive wheels raised or mechanically disengaged.
5. Run `software/raspberry_pi/motor_control/motor_test.py`.
6. Test F, B, S, and loss of heartbeat. Verify the physical emergency stop.

The firmware and Pi serial utilities are integration-stage code. Recheck timing, direction, driver current, stop response, and watchdog behaviour on the actual hardware.