# Circuit diagrams

Store the editable circuit source and exported wiring diagrams for the Raspberry Pi, sensors, Arduino, TB6600, and power supplies here.

## Current prototype connections

The Arduino Uno communicates with the Raspberry Pi over USB serial. The motor-control sketch uses:

| Arduino Uno | TB6600 |
|---|---|
| D2 | PUL+ |
| D3 | DIR+ |
| GND | PUL- and DIR- |

ENA is not connected in the current test wiring. The TB6600 has a separate 12 V supply, and the NEMA 23 motor connects to the driver's motor-output terminals. Verify the terminal labels on the actual driver before connecting power.

The three HC-SR04 sensors connect to the Raspberry Pi using BCM pins documented in \`docs/hardware-setup.md\`. Every ECHO signal requires a voltage divider or level shifter.

Add a complete power and ground diagram before full-system operation. Do not power the stepper motor from the Raspberry Pi or Arduino 5 V rail.