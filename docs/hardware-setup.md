# Hardware Setup

## Main components

- Raspberry Pi 4 Model B
- Raspberry Pi Camera Module (OV5647)
- Three HC-SR04 ultrasonic sensors
- Arduino Uno
- TB6600 stepper motor driver
- NEMA 23 stepper motor
- Suitable regulated power supplies and wiring

## Ultrasonic sensor GPIO mapping

The current Raspberry Pi setup uses BCM numbering:

| Sensor | TRIG | ECHO |
|---|---:|---:|
| Left | GPIO 23 | GPIO 24 |
| Centre | GPIO 17 | GPIO 27 |
| Right | GPIO 22 | GPIO 5 |

**Echo voltage warning:** HC-SR04 ECHO outputs can be 5 V. Raspberry Pi GPIO is 3.3 V only. Use a correctly sized voltage divider or level shifter on every ECHO line. Do not connect a 5 V ECHO signal directly to a Pi GPIO pin.

## Motor control

The current prototype uses an Arduino Uno to generate the control signals for a TB6600 driver connected to a NEMA 23 stepper motor. The motor supply and driver wiring must follow the specific driver's documentation. Do not power the motor from the Raspberry Pi or Arduino 5 V pin.

## Before powering the system

- Verify common ground and signal wiring where required by the driver interface.
- Check supply voltage and current ratings.
- Confirm stepper-driver current and microstep settings.
- Keep the drive wheels raised or mechanically disengaged during initial tests.
- Add an accessible emergency stop and test it before autonomous motion.

Add verified wiring diagrams and photographs under `hardware/electronics/` and `docs/wiring-diagrams/`.
