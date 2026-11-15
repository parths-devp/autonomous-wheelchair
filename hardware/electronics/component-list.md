# Component List

| Component | Quantity | Role | Current details |
|---|---:|---|---|
| Raspberry Pi 4 Model B Rev 1.5 | 1 | Main computer | aarch64 development platform |
| OV5647 Raspberry Pi Camera Module Rev 1.3 | 1 | Visual input | Picamera2 camera |
| HC-SR04 | 3 | Proximity sensing | Front, left, and right |
| Arduino Uno | 1 | Motor interface | USB serial command receiver |
| TB6600 stepper driver | 1 | Drive motor driver | 12 V supply used in prototype test |
| NEMA 23 stepper motor | 1 | Drive motor | Four-wire motor |
| NEMA 17 stepper motor | 1 | Steering actuator | Separate gear-driven steering mechanism |
| PLA printed gears | 1 set | Steering transmission | 15 mm face width; 15% rectilinear infill used for the discussed print |
| Power supplies | As required | System power | Confirm exact voltage/current ratings from labels |

## Motor interface wiring

The current Arduino test wiring assigns D2 to TB6600 PUL+, D3 to DIR+, and Arduino GND to PUL- and DIR-. ENA is disconnected. The Pi communicates with the Uno over USB serial.

## Items to complete

Record the exact NEMA 23 and NEMA 17 model numbers, TB6600 current/microstep switch settings, power-supply ratings, wiring gauge, connector types, fasteners, and final sensor mounting dimensions from the physical prototype. Do not infer electrical ratings from component family names.