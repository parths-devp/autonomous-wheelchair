# Wiring diagrams

Store exported diagrams and editable source files for the wheelchair electrical system here.

## Required diagrams

- Raspberry Pi to three HC-SR04 sensors, including all ECHO voltage dividers.
- Raspberry Pi USB connection to Arduino Uno.
- Arduino Uno to TB6600 STEP, DIR, and ground terminals.
- TB6600 motor outputs to the NEMA 23 motor and the separate motor power supply.
- Full system power distribution and emergency-stop arrangement.

## Known signal assignments

| Connection | Assignment |
|---|---|
| Front HC-SR04 TRIG / ECHO | BCM 17 / BCM 27 |
| Right HC-SR04 TRIG / ECHO | BCM 22 / BCM 5 |
| Left HC-SR04 TRIG / ECHO | BCM 23 / BCM 24 |
| Arduino STEP signal | D2 to TB6600 PUL+ |
| Arduino DIR signal | D3 to TB6600 DIR+ |
| TB6600 PUL- and DIR- | Arduino GND |
| Arduino serial link | USB, typically `/dev/ttyACM0`, 115200 baud |

The current test wiring leaves ENA disconnected. Verify the actual TB6600 terminal labels and the specific module's wiring requirements before powering it. All HC-SR04 ECHO lines require 3.3 V-safe level conversion.

Only add a diagram as verified after checking it against the physical wiring. Include a revision date and hardware version.