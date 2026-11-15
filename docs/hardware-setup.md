# Hardware Setup

## Main hardware

| Component | Role |
|---|---|
| Raspberry Pi 4 Model B Rev 1.5 | Main computer |
| OV5647 Raspberry Pi Camera Module Rev 1.3 | Visual input |
| HC-SR04 × 3 | Front, left, and right proximity sensing |
| Arduino Uno | Step pulse and direction controller |
| TB6600 | NEMA 23 stepper driver |
| NEMA 23 | Drive motor |
| NEMA 17 | Separate steering mechanism actuator |
| 12 V supply | TB6600 motor-driver supply used in the prototype |

Check the actual labels and ratings on each component before wiring. The NEMA 17 steering mechanism is separate from the NEMA 23 drive system.

## Raspberry Pi ultrasonic GPIO mapping

Use BCM numbering.

| Sensor | TRIG | ECHO |
|---|---:|---:|
| Left | GPIO 23 | GPIO 24 |
| Front/centre | GPIO 17 | GPIO 27 |
| Right | GPIO 22 | GPIO 5 |

The sensors are read sequentially by `software/raspberry_pi/ultrasonic_sensors/ultrasonic.py` using gpiozero and system Python.

**ECHO voltage warning:** HC-SR04 ECHO outputs can be 5 V. Raspberry Pi GPIO is 3.3 V only. Use a correctly sized voltage divider or level shifter on every ECHO line. Never connect a 5 V ECHO signal directly to a Pi GPIO pin.

## Arduino to TB6600

The current test wiring is:

| Arduino Uno | TB6600 |
|---|---|
| D2 | PUL+ |
| D3 | DIR+ |
| GND | PUL- and DIR- |

ENA is currently disconnected. The TB6600 uses a separate 12 V supply. Connect the NEMA 23 motor to the driver's motor output terminals according to the driver's documentation. Do not power the motor from the Raspberry Pi or Arduino 5 V pin.

The Arduino connects to the Raspberry Pi over USB serial, typically `/dev/ttyACM0`, at 115200 baud.

## Before powering the system

- Verify all signal and power terminals against the actual driver markings.
- Check supply voltage, current rating, and polarity.
- Confirm TB6600 current and microstep settings for the motor.
- Verify the Raspberry Pi and driver grounding arrangement required by the interface.
- Keep drive wheels raised or mechanically disengaged during initial tests.
- Install and test an accessible physical emergency stop.
- Check motor direction at low risk before attaching the drive load.

Do not enable autonomous movement until the sensor readings, serial commands, watchdog stop, and emergency stop have been tested. Store checked diagrams under `hardware/electronics/circuit-diagrams/` and `docs/wiring-diagrams/`.